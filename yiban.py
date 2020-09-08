# -*- coding: utf-8 -*-
"""
@Time ： 2020/8/10 上午11:40
@Auth ： apecode.
@File ： yiban.py
@Software  ： PyCharm
@Blog ： https://liuyangxiong.cn
"""
import json
import re
import time

import requests
import util


class Yiban:
    CSRF = "9cd990dfd520072e0ee032c46df5f99e"
    COOKIES = {"csrf_token": CSRF}
    HEADERS = {"Origin": "https://c.uyiban.com", "User-Agent": "yiban"}
    EMAIL = {}

    def __init__(self, account, passwd):
        self.account = account
        self.passwd = passwd
        self.session = requests.session()

    def request(self, url, method="get", params=None, cookies=None):
        if method == "get":
            response = self.session.get(url=url, timeout=10, headers=self.HEADERS, params=params, cookies=cookies)
        else:
            response = self.session.post(url=url, timeout=10, headers=self.HEADERS, data=params, cookies=cookies)

        return response.json()

    def login(self):
        """
        登录
        :return:
        """
        params = {
            "account": self.account,
            "passwd": self.passwd,
            "ct": 2,
            "app": 1,
            "v": "4.7.11",
            "apn": "ctnet",
            "identify": "0",
        }

        response = self.request("https://mobile.yiban.cn/api/v2/passport/login", params=params, cookies=self.COOKIES)

        if response is not None and response["response"] == "100":
            self.access_token = response["data"]["access_token"]
            self.name = response["data"]["user"]["name"]
            return response
        else:
            return response

    def auto(self) -> json:
        """
        登录验证
        :return:
        """
        location = self.session.get("http://f.yiban.cn/iapp/index?act=iapp7463&v=" + self.access_token,
                                    allow_redirects=False).headers["Location"]
        verifyRequest = re.findall(r"verify_request=(.*?)&", location)[0]
        return self.request(
            "https://api.uyiban.com/base/c/auth/yiban?verifyRequest=" + verifyRequest + "&CSRF=" + self.CSRF,
            cookies=self.COOKIES)

    def getUncompletedList(self) -> json:
        """
        获取未完成的表单
        :return:
        """
        response = self.request("https://api.uyiban.com/officeTask/client/index/uncompletedList?CSRF=" + self.CSRF,
                                cookies=self.COOKIES)
        return response

    def getUncompletedListTime(self) -> json:
        """
        获取特定时间未完成的表单
        :return:
        """
        response = self.request("https://api.uyiban.com/officeTask/client/index/uncompletedList?StartTime=2020-08-31 00:00&EndTime="+time.strftime("%Y-%m-%d 23:59:00", time.localtime(int(time.time())))+"&CSRF=" + self.CSRF,
                                cookies=self.COOKIES)
        return response

    def getCompletedList(self) -> json:
        """
        获取已经完成的表单
        :return:
        """
        return self.request("https://api.uyiban.com/officeTask/client/index/completedList?CSRF=" + self.CSRF,
                            cookies=self.COOKIES)

    def getDetail(self, taskId) -> json:
        """
        获取表单WFId
        获取发布人信息,后面提交表单时要用到
        :param taskId:
        :return:
        """
        response = self.request(
            "https://api.uyiban.com/officeTask/client/index/detail?TaskId=" + taskId + "&CSRF=" + self.CSRF,
            cookies=self.COOKIES)
        self.WFId = response['data']['WFId']
        self.Title = response['data']["Title"]
        self.PubOrgName = response["data"]["PubOrgName"]
        self.PubPersonName = response["data"]["PubPersonName"]
        print("WFID: " + self.WFId)
        return response

    def getForm(self):
        """
        首次使用,需要创建提交表单用的数据
        此方法是用来创建表单数据的
        :return:
        """
        form_data = {}
        response = self.request("https://api.uyiban.com/workFlow/c/my/form/%s?CSRF=%s" % (self.WFId, self.CSRF),
                                cookies=self.COOKIES)
        for i in response["data"]["Form"]:
            if i["component"] == "Radio":
                print(i["props"]["label"] + ": " + i["props"]["extra"])
                for option in i["props"]["options"]:
                    print(option)
                o = input("选择: ")
                form_data[i["id"]] = i["props"]["options"][int(o) - 1]
            elif i["component"] == "Input":
                o = input(i["props"]["label"] + ": " + i["props"]["placeholder"] + ": ")
                form_data[i["id"]] = o
            else:
                pass
        util.writerTaskFrom(form_data)

    def getFormapi(self) -> json:
        """
        首次使用,需要创建提交表单用的数据
        此方法是用来创建表单数据的
        :return:
        """
        form_data = {}
        response = self.request("https://api.uyiban.com/workFlow/c/my/form/%s?CSRF=%s" % (self.WFId, self.CSRF),
                                cookies=self.COOKIES)
        return response

    def nightAttendance(self, reason) -> json:
        """
        晚点名签到
        :param reason: 坐标信息
        :return:
        """
        params = {
            "Code": "",
            "SignInfo": reason,
            "OutState": "1"
        }
        response = self.request("https://api.uyiban.com/nightAttendance/student/index/signIn?CSRF=" + self.CSRF,
                                method="post", params=params, cookies=self.COOKIES)
        return response

    def submitApply(self, data, extend) -> json:
        """
        提交表单
        :param data: 提交表单的参数
        :param extend: 发布人信息
        :return: 表单url
        """
        params = {
            "data": data,
            "extend": json.dumps(extend, ensure_ascii=False)
        }
        return self.request(
            "https://api.uyiban.com/workFlow/c/my/apply/%s?CSRF=%s" % (self.WFId, self.CSRF), method="post",
            params=params,
            cookies=self.COOKIES)

    def getShareUrl(self, initiateId) -> json:
        return self.request(
            "https://api.uyiban.com/workFlow/c/work/share?InitiateId=%s&CSRF=%s" % (initiateId, self.CSRF),
            cookies=self.COOKIES)

    def photoRequirements(self):
        """
        晚点名签到所需
        :return:
        """
        return self.request(
            url="https://api.uyiban.com/nightAttendance/student/index/photoRequirements?CSRF=" + self.CSRF,
            cookies=self.COOKIES)

    def deviceState(self):
        """
        晚点名签到所需
        :return:
        """
        return self.request(url="https://api.uyiban.com/nightAttendance/student/index/deviceState?CSRF=" + self.CSRF,
                            cookies=self.COOKIES)

    def sginPostion(self):
        """
        晚点名签到所需
        :return:
        """
        return self.request(url="https://api.uyiban.com/nightAttendance/student/index/signPosition?CSRF=" + self.CSRF,
                            cookies=self.COOKIES)
