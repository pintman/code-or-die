from common.test import db
from ship.database import *


def test_get_ship(db):
    ship = get_ship(db, "key1", 1)
    assert ship["id"] == 1