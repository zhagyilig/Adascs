#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : xtrdb.net
# File   : 函数式编程.py
# Time   : 2017/12/21

def operator(name,fn):
    fn(name)

def sayhello(name):
    print("hello,%s" %name)

def sayhehe(name):
    print("hello,%s" %name)

operator("xtrdb",sayhello)
operator("xtrdb",sayhehe)
'''output:
hello,xtrdb
hello,xtrdb'''





