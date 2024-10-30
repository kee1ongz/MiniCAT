#!/bin/bash

# Check if codeql command is executable
if ! command -v codeql &> /dev/null
then
    echo "Error: codeql command not found. Please install CodeQL."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1)
if [[ $PYTHON_VERSION == *"Python 3."* && ${PYTHON_VERSION:9:1} -ge 6 ]]; then
    echo "Python version is OK: $PYTHON_VERSION"
else
    if [[ $PYTHON_VERSION == *"Python 2."* ]]; then
        echo "Error: Python 2 detected. Please use Python 3.6 or above."
    else
        echo "Error: Unsupported Python version. Please use Python 3.6 or above."
    fi
    exit 1
fi

# Check if npm and nodejs are installed
if ! command -v npm &> /dev/null || ! command -v node &> /dev/null
then
    echo "Error: npm and/or nodejs command not found. Please install Node.js and npm."
    exit 1
fi

# Prompt user to enter project root directory
read -p "Please enter the absolute path to your project directory: " PROJECT_DIR

# Navigate to project root directory and install dependencies
cd "$PROJECT_DIR" || exit
npm install

if [ -f requirements.txt ]; then
    pip3 install -r requirements.txt
else
    echo "Warning: requirements.txt not found in project root directory."
fi


cd "$PROJECT_DIR/wxappUnpacker" || exit
npm install esprima
npm install css-tree
npm install cssbeautify
npm install vm2
npm install uglify-es
npm install js-beautify
npm install .

# Install dependencies in /baidu_smapp_unpacker
cd "$PROJECT_DIR/baidu_smapp_unpacker" || exit
npm install

# Prompt user to configure config.ini
cat << EOF
Please configure your config.ini with the following content (USE ABSOLUTE PATHS):

[Query Paths]
; Directory where the WeChat mini-programs are stored
e.g miniapp_dict = C:/Users/Administrator/Documents/WeChat Files/Applet
miniapp_dict = E:/MiniCAT_Linux_sync/miniapp_dict
; Directory where this script is stored. After querying, res/ etc. directories will be generated here
e.g query_dir = E:/MiniCAT_Linux_sync/MiniCAT
; Dec_dir, make sure this directory has enough disk storage.
e.g dec_dir = E:/MiniCAT_Linux_sync/dec_dir

EOF


echo "Project entry point is main_reborn.py in the project directory. Use -h to see help information."
