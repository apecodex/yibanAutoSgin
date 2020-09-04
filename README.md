
## 使用方式:

```git clone https://github.com/rookiesmile/yibanAutoSgin.git```

```pip install requests```

```python main.py```

- - - 

## 目录说明: 

    data:
        存放信息（账号、表单信息、签到信息）
        account.txt:
            {"易班账号":"易班密码"}
        log.txt:
            存放每次签到的信息
        nightSgin.txt:
            {"Reason":"","AttachmentFileName":"","LngLat":"坐标","Address":"地址"}
            需要填写坐标和地址
            比如：
            {"Reason":"","AttachmentFileName":"","LngLat":"102.713989,25.037652","Address":"云南省昆明市五华区护国街道南屏街华域大厦"}
            
        taskForm.txt:
            不用填，除非表单已经更改了
            {"7aefebd412afe11597f8e8a5c28fd54e":"1.身体健康","f89c31fd874cea498c3f1077a4b77109":"1.无状况","4106b198bcda151e1ccb1f9799b41e68":"无"}
    
    main.py:
        运行文件
    util.py:
        里面有的邮箱地址需要自己填写，为send_mail函数
    yiban.py;
        ....
