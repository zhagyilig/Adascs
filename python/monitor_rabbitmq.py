import sys, json, httplib, urllib, base64, socket

# https://juejin.im/post/5ad1d975f265da238e0e2cd4

# 1.定义状态码
EXIT_OK = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_UNKNOWN = 3

# 2.解析参数
server, port = sys.argv[1].split(":")
vhost = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]
queue_name = sys.argv[5]
auto_delete = json.loads(sys.argv[6].lower())
durable = json.loads(sys.argv[7].lower())

# 3.连接服务器
conn = httplib.HTTPConnection(server, port)

# 4.构建api路径
path = "/api/queues/%s/%s" % (urllib.quote(vhost, safe=""),
                              urllib.quote(queue_name))
method = "GET"

# 5.执行http请求
credentials = base64.b64encode("%s:%s" % (username, password))
try:
    conn.request(method, path, "",
                 {"Content-Type" : "application/json",
                  "Authorization" : "Basic " + credentials})

# 6.连接异常，退出
except socket.error:
    print "UNKNOWN: Could not connect to %s:%s" % (server, port)
    exit(EXIT_UNKNOWN)

response = conn.getresponse()

# 7.状态码为404，说明队列不存在，退出
if response.status == 404:
    print "CRITICAL: Queue %s does not exist." % queue_name
    exit(EXIT_CRITICAL)

# 8.durable属性是否正确
if response["durable"] != durable:
    print "WARN: Queue '%s' - durable flag is NOT %s." % \
          (queue_name, durable)
    exit(EXIT_WARNING)

# 9.返回正常
print "OK: Queue %s configured correctly." % queue_name
exit(EXIT_OK)

