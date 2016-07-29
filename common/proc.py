#!/usr/bin/python

import time
import multiprocessing


def start(run_func, proc_name):
    process = multiprocessing.Process(target=run_func, name=proc_name)
    process.start()

def mock_func():
    count = 0
    while 1:
        count += 1
        print "this is the %dth message" % (count)
        time.sleep(1)


if __name__ == "__main__":
    start(mock_func, "mock process 1")
    start(mock_func, "mock process 2")
    print "start the mock process"

