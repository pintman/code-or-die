from database.common import set_system_orders, get_civ_by_name

def process_system_orders(db):
    systems = db.query("SELECT id, production, controller, orders FROM systems").dictresult()
    _process_unit_production(db, systems)
    _process_beam_motivator_toggles(db, systems)
    _process_abandon_system(db, systems)


def _process_unit_production(db, systems):
    for system in systems:
        system_id = system['id']
        production = system["production"]
        orders = system["orders"]
        orders_to_keep = []
        for order in orders:
            if order["order"] != "build":
                orders_to_keep.append(order)
            else:
                if not "civ" in order:
                    return
                civ = get_civ_by_name(db, order["civ"])
                if not civ:
                    return
                count = order["count"]
                if count > production:
                    orders_to_keep.append(order)
                else:
                    db.query_formatted("INSERT INTO ships (shipyard, location, flag)"
                                       "VALUES (%s, %s, %s)",
                                       (system_id, system_id, civ))
                break
        set_system_orders(db, system_id, orders_to_keep)


def _process_beam_motivator_toggles(db, systems):
    # TODO add beam burnout, until then this is useless
    pass


def _process_abandon_system(db, systems):
    # TODO why would anyone want to abandon a system?
    pass
