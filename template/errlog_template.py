#!/usr/bin/python
#coding=utf-8


def get_weixin_message(log_message, project_name, log_file_name):
    weixin_message = "\n告警类型: error日志实时告警,\n所属项目: %s,\n日志文件: %s,\n日志内容: %s" % (project_name, log_file_name, log_message)
    return weixin_message


def get_mail_message(log_message, project_name, log_file_name):
    mail_message = "所属项目: %s,\n日志文件: %s,\n日志内容: %s" % (project_name, log_file_name, log_message)
    return mail_message


if __name__ == "__main__":
    print get_weixin_message("an error log in your project", "demo-service", "demo.log")
    print get_mail_message("an error log in your project", "demo-service", "demo.log")

