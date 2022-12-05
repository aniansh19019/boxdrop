import requests
from requests.auth import HTTPBasicAuth

endpoint = "http://127.0.0.1:5000"

data = {"message": "hello world"}

auth = HTTPBasicAuth('aniansh@yahoo.com', 'password')

# header = {"Authorisation"}

response = requests.post(endpoint, data, auth=auth)

print(response.text)