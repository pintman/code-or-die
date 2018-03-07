from database.test_common import db
import pg
from system import *


def test_system_info(db):
    # Right permissions
    assert system_info(db, "key1", 1) is not None
    assert system_info(db, "key1", 2) is None
    assert system_info(db, "key1", 3) is None
    assert system_info(db, "key1", 4) is not None

    db.query("INSERT INTO systems VALUES (5, 'active', 'transit', 1, 1, 0, '{\"name1\", \"name2\"}')")
    # Right results
    assert system_info(db, "key1", 5) == {
        "id": 5,
        "status": "active",
        "mode": "transit",
        "controller": 1,
        "production": 1,
        "tuning": 0,
        "names": ["name1", "name2"],
        "orders": []
    }


def test_system_id_from_name(db):
    assert system_id_from_name(db, "home") == 3
    assert system_id_from_name(db, "venus") == 3
    assert system_id_from_name(db, "war") == 4


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
    assert system_orders(db, "key1", 1) == []
    add_order_to_system(db, "key1", 1, {"order", "repair-mode"})
    assert system_orders(db, "key1", 1) == [{"order": "repair-mode"}]


def test_remove_all_orders_from_system(db):
    pass


def test_remove_order_from_system(db):
    pass
