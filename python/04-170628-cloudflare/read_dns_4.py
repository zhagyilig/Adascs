# coding=utf-8
# auth: zhangyiling
# time: 2019/1/14 下午5:01
# description: 读取所有DNS记录

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
    """Cloudflare API code"""
    try:
        zone_name = sys.argv[1]
        zone_id = sys.argv[2]
    except IndexError:
        exit('usage: provide a zone name as an argument on the command line.')

    cf = CloudFlare.CloudFlare()

    # Now read back all the DNS records
    print('Read back DNS records ...')
    try:
        dns_records = cf.zones.dns_records.get(zone_id)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones.dns_records.get %s - %d %s' % (zone_name, e, e))

    for dns_record in sorted(dns_records, key=lambda v: v['name']):
        print('\t%s %30s %6d %-5s %s ; proxied=%s proxiable=%s' % (
            dns_record['id'],
            dns_record['name'],
            dns_record['ttl'],
            dns_record['type'],
            dns_record['content'],
            dns_record['proxied'],
            dns_record['proxiable']
        ))

if __name__ == '__main__':
    main()
