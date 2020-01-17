[![Save Service](https://github.com/jax79sg/artyins-saveservice/raw/master/images/SoftwareArchitectureSaveService.jpg)]()

# Save For artyins deployment architecture
This is a submodule for the artyins deployment architecture. Please refer to [main module](https://github.com/jax79sg/artyins) for full build details.

[![Build Status](https://travis-ci.com/jax79sg/artyins-saveservice.svg?branch=master)](https://travis-ci.com/jax79sg/artyins-saveservice)
[![Container Status](https://quay.io/repository/jax79sg/artyins-saveservice/status)](https://quay.io/repository/jax79sg/artyins-saveservice)

Refer to [Trello Task list](https://trello.com/c/x7u3MPQX) for running tasks.

---

## Table of Contents

- [Usage](#Usage)
- [Virtualenv](#Virtualenv)
- [Tests](#Tests)

---

## Usage
The save service can be called by a HTTP POST call. Primarily on http://saveservice:9891/save_reports, http://saveservice:9891/save_ingests and http://saveservice:9891/updateingests. It expects a json of the following formats.
```json
[{"filename":"file01.pdf","id":1,"class":"DOCTRINE","section":"observation","content":"adfsfswjhrafkf"},{"filename":"file02.pdf","id":2,"class":"DOCTRINE","section":"observation","content":"kfsdfjsfsjhsd"}]}  
```
and will vomit 2 keys. Content of these 2 keys are the associated errors if any.
```json
[{"filename":"file01.pdf","id":1,"error":"report already exists"},{"filename":"file01.pdf","id":2,"results":"Some SQL problems, check logs"}]
```

### config.py
The configuration file will indicate the save class to use and any other configuration the author deemed necessary for their class. For testing purposes, the mysql-connector-python library is used. 
```python
    MODEL_MODULE="savers.sqlsaver"
    MODEL_CLASS="SQLSaver"
    SHARED_DATA_PATH="/shareddata"
    SQL_HOST="mysqldb"
    SQL_USER="user"
    SQL_PASSWD="password"
    SQL_DATABASE="reportdb"
```

### Abstract Saver Class
All implementations of savers must implement this abstract class.
savers/save.py
```python
from abc import ABC, abstractmethod
class SaverInterface(ABC):
    """  An abstract base class for saving tools """

    @abstractmethod
    def __init__(self):
        raise NotImplementedError()

    @abstractmethod
    def create(self, json):
        raise NotImplementedError()
    
    @abstractmethod
    def update(self, json):
        raise NotImplementedError()
  
    @abstractmethod
    def get(self, json):
        raise NotImplementedError()

    @abstractmethod
    def delete(self, json):
        raise NotImplementedError()

    def freequery(self, string):
        raise NotImplementedError()
```

### An example on how to implement the Abstract Saver class
```python
from savers.saver import SaverInterface
import os
from config import SaverConfig
import mysql.connector
import json
import logging
class SQLSaver(SaverInterface):
# This class takes in json files and will interpret the jsons as follows.
# {'tablename':[{'columnname01':'somevalue','columnname02':'somevalue'},{'columnaname02':'somevalue'}]}    
    
    def connect(self):
        self.logging.info("Logging to %s@%s:%s -p %s", self.config.SQL_USER, self.config.SQL_HOST, self.config.SQL_DATABASE, self.config.SQL_PASSWD)
        self.db = mysql.connector.connect(host=self.config.SQL_HOST, user=self.config.SQL_USER, passwd=self.config.SQL_PASSWD, database=self.config.SQL_DATABASE, auth_plugin='mysql_native_password') 
        self.logging.info("Log in is successful")

    def executesql(self, sqlstatement):
        self.logging.debug("Executing %s", sqlstatement)
        cursor=self.db.cursor()
        cursor.execute(sqlstatement)
        self.db.commit()
        rowcount=cursor.rowcount
        cursor.close()
        return rowcount

    def executesql(self, sqlstatement, data):
        try:
           self.logging.debug("Executing %s with data as follows %s", sqlstatement, data)
           cursor=self.db.cursor()
           cursor.execute(sqlstatement, data)
           self.db.commit()
           rowcount=cursor.rowcount
           cursor.close()
        except Exception as e:
           self.logging.debug("Problem executing SQL: %s", str(e))
           rowcount=0
        return rowcount
    
    def querysql(self,sqlstatement):
        print("Statements to execute\n",sqlstatement)
        cursor=self.db.cursor()
        cursor.execute(sqlstatement)
        records = cursor.fetchall()
        cursor.close()
        return records

    def __init__(self,config=None):
        if config == None:
           self.config = SaverConfig() 
        logging.basicConfig(level=logging.DEBUG,handlers=[
        logging.FileHandler("{0}/{1}.log".format("/logs", "saverservice-sqlsaver")),
        logging.StreamHandler()
    ],
                format="%(asctime)-15s %(levelname)-8s %(message)s")
        self.logging=logging
        self.connect()

    def freequery(self, sqlstring):
        records=self.querysql(sqlstring)
        return records

    def create(self, jsonobject):
        try:
           self.logging.info("Starting create operations")
           if isinstance(jsonobject, str):
              self.logging.debug("data obj received is not json, manually converting")
              jsonobject = json.loads(jsonobject)
           dictkeys= jsonobject.keys() 
           totalrowcount=0       
           for tablename in dictkeys:
              rowstoadd=jsonobject[tablename]
              self.logging.debug("Table: %s Rows: %s",tablename, rowstoadd)
              sqlstatementcolnames=""
              sqlstatementcolvalues=""
              for row in rowstoadd:
                  print("Row:{}".format(row))
                  dictcolsinrow=row.keys()
                  print("ColumnNames: {}".format(dictcolsinrow))
                  colCount=0
                  datalist=[]
                  for col in dictcolsinrow:
                      self.logging.debug("Col:%s,Val:%s",col,row[col])
                      if colCount==0:
                          sqlstatementcolnames=col
                          #sqlstatementcolvalues="\'"+str(row[col])+"\'"
                          sqlstatementcolvalues="%s"
                          datalist.append(str(row[col]))
                      else:
                          sqlstatementcolnames=sqlstatementcolnames+','+col
                          #sqlstatementcolvalues=sqlstatementcolvalues+','+"\'"+str(row[col])+"\'"
                          sqlstatementcolvalues=sqlstatementcolvalues+",%s"
                          datalist.append(str(row[col]))
                      colCount=colCount+1
                  sqlstatement="INSERT INTO " + tablename + "(" + sqlstatementcolnames + ") VALUES (" + sqlstatementcolvalues + ")"
                  rowcount=self.executesql(sqlstatement, datalist)
                  totalrowcount=totalrowcount+rowcount
        except Exception as e:
           totalrowcount=0
        return totalrowcount

    def update(self,jsonobject):
         #Expects the following json
         #{"tablename":[
         #{"row":
         #{"data":{"columnname02":"01value","columnname02":"02value"},"condition":{"columnname03":"03value"}}},
         #{"row":
         #{"data":{"columnname04":"04value","columnname05":"05value"},"condition":{"columnname06":"06value"}}}
         #]}
         dictkeys= (jsonobject.keys())
         print("Dict keys:",dictkeys)
         sqlstatements=[]
         for tablename in dictkeys:
             rowstoupdate=jsonobject[tablename]
             print("Table: {}\nRows:{}".format(tablename,rowstoupdate))
             for rowtoupdate in rowstoupdate:
                 rowdata=rowtoupdate['row']['data']
                 rowcondition=rowtoupdate['row']['condition']
                 print("ROW:\n\tRowData:{}\n\tRowCondition:{}".format(rowdata,rowcondition))
                 sqlstatementdata=""
                 colCount=0
                 for colname in rowdata.keys():
                     if colCount==0:
                          sqlstatementdata = colname+"="+"\'"+str(rowdata[colname])+"\'"
                     else:
                          sqlstatementdata = sqlstatementdata+","+colname+"="+"\'"+str(rowdata[colname])+"\'"
                     colCount=colCount+1
                 sqlstatementcondition=""
                 colCount=0
                 for colname in rowcondition.keys():
                     if colCount==0:
                          sqlstatementcondition=colname+"="+"\'"+str(rowcondition[colname])+"\'"
                     else:
                          sqlstatementcondition=sqlstatementcondition+" AND "+ colname+"="+"\'"+str(rowcondition[colname])+"\'"
                     colCount=colCount+1
                 sqlstatement="UPDATE " + tablename + " SET " + sqlstatementdata + " WHERE " + sqlstatementcondition
                 sqlstatements.append(sqlstatement)
         self.executesql(sqlstatements)

    def get(self):
         super.get()

    def delete(self):
         super.delete()
```

## Virtualenv
```shell
python3 -m venv venv
source venv/bin/activate
pip install --user -r requirements.txt`
```
---

## Tests 
This repository is linked to [Travis CI/CD](https://travis-ci.com/jax79sg/artyins-saveservice). You are required to write the necessary unit tests and `.travis.yml` if you introduce more Saver classes.

### Web Service Test
```
#Start gunicorn wsgi server
gunicorn --bind 0.0.0.0:9891 --daemon --workers 10 wsgi:app
```
### Send test POST request
```python
URL = "http://127.0.0.1:9891/test"

# sending get request and saving the response as response object
r = requests.get(url = URL)
print(r)
```

---

