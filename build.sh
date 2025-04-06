#!/bin/bash

# Build whl
uv build

# Build image
docker build -t avidito/revirathya-toolbox:0.1.0 .