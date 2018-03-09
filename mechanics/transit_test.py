from test.fixtures import db
from database.common import *
from database.key_access import get_ship_for_civ
from mechanics.transit import *


def test_transit_is_done(db):
    transit1 = {"id": 1, "ship": 1, "origin": 1, "destination": 4, "time": 13.3, "type": "ftl_transit"}
    assert not transit_is_done(db, transit1, 13)
    assert not transit_is_done(db, transit1, 14.2)
    assert transit_is_done(db, transit1, 14.4)

    transit2 = {"id": 1, "ship": 2, "origin": 2, "destination": 4,
                "time": 13.3, "type": "beam_transit", "tuning": 13}
    assert transit_is_done(db, transit2, 14)

    transit3 = {"id": 1, "ship": 2, "origin": 4, "destination": 2,
                "time": 13.3, "type": "beam_transit", "tuning": 13}
    assert transit_is_done(db, transit2, 14)


def test_travel_time(db):
    assert travel_time(db, {"origin": 1, "destination": 4}) == 1


def test_finish_transit(db):
    pass
