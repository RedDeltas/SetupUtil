import os
import json
from typing import List
from huggingface_hub import hf_hub_download

os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"


def load_models_from_huggingface(models:List[dict]):
    for model in models:
        hf_hub_download(**model)
