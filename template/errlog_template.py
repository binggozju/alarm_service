#!/usr/bin/python
#coding=utf-8


def get_weixin_message(log_message, project_name, log_file_name, seq_id):
    weixin_message = "\n告警类型: error日志实时告警,\n所属项目: %s,\n告警序号: %s,\n日志文件: %s,\n日志内容: %s" % (project_name, seq_id, log_file_name, log_message)
    return weixin_message


def get_mail_message(log_message, project_name, log_file_name, seq_id):
    mail_message = "所属项目: %s,\n告警序号: %s,\n日志文件: %s,\n日志内容: %s" % (project_name, seq_id, log_file_name, log_message)
    return mail_message


def get_weixin_daily_report(statistical_result):
    weixin_daily_report = "error日志实时告警简报"
    weixin_daily_report += "\n------------------------------"
    weixin_daily_report += "\n%-25s%s" % ("项目", "告警次数")
    
    for project, num in statistical_result.items():
        weixin_daily_report += "\n%-25s%d" % (project, num)
    return weixin_daily_report


def get_mail_daily_report(statistical_result):
    mail_daily_report = "%-40s%s" % ("项目名称", "告警次数")
    mail_daily_report += "\n------------------------------------------------------"

    for project, num in statistical_result.items():
        mail_daily_report += "\n%-40s%d" % (project, num)

    mail_daily_report += "\n------------------------------------------------------"
    mail_daily_report += "\n备注说明:"
    mail_daily_report += "\n* 各项目告警次数限额100次，告警次数等于100通常表示当天error日志远多于100条"
    mail_daily_report += "\n* 告警次数为0表示该项目尚未接入alarm service或日志不符合标准格式"
    mail_daily_report += "\n* 该简报仅作为参考，旨在监督各项目提升服务质量，减少错误"
    return mail_daily_report


if __name__ == "__main__":
    print get_weixin_message("an error log in your project", "demo-service", "demo.log", 1)
    print get_mail_message("an error log in your project", "demo-service", "demo.log", 1)
    
    statistical_result = {"mock": 1, "project1": 2, "project2": 3}
    weixin_daily_report = get_weixin_daily_report(statistical_result)
    print weixin_daily_report
    mail_daily_report = get_mail_daily_report(statistical_result)
    print mail_daily_report
