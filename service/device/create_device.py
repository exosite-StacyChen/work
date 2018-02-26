import requests
import json
import time
import random
import string


def main():
    # projectId = "b5bsxk62654g00000"
    # env = "staging"
    projectId = "n1rzjq469jvog0000"
    env = "dev"
    host = "https://bizapi-{env}.hosted.exosite.io/api:1/service/{projectId}/device2/identity".format(
        **locals())
    create_one_device(host, env, projectId, "device_51")
    # create_one_device(host,env, projectId, "device_50_pegasus")
    # create_one_device(host,env, projectId, "device_50")
    # create_one_device(host,env, projectId, "device_1001")
    # create_device(host, 50)
    # delete_all_device(host)


def create_one_device(host, env, projectId, sn):
    print "create device {}".format(sn)
    post_request(host, sn)
    device_activate(projectId, env ,sn)


def getData():
    size = random.randint(1, 10)
    data = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(size))
    print "Device: {}".format(data)
    return data


def create_device(host, count):
    for x in xrange(count):
        print "------------------------"
        print "Count: {}".format(x)
        sn = getData()
        print "create device"
        post_request(host, sn)
        print "------------------------"


def delete_all_device(host):
    response = get_device_list(host)
    data = response.json()
    for device in data["devices"]:
        print "Delete device: {}".format(device["identity"])
        delete_device(host, device["identity"])


def get_device_list(host):
    HEADER = {'content-type': 'application/json',
              'Authorization': 'Basic dGVzdGluZ0BleG9zaXRlLmNvbToxMjM0ZXN6eGN2Kys='}
    try:
        response = requests.get(
            "{host}/".format(**locals()),
            headers=HEADER
        )
        return response
    except Exception, e:
        print e


def delete_device(host, sn):
    HEADER = {'content-type': 'application/json',
              'Authorization': 'Basic dGVzdGluZ0BleG9zaXRlLmNvbToxMjM0ZXN6eGN2Kys='}
    try:
        response = requests.delete(
            "{host}/{sn}".format(**locals()),
            headers=HEADER
        )
        print response
    except Exception, e:
        print e
    print response


def device_activate(projectId, env, sn):
    HEADER = {'content-type': 'application/x-www-form-urlencoded; charset=utf-8'}
    response = ''
    data = "sn={}".format(sn)
    try:
        response = requests.post(
            "https://{projectId}.m2.exosite-{env}.io/provision/activate".format(
                **locals()),
            headers=HEADER,
            data=data
        )
    except Exception, e:
        print e
    print response
    print response.content


def post_request(host, sn):
    HEADER = {'content-type': 'application/json',
              'Authorization': 'Basic dGVzdGluZ0BleG9zaXRlLmNvbToxMjM0ZXN6eGN2Kys='}
    response = ''
    data = {"locked": False}
    try:
        response = requests.put(
            "{host}/{sn}".format(
                **locals()),
            headers=HEADER,
            data=json.dumps(data)
        )
    except Exception, e:
        print e
    print response
    print response.content

if __name__ == '__main__':
    main()
