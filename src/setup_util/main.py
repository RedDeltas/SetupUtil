import json
from argparse import ArgumentParser
from setup_util.banner import banner
from setup_util.load_models_from_huggingface import load_models_from_huggingface

parser = ArgumentParser()

parser.add_argument("config_file", help="Config file for setup (see example_configs in Github)")

args = parser.parse_args()

def main():
    print(banner)
    with open(args.config_file) as file:
        config = json.load(file)
    
    if "hf_models" in config:
        load_models_from_huggingface(config["hf_models"])
