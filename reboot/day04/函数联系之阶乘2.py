#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : xtrdb.net
# File   : 函数联系之阶乘2.py
# Time   : 2017/12/21


def fib(num):
    if num == 1:
        return 1
    return num*fib(num-1)
print(fib(5))