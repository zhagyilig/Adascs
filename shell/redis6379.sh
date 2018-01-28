#!/bin/sh
#
# https://redisdoc.com
# https://redis.io/
# Simple Redis init.d script conceived to work on Linux systems
# as it does use of the /proc filesystem.
# chkconfig: 2345 66 92
# description:  Starts, stops and saves nosql redis

. /etc/init.d/functions
REDISPORT=6379
EXEC="/usr/local/redis/bin/redis-server"
CLIEXEC="/usr/local/redis/bin/redis-cli"
DATADIR="/data/redis/redis${REDISPORT}"
PIDFILE="${DATADIR}/data/redis${REDISPORT}.pid"
CONF="${DATADIR}/redis${REDISPORT}.conf"

case "$1" in
    start)
        if [ -f $PIDFILE ]
        then
                echo "$PIDFILE exists, process is already running or crashed"
        else
                action "Starting Redis server ..." /bin/true
                $EXEC $CONF
        fi
        ;;
    stop)
        if [ ! -f $PIDFILE ]
        then
                echo "$PIDFILE does not exist, process is not running"
        else
                PID=$(cat $PIDFILE)
                action  "Stopping Redis server ..."  /bin/true
                $CLIEXEC -p $REDISPORT shutdown
                while [ -x /proc/${PID} ]
                do
                    echo "Waiting for Redis to shutdown ..."
                    sleep 1
                done
                echo "Redis stopped"
        fi
        ;;
     restart)
        $0 stop
        sleep 1
        $0 start
        ;;
    *)
        echo -e "Usage: $0 {start|stop|restart}"
esac
