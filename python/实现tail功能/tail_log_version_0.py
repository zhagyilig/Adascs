#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : xtrdb.net
# File   : tail_f脚本实现.py
# Time   : 2017/12/22


with open("access.log") as f:
    f.seek(0,2)
    while True:
        last_post = f.tell()
        line = f.readline()
        if line:
            print line
