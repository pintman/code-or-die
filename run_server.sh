#!/bin/bash
pg_ctl -D '/Users/julianzucker/.pgsql/data' -l logfile stop
pg_ctl -D '/Users/julianzucker/.pgsql/data' -l logfile start

LOGFILE=/var/log/code-or-die.log
exec 2>&1
exec > LOGFILE
sudo python3 app.py
