import requests
import os
import sys
import base64
import json
import time
import threading
import subprocess
import random
import math
import re
import signal
import string


def main():
    host = "https://bizapi-staging.hosted.exosite.io/api:1/business/loz8gtd7hcmims4i/solution/"
    for x in xrange(1,1000):
        print "{} Count".format(x)
        create_solution(host,"product")

def create_solution(host,type):
    
    name = ''.join(random.choice(
                string.ascii_uppercase + string.digits) for _ in range(10))
    HEADER = {'content-type': 'application/json',
              'Authorization': 'Basic dGVzdGluZ0BleG9zaXRlLmNvbToxMjM0ZXN6eGN2Kys='}
    data={"label": "qa{}".format(name), "type": type}
    try:
        print "create {} ......".format(type)
        print data
        response = requests.post(
            host,
            headers=HEADER,
            data=json.dumps(data)
        )
        print response
        print response.content
        print "delete {} ......".format(type)
        response = requests.delete(
            "{}{}".format(host, response.json()['id']),
            headers=HEADER
        )
        print response
    except Exception, e:
        print e

if __name__ == '__main__':
    main()
