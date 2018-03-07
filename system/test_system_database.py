from common.test import db
from system.database import *


def test_get_system(db):
    system3 = get_system(db, "key3", 3)
    assert system3 == get_system(db, "key3", "venus")
    assert system3["id"] == 3
    assert system3["orders"] == []
    assert system3["controller"] == 3


def test_get_system_by_name(db):
    assert get_system(db, "key3", "venus")["id"] == 3
