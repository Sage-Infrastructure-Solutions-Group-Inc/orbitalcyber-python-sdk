# Package Build Instructions
This document describes the process that must be followed to build and deploy this package to PyPi.

## Prerequisites
Aside from the obvious prerequisite of Python3, you will also need to install the latest version of the twine and build python modules. These modules can be installed with the command below on most systems:
```bash
python3 -m install --upgrade twine build
```

## Building
To build the package change to this directory and run the following command:
```bash
python3 -m build
```

## Uploading
To upload the package you will need to use the following command:
```bash
# TestPyPi
python3 -m twine upload --repository testpypi dist/*
# Production
python3 -m twine upload --repository pypi dist/*
```