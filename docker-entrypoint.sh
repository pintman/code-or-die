#!/bin/bash
DATABASE=code_or_die

/etc/init.d/postgresql start

cd /code-or-die
su -c "psql -c \"CREATE DATABASE $DATABASE \"" postgres
mkdir -p /var/lib/postgresql/9.4/main/logs
su -c make postgres

while true; do
	echo "running in endless loop"; 
	sleep 60;
done
