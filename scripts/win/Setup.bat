@echo off

set SCRIPT_DIR=%~dp0
set ROOT_DIR=%SCRIPT_DIR%..\..

REM Set Install Env.
set PYTHON_VERSION=3.13.13
set PYTHON_BIN_DIR=%ROOT_DIR%\bin
set VENV_DIR=%ROOT_DIR%\.venv

REM Install Python.
if not exist %PYTHON_BIN_DIR% (
    mkdir %PYTHON_BIN_DIR%
)
if not exist %PYTHON_BIN_DIR%\nuget.exe (
    curl -L -o %PYTHON_BIN_DIR%\nuget.exe https://dist.nuget.org/win-x86-commandline/latest/nuget.exe
)
%PYTHON_BIN_DIR%\nuget.exe install python -Version %PYTHON_VERSION% -OutputDirectory %PYTHON_BIN_DIR%
set PYTHON_EXE=%PYTHON_BIN_DIR%\python.%PYTHON_VERSION%\tools\python.exe

REM Create venv.
%PYTHON_EXE% -m venv %VENV_DIR%
call %VENV_DIR%\Scripts\activate
python -m pip install --upgrade pip
if exist %ROOT_DIR%\requirements.txt (
    pip install -r %ROOT_DIR%\requirements.txt
)

REM Clean up.
del %PYTHON_BIN_DIR%\nuget.exe

echo Complete setup Python %PYTHON_VERSION% venv.
pause
