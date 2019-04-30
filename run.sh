#!/bin/bash
case $1 in
    "up")
        uwsgi --socket :8000 --buffer-size 32768 --daemonize /var/log/ALGYunXS.log --module ALGXS.wsgi &
        echo "ALGYun已启动"
    ;;
    "down")
        port=8000
        lsof -i :$port | awk '{print $2}' > tmp
        pid=$(awk 'NR==2{print}' tmp);

        kill -9 $pid

        echo "ALGYun已经关闭"

        rm tmp
    ;;
    "restart")
        port=8000
        lsof -i :$port | awk '{print $2}' > tmp
        pid=$(awk 'NR==2{print}' tmp);

        kill -9 $pid

        uwsgi --socket :8000 --buffer-size 32768 --daemonize /var/log/ALGYunXS.log --module ALGXS.wsgi &

        echo "ALGYun重启成功"

        rm tmp
    ;;
    "makemigrationsall")
        python3 manage.py makemigrations account FandQ helps log market PTJ
    ;;
    "makemigrations")
        python3 manage.py makemigrations ${@:2}
    ;;
    "migrate")
        python3 manage.py migrate
    ;;
    "createsuperuser")
        python3 manage.py createsuperuser
    ;;
    "log")
        tail -f /var/log/ALGYunXS.log
    ;;
    "backup")
        mysqldump -u root -p ALGYunXS > /home/database-backup/alg_database_backup.sql
    ;;
    *)
        echo "unknown command"
    ;;
esac