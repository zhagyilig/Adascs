#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : xtrdb.net
# File   : log_html.py
# Time   : 2017/12/21


# 过滤日志需要的信息:
with open("nginx.log") as f:
    res_dict = {}
    for line in f:
        if line == "\n":
            continue
        res = line.split()
        tup = (res[0],res[8])  # 元组可以当dict 的key，这是重要的特性，也是这个scripts的知识点
        res_dict[tup] = res_dict.get(tup,0)+1
        res_list = res_dict.items()

 # 冒泡排序:
for j in range(10):
    for i in range(len(res_list)-1):
        if res_list[i][1] > res_list[i+1][1]:
            res_list[i],res_list[i+1] = res_list[i+1],res_list[1]

# 打印前十名信息:
print(res_list[-10:])

# log html网页展示:
html_str = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>NGINX日志分析</title>
        </head>
    <body>
    <table border="1">"""
tr_tmpl = """
        <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
        </tr>"""

html_str += tr_tmpl%('IP','STATUS','COUNT')

for (ip,status),count in res_list[-10:]:
    html_str+=tr_tmpl%(ip,status,count)
html_str += """
            </table>
            </body>
            </html>"""

with open("res.html","w") as  html_f:
    html_f.write(html_str)  
    

