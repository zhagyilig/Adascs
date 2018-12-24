#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : xtrdb.net
# File   : 函数练习之阶乘1.py
# Time   : 2017/12/21


def wife(num):
    fa = 1
    if num < 0:
        print("sorry ...")
    else:
        for n in range(1,num+1):
            fa *= n
        print('%d 的阶乘为: %d' %(num,fa))
wife(5)

print(range(1,5))



