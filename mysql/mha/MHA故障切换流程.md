//  MHA切换流程
//  检查ssh 和 master的状态,确定master宕机
//  疑问：执行的什么操作(命令)去检查master的状态
//  检测master的状态，方法是一秒一次"SELECT 1 As Value"，发现没有响应后会重复3次检查，如果还没有响应，shutdown并再重复一次SELECT 1 As Value确认master关闭
Sat Jan 13 09:28:35 2018 - [warning] Got error on MySQL select ping: 2006 (MySQL server has gone away)
Sat Jan 13 09:28:35 2018 - [info] Executing SSH check script: exit 0
Sat Jan 13 09:28:35 2018 - [debug] SSH connection test to 172.168.64.91, option -o StrictHostKeyChecking=no -o PasswordAuthentication=no -o BatchMode=yes -o ConnectTimeout=5, timeout 5
Sat Jan 13 09:28:35 2018 - [info] HealthCheck: SSH to 172.168.64.91 is reachable.
Sat Jan 13 09:28:36 2018 - [warning] Got error on MySQL connect: 2013 (Lost connection to MySQL server at 'reading initial communication packet', system error: 111)
Sat Jan 13 09:28:36 2018 - [warning] Connection failed 2 time(s)..
Sat Jan 13 09:28:37 2018 - [warning] Got error on MySQL connect: 2013 (Lost connection to MySQL server at 'reading initial communication packet', system error: 111)
Sat Jan 13 09:28:37 2018 - [warning] Connection failed 3 time(s)..
Sat Jan 13 09:28:38 2018 - [warning] Got error on MySQL connect: 2013 (Lost connection to MySQL server at 'reading initial communication packet', system error: 111)
Sat Jan 13 09:28:38 2018 - [warning] Connection failed 4 time(s)..
Sat Jan 13 09:28:38 2018 - [warning] Master is not reachable from health checker!
Sat Jan 13 09:28:38 2018 - [warning] Master 172.168.64.91(172.168.64.91:3306) is not reachable!
Sat Jan 13 09:28:38 2018 - [warning] SSH is reachable.

//  尝试连接所有的MySQL Server
//  给出消息：Connecting to a master server failed，并开始读取配置文件masterha_default.conf和app1.conf
Sat Jan 13 09:28:38 2018 - [info] Connecting to a master server failed. Reading configuration file /etc/masterha/masterha_default.conf and /etc/masterha/app1.conf again, and trying to connect to all servers to check server status..

Sat Jan 13 09:28:38 2018 - [info] Reading default configuration from /etc/masterha/masterha_default.conf..
Sat Jan 13 09:28:38 2018 - [info] Reading application default configuration from /etc/masterha/app1.conf..
Sat Jan 13 09:28:38 2018 - [info] Reading server configuration from /etc/masterha/app1.conf..
Sat Jan 13 09:28:38 2018 - [debug] Skipping connecting to dead master 172.168.64.91(172.168.64.91:3306). //  跳过不能连接的server

Sat Jan 13 09:28:38 2018 - [debug] Connecting to servers..
Sat Jan 13 09:28:38 2018 - [debug]  Connected to: 172.168.64.89(172.168.64.89:3306), user=zyl
Sat Jan 13 09:28:38 2018 - [debug]  Number of slave worker threads on host 172.168.64.89(172.168.64.89:3306): 0
Sat Jan 13 09:28:38 2018 - [debug]  Comparing MySQL versions..
Sat Jan 13 09:28:38 2018 - [debug]   Comparing MySQL versions done.
Sat Jan 13 09:28:38 2018 - [debug] Connecting to servers done.

//  确认复制切换模式
Sat Jan 13 09:28:38 2018 - [info] GTID failover mode = 1

//  报告整个结构中机器的存活的情况，我的是一主一从结构
Sat Jan 13 09:28:38 2018 - [info] Dead Servers:
Sat Jan 13 09:28:38 2018 - [info]   172.168.64.91(172.168.64.91:3306)
Sat Jan 13 09:28:38 2018 - [info] Alive Servers:
Sat Jan 13 09:28:38 2018 - [info]   172.168.64.89(172.168.64.89:3306)
Sat Jan 13 09:28:38 2018 - [info] Alive Slaves:
Sat Jan 13 09:28:38 2018 - [info]   172.168.64.89(172.168.64.89:3306)  Version=5.7.20-log (oldest major version between slaves) log-bin:enabled

//  检查存活的实例版本、GTID开启情况、是否开启read_only以及复制过滤情况
Sat Jan 13 09:28:38 2018 - [info]     GTID ON
Sat Jan 13 09:28:38 2018 - [debug]    Relay log info repository: FILE
Sat Jan 13 09:28:38 2018 - [info]     Replicating from 172.168.64.91(172.168.64.91:3306)
Sat Jan 13 09:28:38 2018 - [info]     Primary candidate for the new Master (candidate_master is set)
Sat Jan 13 09:28:38 2018 - [info] Checking slave configurations..
Sat Jan 13 09:28:38 2018 - [info]  read_only=1 is not set on slave 172.168.64.89(172.168.64.89:3306).
Sat Jan 13 09:28:38 2018 - [info] Checking replication filtering settings..
Sat Jan 13 09:28:38 2018 - [info]  Replication filtering check ok.

Sat Jan 13 09:28:38 2018 - [info] Master is down!

Sat Jan 13 09:28:38 2018 - [info] Terminating monitoring script.
Sat Jan 13 09:28:38 2018 - [info] Got exit code 20 (Master dead).
Sat Jan 13 09:28:38 2018 - [info] MHA::MasterFailover version 0.56.
Sat Jan 13 09:28:38 2018 - [info] Starting master failover.
Sat Jan 13 09:28:38 2018 - [info] 

//  在GTID复制基础上的切换过程
//  配置文件检查
Sat Jan 13 09:28:38 2018 - [info] * Phase 1: Configuration Check Phase..
Sat Jan 13 09:28:38 2018 - [info] 
Sat Jan 13 09:28:38 2018 - [debug] Skipping connecting to dead master 172.168.64.91.
Sat Jan 13 09:28:38 2018 - [debug] Connecting to servers..
Sat Jan 13 09:28:38 2018 - [debug]  Connected to: 172.168.64.89(172.168.64.89:3306), user=zyl
Sat Jan 13 09:28:38 2018 - [debug]  Number of slave worker threads on host 172.168.64.89(172.168.64.89:3306): 0
Sat Jan 13 09:28:38 2018 - [debug]  Comparing MySQL versions..
Sat Jan 13 09:28:38 2018 - [debug]   Comparing MySQL versions done.
Sat Jan 13 09:28:38 2018 - [debug] Connecting to servers done.
Sat Jan 13 09:28:38 2018 - [info] GTID failover mode = 1
Sat Jan 13 09:28:38 2018 - [info] Dead Servers:
Sat Jan 13 09:28:38 2018 - [info]   172.168.64.91(172.168.64.91:3306)
Sat Jan 13 09:28:38 2018 - [info] Checking master reachability via MySQL(double check)...
Sat Jan 13 09:28:38 2018 - [info]  ok.
Sat Jan 13 09:28:38 2018 - [info] Alive Servers:
Sat Jan 13 09:28:38 2018 - [info]   172.168.64.89(172.168.64.89:3306)
Sat Jan 13 09:28:38 2018 - [info] Alive Slaves:
Sat Jan 13 09:28:38 2018 - [info]   172.168.64.89(172.168.64.89:3306)  Version=5.7.20-log (oldest major version between slaves) log-bin:enabled
Sat Jan 13 09:28:38 2018 - [info]     GTID ON
Sat Jan 13 09:28:38 2018 - [debug]    Relay log info repository: FILE
Sat Jan 13 09:28:38 2018 - [info]     Replicating from 172.168.64.91(172.168.64.91:3306)
Sat Jan 13 09:28:38 2018 - [info]     Primary candidate for the new Master (candidate_master is set)
Sat Jan 13 09:28:38 2018 - [info] Starting GTID based failover.
Sat Jan 13 09:28:38 2018 - [info] 
Sat Jan 13 09:28:38 2018 - [info] ** Phase 1: Configuration Check Phase completed.
Sat Jan 13 09:28:38 2018 - [info] 

//  彻底关闭master连接的阶段，避免master未关闭导致的脑裂
Sat Jan 13 09:28:38 2018 - [info] * Phase 2: Dead Master Shutdown Phase..
Sat Jan 13 09:28:38 2018 - [info] 
Sat Jan 13 09:28:38 2018 - [info] Forcing shutdown so that applications never connect to the current master..
Sat Jan 13 09:28:38 2018 - [info] Executing master IP deactivation script:
Sat Jan 13 09:28:38 2018 - [info]   /etc/masterha/master_ip_failover --orig_master_host=172.168.64.91 --orig_master_ip=172.168.64.91 --orig_master_port=3306 --command=stopssh --ssh_user=root  

//  停止接管机器的 IO thread
Sat Jan 13 09:28:38 2018 - [debug]  Stopping IO thread on 172.168.64.89(172.168.64.89:3306)..
Sat Jan 13 09:28:39 2018 - [debug]  Stop IO thread on 172.168.64.89(172.168.64.89:3306) done.
Sat Jan 13 09:28:39 2018 - [info]  done.

Sat Jan 13 09:28:39 2018 - [warning] shutdown_script is not set. Skipping explicit shutting down of the dead master.
Sat Jan 13 09:28:39 2018 - [info] * Phase 2: Dead Master Shutdown Phase completed.
Sat Jan 13 09:28:39 2018 - [info] 

//  master 转移恢复过程
Sat Jan 13 09:28:39 2018 - [info] * Phase 3: Master Recovery Phase..
Sat Jan 13 09:28:39 2018 - [info] 

//  确认relay log最新的slave实例
Sat Jan 13 09:28:39 2018 - [info] * Phase 3.1: Getting Latest Slaves Phase..
Sat Jan 13 09:28:39 2018 - [info] 
Sat Jan 13 09:28:39 2018 - [debug] Fetching current slave status..
Sat Jan 13 09:28:39 2018 - [debug]  Fetching current slave status done.

Sat Jan 13 09:28:39 2018 - [info] The latest binary log file/position on all slaves is mysql-bin.000001:7859538

Sat Jan 13 09:28:39 2018 - [info] Retrieved Gtid Set: cca639fa-f5e2-11e7-8d18-000c297cac83:1-27338
Sat Jan 13 09:28:39 2018 - [info] Latest slaves (Slaves that received relay log files to the latest):
Sat Jan 13 09:28:39 2018 - [info]   172.168.64.89(172.168.64.89:3306)  Version=5.7.20-log (oldest major version between slaves) log-bin:enabled
Sat Jan 13 09:28:39 2018 - [info]     GTID ON
Sat Jan 13 09:28:39 2018 - [debug]    Relay log info repository: FILE
Sat Jan 13 09:28:39 2018 - [info]     Replicating from 172.168.64.91(172.168.64.91:3306)
Sat Jan 13 09:28:39 2018 - [info]     Primary candidate for the new Master (candidate_master is set)
Sat Jan 13 09:28:39 2018 - [info] The oldest binary log file/position on all slaves is mysql-bin.000001:7859538
Sat Jan 13 09:28:39 2018 - [info] Retrieved Gtid Set: cca639fa-f5e2-11e7-8d18-000c297cac83:1-27338
Sat Jan 13 09:28:39 2018 - [info] Oldest slaves:
Sat Jan 13 09:28:39 2018 - [info]   172.168.64.89(172.168.64.89:3306)  Version=5.7.20-log (oldest major version between slaves) log-bin:enabled
Sat Jan 13 09:28:39 2018 - [info]     GTID ON
Sat Jan 13 09:28:39 2018 - [debug]    Relay log info repository: FILE
Sat Jan 13 09:28:39 2018 - [info]     Replicating from 172.168.64.91(172.168.64.91:3306)
Sat Jan 13 09:28:39 2018 - [info]     Primary candidate for the new Master (candidate_master is set)
Sat Jan 13 09:28:39 2018 - [info] 

Sat Jan 13 09:28:39 2018 - [info] * Phase 3.3: Determining New Master Phase..
Sat Jan 13 09:28:39 2018 - [info] 
Sat Jan 13 09:28:39 2018 - [debug] Checking replication delay on 172.168.64.89(172.168.64.89:3306).. 
Sat Jan 13 09:28:39 2018 - [debug]  ok.
Sat Jan 13 09:28:39 2018 - [info] Searching new master from slaves..
Sat Jan 13 09:28:39 2018 - [info]  Candidate masters from the configuration file:
Sat Jan 13 09:28:39 2018 - [info]   172.168.64.89(172.168.64.89:3306)  Version=5.7.20-log (oldest major version between slaves) log-bin:enabled
Sat Jan 13 09:28:39 2018 - [info]     GTID ON
Sat Jan 13 09:28:39 2018 - [debug]    Relay log info repository: FILE
Sat Jan 13 09:28:39 2018 - [info]     Replicating from 172.168.64.91(172.168.64.91:3306)
Sat Jan 13 09:28:39 2018 - [info]     Primary candidate for the new Master (candidate_master is set)
Sat Jan 13 09:28:39 2018 - [info]  Non-candidate masters:
Sat Jan 13 09:28:39 2018 - [info]  Searching from candidate_master slaves which have received the latest relay log events..
Sat Jan 13 09:28:39 2018 - [info] New master is 172.168.64.89(172.168.64.89:3306)
Sat Jan 13 09:28:39 2018 - [info] Starting master failover..
Sat Jan 13 09:28:39 2018 - [info] 
From:
172.168.64.91(172.168.64.91:3306) (current master)
 +--172.168.64.89(172.168.64.89:3306)

To:
172.168.64.89(172.168.64.89:3306) (new master)
Sat Jan 13 09:28:39 2018 - [info] 
Sat Jan 13 09:28:39 2018 - [info] * Phase 3.3: New Master Recovery Phase..
Sat Jan 13 09:28:39 2018 - [info] 
Sat Jan 13 09:28:39 2018 - [info]  Waiting all logs to be applied.. 
Sat Jan 13 09:28:39 2018 - [info]   done.
Sat Jan 13 09:28:39 2018 - [debug]  Stopping slave IO/SQL thread on 172.168.64.89(172.168.64.89:3306)..
Sat Jan 13 09:28:39 2018 - [debug]   done.
Sat Jan 13 09:28:39 2018 - [info] Getting new master's binlog name and position..
Sat Jan 13 09:28:39 2018 - [info]  mysql-bin.000002:7290281
Sat Jan 13 09:28:39 2018 - [info]  All other slaves should start replication from here. Statement should be: CHANGE MASTER TO MASTER_HOST='172.168.64.89', MASTER_PORT=3306, MASTER_AUTO_POSITION=1, MASTER_USER='zyl', MASTER_PASSWORD='xxx';
Sat Jan 13 09:28:39 2018 - [info] Master Recovery succeeded. File:Pos:Exec_Gtid_Set: mysql-bin.000002, 7290281, c83ebdde-f5e2-11e7-8d3d-000c295e93e0:1-290,
cca639fa-f5e2-11e7-8d18-000c297cac83:1-27338

//  切换vip
Sat Jan 13 09:28:39 2018 - [info] Executing master IP activate script:
Sat Jan 13 09:28:39 2018 - [info]   /etc/masterha/master_ip_failover --command=start --ssh_user=root --orig_master_host=172.168.64.91 --orig_master_ip=172.168.64.91 --orig_master_port=3306 --new_master_host=172.168.64.89 --new_master_ip=172.168.64.89 --new_master_port=3306 --new_master_user='zyl' --new_master_password='888888' 

Set read_only=0 on the new master.
RTNETLINK answers: Cannot assign requested address
RTNETLINK answers: File exists
Sat Jan 13 09:28:39 2018 - [info]  OK.
Sat Jan 13 09:28:39 2018 - [info] ** Finished master recovery successfully.
Sat Jan 13 09:28:39 2018 - [info] * Phase 3: Master Recovery Phase completed.

//  slave恢复阶段
//  先停止IO线程，等待SQL线程执行完成后，stop slave，清除原slave信息，重新change master指向新的master,start slave;
Sat Jan 13 09:28:39 2018 - [info] 
Sat Jan 13 09:28:39 2018 - [info] * Phase 4: Slaves Recovery Phase..
Sat Jan 13 09:28:39 2018 - [info] 
Sat Jan 13 09:28:39 2018 - [info] 
Sat Jan 13 09:28:39 2018 - [info] * Phase 4.1: Starting Slaves in parallel..
Sat Jan 13 09:28:39 2018 - [info] 
Sat Jan 13 09:28:39 2018 - [info] All new slave servers recovered successfully.
Sat Jan 13 09:28:39 2018 - [info] 

//  清除新选出的master上的slave信息
Sat Jan 13 09:28:39 2018 - [info] * Phase 5: New master cleanup phase..
Sat Jan 13 09:28:39 2018 - [info] 
Sat Jan 13 09:28:39 2018 - [info] Resetting slave info on the new master..
Sat Jan 13 09:28:39 2018 - [debug]  Clearing slave info..
Sat Jan 13 09:28:39 2018 - [debug]  Stopping slave IO/SQL thread on 172.168.64.89(172.168.64.89:3306)..
Sat Jan 13 09:28:39 2018 - [debug]   done.
Sat Jan 13 09:28:39 2018 - [debug]  SHOW SLAVE STATUS shows new master does not replicate from anywhere. OK.
Sat Jan 13 09:28:39 2018 - [info]  172.168.64.89: Resetting slave info succeeded.
Sat Jan 13 09:28:39 2018 - [info] Master failover to 172.168.64.89(172.168.64.89:3306) completed successfully.

Sat Jan 13 09:28:39 2018 - [debug]  Disconnected from 172.168.64.89(172.168.64.89:3306)
Sat Jan 13 09:28:39 2018 - [info] 

//  至此，整个切换过程完成，最后生成切换报告
----- Failover Report -----

app1: MySQL Master failover 172.168.64.91(172.168.64.91:3306) to 172.168.64.89(172.168.64.89:3306) succeeded

Master 172.168.64.91(172.168.64.91:3306) is down!

Check MHA Manager logs at pxc1:/var/log/masterha/app1/app1.log for details.

Started automated(non-interactive) failover.
Invalidated master IP address on 172.168.64.91(172.168.64.91:3306)
Selected 172.168.64.89(172.168.64.89:3306) as a new master.

172.168.64.89(172.168.64.89:3306): OK: Applying all logs succeeded.
172.168.64.89(172.168.64.89:3306): OK: Activated master IP address.
172.168.64.89(172.168.64.89:3306): Resetting slave info succeeded.
Master failover to 172.168.64.89(172.168.64.89:3306) completed successfully.
