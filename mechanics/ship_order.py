from database.mechanics import set_ship_orders


def process_ship_orders(db):
    """Processes all the orders from ships, adding transits to the right table,
    killing ships told to suicide, and seizing systems. Attacks are NOT handled here.

    :param db: the database to process
    """
    ship_orders = db.query("SELECT (id, orders) FROM ships;").dictresult()
    ship_orders_with_flag = db.query(
        "SELECT (id, flag, location, orders) FROM ships;").dictresult()

    _add_all_transits(db, ship_orders)
    _do_all_suicides(db, ship_orders)
    _seize_systems(db, ship_orders_with_flag)


def _add_all_transits(db, ship_order_pairs):
    for ship_and_orders in ship_order_pairs:
        ship_id = ship_and_orders["id"]
        orders = ship_and_orders["orders"]
        orders_not_processed = []
        for order in orders:
            if order["order"] == "ftl_transit":
                _add_ftl_transit(db, ship_id, order)
            elif order["order"] == "beam_transit":
                _add_beam_transit(db, ship_id, order)
            else:
                orders_not_processed.append(order)
        set_ship_orders(db, ship_id, orders_not_processed)


def _add_ftl_transit(db, ship_id, order):
    db.query_formatted("INSERT INTO ftl_transit (ship, origin, destination)"
                       "VALUES (%s, %s, %s)",
                       (ship_id, order["origin"], order["destination"]))


def _add_beam_transit(db, ship_id, order):
    db.query_formatted("INSERT INTO beam_transit (ship, origin, destination, tuning)"
                       "VALUES (%s, %s, %s, %s)",
                       (ship_id, order["origin"], order["destination"], order["tuning"]))


def _do_all_suicides(db, ship_order_pairs):
    for ship_and_orders in ship_order_pairs:
        ship = ship_and_orders["id"]
        orders = ship_and_orders["orders"]

        for order in orders:
            if order["order"] == "suicide":
                db.delete("ships", id=ship)


def _seize_systems(db, ships_info):
    system_seize_attempts_by_civ = {}
    orders_not_processed = []

    for ship_info in ships_info:
        ship_id = ship_info["id"]
        orders = ship_info["orders"]
        location = ship_info["location"]
        civ = ship_info["flag"]
        for order in orders:
            if order["order"] == "seize":
                if not location in system_seize_attempts_by_civ:
                    system_seize_attempts_by_civ[location] = {}
                seize_attempts = system_seize_attempts_by_civ[location]

                if civ in seize_attempts:
                    seize_attempts[civ] += 1
                else:
                    seize_attempts[civ] = 1
            else:
                orders_not_processed.append(order)
        set_ship_orders(db, ship_id, orders_not_processed)

    for system, seize_attempts_list in system_seize_attempts_by_civ.items():
        strongest_civ, strength = seize_attempts_list.popitem()
        for civ, cur_strength in seize_attempts_list:
            if cur_strength > strength:
                strongest_civ = civ
                strength = cur_strength

        db.query_formatted("UPDATE systems SET controller = %s WHERE id = %s",
                           (strongest_civ, system))
