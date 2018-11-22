#!/bin/bash
uwsgi --socket :8000 --buffer-size 32768 --module ALGXS.wsgi &