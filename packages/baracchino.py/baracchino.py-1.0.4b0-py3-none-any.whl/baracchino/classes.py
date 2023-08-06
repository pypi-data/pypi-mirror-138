import requests
import baracchino.constants
class User(object):
    def __init__(self, key):
        self.key = key
        r = requests.get(f"{constants.API_URL}/me", headers={"Authorization": f"{self.key}"})

class File(object):
    def __init__(self, filename, url):
        self.name = filename
        self.url = url
    
    async def download(self, filename):
        r = requests.get(self.url)
        with open(filename, 'wb') as f:
            f.write(r.content)
        