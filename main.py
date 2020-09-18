# -*- coding: utf-8 -*-
"""
@Time ： 2020/8/19 下午12:06
@Auth ： apecode.
@File ： main.py
@Software  ： PyCharm
@Blog ： https://liuyangxiong.cn
"""

import json
import time
import requests
import util
from yiban import Yiban
import re

login_times = 1
email_str = ""
account = json.loads(util.readAccount()[0])

flag = False

for ac in account:
    yiban = Yiban(ac, account[ac])
    while login_times <= 5:
        try:
            login = yiban.login()
            if login is not None and login["response"] == "100":
                try:
                    data_url = auto["data"].get("Data")
                except AttributeError as a:
                    login = yiban.login()
                    auto = yiban.auto()
                    try:
                        data_url = auto["data"].get("Data")
                    except:
                        print("表单和签到提交失败,请手动提交")
                if data_url is not None:  # 授权过期
                    result_html = yiban.session.get(url=data_url, headers=yiban.HEADERS,
                                                cookies={"loginToken": yiban.access_token}).text
                    re_result = re.findall(r'input type="hidden" id="(.*?)" value="(.*?)"', result_html)
                    print(re_result)
                    post_data = {"scope": "1,2,3,"}
                    for i in re_result:
                        post_data[i[0]] = i[1]
                    usersure_result = yiban.session.post(url="https://oauth.yiban.cn/code/usersure",
                                                    data=post_data,
                                                    headers=yiban.HEADERS, cookies={"loginToken": yiban.access_token})
                    if usersure_result.json()["code"] == "s200":
                        print("授权成功！")
                    else:
                        print("授权失败！")
                    auto = yiban.auto()
                # print(auto)
                if auto["code"] == 0:
                    allList = yiban.getUncompletedListTime()
                    if allList["code"] == 0 and allList["data"] != []:
                        nowTime = util.GenerateNowTime();
                        for nowTask in allList["data"]:
                            if nowTask["StartTime"] == nowTime:
                                today_taskID = nowTask["TaskId"]
                                detail = yiban.getDetail(today_taskID)
                                title  = nowTask["Title"]
                                flag = True
                                break
                        if (flag):
                            extend = {
                                "TaskId": today_taskID,
                                "title": "任务信息",
                                "content": [
                                    {"label": "任务名称", "value": detail["data"]["Title"]},
                                    {"label": "发布机构", "value": detail["data"]["PubOrgName"]},
                                    {"label": "发布人", "value": detail["data"]["PubPersonName"]}
                                ]
                            }

                            form_data = util.readTaskForm()[0]
                            reason = util.getReason()[0]
                            yiban.photoRequirements()
                            yiban.deviceState()
                            yiban.sginPostion()
                            night_s = yiban.nightAttendance(reason)
                            sb = yiban.submitApply(form_data, extend)
                            if sb["code"] == 0 and night_s["code"] == 0:
                                print("签到和表单提交成功!")
                                share_url = yiban.getShareUrl(sb["data"])["data"]["uri"]
                            
                                email_str = util.html_format(
                                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
                                    "签到和表单提交成功",
                                    share_url, json.loads(reason)["Address"])
                            
                                util.log(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                                    int(time.time()))) + " 签到和表单提交成功 url: " + share_url + "\n")
                            
                                util.send_mail(email_str)
                            elif sb["code"] == 0 and night_s["code"] != 0:
                                print("表单提交成功!但是签到没成功")
                                share_url = yiban.getShareUrl(sb["data"])["data"]["uri"]
                            
                                email_str = util.html_format(
                                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
                                    "表单提交成功!但是签到没成功!",
                                    share_url, "签到没成功")
                            
                                util.log(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                                    int(time.time()))) + " 表单提交成功!但是签到没成功 url: " + share_url + "\n")
                            
                                util.send_mail(email_str)
                            elif sb["code"] != 0 and night_s["code"] == 0:
                                print("签到提交成功!但是表单没成功")
                            
                                email_str = util.html_format(
                                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
                                    "签到提交成功!但是表单没成功!",
                                    "表单没成功", json.loads(reason)["Address"])
                            
                                util.log(
                                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))) + " 签到提交成功!但是表单没成功")
                                util.send_mail(email_str)
                            else:
                                print("都没有成功!")
                                util.send_mail("提交失败!")
                        else:
                            print("没有可提交的表单!")
                            util.send_mail("没有可提交的表单!")
                    else:
                        print("没有可提交的表单!")
                        util.send_mail("没有可提交的表单!")

                break
            else:
                print(login["message"])
                break
        except requests.exceptions.ConnectionError:
            print("失败, 可能是网络原因, %s 后开始 第'%s'次 尝试..." % (util.getTenAfter(), str(login_times)))
            time.sleep(600)
            login_times += 1
            continue

    if login_times == 6:
        print("可能是网络原因,无法正常访问!请手动签到!")
        util.send_email("可能是网络原因,无法正常访问到易班!请手动签到!")
        login_times = 1
