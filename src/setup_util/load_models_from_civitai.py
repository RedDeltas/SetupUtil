import os
import requests
from tqdm import tqdm
from typing import List

def get_headers(token:str) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    return headers

def load_models_from_civitai(models:List[dict]):
    print("Downloading models from CivitAI")

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

        with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
            progress_bar.set_description(filename)
            with open(filepath, mode="wb") as file:
                for chunk in r.iter_content(chunk_size):
                    progress_bar.update(len(chunk))
                    file.write(chunk)
