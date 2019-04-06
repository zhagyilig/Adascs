#!/usr/bin/python3
# coding:utf8
# auth: zhangyiling
# description: 通过CMDB(asset_goservices)表中服务信息和服务ping接口, 检查服务的健康状态, 发送通知

import os
import sys
import json
import time
import pymysql
import requests
import logging
from datetime import datetime
from requests import exceptions


logging.basicConfig(
    filename='/tmp/service_api_check_alter.log',
    format="%(asctime)s:%(levelname)s:%(message)s",
    datefmt="%Y-%m-%d %T",
    level=logging.INFO,
)

logging.info('{} start executing the script....'.format(
    datetime.now().strftime('%m/%d/%Y %H:%M:%S %p')))


def get_service_info():
    """ 从CMDB获取服务相关信息: name, ip, port, owner """
    serviceApi = {}
    # 获取服务名, ip, 端口, 服务负责人
    SQL = """select a.name, a.ip, a.ports, b.saltname, a.owner from asset_goservices a \
             inner join asset_minion b where a.ip = b.ip and a.ports REGEXP '^[[:digit:]]+$' \
             and b.saltname like '%sg-service-%';"""
    cursor = ""
    try:
        connect = pymysql.Connection(host='lsg-zabbix-1',
                                     user='cmdb',
                                     password='xUqX9JbNezAcDvU3',
                                     database='cmdb', )
        cursor = connect.cursor()
        cursor.execute(SQL)
    except Exception as e:
        send_msg('服务健康检查连接数据库失败:{}\nTime: {}\n@张艺龄 @汤龙'.format(
            e, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        logging.info('查询数据库失败: {}'.format(e))
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
    """ 检查服务的ping接口 """
    try:
        req = requests.get(url, timeout=12)
        if req.status_code in [200, 403, 500]:
            return 1
        elif req.status_code in [404]:
            return 2
    except exceptions.ConnectionError as e:
        print('拒绝连接:{}, url:{}'.format(e, url))
        logging.info('拒绝连接:{}, url:{}'.format(e, url))
        return 3
    except exceptions.Timeout as e:
        print('连接超时:{}, url:{}'.format(e, url))
        logging.info('连接超时:{}, url:{}'.format(e, url))
        return 4
    except BaseException as e:
        logging.info('未知异常:{}, url:{}'.format(e, url))
        send_msg('Service api check PROBLEM[未知异常]{}\nTime: {}\n@张艺龄 @汤龙'.format(
            e, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


def send_msg(info):
    """ 发送微信通知 """
    # url = 'http://wechat.ezbuy.me/robot/send?access_token=db08e4311793c7918a139abf7ac891bf'
    url = 'http://wechat.ezbuy.me/robot/send?access_token=xx'
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
    """ 检查所有服务的ping接口, 发送微信通知, 并记录bad_url """
    badUrls = {}
    services = get_service_info()
    for ser in services:
        # [('http://10.21.5.241:50517/ping', 'lsg-service-1', 'owner')]
        serInfo = services.get(ser)
        if serInfo:
            for item in serInfo:
                # item: ('http://10.21.5.241:50517/ping', 'lsg-service-1',
                # 'owner')
                print('检查服务信息: {} => {}'.format(ser, item))
                logging.info('检查的服务: {}'.format(ser))
                if check_url(item[0]) == 2:
                    info = """Service api check Error[状态码: 404]\nEnv: {}\nService: {}\nOwner: @{}\nApi: {}\nTime: {} """.format(
                        item[1], ser, item[2], item[0], datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    send_msg(info)
                    print(info)
                    bad_url = ser
                    if bad_url not in badUrls:
                        badUrls[ser] = (item[1], item[2], item[0])
                    logging.info(
                        'Service api check Error[httpcode:404]: {}'.format(ser))
                elif check_url(item[0]) == 3:
                    info = """Service api check PROBLEM[连接拒绝]\nEnv: {}\nService: {}\nOwner: @{}\nApi: {}\nTime: {} """.format(
                        item[1], ser, item[2], item[0], datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    send_msg(info)
                    print(info)
                    bad_url = ser
                    if bad_url not in badUrls:
                        badUrls[ser] = (item[1], item[2], item[0])
                elif check_url(item[0]) == 4:
                    info = """Service api check PROBLEM[连接超时]\nEnv: {}\nService: {}\nOwner: @{}\nApi: {}\nTime: {} """.format(
                        item[1], ser, item[2], item[0], datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    send_msg(info)
                    print(info)
                    logging.info(
                        'Service api check PROBLEM[httpcode:404]: {}'.format(ser))
                    bad_url = ser
                    if bad_url not in badUrls:
                        badUrls[ser] = (item[1], item[2], item[0])
                time.sleep(0.1)
    time.sleep(60)
    check_bad_urls(badUrls)


def check_bad_urls(bad_urls):
    """ 检查访问失败的ping接口 """
    for item in bad_urls:
        url = bad_urls.get(item)[2]  # http://10.21.5.229:14421/ping
        owner = bad_urls.get(item)[1]  # owner
        env = bad_urls.get(item)[0]  # lsg-service-3
        ser = item  # spkadmin_service_importjob

        if check_url(url) == 1:
            info = """Service api check OK\nEnv: {}\nService: {}\nOwner: @{}\nApi: {}\nTime: {} """.format(
                env, ser, owner, url, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            send_msg(info)
            bad_urls.pop(item, None)
            time.sleep(2)


if __name__ == '__main__':
    check_all_urls()
