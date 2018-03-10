import pg
from database.common import *


def get_civ(db, key):
    """Returns the id of the civilization with the given key

    :param db: the database to check
    :param key: the key to lookup
    :return: the id of the corresponding civilization, or None
    """
    try:
        return db.get("civilizations", key, "key")["id"]
    except pg.DatabaseError as _:
        return None


def set_civ_key(db, civ_id, new_key):
    """Sets the key of a given civilization.

    :param db: the database to update
    :param civ_id: the civ to update
    :param new_key: the new key
    :return: True if successful, False otherwise
    """
    try:
        db.update("civilizations", {"id": civ_id}, key=new_key)
        return True
    except pg.DatabaseError as _:
        return False


def civ_systems(db, key):
    """Returns the IDs of all systems that belong to the civilization with the given key.

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
    """Does the given civilization own the given system?

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
    """Does the civ with the given key own the given system?

    :param db: the database to use
    :param key: the key to use
    :param system: the system to check
    :return: whether the civ owns it
    """
    return civ_owns(db, get_civ(db, key), system)


def civ_can_see(db, key, system):
    """Can the given civ see the given system?

    :param db: the database to use
    :param key: the key to use
    :param system: the system to check
    :return: whether they can
    """
    return civ_owns_by_key(db, key, system) or civ_has_ships_at(db, key, system)


def civ_has_ships_at(db, key, system):
    """Does the given civ have ships at the given system>?

    :param db: the database to use
    :param key: the key of the civilization to check
    :param system: the system
    :return: whether they do
    """
    result = db.query_formatted("SELECT * FROM ships WHERE location = %s AND flag = %s",
                                (system, get_civ(db, key)), )
    return len(result.dictresult())


def get_ship_for_civ(db, key, ship):
    """Gets information on the ship by the given id, if the civ for the given key can see it.

    :param db: the database to check
    :param key: the key of the civilzation checking
    :param ship: the ship to check
    :return: information, if the ship exists and can be seen by the given civ, None otherwise
    """
    ship = db.query_formatted("SELECT * FROM ships WHERE id = %s AND flag = %s",
                              (ship, get_civ(db, key))
                              ).dictresult()
    if not ship:
        return None
    else:
        return ship[0]


def get_ships_for_civ(db, key):
    """Gets all the ships owned by the given civilization.

    :param db: the database to check
    :param key: the key to the civilization
    :return: all the ships
    """
    civ = get_civ(db, key)
    if not civ:
        return None

    ships = db.query_formatted("SELECT * FROM ships WHERE flag = %s",
                               (civ,)
                               ).dictresult()
    if not ships:
        return []
    else:
        return ships


def get_ship_orders(db, key, ship):
    """Produces the orders for the given ship.

    :param db: the database to check
    :param key: the key of the civilization looking
    :param ship: the ship to check
    :return: the orders, if the ship exists and the civ can see it
    """
    ship = get_ship_for_civ(db, key, ship)
    if ship is None:
        return None
    else:
        return ship["orders"]


def set_ship_orders(db, key, ship, orders):
    """Sets the orders for the given ship.

    :param db: the database to update
    :param key: the key of the civilization making changes
    :param ship: the ship to be updated
    :param orders: the new list of orders
    :return: None
    """
    db.query_formatted("UPDATE ships SET orders = %s WHERE id = %s AND flag = %s",
                       (pg.jsonencode(orders), ship, get_civ(db, key)))
    return True


def get_system_info(db, key, system):
    """Gets the system with the given id or name, if the civilization can see it

    :param db: the database to check
    :param key: the key to use
    :param system: the system to get
    :return: The system, or None if the system doesn't exist or can't be seen
    """
    system_id = system_to_id(db, system)
    if system_id is None or not civ_can_see(db, key, system_id):
        return None

    system = _get_system_by_id(db, system_id)

    system_names = system["names"]
    controller_id = system["controller"]
    production = system["production"]
    armies = army_sizes_at_system(db, system_id)
    routes = routes_from(db, system_id)
    if civ_owns(db, get_civ(db, key), system_id):
        owner_information = {
            "tuning-parameters": system["historical_tuning"],
            "tuning_destinations": system["tuning_destinations"]
        }
    else:
        owner_information = None

    return {
        "id": system_id,
        "names": system_names,
        "controller": controller_id,
        "production": production,
        "armies": armies,
        "routes": routes,
        "owner-information": owner_information
    }

def _get_system_by_id(db, system_id):
    """Gets the system with the given id.

    :param db: the database to search
    :param system_id: the id of the system to find
    :return: the system, or None if there isn't one
    """
    result = db.query_formatted("SELECT * FROM systems WHERE id = %s", (system_id,))
    return result_to_first_element(result)


def _get_system_by_name(db, name):
    """Gets the system with the given name.

    :param db: the database to search
    :param name: the name of the system to find
    :return: the system, or None if there isn't one
    """
    result = db.query_formatted("SELECT * FROM systems WHERE %s = ANY(names)", (name,))
    return result_to_first_element(result)



def get_system_orders(db, key, system):
    """Gets the orders for the given system.

    :param db: the database to check
    :param key: the key of the civilization asking
    :param system: the system to check
    :return: the orders for the system, or None if there is no system with the given name/id or you aren't allowed
    to see it
    """
    if not civ_owns_by_key(db, key, system):
        return None

    sys = get_system(db, system)
    if sys is None:
        return None
    else:
        return sys["orders"]


def set_system_orders(db, key, system, orders):
    """Sets the orders for a given system.

    :param db: the database to update
    :param key: the key to change
    :param system: the system to set
    :param orders: the new set of orders
    :return: the old set of orders
    """
    if not civ_owns_by_key(db, key, system):
        return None

    sys = get_system(db, system)
    if sys is None:
        return None
    db.query_formatted("UPDATE systems SET orders = %s WHERE id = %s",
                       (pg.jsonencode(orders), sys["id"]))
    return sys['orders']
