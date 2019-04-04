# coding=utf-8
# auth: zhangyiling
# time: 2019/3/14 下午11:36
# description:

import sys
import time
import socket
import xmlrpclib
import consul

host = '127.0.0.1'
node = socket.gethostname()  # consul节点
try:
    service = sys.argv[1]  # 服务名
    dc = sys.argv[2]  # consul dc
except Exception as e:
    # 如果位置参数为空, 就使用默认参数
    # service = 'zuul'
    # dc = 'uat'
    print('Usage: {} service dc'.format(sys.argv[0]))
    exit(1)

# 实例化
c = consul.Consul(host=host, dc=dc)

def derService(service, host, node, serverId):
    """
    指定服务从consul中注销
    """
    try:
        c.catalog.deregister(node, serverId)
        print('服务注销成功,重启服务...')
        time.sleep(8)
        # 重启服务
        reService(service, host)
    except Exception as e:
        print('服务注销失败:{}'.format(e))


def reService(service, host):
    """
    重启服务
    """
    # 连接supervisor
    try:
        server = xmlrpclib.Server('http://admin:ezbuyisthebest@{}:29001/RPC2'.format(host))
    except Exception as e:
        print("连接supervisor失败:{}".format(e))
    # 重启服务
    try:
        server.supervisor.stopProcess(service)
        server.supervisor.startProcess(service)
        print('服务[{}]重启成功'.format(service))
    except Exception as e:
        print('服务[{}]重启失败:{}'.format(service,e))

if __name__ == "__main__":
    try:
        # SercerID
        serverId = c.catalog.service(service)[1][0]['ServiceID']
    except IndexError as e:
        print('该服务[{}]没有注册到consul: {}'.format(service, e))
        print('重启服务...'.format(service))
        # 重启服务
        sys.exit(reService(service, host))
    print(service, host, node, serverId, dc)
    derService(service, host, node, serverId)