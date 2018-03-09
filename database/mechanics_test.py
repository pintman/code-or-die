from database.mechanics import *
from test.fixtures import db

def test_get_route_distance(db):
    assert get_route_distance(db, 1, 4) == 1
    assert get_route_distance(db, 2, 4) == 2
    assert get_route_distance(db, 3, 4) == 5
