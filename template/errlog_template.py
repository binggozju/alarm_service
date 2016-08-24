#!/usr/bin/python
#coding=utf-8

def get_weixin_message(log_message, project_name, log_file_name, seq_id):
    weixin_message = "\n告警类型: error日志实时告警,\n所属项目: %s,\n告警序号: %s,\n日志文件: %s,\n日志内容: %s" % (project_name, seq_id, log_file_name, log_message)
    return weixin_message


def get_mail_message(log_message, project_name, log_file_name, seq_id):
    mail_message = "所属项目: %s,\n告警序号: %s,\n日志文件: %s,\n日志内容: %s" % (project_name, seq_id, log_file_name, log_message)
    return mail_message


def get_daily_report(statistical_result):
    daily_report = "error日志实时告警统计日报"
    daily_report += "\n----------------------------------------"
    daily_report += "\n%-25s%s" % ("项目", "告警次数")
    
    for project, num in statistical_result.items():
        daily_report += "\n%-25s%d" % (project, num)
    return daily_report


if __name__ == "__main__":
    print get_weixin_message("an error log in your project", "demo-service", "demo.log", 1)
    print get_mail_message("an error log in your project", "demo-service", "demo.log", 1)
    
    statistical_result = {"mock": 1, "project1": 2, "project2": 3}
    daily_report = get_daily_report(statistical_result)
    print daily_report
