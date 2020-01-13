# Import libraries
import os
import sys
import random
import math
import re
import time
import logging
import argparse
import json
import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
import requests
from flask import Flask, jsonify, request

from time import sleep
sleep(15)
# Root directory of the project
ROOT_DIR = os.path.abspath("../")
sys.path.append(ROOT_DIR)  # To find local version of the library

# Logging confg
logging.basicConfig(level=logging.DEBUG,handlers=[
                   logging.FileHandler("{0}/{1}.log".format(".", "log")),
                   logging.StreamHandler()
                ] ,
                format="%(asctime)-15s %(levelname)-8s %(message)s")

############################################################
#  Configurations
#  Inherits from config.py
############################################################
from config import SaverConfig
config = SaverConfig()
PREFIX_PATH=config.SHARED_DATA_PATH
# Create model object in inference mode.
module = __import__(config.MODEL_MODULE, fromlist=[config.MODEL_CLASS])
my_class = getattr(module,config.MODEL_CLASS)
saver = my_class()
print("{}.{} loaded successfully!".format(config.MODEL_MODULE,config.MODEL_CLASS))

def run_savereports(data):
    # Expecting {filename:'path'}
    logging.info('Loading data: %s', data)
    results=saver.create(data)
    return results

def run_saveingests(data):
    logging.info('Loading data: %s',data)
    results=saver.create(data)
    return results

def run_updateingests(data):
    logging.info('Loading data: %s',data)
    results = saver.update(data)
    return results

# Instantiate the Node
app = Flask(__name__)

@app.route('/savereports', methods=['POST'])
def savereports_get():

    if request.method == 'POST':
        request_json = request.get_json(force=True)
        result = run_savereports(request_json)
        
        response_msg = json.dumps(result)
        return jsonify(response_msg), 200

@app.route('/saveingests',methods=['POST'])
def saveingests_get():
    if request.method == 'POST':
        request_json = request.get_json(force=True)
        result = run_saveingests(request_json)
        response_msg = json.dumps(result)
        return jsonify(response_msg), 200


@app.route('/updateingests',methods=['POST'])
def updateingests_get():
    if request.method == 'POST':
        request_json = request.get_json(force=True)
        result = run_updateingests(request_json)
        response_msg = json.dumps(result)
        return jsonify(response_msg), 200

@app.route('/test',methods=['GET'])
def test_get():
    return jsonify('ok'), 200

if __name__ == '__main__':

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=9898, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port, debug=True)
