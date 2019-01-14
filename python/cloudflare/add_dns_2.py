# coding=utf-8
# auth: zhangyiling
# time: 2019/1/14 下午5:53
# description: 添加域名

"""
(ven363) ➜  cloudflare git:(master) ✗ cat ~/.cloudflare/cloudflare.cfg
[CloudFlare]
email = xxx@xx.xx
token = xxx
"""

from __future__ import print_function

import os
import sys

sys.path.insert(0, os.path.abspath('..'))
import CloudFlare


def main():
    """添加域名"""
    try:
        zone_name = sys.argv[1]
        zone_id = sys.argv[2]
    except IndexError:
        exit('usage: provide a zone name as an argument on the command line.')

    cf = CloudFlare.CloudFlare()

    print('Create zone %s ...' % (zone_name))
    try:
        zone_info = cf.zones.post(data={'jump_start': False, 'name': zone_name})
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones.post %s - %d %s' % (zone_name, e, e))
    except Exception as e:
        exit('/zones.post %s - %s' % (zone_name, e))

    zone_id = zone_info['id']
    if 'email' in zone_info['owner']:
        zone_owner = zone_info['owner']['email']
    else:
        zone_owner = '"' + zone_info['owner']['name'] + '"'
    zone_plan = zone_info['plan']['name']
    zone_status = zone_info['status']
    print('\t%s name=%s owner=%s plan=%s status=%s\n' % (
        zone_id,
        zone_name,
        zone_owner,
        zone_plan,
        zone_status
    ))


if __name__ == '__main__':
    main()
