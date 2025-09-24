# /// script
# dependencies = [
#   "torch>=2.0.0",
#   "torchvision>=0.15.0",
#   "diffusers @ git+https://github.com/huggingface/diffusers",
#   "transformers>=4.35.0",
#   "accelerate>=0.25.0",
#   "safetensors>=0.4.0",
#   "huggingface-hub>=0.20.0",
#   "Pillow>=9.0.0",
# ]
# ///

"""
This script wrapper allows direct execution via:
uv run https://raw.githubusercontent.com/ivanfioravanti/qwen-image-mps/main/qwen-image-mps.py

For package installation, use: pip install qwen-image-mps
"""

import importlib.util
import os
import sys
import tempfile
import urllib.request


def import_from_url(url, module_name):
    """Import a Python module from a URL."""
    with urllib.request.urlopen(url) as response:
        code = response.read()

    # Create a temporary file to hold the module
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".py", delete=False) as tmp:
        tmp.write(code)
        tmp_path = tmp.name

    try:
        # Load the module from the temporary file
        spec = importlib.util.spec_from_file_location(module_name, tmp_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        # Clean up the temporary file
        os.unlink(tmp_path)


if __name__ == "__main__":
    import sys

    repo_root = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(repo_root, "src")
    if os.path.isdir(src_path) and src_path not in sys.path:
        sys.path.insert(0, src_path)

    try:
        from qwen_image_mps import cli as cli_module
    except ModuleNotFoundError:
        default_cli_url = (
            "https://raw.githubusercontent.com/ivanfioravanti/qwen-image-mps/"
            "main/src/qwen_image_mps/cli.py"
        )
        cli_url = os.environ.get("QWEN_IMAGE_MPS_CLI_URL", default_cli_url)
        cli_module = import_from_url(cli_url, "qwen_image_mps_cli")

    cli_module.main()
