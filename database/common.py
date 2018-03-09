def system_to_id(db, system):
    try:
        return int(system)
    except ValueError as e:
        for entry in get_all_system_convenience_names(db):
            if system in entry["names"]:
                return entry["id"]
        return None


def get_all_system_convenience_names(db):
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
