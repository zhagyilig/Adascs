#!/usr/bin/env python3
# coding=utf-8
# Author: YilingZhang


import os
import sys
import time
import shlex
import logging
import pymysql
import traceback
from subprocess import PIPE, Popen, STDOUT

"""
1.Xtrabackup required permissions:
CREATE USER 'bkpuser'@'localhost' IDENTIFIED BY 'bkpuser51888;
GRANT INSERT, RELOAD, PROCESS, LOCK TABLES, REPLICATION CLIENT ON *.* TO 'bkpuser'@'localhost'

2.Create schema:
CREATE DATABASE xtrabackup;
USE xtrabackup;
CREATE TABLE `innobackup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `db_user` varchar(32) NOT NULL,
  `db_passwd` varchar(32) NOT NULL,
  `server_id` int(11) NOT NULL,
  `ctime` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

# MySQL connection infomation.
db_host = "localhost"
db_port = 9036
db_user = "bkpuser"
db_passwd = "xxx"
db_socket = "/home/mysql/mysql_%s/mysql.sock" % (db_port)
db_name = "xtrabackup"

# Backup options.
db_serverid = "0229036"
back = "/home/mysql/innobackupex_full"
conf = "/home/mysql/mysql_%s/my%s.cnf" % (db_port, db_port)
business = "YP"
target_dir = "%s/%s_%s_full_%s" % (back, business, db_serverid, time.strftime("%Y%m%d%H%M%S"))
monitor = "/tmp/zabbix"
monitor_file = "%s/db_innobackup_status" % (monitor)

# Xtrabackup command.
pt_xtrabackup = "/usr/bin/innobackupex"

# Save the number of days.
saved_time = "3"

# Stream backup.
stream_dir = "/usr/local/dir_samba/db_%s_full_bak" % (db_serverid)
stream_host = "172.18.xxx"
stream_file = "fusCN_%s_full_%s.tar.gz" % (db_serverid, time.strftime("%%Y%m%d%H%M%S"))

# Log format.
logging.basicConfig(
    filename="/tmp/innobackupex_backup_%s.log" % (time.strftime("%Y%m%d")),
    format="%(asctime)s : %(levelname)s : %(message)s",
    datefmt="%Y-%m-%d %T",
    level=logging.INFO
)
logging.info("Start backup...")


class Backup(object):
    """ Define the backup and apply class. """

    def __init__(self, db_conf, user, host, passwd, port, socket, bak_dir):
        self.user = db_user
        self.host = db_host
        self.passwd = db_passwd
        self.port = db_port
        self.socket = db_socket
        self.defaults_file = conf

        # Local backupDir.
        self.target_dir = target_dir

        # Remote backupDir.
        self.stream_file = stream_file
        self.stream_dir = stream_dir

    def backup(self):
        """ Xtrabackup start full-backup. """
        command = "{0} --defaults-file={1} --user={2} --password='{3}' --host={4} --port={5} --socket={6} --no-timestamp {7}".format(
            pt_xtrabackup, self.defaults_file, self.user, self.passwd, self.host, self.port, self.socket,
            self.target_dir)

        status = runCommand(command)
        if status == 1:
            return 1
        return 0

    def applylog(self):
        """ Xtrabackup start full-prepared. """
        command = "%s --defaults-file=%s/backup-my.cnf --apply-log --user=%s --password='%s' --host=%s --port=%s --socket=%s %s" % (
            pt_xtrabackup, target_dir, self.user, self.passwd, self.host, self.port, self.socket, target_dir)
        status = runCommand(command)
        if status == 1:
            return 1
        return 0

    def remoteFullBak(self):
        """ Xtrabackup start stream backup. """
        command = "%s --defaults-file=%s --user=%s --password='%s' --host=%s --port=%s --socket=%s --no-timestamp --stream=tar /tmp | ssh -p22201 dev@jky_tomcat \ 'gzip > %s/%s'" % (
            pt_xtrabackup, self.defaults_file, self.user, self.passwd, self.host, self.port, self.socket, stream_dir,
            stream_file)
        status = runCommand(command)
        if status == 1:
            return 1
        return 0

    def removelog(self):
        """ Backup the number of days saved. """
        command = "find %s -name '%s*' -type d -mtime +%s -exec rm -fr {} \;" % (back, business, saved_time)
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
    if os.path.exists(back) and os.path.exists(monitor) == False:
        os.makedirs(back)
        os.makedirs(monitor)

    # Buried point, data check.
    conn = pymysql.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        passwd=db_passwd,
        db=db_name,
        unix_socket=db_socket)

    cur = conn.cursor()
    sql = ("insert into innobackup(db_user, db_passwd, server_id, ctime) values('%s', '%s', '%s', now())" % (
        db_user, db_passwd, db_serverid))
    try:
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        with open(monitor_file, "w+") as f:
            traceback.print_exc(file=f)
    finally:
        conn.close()

    try:
        # 1.Start local full backup.
        t = Backup("defaults_file", "db_user", "db_passwd", "db_host", "db_port", "db_socket", "target_dir")
        backup_status = t.backup()

        # 2.Start apply-log.
        logging.info('Start apply-log: ')
        apply_status = t.applylog()
        if apply_status == 0:
            db_size = os.popen("du -sh %s" % target_dir).read().split("\t")
            logging.info("Local backup up dbszie: %s" % db_size[0])

        # 3.Start removing more than saved_time of backup.
        removelog_success = t.removelog()
        if removelog_success == 0:
            logging.info('Local backup the number of days saved: %s' % saved_time)

        # 4.Start remote full backup.
        # logging.info('Start stream backup to %s(%s) ...' % (stream_host, stream_dir))
        # os.system("sh /root/lw/scripts/innobackupex_stream_backup.sh  >> /tmp/innobackupex_backup_%s.log 2>&1" % (
        #     time.strftime("%Y%m%d")))

        logging.info("End backup.")
        os.system("echo 'Yes' > %s" % monitor_file)
    except Exception as e:
        with open(monitor_file, 'w+') as f:
            traceback.print_exc(file=f)
