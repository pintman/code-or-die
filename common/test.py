import pytest
import pg

@pytest.fixture
def db():
    db = pg.DB(dbname="test", host="localhost")
    with open("common/test_data.sql") as test_data:
        db.query(test_data.read(-1))
    return db