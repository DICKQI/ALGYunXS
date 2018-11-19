#!/bin/bash
uwsgi --socket :4000 --plugin python3 --module ALGXS.wsgi &