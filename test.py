import unittest
from time import sleep
import json
class TestModels(unittest.TestCase):

    def test_sqlsaver1createreport(self):
        sleep(15)
        print("Running SQLSaver create report")
        from savers.sqlsaver import SQLSaver
        saver = SQLSaver()
        createData=open('create_report.json','r')
        createjsonobj = json.load(createData)
        saver.create(createjsonobj)

    def test_sqlsaver2createingest(self):
        sleep(15)
        print("Running SQLSaver create report")
        from savers.sqlsaver import SQLSaver
        saver = SQLSaver()
        createData=open('create_report.json','r')
        createjsonobj = json.load(createData)
        saver.create(createjsonobj)
        print("Running SQLSaver create ingest")
        createData=open('create_ingest.json','r')
        createjsonobj = json.load(createData)
        saver.create(createjsonobj)

    def test_sqlsaver3updateingest(self):
        sleep(15)
        print("Running SQLSaver update ingest")
        from savers.sqlsaver import SQLSaver
        saver = SQLSaver()
        createData=open('update_ingest.json','r')
        createjsonobj = json.load(createData)
        saver.update(createjsonobj)

if __name__ == '__main__':
    unittest.main()
