import time
import random
from common import *

# engineering.kli.v3.tracking
# meet.plan
# dontmeet.plan


def main():
    grafanaHead = "engineering.kli.v3.tracking"
    env = raw_input("ENV? ( production / staging / dev ) ")
    domain = "{}.{}.".format(grafanaHead, str(env))
    targets = ["ticket.goal", "ticket.actual", "meet.plan", "dontmeet.plan","spend.times"]
    # targets = ["spend.times"]
    start = 0
    end = input("Count? ")
    value_start = input("Value Range(?~)? ")
    value_end = input("Value Range(~?)? ")
    timestamp = int(time.time()) - 3600
    interval = int(3600 / (end + 1))
    for x in xrange(start, end):
        timestamp = timestamp + interval
        print "-------------------"
        print "Count: {} Time: {}".format(x, timestamp)
        print "-------------------"
        for target in targets:
            value = random.randint(value_start, value_end)
            common().graphiteLog(domain + target, value,timestamp)
            print "    Send To \"{}\" Data: {} ".format(domain + target, value)
        # time.sleep(0.5)

if __name__ == '__main__':
    main()

