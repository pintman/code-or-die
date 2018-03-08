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


def test_can_send_valid_orders(db):
    order_attack_one = {"order": "attack", "civ": ["mars"]}
    order_attack_multiple = {"order": "attack", "civ": ["mars", "earth"]}
    order_beam = {"order": "beam", "destination": 4, "tuning": 13}
    order_ftl = {"order": "ftl", "destination": 4}
    order_sieze = {"order": "sieze"}
    order_suicide = {"order": "suicide"}

    orders = [order_attack_one,
              order_attack_multiple,
              order_beam,
              order_ftl,
              order_sieze,
              order_suicide]

    try:
        for order in orders:
            add_order_to_ship(db, "key1", 1, order)
        success = True
    except:
        success = False

    assert success


def test_cant_send_invalid_orders(db):
    order_attack_none = {"order": "attack", "civ": []}
    order_not_in_list = {"order": "foo"}
    order_beam_without_destination = {"order": "beam", "tuning": 213}
    order_beam_without_tuning = {"order": "beam", "destination": 4}
    order_beam_without_either = {"order": "beam"}

    orders = [order_attack_none,
              order_not_in_list,
              order_beam_without_destination,
              order_beam_without_tuning,
              order_beam_without_either]

    for order in orders:
        try:
            add_order_to_ship(db, "key1", 1, order)
            assert order is False
        except NotImplementedError as e:
            assert True


def test_get_ships(db):
    key1ships = get_ships(db, "key1")
    expected1 = [{"id": 1, "shipyard": 1, "location": 1, "flag": 1, "orders": []},
                 {"id": 2, "shipyard": 1, "location": 1, "flag": 1, "orders": []},
                 {"id": 3, "shipyard": 1, "location": 4, "flag": 1, "orders": []}]
    assert key1ships == expected1

    key3ships = get_ships(db, "key3")
    expected3 = [{"id": 4, "shipyard": 3, "location": 4, "flag": 3, "orders": []}]
    assert key3ships == expected3

    assert get_ships(db, "no such key") is None


def test_get_ship_info(db):
    assert get_ship_info(db, "key1", 1) == {"id": 1, "shipyard": 1, "location": 1, "flag": 1, "orders": []}
    assert get_ship_info(db, "key1", 4) is None
