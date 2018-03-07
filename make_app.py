"""Create the flask application, with parameters to allow for easier testing"""
from flask import Flask
import pg


def make_app(database=None):
    app = Flask(__name__)

    app.db = database or build_local_database()


def build_local_database():
    with open("secrets.txt") as secrets:
        dbname = secrets.readline().splitlines()[0]
        host = secrets.readline().splitlines()[0]
        port = int(secrets.readline())

    db = pg.DB(dbname=dbname,
               host=host,
               port=port)
    return db
