# coding:utf8
# auth: zhangyiling
# description: 通过CMDB(asset_goservices)表中服务信息和服务ping接口, 检查服务的健康状态, 发送通知

import os
import sys
import json
import time
import datetime
import pymysql
import requests


def get_service_info():
    """
    从CMDB获取服务相关信息: name, ip, port, owner
    """
    serviceApi = {}
    # 获取服务名, ip, 端口, 服务负责人
    SQL = """select a.name, a.ip, a.ports, b.saltname, a.owner from asset_goservices a \
             inner join asset_minion b where a.ip = b.ip and a.ports REGEXP '^[[:digit:]]+$' \
             and b.saltname like 'lsg-service-%' group by a.name;"""
    cursor = ""
    try:
        connect = pymysql.Connection(host='192.168.10.191',
                                     user='cmdb',
                                     password='65daigou@ezbuy',
                                     database='cmdb', )
        cursor = connect.cursor()
        cursor.execute(SQL)
    except Exception as e:
        print('查询数据库失败: {}'.format(e))
    finally:
        connect.close()

    go_service_info = cursor.fetchall()
    for item in go_service_info:
        # item: ('zhantang_service_proxy', '10.21.5.188', '14519',
        # 'lsg-service-5', 'owner')
        name, ip, ports, hostname, owner = item
        port = ports.split(',')[0]
        url = 'http://{}:{}/ping'.format(ip, port)
        if not serviceApi.get(name):
            serviceApi[name] = []
            serviceApi[name].append((url, hostname, owner))
        else:
            serviceApi[name].append((url, hostname, owner))
    # {'spike_service_feed': [('http://192.168.10.123:14203/ping', 'lsg-service-5', 'owner')],}
    return serviceApi


def check_url(url):
    """
    检查服务的ping接口
    """
    try:
        req = requests.get(url, timeout=30)
        if req.status_code == 200:
            return 1
    except BaseException:
        return -1


def send_msg(info):
    """
    发送微信通知
    """
    url = 'http://wechat.ezbuy.me/robot/send?access_token=dad5d1b5465f645959ef107aa544b215'
    header = {
        'Content-Type': 'application/json'
    }
    msg = {
        "msgtype": "text",
        "text": {
            "content": "{}".format(info)
        },
    }
    requests.post(url=url, data=json.dumps(msg), headers=header)


def check_all_urls():
    """
    检查所有服务的ping接口, 发送微信通知, 并记录bad_url
    """
    badUrls = {}
    services = get_service_info()
    for ser in services:
        # [('http://10.21.5.241:50517/ping', 'lsg-service-1', 'owner')]
        serInfo = services.get(ser)
        if serInfo:
            for item in serInfo:
                # item: ('http://10.21.5.241:50517/ping', 'lsg-service-1',
                # 'owner')
                print('检查服务信息: {}'.format(item))
                if check_url(item[0]) == -1:
                    info = """Service api check error\nEnv: {}\nService: {}\nOwner: {}\nApi: {}\nTime: {} """.format(
                        item[1], ser, item[2], item[0], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    send_msg(info)
                    print(info)
                    # time.sleep(1)
                    bad_url = ser
                    if bad_url not in badUrls:
                        badUrls[ser] = (item[1], item[2], item[0])

    time.sleep(180)
    check_bad_urls(badUrls)


def check_bad_urls(bad_urls):
    """
    检查访问失败的ping接口
    """
    for item in bad_urls:
        url = bad_urls.get(item)[2]  # http://10.21.5.229:14421/ping
        owner = bad_urls.get(item)[1]  # owner
        env = bad_urls.get(item)[0]  # lsg-service-3
        ser = item  # spkadmin_service_importjob

        try:
            req = requests.get(url, timeout=30)
            if ser == 'titans':
                if req.status_code == 500:
                    info = """Service api check success\nEnv: {}\nService: {}\nOwner: {}\nApi: {}\nTime: {} """.format(
                        env, ser, owner, url, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    send_msg(info)
                    bad_urls.pop(item, None)

            elif req.status_code == 200:
                info = """Service api check success\nEnv: {}\nService: {}\nOwner: {}\nApi: {}\nTime: {} """.format(
                    env, ser, owner, url, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                send_msg(info)
                bad_urls.pop(item, None)
        except Exception as e:
            print('检查访问失败的ping接口异常: {}'.format(e))


if __name__ == '__main__':
    check_all_urls()
