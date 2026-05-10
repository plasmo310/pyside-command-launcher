#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

VENV_DIR="$ROOT_DIR/.venv"
PYTHON_EXE="$VENV_DIR/bin/python"
if [ ! -f "$PYTHON_EXE" ]; then
    echo "Not found python env. Please execute 'scripts/mac/Setup.sh'."
    read -r -p "Press Enter to continue..."
    exit 1
fi

export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$ROOT_DIR/python"

source "$VENV_DIR/bin/activate"

PARAM_JSON_PATH="$ROOT_DIR/data/mac/ItemData_Dev.json"
if [ ! -f "$PARAM_JSON_PATH" ]; then
    echo "Not found json file. Please create a json file at the following path."
    echo "$PARAM_JSON_PATH"
    read -r -p "Press Enter to continue..."
    exit 1
fi

"$PYTHON_EXE" -m cmdlaunch.main --json-path "$PARAM_JSON_PATH"
