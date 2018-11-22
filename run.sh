#!/bin/bash
uwsgi --socket :4000 --plugin python3 --buffer-size 32768 --module ALGXS.wsgi &