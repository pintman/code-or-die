"""Functions related to system management"""

from database.key_access import *


def system_info(db, key, system):
    """
    Returns all available information about a system, for the civilization associated
    with the given key.
    :param db: the database to search
    :param key: the key of the civilization making the query
    :param system: the system to get information about
    :return: all available information about the system, or None if there is none
    """
    return get_system_info(db, key, system)


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
    return get_system_orders(db, key, system)


def add_order_to_system(db, key, system, order):
    """
    Adds the given order to the given system.
    :param db: the database to modify
    :param key: the key of the civilization
    :param system: the system to add the order to
    :param order: the order
    :return: the new list of orders at the given system, or None if you can't add that order
    """
    new_orders = get_system_orders(db, key, system) or []
    new_orders.append(order)
    set_system_orders_by_key(db, key, system, new_orders)
    return new_orders


def remove_all_orders_from_system(db, key, system):
    """
    Removes all the orders in a given system from the civilization making the request.
    :param db: the database to use
    :param key: the key of the civilization
    :param system: the id of the system
    :return: the list of orders that used to be in the system
    """
    return set_system_orders_by_key(db, key, system, [])


def remove_order_from_system(db, key, system, order_index):
    """
    Removes the given order from the given system.
    :param db: the database to update
    :param key: the civilization making the request
    :param system: the system to update
    :param order_index: the
    :return: the removed order
    """
    orders = get_system_orders(db, key, system)
    orders.remove(orders[order_index])
    set_system_orders_by_key(db, key, system, orders)
