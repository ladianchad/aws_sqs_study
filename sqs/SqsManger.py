from typing import Any
import boto3
from botocore.config import Config
import json
import queue

class SqsManger():

    class MessageDto():
        def __init__(self, receipt_handle: str, data : Any) -> None:
            self.receipt_handle = receipt_handle
            self.data = data
        
        def __str__(self) -> str:
            return f'receipt_handle : {self.receipt_handle}\ndata : {self.data}'

    def __init__(self, region: str, access_key: str, secret_key: str, queue_url: str) -> None:
        config = Config(
            region_name = region
        )
        
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region

        self.client = boto3.client('sqs', 
            config = config,
            aws_access_key_id = access_key,
            aws_secret_access_key = secret_key
        )

        self.queue_url = queue_url
        self.queue = queue.Queue()

    def __str__(self) -> str:
        return f'using boto3 sqs client\naccess_key_id is {len(self.access_key)} character start with {self.access_key[0]}\nsecret_key is {len(self.secret_key)} character start with {self.secret_key[0]}\nregion is {self.region}\nqueue name is {self.queue_url}'

    def __len__(self):
        return self.queue.qsize()

    def __receivce(self) -> None:
        print(self.queue_url)
        response = self.client.receive_message(QueueUrl = self.queue_url, MaxNumberOfMessages = 10)
        print(response)
        if 'Messages' in response:
            for message in response['Messages']:
                body = ''
                try:
                    body = json.loads(message['Body'])
                except :
                    body = message['Body']

                data = SqsManger.MessageDto(
                    receipt_handle = message['ReceiptHandle'],
                    data = body
                )
                self.queue.put(data)
    
    def get(self) -> Any:
        if self.queue.empty():
            self.__receivce()
        if not self.queue.empty():
            message : SqsManger.MessageDto = self.queue.get()
            self.client.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=message.receipt_handle
            )
            return message.data
        return None