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
server.login("8xx554@qq.com","pass")
server.sendmail(FROM, [TO], BODY)
server.quit()
