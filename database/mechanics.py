from database.common import *
import pg

def get_transits(db):
    """
    Gets all the transits currently in progress in the database.
    :param db:
    :return:
    """
    return db.query("SELECT * FROM transit").dictresult()


def get_route_distance(db, system1, system2):
    id1 = system_to_id(db, system1)
    id2 = system_to_id(db, system2)
    result = db.query_formatted(
        "SELECT distance FROM routes WHERE origin = %s AND destination = %s",
        (min(id1, id2), max(id1, id2)))
    result = result_to_first_element(result)
    if result is None:
        return None
    else:
        return result["distance"]


def remove_transit(db, id, type):
    if type == "beam_transit":
        db.query_formatted("DELETE FROM beam_transit WHERE id = %s", (id,))
    if type == "ftl_transit":
        db.query_formatted("DELETE FROM ftl_transit WHERE id = %s", (id,))


def set_ship_location(db, ship_id, new_location):
    db.query_formatted("UPDATE ships SET location = %s WHERE id = %s",
                       (new_location, ship_id))

def set_ship_orders(db, ship, orders):
    db.query_formatted("UPDATE ships SET orders = %s WHERE id = %s",
                       (pg.jsonencode(orders), ship))