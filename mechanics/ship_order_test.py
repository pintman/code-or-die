from test.fixtures import db
from mechanics.ship_order import process_ship_orders
import pg


def add_order(db, ship_id, order):
    orders = db.get("ships", ship_id)["orders"]
    orders.append(order)
    db.query_formatted("UPDATE ships SET orders = %s WHERE id = %s",
                       (pg.jsonencode(orders), ship_id))


def test_ftl_transit_processing(db):
    def transits():
        return db.query("SELECT * FROM transit").dictresult()

    assert len(transits()) == 0
    add_order(db, 1, {"order": "ftl_transit", "origin": 1, "destination": 4})
    assert len(transits()) == 0

    process_ship_orders(db)

    assert len(transits()) == 1
    assert transits()[0]["ship"] == 1
    assert transits()[0]["destination"] == 4

def test_beam_transit_processing(db):
    def transits():
        return db.query("SELECT * FROM transit").dictresult()

    assert len(transits()) == 0
    add_order(db, 1, {"order":"beam_transit", "origin": 1, "destination": 4, "tuning": 0})
    assert len(transits()) == 0

    process_ship_orders(db)
    assert len(transits()) == 1
    assert transits()[0]["ship"] == 1


def test_suicide_processing(db):
    def ships():
        return db.query("SELECT * FROM ships").dictresult()

    assert len(ships()) == 4
    add_order(db, 1, {"order": "suicide"})
    assert len(ships()) == 4
    process_ship_orders(db)
    assert len(ships()) == 3

def test_seizing_systems(db):
    from database.key_access import civ_systems

    assert len(civ_systems(db, "key1")) == 2

    add_order(db, 4, {"order": "seize"})
    process_ship_orders(db)

    assert len(civ_systems(db, "key1")) == 1
