#/bin/sh

# Building container
docker build -t cod .

# Running container and exposing the port of the postgres DB
docker run -d -p 5432:5432 --name cod_1 cod
