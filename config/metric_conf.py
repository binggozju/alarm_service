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
