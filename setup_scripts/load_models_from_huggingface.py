import os
import click
import json
from huggingface_hub import hf_hub_download

os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

@click.command()
@click.option(
    "--config_file",
    prompt="Path to config file",
    help="The path to your config file containing the models you want to download",
)
def load_models_from_huggingface(config_file:str):
    with open(config_file) as file:
        config = json.load(file)
    
    for model in config.get('models'):
        hf_hub_download(**model)
