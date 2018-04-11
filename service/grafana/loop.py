import time
import random
import socket
from common import *


def main():
    grafanaHead = "kv.tracking"
    env = str(raw_input("ENV? ( staging / staging-preview ) ") or "staging")
    domain = "{}.{}.".format(grafanaHead, str(env))
    targets = [
        # "delete.times",
        "clear.times",
        # "get.times",
        # "info.times",
        # "set.times",
    ]
    start = 0
    end = int(raw_input("Count? ") or 1)
    value_start = int(raw_input("Value Range(?~)? ") or 1)
    value_end = int(raw_input("Value Range(~?)? ") or 1)

    # calculate timestamp
    now = int(time.time())
    def_timestamp = now - 3600
    timestamp = int(raw_input("timestamp : ") or def_timestamp)
    interval = abs(now - timestamp)
    interval = int(interval / end)

    for x in xrange(start, end):
        timestamp = timestamp + interval
        print "-------------------"
        print "Count: {} Time: {}".format(x, timestamp)
        print "-------------------"
        for target in targets:
            value = random.randint(value_start, value_end)
            # common().graphiteLog(domain + target, value, timestamp)
            graphiteLog(domain + target, value, timestamp)
            print "    Send To \"{}\" Data: {} ".format(domain + target, value)


def graphiteLog(operation, value, times):
    data = "\"{} {} {}\"".format(operation, value, times)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # graphitePort = 8088
    # graphiteServer = 'localhost'
    graphitePort = 2003
    graphiteServer = "tsdb-sink.exosite.com"
    sock.connect((graphiteServer, graphitePort))
    sock.sendall(data)
    sock.shutdown(socket.SHUT_WR)
    while 1:
        rep = sock.recv(1024)
        if rep == "":
            break
        print "Received:", repr(rep)
    sock.close()


if __name__ == '__main__':
    main()
