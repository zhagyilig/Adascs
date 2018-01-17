#!/bin/sh
# zabbix agent install.

id zabbix
groupadd zabbix
useradd zabbix -s /sbin/nologin -g zabbix

cd /usr/local/src
tar xf zabbix-3.0.3.tar.gz
cd zabbix-3.0.3
./configure --prefix=/usr/local/zabbix --with-net-snmp --enable-agent
echo $?
make && make install
echo %?
cp misc/init.d/tru64/zabbix_agentd /etc/init.d/
chmod +x /etc/init.d/zabbix_agentd
