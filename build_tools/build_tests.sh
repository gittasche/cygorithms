#!/bin/bash

set -e
set -x

cd ../../

python -m venv test_env
source test_env/bin/activate

python -m pip install pytest

cd cygorithms/cygorithms
ls
python -m pip install .
python -m pytest /tests
