# coding=utf-8
# auth: zhangyiling
# time: 2019/1/14 下午4:54
# description: 列出账户下的所有的dns

"""
(ven363) ➜  cloudflare git:(master) ✗ cat ~/.cloudflare/cloudflare.cfg
[CloudFlare]
email = xxx@xx.xx
token = xxx
"""

import CloudFlare


def main():
    """打印改账号下所有的域名信息"""
    cf = CloudFlare.CloudFlare()
    zones = cf.zones.get()
    for zone in zones:
        zone_id = zone['id']
        zone_name = zone['name']
        print(zone_id, zone_name)


if __name__ == '__main__':
    main()
