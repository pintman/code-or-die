ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
SHELL    := /usr/bin/env /bin/zsh
DB_DIR   := /var/lib/postgresql/9.4/main
LOGS_DIR := $(DB_DIR)/logs
DATABASE := code_or_die

.PHONY: test
test:
	which psql jinja2 || exit 1
	psql -d "$(DATABASE)" < "$(ROOT_DIR)/layout.sql"
	psql -d "$(DATABASE)" <<( "$(ROOT_DIR)/bitemporal.sh" "$(DATABASE)" )
	psql -d "$(DATABASE)" < "$(ROOT_DIR)/dummy.sql"
	psql -d "$(DATABASE)" <<( "$(ROOT_DIR)/orm.sh" "$(DATABASE)"  )

.PHONY: dump.sql
dump.sql:
	tables=(objects.{civilizations,systems,ships},names.{civilizations,systems,ships},orders.{systems,ships},events.{build,transit,attack,warp}) && \
	pg_dump -d "$(DATABASE)" --data-only --column-inserts $${(z)tables/#/-t } > dump.sql

.PHONY: start-db stop-db db-shell run-db
start-db:
	pg_ctl -D "$(DB_DIR)" -l "$(LOGS_DIR)/`date +%Y-%m-%d.%H%M%S`.log" start
stop-db:
	pg_ctl -D "$(DB_DIR)" stop
run-db:
	./run-db.sh "$(DB_DIR)" "$(LOGS_DIR)"
db-shell:
	PSQLRC=psqlrc psql -d "$(DATABASE)"
