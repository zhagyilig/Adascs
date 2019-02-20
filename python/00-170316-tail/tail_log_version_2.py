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

    def follow(self, n=10):
        try:
            with open(self.file_name) as f:
                self._file = f
                self.showLastLine(n)
                self._file.seek(0,2)
                while True:
                    line = self._file.readline()
                    if line:
                        self.callback(line)
                    time.sleep(1)
        except Exception as e:
            print("open file is faild.")
            print(e)

    def showLastLine(self, n):
        last_lines = self._file.readline()[-n]
        for line in last_lines:
            self.callback(line)

py_tail = Tail(sys.argv[1])
py_tail.follow()
