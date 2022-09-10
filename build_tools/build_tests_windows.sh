#!/bin/bash

set -e
set -x

cd ../../

python -m venv test_env
test_env/Scripts/activate

python -m pip install cygorithms/cygorithms/.
python -m pip install pytest

cd cygorithms/cygorithms
python -m pytest tests/
