import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os
import chunker
import mq_sender
import mq_receiver
import sys
import config

counter = 0

sender = mq_sender.MessageSender()


# TODO: Also notify other devices in the same event handlers
# TODO: Watch for changes in the cloud

def on_created(event):
    print(f"New file created: {event.src_path}")
    print("Updating metadata...")
    chunker.create_file_metadata(event.src_path)

def on_deleted(event):
    print(f"File deleted: {event.src_path}")
    print("Updating metadata...")
    chunker.delete_file_metadata(event.src_path)

def on_modified(event):
    # Tell the chunker to upload the modified chunks and to modify the metadata of this file
    print(f"File modified: {event.src_path}")
    print("Updating metadata...")
    chunker.update_file_metadata(event.src_path)


def on_moved(event):
    print(f"File moved from {event.src_path} to {event.dest_path}")
    print("Updating metadata...")
    chunker.move_file_metadata(event.src_path, event.dest_path)


#! Order not guaranteed!
# TODO: send messages after the metadata is updated, use blocking functions

# ! Problems with pausing the watcher
# ? Can you destroy and create the watcher to fix the hacky time fix?
class Watcher:
    def __init__(self) -> None:
        self.is_paused = False
        root_dir = config.Config.ROOT_DIR
        patterns = ["*"]
        ignore_patterns = config.Config.SKIP_FILES
        ignore_directories = False
        case_sensitive = False
        self.my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        # my_event_handler.on_created = on_created
        # my_event_handler.on_deleted = on_deleted
        # my_event_handler.on_modified = on_modified
        # my_event_handler.on_moved = on_moved
        self.my_event_handler.on_any_event = self.on_any_event
        self.path = os.path.abspath(root_dir)
        assert os.path.exists(self.path)
        self.my_observer = Observer()
        self.watch = self.my_observer.schedule(self.my_event_handler, self.path, recursive=True, )
        self.my_observer.start()
        # Start the receiver
        self.receiver = mq_receiver.MessageReceiver(observer_ref=self)
        self.receiver.spawn_receiver()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.my_observer.stop()
            self.my_observer.join()
        
    def stop(self):
        self.is_paused = True

    def start(self):
        self.is_paused = False

    def __del__(self):
        self.my_observer.stop()
        self.my_observer.join()
        pass
    
    def on_any_event(self, event):

        # if paused, ignore all changes
        if self.is_paused:
            print("Watcher Off....")
            return
        # call event handlers manually to preserve order

        if event.event_type == 'created':
            on_created(event)
            pass
        if event.event_type == 'modified':
            on_modified(event)
            pass
        if event.event_type == 'moved':
            on_moved(event)
            pass
        if event.event_type == 'deleted':
            on_deleted(event)
            pass

        # ! Hacky FIX, adding a time delay

        # time.sleep(2)

        # Send messages only after the updates have happened in the metadata_db and s3
        event_message = {
            'event_type': event.event_type,
            'src_path': os.path.relpath(event.src_path, config.Config.ROOT_DIR),
            'is_dir': event.is_directory
        }

        if event.event_type == 'moved':
            event_message['dest_path'] = os.path.relpath(event.dest_path, config.Config.ROOT_DIR)

        print(event_message)
        sender.send_directory_update(event_message)

# watcher = Watcher()