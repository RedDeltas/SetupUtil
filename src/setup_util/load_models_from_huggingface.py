import os
import json
from typing import List
from huggingface_hub import hf_hub_download
from huggingface_hub.errors import RepositoryNotFoundError

os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"


def load_models_from_huggingface(models:List[dict]):
    print("Downloading models from HuggingFace")
    
    for model in models:
        try:
            hf_hub_download(**model)
        except RepositoryNotFoundError:
            hf_token = input("Unauthorised, please enter token:")
            os.environ["HF_TOKEN"] = hf_token
            try:
                hf_hub_download(**model)
            except RepositoryNotFoundError:
                raise Exception(f"Could not find HuggingFace repository: {model['repo_id']}")
