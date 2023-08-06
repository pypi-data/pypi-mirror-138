#!python
import os
import sys
import json
import logging
import argparse
import subprocess
from webbrowser import get
import botocore
import boto3
from tqdm import tqdm
from boto3.s3.transfer import TransferConfig
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

GB = 1024 ** 3
MULTIPART_THRESHOLD = GB/100
MAX_CONCURRENCY = 10
NUM_DOWNLOAD_ATTEMPTS = 10
USE_THREADS = True

VISIBILITY_TIMEOUT = 43200
DELAY_SECONDS = 0

class bcolors:
    WARNING = '\033[93m'
    ENDC = '\033[0m'

class Config:
    def __init__(self, path, file):
        self.path = path
        self.file = os.path.join(path,file)
        self.config = {}

        self.load()

    def save(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        with open(self.file, 'w') as config_file:
            json.dump(self.config, config_file)
        return

    def load(self):
        if os.path.isfile(self.file):
            with open(self.file) as config_file:
                self.config = json.load(config_file)
                return True
        else:
            return False            

    @property
    def region(self):
        return self.config.get('region', None)

    @region.setter
    def region(self, region):
        self.config['region'] = region

    @property
    def queue(self):
        return self.config.get('queue', None)

    @queue.setter
    def queue(self, queue):
        self.config['queue'] = queue

    @property
    def bucket(self):
        return self.config.get('bucket', None)

    @bucket.setter
    def bucket(self, bucket):
        self.config['bucket'] = bucket

    @property
    def prefix(self):
        return self.config.get('prefix', None)

    @prefix.setter
    def prefix(self, prefix):
        self.config['prefix'] = prefix

    @property
    def profile(self):
        return self.config.get('profile', None)

    @profile.setter
    def profile(self, profile):
        self.config['profile'] = profile

config = Config(os.path.join(os.path.expanduser('~'),'.s3copy'), 's3copy_config.json')


class Bucket:
    def __init__(self, session, bucket_name, prefix):
        self.s3 = session.client('s3')
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.config = TransferConfig(multipart_threshold = MULTIPART_THRESHOLD, 
                                     max_concurrency = MAX_CONCURRENCY,
                                     use_threads = USE_THREADS,
                                     num_download_attempts = NUM_DOWNLOAD_ATTEMPTS)

        self.__create()
        self.put_lifecycle_configuration({
            'Rules': [{
                'Expiration': {
                    'Days':1
                },
                'ID':'s3copy',
                'Filter':{'Tag':{'Key':'s3copy','Value':'delete'}},
                'Status':'Enabled'
            }]
        })
        
    def __create(self):
        #Create bucket if it doesn't exist
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == '404':
                try:
                    self.s3.create_bucket(Bucket=self.bucket_name)
                except botocore.exceptions.ClientError as error:
                    logger.error(error)                    
            else:
                logger.error(error)                
            
    def put_lifecycle_configuration(self, lifecyle_configuration):
        try:
            self.s3.put_bucket_lifecycle_configuration(
                Bucket = self.bucket_name,
                LifecycleConfiguration = lifecyle_configuration)
        except botocore.exceptions.ClientError as error:
            logger.error(error)
        
    def upload_file(self, file_name, show_progress=False):
        try:
            params = {
                'Filename': file_name,
                'Bucket': self.bucket_name, 
                'Key': f'{self.prefix}/{file_name}',                     
                'ExtraArgs': {'Metadata':{'s3copy':'delete'}},
                'Config': self.config}

            if show_progress:
                file_size = os.stat(file_name).st_size                

                with tqdm(total=file_size, unit="B", unit_scale=True, desc='Sending file') as pbar:
                    params['Callback'] = lambda bytes_transferred: pbar.update(bytes_transferred)
                    self.s3.upload_file(**params)                                
            else:                            
                self.s3.upload_file(**params)

        except botocore.exceptions.ClientError as error:
            logger.error(error)
            raise Exception(f"Unable to upload file: {file_name}")

    def download_file(self, file_name, show_progress=False, delete=True):
        try:
            path = os.path.dirname(file_name)
            
            if len(path) > 0 and not os.path.exists(path):     
                try:
                    os.makedirs(path)
                except OSError:
                    logger.debug('It seems another thread created {path} before')
                    pass

            params = {
                'Bucket': self.bucket_name, 
                'Key': f'{self.prefix}/{file_name}', 
                'Filename': file_name, 
                'Config': self.config}

            if show_progress:
                object_size = self.s3.head_object(Bucket=params['Bucket'], Key=params['Key'])["ContentLength"]            
                with tqdm(total=object_size, unit="B", unit_scale=True, desc='Downloading file') as pbar:
                    params['Callback'] = lambda bytes_transferred: pbar.update(bytes_transferred)
                    self.s3.download_file(**params)
            
            else:
                self.s3.download_file(**params)

            if delete:
                self.delete_file(file_name)

        except botocore.exceptions.ClientError as error:                  
            if error.response['Error']['Code'] == '404':
                logger.warning(f'{self.prefix}/{file_name} not found on S3')
            else:
                logger.error(f'Error downloading: {self.prefix}/{file_name}')
                logger.error(error)
                raise Exception(f"Unable to download file: {file_name}")

    def delete_file(self, file_name):
        try:
            self.s3.delete_object(Bucket = self.bucket_name, Key=f'{self.prefix}/{file_name}')
        except botocore.exceptions.ClientError as error:
            logger.error(error)

    def check_if_exists(self, file_name):
        try:
            self.s3.head_object(Bucket = self.bucket_name, Key = f'{self.prefix}/{file_name}')            
            return True
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == '404':
                logger.error('File does not exist')   
            else:
                logger.error(error)                

        return False
                

class Queue:
    def __init__(self, session, queue_name):
        self.sqs = session.client('sqs')

        # Create queue if doesn't exist
        response = self.sqs.list_queues(QueueNamePrefix = queue_name) 
        if 'QueueUrls' not in response or len(response['QueueUrls'])==0:
            self.sqs.create_queue(QueueName = config.queue,
                                  Attributes = {
                                    "DelaySeconds": str(DELAY_SECONDS),
                                    "VisibilityTimeout": str(VISIBILITY_TIMEOUT)})

    def get_url(self):
        try:
            response = self.sqs.get_queue_url(QueueName = config.queue)
            return response["QueueUrl"]
        except botocore.exceptions.ClientError as error:
            logger.error(error)

    def delete_message(self, receipt_handle):
        try:
            response = self.sqs.delete_message(
                QueueUrl = self.get_url(),
                ReceiptHandle=receipt_handle,
            )
        except botocore.exceptions.ClientError as error:
            logger.error(error)
        
    def send_message(self, message):
        try:
            self.sqs.send_message(
                QueueUrl=self.get_url(),
                MessageBody=json.dumps(message))    
        except botocore.exceptions.ClientError as error:
            logger.error(error)

    def receive_messages(self, fnc):
        def process_message(message, pbar, fnc):
            message_body = json.loads(message["Body"])
            
            if isinstance(pbar,tqdm):                   
                fnc(message_body, callback = pbar.update)                
                
            else:                
                fnc(message_body, show_progress = True)                
            self.delete_message(message['ReceiptHandle'])
        
        def process_messages(messages, pbar, fnc):
            futures = {}
            with ThreadPoolExecutor() as executor:
            
                for message in messages:                 
                    futures[executor.submit(process_message, message, pbar, fnc)] = message

                pending_messages = []
                for future in as_completed(futures):
                    message = futures[future]
                    try:
                        result = future.result()
                    except Exception as error:                                
                        pending_messages.append(message)
                        
                return pending_messages

        def get_messages():
            try:
                response = self.sqs.receive_message(
                    QueueUrl=self.get_url(),
                    MaxNumberOfMessages=10,
                    WaitTimeSeconds=5)

                return response.get('Messages', [])
                
            except botocore.exceptions.ClientError as error:
                logger.error(error)
        
        def iterate(messages, fnc, pbar = None):
            pending_messages = process_messages(messages, pbar, fnc)
            while len(pending_messages) > 0:                
                pending_messages = process_messages(pending_messages, pbar, fnc)

        messages = get_messages()
        while len(messages) > 0:
            if len(messages) > 1:
                with tqdm(total=len(messages), unit='files', desc='Downloading files') as pbar:                    
                    iterate(messages, fnc, pbar)
            else:
                iterate(messages, fnc)
            messages = get_messages()        

class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance

        return cls._instances[cls]

class Init(metaclass = SingletonMeta ):
    def __init__(self):        
        if not config.load() or len(config.bucket)==0:
            logger.error('You first must configure the tool')
            sys.exit()

        try:
            session = boto3.Session(region_name = config.region,
                                    profile_name = config.profile)

            self.bucket = Bucket(session, config.bucket, config.prefix)
            self.queue = Queue(session, config.queue)
        
        except botocore.exceptions.ProfileNotFound as error:
            if config.profile == 'default':
                session = boto3.Session(region_name = config.region)

                self.bucket = Bucket(session, config.bucket, config.prefix)
                self.queue = Queue(session, config.queue)
            else:
                logger.error(error)
                sys.exit()            

class S3CP:
    def __init__(self):        
        self.__version__ = '0.2.2'
        self.check_if_is_latest_version()

    def check_if_is_latest_version(self):        
        latest_version = str(subprocess.run([sys.executable, '-m', 'pip', 'install', 's3cp==random'], capture_output=True, text=True))
        latest_version = latest_version[latest_version.find('(from versions:')+15:]
        latest_version = latest_version[:latest_version.find(')')]
        latest_version = latest_version.replace(' ','').split(',')[-1]

        current_version = str(subprocess.run([sys.executable, '-m', 'pip', 'show', 's3cp'], capture_output=True, text=True))
        current_version = current_version[current_version.find('Version:')+8:]
        current_version = current_version[:current_version.find('\\n')].replace(' ','') 


        if current_version != latest_version:
            print(bcolors.WARNING + f'WARNING: You are using s3cp version {current_version}; however, version {latest_version} is available.')
            print(f"You should consider upgrading via the '{sys.executable} -m pip install --upgrade s3cp' command." + bcolors.ENDC)
            print('')
    
    def get_version(self):
        return self.__version__

    def send_files(self, **args):        
        init = Init()    
        def count_files(files):
                total_files = 0
                for path in files:                
                    if os.path.isfile(path):                                                        
                        total_files += 1
                    elif os.path.isdir(path):        
                        for (root,dirs,files) in os.walk(path, topdown=True):
                            for file in files:                                                                                
                                total_files += 1
                return total_files    

        def handler(files, pbar):
            bucket = init.bucket
            queue = init.queue

            def send_file(bucket, queue, file_name, show_progress = False):
                bucket.upload_file(file_name, show_progress)        
                message = {'file': file_name}
                queue.send_message(message)
                return f'{file_name} sent'  

            
                    
            futures = {}
            with ThreadPoolExecutor() as executor:            
                for path in files:                
                    if os.path.isfile(path):                             
                        if isinstance(pbar,tqdm):                               
                            futures[executor.submit(send_file, bucket, queue, path)] = path                                                  
                        else:
                            futures[executor.submit(send_file, bucket, queue, path, True)] = path              
                            
                    elif os.path.isdir(path):        
                        for (root,dirs,files) in os.walk(path, topdown=True):
                            for file in files:                                                    
                                file_path = os.path.join(root,file)                                                    
                                futures[executor.submit(send_file, bucket, queue, file_path)] = file_path                            
                    else:
                        logger.error('File not found or not supported')
                
                pending_files = []
                for future in as_completed(futures):
                    path = futures[future]
                    try: 
                        result = future.result()                    
                    except Exception as error:                                
                        pending_files.append(path)                    
                    else:
                        if hasattr(pbar, 'update'):
                            pbar.update()                    
                        
                return pending_files

        def iterate(files, pbar = None):
            pending_files = handler(files, pbar)
            while len(pending_files)>0:            
                pending_files = handler(pending_files, pbar)

        num_files = count_files(args['files'])

        if num_files>1:
            with tqdm(total=num_files, unit='files', desc='Sending files') as pbar:
                iterate(args['files'], pbar)
        else:         
            iterate(args['files'])

    def receive_files(self):
        init = Init()    
        
        bucket = init.bucket
        queue = init.queue

        def process_message(message_body, show_progress = False, callback = lambda: None):        
            file_name = message_body['file'] 
            bucket.download_file(file_name, show_progress)  
            if not show_progress:
                callback()                 

        queue.receive_messages(process_message)

    def configure(self):
        parameters = {
            'region': 'us-east-1',
            'queue': 's3copy',
            'bucket': '',
            'prefix': 's3copy',
            'profile': 'default'}
        
        for param in parameters:
            attr = getattr(config, param, None) 
            val = attr if attr != None else parameters[param]
            setattr(config, param, input(f'{param} [{val}]: ') or val)
        
        config.save()

s3cp = S3CP()

def invalid_command():
    raise Exception('Invalid action')

def command_selector(command, **args):    
    commands = {
        'configure': s3cp.configure, 
        'send': s3cp.send_files,
        'receive': s3cp.receive_files,
        'version': s3cp.get_version}

    command_fnc = commands.get(command, invalid_command)

    return command_fnc(**args)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Simple tool to copy files using Amazon S3.',
        epilog="Don't forget to configure it before using it.")

    subparsers = parser.add_subparsers(title='actions to perform', dest='command')

    configure_parser = subparsers.add_parser('configure', help='set the configuration parameters')

    send_parser = subparsers.add_parser('send', help='send files')
    send_parser.add_argument(nargs='+', dest='files')

    receive_parser = subparsers.add_parser('receive', help='receive files')

    version_parser = subparsers.add_parser('--version', help='print s3cp version number and exit')

    args = parser.parse_args()    


    if args.command==None:        
        parser.print_help()

    else:
        command_selector(**vars(args))    
