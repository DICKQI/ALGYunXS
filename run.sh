#!/bin/bash
uwsgi --socket :8000 --touch-reload /home/ALGYunXS/ --buffer-size 32768 --module ALGXS.wsgi &