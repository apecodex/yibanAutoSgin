# -*- coding: utf-8 -*-
"""
@Time ： 2020/8/19 下午12:06
@Auth ： apecode.
@File ： main.py
@Software  ： PyCharm
@Blog ： https://liuyangxiong.cn
"""

import json
import random
import time
import util
from yiban import Yiban

login_times = 1
email_str = ""
account = util.readAccount()  # 获取所有的账号和密码

flag = False
for ac in account:
    ac_json = json.loads(ac)
    for aj in ac_json:
        yiban = Yiban(aj, ac_json[aj])
        login = yiban.login()
        if login["response"] != 100:
            print(login["message"])
        else:
            auth = yiban.auth()
            if auth["code"] == 0:
                today_task = yiban.getUncompletedListTime()    # 获取今日签到表单
                if not len(today_task["data"]):
                    print("没有找到今天要提交的表单")
                else:
                    today_task_id = today_task["data"][0]["TaskId"]
                    detail = yiban.getDetail(today_task_id)
                    extend = {
                        "TaskId": today_task_id,
                        "title": "任务信息",
                        "content": [
                            {"label": "任务名称", "value": detail["data"]["Title"]},
                            {"label": "发布机构", "value": detail["data"]["PubOrgName"]},
                            {"label": "发布人", "value": detail["data"]["PubPersonName"]}
                        ]
                    }

                    # 假期表单
#                     task = {
#                         "55e9aaf31b36aada75e4aa84f28827a4": str(round(random.uniform(36.1, 36.9), 1)),
#                         "8e62115236c4ec05c45daff18a6b0e1c": ["以上都无"],
#                         "0596b8e5dab5bbc35daea35e46a2fbfa": "好"
#                     }

                    # 最新表单，体温36.1~36.9随机
                    # 学校表单
                    task = {
                        "6a2c48587652c472b625d612c03831eb": "是",
                        "55e9aaf31b36aada75e4aa84f28827a4": str(round(random.uniform(36.1, 36.9), 1)),
                        "8e62115236c4ec05c45daff18a6b0e1c": ["以上都无"],
                        "0596b8e5dab5bbc35daea35e46a2fbfa": "好"
                    }

                    # 位置

                    night_sgin = '{"Reason":"","AttachmentFileName":"","LngLat":"102.449018,24.875743","Address":"云南省 昆明市 安宁市县街街道昆明冶金高等专科学校-教学大楼 "}'

                    # # 提交表单
                    sb_result = yiban.submitApply(task, extend)
                    # 位置签到
                    yiban.photoRequirements()
                    yiban.deviceState()
                    yiban.sginPostion()
                    ns_result = yiban.nightAttendance(night_sgin)
                    # print(sb_result)
                    print(ns_result)
                    if sb_result["code"] == 0 and ns_result["code"] == 0:
                        print("表单和位置签到提交成功！")
                        share_url = yiban.getShareUrl(sb_result["data"])["data"]["uri"]
                        util.log(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))) +
                                 " 表单和位置签到提交成功 url: " + share_url + " 位置: " + json.loads(night_sgin)["Address"] + "\n")
                    elif sb_result["code"] == 0 and ns_result["code"] != 0:
                        print("表单提交成功！")
                        share_url = yiban.getShareUrl(sb_result["data"])["data"]["uri"]
                        util.log(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))) +
                                 " 表单提交成功 url: " + share_url + "\n")
                    elif sb_result["code"] != 0 and ns_result["code"] == 0:
                        print("位置签到提交成功！")
                        util.log(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))) +
                                 " 位置: " + json.loads(night_sgin)["Address"] + "\n")
                    else:
                        print("失败！")

            else:
                print("登录验证失败，请重新登录!")
