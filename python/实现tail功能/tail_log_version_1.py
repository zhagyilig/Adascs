#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : xtrdb.net
# File   : tail_f脚本实现.py
# Time   : 2017/12/22

import sys
import time

class Tail(object):
    def __init__(self,file_name,callback=sys.stdout.write):
        self.file_name = file_name
        self.callback = callback
        
    def follow(self):
        try:
            with open(self.file_name) as f:
                f.seek(0,2)
                while True:
                    line = f.readline()
                    if line:
                        self.callback(line)
                    time.sleep(1)
        except Exception as e:
            print("open file is faild.")
            print(e)
py_tail = Tail(sys.argv[1])
py_tail.follow()
