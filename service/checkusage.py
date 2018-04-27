import requests
import json
import calendar
import time


url = "https://pegasus-api-staging.hosted.exosite.io/api/v1/solution/u58cvblvsrmk00000/usage"

payload = ""
headers = {'content-type': 'application/json'}
service = '_global'
target = ['processing_time_total',
          'processing_time_monthly', 'processing_time_daily']

while True:
    timestamp = calendar.timegm(time.gmtime())
    response = requests.request("GET", url, data=payload, headers=headers)
    usage = json.loads(response.text)
    result = "Timestamp: {}\t".format(timestamp)
    for x in xrange(len(target)):
        item = str(target[x])
        result = result + \
            "{}: {}\t".format(item, usage[service]['usage'][item])
    print(result)
    time.sleep(5)
