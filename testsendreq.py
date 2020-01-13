import requests 

URL = "http://127.0.0.1:9891/updateingests"
DATA = {"ingests":[{"row":{"data":{"annotated_category":"TRAINING"},"condition":{"id":1}}},{"row":{"data":{"annotated_category":"TRAINING","predicted_category":"TRAINING"},"condition":{"id":"2"}}}]}
# sending get request and saving the response as response object 
r = requests.post(url = URL, json  = DATA) 
print(r) 


URL = "http://127.0.0.1:9891/savereports"
DATA = {"reports":[{"filename":"file01.pdf","created_at":"20200108133333","currentloc":"//mnt//sharedata"},{"filename":"file02.pdf","created_at":"20200108144444","currentloc":"//mnt//sharedata"}]}
# sending get request and saving the response as response object
r = requests.post(url = URL, json  = DATA)
print(r)


URL = "http://127.0.0.1:9891/saveingests"
DATA = {"ingests":[{"text":"This is the weather for singapore","section":"observation","created_at":"20200108133333","ingest_id":2,"predicted_category":"DOCTRINE","annotated_category":"DOCTRINE"},{"text":"Mental stress along with physical pain...silence","section":"observation","created_at":"20200108122222","ingest_id":2,"predicted_category":"DOCTRINE","annotated_category":"DOCTRINE"}]}

# sending get request and saving the response as response object
r = requests.post(url = URL, json  = DATA)
print(r)
