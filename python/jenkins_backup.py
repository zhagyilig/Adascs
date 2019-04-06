#!/usr/bin/evn python
# conding=utf-8
# Filename: jenkins_backup.py

import time
import os
import logging

# Options.
source = '/var/lib/jenkins'
target_dir = '/mnt/uatjenkins'

# Log format.
logging.basicConfig(
    filename="/tmp/backup_jenkins_%s.log" % (time.strftime("%Y%m%d")),
    format="%(asctime)s : %(levelname)s : %(message)s",
    datefmt="%Y-%m-%d %T",
    level=logging.INFO
)
logging.info("Start backup jenkins ...")


def backup():
    '''
    Back up the jenkins function.
    '''
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        logging.warning('Create dir ' + target_dir + ' successfully')

    os.chdir(source)
    tar_cmd = "tar zcf %s/jenkins.%s.tar.gz ." % (target_dir,
                                                  time.strftime('%Y%m%d%H%M%S'),)
    if os.system(tar_cmd) == 0:
        logging.info('Running command: %s' % tar_cmd)
        logging.info('Jenkins successful backup to %s' % target_dir)
    else:
        logging.warning('Jenkisn backup failed.')


def listDir(fileDir):
    '''
    Save a month's backupi function.
    '''
    for n in os.listdir(fileDir):
        if os.path.isfile(fileDir + '/' + n):  # Determine whether it is a file.
            ft = os.stat(fileDir + '/' + n)
            ltime = int(ft.st_mtime)
            ntime = int(time.time()) - 3600*24*30   # 3 month
            if ltime <= ntime:
                print 'remove file: ' + fileDir + "/" + n
                os.remove(fileDir + '/' + n)
                logging.info('Remove file: ' + fileDir + '/' + n)

        elif os.path.isdir(fileDir + '/' + n):  # if not file.
            listDir(fileDir + '/' + n)


if __name__ == '__main__':
    backup()
    listDir(target_dir)
