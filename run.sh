#!/bin/bash
uwsgi --http localhost:4000 --plugin python3 --buffer-size 32768 --module ALGXS.wsgi &