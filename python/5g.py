import ast
import requests
import os
import sys
import base64
import json
import time
import subprocess
import random
import math

def main():
    # host = "localhost:4000"
    biz_info = {
        "basic_authorization": "Basic bmluYXpoYW5nK3ByZXZpZXdAZXhvc2l0ZS5jb206bmluYXpoYW5nK3ByZXZpZXc=",
        "biz_host": "bizapi-staging-preview.hosted.exosite.io",
        "solution_host": "apps.preview.exosite-staging.io"
    }

    def single_export_size(biz_info, startTime, endTime):
        '''
            Export performance - single export
            Data schema: 10 Metrics and 2 tags
            500 KB, 50 MB, 5 GB
        '''
        # solutions = {
        #     "name":"qa-201700920-testing-08",
        #     "sid":"y4px4votkm3s00000"
        # }
        
        # one solution many times
        # host = 'https://{}.{}'.format(solutions['name'], biz_info['solution_host'])
        # retried = 1
        # while retried <= 5:
        #     print("{}:".format(retried))
        #     out = query_and_wait(host, startTime, endTime, "metric10", 10)
        #     retried = retried + 1

        # one solution list all status
        # data=getData(host+'/tsdb/export/list')
        # i=0
        # data=json.loads(data)
        # # print(data[1])
        # # print(data[1].get('state'))
        # while i<100:
        #     # d=json.loads(data[i])
        #     # print(i)
        #     if data[i].get('state')!="enqueued":
        #         print(data[i].get('state'))
        #         # break
        #     i=i+1

        # print("current {}".format(i))
        # print(len(length))

        solutions = [
            {
                "name":"qa-201700920-testing-09",
                "sid":"splj3wpelozk0000"
            },
            {
                "name":"qa-201700920-testing-02",
                "sid":"e30n8hb5770800000"
            },
            {
                "name":"qa-201700920-testing-03",
                "sid":"n4qaa4vky5r000000"
            },
            {
                "name":"qa-201700920-testing-04",
                "sid":"w3y4e5fzieck00000"
            },
            {
                "name":"qa-201700920-testing-05",
                "sid":"t3h0n0p4bb3g00000"
            },
            {
                "name":"qa-201700920-testing-06",
                "sid":"l2wxebn01cts00000"
            },
            {
                "name":"qa-201700920-testing-07",
                "sid":"c50r06atnz0000000"
            },
            {
                "name":"qa-201700920-testing-08",
                "sid":"y4px4votkm3s00000"
            }
        ]
        requestid=[{"job_id":"QcivuCO7768dAXOxZ7CXCR1SRpCkE43RuA0a4BmkZ4tUk32N.iz6g00c7VYW8ua58KWOobPhrmRbTIT8QKpnDcsxlTW_tEAeALaLRAt4bUXJ0MAtHEVc0T9kFn5WOOAW"},
            {"job_id":"zaVyQQgUdK1kUWQ1553MUM.AoIpNubvpznQqYJFhhHc6N68IWF9tQepSm0JiSyojOl12x7_EfNIqgCzdfXr.0SCu8nZFeSxdPifv3iCu.tX0WmzfNCRlnsIYM.NZ2kYy"},
            {"job_id":"RL8jOwcjJ8SITtrk5SOybWB_JqqCi1V9pxVPQhkS8UHzIBXL9Us5OKNSUoI_JCguIO5sn70RK4Rr61Y6aLX17o5kqh7u0IvbWqCpiob9DIODH5ETqXHiWyaoiHaCbM6w"},
            {"job_id":"xo2RwGPIbYTXtMP_wp5_gfBqWgyNInJMfPpB8tDhje4_Ja.UDM2drzlu4EHIhpkizYVjjaAylThbsS85IDYjR.0yqX..hBvw2iSfyrnfpHmun9xUGwLHtQZmkbaf6NH1"},
            {"job_id":"1P1yB2S0cRboJncopGaN738ZEyHck6KummC5g2KDvwhfOlq2MYLF4tTrrbQs7B05JOUOonY_w2y.w_XN2XfP4AUhxGvxokY3OeqwBQxSQxkMn3i6TGaRJhuXPMXlJ1e4"},
            {"job_id":"KwwTYuabMJKocSTEi3pU.T2MtYnRBVzxNTiLZWWCVXjWFoOaNkBVi2Tw67rqCkQMwKVxXOpd5uwdrtg8sACOsBwbXM11Xmhmwvk9xShcnwMGIdBorFBdGGUaylCdbclq"},
            {"job_id":"dqys0s4KiSDCDHLq7bPVEQ.e9axn0SQu3bWOy5UA3K_8rnJ1962IQTAMfXrZebQ1d926GPUQ8FA_590.DpC6vqBYT6obhKjhlMBQBnQNmrGIQqPmAZJgZuVHOXEX.6Zf"},
            {"job_id":"xil82.9gqOO_OsjGxKyJTULp94wLrzpk2ll.wPxKylSfDYU7AKY52F2NTZwxJ8xjkkKHhBiyK0Ku0BfipKRXYPo2XUEPB9k_jFj.UmMWdFLFU75XiynceK8nkk7H.5IM"}]
        
        # many solution one times
        retried = 1
        index=0
        # while index < len(solutions):
        #     host = 'https://{}.{}'.format(solutions[index]['name'], biz_info['solution_host'])
        #     out = query_and_wait(host, startTime, endTime, "metric10", 10)
        #     index=index+1

        # many solution list one status
        # print(data[1])
        # print(data[1].get('state'))
        while index < len(solutions):
            host = 'https://{}.{}'.format(solutions[index]['name'], biz_info['solution_host'])
            data=getData(host+'/tsdb/export/list')
            data=json.loads(data)
            i=0
            # while data[i].get('job_id')!=requestid[index].get('job_id'):
            #     i=i+1
            # print("{}:{}".format(index,data[i].get('job_id')))
            print("{}:{}".format(index,data[i].get('state')))
            index=index+1
        # print("current {}".format(i))
        
        

    startTime = 1505903659000
    endTime = 1537497255000
    single_export_size(biz_info, startTime, endTime)
    # Merics50with5g(host, startTime, endTime)
    # Merics1with5g(host, startTime, endTime)
    # Merics10with5g(host, startTime, endTime)
    # query(host, sid, startTime, endTime, interval)
def getQueryBody(metricName, count, start_time, end_time):
    metrics = {}
    query = []
    for i in range(1, int(count)+1, 1):
        query.append("{}_{}".format(metricName, i))
    query = {
        'metrics': query,
        'tags': {
            'exp_Metric_N': str(count),
            'exp_Name': metricName
        },
        'start_time': start_time,
        'end_time': end_time
    }
    data = {
        'query':query,
        'filename': 'qa_export'
    }
    return data

def query_and_wait(host, startTime, endTime, metricName, count):
    request = None
    while not request:
        data = getQueryBody(metricName, count, startTime, endTime)
        # print "  Query Data: {}".format(json.dumps(data))
        request = readData(host + '/tsdb/export', data)
        s_t = time.time()
        if 'job_id' in request:
            print " Request ID: {}".format(request)
        else:
            print "{}".format(request)

    
def clear_content(host):
    response = requests.get(
        host+'/content/clear', 
        headers={'content-type': 'application/json'}
    )
    print response.status_code
    if response.status_code == 200:
        print "Clear the content"
        return 1
    return 0

def readData(host, data):
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
            host,
            headers=HEADER,
            data=json.dumps(data)
        )
    except Exception, e:
        print "Connect Error({}): {}".format(e.errno, e.strerror)
    else:
        if response.status_code == 200:
            requestResult = response.content
        else:
            print "## Get error {}".format(response.content)
    return requestResult

def getData(host):
    '''
    random.seed(i)
    data = getRandomData()
    writeData(data)
    return (1 ok, 0 fail)
    '''
    HEADER = {'content-type': 'application/json'}
    requestResult = 0
    try:
        response = requests.get(
            host,
            headers=HEADER
        )
    except Exception, e:
        print "Connect Error({}): {}".format(e.errno, e.strerror)
    else:
        if response.status_code == 200:
            requestResult = response.content
        else:
            print "## Get error {}".format(response.content)
    return requestResult
if __name__ == '__main__':
    main()