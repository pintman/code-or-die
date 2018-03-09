from test.fixtures import db
from database.key_access import *


def test_get_ship(db):
    ship = get_ship_for_civ(db, "key1", 1)
    assert ship["id"] == 1
