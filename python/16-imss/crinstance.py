# coding=utf-8
# auth: zhangyiling
# time: 2019-03-30 22:42
# description:
#   - 创建ec2实例
#   - 通过主机名添加相关的zabbix监控
#   - 添加域名解析


class Instance(object):
    """
    实例类
    """
    def __init__(self, hostname, ip):
        """ hostname: 主机名
            ip: 实例的ip地址
        """
        self.hostname = hostname
        self.ip = ip

    def createInstance(self):
        """ 创建ec2实例 """
        pass

    def addZbx(self):
        """ 添加监控 """
        pass

    def addRoute53(self):
        """ 添加主机域名解析 """
        pass


if __name__ == '__main__':
    pass
