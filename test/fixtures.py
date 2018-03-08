import pytest
import pg
import os

@pytest.fixture
def db():
    """A test fixture that has a test database with the same shape as the prod db"""
    db = pg.DB(dbname="test", host="localhost")

    # Finds the path to the data file
    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]
    data_path  = "data/test.sql"
    abs_file_path = os.path.join(script_dir, data_path)

    with open(abs_file_path) as test_data:
        db.query(test_data.read(-1))
    return db