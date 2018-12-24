#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : xtrdb.net
# File   : 函数排序.py
# Time   : 2017/12/21


def my_sort(tlist):
    if not isinstance(tlist,list):
        print("master need list.")
        exit()

    for i in range(len(tlist)):
        for n in range(len(tlist)-1):
            if tlist[n] > tlist[n+1]:
                tlist[n],tlist[n+1] = tlist[n+1],tlist[n]
    print(tlist)

my_sort([6,5,4,5,2,1,3,0,77,88,545,5])
my_sort('h')


