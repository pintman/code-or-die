#/bin/sh

# Building container
docker build -t cod .

# Running container and exposing the port of the postgres DB
docker run -it -p 5432:5432 cod
