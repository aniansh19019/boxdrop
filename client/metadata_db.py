import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

import sqlitedict
from sqlitedict import SqliteDict
from pymongo import MongoClient
import os

app = firebase_admin.initialize_app()
db = firestore.client()


MAX_CHUNK_SIZE = 4096 # Max chunk size in bytes
MIN_CHUNK_SIZE = 256 # Minimum chunk size in bytes
CACHE_SIZE = 1024 # Number of chunks to store in the offline cache
SKIP_FILES = ['.DS_Store', '__pycache__']
ROOT_DIR = os.path.abspath('../example_sync_dir')

def put_user_record(user_record):
    '''
    Put the given user record in the 'users' collection, using the 'id' field in the record as key.
    Return the id of the new record.
    Raise error if unsuccessful.
    '''
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["mydatabase"]
        users_collection = db["users"]

        # Create a user document
        user = {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "age": 26
        }

        users_collection.update_one(user_record, upsert=True)       # Insert the document if it does not already exist, or update it if it does.
    
    except Exception as e:
        print(e)
        
    pass

def put_file_record(file_record):
    '''
    Put the given file record in the 'files' collection, using the 'id' field in the record as key.
    Return the id of the new record.
    Raise error if unsuccessful.
    '''
    try:
        file_db = sqlitedict.SqliteDict("internal_db/file.db", autocommit= True)
        # file = file_db.find_one({"_id": file_record['id']})

        # if(file_db[file_record["id"]])
        if file_record["id"] in file_db.keys():
            print("file already exists")

        else:
            file_db[file_record['id']] = file_record

        # if(file != file_record):
        #     file_db[file_record['id']:file_record]

        # else:
        #     print("file already exists")

        return file_record["id"]

        #print("One line Code Key value: ", list(my_dict.keys())
      # [list(my_dict.values()).index(100)])

    except Exception as e:
        print(e)

    pass

def put_chunk_record(chunk_record):
    '''
    Put the given chunk record in the 'chunks' collection, using the hash as the key.
    Return the id of the new record.
    Raise error if unsuccessful.
    '''
    try:
        chunk_db = sqlitedict.SqliteDict("internal_db/chunk_cache.db", autocommit=False, outer_stack= False)

        if chunk_record["id"] in chunk_db.keys():
            print("file already exists")

        else:
            chunk_db[chunk_record['id']] = chunk_record

        return file_record["id"]

    except Exception as e:
        print(e)
    
    pass





def get_user_record_from_id(user_id):
    '''
    Get the user record from the 'users' collection with the given id.
    Return the user record as a dict.
    Raise error if unsuccessful.
    '''
    pass

def get_user_record_from_email(email):
    '''
    Get the user record from the 'users' collection with the given email.
    Return the user record as a dict.
    Raise error if unsuccessful.
    '''
    try:
        user_db = sqlitedict.SqliteDict("internal_db/file.db", autocommit= True)

        for user in user_db.values():
            if user["email"] == email:                    # assuming file db dict has a "name" field
                return user
            
            else:
                message = "User with this email not found."
                return message 

    except Exception as e:
        print(e)

    pass


def get_file_record_from_path(file_path):
    '''
    Get the file record from the 'files' collection with the given path.
    Return the file record as a dict.
    Raise error if unsuccessful.
    '''
    try:
        file_db = sqlitedict.SqliteDict("internal_db/file.db", autocommit= True)
        file_name = os.path.basename(file_path)

        for file in file_db.values():
            if file["name"] == file_name:                    # assuming file db dict has a "name" field
                return file
            
            else:
                message = "File with this path not found."
                return message 

    except Exception as e:
        print(e)

    pass

def get_file_record_from_id(file_id):
    '''
    Get the file record from the 'files' collection with the given id.
    Return the file record as a dict.
    Raise error if unsuccessful.
    '''
    try:
        file_db = sqlitedict.SqliteDict("internal_db/file.db", autocommit= True)

        if file_id in file_db.keys():
            return file_db[file_id]

        else:
            message = "File doesn't exist"
            return message

    except Exception as e:
        print(e)

    pass

def get_chunk_record_from_hash(chunk_hash):
    '''
    Get the chunk record from the 'chunks' collection with the given hash.
    Return the chunk record as a dict.
    Raise error if unsuccessful.
    '''
    pass




def update_user_record(user_record):
    '''
    Update the given user record in the 'users' collection. The key being the 'id' field of the record.
    Raise error if unsuccessful.
    '''
    
    pass

thisdict.update({"color": "blue"})

def update_file_record(file_record):
    '''
    Update the given file record in the 'files' collection. The key being the 'id' field of the record.
    Raise error if unsuccessful.
    '''
    try:
        file_db = sqlitedict.SqliteDict("internal_db/file.db", autocommit= True)

        if file_record["id"] in file_db.keys():
            file_db.update({file_record["id"]: file_record})

        else:
            message = "File doesn't exist"
            return message

    except Exception as e:
        print(e)
        
    pass

def update_chunk_record(chunk_record):
    '''
    Update the given chunk record in the 'chunks' collection. The key being the 'id' field of the record.
    Raise error if unsuccessful.
    '''
    try:
        chunk_db = sqlitedict.SqliteDict("internal_db/chunk_cache.db", autocommit=False, outer_stack= False)

        if chunk_db["id"] in chunk_db.keys():
            chunk_db.update({chunk_record["id"]: chunk_record})

        else:
            message = "File doesn't exist"
            return message

    except Exception as e:
        print(e)

    pass





def delete_user_record(user_id):
    '''
    Delete the user record from the 'users' collection with the given id.
    Raise error if unsuccessful.
    '''
    pass

def delete_file_record(file_id):
    '''
    Delete the file record from the 'files' collection with the given id.
    Raise error if unsuccessful.
    '''
    try:
        file_db = sqlitedict.SqliteDict("internal_db/file.db", autocommit= True)

        if file_id in file_db.keys():
            del file_db[file_id]

        else:
            message = "File doesn't exist"
            return message

    except Exception as e:
        print(e)

    pass

def delete_chunk_record(chunk_hash):
    '''
    Delete the chunk record from the 'chunks' collection with the given hash.
    Raise error if unsuccessful.
    '''
    # chunk_hash = chunk.hash
    try:
        chunk_db = sqlitedict.SqliteDict("internal_db/chunk_cache.db", autocommit=False, outer_stack= False)

        if chunk_db["id"] in chunk_db.keys():
            chunk_db.update({chunk_record["id"]: chunk_record})

        else:
            message = "File doesn't exist"
            return message

    except Exception as e:
        print(e)
        
    pass
