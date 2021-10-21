# -*- coding: utf-8 -*-
"""
@Time ： 2020/8/19 下午12:06
@Auth ： apecode.
@File ： main.py
@Software  ： PyCharm
@Blog ： https://liuyangxiong.cn
"""

import json
import os
import time
import util
from yiban import Yiban
import config
from notice import Notice

# ===========================================================
# Github actions 使用，本地使用请注释
try:
    config.account[0]["mobile"] = os.environ["YB_MOBILE"]
    config.account[0]["password"] = os.environ["YB_PASSWORD"]
    config.account[0]["mail"] = os.environ["YB_MAIL"]
    config.account[0]["pushToken"] = os.environ["YB_PUSHTOKEN"]
    config.account[0]["notice"] = os.environ["YB_NOTICE"]
except KeyError:
    pass
# # ===========================================================

for ac in config.account:
    yb = Yiban(ac.get("mobile"), ac.get("password"))
    nowPeriod = util.getTimePeriod()  # 获取签到时段数值
    if nowPeriod == 0:
        login = yb.login()
        if (login["response"]) != 100:
            print(login["message"])
        else:
            notice = Notice(config.admin, ac)
            auth = yb.auth()
            if auth["code"] != 0:
                timePeriod = util.fromIntGetTimePeriod(nowPeriod)
                now_task = yb.getUncompletedListTime(timePeriod[0], timePeriod[1])
                print(now_task)
                if not len(now_task["data"]):
                    print("没有找到要提交的表单")
                else:
                    now_task_id = now_task["data"][0]["TaskId"]
                    detail = yb.getDetail(now_task_id)
                    extend = {
                        "TaskId": now_task_id,
                        "title": "任务信息",
                        "content": [
                            {"label": "任务名称", "value": detail["data"]["Title"]},
                            {"label": "发布机构", "value": detail["data"]["PubOrgName"]},
                            {"label": "发布人", "value": detail["data"]["PubPersonName"]}
                        ]
                    }
                    sb_result = yb.submitApply(config.tasks[nowPeriod - 1], extend)
                    if nowPeriod != 3:
                        if sb_result["code"] == 0:
                            # share_url = yb.getShareUrl(sb_result["data"])
                            # result = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))) + " 表单提交成功 url: " + share_url + "\n"
                            result = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))) + " 表单提交成功\n"
                            notice.send(result)
                        else:
                            result = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))) + "表单提交失败！请检查\n"
                            notice.send(time.strftime(result))
                            Notice.log(result)
                    else:
                        # 位置签到
                        yb.photoRequirements()
                        yb.deviceState()
                        yb.signPostion()
                        ns_result = yb.nightAttendance(config.address)
                        if sb_result["code"] == 0 and ns_result["code"] == 0:
                            # share_url = yb.getShareUrl(sb_result["data"])
                            # result = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))) + " 表单和位置签到提交成功 url: " + share_url + " 位置: " + json.loads(config.address)["Address"] + "\n"
                            result = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))) + " 表单和位置签到提交成功 位置: " + json.loads(config.address)["Address"] + "\n"
                            notice.send(result)
                        elif sb_result["code"] == 0 and ns_result["code"] != 0:
                            # share_url = yb.getShareUrl(sb_result["data"])
                            # result = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))) +" 表单提交成功 url: " + share_url + "\n"
                            result = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))) +" 表单提交成功 \n"
                            notice.send(result)
                        elif sb_result["code"] != 0 and ns_result["code"] == 0:
                            result = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))) +" 位置: " + json.loads(config.address)["Address"] + "\n"
                            notice.send(result)
                        else:
                            result = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(time.time())) + "签到失败，请检查\n")
                            notice.send(result)
            else:
                print("登录授权失败，请重新登录!")
                notice.send(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(time.time())) + "登录授权失败，请重新登录\n"))
    else:
        print("未到签到时间")
