#!/bin/bash
uwsgi --http localhost:4000 --buffer-size 32768 --module ALGXS.wsgi &