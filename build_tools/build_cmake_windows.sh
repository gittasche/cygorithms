#!/bin/bash

python -m pip install cmake

cd cygorithms_ctypes

mkdir build
cd build
cmake .. -G"Visual Studio 17 2022" -DCMAKE_CONFIGURATION_TYPES="Release" -A x64
cmake --build . build64 --config Release

cd ../../
