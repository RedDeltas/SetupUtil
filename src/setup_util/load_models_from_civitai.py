import os
import requests
import threading
from tqdm import tqdm
from typing import List

def Handler(start, end, url, filename): 
     
    # specify the starting and ending of the file 
    headers = {'Range': 'bytes=%d-%d' % (start, end)} 
  
    # request the specified part and get into variable     
    r = requests.get(url, headers=headers, stream=True) 
  
    # open the file and write the content of the html page  
    # into file. 
    with open(filename, "r+b") as fp: 
      
        fp.seek(start) 
        var = fp.tell() 
        fp.write(r.content) 

def load_models_from_civitai(models:List[dict]):

    for model in models:
        r = requests.get(model['url'], stream=True)
        content_disposition = r.headers["content-disposition"]
        filename = content_disposition.split("filename=")[1].replace('"', '')
        filepath = os.path.join(model['local_dir'], filename)
        
        with open(filepath, mode="wb") as file:
            for chunk in tqdm(r.iter_content(chunk_size=10 * 1024)):
                file.write(chunk)
