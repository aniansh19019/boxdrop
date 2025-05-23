import os
class Config:
    test_mode = False
    # TODO: make the root dir before accessing
    ROOT_DIR = os.path.abspath("~/BoxDrop")
    RABBIT_MQ_IP = "34.224.214.95"
    # RABBIT_MQ_IP = "localhost"
    MAX_CHUNK_SIZE = 1048576 # Max chunk size in bytes
    MIN_CHUNK_SIZE = 1024 # Minimum chunk size in bytes
    CACHE_SIZE = 1024 # Number of chunks to store in the offline cache
    SKIP_FILES = ['.DS_Store', '__pycache__', '.vscode']
    FIREBASE_AUTH_CONFIG=os.environ.get('FIREBASE_AUTH_CONFIG') or {
        "apiKey": "AIzaSyBYHMt5pzxnrfgm_2_LUJHyJzCAGOK8KzI",
        "authDomain": "cldcauth.firebaseapp.com",
        "databaseURL": "",
        "projectId": "cldcauth",
        "storageBucket": "cldcauth.appspot.com",
        "messagingSenderId": "661364563492",
        "appId": "1:661364563492:web:7eeb520dfff35399c8c2b1"
    }
    FIREBASE_ADMIN_CONFIG=os.environ.get('FIREBASE_ADMIN_CONFIG') or {
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
    }
    AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID') or "AKIA4FI2HJLSR6VWQO7X"
    AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY') or "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"
    AWS_REGION_NAME=os.environ.get('AWS_REGION_NAME') or "us-east-1"


