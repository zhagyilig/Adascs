#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:xtrdb.net

import os
import sys
import time
import logging
import getopt
import shlex
#import MySQLdb
from subprocess import PIPE, Popen, STDOUT

db_host = "localhost"
db_port = "5501"
db_user = "bkpuser"
db_passwd = '14p48oacU6'
db_name = "mysql"
conf = "/data/mysql/mysql5501/my5501.cnf"
target_dir = "/data/mysql/innobackupex_full/fusCN_0335501_full_%s" %(time.strftime("%Y%m%d"))
pt_xtrabackup = "/usr/bin/innobackupex"
back = "/data/mysql/innobackupex_full"
saved_time = "3"

# start logging
logging.basicConfig(
    filename="/tmp/innobackupex_backup_%s.log" %(time.strftime("%Y%m%d")),
    format="%(asctime)s : %(levelname)s : %(message)s",
    datefmt="%Y-%m-%d %T",
    level=logging.INFO
)
logging.info("Start backup...")

class Backup(object):
    """ Define the backup and apply class. """
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
        """ Xtrabackup start full-backup. """
        command = "{0} --defaults-file={1} --user={2} --password='{3}' --host={4} --port={5} --no-timestamp {6}".format(pt_xtrabackup, self.defaults_file, self.user, self.passwd, self.host, self.port, self.target_dir)
        status = runCommand(command)
        if status == 1:
            return 1

    def applylog(self):
        """ Xtrabackup start full-prepared. """
        command = "%s --defaults-file=%s/backup-my.cnf --apply-log  --user=%s --password='%s' --host=%s --port=%s  %s" % (pt_xtrabackup, target_dir,self.user, self.passwd, self.host,self.port, target_dir)
        status = runCommand(command)
        if status == 1:
            return 1
        return 0

    def removelog(self):
        """ Backup the number of days saved. """        
        command = "find %s -name 'fusCN*' -type d -mtime +%s -exec rm -fr {} \;" %(back,saved_time)
        status = runCommand(command)
        if status == 1:
            return 1
        return 0

def runCommand(command):
    """ Functions that perform the above class method. """
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
        logging.info("Backup up dbszie: %s" %db_size[0])

    removelog_success = t.removelog()
    if removelog_success == 0:
        logging.info('Backup the number of days saved: %s'%saved_time)

    logging.info("End backup.")
