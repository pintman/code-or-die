from civilization.database import *



def test_get_civ(db):
    assert get_civ(db, "key1") == 1
    assert get_civ(db, "key2") == 2
    assert get_civ(db, "key3") == 3


def test_set_civ_key(db):
    result = db.query("SELECT * FROM civilizations WHERE key='more keys'").dictresult()
    assert len(result) == 0

    assert set_civ_key(db, 1, "a new key")
    assert set_civ_key(db, 1, "more keys")

    result = db.query("SELECT * FROM civilizations WHERE key='more keys'").dictresult()
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_civ_systems(db):
    assert civ_systems(db, "key1") == [1, 4]
    assert civ_systems(db, "key2") == [2]
    assert civ_systems(db, "key3") == [3]


def test_civ_owns(db):
    assert civ_owns(db, 1, 1)
    assert not civ_owns(db, 1, 2)
    assert not civ_owns(db, 1, 3)
    assert civ_owns(db, 1, 4)

