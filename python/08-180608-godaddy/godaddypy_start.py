# coding=utf-8
# auth: zhangyiling
# time: 2019/1/28 下午6:06
# description:

"""
url: https://pypi.org/project/GoDaddyPy/
install: pip install GoDaddyPy
"""

import json
from godaddypy import Client, Account

conf_info = '/Users/mac/.config/py_conf/conf'

# 从配置文件中获取认证信息
try:
    with open(conf_info, 'r',encoding='utf-8') as f:
        results = json.load(f)
        api_key = results['godaddypy']['api_key']
        api_secret = results['godaddypy']['api_secret']
        print(api_key, api_secret)
except FileNotFoundError as e:
    print('No such file or directory: %s' % conf_info)
 
my_acct = Account(api_key, api_secret)
client = Client(my_acct)

domains = client.get_domains()  # 获取所有的域名
print(domains)


records = client.get_records('alsdelivery.com') # 获取域名所有的解析
print(records)


""" https://pypi.org/project/GoDaddyPy/
>>> from godaddypy import Client, Account
>>>
>>> my_acct = Account(api_key='PUBLIC_KEY', api_secret='SECRET_KEY')
>>> delegate_acct = Account(api_key='PUBLIC_KEY', api_secret='SECRET_KEY', delegate='DELEGATE_ID')
>>> client = Client(my_acct)
>>> delegate_client = Client(delegate_acct)
>>>
>>> client.get_domains()
['domain1.example', 'domain2.example']
>>>
>>> client.get_records('domain1.example', record_type='A')
[{'name': 'dynamic', 'ttl': 3600, 'data': '1.1.1.1', 'type': 'A'}]
>>>
>>> client.update_ip('2.2.2.2', domains=['domain1.example'])
True
>>>
>>> client.get_records('domain1.example')
[{'name': 'dynamic', 'ttl': 3600, 'data': '2.2.2.2', 'type': 'A'}, {'name': 'dynamic', 'ttl': 3600, 'data': '::1',
'type': 'AAAA'},]
>>>
>>> client.get_records('apple.com', record_type='A', name='@')
[{u'data': u'1.2.3.4', u'type': u'A', u'name': u'@', u'ttl': 3600}]
>>>
>>> client.update_record_ip('3.3.3.3', 'domain1.example', 'dynamic', 'A')
True
>>>
>>> client.add_record('apple.com', {'data':'1.2.3.4','name':'test','ttl':3600, 'type':'A'})
True
>>>
>>> client.delete_records('apple.com', name='test')
True
"""

