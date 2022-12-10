import boto3

# S3 client
s3 = boto3.client('s3')

bucketName = 'battyfer'

# Creating bucket
response = s3.create_bucket(Bucket = bucketName)
## print(response)

# Data file in S3
file = 'data.txt'


# Do all the initialisation, authentication etc here.



def put_multiple_chunks_concur(hash_list, bytes_list):
    '''
    Put the given chunks (bytes_list) in the store with their keys = hash_list elements.
    Use any existing AWS S3 API for this or to do this yourself, use the python multiprocessing module.
    DO NOT USE python threads as they are not concurrent.
    Raise error if unsuccessful.
    '''


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
    
    try:
        metadata = {
            'hash': hash
        }

        # to give public access
        # args = {'ACL' : 'public-read'}

        response = s3.put_object(Bucket = bucketName, Key = file, Body = bytes, Metadata = metadata)
        # print(response)
        return True
    except Exception as e:
        print(e)


def get_chunk(hash):

    try:
        response = s3.get_object(Bucket = bucketName, Key = file)

        metadata = response['Metadata']

        hash_obj = metadata['hash']

        if hash_obj == hash:
            value = response['Body'].read()
            print('Hash found')
            return value
        else:
            print('Error: Hash not found')
            return FileNotFoundError
        
    except Exception as e:
        print(e)


def chunk_exists(hash):
    
    try:
        response = s3.get_object(Bucket = bucketName, Key = file)

        metadata = response['Metadata']

        hash_obj = metadata['hash']

        if hash_obj == hash:
            value = response['Body'].read()
            return True
        else:
            return False

    except Exception as e:
        print(e)


# put_chunk('1234567890abcdef', b'Hello, world!')
# get_chunk('1234567890abcdef')
get_chunk('1234567890')
# print(chunk_exists('1234567890abcdef'))
# print(chunk_exists('1234567890abcdef324'))