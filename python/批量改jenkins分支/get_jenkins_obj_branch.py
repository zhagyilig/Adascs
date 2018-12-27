# -*- coding: utf-8 -*-

import os
import sys
import json
import requests
from git.cmd import Git
from jenkinsapi.jenkins import Jenkins

IGNORES = ['goflow', 'base', 'lib', 'vendor', 'notify', 'notify2', 'notify3', 'gospider', 'test', 'mqClient']


class JK(object):
    def __init__(self, env, base_url, username, password):
        self.c = Jenkins('%s/job/%s' % (base_url, env), username=username, password=password)
        self.env = env

    def test(self, job_name):
        """构建job"""
        try:
            self.c.build_job(job_name)
        except Exception as e:
            print str(e)

    def _work(self, job_name):
        try:
            job = self.c.get_job(job_name)
            branch = job.get_scm_branch() # 获取job分支
            assert len(branch) == 1, '改job有很多的构建分支'
            print("job分支: ",branch[0])
            branch = branch[0].strip('*/')
            print("job分支: ",branch)

            if branch != 'master':
                print "==>branch不是master分支的job: %s <==" % job_name
                workspace = '/srv/%s/goflow/src/gitlab.1dmy.com/ezbuy/%s' % (self.env, job_name)
                rebase(workspace, branch)
                try:
                    print('构建job: ',job_name)
                    self.c.build_job(job_name)
                except Exception as e:
                    print str(e)
        except Exception as e:
            print("获取分支job等失败")
            print str(e)
            send_msg(job_name, branch, str(e))

    def work(self):
        [self.test(job_name) for job_name in self.c.keys() if not job_name.startswith('http:/') and job_name not in IGNORES]

    def job_lists(self):
        """获取job列表"""
        job_list = self.c.keys()[::2] # 取job名
        job = ''
        bra = ''  # 分支
        try:
            count = 1
            for n in job_list:
               job = self.c.get_job(n)
               #print self.c.get_job(n)
               bra = job.get_scm_branch()[0].strip("*/")
               #print job.get_scm_branch()[0]
               if bra != "master":
                   print count,job,bra
                   count += 1
        except Exception as e:
              print job,bra

def rebase(workspace, branch):
    """git操作"""
    g = Git(workspace)
    tmp_branch = 'tmp/xxx-by-jenkins'
    g.checkout('-B', tmp_branch, '--track', 'origin/'+branch)
    g.pull()
    try:
        g.merge('origin/master', '-m', 'Auto merged by Jenkins Script')
    except Exception as e:
        g.merge('--abort')
        raise e
    g.submodule('update')
    g.push('origin', tmp_branch+':'+branch)


def main():
    env = sys.argv[1]
    base_url = 'http://192.168.199.120:8080'
    username = 'admin'
    password = 'admin@ezbuy'
    jk = JK(env=env, base_url=base_url, username=username, password=password)
    #jk.work()
    jk.job_lists()


if __name__ == '__main__':
    main()
