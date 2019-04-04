# coding=utf-8
# auth: zhangyiling
# time: 2019-03-31 10:23
# description: zabbix, aws 认证key



import route53
import json
import os
import sys

# 认证相关配置文件
conf_info = '/Users/mac/.config/py_conf/conf'

# 加载配置文件
try:
    with open(conf_info, 'r') as f:
        results = json.load(f)
        aws_access_key_id = results['lsg_key']['id']
        aws_secret_access_key = results['lsg_key']['key']
except FileNotFoundError as e:
    print('No such file or directory: %s' % conf_info)