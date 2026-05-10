@echo off

set SCRIPT_DIR=%~dp0
set BUILD_ENV_DIR=%SCRIPT_DIR%..\..
set ROOT_DIR=%SCRIPT_DIR%..\..\..

REM Set Install Env.
set PYTHON_VERSION=3.13.13
set PYTHON_BIN_DIR=%ROOT_DIR%\bin
set PYTHON_EXE=%PYTHON_BIN_DIR%\python.%PYTHON_VERSION%\tools\python.exe
set VENV_DIR=%BUILD_ENV_DIR%\.venv

REM Check Python bin.
if not exist %PYTHON_EXE% (
    echo Python not found in %PYTHON_BIN_DIR%.
    echo Please run 'scripts\win\Setup.bat' in the root directory first.
    pause
    exit /b 1
)

REM Create venv.
%PYTHON_EXE% -m venv %VENV_DIR%
call %VENV_DIR%\Scripts\activate
python -m pip install --upgrade pip
if exist %BUILD_ENV_DIR%\requirements.txt (
    pip install -r %BUILD_ENV_DIR%\requirements.txt
)

echo Complete setup Python %PYTHON_VERSION% venv.
pause
