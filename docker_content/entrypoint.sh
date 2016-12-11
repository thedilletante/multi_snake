#!/bin/sh
nginx -g "daemon off;" >/var/log/nginx/stdout.log 2>&1 &
python3.5 /opt/snake_tournament/server/index.py
