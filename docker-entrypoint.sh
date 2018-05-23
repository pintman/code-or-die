#!/bin/bash
DATABASE=code_or_die

/etc/init.d/postgresql start
alias pg_ctl=pg_ctlcluster

cd /code-or-die
su -c "psql -c \"CREATE DATABASE $DATABASE \"" postgres
mkdir -p /var/lib/postgresql/9.4/main/logs
#sleep 10
su -c make postgres
