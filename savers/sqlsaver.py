from savers.saver import SaverInterface
import os
from config import SaverConfig
import mysql.connector
import json
class SQLSaver(SaverInterface):
# This class takes in json files and will interpret the jsons as follows.
# {'tablename':[{'columnname01':'somevalue','columnname02':'somevalue'},{'columnaname02':'somevalue'}]}    
    
    def connect(self):
        self.db = mysql.connector.connect(host=self.config.SQL_HOST, user=self.config.SQL_USER, passwd=self.config.SQL_PASSWD, database=self.config.SQL_DATABASE, auth_plugin='mysql_native_password') 

    def executesql(self, sqlstatement):
        cursor=self.db.cursor()
        cursor.execute(sqlstatement)
        self.db.commit()
        rowcount=cursor.rowcount
        cursor.close()
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
        self.connect()

    def freequery(self, sqlstring):
        records=self.querysql(sqlstring)
        return records

    def create(self, jsonobject):
        dictkeys= jsonobject.keys() 
        totalrowcount=0       
        for tablename in dictkeys:
           rowstoadd=jsonobject[tablename]
           print("Table: {}\nRows:{}".format(tablename, rowstoadd))
           sqlstatementcolnames=""
           sqlstatementcolvalues=""
           for row in rowstoadd:
               print("Row:{}".format(row))
               dictcolsinrow=row.keys()
               print("ColumnNames: {}".format(dictcolsinrow))
               colCount=0
               for col in dictcolsinrow:
                   print("Col:{},Val:{}".format(col,row[col]))
                   if colCount==0:
                       sqlstatementcolnames=col
                       sqlstatementcolvalues="\'"+str(row[col])+"\'"
                   else:
                       sqlstatementcolnames=sqlstatementcolnames+','+col
                       sqlstatementcolvalues=sqlstatementcolvalues+','+"\'"+str(row[col])+"\'"
                   colCount=colCount+1
               sqlstatement="INSERT INTO " + tablename + "(" + sqlstatementcolnames + ") VALUES (" + sqlstatementcolvalues + ")"
               rowcount=self.executesql(sqlstatement)
               totalrowcount=totalrowcount+rowcount
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
