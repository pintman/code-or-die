"""Create the flask application, with parameters to allow for easier testing"""
from flask import Flask
import pg
import os


def make_app(test=False):
    app = Flask(__name__)

    if test:
        app.db_config = local_database("test")
    else:
        app.db_config = local_database()

    def make_db(**config):
        return lambda: pg.DB(**config)

    app.db_conn = make_db(**app.db_config)

    db = app.db_conn()

    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]

    with open(script_dir + "/database/layout.sql") as layout:
        db.query(layout.read())

    return app


def local_database(dbname=None):
    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]

    secrets_file = "secrets.txt"
    abs_file_path = os.path.join(script_dir, secrets_file)
    def next():
        return secrets.readline().replace("\n", "")

    with open(abs_file_path) as secrets:
        if dbname:
            next()
        else:
            dbname = next()
        host = next()
        port = int(next())
        user = next()
        password = next()

    return dict(dbname=dbname,
                host=host,
                port=port,
                user=user,
                passwd=password)
