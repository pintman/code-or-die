"""Functions related to system management"""

from civilization.database import get_civ, civ_owns


def system_info(db, key, system):
    """
    Returns all available information about a system, for the civilization associated
    with the given key.
    :param db: the database to search
    :param key: the key of the civilization making the query
    :param system: the system to get information about
    :return: all available information about the system, or None if there is none
    """
    system_id = _system_to_id(db, system)
    civ_id = get_civ(db, key)
    if system_id is None or civ_id is None:
        return None

    if civ_owns(db, civ_id, system_id):
        return _get_system_info(db, system_id)
    else:
        return None


def _get_system_info(db, system_id):
    result = db.query_formatted("SELECT * FROM systems WHERE id = %s", (system_id,))
    try:
        return result.dictresult()[0]
    except IndexError as e:
        return None


def system_id_from_name(db, name):
    """
    Returns the id of the system with the given name.
    :param db: the database to search
    :param name: the name of the system to lookup
    :return: the id of the corresponding system
    """
    result = db.query_formatted("SELECT id FROM systems WHERE %s = ANY(names)", (name,))
    try:
        return result.dictresult()[0]["id"]
    except IndexError or KeyError as e:
        return None


def get_system_convenience_names(db, system_id):
    """
    Returns the list of all names associated with the system with the given id.
    :param db: the database to search
    :param system_id: the system to check
    :return: the corresponding names
    """
    result = db.query_formatted("SELECT names FROM systems WHERE id = %s", (system_id,))

    try:
        return result.dictresult()[0]["names"]
    except IndexError as e:
        return None


def add_convenience_name(db, system_id, name):
    """
    Adds the given name to the names of the system with the given id
    :param db: the database to use
    :param system_id: the system that is getting the name
    :param name: the name to add
    :return: True if successful, False otherwise
    """
    db.query_formatted(
        "UPDATE systems SET names = array_append(names, %s) WHERE id = %s  ",
        (name, system_id))


def system_orders(db, key, system):
    """
    Returns all the orders in a given system from the civilization making the request.
    :param db: the database to use
    :param key: the key of the civilization
    :param system: the system to check
    :return: the list of orders in the system
    """
    result = db.query_formatted(
        "SELECT orders FROM systems WHERE id = %s AND CONTROLLER = %s",
        (_system_to_id(db, system), get_civ(db, key)))
    try:
        return result.dictresult()[0]["orders"]
    except:
        return None


def add_order_to_system(db, key, system, order):
    """
    Adds the given order to the given system.
    :param db: the database to modify
    :param key: the key of the civilization
    :param system: the system to add the order to
    :param order: the order
    :return: the new list of orders at the given system
    """
    result = db.query_formatted("db")


def remove_all_orders_from_system(db, key, system_id):
    """
    Removes all the orders in a given system from the civilization making the request.
    :param db: the database to use
    :param key: the key of the civilization
    :param system_id: the id of the system
    :return: the list of orders that used to be in the system
    """
    pass


def remove_order_from_system(db, key, system_id, order_index):
    """
    Removes the given order from the given system.
    :param db: the database to update
    :param key: the civilization making the request
    :param system_id: the system to update
    :param order_index: the
    :return: the removed order
    """
    pass


def _system_to_id(db, system):
    """
    Converts the given system, as either a name or a StringN id, to an integer id.
    :param system: the system specification
    :return: the id of the system, or None if given a system that doesn't exist
    """
    try:
        system_id = int(system)
    except ValueError as e:
        system_id = system_id_from_name(db, system)
    return system_id
