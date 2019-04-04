# /Users/mac/venv/ven363/bin/python
# coding: utf-8
# Usage: python gitlab_add_user_v4.py username

import sys
import json
import gitlab
import random
import string

DOMAIN = 'ezbuy.com'

# 加载配置文件,获取 gitlab api 认证
conf_info = '/Users/mac/.config/py_conf/conf'
try:
    with open(conf_info, 'r') as f:
        results = json.load(f)
        url = results['gitlab']['url']
        token = results['gitlab']['token']
except FileNotFoundError as e:
    print('No such file or directory: %s' % conf_info)

gl = gitlab.Gitlab(url, token)

def create_user(username):
    """
    创建用户
    """
    password = ''.join([random.choice(string.digits + string.ascii_letters) for i in range(16)])
    print(password)

    data = {
        'email': '{0}@{1}'.format(username, DOMAIN),
        'password': password,
        'username': username,
        'name': username,
    }

    user = gl.users.create(data)
    print('++++++ gitlab信息如下 ++++++')
    print('浏览器地址: git.ezbuy.me')
    print('用户名: %s' % username)
    print('密码: %s' % password)
    print('登陆前确认邮件,再登陆 :)')
    return user.id

def add_member(group, user_id):
    """
    添加用户到组
    """
    data = {
        'user_id': user_id,
        'access_level': 30,
    }

    groups = gl.groups.list()
    for n in groups:
        groupName = gl.groups.get(n.id)
        if groupName.name == group:
            member = groupName.members.create(data)

def main():
    username = sys.argv[1]
    groups = ['xxx', 'yyy', ]
    user_id = create_user(username)  # 创建用户
    [add_member(group, user_id) for group in groups]  # 将用户添加到组

if __name__ == '__main__': main()