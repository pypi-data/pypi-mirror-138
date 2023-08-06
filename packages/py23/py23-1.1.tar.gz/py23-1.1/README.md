[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/vb64/py23/Py23?label=Python%202.7%203.6%203.7%203.8%203.9%203.10&style=plastic)](https://github.com/vb64/py23/actions?query=workflow%3A%22Py23%22)
# py23
Python 2/3 compatible functions

## Installation

```
$ pip install py23
```

## Usage

```python

import os
from py23 import load_module_by_path

py_module = load_module_by_path(os.path.join('py23', '__init__.py')
callable(py_module.remove_symbols)
True
```

## Development

```
$ git clone git@github.com:vb64/py23.git
$ cd py23
```
With Python 3:
```
$ make setup PYTHON_BIN=/path/to/python3/executable
```
With Python 2:
```
$ make setup2 PYTHON_BIN=/path/to/python2/executable
```
Run autotests
```
$ make tests
```
