#!/bin/sh
set -x -e

# ruff
ruff check .

# Check formatting
ruff format --check .

# mypy
mypy

# pytest
pytest .
