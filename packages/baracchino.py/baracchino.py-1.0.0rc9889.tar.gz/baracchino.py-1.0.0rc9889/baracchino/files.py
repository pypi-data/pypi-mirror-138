import asyncio, requests, json, os, sys, time
from .constants import *
from .classes import *

async def list_files(key):
    
    r = requests.get(API_URL + "/files", headers={"Authorization": f"{key}"})
        
    json_values = r.json()["message"]
    files = []
    for a in json_values:
        files.append(File(a[0], a[1]))
        
    return files
    
    
    
