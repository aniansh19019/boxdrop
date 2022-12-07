import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os
import chunker

counter = 0

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


def on_any_event(event):
    global counter
    counter+=1
    print(event)
    print(f"counter:{counter}")
    pass

if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = [".DS_Store"]
    ignore_directories = False
    case_sensitive = False
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved
    # my_event_handler.on_any_event = on_any_event
    path = os.path.abspath("../example_sync_dir")
    assert os.path.exists(path)
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=True, )
    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
    