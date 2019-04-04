# coding=utf-8
# auth: zhangyiling
# time: 2019/1/16 下午7:39
# description:


import sys
import json
import requests
import os

# 认证相关配置文件
conf_info = '/Users/mac/.config/py_conf/conf'
headers = {'Content-Type': 'application/json-rpc'}

# 加载配置文件
try:
    with open(conf_info, 'r') as f:
        results = json.load(f)
        url = results['zabbix']['url']
        auth = results['zabbix']['auth']
        passwd = results['zabbix']['passwd']
        # print(url,auth)
except FileNotFoundError as e:
    print('No such file or directory: %s' % conf_info)

def apiinfo():
    """
    获取zabbix版本
    """
    data = {
        "jsonrpc": "2.0",
        "method": "apiinfo.version",
        "id": 1,
        "auth": None,
        "params": {},
    }

    r = requests.get(url, headers=headers, data=json.dumps(data))
    print(r.json())


def userlogin():
    """
    获取登陆token
    """
    data = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": "zhangyiling",
            "password": "%s" % passwd
        },
        "id": 1,
        "auth": auth
    }

    r = requests.post(url, headers=headers, data=json.dumps(data))
    print(r.json())  # {'jsonrpc': '2.0', 'result': 'xxx', 'id': 1}


def get_hosts_info():
    """
    获取主机信息
    """
    data = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": ["hostid", "host", ],
            "selectInterfaces": ["ip", ],
        },
        "auth": "%s" % auth,
        "id": 1
    }

    r = requests.post(url, headers=headers, data=json.dumps(data))
    print(json.dumps(r.json()))


def crate_host(host, ip):
    """
    创建主机
    """
    data = {
        "jsonrpc": "2.0",
        "method": "host.create",
        "params": {
            "host": host ,
            "interfaces": [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": ip,
                    "dns": "",
                    "port": "10050"
                }
            ],
            "groups": [
                {
                    "groupid": "32"
                }
            ],
            "templates": [
                {
                    "templateid": "10001",
                },
                {
                    "templateid": "10647"
                }
            ],
            # "macros": [
            #     {
            #         "macro": "{$USER_ID}",
            #         "value": "123321"
            #     }
            # ],
            # "inventory_mode": 0,
            # "inventory": {
            #     "macaddress_a": "01234",
            #     "macaddress_b": "56768"
            # }
        },
        "auth": "%s" % auth,
        "id": 1
    }
    r = requests.post(url, headers=headers, data=json.dumps(data))
    print(json.dumps(r.json()))


def get_host_group():
    """
    获取主机组
    """
    data = {
        "jsonrpc": "2.0",
        "method": "hostgroup.get",
        "params": {
            "output": "extend",
            "filter": {
                "name": [
                    "server of lsg",  # 32
                ]
            }
        },
        "auth": "%s" % auth,
        "id": 1
    }

    r = requests.post(url, headers=headers, data=json.dumps(data))
    print(json.dumps(r.json()))


def get_tmplate():
    """
    获取模版
    """
    data = {
        "jsonrpc": "2.0",
        "method": "template.get",
        "params": {
            "output": "extend",
            "filter": {
                "host": [
                    "Template OS Linux",  # 10001
                ]
            }
        },
        "auth": "%s" % auth,
        "id": 1
    }

    r = requests.post(url, headers=headers, data=json.dumps(data))
    print(json.dumps(r.json()))


def del_host():
    """
    删除主机
    """
    data = {
        "jsonrpc": "2.0",
        "method": "host.delete",
        "params": [
            "10562",
        ],
        "auth": "%s" % auth,
        "id": 1
    }

    r = requests.post(url, headers=headers, data=json.dumps(data))
    print(json.dumps(r.json()))

def host_link_tmp(hostid):
    """ 关联主机到模版 """
    data = {
    "jsonrpc": "2.0",
    "method": "template.massadd",
    "params": {
        "templates": [
            {
                "templateid": "10001",
            },
            {
                "templateid": "10647"
            }
        ],
        "hosts": [
            {
                "hostid": hostid
            },
        ]
    },
    "auth": "%s" % auth,
    "id": 1
}
    r = requests.post(url, headers=headers, data=json.dumps(data))
    print(json.dumps(r.json()))


if __name__ == '__main__':
    host = sys.argv[1]
    ip = sys.argv[2]
    # print(host, ip)

    crate_host(host,ip)

    # apiinfo()
    # userlogin()
    # get_hosts_info()
    # get_host_group()
    # get_tmplate()
    # crate_host(host,ipaddr)
    # del_host()
