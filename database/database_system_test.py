from test.fixtures import db
from database.key_access import *


def test_get_system(db):
    system3 = get_system_info(db, "key3", 3)
    assert system3 == get_system_info(db, "key3", "venus")
    assert system3["id"] == 3
    assert system3["controller"] == 3


def test_get_system_by_name(db):
    assert get_system_info(db, "key3", "venus")["id"] == 3
