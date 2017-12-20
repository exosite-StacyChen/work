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
    global host
    global domain
    # host = "localhost:4000"
    domain = "stacychen.apps.exosite-dev.io/write"
    host = "pegasus-cass-service-dev.hosted.exosite.io"
    # solution =
    #     {
    #         "name": "stacy4",
    #         "sid": "u2o29ufxmmfc00000"
    #     }
    #
    solution = {
        "name": "stacychen",
        "sid": "xrv6xq7vzgz40000"
    }

    # 400 {"result":null,"error":"Client Error: Exceeds maximum metric value size, 491520 bytes."}
    # write(solution,  "qa_metrics", 1, 0, 491520, 1)
    # 400 {"result":null,"error":"Client Error: Exceeds maximum number of data entries. [Max: 2000]"}
    # write(solution,  "qa_metrics", 1, 0, 5, 2001)

    write(solution, "qa_metrics", metricsCount=1,
          tagsCount=0, metricsSize=100, count=2001, return_ts=False)

    # write(solution,  "qa_metrics", metricsCount=100,
    #       tagsCount=0, metricsSize=100, count=21, return_ts=False)

    # write(solution, "qa_metrics", metricsCount=1,
    #       tagsCount=20, metricsSize=100, count=96, return_ts=False)

    # write(solution, "qa_metrics", metricsCount=100,
    #       tagsCount=19, metricsSize=100, count=3, return_ts=False)

    # write(solution, "qa_metrics", metricsCount=10,
    #       tagsCount=5, metricsSize=100, count=40, return_ts=False)
    # ts
    # [{"write_timestamp":1513669787791051},{"write_timestamp":1513669787791051}]
    # write(host, solution, "qa_metrics", metricsCount=1, tagsCount=0,
    # metricsSize=5, count=2,return_ts=True)


def write(solution, metricName, metricsCount, tagsCount, metricsSize, count, return_ts=False):
    response = ""
    startTime = time.time()
    print "----------------------------------------"
    print "-------------Call PegasusAPI------------"
    print "----------------------------------------"
    postData = getData(
        metricName, metricsCount, tagsCount, metricsSize, count, return_ts)

    response = postMultiDataVaiPegasus(solution['sid'], postData)
    all = time.time() - startTime

    saveResult(solution, metricName, metricsCount,
               tagsCount, metricsSize, count, postData, response, all)
    # print "----------------------------------------"
    # print "-------------Call BizAPI----------------"
    # print "----------------------------------------"
    # postData = getData(
    #     metricName, metricsCount, tagsCount, metricsSize, count, return_ts)
    # response = postMultiDataVaiBiz(postData)

    # saveResult(solution, metricName, metricsCount,
    #            tagsCount, metricsSize, count, postData, response, response.content)


def saveResult(solution, metricName, metricsCount, tagsCount, metricsSize, count, postData, response, spendTime):
    timestamp = int(round(time.time() * 1000))
    result_path = "data/post_results_{}.txt".format(timestamp)
    post_path = "data/post_body_{}.txt".format(timestamp)
    data = ""
    try:
        f = open(post_path, "w")
        try:
            f.write(json.dumps(postData))  # Write a string to a file
        finally:
            f.close()
    except IOError:
        pass
    data = data + "solutionID: {} \n".format(solution['sid'])
    data = data + "Metirc: {} \nMetirc Size: {} \n".format(metricName, metricsSize)
    data = data + "Tags Size: {} \n".format(tagsCount)
    data = data + "Datapoint length: {} \n".format(count)
    data = data + "export post Data to {} \n".format(post_path)
    data = data + "export post Results to {} \n".format(result_path)
    data = data + "Get Response: {} \n".format(response.content)
    data = data + "spend times : {} ".format(spendTime)
    print data
    try:
        f = open(result_path, "w")
        try:
            f.write(data)  # Write a string to a file
        finally:
            f.close()
    except IOError:
        pass


def getData(metricName, metricsCount, tagsCount, metricsSize, count, return_ts):
    tags = {}
    data = {}
    datapoints = []
    byte = 0

    for x in xrange(0, tagsCount):
        tags.update({"{}_{}".format(metricName, x): str(metricName)})

    for x in xrange(0, count):
        metrics = {}
        for x in xrange(0, metricsCount):
            # 491520 480kb
            size = random.randint(1, metricsSize)
            file = os.urandom(size)
            file = base64.b64encode(file).decode('utf-8')
            byte = byte + sys.getsizeof(repr(file))
            metrics.update({"{}_{}".format(metricName, x): str(file)})

        millis = int(round(time.time() * 1000))
        items = {
            "metrics": metrics,
            "tags":  tags,
            "ts": "{}ms".format(millis)
        }
        datapoints.append(items)

    data = {
        "datapoints": datapoints, "return_ts": return_ts
    }

    print "Data Size:{} byte".format(byte)
    return data


def postMultiDataVaiBiz(data):
    HEADER = {'content-type': 'application/json'}
    response = ""
    try:
        response = requests.post(
            "https://{}".format(domain),
            headers=HEADER,
            data=json.dumps(data)
        )

    except Exception, e:
        print e
        print "Connect Error({}): {}".format(e.errno, e.strerror)
    else:
        print response.status_code
    return response


def postMultiDataVaiPegasus(sid, data):
    HEADER = {'content-type': 'application/json'}
    response = ""
    try:
        response = requests.post(
            "http://{}/api/v1/timeseries/{}/multi_data".format(host, sid),
            headers=HEADER,
            data=json.dumps(data)
        )
    except Exception, e:
        print e
        print "Connect Error({}): {}".format(e.errno, e.strerror)
        subprocess.Popen(["oc", "project", "murano-staging"])
        time.sleep(5)
        subprocess.Popen(
            ["oc", "port-forward", "pegasus-cass-service-hopper", "4000"])
        time.sleep(5)
    else:
        print response.status_code

    return response

if __name__ == '__main__':
    main()
