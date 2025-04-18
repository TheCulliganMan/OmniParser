import os
from huggingface_hub import hf_hub_download
import shutil

# Configure HTTP backend to disable SSL verification
# Blocked where I'm running
import requests
from huggingface_hub import configure_http_backend

# Security blocks huggingface
def backend_factory() -> requests.Session:
    session = requests.Session()
    session.verify = False
    return session

configure_http_backend(backend_factory=backend_factory)

# List of files to download
files = [
    "icon_detect/train_args.yaml",
    "icon_detect/model.pt",
    "icon_detect/model.yaml",
    "icon_caption/config.json",
    "icon_caption/generation_config.json",
    "icon_caption/model.safetensors"
]

# Download each file
for file in files:
    hf_hub_download(
        repo_id="microsoft/OmniParser-v2.0",
        filename=file,
        local_dir="weights"
    )

# Move the directory
if os.path.exists("weights/icon_caption"):
    if os.path.exists("weights/icon_caption_florence"):
        shutil.rmtree("weights/icon_caption_florence")
    shutil.move("weights/icon_caption", "weights/icon_caption_florence")