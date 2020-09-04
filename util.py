# -*- coding: utf-8 -*-
"""
@Time ： 2020/8/10 下午12:31
@Auth ： apecode.
@File ： utili.py
@Software  ： PyCharm
@Blog ： https://liuyangxiong.cn
"""
import json
import time
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL


def readAccount() -> str:
    with open("data/account.txt", encoding="utf-8") as f:
        reason = f.read().splitlines();
    return reason

def log(message):
    with open("data/log.txt", "a+") as w:
        w.write(message)

def getReason():
    with open("data/nightSign.txt", encoding="utf-8") as f:
        reason = f.read().splitlines()
    return reason

def readTaskForm():
    with open("data/taskForm.txt", encoding="utf-8") as r:
        data = r.read().splitlines()
    return data

def writerTaskFrom(form_data):
    with open("data/taskForm.txt", 'w') as w:
        w.write(str(form_data).replace(" ", "").replace("'", "\""))

def getTenAfter():
    now = int(time.time() + 600)
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    timeArray = time.localtime(now)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

def send_mail(message):
    try:
        host_server = 'smtp.qq.com'
        # 发件人的邮箱
        sender_qq = '123@qq.com'
        # 邮箱的授权码
        pwd = ''
        # 发件人的邮箱
        sender_qq_mail = '123@qq.com'
        # 收件人邮箱
        receiver = ''
        # 邮件的正文内容
        mail_content = message
        # 邮件标题
        mail_title = "易班 " + time.strftime("%Y-%m-%d", time.localtime(int(time.time()))) + " 签到情况"
        # ssl登录
        smtp = SMTP_SSL(host_server)
        smtp.ehlo(host_server)
        smtp.login(sender_qq, pwd)

        msg = MIMEText(mail_content, "html", 'utf-8')
        msg["Subject"] = Header(mail_title, 'utf-8')
        msg["From"] = sender_qq_mail
        msg["To"] = receiver
        smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
        smtp.quit()
        return True
    except Exception as e:
        print(e)
        return False

def html_format(date, postContext, url, signStr) -> str:
    html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
            <style>
                body {
                    background: rgba(34, 29, 29);
                }
                h1 {
                    color: crimson;
                    text-align: center;
                }
                h2 {
                    color: #ef3030;
                    text-align: center;
                }
                a {
                    text-decoration: none;
                    color: #590b81;
                }
                span {
                    color: darkslateblue;
                }
            </style>
        </head>
        <body>
            <h1>%s</h1>
            <h2>%s</h2>
            <h2><strong>表单详细: </strong><a href="%s">%s</a></h2>
            <h2><strong>签到位置: </strong><span>%s</span></h2>
        </body>
        </html>
    """ % (date, postContext, url, url, signStr)
    return html