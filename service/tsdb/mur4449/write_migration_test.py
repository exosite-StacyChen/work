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


def main():
    host = "localhost:4000"

    solutions = [
        {
            "name": "stacy",
            "sid": "x4iv6eyobnhg00000"
        }
    ]
    # solutions = [
    #     {
    #         "name": "stacy2",
    #         "sid": "t4w4jtshjooa00000"
    #     }
    # ]
    
    # write(host, solutions, 0, 100, "qa_metrics",1,0)
    # write(host, solutions, 0, 100, "qa_metricsAndTags",1,1)
    # write(host, solutions, 0, 100, "qa_metricsM",2,0)
    # write(host, solutions, 0, 100, "qa_metricsAndTagsM",2,2)

def getData(metricName,metricsCount,tagsCount):
    metrics = {}
    tags = {}
    data = {}
    for x in xrange(0,metricsCount):
        file = os.urandom(5)
        file = base64.b64encode(file).decode('utf-8')
        metrics.update({"{}_{}".format(metricName,x): str(file)})

    for x in xrange(0,tagsCount):
        tags.update({"{}_{}".format(metricName,x): str(metricName)})

    data = {
        'metrics': metrics,
        'tags': tags
    }
    print "Data: {}".format(data)
    return data


def write(host, solutions, start, end, metricName,metricsCount,tagsCount):
    for i in range(start, end, 1):
        out = 0
        while not out:
            print solutions
            for sid in solutions:
                print sid
                out = fillData(host, sid['sid'], getData(metricName,metricsCount,tagsCount))
        print "Count: {} ".format(i)


def fillData(host, sid, data):
    '''
    random.seed(i)
    data = getRandomData()
    writeData(data)
    return (1 ok, 0 fail)
    '''
    HEADER = {'content-type': 'application/json'}
    requestResult = 0
    try:
        response = requests.post(
            "http://{}/api/v1/timeseries/{}/data".format(host, sid),
            headers=HEADER,
            data=json.dumps(data)
        )
        # response = requests.delete(
        #     "http://{}/api/v1/timeseries/{}/delete_all".format(host, sid),
        #     headers=HEADER,
        # )
        print response.content
    except Exception, e:
        requestResult = 0
        print e
        print "Connect Error({}): {}".format(e.errno, e.strerror)
        subprocess.Popen(["oc", "project", "murano-staging"])
        time.sleep(5)
        subprocess.Popen(
            ["oc", "port-forward", "pegasus-cass-service-hopper", "4000"])
        time.sleep(5)
    else:
        print response.status_code
        if response.status_code == 204:
            requestResult = 1

    return requestResult
if __name__ == '__main__':
    main()
