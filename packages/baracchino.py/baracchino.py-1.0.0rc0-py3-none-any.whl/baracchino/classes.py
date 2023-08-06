import requests
from .constants import *
class User(object):
    def __init__(self, key):
        self.key = key
        r = requests.get(f"{API_URL}/me", headers={"Authorization": f"{self.key}"})

class File(object):
    def __init__(self, filename, url):
        self.filename = filename
        self.url = url
    
    async def download(self, filename):
        r = requests.get(self.url)
        with open(self.filename, 'wb') as f:
            f.write(r.content)
        