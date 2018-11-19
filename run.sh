#!/usr/bin/env bash
uwsgi --socket :4000 --plugin python3 --module ALGXS.wsgi &