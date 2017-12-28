#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : xtrdb.net
# File   : 排序打印前10名.py
# Time   : 2017/12/20


# 打印字符出现的次数
content = 'Percona Monitoring Plugins are high-quality components to add enterprise-clas'

# 字符:次数
res = {}
for s in content:
    if s == " ":
        continue
    else:
        res[s] = res.get(s,0)+1  # 更简介，明了
print(res)

# 排序,前十名
# 冒泡
res_list = [(k[0],v) for k,v in res.items()]
for i in range(10):
    for j in range(len(res_list)-1):
        if res_list[j][1] > res_list[j+1][1]:
            res_list[j],res_list[j+1] = res_list[j+1],res_list[j]

for index,r in enumerate(res_list[-10:]):
    print("%s. char %s count is %s"%(index,r[0],r[1]))
