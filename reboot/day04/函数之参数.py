#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : xtrdb.net
# File   : 函数之参数.py
# Time   : 2017/12/21

# *args
# def sum(*args):
#     fa = 1
#     for n in args:
#         fa *= n
#     print(fa)
# sum(1,2,3,4,10,)

# **kwargs
# def hello(*args,**kwargs):
#     print(args,kwargs)
# hello(1,2,4,a=1,b=3)

res = [['192.1','200'],['192.2','400'],['192.2','500']]

def hello(ip,status):
    print("%s:%s" %(ip,status))

for r in res:
    hello(*r)

res_dict = [{'ip':'192','status':"300"},{'ip':'196','status':"500"}]
# **在调用的时候，可以把dict展开，当成关键字参数
for r in res_dict:
    hello(**r)


