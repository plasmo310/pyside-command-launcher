#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BUILD_ENV_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
ROOT_DIR="$(cd "$BUILD_ENV_DIR/.." && pwd)"

PYTHON_EXE="$BUILD_ENV_DIR/.venv/bin/python"
if [ ! -f "$PYTHON_EXE" ]; then
    echo "Not found python env. Please execute 'build_env/scripts/mac/Setup.sh'."
    read -r -p "Press Enter to continue..."
    exit 1
fi

export PYTHONDONTWRITEBYTECODE=1
PYTHON_SRC_DIR="$ROOT_DIR/python"
PYTHON_RESOURCES_DIR="$ROOT_DIR/resources"
DATA_DIR="$ROOT_DIR/data"

VENV_DIR="$BUILD_ENV_DIR/.venv"
source "$VENV_DIR/bin/activate"

cd "$BUILD_ENV_DIR" || exit 1

BUILD_TMP_DIR="$SCRIPT_DIR/build"
BUILD_DIST_DIR="$SCRIPT_DIR/dist"

EXE_NAME="CommandLauncher"
ICON_PATH="$ROOT_DIR/resources/icon/tool_icon_round.icns"

# References: https://pyinstaller.org/en/stable/usage.html
pyinstaller --noconsole --onedir --name "$EXE_NAME" --hidden-import "PySide6" --paths "$PYTHON_SRC_DIR" "$BUILD_ENV_DIR/python/run.py" --add-data "$PYTHON_RESOURCES_DIR:./resources" --icon "$ICON_PATH" --distpath "$BUILD_DIST_DIR" --workpath "$BUILD_TMP_DIR"

# Copy data
mkdir -p "$BUILD_DIST_DIR/$EXE_NAME/data"
cp -R "$DATA_DIR/mac" "$BUILD_DIST_DIR/$EXE_NAME/data/"

mkdir -p "$BUILD_DIST_DIR/$EXE_NAME.app/Contents/data"
cp -R "$DATA_DIR/mac" "$BUILD_DIST_DIR/$EXE_NAME.app/Contents/data/"

# Clean up
rm -rf "$BUILD_TMP_DIR"
find "$PYTHON_SRC_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

echo "Complete build app."
read -r -p "Press Enter to continue..."
