'''
Add code to send the messages about filesystem changes to the kubernetes hosted rabbitMQ.
'''

import pika
import json
import uuid
import config
import os
import auth

# TODO error handling

class MessageSender:

    def open(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.Config.RABBIT_MQ_IP))
        self.channel = self.connection.channel()
        self.user_email = auth.user_email()
        self.channel.exchange_declare(exchange=self.user_email, exchange_type='fanout')
    
    def send_directory_update(self, message):
        # open connection
        self.open()
        # send message
        message['from'] = str(uuid.UUID(int=uuid.getnode()))
        if config.Config.test_mode:
            message['from'] += str(os.getpid())
        # Fix for broken pipe error
        try:
            self.channel.basic_publish(exchange=self.user_email, routing_key='',body=json.dumps(message))
        except:
            print("Problem with the send queue, retrying...")
            self.close()
            self.send_directory_update(message)
            pass
        print("Sent update message to {} exchange!".format(self.user_email))
        # close connection
        self.close()
    
    def close(self):
        self.connection.close()



