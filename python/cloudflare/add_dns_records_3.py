# coding=utf-8
# auth: zhangyiling
# time: 2019/1/14 下午5:01
# description: 增加解析记录

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

    # DNS records to create
    dns_records = [
        {'name': 'xx-test-xxxx', 'type': 'A', 'content': '192.168.xx.75'},
    ]



    print('Create DNS records ...')
    for dns_record in dns_records:
        # Create DNS record
        try:
            r = cf.zones.dns_records.post(zone_id, data=dns_record)
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            exit('/zones.dns_records.post %s %s - %d %s' % (zone_name, dns_record['name'], e, e))

        # Print respose info - they should be the same
        dns_record = r
        print('\t%s %30s %6d %-5s %s ; proxied=%s proxiable=%s' % (
            dns_record['id'],
            dns_record['name'],
            dns_record['ttl'],
            dns_record['type'],
            dns_record['content'],
            dns_record['proxied'],
            dns_record['proxiable']
        ))

        # set proxied flag to false - for example
        dns_record_id = dns_record['id']

        new_dns_record = {
            # Must have type/name/content (even if they don't change)
            'type': dns_record['type'],
            'name': dns_record['name'],
            'content': dns_record['content'],
            # now add new values you want to change
            'proxied': False
        }

        try:
            dns_record = cf.zones.dns_records.put(zone_id, dns_record_id, data=new_dns_record)
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            exit('/zones/dns_records.put %d %s - api call failed' % (e, e))

    print('域名解析添加成功 :)')


if __name__ == '__main__':
    main()
