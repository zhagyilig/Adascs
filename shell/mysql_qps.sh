#!/bin/sh

mysqladmin  -uroot -pbTa*Eozx9ba0123 -S /home/mysql/mysql_9036/mysql.sock -i 1 extended-status |\
awk -F"|" \
"BEGIN{ count=0; }"\
'{ if($2 ~ /Variable_name/ && ((++count)%20 == 1)){\
    print "----------|---------|-----------------------|---------------------|--- MySQL Command Status --|----- Innodb row operation ----|-- Buffer Pool Read --|";\
    print "---Time---|---QPS---|---Threads_connected---|---Threads_running---|select insert update delete|  read inserted updated deleted|   logical    physical|";\
}\
else if ($2 ~ /Threads_connected/){Threads_connected=$3;}\
else if ($2 ~ /Threads_running/){Threads_running=$3;}\
else if ($2 ~ /Queries/){queries=$3-queries_tmp;queries_tmp=$3}\
else if ($2 ~ /Com_select /){com_select=$3-com_select_tmp;com_select_tmp=$3}\
else if ($2 ~ /Com_insert /){com_insert=$3-com_insert_tmp;com_insert_tmp=$3}\
else if ($2 ~ /Com_update /){com_update=$3-com_update_tmp;com_update_tmp=$3}\
else if ($2 ~ /Com_delete /){com_delete=$3-com_delete_tmp;com_delete_tmp=$3}\
else if ($2 ~ /Innodb_rows_read/){innodb_rows_read=$3-innodb_rows_read_tmp;innodb_rows_read_tmp=$3}\
else if ($2 ~ /Innodb_rows_deleted/){innodb_rows_deleted=$3-innodb_rows_deleted_tmp;innodb_rows_deleted_tmp=$3}\
else if ($2 ~ /Innodb_rows_inserted/){innodb_rows_inserted=$3-innodb_rows_inserted_tmp;innodb_rows_inserted_tmp=$3}\
else if ($2 ~ /Innodb_rows_updated/){innodb_rows_updated=$3-innodb_rows_updated_tmp;innodb_rows_updated_tmp=$3}\
else if ($2 ~ /Innodb_buffer_pool_read_requests/){innodb_lor=$3-innodb_lor_tmp;innodb_lor_tmp=$3}\
else if ($2 ~ /Innodb_buffer_pool_reads/){innodb_phr=$3-innodb_phr_tmp;innodb_phr_tmp=$3}\
else if ($2 ~ /Uptime / && count >= 2){\
  printf(" %s |%9d|%23d|%21d",strftime("%H:%M:%S"),queries,Threads_connected,Threads_running);\
  printf("|%6d %6d %6d %6d",com_select,com_insert,com_update,com_delete);\
  printf("|%6d %8d %7d %7d",innodb_rows_read,innodb_rows_inserted,innodb_rows_updated,innodb_rows_deleted);\
  printf("|%10d %11d|\n",innodb_lor,innodb_phr);\
}}'
