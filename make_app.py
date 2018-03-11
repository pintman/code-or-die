"""Create the flask application, with parameters to allow for easier testing"""
from flask import Flask
import pg
import os


def make_app(test=False):
    app = Flask(__name__)
    if test:
        app.db = build_local_database("test")
    else:
        app.db = build_local_database()

    return app


def build_local_database(dbname=None):
    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]
    secrets_file = "secrets.txt"
    abs_file_path = os.path.join(script_dir, secrets_file)

    with open(abs_file_path) as secrets:
        if dbname:
            secrets.readline()
        else:
            dbname = secrets.readline().replace("\n", "")
        host = secrets.readline().replace("\n", "")
        port = int(secrets.readline())

    db = pg.DB(dbname=dbname,
               host=host,
               port=port)

    with open(script_dir + "/database/layout.sql") as layout:
        db.query(layout.read())
    return db
