#!/usr/bin/python
"""
the entrance for alarm service.
"""

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
homepath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(homepath)
sys.path.append("/var/www")

from alarm_service.config import app_conf
from alarm_service.config import metric_conf
from alarm_service.common import logger
from alarm_service.common import kafka
from alarm_service.common import msgsender
from alarm_service.common import proc
from alarm_service.alarm import errlog_alarm


# global variables, not modity them during runtime.
app_settings = None
metric_settings = None
main_logger = None

def init(env):
    """
    the item to be init:
    * global variables about the configuration
    * the common module, such as logger, kafka, msgsender
    * the alarm module, such as errlog alarm
    """
    global app_settings, metric_settings
    # load the config
    app_settings = app_conf.get_app_settings(env)
    metric_settings = metric_conf.get_metric_settings(env)
    print "load the config info"

    # init the common modules
    logger.init(app_settings["log"]["home"], app_settings["log"]["file"])
    print "init the logger module"
    kafka.init(app_settings["kafka_hosts"], app_settings["zk_hosts"])
    print "init the kafka module"
    msgsender.init(app_settings["msgsender"])
    print "init the msgsender module"

    # init the alarm modules
    errlog_alarm.init(app_settings, metric_settings)
    print "init the errlog alarm module"
    
    global main_logger
    main_logger = logger.get_logger("root")
    if main_logger == None:
        print "get logger failed"
        return
    

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
    
    # start errlog alarm module
    proc.start(errlog_alarm.run, "errlog alarm process" )


if __name__ == "__main__":
    sys.exit(main(sys.argv))

