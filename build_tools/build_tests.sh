#!/bin/bash

set -e
set -x

cd ../../

python -m venv test_env
source test_env/bin/activate

python -m pip install cygorithms/cygorithms/*.tar.gz
python -m pip install pytest

cd cygorithms/cygorithms
python -m pytest tests/
