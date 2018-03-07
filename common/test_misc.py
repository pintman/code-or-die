from common.test import db
from common.misc import system_to_id, get_all_system_convenience_names

def test_system_to_id(db):
    assert system_to_id(db, 1) == 1
    assert system_to_id(db, 3) == 3
    assert system_to_id(db, "venus") == 3
    assert system_to_id(db, "war") == 4
