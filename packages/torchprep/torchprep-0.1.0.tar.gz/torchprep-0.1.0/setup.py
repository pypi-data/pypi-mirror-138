# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torchprep']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.9.1,<2.0.0', 'tqdm>=4.62.3,<5.0.0', 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['torchprep = torchprep.main:app']}

setup_kwargs = {
    'name': 'torchprep',
    'version': '0.1.0',
    'description': 'The easiest way to prepare Pytorch models for inference',
    'long_description': '# Torchprep\n\nA CLI tool to prepare your Pytorch models for efficient inference. The only prerequisite is a model trained and saved with `torch.save(model_name, model_path)`. See `example.py` for an example.\n\n**Be warned**: `torchprep` is an experimental tool so expect bugs, deprecations and limitations. That said if you like the project and would like to improve it please open up a Github issue!\n\n## Install from source\n\nCreate a virtual environment \n\n```sh\napt-get install python3-venv\npython3 -m venv venv\nsource venv/bin/activate\n```\n\nInstall `poetry`\n\n```sh\nsudo python3 -m pip install -U pip\nsudo python3 -m pip install -U setuptools\npip install poetry\n```\n\nInstall `torchprep`\n\n```sh\ncd torchprep\npoetry install\n```\n\n## Install from Pypi (Coming soon)\n\n```sh\npip install torchprep\n```\n\n## Usage\n\n```sh\ntorchprep quantize --help\n```\n\n### Example\n\n```sh\n# Install example dependencies\npip install torchvision transformers\n\n# Download resnet example\npython example.py\n\n# quantize a cpu model with int8 on cpu and profile with a float tensor of shape [64,3,7,7]\ntorchprep quantize models/resnet152.pt int8 --input-shape 64,3,7,7\n\n# profile a model for a 100 iterations\ntorchprep profile models/resnet152.pt --iterations 100 --device cpu --input-shape 64,3,7,7\n\n# set omp threads to 1 to optimize cpu inference\ntorchprep env --device cpu\n\n# Prune 30% of model weights\ntorchprep prune models/resnet152.pt --prune-amount 0.3\n```\n\n\n### Available commands\n\n\n```\nUsage: torchprep [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --install-completion  Install completion for the current shell.\n  --show-completion     Show completion for the current shell, to copy it or\n                        customize the installation.\n  --help                Show this message and exit.\n\nCommands:\n  distill        Create a smaller student model by setting a distillation...\n  prune          Zero out small model weights using l1 norm\n  env-variables  Set environment variables for optimized inference.\n  fuse           Supports optimizations including conv/bn fusion, dropout...\n  profile        Profile model latency \n  quantize       Quantize a saved torch model to a lower precision float...\n```\n\n### Usage instructions for a command\n\n`torchprep <command> --help`\n\n```\nUsage: torchprep quantize [OPTIONS] MODEL_PATH PRECISION:{int8|float16}\n\n  Quantize a saved torch model to a lower precision float format to reduce its\n  size and latency\n\nArguments:\n  MODEL_PATH                [required]\n  PRECISION:{int8|float16}  [required]\n\nOptions:\n  --device [cpu|gpu]  [default: Device.cpu]\n  --input-shape TEXT  Comma seperated input tensor shape\n  --help              Show this message and exit.\n```\n\n### Create binaries\n\nTo create binaries and test them out locally\n\n```sh\npoetry build\npip install --user /path/to/wheel\n```\n\n### Upload to Pypi\n\n```sh\npoetry config pypi-token.pypi <SECRET_KEY>\npoetry publish --build\n```\n\n## Roadmap\n* Supporting add custom model names and output paths\n* Support multiple input tensors for models like BERT that expect a batch size and sequence length\n* Support multiple input tensor types\n* Automatic distillation example: Reduce parameter count by 1/3 `torchprep distill model.pt 1/3`\n* Automated release with github actions\n* TensorRT, IPEX, AMP and autocast support\n* Training aware optimizations\n* Get model input shape using fx instead of asking user for it\n* Refactor profiling, loading and saving into seperate functions\n* More environment variable setting and a way to reverse environment variables (e.g: save current ones in user file)\n',
    'author': 'Mark Saroufim',
    'author_email': 'marksaroufim@fb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
