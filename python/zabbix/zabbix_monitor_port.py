# coding: utf-8

import os
import json

portlist = []
new_port_list = []
port_dict = {"data":None}

# get local ports
cmd = '''netstat -tnlp|egrep -i "$1"|awk {'print $4'}|'''
cmd += '''awk -F':' '{if ($NF~/^[0-9]*$/) print $NF}'|sort -n| uniq 2>/dev/null'''
auto_localport = os.popen(cmd).readlines()

# manually specify ports
portlist = ['5601', '5778', '9200', '14268', '16686',]

"""
for ports in auto_localport:
    new_port = ports.strip()
    portlist.append(new_port)
"""

for port in portlist:
    pdict = {}
    pdict["{#TCP_PORT}"] = port
    new_port_list.append(pdict)
    port_dict["data"] = new_port_list
    jsonStr = json.dumps(port_dict,sort_keys=True,indent=4)

print(jsonStr)

"""
1. zabbix_agent:
[root@slq-xxxxxx-1 /etc/zabbix/scripts]# tail -n 1 ../zabbix_agentd.conf
UserParameter=tcpPortListen,python /etc/zabbix/scripts/zabbix_monitor_port.py
[root@slq-xxxxxx-1 /etc/zabbix/scripts]# pwd
/etc/zabbix/scripts
[root@slq-jaeger-1 /etc/zabbix/scripts]# ls
zabbix_monitor_port.py

2. zabbix_service:
[root@slq-xxxxxx-1 ~]# zabbix_get -s 192.168.199.70 -k 'tcpPortListen'
{
    "data": [
        {
            "{#TCP_PORT}": "5601"
        },
        {
            "{#TCP_PORT}": "5778"
        },
        {
            "{#TCP_PORT}": "9200"
        },
        {
            "{#TCP_PORT}": "14268"
        },
        {
            "{#TCP_PORT}": "16686"
        }
    ]
}

3. zabbix lld
"""
