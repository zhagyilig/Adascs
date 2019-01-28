#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# Author  : xtrdb.net

from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.console import confirm


env.user='admin'
env.hosts=['139.19.8.59']
 
@task
@runs_once
def tar_task():
    with lcd("/data/redis"):
        local("tar -czf redis57777.tar.gz redis57777")

@task
def put_task():
    run("mkdir -p /tmp/fabric")
    with cd("/tmp/fabric"):
        with settings(warn_only=True):
            result = put("/data/redis/redis57777.tar.gz","/tmp/fabric/redis57777.tar.gz")
        if result.failed and not confirm("put file failed, Continue[y/n]?:"):
            abort("Aborting file put task!")

@task
def check_task():
    with settings(warn_only=True):
        lmd5 = local("md5sum /data/redis/redis57777.tar.gz",capture=True).split(' ')[0]
        rmd5 = run("md5sum /tmp/fabric/redis57777.tar.gz").split(' ')[0]
        if lmd5 == rmd5:
            print("ok.")
        else:
            print("error.")
@task
def go():
    tar_task()
    put_task()
    check_task()
