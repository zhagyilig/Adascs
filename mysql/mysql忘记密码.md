## mysql忘记密码后重置root密码的方法
## 知数堂同学廖尧同学整理,我也记下 :)

### 方法一：通过忽略授权表的方式重启MySQL,然后修改密码

```
在my.cnf中的[msyqld]段落中添加一下2行内容
skip-grant-tables = 1           #忽略授权表
skip-networking = 1             #在重置密码的过程中因为忽略了授权表，所以为了安全考虑就暂时不提供网络服务


#重新启动MySQL服务
[root@mysql ~]# /usr/local/mysql/bin/mysqld --defaults-file=/data/mysql/mysql3306/conf/my.cnf &
[2] 4517
[root@mysql ~]# ps aux |grep mysql3306 |grep -v grep
mysql     4517  1.5 17.7 1077540 180604 pts/1  Sl   04:07   0:00 /usr/local/mysql/bin/mysqld --defaults-file=/data/mysql/mysql3306/conf/my.cnf

#通过查看发现并没有提供网络服务
[root@mysql ~]# ss -tnl
State      Recv-Q Send-Q                                                                       Local Address:Port                                                                         Peer Address:Port
LISTEN     0      128                                                                                      *:22                                                                                      *:*
LISTEN     0      100                                                                              127.0.0.1:25                                                                                      *:*
LISTEN     0      70                                                                                      :::3307                                                                                   :::*
LISTEN     0      128                                                                                     :::22                                                                                     :::*
LISTEN     0      100                                                                                    ::1:25                                                                                     :::*


#连接到mysql进行密码修改
[root@mysql ~]# /usr/local/mysql/bin/mysql -u root -S /tmp/mysql3306.sock
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 3
Server version: 5.7.20-log MySQL Community Server (GPL)

Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

root@localhost [(none)]>

root@localhost [(none)]> select user,host,authentication_string from mysql.user;
+---------------+-----------+-------------------------------------------+
| user          | host      | authentication_string                     |
+---------------+-----------+-------------------------------------------+
| root          | localhost | *6BB4837EB74329105EE4568DDA7DC67ED2CA2AD9 |
| mysql.session | localhost | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE |
| mysql.sys     | localhost | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE |
+---------------+-----------+-------------------------------------------+
3 rows in set (0.00 sec)

#修改'root'@'localhost'的密码为abc123
root@localhost [(none)]> update mysql.user set authentication_string=password('abc123') where user='root';
Query OK, 1 row affected, 1 warning (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 1

root@localhost [(none)]> select user,host,authentication_string from mysql.user;
+---------------+-----------+-------------------------------------------+
| user          | host      | authentication_string                     |
+---------------+-----------+-------------------------------------------+
| root          | localhost | *6691484EA6B50DDDE1926A220DA01FA9E575C18A |
| mysql.session | localhost | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE |
| mysql.sys     | localhost | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE |
+---------------+-----------+-------------------------------------------+
3 rows in set (0.00 sec)

root@localhost [(none)]> flush privileges;
Query OK, 0 rows affected (0.00 sec)



#修改my.cnf删除之前添加的2行内容，然后重新启动
[root@mysql ~]# /usr/local/mysql/bin/mysqladmin -u root -pabc123 -S /tmp/mysql3306.sock shutdown
mysqladmin: [Warning] Using a password on the command line interface can be insecure.

[root@mysql ~]# /usr/local/mysql/bin/mysqld --defaults-file=/data/mysql/mysql3306/conf/my.cnf &
[2] 4559
[root@mysql ~]# ss -tnl |grep 3306
LISTEN     0      70                       :::3306                    :::*
[root@mysql ~]# ps aux |grep mysql3306 |grep -v grep
mysql     4559  0.6 17.7 1077720 180956 pts/1  Sl   04:14   0:00 /usr/local/mysql/bin/mysqld --defaults-file=/data/mysql/mysql3306/conf/my.cnf

#使用新密abc123连接mysql
[root@mysql ~]# /usr/local/mysql/bin/mysql -u root -pabc123 -S /tmp/mysql3306.sock
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 3
Server version: 5.7.20-log MySQL Community Server (GPL)

Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

root@localhost [(none)]>
```



### 方法2：通过使用参数init-file来重置root登录密码

```
关闭mysql 服务
[root@mysql ~]# /usr/local/mysql/bin/mysqladmin -u root -plyao36843 -S /tmp/mysql3306.sock shutdown

[root@mysql ~]# ss -tnl |grep 3306 |grep -v grep

#在my.cnf中添加下面的参数
[root@mysql ~]# cat /data/mysql/mysql3306/conf/my.cnf |grep setpass
init-file = /tmp/setpassword.sql

#文件内容入下,主要是将密码修改为haha123
[root@mysql ~]# cat /tmp/setpassword.sql
update mysql.user set authentication_string=password('haha123') where user='root';
flush privileges;


#重新启动mysql服务
[root@mysql ~]# /usr/local/mysql/bin/mysqld --defaults-file=/data/mysql/mysql3306/conf/my.cnf &
[2] 4707
[root@mysql ~]# ss -tnl |grep 3306 |grep -v grep
LISTEN     0      70                       :::3306                    :::*

#使用新密码haha123进行连接
[root@mysql ~]# /usr/local/mysql/bin/mysql -u root -phaha123 -S /tmp/mysql3306.sock
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 4
Server version: 5.7.20-log MySQL Community Server (GPL)

Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

root@localhost [(none)]>
```
### 方法3: 在mysql不重启的情况下重置登录密码

```
#进到mysql3306实例的数据目录下
[root@mysql mysql]# pwd
/data/mysql/mysql3306/data/mysql

[root@mysql mysql]# ll |grep user
-rw-r----- 1 mysql mysql   10816 1月  11 03:55 user.frm
-rw-r----- 1 mysql mysql     508 1月  18 04:37 user.MYD
-rw-r----- 1 mysql mysql    4096 1月  18 04:37 user.MYI


#在操作前先将这3个文件备份下，避免出错
[root@mysql mysql]# cp user.frm user.frm_bak_20180118
[root@mysql mysql]# cp user.MYD user.MYD_bak_20180118
[root@mysql mysql]# cp user.MYI user.MYI_bak_20180118


#将这3个文件复制到其它mysql示例的某个数据目录下，我这里复制到msyql3307下的mytest数据目录下
[root@mysql mysql]# cp user.* /data/mysql/mysql3307/data/mytest/
[root@mysql mysql]# chown -R mysql.mysql /data/mysql/mysql3307/data/mytest

#连接到mysql3307实例上
[root@mysql mysql]# /usr/local/mysql/bin/mysql -u root -p123456 -S /tmp/mysql3307.sock mytest
mysql: [Warning] Using a password on the command line interface can be insecure.
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 7
Server version: 5.7.20-log MySQL Community Server (GPL)

Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

root@localhost [mytest]> show tables;
+------------------+
| Tables_in_mytest |
+------------------+
| user             |
+------------------+
1 row in set (0.00 sec)

#查看user的表结构
root@localhost [mytest]> desc user;
+------------------------+-----------------------------------+------+-----+-----------------------+-------+
| Field                  | Type                              | Null | Key | Default               | Extra |
+------------------------+-----------------------------------+------+-----+-----------------------+-------+
| Host                   | char(60)                          | NO   | PRI |                       |       |
| User                   | char(32)                          | NO   | PRI |                       |       |
| Select_priv            | enum('N','Y')                     | NO   |     | N                     |       |
| Insert_priv            | enum('N','Y')                     | NO   |     | N                     |       |
| Update_priv            | enum('N','Y')                     | NO   |     | N                     |       |
| Delete_priv            | enum('N','Y')                     | NO   |     | N                     |       |
| Create_priv            | enum('N','Y')                     | NO   |     | N                     |       |
| Drop_priv              | enum('N','Y')                     | NO   |     | N                     |       |
| Reload_priv            | enum('N','Y')                     | NO   |     | N                     |       |
| Shutdown_priv          | enum('N','Y')                     | NO   |     | N                     |       |
| Process_priv           | enum('N','Y')                     | NO   |     | N                     |       |
| File_priv              | enum('N','Y')                     | NO   |     | N                     |       |
| Grant_priv             | enum('N','Y')                     | NO   |     | N                     |       |
| References_priv        | enum('N','Y')                     | NO   |     | N                     |       |
| Index_priv             | enum('N','Y')                     | NO   |     | N                     |       |
| Alter_priv             | enum('N','Y')                     | NO   |     | N                     |       |
| Show_db_priv           | enum('N','Y')                     | NO   |     | N                     |       |
| Super_priv             | enum('N','Y')                     | NO   |     | N                     |       |
| Create_tmp_table_priv  | enum('N','Y')                     | NO   |     | N                     |       |
| Lock_tables_priv       | enum('N','Y')                     | NO   |     | N                     |       |
| Execute_priv           | enum('N','Y')                     | NO   |     | N                     |       |
| Repl_slave_priv        | enum('N','Y')                     | NO   |     | N                     |       |
| Repl_client_priv       | enum('N','Y')                     | NO   |     | N                     |       |
| Create_view_priv       | enum('N','Y')                     | NO   |     | N                     |       |
| Show_view_priv         | enum('N','Y')                     | NO   |     | N                     |       |
| Create_routine_priv    | enum('N','Y')                     | NO   |     | N                     |       |
| Alter_routine_priv     | enum('N','Y')                     | NO   |     | N                     |       |
| Create_user_priv       | enum('N','Y')                     | NO   |     | N                     |       |
| Event_priv             | enum('N','Y')                     | NO   |     | N                     |       |
| Trigger_priv           | enum('N','Y')                     | NO   |     | N                     |       |
| Create_tablespace_priv | enum('N','Y')                     | NO   |     | N                     |       |
| ssl_type               | enum('','ANY','X509','SPECIFIED') | NO   |     |                       |       |
| ssl_cipher             | blob                              | NO   |     | NULL                  |       |
| x509_issuer            | blob                              | NO   |     | NULL                  |       |
| x509_subject           | blob                              | NO   |     | NULL                  |       |
| max_questions          | int(11) unsigned                  | NO   |     | 0                     |       |
| max_updates            | int(11) unsigned                  | NO   |     | 0                     |       |
| max_connections        | int(11) unsigned                  | NO   |     | 0                     |       |
| max_user_connections   | int(11) unsigned                  | NO   |     | 0                     |       |
| plugin                 | char(64)                          | NO   |     | mysql_native_password |       |
| authentication_string  | text                              | YES  |     | NULL                  |       |
| password_expired       | enum('N','Y')                     | NO   |     | N                     |       |
| password_last_changed  | timestamp                         | YES  |     | NULL                  |       |
| password_lifetime      | smallint(5) unsigned              | YES  |     | NULL                  |       |
| account_locked         | enum('N','Y')                     | NO   |     | N                     |       |
+------------------------+-----------------------------------+------+-----+-----------------------+-------+
45 rows in set (0.00 sec)

#查看表中的用户数据
root@localhost [mytest]> select user,host,authentication_string from user;
+---------------+-----------+-------------------------------------------+
| user          | host      | authentication_string                     |
+---------------+-----------+-------------------------------------------+
| root          | localhost | *243A628A55621C5AE3B405C0A8EDF5E85DAD86F9 |
| mysql.session | localhost | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE |
| mysql.sys     | localhost | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE |
+---------------+-----------+-------------------------------------------+
3 rows in set (0.00 sec)

#修改密码为helloworld
root@localhost [mytest]> update user set  authentication_string=password('helloworld') where user='root';
Query OK, 1 row affected, 1 warning (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 1

root@localhost [mytest]> select user,host,authentication_string from user;
+---------------+-----------+-------------------------------------------+
| user          | host      | authentication_string                     |
+---------------+-----------+-------------------------------------------+
| root          | localhost | *D35DB127DB631E6E27C6B75E8D376B04F64FAF83 |
| mysql.session | localhost | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE |
| mysql.sys     | localhost | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE |
+---------------+-----------+-------------------------------------------+
3 rows in set (0.00 sec)


#将修改后的数据文件复制回mysql3306实例下
[root@mysql mytest]# pwd
/data/mysql/mysql3307/data/mytest
[root@mysql mytest]# cp user.frm /data/mysql/mysql3306/data/mysql
cp：是否覆盖"/data/mysql/mysql3306/data/mysql/user.frm"？ y
[root@mysql mytest]# cp -rf user.MYD /data/mysql/mysql3306/data/mysql
cp：是否覆盖"/data/mysql/mysql3306/data/mysql/user.MYD"？ y
[root@mysql mytest]# cp -rf user.MYI /data/mysql/mysql3306/data/mysql
cp：是否覆盖"/data/mysql/mysql3306/data/mysql/user.MYI"？ y

#查看下mysql3306实例下的文件权限
[root@mysql mysql]# pwd
/data/mysql/mysql3306/data/mysql
[root@mysql mysql]# ll |grep user
-rw-r----- 1 mysql mysql   10816 1月  18 05:24 user.frm
-rw-r----- 1 root  root    10816 1月  18 04:42 user.frm_bak_20180118
-rw-r----- 1 mysql mysql     508 1月  18 05:25 user.MYD
-rw-r----- 1 root  root      508 1月  18 04:42 user.MYD_bak_20180118
-rw-r----- 1 mysql mysql    4096 1月  18 05:25 user.MYI
-rw-r----- 1 root  root     4096 1月  18 04:43 user.MYI_bak_20180118



#获取mysql3306实例的pid
[root@mysql mysql]# ps aux |grep mysql3306 |grep -v grep | awk '{print $2}'
4707

#发送SIGHUP信号
[root@mysql mysql]# kill -SIGHUP 4707
[root@mysql mysql]# ps aux |grep mysql3306 |grep -v grep
mysql     4707  0.0 18.9 1077920 192728 ?      Sl   05:06   0:00 /usr/local/mysql/bin/mysqld --defaults-file=/data/mysql/mysql3306/conf/my.cnf

#使用新密码helloworld进行连接
[root@mysql mysql]# /usr/local/mysql/bin/mysql -u root -phelloworld -S /tmp/mysql3306.sock
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 5
Server version: 5.7.20-log MySQL Community Server (GPL)

Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

root@localhost [(none)]>


从上面结果能看到可以正常使用新密进行连接，整个过程没有重启mysql3306实例
```
