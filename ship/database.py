import pg
from civilization.database import get_civ


def get_ship(db, key, ship):
    ship = db.query_formatted("SELECT * FROM ships WHERE id = %s AND flag = %s",
                              (ship, get_civ(db, key))
                              ).dictresult()
    if not ship:
        return None
    else:
        return ship[0]


def get_ship_orders(db, key, ship):
    ship = get_ship(db, key, ship)
    if ship is None:
        return None
    else:
        return ship["orders"]


def set_ship_orders(db, key, ship, orders):
    db.query_formatted("UPDATE ships SET orders = %s WHERE id = %s AND flag = %s",
                       (pg.jsonencode(orders), ship, get_civ(db, key)))
