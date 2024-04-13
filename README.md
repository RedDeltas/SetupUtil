# SetupUtil
```
   ___         __        
  / _ \___ ___/ /        
 / , _/ -_) _  /         
/_/|_|\__/\_,_/          
   ___      ____         
  / _ \___ / / /____ ____
 / // / -_) / __/ _ `(_-<
/____/\__/_/\__/\_,_/___/
```
This is a simple utility to make getting up and running with Stable Diffusion environments easier, it is designed with RunPod in mind but should work for any environment

## Installation
```
pip install git+https://github.com/RedDeltas/SetupUtil.git
```

## Usage
Simply run `setup_util` passing your config as an argument
```
setup_util config.json
```
You can also pass multiple config files, this makes it easy to make your configuration composable depending on what you're doing. For example:
```
setup_util SUPIR_models.json SDXLIPAdapters.json
```
## Config
The expected config file is in JSON format, at the top level it will have various keys such as `"hf_models"` which will correspond with a set of activities that `setup_util` will complete. You can find examples in the `example_configs/` directory.

The currently available keys are:
* `"hf_models"`      - for downloading models from HuggingFace
* `"civitai_models"` - for downloading models from CivitAI

Although I plan to add more later

### Downloading Models From HuggingFace
The config for downloading models from HuggingFace looks like this:
```json
{
   ...,
   "hf_models": [
      {
         "repo_id": "RunDiffusion/Juggernaut-XL-v9",
         "filename": "Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors",
         "local_dir": "/workspace/ComfyUI/models/checkpoints",
         "cache_dir": "/workspace/cache"
      },
      ...
   ],
   ...
}
```
If the specified repo is a private one then it will prompt to ask for a HuggingFace token - this will be saved and used for subsequent models within this run of the `setup_util` so you don't need to enter it multiple times.

#### Arguments
These are the main arguments:
* `"repo_id"` - The HuggingFace repo you want to download the model from
* `"filename"` - The name of the file within the HuggingFace repo that you wish to download
* `"local_dir"` - The local directory where you want the model to be stored
* `"cache_dir"` - The directory to be used for caching (don't worry about this too much but make sure it is within `/workspace/` if you're using runpod)

Although anything you add will be passed into the `hf_hub_download()` function if you want to add anything extra https://huggingface.co/docs/huggingface_hub/v0.21.3/en/package_reference/file_download#huggingface_hub.hf_hub_download

### Downloading Models From CivitAI
The config for downloading models from CivitAI looks like this:
```json
{
   ...,
   "civitai_models": [
      {
         "name": "Detail Tweaker LoRA",
         "url": "https://civitai.com/api/download/models/62833?type=Model&format=SafeTensor",
         "local_dir": "/workspace/ComfyUI/models/loras"
      },
      ...
   ],
   ...
}
```
#### Arguments
These are the main arguments:
* `"name"` - The name of this model - not used anywhere just so you can see what it is as the URL is non human-readable
* `"url"` - The url for the model, you can get this by right clicking the "download" button on CivitAI and selecting "copy link"
* `"local_dir"` - The local directory where you want the model to be stored
