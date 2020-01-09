[![Extraction Service](https://github.com/jax79sg/artyins-extractionservice/raw/master/images/SoftwareArchitectureExtractionService.jpg)]()

# Extraction Service For artyins deployment architecture
This is a submodule for the artyins architecture. Please refer to [main module](https://github.com/jax79sg/artyins) for full build details.

[![Build Status](https://travis-ci.com/jax79sg/artyins-extractionservice.svg?branch=master)](https://travis-ci.com/jax79sg/artyins-extractionservice)

Refer to [Trello Task list](https://trello.com/c/mKnW1fgx) for running tasks.

---

## Table of Contents (Optional)

- [Usage](#Usage)
- [Virtualenv](#Virtualenv)
- [Tests](#Tests)

---

## Usage
The extraction service can be called by a HTTP POST call. Primarily on http://webserverip:port/extract_content. It expects a json of the following format
```python
[{'filename':'file01.pdf',},{'filename':'file02.pdf'}]
```
### config.py
The configuration file will indicate the extractor class to use. For testing purposes, the tika library is used. 
```python
class ExtractorConfig():    
    MODEL_MODULE="extractors.tikextractor"
    MODEL_CLASS="TIKExtractor"
    SHARED_DATA_PATH="/mnt/shareddata" #The path to which the raw reports must be found
```

### Abstract Extraction Class
All implementations of extractors must implement this abstract class.
```python
from abc import ABC, abstractmethod
class ExtractorInterface(ABC):
    """  An abstract base class for report extraction tools """

    @abstractmethod
    def __init__(self):
        raise NotImplementedError()

    @abstractmethod
    def extract(self, fileobject):
        raise NotImplementedError()
```

### An example on how to implement the Abstract Extraction class
```python
from extractors.extractor import ExtractorInterface
import os
from config import ExtractorConfig
import tika
from tika import parser

class TIKExtractor(ExtractorInterface):
    
    def __init__(self,config=None):
        if config == None:
           config = ExtractorConfig() 
        tika.initVM()

    def extract(self, fileobject):
        parsed = parser.from_file(fileobject)
        return parsed["content"]

if __name__=="__main__":
    myextractor = TIKExtractor()
    content=myextractor.extract(open('test.pdf'))	
    print("Test content:\n",content)
```

### Adding your extraction into Web Service
You will need to add your extraction function into the Web Service (flask_app.py). Here is an example, you may simply add your functions.
```python
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

# Root directory of the project
ROOT_DIR = os.path.abspath("../")
sys.path.append(ROOT_DIR)  # To find local version of the library

# Logging confg
logging.basicConfig(level=logging.DEBUG, filename="log", filemode="a+",
                format="%(asctime)-15s %(levelname)-8s %(message)s")

############################################################
#  Configurations
#  Inherits from config.py
############################################################
from config import ExtractorConfig
config = ExtractorConfig()
PREFIX_PATH=config.SHARED_DATA_PATH
# Create model object in inference mode.
module = __import__(config.MODEL_MODULE, fromlist=[config.MODEL_CLASS])
my_class = getattr(module,config.MODEL_CLASS)
extractor = my_class()
print("{}.{} loaded successfully!".format(config.MODEL_MODULE,config.MODEL_CLASS))

def run_extract_content(data):
    # Expecting {filename:'path'}
    logging.info('Loading data: %s', data)
    allresults=[]
    for entry in data:
        print("Processing: ",entry['filename'])
        results = extractor.extract(PREFIX_PATH+entry['filename'])
        myresult={'filename':entry['filename'],'content':results}
        print(myresult)
        allresults.append(myresult)

    return allresults


# Instantiate the Node
app = Flask(__name__)

@app.route('/extract_content', methods=['POST'])
def extract_content_get():

    if request.method == 'POST':
        request_json = request.get_json(force=True)
        result = run_extract_content(request_json)
        
        response_msg = json.dumps(result)
        #response = {
        #   'message': response_msg
        #}
        return jsonify(response_msg), 200


if __name__ == '__main__':

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=9898, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port, debug=True)
```
---

## Virtualenv
```shell
python3 -m venv venv
source venv/bin/activate
pip install --user -r requirements.txt`
```
---

## Tests 
This repository is linked to [Travis CI/CD](https://travis-ci.com/jax79sg/artyins-extractionservice). You are required to write the necessary unit tests if you introduce more extraction classes.
### Unit Tests
```python
import unittest

class TestModels(unittest.TestCase):

    def test_tikextractor(self):
        print("Running tikextractor")
        from extractors.tikextractor import TIKExtractor
        myextractor = TIKExtractor()
        
        results=myextractor.extract("test.pdf")
        print(results)

if __name__ == '__main__':
    unittest.main()
```

### Web Service Test
```
#Start gunicorn wsgi server
gunicorn --bind 0.0.0.0:9898 --daemon --workers 1 wsgi:app
```
### Send test POST request
```python
import requests 

URL = "http://localhost:9898/extract_content"
DATA = [{'filename':'/test.pdf',},{'filename':'/test2.pdf'}]
  
# sending get request and saving the response as response object 
r = requests.post(url = URL, json  = DATA) 
print(r) 
# extracting results in json format 
data = r.json()
print("Data sent:\n{}\n\nData received:\n{}".format(DATA,data))
```

---

