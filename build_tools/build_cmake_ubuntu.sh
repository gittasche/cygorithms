#!/bin/bash

sudo apt-get install -y --no-install-recommends ninja-build

cd cygorithms_ctypes

mkdir build
cd build
cmake .. -DBUILD_STATIC_LIB=OFF -GNinja
cmake --build .

cd ../../
