def system_to_id(db, system):
    """What is the id of the given system? Accepts int-able strings,
    or converts a name into the id

    :param db: the db to check
    :param system: a string representing the system's id or name
    :return: the id of the system
    """
    try:
        return int(system)
    except ValueError as e:
        for entry in get_all_system_convenience_names(db):
            if system in entry["names"]:
                return int(entry["id"])
        return None


def get_all_system_convenience_names(db):
    """
    Returns the convenience names of all systems

    :param db: the db to check
    :return: an array of dictionaries, with key as id and value being the names of the system
    """
    return db.query("SELECT id, names FROM systems").dictresult()


def result_to_first_element(result):
    """Turns a database query result into a single element

    :param result: the result to use
    :return: the first element, or none if it is empty
    """
    d = result.dictresult()
    if len(d) == 0:
        return None
    else:
        return d[0]


def army_sizes_at_system(db, id):
    """Produces the list of all civilizations with at least one ship, and how many
    ships they own.

    :param db: the database to check
    :param id: the id of the system to find
    :return: the list
    """
    out = {}
    for civ_id, ships in ships_at_system(db, id).items():
        out[get_civ_name(db, civ_id)] = len(ships)
    return out


def ships_at_system(db, system_id):
    """Creates a list of the ships at each system, as a dictionary from
    civilization ids to a list of ship id's

    :param db: the database to use
    :param system_id: the id of the system to check
    :return: the civilizations at the system, and which ships each one owns
    """
    ships = db.query_formatted("SELECT id, flag FROM ships WHERE location = %s", (system_id,)
                               ).dictresult()
    armies = {}
    for ship in ships:
        flag = ship["flag"]
        id = ship["id"]

        if flag in armies:
            armies[flag].append(id)
        else:
            armies[flag] = [id]
    return armies


def get_civ_name(db, civ_id):
    """Returns the name of the civ with the given id.

    :param db: the database to search
    :param civ_id: the civ to find
    :return: the name of the civ
    """
    result = db.query_formatted("SELECT name FROM civilizations WHERE id = %s", (civ_id,))
    return result_to_first_element(result)["name"]


def routes_from(db, id):
    """Returns all routes from the given system.

    :param db: the database to check
    :param id: the id of the system
    :return: the routes from the system
    """
    routes = db.query_formatted("SELECT * FROM routes WHERE destination = %s OR origin = %s",
                                (id, id)).dictresult()
    out = []
    for route in routes:
        destination = [route["destination"] if route["origin"] == id else route["origin"]]
        distance = route["distance"]
        out.append({"destination": destination, "distance": distance})
    return out


def get_system(db, system):
    result = db.query_formatted("SELECT * FROM systems WHERE id = %s",
                                (system_to_id(db, system),))
    return result_to_first_element(result)
