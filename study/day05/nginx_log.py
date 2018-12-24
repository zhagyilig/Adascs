#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Author : xtrdb.net
# File   : log_html.py
# Time   : 2017/12/21

def nginx():
    with open("nginx.log") as f:
        res_dict = {}
        for line in f:
            if line == "\n":
                continue
            res = line.split()
            tup = (res[0],res[8])
            res_dict[tup] = res_dict.get(tup,0)+1
            res_list = list(res_dict.items())
    for j in range(10):
        for i in range(len(res_list)-1):
            if res_list[i][1] > res_list[i+1][1]:
                res_list[i],res_list[i+1] = res_list[i+1],res_list[1]
    html_str = '<table border="1">'
    tr_tmpl = """
            <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
            </tr>"""

    html_str += tr_tmpl%('IP','STATUS','COUNT')

    for (ip,status),count in res_list[-10:]:
        html_str+=tr_tmpl%(ip,status,count)
    html_str += '</table>'

    with open("res.html","w") as  html_f:
        html_f.write(html_str)
nginx()
