#!/usr/bin/python

from alarm_service.common import logger


app_settings = None
metric_settings = None
errlog_logger = None

def init(_app_settings, _metric_settings):
    global app_settings, metric_settings
    app_settings = _app_settings
    metric_settings = _metric_settings

    global errlog_logger
    errlog_logger = logger.get_logger("main.errlog_alarm")

    print "init errlog alarm"


def run():
    if errlog_logger == None:
        print "errlog_alarm has not been initialized"
        return
    pass


if __name__ == "__main__":
    logger.init_log("../logs/", "errlog_alarm.log")

    mock_logger = logger.get_logger("main.errlog_alarm")
    mock_logger.info("hello errlog alarm")

