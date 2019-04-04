# coding:utf8
import pymysql
import requests
import json
import time
import datetime


def get_service_info(env, exc):
    UAT_INFO = {
        'UAT1': '192.168.199.32',
        'UAT2': '192.168.199.0',
        'UAT3': '192.168.199.28',
        'UAT4': '192.168.199.1',
        'UAT5': '192.168.199.2'
    }
    Service2URL = {}
    SQL = """
    select distinct name, ports, owner from asset_goservices where ports is not null and name not in (select name from {}) order by name;
    """
    cursor = ""
    try:
        connect = pymysql.Connection(
            host='192.168.199.69',
            user='monitor',
            password='monitor',
            database='cmdb')
        cursor = connect.cursor()
        cursor.execute(SQL.format(exc))
    except Exception as e:
        print(e)
    finally:
        connect.close()
    go_service_info = cursor.fetchall()
    for item in go_service_info:
        name, ports, owner = item
        port = ports.split(',')[0]
        url = 'http://{}:{}/ping'.format(UAT_INFO.get(env), port)
        if not Service2URL.get(env):
            Service2URL[env] = []
            Service2URL[env].append((url, name, owner))
        else:
            Service2URL[env].append((url, name, owner))
    return Service2URL


def check_url(url):
    try:
        req = requests.get(url, timeout=3)
        if req.status_code == 200:
            return 1
    except BaseException:
        return -1


def send_msg(info):
    url = 'http://wechat.65dg.me/robot/send?access_token=dad5d1b5465f645959ef107aa544b215&toall=1'
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


# 检查所有的URL, 发送微信通知、并记录bad_url
def check_all_urls():
    NOT_MONITOR = {
        'UAT1': 'uat1_not',
        'UAT2': 'uat2_not',
        'UAT3': 'uat3_not',
        'UAT4': 'uat4_not',
        'UAT5': 'uat5_not'
    }
    BAD_URLS = []
    while True:
        for e in NOT_MONITOR:
            go_services = get_service_info(e, NOT_MONITOR.get(e))
            services = go_services.get(e)
            if services:
                for item in services:
                    if check_url(item[0]) == -1:
                        info = """URL check Error !!!\nEnvironment: {}\nService name: {}\nOwner: {}\nChecked url: {}\nTime: {} """.format(
                            e, item[1], item[2], item[0], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        print(info)
                        # 环境、项目名、负责人、检查的URL
                        bad_url = (e, item[1], item[2], item[0])
                        if bad_url not in BAD_URLS:
                            BAD_URLS.append((e, item[1], item[2], item[0]))
        time.sleep(5)
        print(BAD_URLS)
        check_bad_urls(BAD_URLS)


def check_bad_urls(bad_urls):
    for item in bad_urls:
        env, name, owner, url = item
        try:
            req = requests.get(url, timeout=3)
            if name == 'titans':
                if req.status_code == 500:
                    info = """URL check OK !!\nEnvironment: {}\nService name: {}\nOwner: {}\nChecked url: {}\nTime: {} """.format(
                        env, name, owner, url, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    print(info)
                    bad_urls.remove(item)

            if req.status_code == 200:
                info = """URL check OK !!\nEnvironment: {}\nService name: {}\nOwner: {}\nChecked url: {}\nTime: {} """.format(
                    env, name, owner, url, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                print(info)
                bad_urls.remove(item)
        except Exception as e:
            pass


if __name__ == '__main__':
    check_all_urls()
