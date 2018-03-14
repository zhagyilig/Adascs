#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : xtrdb.net
# File   : smtp_mail.py
# Time   : 2018/3/14

import smtplib
import string

HOST = "smtp.qq.com"
SUBJECT = "Test email from python"
TO = "316@qq.com"
FROM = "81@qq.com"
text = "Python rules them all!"
# BODY= string.join((   # python2 的用法
#     "From: %s" %FROM,
#     "To: %s" %TO,
#     "Subject: %s" %SUBJECT,
#     "",
#     text
# ),"\t\n")

BODY= "\r\n".join((   # python3 的用法
    "From: %s" %FROM,
    "To: %s" %TO,
    "Subject: %s" %SUBJECT,
    "",
    text
))

server = smtplib.SMTP()
server.connect(HOST,"587")
server.starttls()
server.login("81@qq.com","password")
server.sendmail(FROM, [TO], BODY)
server.quit()


## python3与python2中的string.join()函数
在python2中，string 模块中有一个join()函数，用于以特定的分隔符分隔源变量中的字符串，将其作为新的元素加入到一个列表中，例如：
body=string.join((
                          "From： %s" % FROM,
                          "To: %s" % TO,
                          "Subject: %s" % SUBJECT,
                          ""
                          text
                          ),"\r\n") 
这是一个电子邮件的标准格式，通过string.join()函数，可以把元组中的各个字段以"\r\n"分隔后保存到body变量中

但是在python3中，string模块中取消了join()函数，join()函数作为一个全局函数被使用，函数变量也有两个改为了一个使用方法为：

复制代码
body="\r\n".join((
                          "From： %s" % FROM,
                          "To: %s" % TO,
                          "Subject: %s" % SUBJECT,
                          ""
                          text
                    ))  
即，原来string模块的申明位置定义分隔符，要分割的源变量整体作为一个参数传入join()函数
