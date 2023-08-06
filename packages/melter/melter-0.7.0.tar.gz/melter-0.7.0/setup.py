# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['melter']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0', 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['melter = melter.main:app']}

setup_kwargs = {
    'name': 'melter',
    'version': '0.7.0',
    'description': 'Identifies unsolved cases that should be analyzed again',
    'long_description': '# melter\n\nIdentifies unsolved cases that should be analysed again.\n\n## Installation\n\n### For users\nInstall melter in an environment with python 3.9:\n```bash\n$ pip install melter\n```\n\n### For developers\nClone the repository:\n```bash\n$ git clone git@github.com:Clinical-Genomics/melter.git\n```\nEnter the root folder of the project:\n```bash\n$ cd melter/\n```\nCreate the melter environment:\n```bash\n$ conda env create -f environment.yaml\n```\nActivate the melter environment:\n```bash\n$ conda activate melter\n```\nIf poetry is not installed, install poetry via:\n```bash\n$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -\n```\nTo configure your current shell:\n```bash\n$ source $HOME/.poetry/env\n```\nInstall dependencies:\n```bash\n$ poetry install\n```\n\n## Usage\n\nTo see available commands:\n```bash\n$ melter --help\n```\n\n## License\n\n`melter` was created by Henning Onsbring. It is licensed under the terms of the MIT license.\n',
    'author': 'Henning Onsbring',
    'author_email': 'henning.onsbring@scilifelab.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
