FROM debian:jessie

RUN apt-get update && apt-get install -y wget zsh \
	postgresql-client postgresql python3 python3-pip\
	libpq-dev libyaml-dev \
	pgxnclient postgresql-server-dev-all \
	postgresql-plpython3

WORKDIR /code-or-die
COPY . .
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN pip3 install -r requirements.txt

RUN pgxn install temporal_tables

CMD ["/docker-entrypoint.sh"]
