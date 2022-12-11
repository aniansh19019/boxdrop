'''
Add code to send the messages about filesystem changes to the kubernetes hosted rabbitMQ.
'''

import pika
import json
import uuid
from config import Config
import os
import auth

# TODO error handling

class MessageSender:
    def __init__(self) -> None:
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=Config.RABBIT_MQ_IP, heartbeat=30))
        self.channel = self.connection.channel()
        # TODO: Get user email
        self.user_email = auth.user_email() or "aniansh@yahoo.com"
        self.channel.exchange_declare(exchange=self.user_email, exchange_type='fanout')
    
    def send_directory_update(self, message):
        message['from'] = str(uuid.UUID(int=uuid.getnode()))
        if Config.test_mode:
            message['from'] += str(os.getpid())
        self.channel.basic_publish(exchange=self.user_email, routing_key='',body=json.dumps(message))
        print("Sent update message to {} exchange!".format(self.user_email))
    

        
    def __del__(self):
        self.connection.close()



