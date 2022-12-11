import sqlitedict

def get_file_db():
    return sqlitedict.SqliteDict("internal_db/file.db", autocommit= True)

def get_chunk_db():
    return sqlitedict.SqliteDict("internal_db/chunk_cache.db", autocommit=True, outer_stack= False)

def get_user_db():
    return sqlitedict.SqliteDict("internal_db/user.db", autocommit= True)

def put_user_record(user_record):
    '''
    Put the given user record in the 'users' collection, using the 'id' field in the record as key.
    Return the id of the new record.
    Raise error if unsuccessful.
    '''
    user_db = get_user_db()
    user_db[user_record['id']] = user_record

    # close the db
    user_db.close()
    
    pass

def put_file_record(file_record):
    '''
    Put the given file record in the 'files' collection, using the 'id' field in the record as key.
    Return the id of the new record.
    Raise error if unsuccessful.
    '''
    file_db = get_file_db()
    file_db[file_record['id']] = file_record

    # close the db
    file_db.close()
    pass

def put_chunk_record(chunk_record):
    '''
    Put the given chunk record in the 'chunks' collection, using the hash as the key.
    Return the id of the new record.
    Raise error if unsuccessful.
    '''
    chunk_db = get_chunk_db()
    chunk_db[chunk_record['hash']] = chunk_record

    # close the db
    chunk_db.close()

    pass





def get_user_record_from_id(user_id):
    '''
    Get the user record from the 'users' collection with the given id.
    Return the user record as a dict.
    Raise error if unsuccessful.
    '''
    user_db = get_user_db()
    user_record = user_db[user_id]

    # close the db
    user_db.close()

    return user_record


    pass

def get_user_record_from_email(email):
    '''
    Get the user record from the 'users' collection with the given email.
    Return the user record as a dict.
    Raise error if unsuccessful.
    '''
    user_db= get_user_db()
    user_record = {}
    for key in user_db:
        if user_db[key]['email'] == email:
            user_record = user_db[key]
            break
    
    # close the db
    user_db.close()

    return user_record

    pass


def get_file_record_from_path(file_path):
    '''
    Get the file record from the 'files' collection with the given path.
    Return the file record as a dict.
    Raise error if unsuccessful.
    '''
    file_db = get_file_db()
    file_record = {}
    for key in file_db:
        if file_db[key]['path'] == file_path:
            file_record = file_db[key]
            break
    
    # close the db
    file_db.close()

    return file_record
    pass

def get_file_record_from_id(file_id):
    '''
    Get the file record from the 'files' collection with the given id.
    Return the file record as a dict.
    Raise error if unsuccessful.
    '''
    file_db = get_file_db()
    print(f"file id: {file_id}")
    file_record = file_db[file_id]
    
    # close the db
    file_db.close()

    return file_record
    pass

def get_chunk_record_from_hash(chunk_hash):
    '''
    Get the chunk record from the 'chunks' collection with the given hash.
    Return the chunk record as a dict.
    Raise error if unsuccessful.
    '''
    chunk_db = get_chunk_db()
    chunk_record = chunk_db[chunk_hash]

    # close the db
    chunk_db.close()

    return chunk_record
    pass




def update_user_record(user_record):
    '''
    Update the given user record in the 'users' collection. The key being the 'id' field of the record.
    Raise error if unsuccessful.
    '''
    user_db = get_user_db()
    user_db[user_record['id']] = user_record

    # close the db
    user_db.close()
    pass

def update_file_record(file_record):
    '''
    Update the given file record in the 'files' collection. The key being the 'id' field of the record.
    Raise error if unsuccessful.
    '''
    file_db = get_file_db()
    file_db[file_record['id']] = file_record

    # close the db
    file_db.close()

    pass

def update_chunk_record(chunk_record):
    '''
    Update the given chunk record in the 'chunks' collection. The key being the 'id' field of the record.
    Raise error if unsuccessful.
    '''
    chunk_db = get_chunk_db()
    chunk_db[chunk_record['hash']] = chunk_record

    # close the db
    chunk_db.close()

    pass



def delete_user_record(user_id):
    '''
    Delete the user record from the 'users' collection with the given id.
    Raise error if unsuccessful.
    '''
    user_db = get_user_db()
    del user_db[user_id]

    # close the db
    user_db.close()

    pass

def delete_file_record(file_id):
    '''
    Delete the file record from the 'files' collection with the given id.
    Raise error if unsuccessful.
    '''
    file_db = get_file_db()
    del file_db[file_id]

    # close the db
    file_db.close()

    pass

def delete_chunk_record(chunk_hash):
    '''
    Delete the chunk record from the 'chunks' collection with the given hash.
    Raise error if unsuccessful.
    '''
    chunk_db = get_chunk_db()
    del chunk_db[chunk_hash]

    # close the db
    chunk_db.close()

    pass