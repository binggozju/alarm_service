#!/usr/bin/python

# configuration for development env
_dev_app_settings = {
        # kafka cluster
        "kafka_hosts": "localhost:9092,localhost:9093",
        "zk_hosts": "localhost:2181",

        # topic of kafka
        "topic_errlog": "alarm-errlog",
        "consumer_group_errlog": "errlog-consumer",

        # log
        "log": {
            "home": "./logs/",
            "file": "alarm-service.log"
        },
        
        # msgsender
        "msgsender": "http://localhost:8090/",
        
        # receivers for daily report
        "daily_report_receivers": {
            "weixin": "ybzhan",
            "mail": "ybzhan@ibenben.com"
        }
    }

# configuration for production env
_app_settings = {
        # kafka cluster
        "kafka_hosts": "10.168.72.226:9092,10.168.76.90:9092,10.168.59.183:9092",
        "zk_hosts": "10.168.72.226:2181,10.168.76.90:2181,10.168.59.183:2181",

        # topic of kafka
        "topic_errlog": "alarm-errlog",
        "consumer_group_errlog": "errlog-consumer",

        # log
        "log": {
            "home": "/data0/alarm-service/logs/",
            "file": "alarm-service.log"
        },
        
        # msgsender
        "msgsender": "http://10.171.199.173:8090/",

        # receivers for daily report
        "daily_report_receivers": {
            "weixin": "wjzhu;ybzhan",
            "mail": "wjzhu@ibenben.com;ybzhan@ibenben.com"
        }
    }

def get_app_settings(env):
    if env == "dev":
        return _dev_app_settings
    else:
        return _app_settings


if __name__ == "__main__":
    print _app_settings
