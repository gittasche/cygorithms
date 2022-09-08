#!/bin/bash

set -e
set -x

cd ../../

python -m venv test_env
source test_env/bin/activate

python -m cygorithms/cygorithms
python -m pip install pytest

cd cygorithms/cygorithms
python -m pytest tests/
