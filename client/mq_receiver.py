'''
Add code to get the messages about the filesystem changes from the kubernetes hosted rabbitMQ and to apply the changes to the root directory.
'''
# TODO: Add authentication on queue
import pika
import sys
import getpass
import json
import socket
import uuid
import threading
import os
import config
import indexer
import auth

# TODO terminate thread


class MessageReceiverKernel:
    def __init__(self, observer_ref) -> None:
        self.observer_ref = observer_ref
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.Config.RABBIT_MQ_IP))
        self.channel = self.connection.channel()
        self.user_email = auth.user_email()
        self.channel.exchange_declare(exchange=self.user_email, exchange_type='fanout')
        self.queue_name = str(getpass.getuser()) + "@" + str(socket.gethostname()) + "-" + str(uuid.UUID(int=uuid.getnode()))
        if config.Config.test_mode:
            # If testing on the same machine, make the queues temporary
            self.queue_name = ''
        result = self.channel.queue_declare(queue=self.queue_name, exclusive=config.Config.test_mode)
        # added because of test mode
        self.queue_name = result.method.queue
        self.channel.queue_bind(queue=self.queue_name, exchange=self.user_email)
        # see if any other consumption method is more suitable
        self.channel.basic_consume(queue=result.method.queue, on_message_callback=self.callback, auto_ack=True)

        pass
    
    def start_receiver(self):
        print("Starting consumption from exchange: {} and queue: {}".format(self.user_email, self.queue_name))
        self.channel.start_consuming()


    def __del__(self):
        # disable consumption
        self.connection.close()
        pass

    def callback(self, ch, method, properties, body):
        message = json.loads(body)
        # Ignore message if from the same device
        compare_string = str(uuid.UUID(int=uuid.getnode()))
        if config.Config.test_mode:
            compare_string += str(os.getpid())
        if message['from'] == compare_string:
            return

        print("Received new message! Updating Files...")
        print(message)
        print(self.observer_ref)
        indexer.handle_update_message(message=message, watcher_ref=self.observer_ref)




def start_consumption(observer_ref):
    # print(observer_ref)
    consumer = MessageReceiverKernel(observer_ref=observer_ref)
    consumer.start_receiver()

class MessageReceiver:
    def __init__(self, observer_ref) -> None:
        self.observer_ref = observer_ref
        self.is_spawned = False
        pass
    
    def spawn_receiver(self):
        if not self.is_spawned:
            self.consumer_thread = threading.Thread(target=start_consumption, args=[self.observer_ref])
            self.consumer_thread.start()
            self.is_spawned = True
            pass

    def __del__(self):
        if self.is_spawned:
            self.consumer_thread.join(timeout=10)


    

