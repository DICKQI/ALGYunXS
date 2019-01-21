#!/bin/bash
case $1 in
    "start")
        uwsgi --socket :8000 --buffer-size 32768 --daemonize /var/log/ALGYunXS.log --module ALGXS.wsgi &
    ;;
    "stop")
        port=8000
        lsof -i :$port | awk '{print $2}' > tmp
        pid=$(awk 'NR==2{print}' tmp);

        kill -9 $pid

        echo "ALGYun已经关闭"
    ;;
    "restart")
        port=8000
        lsof -i :$port | awk '{print $2}' > tmp
        pid=$(awk 'NR==2{print}' tmp);

        kill -9 $pid

        uwsgi --socket :8000 --buffer-size 32768 --daemonize /var/log/ALGYunXS.log --module ALGXS.wsgi &
    ;;
esac