# coding=utf-8
# auth: zhangyiling
# time: 2019/2/19 下午6:53
# description: aws route53入门

import route53
import json

name_to_match = 'ezbuy.me.'

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

"""
This is a generator.
"""
# for zone in conn.list_hosted_zones():
#     # 打印域名
#     print(zone.name)

#     # 打印域名和记录
#     for record_set in zone.record_sets:
#         print(record_set)


"""
Creating a record set
"""
for zone in conn.list_hosted_zones():
    print(zone)
    # print(dir(zone))
    """
    ['caller_reference', 'comment', 'connection', 'create_a_record', 'create_aaaa_record', 
    'create_cname_record', 'create_mx_record', 'create_ns_record', 'create_ptr_record', 
    'create_spf_record', 'create_srv_record', 'create_txt_record', 'delete', 'id', 'name', 
    'nameservers', 'record_sets', 'resource_record_set_count']
    """
    # print(help(zone))
    
    if zone.name == name_to_match:
        print(zone.nae)
        new_record, change_info = zone.create_a_record(
            # Notice that this is a full-qualified name.
            name='lsg-redis-db-1.ezbuy.me.',
            values=['10.21.7.235'],
        )
        print(new_record, change_info)

# Or maybe we want a weighted round-robin set.
# wrr_record1, change_info = zone.create_a_record(
#     name='wrrtest.some-domain.com.',
#     values=['8.8.8.8'],
#     weight=1
#     set_identifier='set123,
# )
# wrr_record2, change_info = zone.create_a_record(
#     name='wrrtest.some-domain.com.',
#     values=['6.6.6.6'],
#     weight=2
#     set_identifier='set123,
# )


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
