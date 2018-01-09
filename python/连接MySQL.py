#coding=utf-8

import MySQLdb
import time
import random
import string


conn = MySQLdb.connect(
    host = '192.168.0.3',
    port = 9036,
    user = 'zyl',
    passwd = '888888',
    db = 'crash',
    unix_socket = '/tmp/mysql9036.sock',
    )

cur = conn.cursor()

def python_db():
    for n in range(1,20000):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        random_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        cur.execute("INSERT INTO recovery(name,ctime) VALUES('%s','%s')" %(random_str,now))	
        conn.commit()
        print(random_str,now)
        time.sleep(5)
    conn.close()

if __name__ == '__main__':
    python_db()
