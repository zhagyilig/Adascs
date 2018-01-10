#!/bin/bash
## 
## 注意事项：
## 1、运行sysbench的客户机和MySQL DB服务器尽量不要在同一台主机上，也包括一台宿主机上启动两个虚机的情形；
## 2、测试表的数量不宜太少，至少要求20个表以上；
## 3、每个表的数据量不宜太少，通常至少要求1千万以上，当然了，也要根据DB服务器的配置适当调整；
## 4、每次进行基准压测的时长不宜过短，通常要求持续15分钟以上；
## 5、每轮测试完毕后，中间至少暂停5分钟，或者确认系统负载完全恢复空跑状态为止；
## 6、测试DB服务器要是专用的，不能和其他业务混跑，否则测试结果就不靠谱了；
## 7、其余未尽事宜，后续再行补充。
##
## sysbench项目地址： https://github.com/akopytov/sysbench
## 老叶的文章： https://github.com/zhishutech/mysqldba/blob/master/mysql-benchmark/sysbench-oltp.sh
##

export LD_LIBRARY_PATH=/usr/local/mysql/lib/

. ~/.bash_profile

# 需要启用DEBUG模式时将下面三行注释去掉即可
#set -u
#set -x
#set -e

BASEDIR="/server/sysbench/sysbench_test"
[ -d $BASEDIR ] || mkdir -p $BASEDIR
cd $BASEDIR

LUADIR="/usr/local/share/sysbench"

# 记录所有错误及标准输出到 sysbench.log
exec 3>&1 4>&2 1>> sysbench.log 2>&1

# 连接数据库信息:
DBIP=xxxxxxxxxxx
DBPORT=9036
DBUSER='zyl'
DBPASSWD='xxxxxxxxxxxx'
DBNAME="sbtest"  # 压测指定的数据库

NOW=`date +'%Y%m%d%H%M'`
TBLCNT=30    	 # 创建多少张表 --oltp-tables-count
DURING=30        # 采集的时间 --time
ROWS=20000       # 每张表的数据量(行) --oltp-table-size

# 并发压测的线程数,根据机器配置实际情况进行调整
# RUN_NUMBER="8 64 128 256 512 768 1024 1664 2048 4096"
RUN_NUMBER="2 4"      

## 初始化数据:
# prepare,在本地数据库的sbtest库中,初始化表(${DBNAME}...),存储引擎是innodb,每张表20000数据。
sysbench  --test=${LUADIR}/tests/include/oltp_legacy/oltp.lua --oltp-table-size=${ROWS} --oltp-tables-count=${TBLCNT} --mysql-table-engine=innodb --mysql-user=${DBUSER} --mysql-password=${DBPASSWD} --mysql-host=${DBIP} --mysql-port=${DBPORT} --mysql-db=${DBNAME} --report-interval=1 prepare >> prepare_test.log

round=1

# 一般至少跑3轮测试，我正常都会跑10轮以上
while [ $round -lt 3 ]
do
    rounddir=logs-round${round}
    mkdir -p ${rounddir}

    for thread in `echo "${RUN_NUMBER}"`    # 压测线程数
    do
	sysbench --test=${LUADIR}/tests/include/oltp_legacy/oltp.lua --db-driver=mysql --mysql-user=${DBUSER} --mysql-password=${DBPASSWD} --mysql-host=116.196.110.16 --mysql-port=9036--mysql-db=${DBNAME} --oltp_tables_count=${TBLCNT}  --oltp-table-size=${ROWS} --rand-init=on --threads=4 --oltp-read-only=off --report-interval=1 --rand-type=uniform --time=120 --events=0 --percentile=99 run >> ./${rounddir}/sbtest_${thread}.log
        sleep 30
    done

    round=`expr $round + 1`
    sleep 300
done


