#!/usr/bin/python
"""
for each metric:
- state: 1 -> open; 0 -> close
- alarm_type: 1(01) -> weixin; 2(10) -> mail; 3(11) -> both;
- weixin_receivers: format as "ybzhan;jjweng"
- mail_receivers: format as "ybzhan@ibenbenc.com;jjwang@ibenbenc.om"
"""

# configuration for development env
_dev_metric_settings = {
        "oms": {
            "errlog": {
                "state": 1,
                "alarm_type": 3,
                "weixin_receivers": "ybzhan",
                "mail_receivers": "ybzhan@ibenben.com"
            },

            "other_metric": {}
        },

        "other_project": {}
    }

# configuration for production env
_metric_settings = {
        "mock": {
            "errlog": {
                "state": 1,
                "alarm_type": 3,
                "weixin_receivers": "ybzhan",
                "mail_receivers": "ybzhan@ibenben.com"
            }
        },
        "oms": {
            "errlog": {
                "state": 1,
                "alarm_type": 1,
                "weixin_receivers": "jjweng",
                "mail_receivers": "jjweng@ibenben.com"
            }
        },
        "wmsadmin": {
            "errlog": {
                "state": 1,
                "alarm_type": 1,
                "weixin_receivers": "qdi",
                "mail_receivers": ""
            }
        },
        "wmsadminapi": {
            "errlog": {
                "state": 1,
                "alarm_type": 1,
                "weixin_receivers": "qdi",
                "mail_receivers": ""
            }
        },
        "pmsadmin": {
            "errlog": {
                "state": 1,
                "alarm_type": 1,
                "weixin_receivers": "sszheng",
                "mail_receivers": ""
            }
        },
        "pmsadminapi": {
            "errlog": {
                "state": 1,
                "alarm_type": 1,
                "weixin_receivers": "sszheng",
                "mail_receivers": ""
            }
        },
        "bmsadmin": {
            "errlog": {
                "state": 1,
                "alarm_type": 1,
                "weixin_receivers": "sszheng",
                "mail_receivers": ""
            }
        },
        "bmsadminapi": {
            "errlog": {
                "state": 1,
                "alarm_type": 1,
                "weixin_receivers": "sszheng",
                "mail_receivers": ""
            }
        },
        "wmsexpress": {
            "errlog": {
                "state": 1,
                "alarm_type": 1,
                "weixin_receivers": "qxu",
                "mail_receivers": ""
            }
        },
        "wmsexpressapi": {
            "errlog": {
                "state": 1,
                "alarm_type": 1,
                "weixin_receivers": "qxu",
                "mail_receivers": ""
            }
        },
        "wmsinventoryapi": {
            "errlog": {
                "state": 1,
                "alarm_type": 1,
                "weixin_receivers": "fgao;jwang",
                "mail_receivers": ""
            }
        },
        "tmsweb": {
            "errlog": {
                "state": 1,
                "alarm_type": 1,
                "weixin_receivers": "jwpeng",
                "mail_receivers": ""
            }
        },
        "testtmsweb": {
            "errlog": {
                "state": 1,
                "alarm_type": 1,
                "weixin_receivers": "jwpeng",
                "mail_receivers": ""
            }
        },
        "cronjob": {
            "errlog": {
                "state": 1,
                "alarm_type": 1,
                "weixin_receivers": "qdi",
                "mail_receivers": ""
            }
        },
        "tmsaddress": {
            "errlog": {
                "state": 1,
                "alarm_type": 1,
                "weixin_receivers": "jwpeng",
                "mail_receivers": ""
            }
        },
        "report": {
            "errlog": {
                "state": 1,
                "alarm_type": 1,
                "weixin_receivers": "jzhang2;jwang",
                "mail_receivers": ""
            }
        },
        "pmsapi": {
            "errlog": {
                "state": 1,
                "alarm_type": 1,
                "weixin_receivers": "fyzhu;qxu",
                "mail_receivers": ""
            }
        }
    }

def get_metric_settings(env):
    if env == "dev":
        return _dev_metric_settings
    else:
        return _metric_settings


if __name__ == "__main__":
    if _dev_metric_settings.has_key("hello"):
        print "in"
    else:
        print "not in"
