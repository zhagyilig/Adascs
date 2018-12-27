#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
# File      : zabbix_report.py
# Time      : 2017/12/8
# 知数堂吴老师(wubx.net)之作，我根据自己的生产场景做了修改.

import sys
import MySQLdb
import time
from datetime import datetime, timedelta
import calendar  # 日历
import os
import os.path

from tempfile import TemporaryFile   # 临时文件
from xlwt import Workbook,easyxf
from xlrd import open_workbook

# 当天日期
#today = datetime.date.today()
"""
>>> datetime.date.today()
datetime.date(2017, 12, 8)
"""

# 生成报表的目录
report_dir="/tmp/reports"

# MySQL的相关信息
dbhost='10.33.67.228'
port=3306
user = 'wubx_all'
password = 'abcd'
database = 'zabbix'


# 要生成执行的KEY，都存到此元组中
keys = ("cpuload","disk_usage","network_in","network_out")
keys = "'system.cpu.util[,idle]','system.cpu.util[,iowait]','vfs.fs.size[/data,free]'"
keys = "'system.cpu.util[,idle]'"

# 除boolen型（如vip)的监控项外，都设置了阀值，出报表区间内最大值操作此值的，显示背景红色
# 所有没有单独判断的key, 都要在此字典中定义其阀值
# 网卡流量阀值：50M/s
thre_dic = {"cpuload":15,"disk_usage":85,"network_in":409600}

# 自定义生成报表：
def custom_report(startTime,endTime):
	sheetName =  time.strftime('%m%d_%H%M',startTime) + "_TO_" +time.strftime('%m%d_%H%M',endTime)
	customStart = time.mktime(startTime)
	customEnd = time.mktime(endTime)
	generate_excel(customStart,customEnd,0,sheetName)

# 按日生成报表：
# 	以执行脚本当前unix timestamp和当天午夜的unix timestamp来抽取报表
#	脚本一定要24点之前运行
def daily_report():
#	today = datetime.date.today() #获取今天日期
	dayStart = time.mktime(today.timetuple()) #由今天日期，取得凌晨unix timestamp
	dayEnd = time.time() #获取当前系统unix timestamp
	sheetName = time.strftime('%Y%m%d',time.localtime(dayEnd))
	generate_excel(dayStart,dayEnd,1,sheetName)


# 按星期生成报表
def weekly_report():
	lastMonday = today
#	lastMonday = datetime.date.today()#获取今天日期
#取得上一个星期一
	while lastMonday.weekday() != calendar.MONDAY:
		lastMonday -= datetime.date.resolution

	weekStart = time.mktime(lastMonday.timetuple())# 获取周一午夜的unix timestamp
	weekEnd = time.time()
#获取当前系统unix timestamp
#weekofmonth = (datetime.date.today().day+7-1)/7
	weekofmonth = (today.day+7-1)/7
	sheetName = "weekly_" + time.strftime('%Y%m',time.localtime(weekEnd)) + "_" + str(weekofmonth)
	generate_excel(weekStart,weekEnd,2,sheetName)

#-------------------------------------------------------------
# 按月生成报表
#-------------------------------------------------------------

def monthly_repport():
#	firstDay =  datetime.date.today() #当前第一天的日期
	firstDay =  today #当前第一天的日期
#取得当月第一天的日期
	while firstDay.day != 1:
		firstDay -= datetime.date.resolution

	monthStart = time.mktime(firstDay.timetuple()) #当月第一天的unix timestamp
	monthEnd = time.time()	#当前时间的unix timestamp
	sheetName = "monthly_" + time.strftime('%Y%m',time.localtime(monthEnd))
	generate_excel(monthStart,monthEnd,3,sheetName)


#-------------------------------------------------------------
#  获取MySQL Connection
#-------------------------------------------------------------
def getConnection():
# print "准备连接MySQL "
	try:
		connection=MySQLdb.connect(host=dbhost,port=port,user=user,passwd=password,db=database,connect_timeout=10);
	except MySQLdb.Error as e:
		print("ABC Error %d: %s" % (e.args[0], e.args[1]))
		sys.exit(1)
	return connection

#-------------------------------------------------------------
# 返回所有主机IP和hostid, 如：('192.168.10.62', 10113L,0)
#-------------------------------------------------------------

def getHosts():
    conn=getConnection()
    cursor = conn.cursor()
    command = cursor.execute("""select host,hostid from hosts where host<>'Zabbix server' and host<>'' and host<>'127.0.0.1' and status=0 and flags=0 order by host;""");
    hosts = cursor.fetchall()
    cursor.close()
    conn.close()
    return hosts

#-------------------------------------------------------------
# 返回指定主机监控Item的itmeid,
#-------------------------------------------------------------
def getItemid(hostid):
	keys_str =keys
	conn=getConnection()
	cursor = conn.cursor()
	command = cursor.execute("""select itemid from items where hostid=%s and key_ in ('%s')""" %(hostid,keys_str));
	itemids =  cursor.fetchall()
	cursor.close()
	conn.close()
	return itemids
#-------------------------------------------------------------
# 返回无指定hostid主机的报表值， 只针对数字history表中
#-------------------------------------------------------------

def getReportById_1(hostid,start,end):
	keys_str = "','".join(keys)
	keys_str = keys
	conn=getConnection()
	cursor = conn.cursor()
	#print "select items.itemid , key_ as key_value ,units, max(history.value) as max,avg(history.value) as average ,min(history.value) as min  from history, items where items.hostid=%s and items.key_ in ('%s')and items.value_type=0  and history.itemid=items.itemid  and (clock>%s and clock<%s)  group by itemid, key_value;" %(hostid,keys_str,start,end)
	command = cursor.execute("""select items.itemid , key_ as key_value ,units, max(history.value) as max,avg(history.value) as average ,min(history.value) as min  from history, items where items.hostid=%s and items.key_ in (%s)and items.value_type=0  and history.itemid=items.itemid  and (clock>%s and clock<%s)  group by itemid, key_value;""" %(hostid,keys_str,start,end));
	values =  cursor.fetchall()
	cursor.close()
	conn.close();
	return values

#-------------------------------------------------------------
# 返回无指定hostid主机的报表值， 只针无符号数history_uint表, items.value_type=3
#-------------------------------------------------------------

def getReportById_2(hostid,start,end):
	keys_str = "','".join(keys)
	conn=getConnection()
	cursor = conn.cursor()
	command = cursor.execute("""select items.itemid , key_ as key_value ,units, max(history_uint.value) as max,avg(history_uint.value) as average ,min(history_uint.value) as min  from history_uint, items where items.hostid=%s and items.key_ in ('%s')and items.value_type=3  and history_uint.itemid=items.itemid and (clock>%s and clock<%s) group by itemid, key_value;""" %(hostid,keys_str,start,end));
	values =  cursor.fetchall()
	cursor.close()
	conn.close();
	return values


###############
argvCount=len(sys.argv)
if argvCount<2:
    print("Time  error")
    exit(1)

dateFormat="%Y-%m-%d %H:%M:%S"
startTime=time.mktime(datetime.strptime(sys.argv[1],dateFormat).timetuple())
#print startTime

stopTime=time.mktime(datetime.strptime(sys.argv[2],dateFormat).timetuple())
#print stopTime
hosts=getHosts()
for host,hostid in hosts:
    #print host,hostid
    values=getReportById_1(hostid,startTime,stopTime)
    for v in values:
           if int(v[5])<91:
               print("\033[31m%s,%s,%s \033[0m"%(host,v[4],v[5]))
           print("%s,%s,%s"%(host,v[4],v[5]))
