# -*- coding: utf-8 -*-
"""
@Time ： 2020/8/10 下午12:31
@Auth ： apecode.
@File ： utili.py
@Software  ： PyCharm
@Blog ： https://liuyangxiong.cn
"""

import time


def getTenAfter():
    now = int(time.time() + 600)
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    timeArray = time.localtime(now)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


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


# 获取时段
def getTimePeriod() -> int:
    def period(t) -> int:
        return int(time.mktime(time.strptime(time.strftime("%Y-%m-%d {}".format(t), time.localtime(int(time.time()))), '%Y-%m-%d %H:%M:%S')))
    nowTime = int(time.time())
    if period("6:30:00") < nowTime <= period("9:00:00"):    # 晨检
        return 1
    elif period("12:00:00") < nowTime <= period("14:30:00"):    # 午检
        return 2
    elif period("19:30:00") < nowTime <= period("21:30:00"):    # 晚检
        return 3
    else:
        return 0    # 未到时间


# 通过数值得到时段
def fromIntGetTimePeriod(num: int):
    if num == 1:
        return [
            time.strftime("%Y-%m-%d 6:30:00", time.localtime(int(time.time()))),
            time.strftime("%Y-%m-%d 9:00:00", time.localtime(int(time.time())))
        ]
    elif num == 2:
        return [
            time.strftime("%Y-%m-%d 12:00:00", time.localtime(int(time.time()))),
            time.strftime("%Y-%m-%d 14:30:00", time.localtime(int(time.time())))
        ]
    elif num == 3:
        return [
            time.strftime("%Y-%m-%d 19:30:00", time.localtime(int(time.time()))),
            time.strftime("%Y-%m-%d 21:30:00", time.localtime(int(time.time())))
        ]
    else:
        return []

# 根据当前时间判断晨检、午检、晚检
def GenerateNowTime() -> str:
    dayTime = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 9:00:00", time.localtime(
                                int(time.time()))), '%Y-%m-%d %H:%M:%S')))
    nowTime = int(time.time())
    if nowTime > dayTime:
        dayTime = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 14:30:00", time.localtime(
                        int(time.time()))), '%Y-%m-%d %H:%M:%S')))
        if nowTime > dayTime:
            dayTime = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 19:30:00", time.localtime(
                        int(time.time()))), '%Y-%m-%d %H:%M:%S')))
        else:
            dayTime = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 12:00:00", time.localtime(
                        int(time.time()))), '%Y-%m-%d %H:%M:%S')))
    else:
        dayTime = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 06:30:00", time.localtime(
                        int(time.time()))), '%Y-%m-%d %H:%M:%S')))
    return dayTime

def when_time():
    dayTime = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 9:00:00", time.localtime(
                                int(time.time()))), '%Y-%m-%d %H:%M:%S')))
    nowTime = int(time.time())
    if nowTime > dayTime:
        dayTime = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 14:30:00", time.localtime(
                        int(time.time()))), '%Y-%m-%d %H:%M:%S')))
        if nowTime > dayTime:
            return 2   # 表示 晚检
        else:
            return 1   # 表示 午检
    else:
        return 0   # 表示 晨检
