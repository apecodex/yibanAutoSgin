# 免责声明
* 本项目（yibanAutoSgin）涉及的任何脚本，仅供学习测试研究，禁止用于商业用途


* 使用本项目（yibanAutoSgin）时，需先遵守法律法规。使用过程中照成的任何后果，需自行承担，对于任何关于本项目（yibanAutoSgin）的问题概不负责，包括使用过程中导致的任何损失和损害。


* 如果`出现发热、干咳、体寒、体不适、胸痛、鼻塞、流鼻涕、恶心、腹泻等症状`。请立即停止使用本项目（yibanAutoSgin），认真实履行社会义务，及时进行健康申报。


* 如有侵权，请提供相关证明，所有权证明，本人收到后删除相关文件。


* 无论以任何方式查看、复制或使用到本项目（yibanAutoSgin）中的任何脚本，都应该仔细阅读此声明。本人保留随时更改或补充的此免责声明的权利。


* 一旦使用并复制了本项目（yibanAutoSgin）的任何相关脚本，则默认视为您已经接受了此免责声明。


> 使用并复制了本项目（yibanAutoSgin）的任何相关脚本或本人制作的任何脚本，则默认视为您`已经接受`了此免责声明。请仔细阅读


- - - 

### 实现功能

* 表单签到
* 位置签到

### 配置信息
#### 管理员设置
```json
admin = {
    "mail": {
        "sendMail": "",     # 发送人邮箱
        "authCode": "",     # 发送人邮箱授权码
        "smtpServer": "smtp.qq.com",
        "port": "465"
    }
}
```
#### 用户设置
```json
account = [
    {
        "mobile": "",      # 易班手机号
        "password": "",    # 易班密码
        "mail": "",        # 接收的邮箱地址
        "pushToken": "",   # pushPlus的Token
        "notice": ""       # 接收通知的方式 (local：本地记录，mail：邮件通知，pp：Push Plus推送)，默认local
    }
]
```

### 注意修改签到位置

在`config.py`文件中

```python
address = '{"Reason":"","AttachmentFileName":"","LngLat":"102.449018,24.875743","Address":"云南省 昆明市 xxx学校xxx楼 "}'
```

需要修改`LngLat`和`Address`

获取签到座标及地址可以参考: 
https://apecodewx.gitee.io/sixuetang/how

### 环境
python3.8

### 运行方式

```shell
git clone https://ghproxy.com/https://github.com/rookiesmile/yibanAutoSgin.git
cd yibanAutoSgin
python main.py
```

1. 手机上可以下载`Termux`这款软件，配置好之后，把代码copy下来，就可以在手机上运行签到了
2. 租服务器
- - -

### 我的crontab配置(供参考)

```shell
40 6 * * * python3 /root/Documents/Python/yibanAutoSgin/main.py
0 7 * * * python3 /root/Documents/Python/yibanAutoSgin/main.py
30 7 * * * python3 /root/Documents/Python/yibanAutoSgin/main.py
10 12 * * * python3 /root/Documents/Python/yibanAutoSgin/main.py
30 12 * * * python3 /root/Documents/Python/yibanAutoSgin/main.py
0 13 * * * python3 /root/Documents/Python/yibanAutoSgin/main.py
40 19 * * * python3 /root/Documents/Python/yibanAutoSgin/main.py
0 20 * * * python3 /root/Documents/Python/yibanAutoSgin/main.py
30 20 * * * python3 /root/Documents/Python/yibanAutoSgin/main.py
```

### 特别说明
* 自动签到自己琢磨，本脚本只提供签到功能
* 只适合本校使用，其他学校自行抓包
