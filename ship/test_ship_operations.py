from common.test import db
from ship.operations import *


def test_sending_ship_orders(db):
    order1 = {"order": "attack", "civ": ["mars"]}
    order2 = {"order": "sieze"}
    order3 = {"order": "suicide"}

    assert get_orders_from_ship(db, "key1", 1) == []
    add_order_to_ship(db, "key1", 1, order1)
    assert get_orders_from_ship(db, "key1", 1) == [order1]

    add_order_to_ship(db, "key1", 1, order2)
    assert get_orders_from_ship(db, "key1", 1) == [order1, order2]

    add_order_to_ship(db, "key1", 1, order3)
    assert get_orders_from_ship(db, "key1", 1) == [order1, order2, order3]

    remove_order_from_ship(db, "key1", 1, 1)
    assert get_orders_from_ship(db, "key1", 1) == [order1, order3]

    remove_all_orders_from_ship(db, "key1", 1)
    assert get_orders_from_ship(db, "key1", 1) == []


def test_get_ships(db):
    key1ships = get_ships(db, "key1")
    expected1 = [{"id": 1, "shipyard": 1, "location": 1, "flag": 1, "orders": []},
                {"id": 2, "shipyard": 1, "location": 1, "flag": 1, "orders": []},
                {"id": 3, "shipyard": 1, "location": 4, "flag": 1, "orders": []}]
    assert key1ships == expected1

    key3ships = get_ships(db, "key3")
    expected3 = [{"id": 4, "shipyard": 3, "location": 4, "flag": 3, "orders": []}]
    assert key3ships == expected3


    assert get_ships(db, "no such key") == None


def test_get_ship_info(db):
    assert get_ship_info(db, "key1", 1) == {"id": 1, "shipyard": 1, "location": 1, "flag": 1, "orders": []}
    assert get_ship_info(db, "key1", 4) == None
