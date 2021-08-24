# -*- coding: utf-8 -*-
"""
@Time ： 2021/8/24 13:00
@Auth ： apecode
@File ：notice.py
@IDE ：PyCharm
@Blog：https://liiuyangxiong.cn

"""
import json
import time
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

import requests
import config


class Notice:

    def __init__(self, admin: dict, account: dict):
        self.admin = admin,
        self.account = account

    def send(self, content):
        if self.account.get("notice") == "" or self.account.get("notice") == "local":
            return Notice.saveLocal(content)
        elif self.account.get("notice") == "mail":
            if self.admin[0]["mail"]["sendMail"] == "" and self.admin[0]["mail"]["authCode"] == "":
                print("未设置发送者邮箱信息，转为本地记录")
                Notice.saveLocal(content)
            else:
                self.send_mail(content)
        else:
            self.sendPushPlus(content)
        print(content)

    def send_mail(self, message: str):
        try:
            host_server = self.admin[0]["mail"]["smtpServer"]
            # 发件人的邮箱
            sendMail = self.admin[0]["mail"]["sendMail"]
            # 邮箱的授权码
            authCode = self.admin[0]["mail"]["authCode"]
            # 收件人邮箱
            receiver = self.account.get("mail")
            # 邮件标题
            mail_title = "易班 " + time.strftime("%Y-%m-%d", time.localtime(int(time.time()))) + " 签到情况"
            # ssl登录
            smtp = SMTP_SSL(host_server)
            smtp.ehlo(host_server)
            smtp.login(sendMail, authCode)

            msg = MIMEText(message, "html", 'utf-8')
            msg["Subject"] = Header(mail_title, 'utf-8')
            msg["From"] = sendMail
            msg["To"] = receiver
            smtp.sendmail(sendMail, receiver, msg.as_string())
            smtp.quit()
            return True
        except Exception as e:
            print(e)
            return False

    # 发送pushPlus
    def sendPushPlus(self, content: str):
        url = 'https://www.pushplus.plus/send'
        headers = {"Content-Type": "application/json"}
        data = json.dumps({
            "token": self.account.get("pushToken"),
            "title": "易班签到通知",
            "content": content,
            "template": "txt"
        })
        response = requests.post(url=url, data=data, headers=headers).json()
        if response['code'] == 200:
            return Notice.log(f"{self.account.get('mobile')}\tPush Plus发送成功！\n")
        else:
            print("发送失败，转为本地记录")
            Notice.saveLocal(content)
            return Notice.log(f"{self.account.get('mobile')}\tPush Plus发送失败！原因: {response['msg']}\n")

    @staticmethod
    def log(message: str):
        with open(file="data/logs.log", mode="a+", encoding="utf-8") as f:
            f.write(message)
            print(message)

    @staticmethod
    def saveLocal(message):
        with open("data/result.log", mode="a+", encoding="utf-8") as w:
            w.write(message)
