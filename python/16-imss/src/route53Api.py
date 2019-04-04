# coding=utf-8
# auth: zhangyiling
# time: 2019/2/19 下午6:53
# description: aws route53 api

import route53
import json
import os
import sys

# 认证相关配置文件
conf_info = '/Users/mac/.config/py_conf/conf'

# 加载配置文件
try:
    with open(conf_info, 'r') as f:
        results = json.load(f)
        aws_access_key_id = results['lsg_key']['id']
        aws_secret_access_key = results['lsg_key']['key']
except FileNotFoundError as e:
    print('No such file or directory: %s' % conf_info)

conn = route53.connect(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)


def route53Info():
    """
    This is a generator.
    """
    for zone in conn.list_hosted_zones():
        # 打印域名
        print(zone.name)

        # 打印域名和记录
        for record_set in zone.record_sets:
            print(record_set)


def createRecord(name, value):
    """
    Creating a record set.
    """
    for zone in conn.list_hosted_zones():
        if zone.name == name_to_match:
            new_record, change_info = zone.create_a_record(
                # Notice that this is a full-qualified name.
                name='{}.{}'.format(name, name_to_match),
                values=['{}'.format(value)],
                # weight=2
                # set_identifier='set123,
            )


"""
Listing record sets
"""
# # Note that this is a fully-qualified domain name.
# for zone in conn.list_hosted_zones():
#     name_to_match = 'ezbuy.me.'
#     for record_set in zone.record_sets:
#         if record_set.name == name_to_match:
#             print(record_set)
#             # Stopping early may save some additional HTTP requests,
#             # since zone.record_sets is a generator.
#             break


"""
Changing a record set
Simply change one of the attributes on the various ResourceRecordSet sub-classed instances and call its save() method:
"""
# record_set.values = ['8.8.8.7']
# record_set.save()

"""
Deleting a record set
Similarly, delete a record set via its delete() method:
"""
# record_set.delete()


if __name__ == "__main__":
    name_to_match = 'ezbuy.me.'
    name = sys.argv[1]
    value = sys.argv[2]
    createRecord(name, value)