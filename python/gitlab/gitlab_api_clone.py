# coding=utf-8

import subprocess
import json
import gitlab
import os
import time

# 加载配置文件,获取 gitlab api 认证
try:
    with open(conf_info, 'r') as f:
        results = json.load(f)
        url = results['gitlab']['url']
        token = results['gitlab']['token']
except FileNotFoundError as e:
    print('No such file or directory: %s' % conf_info)

gl = gitlab.Gitlab(url, token)

pro_url = []

def git_clone():
    for p in gl.projects.list(all=True, as_list=False):
        print("".center(20,"+"))
        
        try:
            pro_get = gl.projects.get(p.id)  # 有相同的项目名, 有500 error
        except Exception as e:
            print('****************************ERROR :{}{}'.format(p.name, p.id))
            time.sleep(1)
            continue

        git_url = pro_get.ssh_url_to_repo
        pro_url.append(git_url)

        if os.path.isdir(pro_get.name):
            print(pro_get.path_with_namespace, pro_get.ssh_url_to_repo)
            pass
        else:
            subprocess.call(['git', 'clone', git_url])

if __name__ == "__main__":
    git_clone()