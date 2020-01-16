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
                          sqlstatementcolvalues="\'%\'"
                          datalist.append(str(row[col]))
                      else:
                          sqlstatementcolnames=sqlstatementcolnames+','+col
                          #sqlstatementcolvalues=sqlstatementcolvalues+','+"\'"+str(row[col])+"\'"
                          sqlstatementcolvalues=sqlstatementcolvalues+",\'%\'"
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

      
if __name__=="__main__":
     jsonobj = json.load(open("create_report.json","r"))
     saver = SQLSaver()
     saver.create(jsonobj)
     jsonobj=json.load(open("create_ingest.json","r"))
     saver.create(jsonobj)

     jsonobj=json.load(open("update_ingest.json","r"))
     saver.update(jsonobj)
#    rowsreportsaffected=saver.save({'reports':[{'filename':'file01.pdf','created_at':'2020-01-09 15:00:00','ingested_at':'2020-01-09 15:01:00','currentloc':'/home/shareddata'},{'filename':'file02.pdf','created_at':'2020-01-09 16:00:00','ingested_at':'2020-01-09 16:01:00','currentloc':'/home/shareddata'}])	
#    rowsingestsaffected=saver.save({'ingests':[{'text':'This is good weather?','section':'observation','created_at':'2020-01-02 12:33:33','ingest_id':'1','predicted_category':'DOCTRINE','annotated_category':'DOCTRINE'}]})
#    rowsingestupdate=save.update({'ingests':[{'id':'1','annotated_category':'PERSONNEL'}]}) 
     pass
