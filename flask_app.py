# Import lmeibraries
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
from collections import defaultdict
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


def run_getreportid(filename):
    logging.info('Loading data: %s', data)
    results = save.getreportid(filename)
    return results

def run_savereportsingests(data):
    '''
    - General idea is save all the data into the database.
   
    REPORTS TABLE
    - Get all unique report filenames from data
       - for each filename, create an entry for each row in the reports table
       - if creation fails, include error in this report filename with reason as report exists.
       - Record the filename with error

    INGESTS TABLE
    - FOr each item in data (skip those with filename in error)
          - Get the id for that item.
          - create an entry for this item in the ingests table.
          - If there's error, include error in report
    
    '''
    logging.info("Startig saving operations")
    logging.debug("DATA %s  TYPE %s", data, type(data))
    if isinstance(data, str):
        data = json.loads(data)
    from datetime import datetime
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    filedict=defaultdict(str)
    for datarow in data:
        filedict[datarow["filename"]]=0
    uniquefilenamelist=filedict.keys()
    
    #filenamelist= [data[x] for x in ['filename']]
    #uniquefilenamelist = list(set(filenamelist))

    #REPORTS TABLE
    logging.debug("Saving reports")
    failed=[]
    filenameidpair={"fake":None}
    for filename in uniquefilenamelist:
        logging.debug("Processing %s", filename)
        reportrecord={"reports":[{"filename":filename,"created_at":now,"ingested_at":now,"currentloc":"PROCESSING"}]}      
        totalcount=saver.create(reportrecord)
        if totalcount==0:
            failed.append(filename)
    
    logging.debug("Saving ingests")
    #INGESTS TABLE
    failedingest=[]
    for datarow in data:
        if datarow["filename"] in failed:
            failjson.append({"filename":datarow["filename"], "id":datarow["id"], "error":"report already exists"})
        else:
            ingestrecord={"ingests":[{"text":datarow["content"],"section":datarow["section"],"created_at":now,"ingest_id":datarow["filename"],"predicted_category":datarow["class"]}]}
            totalcount=saver.create(ingestrecord)
            if totalcount==0:
               failedingest.append(datarow["id"])
    
    failedreportsjson=[]
    failedingestsjson=[]
    for failedreport in failed:
        failedreportsjson.append({"filename":failedreport,"error":"Report already exists"})
    for failedingest in failedingests:
        failedingestsjson.append({"id":failedingest,"error":"Ingestion failed for some reason"})
    logging.info("Saving opertations completed, retuning results")
    return {"failreports":failedreportsjson.append,"failingests":failedingestsjson.append}
    
    
    
    
        

# Instantiate the Node
app = Flask(__name__)

@app.route('/savereports', methods=['POST'])
def savereports_get():

    if request.method == 'POST':
        request_json = request.get_json(force=True)
        result = run_savereports(request_json)
        
        response_msg = json.dumps(result)
        response = {
           'results': response_msg
        }
        return jsonify(response), 200

@app.route('/saveingests',methods=['POST'])
def saveingests_get():
    if request.method == 'POST':
        request_json = request.get_json(force=True)
        result = run_saveingests(request_json)
        response_msg = json.dumps(result)
        response = {
           'results': response_msg
        }
        return jsonify(response), 200


@app.route('/updateingests',methods=['POST'])
def updateingests_get():
    if request.method == 'POST':
        request_json = request.get_json(force=True)
        result = run_updateingests(request_json)
        response_msg = json.dumps(result)
        response = {
           'results': response_msg
        }
        return jsonify(response), 200

@app.route('/getreportid',methods=['POST'])
def getreportid_get():
    if request.method =='POST':
        request_json = request.get_json(force=True)
        result = run_getreportid(request_json)
        response_msg = json.dumps(result)
        response = {
           'results': response_msg
        }
        return jsonify(response), 200       

@app.route('/savecontent',methods=['POST'])
def savecontent_get():
    logging.info("Received quest to save conetnt")
    if request.method =='POST':
        logging.debug("Extracting JSON content")
        request_json = request.get_json(force=True)
        logging.debug("Pass savnig operation to worker function")
        result = run_savereportsingests(request_json)
        logging.debug("Saving operation completes...dumping results")
        response_msg = json.dumps(result)
        response = {
           'results': response_msg
        }
        return jsonify(response), 200


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
