#!/bin/bash
set -e

# Create pip_cache directory if it doesn't exist
mkdir -p pip_cache

# Download all dependencies including sub-dependencies
pip3 download --only-binary=:all: \
    --platform manylinux_2_17_x86_64 \
    --python-version 3.11 \
    --implementation cp \
    --abi cp311 \
    --dest pip_cache \
    -r requirements.txt

echo "All wheel files downloaded successfully to pip_cache directory" 