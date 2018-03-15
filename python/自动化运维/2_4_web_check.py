#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : xtrdb.net

import pycurl
import os
import sys
import time

URL = 'http://xtrdb.net'
c = pycurl.Curl()

c.setopt(pycurl.URL, URL)
c.setopt(pycurl.CONNECTTIMEOUT, 5)
c.setopt(pycurl.TIMEOUT, 5)
c.setopt(pycurl.NOPROGRESS, 1)
c.setopt(pycurl.FORBID_REUSE, 1)
c.setopt(pycurl.MAXREDIRS, 1)
c.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)

indexfile = open(os.path.dirname(os.path.realpath(__file__))+"/context.txt", "wb")
c.setopt(pycurl.WRITEHEADER, indexfile)
c.setopt(pycurl.WRITEDATA, indexfile)

try:
    c.perform()
except Exception as e:
    print("connection error: " + str(e))
    indexfile.close()
    c.close()
    sys.exit()

NAMELOOKUP_TIME = c.getinfo(c.NAMELOOKUP_TIME)
CONNECT_TIME = c.getinfo(c.CONNECT_TIME)
PRETRANSFRT_TIME = c.getinfo(c.PRETRANSFER_TIME)
STARTTRANSFER_TIMR = c.getinfo(c.STARTTRANSFER_TIME)
TOTAL_TIME = c.getinfo(c.TOTAL_TIME)
SIZE_DOWNLOAD = c.getinfo(c.SIZE_DOWNLOAD)
HEADER_SIZE = c.getinfo(c.HEADER_SIZE)
SPEED_DOWNLOAD = c.getinfo(c.SPEED_DOWNLOAD)
HTTP_CODE = c.getinfo(c.HTTP_CODE)

print("HTTP状态码:   %s " %(HTTP_CODE))
print("DNS解析时间： %.2f ms " %(NAMELOOKUP_TIME * 1000))
print("建立连接时间：%.2f ms " %(CONNECT_TIME * 1000))
print("准备传输时间：%.2f ms " %(PRETRANSFRT_TIME *1000))
print("传输开始时间：%.2f ms " %(STARTTRANSFER_TIMR * 1000))
print("传输结束总时间: %.2f ms " %(TOTAL_TIME))
print("下载包数据大小: %d bytes/s " %SIZE_DOWNLOAD)
print("HTTP头部大小:  %d bytes/s " %HEADER_SIZE)
print("平均下载速度： %d bytes/s " %SPEED_DOWNLOAD)

indexfile.close()
c.close()

# output:
HTTP状态码:   200 
DNS解析时间： 3759.00 ms 
建立连接时间：4009.00 ms 
准备传输时间：4009.00 ms 
传输开始时间：4165.00 ms 
传输结束总时间: 4.29 ms 
下载包数据大小: 71921 bytes/s 
HTTP头部大小:  603 bytes/s 
平均下载速度： 17980 bytes/s
