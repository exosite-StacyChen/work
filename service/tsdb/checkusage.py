import requests
import json
import calendar, time

timestamp = calendar.timegm(time.gmtime())

url = "http://localhost:8081/api/v1/solution/o11ykvtva1qvk0000/usage"

payload = ""
headers = {'content-type': 'application/json'}

response = requests.request("GET", url, data=payload, headers=headers)

usage = json.loads(response.text)

proc_quota = usage['_global']['quota']['processing_time_daily']
proc_usage = usage['_global']['usage']['processing_time_daily']

print("Timestamp: {}\tTime: {}\tUsage: {}\tQuota: {}\tPercent: {}".format(timestamp, time.asctime(), proc_usage, proc_quota, '%s%%' % round(proc_usage / proc_quota * 100,3)))