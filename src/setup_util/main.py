import json
from argparse import ArgumentParser
from setup_util.banner import banner
from setup_util.load_models_from_huggingface import load_models_from_huggingface
from setup_util.load_models_from_civitai import load_models_from_civitai

parser = ArgumentParser()

parser.add_argument("config_files", nargs="+", help="One or more config files for setup (see example_configs in Github - https://github.com/RedDeltas/SetupUtil/tree/main/example_configs)")

args = parser.parse_args()

def main():
    print(banner)
    for config_file in args.config_files:
        with open(config_file) as file:
            config = json.load(file)
        
        if "hf_models" in config:
            load_models_from_huggingface(config["hf_models"])
        
        if "civitai_models" in config:
            load_models_from_civitai(config["civitai_models"])

