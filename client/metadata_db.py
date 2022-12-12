import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import asyncio

# Use a service account.
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "boxdrop-cldc",
  "private_key_id": "ead0028244823dd2916074612f5407b6cd900473",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCs4HGYQMxyYyW/\no4h9E4gOXA1uWfXEttJFZfYeRfg2h7LWpBBSZEP28ciS0opcowOgf9JobWKyKvtz\nbQ7kLLB5L1RB2mbOKab/jhgF3os7N+TxpwKodoAAbZEG8UOmHJysW6dJBx3gXyKO\n0uiME2KPLKml/ipqEFGveDZGc2oQH4gTFUdxpYTtOb7wmrEunemv2lEoeO9Ori34\ntCNoV1MkeqJ8LqyZTN3r0GBUh4cGSn0tuxLpE6NC13EaGV0FzUIwYMPLIEWfylE7\nBedrQkM9Qup/FEBpUba2rfLbNuU9wwQ43kYS37KJNEE2vWe4mLTg6FULnsQX6Pvz\noPVyZiV9AgMBAAECggEAG11z3cv0EO9M3GcAhfv/f3Zm0d7/nmHqKv4W1Xfx8H/O\neVeDFee1MnPXchZNvJg5TMCvB8S46McRApZy0v+X97bcOYhe2aeSPcW6W8N8eqVA\nYlgzfYM0g9zUJisusC67RjVD57Vur0Of7sfH89Rlt5A0UohHIn7uzz3SKZi/Y0m3\ne/OxCN+OzJicLLuM3eyYrOXCyhFwhxIqp3BJdidwxzb3govSwu6oUQ3gEYNUkvvO\nPRi0HepzDBlwahpr6YoOJU5V6cb2hr5Tj+GeZjI5h0AcMRBgli5N8uuim4idBJWu\na4nZ3dDNRB9wDLvfjNgwj0rSUiWM4E4vHyQGavBjqQKBgQDqfdbXTFmqJIOdQkQJ\niPAcVhMRDfD004JqeqSOAazOizUBnl4jmwuTnUEBU0xjSM+iy5aOvE0ZGNAamg5O\nm80UeSV5d14wjDugx4aa5uV+8cPu1rX4xH4siCm/YlkJ0CJBflqBjlCvi1RK0Ech\n6sxEDnTOMccUmnHoMPiUYYgnOwKBgQC8u89RSRA+LfOO96LeGQhmziUH8V05GVV5\nhTGqRFe6YOp0EJ3Q7tJPsY9LRzrkBCVKyjURwbZgi4pcSTCp7hK+VtTAbcumSJeQ\nwrsb9QXDH5RqoE88R1PbfLQitlTvYxko9dTrqfPdaQ4Bc4rx7viT+Zq5N7ehIbCK\nINi1MODKpwKBgQDHGCk9i9nlmDMXZpgV8GrN5Fcz975KYPsuJQtqdwmeJJvQ0AHm\nAVKG9tGmqm8FLWD+PBWNA1wCnwqyS3MyUx6A74td4nfaiHZoQICNLNZWPje5phvD\nKDJo5QNtN7eZmVo8eWem8IqZQZdEHisHJTBh6FRMbf82AxwLpOiqM1VC2QKBgGN0\nOIhmDwglIM560jllSZcbFEp+NxjKr88MkCJgRzZwsbudsfwSjYLvV0pc67ySLrCd\no5+Ky7dOcQe2jc1OJlRk31HTydgDMtNWulC+Kl4rOwOBHJ/wGlF0Aly0ZkeLmguK\nl7vj4B0Rqg67u0FII3eetZjasopXfXccXfYFHr/LAoGBAIyykgiZ/ZlROuMj27Uz\n2g73bX3XyHQ9oQ/fdrtyQEfil/zURtX2draDdtHoCcuwaKabiAJOCr9OE5aFYLae\nt0m5kUONymO5aigl63n4OFn3jm4MPGqK9JsZa5R6orjI3muaJo1vEaFCixtRm2CK\nJHKdQGQk0YjaVDF6jIjSZpFP\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-t9l1t@boxdrop-cldc.iam.gserviceaccount.com",
  "client_id": "103225708256749588441",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-t9l1t%40boxdrop-cldc.iam.gserviceaccount.com"
})

app = firebase_admin.initialize_app(cred)

db = firestore.client()
# TODO: Make sure all get and update calls are blocking

def put_user_record(user_record):
    '''
    Put the given user record in the 'users' collection, using the 'id' field in the record as key.
    Return the id of the new record.
    Raise error if unsuccessful.
    '''
    doc_ref = db.collection("users").document(user_record["id"])
    doc_ref.set(user_record)
    return user_record["id"]
    pass

def put_file_record(file_record):
    '''
    Put the given file record in the 'files' collection, using the 'id' field in the record as key.
    Return the id of the new record.
    Raise error if unsuccessful.
    '''
    doc_ref = db.collection("files").document(file_record["id"])
    doc_ref.set(file_record)
    return file_record["id"]
    pass

def put_chunk_record(chunk_record):
    '''
    Put the given chunk record in the 'chunks' collection, using the hash as the key.
    Return the id of the new record.
    Raise error if unsuccessful.
    '''
    doc_ref = db.collection("chunks").document(chunk_record["hash"])
    doc_ref.set(chunk_record)
    return chunk_record["hash"]
    pass





def get_user_record_from_id(user_id):
    '''
    Get the user record from the 'users' collection with the given id.
    Return the user record as a dict.
    Raise error if unsuccessful.
    '''
    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()
    return doc.to_dict()
    pass

def get_user_record_from_email(email):
    '''
    Get the user record from the 'users' collection with the given email.
    Return the user record as a dict.
    Raise error if unsuccessful.
    '''
    doc_ref = db.collection("users").where("email", "==", email)
    docs = doc_ref.get()
    if len(docs) == 0:
        return None
    return docs[0].to_dict()
    pass


def get_file_record_from_path(file_path):
    '''
    Get the file record from the 'files' collection with the given path.
    Return the file record as a dict.
    Raise error if unsuccessful.
    '''
    doc_ref = db.collection("files").where("path", "==", file_path)
    docs = doc_ref.get()
    if len(docs) == 0:
        return None
    return docs[0].to_dict()
    pass

def get_file_record_from_id(file_id):
    '''
    Get the file record from the 'files' collection with the given id.
    Return the file record as a dict.
    Raise error if unsuccessful.
    '''
    doc_ref = db.collection("files").document(file_id)
    doc = doc_ref.get()
    return doc.to_dict()
    pass

def get_chunk_record_from_hash(chunk_hash):
    '''
    Get the chunk record from the 'chunks' collection with the given hash.
    Return the chunk record as a dict.
    Raise error if unsuccessful.
    '''
    doc_ref = db.collection("chunks").document(chunk_hash)
    doc = doc_ref.get()
    return doc.to_dict()
    pass




def update_user_record(user_record):
    '''
    Update the given user record in the 'users' collection. The key being the 'id' field of the record.
    Raise error if unsuccessful.
    '''
    doc_ref = db.collection("users").document(user_record["id"])
    doc_ref.set(user_record)
    pass

def update_file_record(file_record):
    '''
    Update the given file record in the 'files' collection. The key being the 'id' field of the record.
    Raise error if unsuccessful.
    '''
    doc_ref = db.collection("files").document(file_record["id"])
    doc_ref.set(file_record)
    pass

def update_chunk_record(chunk_record):
    '''
    Update the given chunk record in the 'chunks' collection. The key being the 'id' field of the record.
    Raise error if unsuccessful.
    '''
    doc_ref = db.collection("chunks").document(chunk_record["hash"])
    doc_ref.set(chunk_record)
    pass



def delete_user_record(user_id):
    '''
    Delete the user record from the 'users' collection with the given id.
    Raise error if unsuccessful.
    '''
    doc_ref = db.collection("users").document(user_id)
    doc_ref.delete()
    pass

def delete_file_record(file_id):
    '''
    Delete the file record from the 'files' collection with the given id.
    Raise error if unsuccessful.
    '''
    doc_ref = db.collection("files").document(file_id)
    doc_ref.delete()

    pass

def delete_chunk_record(chunk_hash):
    '''
    Delete the chunk record from the 'chunks' collection with the given hash.
    Raise error if unsuccessful.
    '''
    doc_ref = db.collection("chunks").document(chunk_hash)
    doc_ref.delete()
    pass