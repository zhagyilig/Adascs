#!/usr/bin/env python3
# coding: utf-8
# Author : xtrdb.net
# File   : mem.py
# Time   : 2017/12/22


import psutil
import pprint

def mem_get():
    mem_info = {}
    date = psutil.virtual_memory()
    mem_info["total"] = date[0]/1024/1024/1024
    mem_info["available"] = date[1]/1024/1024/1024

    html_str= "<table border='1'><tr><td>status</td><td>data</td></tr>"
    for i,j in mem_info.items():
        html_str += "<tr><td>%s</td><td>%.2f</td></tr>" %(i,j)
    html_str +="</table>"
    return html_str

# with open("mem_info.html",'w') as f:
#     f.write(html_str)