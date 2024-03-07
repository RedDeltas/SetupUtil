import os
import requests
import threading 
from tqdm import tqdm
from typing import List

def get_headers(token:str) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    return headers

def download_model_part(start, end, url, filepath, filename, chunk_size):
    if "CIVITAI_TOKEN" in os.environ:
        civitai_token = os.getenv("CIVITAI_TOKEN")
        headers = get_headers(civitai_token)
    else:
        headers = {}
    
    headers['Range'] = f'bytes={start}-{end}'

    r = requests.get(url, headers=headers, stream=True)

    # with open(filepath, "r+b") as file:
    #     file.seek(start)
    #     var = file.tell()
    #     file.write(r.content)

    with tqdm(total=end-start, unit="B", unit_scale=True) as progress_bar:
            progress_bar.set_description(f'{filename}-{start}')
            with open(filepath, mode="r+b") as file:
                file.seek(start)
                var = file.tell()
                for chunk in r.iter_content(chunk_size):
                    progress_bar.update(len(chunk))
                    file.write(chunk)

def load_models_from_civitai(models:List[dict]):
    print("Downloading models from CivitAI")

    number_of_threads = 4

    for model in models:
        if "CIVITAI_TOKEN" in os.environ:
            civitai_token = os.getenv("CIVITAI_TOKEN")
            headers = get_headers(civitai_token)
        else:
            headers = {}

        r = requests.get(model['url'], headers=headers, stream=True)
        
        if r.status_code == 401:
            civitai_token = input("Unauthorised, please enter token:")
            os.environ["CIVITAI_TOKEN"] = civitai_token
            headers = get_headers(civitai_token)
            r = requests.get(model['url'], headers=headers, stream=True)

        # Get filename
        content_disposition = r.headers["content-disposition"]
        filename = content_disposition.split("filename=")[1].replace('"', '')
        # Get size
        total_size = int(r.headers.get("content-length", 0))
        chunk_size = 10 * 1024

        filepath = os.path.join(model['local_dir'], filename)

        part = int(total_size / number_of_threads)

        # Create file with size of content
        with open(filepath, "wb") as file:
            file.write(b'\0' * total_size)

        for i in range(number_of_threads):
            start = part * i
            end = start + part

            t = threading.Thread(
                target=download_model_part,
                kwargs={
                    'start': start,
                    'end': end,
                    'url': model['url'],
                    'filepath': filepath,
                    'filename': filename,
                    'chunk_size': chunk_size,
                }
            )
            t.setDaemon(True)
            t.start()
        
        main_thread = threading.current_thread()
        for t in threading.enumerate():
            if t is main_thread:
                continue
            t.join()
