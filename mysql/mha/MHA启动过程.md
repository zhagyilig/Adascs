//  MHA 启动流程
//  连接master
Sat Jan 13 09:21:09 2018 - [info] MHA::MasterMonitor version 0.56.
Sat Jan 13 09:21:09 2018 - [debug] Connecting to servers..
Sat Jan 13 09:21:09 2018 - [debug]  Connected to: 172.168.64.89(172.168.64.89:3306), user=zyl
Sat Jan 13 09:21:09 2018 - [debug]  Number of slave worker threads on host 172.168.64.89(172.168.64.89:3306): 0
Sat Jan 13 09:21:09 2018 - [debug]  Connected to: 172.168.64.91(172.168.64.91:3306), user=zyl
Sat Jan 13 09:21:09 2018 - [debug]  Number of slave worker threads on host 172.168.64.91(172.168.64.91:3306): 0
Sat Jan 13 09:21:09 2018 - [debug]  Comparing MySQL versions..
Sat Jan 13 09:21:09 2018 - [debug]   Comparing MySQL versions done.
Sat Jan 13 09:21:09 2018 - [debug] Connecting to servers done.

Sat Jan 13 09:21:09 2018 - [info] GTID failover mode = 1
Sat Jan 13 09:21:09 2018 - [info] Dead Servers:
Sat Jan 13 09:21:09 2018 - [info] Alive Servers:
Sat Jan 13 09:21:09 2018 - [info]   172.168.64.89(172.168.64.89:3306)
Sat Jan 13 09:21:09 2018 - [info]   172.168.64.91(172.168.64.91:3306)
Sat Jan 13 09:21:09 2018 - [info] Alive Slaves:
Sat Jan 13 09:21:09 2018 - [info]   172.168.64.89(172.168.64.89:3306)  Version=5.7.20-log (oldest major version between slaves) log-bin:enabled
Sat Jan 13 09:21:09 2018 - [info]     GTID ON
Sat Jan 13 09:21:09 2018 - [debug]    Relay log info repository: FILE
Sat Jan 13 09:21:09 2018 - [info]     Replicating from 172.168.64.91(172.168.64.91:3306)
Sat Jan 13 09:21:09 2018 - [info]     Primary candidate(候选) for the new Master (candidate_master is set)

Sat Jan 13 09:21:09 2018 - [info] Current Alive Master: 172.168.64.91(172.168.64.91:3306)

//  检查slave的状态
Sat Jan 13 09:21:09 2018 - [info] Checking slave configurations..
Sat Jan 13 09:21:09 2018 - [info]  read_only=1 is not set on slave 172.168.64.89(172.168.64.89:3306).
Sat Jan 13 09:21:09 2018 - [info] Checking replication filtering settings..
Sat Jan 13 09:21:09 2018 - [info]  binlog_do_db= , binlog_ignore_db= 
Sat Jan 13 09:21:09 2018 - [info]  Replication filtering check ok.
Sat Jan 13 09:21:09 2018 - [info] GTID (with auto-pos) is supported. Skipping all SSH and Node package checking.

//  检查ssh key
Sat Jan 13 09:21:09 2018 - [info] Checking SSH publickey authentication settings on the current master..
Sat Jan 13 09:21:09 2018 - [debug] SSH connection test to 172.168.64.91, option -o StrictHostKeyChecking=no -o PasswordAuthentication=no -o BatchMode=yes -o ConnectTimeout=5, timeout 5
Sat Jan 13 09:21:10 2018 - [info] HealthCheck: SSH to 172.168.64.91 is reachable(可到达的).
Sat Jan 13 09:21:10 2018 - [info] 
172.168.64.91(172.168.64.91:3306) (current master)
 +--172.168.64.89(172.168.64.89:3306)

//  检查master vip切换脚本
Sat Jan 13 09:21:10 2018 - [info] Checking master_ip_failover_script status:
Sat Jan 13 09:21:10 2018 - [info]   /etc/masterha/master_ip_failover --command=status --ssh_user=root --orig_master_host=172.168.64.91 --orig_master_ip=172.168.64.91 --orig_master_port=3306 
Sat Jan 13 09:21:10 2018 - [info]  OK.

Sat Jan 13 09:21:10 2018 - [warning] shutdown_script is not defined.  //  停止master脚本,配置文件中没有定义

Sat Jan 13 09:21:10 2018 - [debug]  Disconnected from 172.168.64.89(172.168.64.89:3306)
Sat Jan 13 09:21:10 2018 - [debug]  Disconnected from 172.168.64.91(172.168.64.91:3306)
Sat Jan 13 09:21:10 2018 - [debug] SSH check command: exit 0


Sat Jan 13 09:21:10 2018 - [info] Set master ping interval 1 seconds.  // 　masterha_default.conf定义ping间隔

Sat Jan 13 09:21:10 2018 - [warning] secondary_check_script is not defined. It is highly recommended setting it to check master reachability from two or more routes.


Sat Jan 13 09:21:10 2018 - [info] Starting ping health check on 172.168.64.91(172.168.64.91:3306)..
Sat Jan 13 09:21:10 2018 - [debug] Connected on master.
Sat Jan 13 09:21:10 2018 - [debug] Set short wait_timeout on master: 2 seconds
Sat Jan 13 09:21:10 2018 - [debug] Trying to get advisory lock..
Sat Jan 13 09:21:10 2018 - [info] Ping(SELECT) succeeded, waiting until MySQL doesn't respond..
