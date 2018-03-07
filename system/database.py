from civilization.database import civ_can_see
from common.misc import system_to_id
import pg


def get_system(db, key, system):
    result = get_system_by_id(db, system_to_id(db, system))

    try:
        system_info = result[0]
        if civ_can_see(db, key, system_info['id']):
            return system_info
        else:
            return None
    except IndexError as e:
        return None


def get_system_by_id(db, system_id):
    result = db.query_formatted("SELECT * FROM systems WHERE id = %s", (system_id,))
    return result.dictresult()


def get_system_by_name(db, name):
    result = db.query_formatted("SELECT * FROM systems WHERE %s = ANY(names)", (name,))
    return result.dictresult()


def get_system_orders(db, key, system):
    sys = get_system(db, key, system)
    if sys is None:
        return None
    else:
        return sys["orders"]


def set_system_orders(db, key, system, orders):
    sys = get_system(db, key, system)
    if sys is None:
        return None
    db.query_formatted("UPDATE systems SET orders = %s WHERE id = %s",
                       (pg.jsonencode(orders), sys["id"]))
    return sys['orders']
