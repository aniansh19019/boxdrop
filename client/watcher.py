import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os
import chunker
import mq_sender
import mq_receiver
import sys

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
def on_any_event(event):
    event_message = {
        'event_type': event.event_type,
        'src_path': event.src_path,
        'is_dir': event.is_directory
    }

    if event.event_type == 'moved':
        event_message['dest_path'] = event.dest_path
    
    print(event_message)
    sender.send_directory_update(event_message)

if __name__ == "__main__":
    root_dir = "../example_sync_dir"
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    
    patterns = ["*"]
    ignore_patterns = [".DS_Store"]
    ignore_directories = False
    case_sensitive = False
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    # my_event_handler.on_created = on_created
    # my_event_handler.on_deleted = on_deleted
    # my_event_handler.on_modified = on_modified
    # my_event_handler.on_moved = on_moved
    my_event_handler.on_any_event = on_any_event
    path = os.path.abspath(root_dir)
    assert os.path.exists(path)
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=True, )
    my_observer.start()
    # Start the receiver
    receiver = mq_receiver.MessageReceiver()
    receiver.spawn_receiver()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
    