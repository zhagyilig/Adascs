# coding=utf-8
# auth: zhangyiling
# time: 2019/1/16 下午7:39
# description:


import sys
import json
import requests


# 认证相关配置文件
conf_info = '/Users/mac/.config/py_conf/conf'
headers = {'Content-Type': 'application/json-rpc'}

# 加载配置文件
try:
    with open(conf_info, 'r') as f:
        conf_json = json.load(f)
        url = conf_json['zabbix']['url']
        auth = conf_json['zabbix']['auth']
        passwd = conf_json['zabbix']['passwd']
        print(url,auth)
except FileNotFoundError as e:
    print('No such file or directory: %s' % conf_info)

def apiinfo():
    """获取zabbix版本"""
    data = {
        "jsonrpc": "2.0",
        "method": "apiinfo.version",
        "id": 1,
        "auth": None,
        "params": {},
    }

    r = requests.get(url, headers=headers, data=json.dumps(data))
    # print(r.status_code)  # 200
    # print(r.content)
    print(r.json())


def userlogin():
    """获取登陆token"""
    data = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": "zhangyiling",
            "password": "%s" % passwd
        },
        "id": 1,
        "auth": None
    }

    r = requests.post(url, headers=headers, data=json.dumps(data))
    print(r.json())  # {'jsonrpc': '2.0', 'result': 'xxx', 'id': 1}


def get_hosts_info():
    """获取主机信息"""
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


def crate_host():
    """创建主机"""
    data = {
        "jsonrpc": "2.0",
        "method": "host.create",
        "params": {
            "host": "lsg-ops-1",
            "interfaces": [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": "10.21.10.130",
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
    """删除主机"""
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


if __name__ == '__main__':
    # apiinfo()
    # userlogin()
    # get_hosts_info()
    # get_host_group()
    get_tmplate()
    # crate_host()
    # del_host()
