@echo off

:: Check if codeql command is executable
where codeql >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: codeql command not found. Please install CodeQL.
    exit /b 1
)

:: Check Python version
for /f "tokens=2 delims= " %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
for /f "tokens=1 delims=." %%i in ("%PYTHON_VERSION%") do set PYTHON_MAJOR=%%i
for /f "tokens=2 delims=." %%i in ("%PYTHON_VERSION%") do set PYTHON_MINOR=%%i

if "%PYTHON_MAJOR%"=="3" (
    if "%PYTHON_MINOR%" geq "6" (
        echo Python version is OK: %PYTHON_VERSION%
    ) else (
        echo Error: Unsupported Python version. Please use Python 3.6 or above.
        exit /b 1
    )
) else (
    echo Error: Python 2 detected. Please use Python 3.6 or above.
    exit /b 1
)

:: Check if npm and nodejs are installed
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: npm command not found. Please install Node.js and npm.
    exit /b 1
)
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: node command not found. Please install Node.js and npm.
    exit /b 1
)

:: Prompt user to enter project root directory
set /p PROJECT_DIR=Please enter the absolute path to your project directory: 

:: Navigate to project root directory and install dependencies
cd /d "%PROJECT_DIR%" || exit /b 1
npm install

if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo Warning: requirements.txt not found in project root directory.
)


:: Navigate to wxappUnpacker directory and install dependencies
cd /d "%PROJECT_DIR%\wxappUnpacker" || exit /b 1
npm install esprima
npm install css-tree
npm install cssbeautify
npm install vm2
npm install uglify-es
npm install js-beautify
npm install .

:: Install dependencies in /baidu_smapp_unpacker
cd /d "%PROJECT_DIR%\baidu_smapp_unpacker" || exit /b 1
npm install

:: Prompt user to configure config.ini
echo Please configure your config.ini with the following content (use absolute paths):
echo.
echo [Query Paths]
echo ; Directory where the WeChat mini-programs are stored
echo ; miniapp_dict = C:/Users/Administrator/Documents/WeChat Files/Applet
echo e.g. miniapp_dict = E:/MiniCAT_Linux_sync/miniapp_dict
echo ; Directory where this script is stored. After querying, res/ etc. directories will be generated here
echo e.g. query_dir = E:/MiniCAT_Linux_sync/MiniCAT
echo ; Dec_dir, make sure this directory has enough disk storage.
echo e.g. dec_dir = E:/MiniCAT_Linux_sync/dec_dir


:: Prompt user for project entry point
echo Project entry point is main_reborn.py in the project directory. Use -h to see help information.
