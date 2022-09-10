#!/bin/bash

set -e
set -x

cd ../../

python -m venv build_env
build_env/Scripts/activate

python -m pip install Cython
python -m pip install twine

cd cygorithms/cygorithms
python setup.py build_ext --inplace
python setup.py sdist

twine check dist/*.tar.gz
