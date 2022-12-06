import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os
import chunker

# Also notify other devices

def on_created(event):
    print(f"hey, {event.src_path} has been created!")

def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")

def on_modified(event):
    # Tell the chunker to upload the modified chunks and to modify the metadata of this file
    print(f"File modified: {event.src_path}")
    print("Updating metadata...")
    chunker.update_file_metadata(event.src_path)


def on_moved(event):
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")

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
    