# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fastnn',
 'fastnn.nn',
 'fastnn.processors',
 'fastnn.processors.cv',
 'fastnn.processors.nlp',
 'fastnn.utils',
 'fastnn.utils.qa']

package_data = \
{'': ['*']}

install_requires = \
['transformers>=4.0.0,<5.0.0',
 'tritonclient[all]>=2.18.0,<3.0.0',
 'wget>=3.2,<4.0']

extras_require = \
{'docs': ['mkdocs>=1.1.2,<2.0.0',
          'mkdocs-material>=6.1.5,<7.0.0',
          'mkdocstrings>=0.18.0,<0.19.0'],
 'ios': ['coremltools>=4.0,<5.0'],
 'jupyter': ['jupyter>=1.0.0,<2.0.0',
             'jupyterlab>=2.2.9,<3.0.0',
             'matplotlib>=3.3.3,<4.0.0'],
 'torch': ['torch>=1.0.0,<2.0.0', 'torchvision<1.0.0']}

setup_kwargs = {
    'name': 'fastnn',
    'version': '0.2.0',
    'description': 'A python library and framework for fast neural network computations.',
    'long_description': '# Fast Neural Networks (FastNN)\n\nA framework for deploying serializable and optimizable neural net models at scale in production via. the NVIDIA Triton Inference Server.\n\n<p align="center">\n    <a href="https://hub.docker.com/r/aychang/fastnn">\n        <img src="https://img.shields.io/docker/cloud/build/aychang/fastnn"\n    </a>\n    <a href="https://badge.fury.io/py/fastnn">\n        <img src="https://badge.fury.io/py/fastnn.svg">\n    </a>\n    <a href="https://github.com/aychang95/fastnn/blob/master/LICENSE">\n        <img src="https://img.shields.io/github/license/aychang95/fastnn">\n    </a>\n</p>\n\n## [**FastNN Docker Release Selector (Ubuntu 18.04)**](https://andrewchang.dev/fastnn/index.html#fastnn-docker-release-selector-ubuntu-1804)\n\n## [Documentation](https://andrewchang.dev/fastnn) - Guides, Models, API References\n\n## Features:\n  - **Data Processing**\n    - Intuitive data processing modules for encoding human-readible data into tensors compatible with deep learning libraries\n  - **Model Exporting**\n    - FastNN torch modules and tools for exporting models via. `TorchScript` tracing and scripting to a production environment\n  - **Model Zoo**\n    - Various exported models hosted in this repo via. git-lfs and AWS S3. Includes models from the HuggingFace\'s Transformers and \n    TorchVision\n  - **Model Deployment**\n    - Deploy models using Triton Inference Server on CPU/GPU-compatible server(s) with helm or docker\n  - **FastNN Client**\n    - Client wrapper for Triton Inference Server\'s client module for programmatic requests with python\n\n\n## Pre-Requisites:\n\nGit LFS is required if you\'d like to use any of the models provided by FastNN in `./model_repository`.\n\nCloning this repository without Git LFS will clone a repository with LFS pointers, not the actual model.\n\nAfter the repository is cloned and Git LFS is installed, set up with `git lfs install`.\n\nDownload specific models with:\n\n```sh\ngit lfs pull --include="model_repository/<path-to-model-dir>" --exclude=""\n```\n\nDownload ALL models with:\n\n```sh\ngit lfs pull\n\n# Or\n#git lfs pull --include="*" --exclude=""\n```\n\n\n## Quickstart and Installation:\n\n### *Pre-requisites:*\n\nRequirements: Python 3.7+, PyTorch 1+, TorchVision 0.7+, Triton Client\n\nOptional: CUDA Compatible GPU, NVIDIA Drivers, cudnn (PyTorch pre-built wheels)\n\n1. To install PyTorch with TorchVision, please refer to the installation instructions on their web page [here](https://pytorch.org/get-started/locally/#start-locally).\n\n2. The tritonclient package wheels are not hosted on the public PyPI server. We need to add the address of NVIDA\'s private python package index to the environment. You can complete these steps and install the tritonclient package by running the following.\n\n```sh\n# If you cloned this repo, you can just uncomment and run the one line below\n#sh ./scripts/install_triton_client.\npip install nvidia-pyindex\npip install tritonclient[all]\n```\n\n### **Install via. pip**\n\nOnce the above requirements are set, you can install fastnn with the command below:\n\n```sh\npip install fastnn\n```\n\nIf you are comfortable with the latest default stable releases of PyTorch you can skip step 1 in the pre-requisites and run `pip install fastnn[torch]` instead.\n\n\n### **Install from source with Poetry for development**\n\nYou will need to install poetry by referring to the installation instructions on their web page [here](https://python-poetry.org/docs/#installation).\n\nAfter cloning the repository, just run `poetry install` to install with the .lock file.\n\nActivate the virtual environment with the command below:\n\n```sh\npoetry shell\n```\n\n\n### **Docker**\n\nOfficial FastNN images are hosted on [Docker Hub](https://hub.docker.com/r/aychang/fastnn).\n\nSelect FastNN package and image versions by referencing the [documentation](https://andrewchang.dev/fastnn/index.html#fastnn-docker-release-selector-ubuntu-1804). Development and runtime environments are available.\n\nJupyter lab and notebook servers are accessible with notebook examples and terminal access `localhost:8888` with every image.\n\n\nRun the latest FastNN image by running below:\n\n```sh\ndocker run --gpus all --rm -it -p 8888:8888 aychang/fastnn:latest\n```\n\nRun images with specific configurations as can see in the example command below:\n\n```sh\ndocker run --gpus all --rm -it -p 8888:8888 aychang/fastnn:0.1.0-cuda11.0-runtime-ubuntu18.04-py3.7\n\n```\n\n\n## Triton Inference Server: Local or Kubernetes Cluster\n\n\n### **Local Deployment**\n\nRequirements:\n  - Docker 19.03+\n\nGPU Inference Requirements:\n\n  - NVIDIA CUDA-Compatible GPU\n  \n  - [NVIDIA Container Toolkit (nvidia-docker)](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)\n\nLocal deployment of the Triton Server uses the EXPLICIT model control mode. Local models must be explicitly specified with the `--load-model` \nargument in `./scripts/start_triton_local.sh`\n\n```sh\n\nexport MODEL_REPOSITORY=$(pwd)/model_repository\nsh ./scripts/start_triton_local.sh\n\n```\n\n\n### **Helm Chart install in Kubernetes Cluster**\n\nRequirements: kubectl 1.17+, Helm 3+, Kubernetes 1.17+\n\nYou can currently install the local FastNN helm chart with the following instuctions:\n\n```sh\n\ncd ./k8s\nhelm install fastnn .\nexport MODEL_REPOSITORY=$(pwd)/model_repository\n\n```\n\nNote: The current local helm chart installation deploys Triton using the NONE model control mode. All models available in the S3 Model Zoo will be deployed...good luck. \nDeployed models and model control mode can be edited in the helm chart deployment configuration file.\n\n# License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Andrew Chang',
    'author_email': 'aychang995@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://andrewchang.dev/fastnn/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
