CYgorithms
==========

[![Build Status](https://github.com/gittasche/cygorithms/actions/workflows/build.yml/badge.svg)](https://github.com/gittasche/cygorithms/actions)

About
-----

**CYgorithms** is a Python package with implementation of classical algorithms and data
structures using Cython and C extensions.

This package also is an example of using Cython, Ctypes and Python C API together.

Installation
------------

Create Anaconda environment

```bash
conda env --file environment.yml
conda activate cyalg-env
```

Install package via ``pip``

```bash
cd cygorithms
python -m pip install .
```

Build source in development purposes

```bash
cd cygorithms
python -m setup.py build_ext --inplace
python -m setup.py install
```

Testing
-------

Run tests with pytest

```bash
cd cygorithms
python -m pip install .[tests]
python -m pytest tests/
```
