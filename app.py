#!/usr/bin/python

import os
import sys
homepath = os.path.abspath("..")
sys.path.append(homepath)

from alarm_service.config import app_conf
from alarm_service.config import metric_conf
from alarm_service.common import logger
from alarm_service.common import proc
from alarm_service.alarm import errlog_alarm


# global variables, not modity them during runtime.
app_settings = None
metric_settings = None
main_logger = None

def init(env):
    global app_settings, metric_settings
    # load the config
    app_settings = app_conf.get_app_settings(env)
    metric_settings = metric_conf.get_metric_settings(env)
    print "load the config info"

    # init the logger
    logger.init_log(app_settings["log"]["home"], app_settings["log"]["file"])
    print "init the logger"

    global main_logger
    main_logger = logger.get_logger("main")
    if main_logger == None:
        print "get logger failed"
        return
    
    # init the errlog alarm
    errlog_alarm.init(app_settings, metric_settings)


def main(argv):
    if len(argv) != 2:
        print "Usage: %s dev|production" % (argv[0])
        return
    if argv[1] not in ["dev", "production"]:
        print "Error: unvalid parameter"
        print "Usage: %s dev|production" % (argv[0])
        return

    init(argv[1])
    if main_logger == None:
        print "initialize the app failed"
        return

    main_logger.info("alarm-service has been started")
    
    # start errlog alarm
    proc.start(errlog_alarm.run, "errlog alarm process" )


if __name__ == "__main__":
    sys.exit(main(sys.argv))

