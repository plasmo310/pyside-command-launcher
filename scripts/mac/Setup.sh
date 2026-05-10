#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Set install env
PYTHON_VERSION=3.13.13
PYTHON_BIN_DIR="$ROOT_DIR/bin"
VENV_DIR="$ROOT_DIR/.venv"

# Check for python
PYTHON_EXE=""
if command -v python3 &>/dev/null; then
    PYTHON_EXE="python3"
elif command -v python &>/dev/null; then
    PYTHON_EXE="python"
else
    echo "Python is not installed. Please install Python $PYTHON_VERSION."
    exit 1
fi

# Check python version
INSTALLED_VERSION=$($PYTHON_EXE -c 'import platform; print(platform.python_version())')
if [[ "$INSTALLED_VERSION" != "$PYTHON_VERSION" ]]; then
    echo "Warning: Python $PYTHON_VERSION is recommended, but $INSTALLED_VERSION is installed."
fi

# Create venv
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON_EXE -m venv "$VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

pip install --upgrade pip

if [ -f "$ROOT_DIR/requirements.txt" ]; then
    pip install -r "$ROOT_DIR/requirements.txt"
fi

echo "Complete setup Python $PYTHON_VERSION venv."
