# coding=utf-8
# time: 2018/12/20 下午11:39


import os
import json
import dns.resolver
import xlwt
import socket
from nginx import NGINX

confPath = "/etc/nginx/sites-enabled"
hostname = socket.gethostname()

domainName = []  # 域名,nginx => server_name
recordA = {}  # 解析dns A记录
resolverSucc = []  # 解析成功域名
resolverFail = []  # 解析失败域名

try:
   os.remove("/home/zhangyiling/resolverSucc.txt")
   os.remove("/home/zhangyiling/resolverFaild.txt")
except OSError:
   pass


# 从nginx配置文件中取出域名,并区分可用域名,保存在相应的文件中
for root, dirs, files in os.walk(confPath):  # 取出nginx配置文件
    for conf in files:  # conf => nginx配置文件
        nginx = NGINX(conf)  # 解析配置文件
        for urls in nginx.servers:  # 配置文件中server_name下所有的域名
            for url in urls["server_name"].split(" "):  # 解决server_name多个域名不能循环问题
                try:
                    record_a = dns.resolver.query(url, "A")  # 解析url A 记录 
                    resolverSucc.append(url)  # 将能解析的域名添加到resolverSucc
                    with open("/home/zhangyiling/resolverSucc.txt", "w") as f:
                      json.dump(resolverSucc, f)
                except Exception, e:
                   print("\033[1;31mCan't resolve domain name:\033[0m %s" % url)
                   resolverFail.append(url)  # 将不能解析的域名添加到resolverFail
                   with open("/home/zhangyiling/resolverFaild.txt", "w") as f:
                       json.dump(resolverFail, f)
print('====== 可用域名区分完成 ======\n')
print('====== 开始填充数据到execl ======\n')

# 将所有配置文件信息保存在excel中
def makeExcel():
    header = ["include", "port", "serverName", "backendIp", "backendPath"]
    workbook = xlwt.Workbook(encoding="utf-8")  # 创建一个Workbook对象
    xlwt.add_palette_colour("custom_colour", 0x21)
    workbook.set_colour_RGB(0x21, 251, 228, 228)
    worksheet = workbook.add_sheet(hostname)
    style = xlwt.easyxf("pattern: pattern solid, fore_colour custom_colour")
    i = 0
    row = 1

    # 设置表头
    for eachHeader in header:
        try: 
            worksheet.write(0, i, eachHeader)
            i += 1
        except Exception, e:
            pass

    # 填充每行数据
    for root, dirs, files in os.walk(confPath):
        for conf in files:
            nginx = NGINX(conf)
            for eachRow in nginx.servers:
                include = eachRow['include'] # 包含文件
                port = eachRow['port'] # 服务端口
                serverName = eachRow['server_name'] # server_name下的域名
                # 写到表格中
                worksheet.write(row, 0, include)
                worksheet.write(row, 1, port)
                # 将解析失败的域名标红底
                if serverName in resolverFail:
                    worksheet.write(row, 2, serverName, style)
                else:
                    worksheet.write(row, 2, serverName)
                # 循环处理后端ip和路由
                for n in eachRow['backend']:
                    backend_ip = n['backend_ip']
                    backend_path = n['backend_path']
                    worksheet.write(row, 3, backend_ip)
                    worksheet.write(row, 4, backend_path)
                    row += 1
                print("添加域名: %s" % serverName)
                row += 1
            # 保存excel文件
            workbook.save('/home/zhangyiling/%s.xls' % hostname)

if __name__ == '__main__':
    makeExcel()
    print('====== 脚本执行结束 ======\n')
