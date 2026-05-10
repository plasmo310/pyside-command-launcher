@echo off

set SCRIPT_DIR=%~dp0
set BUILD_ENV_DIR=%SCRIPT_DIR%..\..
set ROOT_DIR=%SCRIPT_DIR%..\..\..
pushd %BUILD_ENV_DIR%

set PYTHON_EXE=%BUILD_ENV_DIR%\.venv\Scripts\python.exe
if not exist %PYTHON_EXE% (
    echo Not found python env. Please execute 'build_env\scripts\win\Setup.bat'.
    pause
    exit /b 1
)

set PYTHONDONTWRITEBYTECODE=1
set PYTHON_SRC_DIR=%ROOT_DIR%\python
set PYTHON_DATA_DIR=%ROOT_DIR%\data
set PYTHON_RESOURCES_DIR=%ROOT_DIR%\resources
set DATA_DIR=%ROOT_DIR%\data

set VENV_DIR=%BUILD_ENV_DIR%\.venv
call %VENV_DIR%\Scripts\activate

set BUILD_TMP_DIR=%SCRIPT_DIR%build
set BUILD_DIST_DIR=%SCRIPT_DIR%dist

set EXE_NAME=CommandLauncher
set ICON_PATH=%ROOT_DIR%\resources\icon\tool_icon_rect.ico

REM References: https://pyinstaller.org/en/stable/usage.html
pyinstaller --noconsole --onedir --name %EXE_NAME% --hidden-import "PySide6" --paths %PYTHON_SRC_DIR% %BUILD_ENV_DIR%\python\run.py --add-data "%PYTHON_RESOURCES_DIR%;.\resources" --icon %ICON_PATH% --distpath %BUILD_DIST_DIR% --workpath %BUILD_TMP_DIR%

REM Copy data.
xcopy /E /I /Y "%DATA_DIR%\win" "%BUILD_DIST_DIR%\%EXE_NAME%\data\win"

popd

REM Clean up.
powershell -Command "Remove-Item -Recurse -Force '%BUILD_TMP_DIR%' -ErrorAction SilentlyContinue"
powershell -Command "Get-ChildItem -Recurse -Filter '__pycache__' '%PYTHON_SRC_DIR%' | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue"

echo Complete build app.
pause
