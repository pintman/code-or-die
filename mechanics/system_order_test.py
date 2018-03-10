from test.fixtures import db
from mechanics.system_order import process_system_orders
from database.common import ships_at_system
import pg

def set_orders(db, system_id, orders):
    db.query_formatted("UPDATE systems SET orders = %s WHERE id = %s",
                       (pg.jsonencode(orders), system_id))

def test_unit_production(db):
    assert len(ships_at_system(db, 1)[1]) == 2
    set_orders(db, 1, [{"order": "build", "count": 1, "team": 1}])
    process_system_orders(db)
    assert len(ships_at_system(db, 1)[1]) == 3