#!/usr/bin/python
# coding=utf-8

import json
import urllib
import urllib2

msgsender_url = ""
mail_url = ""
weixin_url = ""

def init(url):
    global msgsender_url, mail_url, weixin_url
    msgsender_url = url
    mail_url = msgsender_url + "mail/async"
    weixin_url = msgsender_url + "weixin/async"


def send_mail(subject, content, receivers):
    post_args = {"subject": subject, "content": content, "receivers": receivers}
    post_data = json.dumps(post_args)

    request = urllib2.Request(url=mail_url, data=post_data)
    request.add_header("Accept", "application/json")
    request.add_header("Content-Type", "application/json; charset=utf-8")
    response = urllib2.urlopen(request)
    data = response.read()
    print data


def send_weixin(message, receivers):
    post_args = {"content": message, "receivers": receivers}
    post_data = json.dumps(post_args)

    request = urllib2.Request(url=weixin_url, data=post_data)
    request.add_header("Accept", "application/json")
    request.add_header("Content-Type", "application/json; charset=utf-8")
    response = urllib2.urlopen(request)
    data = response.read()
    print data


if __name__ == "__main__":
    init("http://localhost:8090/")
    send_weixin("message from msgsender.py", "ybzhan")
    send_mail("error日志实时告警", "你好，有一条新的错误日志产生", "ybzhan@ibenben.com")

