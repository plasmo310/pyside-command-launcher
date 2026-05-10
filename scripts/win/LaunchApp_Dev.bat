@echo off

set SCRIPT_DIR=%~dp0
set ROOT_DIR=%SCRIPT_DIR%..\..

set PYTHON_EXE=%ROOT_DIR%\.venv\Scripts\python.exe
if not exist %PYTHON_EXE% (
    echo Not found python env. Please execute 'scripts\win\Setup.bat'.
    pause
    exit /b 1
)

set PYTHONDONTWRITEBYTECODE=1
set PYTHONPATH=%ROOT_DIR%\python

set PARAM_JSON_PATH=%ROOT_DIR%\data\win\ItemData_Dev.json
if not exist "%PARAM_JSON_PATH%" (
    echo Not found json file. Please create a json file at the following path.
    echo %PARAM_JSON_PATH%
    pause
    exit /b 1
)

"%PYTHON_EXE%" -m cmdlaunch.main --json-path "%PARAM_JSON_PATH%"
