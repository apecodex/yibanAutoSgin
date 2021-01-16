
## 使用方式:

```git clone https://github.com/rookiesmile/yibanAutoSgin.git```

```pip install requests```

```python main.py```

- - - 

### 注意修改签到位置

在`main.py`文件中

```night_sgin = '{"Reason":"","AttachmentFileName":"","LngLat":"102.449018,24.875743","Address":"云南省 昆明市 安宁市县街街道昆明冶金高等专科学校-教学大楼 "}'```

需要修改`LngLat`和`Address`

获取签到座标及地址可以参考: 
https://apecodewx.gitee.io/sixuetang/how

### 运行方式

1. 手机上可以下载`Termux`这款软件，配置好之后，把代码copy下来，就可以中手机上运行签到了
2. 租服务器
- - -

自动签到自己琢磨，本脚本只提供签到功能

在`account.txt`填入账号和密码即可

只适合本校使用，其他学校自行抓包
