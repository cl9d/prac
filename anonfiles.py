import requests
import ntpath as nt
import sys

def Main():
    arg = sys.argv[1:]
    path = arg[0].replace('\\', '\\\\') 
    files = {'file': (nt.basename(arg[0]), open(path, 'rb'))}
    url = 'https://api.anonfiles.com/upload'
    response = requests.post(url, files=files)
    data = response.json()
    print(data['data']['file']['url']['short']) 
    
Main()