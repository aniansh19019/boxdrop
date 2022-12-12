#!/bin/bash 
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
MAIN_PATH="${SCRIPT_DIR}/client/main.py"
PYTHON_PATH="${SCRIPT_DIR}/.env/bin/python"
CLIENT_DIR="${SCRIPT_DIR}/client"
# Executing script
cd $CLIENT_DIR
$PYTHON_PATH $MAIN_PATH