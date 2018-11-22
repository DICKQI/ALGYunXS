#!/bin/bash
uwsgi --socket :8000 --plugin python --buffer-size 32768 --module ALGXS.wsgi &