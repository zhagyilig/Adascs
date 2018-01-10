#!/bin/bash

echo "########################################################"                                               
echo "#                 xtrdb.net's Script                   #"
echo "########################################################"
echo
echo "##################关键status检查########################"
status(){
mysqladmin  -uroot -pbTa*Eozx9ba0123 -S /home/mysql/mysql_9036/mysql.sock extended-status | awk 'BEGIN { FS="|";s=0; } \
{if($2 ~ /Aborted_connects/){s=1} \
else if($2 ~ /Created_tmp_disk_tables/){s=1} \
else if($2 ~ /Created_tmp_tables/){s=1} \
else if($2 ~ /Handler_read_rnd/){s=1} \
else if($2 ~ /Handler_read_rnd_next/){s=1} \
else if($2 ~ /Innodb_buffer_pool_wait_free/){s=1} \
else if($2 ~ /Innodb_log_waits/){s=1} \
else if($2 ~ /Innodb_row_lock_current_waits/){s=1} \
else if($2 ~ /Open_tables/){s=1} \
else if($2 ~ /Opened_tables/){s=1} \
else if($2 ~ /Select_full_join/){s=1} \
else if($2 ~ /Select_scan/){s=1} \
else if($2 ~ /Sort_merge_passes/){s=1} \
else if($2 ~ /Table_locks_waited/){s=1} \
else if($2 ~ /Threads_cached/){s=1} \
else if($2 ~ /Threads_connected/){s=1} \
else if($2 ~ /Threads_created/){s=1} \
else{s=0}} {if(s==1){sub(/^[[:blank:]]*/,"",$2);print $2"="$3}}'  
}

status 2>/dev/null | awk '{printf "%2d %s\n",NR,$0 }'
echo "##################关键status检查########################"

main(){
while read -p "Enter line number for help(0:exit):  " line
do
        if [[ $line -eq 1 ]]; then
        		echo "Aborted_connects:"
                echo "试图连接到 MySQL 服务器而失败的连接数"
        elif [[ $line -eq 2 ]]; then
        		echo "Created_tmp_disk_tables:"
                echo "服务器执行语句时在硬盘上自动创建的临时表的数量。是指在排序时，内存不够用(tmp_table_size 小于需要排序的结果集)，所以需要创建基于磁盘的临时表进行排序"
        elif [[ $line -eq 3 ]]; then
        		echo "Created_tmp_tables:"
                echo "服务器执行语句时自动创建的内存中的临时表的数量。如果 Created_tmp_disk_tables 较大，你可能要增加 tmp_table_size 值使临时表基于内 存而不基于硬盘"
        elif [[ $line -eq 4 ]]; then
        		echo "Handler_read_rnd"
                echo "根据固定位置读一行的请求数。如果你正执行大量查询并需要对结果进行排序该值较高，说明可能使用了大量需要 MySQL 扫整个表的查询或没有正确使用索引"
        elif [[ $line -eq 5 ]]; then
        		echo "Handler_read_rnd_next"
                echo "在数据文件中读下一行的请求数。如果你正进行大量的表扫 ，该值会较高。通 常说明你的表索引不正确或写入的查询没有利用索引"
        elif [[ $line -eq 6 ]]; then
        		echo "Innodb_buffer_pool_wait_free"
                echo "一般情况，通过后台向 Innodb buffer pool 写。但是，如果需要读或创建页，并且 没有干净的页可用，则它还需要先等待页面清空。该计数器对等待实例进行记数。 如果已经适当设置 Innodb buffer pool大小，该值应小"
        elif [[ $line -eq 7 ]]; then
        		echo "Innodb_log_waits"
                echo "我们必须等待的时间，因为日志缓冲区太小，我们在继续前必须先等待对它清空"
        elif [[ $line -eq 8 ]]; then
        		echo "Innodb_row_lock_current_waits"
                echo "当前等待的待锁定的行数"
        elif [[ $line -eq 9 ]]; then
        		echo "Open_tables"
                echo "表示当前正在打开的table数量"
        elif [[ $line -eq 10 ]]; then
        		echo "Opened_tables"
                echo "表示历史上总共打开过的table数量.opened_tables太大,table_open_cache太小"
        elif [[ $line -eq 11 ]]; then
        		echo "Select_full_join"
                echo "没有使用索引的联接的数量。如果该值不为 0,你应仔细检查表的索引"
        elif [[ $line -eq 12 ]]; then
        		echo "Select_scan"
                echo "全表扫描的次数"
        elif [[ $line -eq 13 ]]; then
        		echo "Sort_merge_passes"
                echo " 由于sort buffer不够大，不得不将需要排序的数据进行分段，然后再通过sort merge的算法完成整个过程的merge总次数，一般这个参数用来参考sort buffer size 是否足够"
        elif [[ $line -eq 14 ]]; then
        		echo "Table_locks_waited"
                echo "table_locks_waited值比较高，则说明表级锁争用比较严重,可能myisam表比较多,或者频繁手动lock table"
        elif [[ $line -eq 15 ]]; then
        		echo "Threads_cached"
                echo "已经被线程缓存池缓存的线程个数"
        elif [[ $line -eq 16 ]]; then
        		echo "Threads_connected"
                echo "当前的连接数";
        elif [[ $line -eq 17 ]]; then
        		echo "Threads_created"
                echo "创建过的线程数.Threads_created 如果比较大，说明thread cache不够用"
        elif [[ $line -eq 0 ]]; then
        		exit 0
        fi
done
}
main
