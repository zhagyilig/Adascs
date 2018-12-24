#!/usr/bin/env python3
# coding: utf-8
# Author : xtrdb.net
# File   : fileutil.py
# Time   : 2017/12/24


# user:pwd
file_dict = {}

# file => dict
def read_file():
    with open('user.txt','r',encoding='utf-8') as f:
        for line in f.read().split('\n'):
            if line:
                temp = line.split(':')  # 列表
                file_dict[temp[0]]  = temp[1]

# dict => file
def wirte_file():
    file_arr = []
    for user,pwd in list(file_dict.items()):
        file_arr.append('%s:%s' %(user,pwd))
    with open('user.txt','w',encoding='utf-8') as f:
        f.write('\n'.join(file_arr))
