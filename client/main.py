import auth
import config
import metadata_db
import uuid
import os
import chunker
import watcher
import time

def init_program():
    # check if a user is logged in
    if not auth.is_logged_in():
        # if not logged in, ask to login or register
        while not auth.interface():
            print("You need to login or register before using BoxDrop!")
    
    # begin program logic

    # check if user record exists
    is_new_user = False
    user_record = metadata_db.get_user_record_from_email(auth.user_email())
    if user_record == None:
        print("New User! Creating Records!")
        user_record = init_user_record(auth.user_email())
        is_new_user = True
    
    # init root directory path
    config.Config.ROOT_DIR = os.path.join(os.path.expanduser("~"), "BoxDrop" + user_record['id'])
    
    # check if the user directory has already been initialised

    if not os.path.exists(config.Config.ROOT_DIR):
        # the directory does not exist
        # make the directory
        os.mkdir(config.Config.ROOT_DIR)

        # check if it is a new user
        if is_new_user:
            # scan the directory into the records
            root_id = chunker.build_directory_tree_metadata(config.Config.ROOT_DIR)
            # update the root id of the user_record and put in the metadata_db
            user_record['root_id'] = root_id
            metadata_db.put_user_record(user_record)
            # 
            pass
        else:
            # rebuild the directory from the records
            chunker.restore_directory_tree(config.Config.ROOT_DIR, user_record['root_id'])

            pass

        pass

    # After all the initialisation, start the watcher
    # ! Hacky Fix

    time.sleep(3)

    watcher.Watcher()
    



        
    pass


def init_user_record(email):
    # Create a user record and return the record
    user_record = {
        "id": uuid.uuid4().hex,
        "name": "",
        "email": email,
        "storage_quota": "",
        "used_quota": "",
        "root_id": ""
    }
    return user_record
    pass

init_program()