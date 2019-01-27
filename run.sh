#!/bin/bash
case $1 in
    "start")
        uwsgi --socket :8000 --buffer-size 32768 --daemonize /var/log/ALGYunXS.log --module ALGXS.wsgi &
        echo "ALGYun已启动"
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

        echo "ALGYun重启成功"
    ;;
    "makemigrations")
        python3 manage.py makemigrations account FandQ helps log market PTJ
    ;;
    "migrate")
        python3 manage.py migrate
    ;;
    "createsuperuser")
        python3 manage.py createsuperuser
    ;;
    *)
        echo "unknown command"
    ;;
esac