# coding=utf-8
# auth: zhangyiling
# time: 2018/9/14 下午00:05
# description: 这是python3，使用request模块; saltstack api所有的操作在这里

import requests
import copy
import json

# 认证相关配置文件
conf_info = '/Users/mac/.config/py_conf/conf'

# 加载配置文件
try:
    with open(conf_info, 'r') as f:
        results = json.load(f)
        url = results['saltApi']['url']
        user = results['saltApi']['user']
        password = results['saltApi']['password']
except FileNotFoundError as e:
    print('No such file or directory: %s' % conf_info)

SALT_API = {'url': url, 'user': user, 'password': password}

class SaltApi(object):
    """
    saltstack api.
    """

    def __init__(self):
        self.__user = SALT_API["user"]
        self.__passwd = SALT_API["password"]
        self.url = SALT_API["url"]
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.__base_data = dict(
            username=self.__user,
            password=self.__passwd,
            eauth='pam'
        )
        self.__token = self.get_token()

    def get_token(self):
        """
        login salt-api and get token_id 
        """
        params = copy.deepcopy(self.__base_data)
        requests.packages.urllib3.disable_warnings()  # close ssl warning, py3 really can do it!
        ret = requests.post(url=self.url + '/login', verify=False, headers=self.headers, json=params)
        ret_json = ret.json()
        token = ret_json["return"][0]["token"]
        return token

    def __post(self, **kwargs):
        """
        custom post interface, headers contains X-Auth-Token 
        """
        headers_token = {'X-Auth-Token': self.__token}
        headers_token.update(self.headers)
        requests.packages.urllib3.disable_warnings()
        ret = requests.post(url=self.url, verify=False, headers=headers_token, **kwargs)
        ret_code, ret_data = ret.status_code, ret.json()
        return (ret_code, ret_data)

    def list_all_keys(self):
        """ 
        show all keys, minions have been certified, minion_pre not certification
        """
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        r = self.__post(json=params)
        minions = r[1]['return'][0]['data']['return']['minions']
        minions_pre = r[1]['return'][0]['data']['return']['minions_pre']
        return minions, minions_pre

    def delete_key(self, tgt):
        """ 
        delete a key
        """
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': tgt}
        r = self.__post(json=params)
        return r[1]['return'][0]['data']['success']

    def accept_key(self, tgt):
        """  
        accept a key 
        """
        params = {'client': 'wheel', 'fun': 'key.accept', 'match': tgt}
        r = self.__post(json=params)
        return r[1]['return'][0]['data']['success']

    def lookup_jid_ret(self, jid):
        """  
        depend on jobid to find result 
        """
        params = {'client': 'runner', 'fun': 'jobs.lookup_jid', 'jid': jid}
        r = self.__post(json=params)
        return r[1]['return'][0]

    def salt_running_jobs(self):
        """ 
        show all running jobs 
        """
        params = {'client': 'runner', 'fun': 'jobs.active'}
        r = self.__post(json=params)
        return r[1]['return'][0]

    def run(self, params):
        """ 
        remote common interface, you need custom data dict
        for example:
        params = {
                'client': 'local',
                'fun': 'grains.item',
                'tgt': '*',
                'arg': ('os', 'id', 'host' ),
                'kwargs': {},
                'expr_form': 'glob',
                'timeout': 60
            }
        """
        r = self.__post(json=params)
        return r[1]['return'][0]

    def remote_execution(self, tgt, fun, arg, ex='glob'):
        """ 
        remote execution, command will wait result
        arg must be a tuple, eg: arg = (a, b)
        expr_form : tgt m
        """
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': ex}
        r = self.__post(json=params)
        return r[1]['return'][0]

    def async_remote_execution(self, tgt, fun, arg, ex='glob'):
        """ 
        async remote exection, it will return a jobid
        tgt model is list, but not python list, just like 'node1, node2, node3' as a string.
         """
        params = {'client': 'local_async', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': ex}
        r = self.__post(json=params)
        return r[1]['return'][0]['jid']

    def salt_state(self, tgt, arg, ex='list'):
        """  
        salt state.sls 
        """
        params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': ex}
        r = self.__post(json=params)
        return r[1]['return'][0]

    def salt_alive(self, tgt, ex='glob'):
        """ 
        salt test.ping 
        """
        params = {'client': 'local', 'tgt': tgt, 'fun': 'test.ping', 'expr_form': ex}
        r = self.__post(json=params)
        return r[1]['return'][0]


    def target_deploy(self,tgt,arg):
        """
        Based on the node group forms deployment
        """
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': 'nodegroup'}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid



if __name__ == '__main__':
    """
    os_info = {
        'client': 'local',
        'fun': 'grains.item',
        'tgt': '*',
        'arg': ('os', 'fqdn', 'host','ipv4','osfinger','mem_total','num_cpus','osrelease'),
        'kwargs': {},
        'expr_form': 'glob',
        'timeout': 60
    }
    """
    obj = SaltApi()
    #ret = obj.list_all_keys()
    ret = obj.accept_key('windows-test')
    # ret = obj.delete_key('windows-test')
    # ret = obj.lookup_jid_ret('20180612111505161780')
    # ret = obj.salt_running_jobs()
    # ret = obj.remote_execution('*', 'grains.item',('ip4_interfaces'))['study-zyl-node5']['ip4_interfaces']['eth0']
    # ret = obj.remote_execution('*', 'cmd.run','sudo supervisorctl status')
    # ret = obj.async_remote_execution('*', 'grains.item', ('os', 'id'))
    # ret =  obj.salt_state("*",'')
    # ret = obj.salt_alive('*', 'glob')
    # ret = obj.run(os_info)
    # ret = obj.get_token()
    # print(json.dumps(ret))
    print(ret)