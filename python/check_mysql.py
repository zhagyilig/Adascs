#!/usr/bin/python
#coding=utf-8
#author: xtrdb.net

import sys
import os
import getopt
import MySQLdb
import logging

dbhost='192.168.9.116'
dbport=9036
dbuser='monitor'
dbpassword='0kS90PCQf2rKDsgbHbrqH5sg4R'

def checkMySQL():
	global dbhost
	global dbport
	global dbuser
	global dbpassword

	shortargs='h:P:'
	opts, args=getopt.getopt(sys.argv[1:],shortargs)
	for opt, value in opts:
		if opt=='-h':
			dbhost=value
		elif opt=='-P':
			dbport=value
	db = instanceMySQL(dbhost, dbport, dbuser, dbpassword)
	st = db.ishaveMySQL()
	return st

class instanceMySQL:
	conn = None
	def __init__(self, host=None,port=None, user=None, passwd=None):
		self.dbhost= host
		self.dbport = int(port)
		self.dbuser = user
		self.dbpassword = passwd

	def ishaveMySQL(self):
		cmd="ps -ef | egrep -i \"mysqld\" | grep %s | egrep -iv \"mysqld_safe\" | grep -v grep | wc -l" % self.dbport
		mysqldNum = os.popen(cmd).read()
		cmd ="netstat -tunlp | grep \":%s\" | wc -l" % self.dbport
		mysqlPortNum= os.popen(cmd).read()
		if ( int(mysqldNum) <= 0):
			print "error"
			return 1
		if ( int(mysqldNum) > 0 and  mysqlPortNum <= 0):
			return 1
		return 0

	def connect(self):
		try:
			self.conn=MySQLdb.connect(host="%s"%self.dbhost, port=self.dbport,user="%s"%dbuser, passwd="%s"%self.dbpassword)
		except Exception, e:
			print e
			return 1
		return 0
	def disconnect(self):
		if (self.conn):
			self.conn.close()
			self.conn = None


if __name__== "__main__":
	st=checkMySQL()
	sys.exit(st)

