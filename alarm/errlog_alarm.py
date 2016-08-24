#!/usr/bin/python
#coding=utf-8
"""
error log alarm service (process)
"""

import json

from alarm_service.common import logger
from alarm_service.common import kafka
from alarm_service.common import msgsender
from alarm_service.common import timeutil
from alarm_service.template import errlog_template

app_settings = None
metric_settings = None
errlog_logger = None

threshold_weixin_msg_num = 100  # max count of sending weixin msg for each project everyday
threshold_mail_msg_num = 30 # max count of sending mail msg for each project everyday

current_day = "2016-08-01"  # reset once a day 
count = {
       # "project": { "weixin": 0, "mail": 0 }    
    }  # reset once a day


def init(_app_settings, _metric_settings):
    """
    initialize the error log alarm service
    """
    global app_settings, metric_settings
    app_settings = _app_settings
    metric_settings = _metric_settings

    global current_day
    current_day = timeutil.get_current_day()

    global count
    for project in metric_settings.keys():
        count[project] = { "weixin": 0, "mail": 0 }

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

    errlog_logger.debug("receive a log: %s" % (content))
    
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


def _send_weixin_alarm(log_message, project_name, log_file_name):
    global current_day, count
    
    alarm_type = metric_settings[project_name]["errlog"]["alarm_type"]

    # check whether or not to send weixin alarm
    if alarm_type & 1 == 1:
        # check whether the count of weixin msg for this project has exceeded the threshold
        if count[project_name]["weixin"] >= threshold_weixin_msg_num:
            errlog_logger.warning("the weixin threshold of '%s' has been exceeded" % (project_name))
            return

        if not metric_settings[project_name]["errlog"].has_key("weixin_receivers"):
            errlog_logger.warning("the weixin receivers of errlog in %s has not been configured" % (project_name))
            return

        weixin_receivers = metric_settings[project_name]["errlog"]["weixin_receivers"].strip()
        if weixin_receivers == "":
            errlog_logger.warning("the weixin receivers of errlog in %s are blank" % (project_name))
            return

        weixin_message = errlog_template.get_weixin_message(log_message, project_name, log_file_name, count[project_name]["weixin"])
        result = msgsender.send_weixin(weixin_message, weixin_receivers)
        if result == 0:
            count[project_name]["weixin"] += 1
            errlog_logger.debug("the weixin message has been send successfully")
        else:
            errlog_logger.error("fail to send the weixin message")


def _send_mail_alarm(log_message, project_name, log_file_name):
    global current_day, count
    
    alarm_type = metric_settings[project_name]["errlog"]["alarm_type"]
    
    # check whether or not to send mail alarm
    if alarm_type & 2 == 2:
        # check whether the count of mail msg for this project has exceeded the threshold
        if count[project_name]["mail"] >= threshold_mail_msg_num:
            errlog_logger.warning("the mail threshold of '%s' has been exceeded" % (project_name))
            return

        if not metric_settings[project_name]["errlog"].has_key("mail_receivers"):
            errlog_logger.warning("the mail receivers of errlog in %s has not been configured" % (project_name))
            return

        mail_receivers = metric_settings[project_name]["errlog"]["mail_receivers"].strip()
        if mail_receivers == "":
            errlog_logger.warning("the mail receivers of errlog in %s are blank" % (project_name))
            return

        mail_message = errlog_template.get_mail_message(log_message, project_name, log_file_name, count[project_name]["mail"])
        result = msgsender.send_mail("error日志实时告警", mail_message, mail_receivers)
        if result == 0:
            count[project_name]["mail"] += 1
            errlog_logger.debug("the mail message has been send successfully")
        else:
            errlog_logger.error("fail to send the mail message")


def _send_alarm(log_message, project_name, log_file_name):
    # check whether it is a new day, then reset current_day and count variables
    global current_day, count
    if current_day != timeutil.get_current_day():
        # send a daily report for error log alarm
        _send_daily_errlog_report()

        # update the internal state
        current_day = timeutil.get_current_day()
        for project in count.keys():
            count[project] = { "weixin": 0, "mail": 0 }

    _send_weixin_alarm(log_message, project_name, log_file_name)
    _send_mail_alarm(log_message, project_name, log_file_name)


def _send_daily_errlog_report():
    """
    send a daily report for error log alarm throungh weixin
    """
    statistical_result = {} # project name -> number of alarm daily

    projects = count.keys()
    projects.remove("mock")
    for p in projects:
        statistical_result[p] = max(count[p]["weixin"], count[p]["mail"])

    daily_report = errlog_template.get_daily_report(statistical_result)

    weixin_receivers = app_settings["daily_report_receivers"]["weixin"].strip()
    result = msgsender.send_weixin(daily_report, weixin_receivers)
    if result == 0:
        errlog_logger.debug("the error log daily report has been send successfully")
    else:
        errlog_logger.error("fail to send the error log daily report")


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
            #errlog_logger.debug("receive an error log: %s" % (msg.value))
            _handle_error_log(msg.value)


if __name__ == "__main__":
    logger.init_log("../logs/", "errlog_alarm.log")

    mock_logger = logger.get_logger("main.errlog_alarm")
    mock_logger.info("hello errlog alarm")

