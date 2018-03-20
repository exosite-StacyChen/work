import time
import random
from common import *

# engineering.kli.v3.tracking
# meet.plan
# dontmeet.plan


def main():
    grafanaHead = "engineering.kli.v3.tracking"
    env = input("ENV? ( production / staging / dev )")
    domain = "{}.{}.".format(grafanaHead, str(env))
    targets = ["meet.plan", "dontmeet.plan"]
    start = 0
    end = input("Count? ")
    valueRange = input("Value Range(0~?)? ")
    for x in xrange(start, end):
        timestamp = int(time.time())
        print "-------------------"
        print "Count: {} Time: {}".format(x, timestamp)
        print "-------------------"
        for target in targets:
            value = random.randint(0, valueRange)
            common().graphiteLog(domain + target, value)
            print "    Send To \"{}\" Data: {} ".format(domain + target, value)
        time.sleep(0.5)

if __name__ == '__main__':
    main()
