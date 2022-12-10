import boto3
from botocore.exceptions import ClientError

# S3 client
s3 = boto3.client('s3')

bucketName = 'battyfer'

# Creating bucket
response = s3.create_bucket(Bucket = bucketName)
## print(response)

# Data file in S3
# file = 'data.txt'


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
    try:
        for i in range(len(bytes_list)):

            key = hash_list[i]

            value = bytes_list[i]

            # Set the metadata for the object
            metadata = {
                'hash': hash_list[i]
            }

            # Upload the object to S3
            s3.put_object(Bucket = bucketName, Key = key, Body = value, Metadata = metadata)
        print('Data uploaded')

    except Exception as e:
        print(e)


def get_multiple_chunks(hash_list):
    '''
    Get the chunks from the store using the keys in hash_list.
    Returns a list of chunk bytes for each of the chunks in hash_list.
    Raise error if unsuccessful.
    '''
    bytes_list = []

    try:
        for hash in hash_list:
            key = hash

            response = s3.get_object(Bucket = bucketName, Key = key)

            metadata = response['Metadata']

            hash_obj = metadata['hash']

            if hash_obj == key:
                value = response['Body'].read()
                bytes_list.append(value)
            else:
                print('Error: Hash not found')
        
        return bytes_list

    except Exception as e:
        print(e)


def put_chunk(hash, bytes):
    
    try:
        metadata = {
            'hash': hash
        }

        # to give public access
        # args = {'ACL' : 'public-read'}

        response = s3.put_object(Bucket = bucketName, Key = hash, Body = bytes, Metadata = metadata)
        # print(response)
        return True
    except Exception as e:
        print(e)


def get_chunk(hash):

    try:
        response = s3.get_object(Bucket = bucketName, Key = hash)

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
        response = s3.head_object(Bucket = bucketName, Key = hash)
        return True

    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise

'''
get_chunk(hash)

hash -> str

'0dafd49005f14ba493deff20631bd811' -> b'usbhvqiuvnluvjnqpivvp-=p=op[k3pok3pofjk34jo0-239jo=-02io-30i-0i-23d23d902i309'


put_chunk(hash, bytes)

'0dafd49005f14ba493deff20631bd811', b'usbhvqiuvnluvjnqpivvp-=p=op[k3pok3pofjk34jo0-239jo=-02io-30i-0i-23d23d902i309'

get_multiple_chunks(hash_list):


hash_list = ['0dafd49005f14ba493deff20631bd811', '0dafd49005f14ba493deff20631bd811', '0dafd49005f14ba493deff20631bd811']
'''