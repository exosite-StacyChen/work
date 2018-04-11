import requests
import json
import calendar, time


url = "http://localhost:8081/api/v1/solution/u2l1b86zyylg00000/usage"

payload = ""
headers = {'content-type': 'application/json'}


while True:
	timestamp = calendar.timegm(time.gmtime())
	response = requests.request("GET", url, data=payload, headers=headers)
	usage = json.loads(response.text)
	keys = usage['keystore']['usage']['keys']
	size = usage['keystore']['usage']['size']

	print("Timestamp: {}\tTime: {}\tKey: {}\tSize: {}".format(timestamp, time.asctime(), keys, size))
	time.sleep(5)