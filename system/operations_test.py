from test.fixtures import db
from system.operations import *

def test_system_info(db):
    # Right permissions
    assert system_info(db, "key1", 1) is not None
    assert system_info(db, "key1", 2) is None
    assert system_info(db, "key1", 3) is None
    assert system_info(db, "key1", 4) is not None


def test_get_system_convenience_names(db):
    assert get_system_convenience_names(db, 1) == []
    assert get_system_convenience_names(db, 4) == ["war"]
    assert get_system_convenience_names(db, 3) == ["home", "venus"]


def test_get_system_convenience_names_nonexistent_system(db):
    assert get_system_convenience_names(db, 5) is None


def test_add_convenience_name(db):
    assert get_system_convenience_names(db, 1) == []
    assert add_convenience_name(db, 1, "name") is None
    assert get_system_convenience_names(db, 1) == ["name"]


def test_add_convenience_name_on_nonexistent_system(db):
    assert add_convenience_name(db, 5, "name") is None
    assert add_convenience_name(db, 6, "name") is None


def test_system_orders(db):
    assert system_orders(db, "key1", 1) == []
    assert system_orders(db, "key3", 3) == []

    import json
    order = [{"order": "repair-mode"}]
    db.query_formatted("INSERT INTO systems (id, status, mode, controller, production, tuning, names, orders) "
                       "VALUES (5, 'active', 'transit', 1, 1, 0, '{}', %s)", (json.dumps(order),))
    assert system_orders(db, "key1", 5) == order


def test_system_orders_is_none_when_no_vision(db):
    assert system_orders(db, "key1", 3) is None
    assert system_orders(db, "key3", 1) is None


def test_system_orders_is_none_when_no_system(db):
    assert system_orders(db, "key1", 100) is None
    assert system_orders(db, "key1", "no system with this name") is None


def test_add_system_orders(db):
    order = {"order": "repair-mode"}
    assert system_orders(db, "key1", 1) == []
    assert add_order_to_system(db, "key1", 1, order) == [order]
    assert system_orders(db, "key1", 1) == [order]

def test_set_system_orders(db):
    order = {"order": "repair-mode"}
    assert get_system_orders(db, "key1", 1) == []
    set_system_orders_by_key(db, "key1", 1, [order])
    assert get_system_orders(db, "key1", 1) == [order]


def test_get_system_orders(db):
    assert get_system_orders(db, "key1", 1) == []

def test_remove_all_orders_from_system(db):
    order = {"order": "repair-mode"}
    assert get_system_orders(db, "key1", 1) == []
    set_system_orders_by_key(db, "key1", 1, [order])
    assert get_system_orders(db, "key1", 1) == [order]
    remove_all_orders_from_system(db, "key1", 1)
    assert get_system_orders(db, "key1", 1) == []


def test_remove_order_from_system(db):
    order1 = {"order": "repair-mode"}
    order2 = {"order": "transit-mode"}

    assert get_system_orders(db, "key1", 1) == []
    set_system_orders_by_key(db, "key1", 1, [order1, order2])
    assert get_system_orders(db, "key1", 1) == [order1, order2]
    remove_order_from_system(db, "key1", 1, 0)
    assert get_system_orders(db, "key1", 1) == [order2]


