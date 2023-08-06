# melter

Identifies unsolved cases that should be analysed again.

## Installation

### For users
Install melter in an environment with python 3.9:
```bash
$ pip install melter
```

### For developers
Clone the repository:
```bash
$ git clone git@github.com:Clinical-Genomics/melter.git
```
Enter the root folder of the project:
```bash
$ cd melter/
```
Create the melter environment:
```bash
$ conda env create -f environment.yaml
```
Activate the melter environment:
```bash
$ conda activate melter
```
If poetry is not installed, install poetry via:
```bash
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
To configure your current shell:
```bash
$ source $HOME/.poetry/env
```
Install dependencies:
```bash
$ poetry install
```

## Usage

To see available commands:
```bash
$ melter --help
```

## License

`melter` was created by Henning Onsbring. It is licensed under the terms of the MIT license.
