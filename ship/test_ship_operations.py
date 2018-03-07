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
    pass


def test_get_ship_info(db):
    pass
