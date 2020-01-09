import unittest
import json
class TestModels(unittest.TestCase):

    def test_sqlsavercreatereport(self):
        from time import sleep
        sleep(5)
        print("Running SQLSaver create report")
        from savers.sqlsaver import SQLSaver
        saver = SQLSaver()
        createData=open('create_report.json','r')
        createjsonobj = json.load(createData)
        saver.create(createjsonobj)

    def test_sqlsavercreateingest(self):
        print("Running SQLSaver create ingest")
        from savers.sqlsaver import SQLSaver
        saver = SQLSaver()
        createData=open('create_ingest.json','r')
        createjsonobj = json.load(createData)
        saver.create(createjsonobj)

if __name__ == '__main__':
    unittest.main()
