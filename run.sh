#!/bin/bash
uwsgi --socket 127.0.0.1:4000 --plugin python3 --module ALGXS.wsgi &