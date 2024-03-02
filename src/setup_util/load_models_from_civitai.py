import os
import requests
from tqdm import tqdm
from typing import List

def load_models_from_civitai(models:List[dict]):
    print("Downloading models from CivitAI")

    for model in models:
        r = requests.get(model['url'], stream=True)
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
