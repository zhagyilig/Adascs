#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# Author:xtrdb.net

import os
import sys
import errno
import time
import logging
import getopt
import shlex
import MySQLdb
from subprocess import PIPE, Popen, STDOUT

db_host = "116.196.xx.16"
db_port = "9036"
db_user = "zyl"
db_passwd = 'g`QnpqD)P>}25B`^l1h)xxxx'
db_name = "mysql"
conf = "/data/mysql/mysql9036/my9036.cnf"
target_dir = "/data/full_back/test_9036_full_{}".format(time.strftime("%Y%m%d"))
pt_xtrabackup = "/usr/bin/innobackupex"

# start logging
logging.basicConfig(
    filename="/tmp/innobackupex.log",
    format="%(asctime)s:%(levelname)s:%(message)s",
    datefmt="%Y-%m-%d %T",
    level=logging.INFO,
)
logging.info("Start backup...")

class Backup(object):
    def __init__(self,db_conf,user,host,passwd,port,bak_dir):
        self.user = db_user
        self.host = db_host
        self.passwd = db_passwd
        self.port = db_port
        if conf == None:
            self.defaults_file = "/etc/my.cnf"
        else:
            self.defaults_file = conf

        self.target_dir = target_dir

    def backup(self):
        command = "{0} --defaults-file={1} --user={2} --password='{3}' --host={4} --port={5} --no-timestamp {6}".format(pt_xtrabackup, self.defaults_file, self.user, self.passwd, self.host, self.port, self.target_dir)
        print(command)
        status = runCommand(command)
        if status == 1:
            return 1

    def applylog(self):
        command = "%s --defaults-file=%s/backup-my.cnf --apply-log  --user=%s --password='%s' --host=%s --port=%s  %s" % (pt_xtrabackup, target_dir,self.user, self.passwd, self.host,self.port, target_dir)
        print(command)
        status = runCommand(command)
        if status == 1:
            return 1
        return 0
def runCommand(command):
    cmd = shlex.split(command)
    logging.debug('Running back command: "' + command + '"')
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    for line in proc.stderr:
        logging.warning(str(line.strip()))

    for line in proc.stdout:
        logging.debug(str(line.strip()))

    proc.wait()

    if proc.returncode != 0:
        logging.critical('Command failed with return code "' + str(proc.returncode) + '"')
    else:
        logging.debug('Command successfully finished with returncode "' + str(proc.returncode) + '"')
        return 0

if __name__ == '__main__':
    t = Backup("defaults_file","db_user","db_passwd","db_host",9036,"target_dir")
    t.backup()
    backup_status = t.applylog()
    if backup_status == 0:
        db_size = os.popen("du -sh %s" %target_dir).read().split("\t")
        logging.info("backup up dbszie: %s" %db_size[0])

    logging.info("End backup")



