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
    data = ""
    types = input("type? ( (1)application / (2)product ) ")
    if types == 1:
        types = "application"
    else:
        types = "product"
    for x in xrange(1, 1000):
        print "{} Count".format(x)
        data = data + create_solution(host, str(types))
    saveData(data,1)


def create_solution(host, type):

    name = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(10))
    HEADER = {'content-type': 'application/json',
              'Authorization': 'Basic dGVzdGluZ0BleG9zaXRlLmNvbToxMjM0ZXN6eGN2Kys='}
    data = {"label": "qa{}".format(name), "type": type}
    p = ""
    try:
        print "------------------------------"
        print "create {} ......".format(type)
        print data
        response = requests.post(
            host,
            headers=HEADER,
            data=json.dumps(data)
        )
        p = p + "create {} ......\n".format(type)
        p = p + "{}\n".format(response)
        p = p + "{}\n".format(response.content)
        print response
        print response.content
        p = p + "delete {} ......\n".format(type)
        print "delete {} ......".format(type)
        response = requests.delete(
            "{}{}".format(host, response.json()['id']),
            headers=HEADER
        )
        print response
        p = p + "{}\n".format(response)
        print "------------------------------"
    except Exception, e:
        print e

    return p


def saveData(postData, y):
    timestamp = int(round(time.time() * 1000))
    post_path = "result_{}.txt".format(timestamp)
    data = ""
    if y == 1:
        try:
            f = open(post_path, "w")
            try:
                f.write(json.dumps(postData))  # Write a string to a file
            finally:
                f.close()
        except IOError:
            pass
    print post_path

if __name__ == '__main__':
    main()
