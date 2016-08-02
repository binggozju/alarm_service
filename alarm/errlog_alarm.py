#!/usr/bin/python
#coding=utf-8
"""
error log alarm service (process)
"""

import json

from alarm_service.common import logger
from alarm_service.common import kafka
from alarm_service.common import msgsender
from alarm_service.template import errlog_template

app_settings = None
metric_settings = None
errlog_logger = None

def init(_app_settings, _metric_settings):
    """
    initialize the error log alarm service
    """
    global app_settings, metric_settings
    app_settings = _app_settings
    metric_settings = _metric_settings

    global errlog_logger
    errlog_logger = logger.get_logger("root.errlog_alarm")


def _handle_error_log(content):
    try:
        json_obj = json.loads(content)
    except Exception as e:
        errlog_logger.error("fail to parse, %s" % (e))
        return

    if not json_obj.has_key("filename"):
        return
    log_file_name = json_obj["filename"]
    if log_file_name == "catalina.out":
        return

    if not json_obj.has_key("message"):
        return
    log_message = json_obj["message"]
    if not json_obj.has_key("type"):
        return
    project_name = json_obj["type"]

    # exit if the project has not been config
    if not metric_settings.has_key(project_name):
        return
    # exit if the errlog alarm item is not included in this project
    if not metric_settings[project_name].has_key("errlog"):
        return
    # exit if the errlog alarm item of this project has been closed
    if metric_settings[project_name]["errlog"]["state"] == 0:
        return

    _send_alarm(log_message, project_name, log_file_name)


def _send_alarm(log_message, project_name, log_file_name):
    alarm_type = metric_settings[project_name]["errlog"]["alarm_type"]

    # check whether or not to send weixin alarm
    if alarm_type & 1 == 1:
        if not metric_settings[project_name]["errlog"].has_key("weixin_receivers"):
            errlog_logger.warning("the weixin receivers of errlog in %s has not been configured" % (project_name))
            return

        weixin_receivers = metric_settings[project_name]["errlog"]["weixin_receivers"].strip()
        if weixin_receivers == "":
            errlog_logger.warning("the weixin receivers of errlog in %s are blank" % (project_name))
            return

        weixin_message = errlog_template.get_weixin_message(log_message, project_name, log_file_name)
        msgsender.send_weixin(weixin_message, weixin_receivers)

    # check whether or not to send mail alarm
    if alarm_type & 2 == 2:
        if not metric_settings[project_name]["errlog"].has_key("mail_receivers"):
            errlog_logger.warning("the mail receivers of errlog in %s has not been configured" % (project_name))
            return

        mail_receivers = metric_settings[project_name]["errlog"]["mail_receivers"].strip()
        if mail_receivers == "":
            errlog_logger.warning("the mail receivers of errlog in %s are blank" % (project_name))
            return

        mail_message = errlog_template.get_mail_message(log_message, project_name, log_file_name)
        msgsender.send_mail("error日志实时告警", mail_message, mail_receivers)
    
    errlog_logger.debug("the alarm message for error log has been sended to receivers")


def run():
    """
    run the error log alarm service, which should be launched by a new process
    """
    if errlog_logger == None:
        print "errlog_alarm has not been initialized"
        return
    
    # get config info about kafka
    topic_name = app_settings["topic_errlog"]
    consumer_group = app_settings["consumer_group_errlog"]
    errlog_logger.info("topic -> %s | consumer group -> %s" % (topic_name, consumer_group))

    consumer = kafka.get_consumer(topic_name, consumer_group)
    errlog_logger.info("errlog process get a consumer")

    # start consume the error log from kafka
    for msg in consumer:
        if msg is not None:
            errlog_logger.debug("receive an error log: %s" % (msg.value))
            _handle_error_log(msg.value)


if __name__ == "__main__":
    logger.init_log("../logs/", "errlog_alarm.log")

    mock_logger = logger.get_logger("main.errlog_alarm")
    mock_logger.info("hello errlog alarm")

