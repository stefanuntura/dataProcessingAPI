import requests

BASE = "http://127.0.0.1:5000/"

url = BASE + "helloworld/stefan/19"

def getRequest():
    return requests.get(url).json()

response = requests.post(url).json()
print(response)
