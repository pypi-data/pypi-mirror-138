import asyncio, requests, json, os, sys, time
import baracchino.constants as constants
import baracchino.classes as classes

async def list_files(key):
    
    r = requests.get(constants.API_URL + "/files", headers={"Authorization": f"{key}"})
        
    json_values = r.json()["message"]
    files = []
    for a in json_values:
        files.append(classes.File(a[0], a[1]))
        
    return files
    
    
    
