from config import Config
import os
import shutil

def handle_update_message(message, watcher_ref):

    print("Pausing the watcher before applying received updates!")
    # Pause the watcher
    watcher_ref.stop()

    src_path = message['src_path']

    if message['event_type'] == 'created':
        if message['is_dir']:
            create_dir(src_path)
        else:
            create_file(src_path)

    elif message['event_type'] == 'modified':
        if message['is_dir']:
            modify_dir(src_path)
        else:
            modify_file(src_path)

    elif message['event_type'] == 'moved':
        dest_path = message['dest_path']
        if message['is_dir']:
            move_dir(src_path, dest_path)
        else:
            move_file(src_path, dest_path)
        pass
    elif message['event_type'] == 'deleted':
        if message['is_dir']:
            delete_dir(src_path)
        else:
            delete_file(src_path)
        pass
    # resume the watcher
    watcher_ref.start()
    print("Resuming Watcher")
    




def create_file(rel_path):
    pass

def create_dir(rel_path):
    pass


def modify_file(rel_path):
    pass

def modify_dir(rel_path):
    pass


def move_file(rel_src, rel_dest):
    pass

def move_dir(rel_src, rel_dest):
    pass


def delete_file(rel_path):
    abs_path = os.path.join(Config.ROOT_DIR, rel_path)
    
    # Update internal db record
    # TODO

    # delete the file
    if os.path.exists(abs_path):
        os.remove(abs_path)
        print("Removed file {}".format(rel_path))
    else:
        print("File {} already removed".format(rel_path))


    pass

def delete_dir(rel_path):
    abs_path = os.path.join(Config.ROOT_DIR, rel_path)
    
    # Update internal db record
    # TODO

    # delete the folder with all the contents
    
    shutil.rmtree(abs_path, ignore_errors=True)
    print("Removed file {}".format(rel_path))


    pass

