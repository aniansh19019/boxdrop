#!/bin/bash 
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
MAIN_PATH="${SCRIPT_DIR}/client/main.py"
PYTHON_PATH="${SCRIPT_DIR}/.env/bin/python"
# echo $SCRIPT_DIR $MAIN_PATH $PYTHON_PATH
cd $SCRIPT_DIR
virtualenv -p python3 .env
source .env/bin/activate
pip install boto3 firebase_admin pyrebase4 pika maskpass fastcdc watchdog sqlitedict
deactivate
