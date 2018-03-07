"""database utils"""

import pg
from common.misc import system_to_id


def get_civ(db, key):
    """
    Returns the id of the civilization with the given key
    :param db: the database to check
    :param key: the key to lookup
    :return: the id of the corresponding civilization, or None
    """
    try:
        return db.get("civilizations", key, "key")["id"]
    except pg.DatabaseError as _:
        return None


def set_civ_key(db, civ_id, new_key):
    """
    Sets the key of a given civilization.
    :param db: the database to update
    :param civ_id: the civ to update
    :param new_key: the new key
    :return: True if successfull, False otherwise
    """
    try:
        db.update("civilizations", {"id": civ_id}, key=new_key)
        return True
    except pg.DatabaseError as _:
        return False


def civ_systems(db, key):
    """
    Returns the IDs of all systems that belong to the civilization with the given key.
    :param db: the database to check
    :param key: the key of the civilization checking
    :return: the list of all the systems related
    """
    civ_id = get_civ(db, key)
    if civ_id is None:
        return []

    result = db.query_formatted("SELECT * FROM systems WHERE controller = %s",
                                (civ_id,))
    dictresult = result.dictresult()
    return [elem["id"] for elem in dictresult]


def civ_owns(db, civ_id, system):
    """
    Does the given civilization own the given system?
    :param db: the database to check
    :param civ_id: the civilization to check
    :param system: the system to check
    :return:
    """
    result = db.query_formatted(
        "SELECT * FROM systems WHERE id = %s AND controller = %s",
        (system_to_id(db, system), civ_id))
    answer = result.dictresult()
    return bool(answer)


def civ_owns_by_key(db, key, system):
    return civ_owns(db, get_civ(db, key), system)


def civ_can_see(db, key, system):
    return civ_owns_by_key(db, key, system) or civ_has_ships_at(db, key, system)


def civ_has_ships_at(db, key, system):
    result = db.query_formatted("SELECT * FROM ships WHERE location = %s AND flag = %s",
                                (system, get_civ(db, key)),)
    return len(result.dictresult())