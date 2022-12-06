


# Do all the initialisation, authentication etc here.



def put_multiple_chunks_concur(hash_list, bytes_list):
    '''
    Put the given chunks (bytes_list) in the store with their keys = hash_list elements.
    Use any existing AWS S3 API for this or to do this yourself, use the python multiprocessing module.
    DO NOT USE python threads as they are not concurrent.
    Raise error if unsuccessful.
    '''


    pass

def get_multiple_chunks_concur(hash_list):
    '''
    Get the chunks from the store CONCURRENTLY using the keys in hash_list.
    Use any existing AWS S3 API for this or to do this yourself, use the python multiprocessing module.
    DO NOT USE python threads as they are not concurrent.
    Returns a list of chunk bytes for each of the chunks in hash_list.
    Raise error if unsuccessful.
    '''
    pass



def put_multiple_chunks(hash_list, bytes_list):
    '''
    Put the given chunks (bytes_list) in the store with their keys = hash_list elements.
    Raise error if unsuccessful.
    '''
    pass

def get_multiple_chunks(hash_list):
    '''
    Get the chunks from the store using the keys in hash_list.
    Returns a list of chunk bytes for each of the chunks in hash_list.
    Raise error if unsuccessful.
    '''
    pass


def put_chunk(hash, bytes):
    '''
    Put the given chunk (bytes) in the store with the key = hash.
    Raise error if unsuccessful.
    '''
    
    pass

def get_chunk(hash):
    '''
    Get the chunk bytes from store with key = hash.
    Return bytes.
    Raise error if unsuccessful.
    '''
    
    pass


def chunk_exists(hash):
    '''
    Checks if a chunk of the given hash exists in the store.
    Returns True or False.
    Raise error if unsuccessful.
    '''
    pass

