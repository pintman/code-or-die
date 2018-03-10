from database.common import ships_at_system
import random


def process_attacks(db):
    systems = [system["id"] for system in db.query("SELECT id FROM systems").dictresult()]

    for system in systems:
        process_attacks_at(db, system)


def process_attacks_at(db, system):
    civ_ships = ships_at_system(db, system)
    ships_for_each = [v for v in civ_ships.values()]
    ships_for_each.sort(key=lambda l1: len(l1))

    # Process the lists of ships in order of who has the most ships in this system
    for ship_ids in ships_for_each:
        for ship_id in ship_ids:
            process_ship_attack(db, ship_id, civ_ships)


def process_ship_attack(db, ship_id, civs_in_system):
    # Only attack 1 in 3 times
    if random.random() > 1/3:
        return

    ship = db.get("ships", ship_id)
    orders = ship["orders"]
    targets = [target for target in ship_targets(orders) if target in civs_in_system]
    if targets == []:
        return

    target_civ = targets[random.randrange(len(targets))]
    possible_ship_targets = civs_in_system[target_civ]
    if possible_ship_targets == []:
        return

    ship_target = possible_ship_targets[random.randrange(len(possible_ship_targets))]
    civs_in_system[target_civ].remove(ship_target)
    db.delete("ships", id=ship_target)


def ship_targets(order):
    targets = []
    for order in order:
        if order["order"] == "attack":
            for civ in order["team"]:
                targets.append(civ)
    return targets


def choose_ship_from_civ_at_system(db, civ, system):
    ships = db.query_formatted("SELECT id FROM ships WHERE flag = %s AND location = %s "
                               "ORDER BY RANDOM()",
                               (civ, system)).dictresult()
    if len(ships) == 0:
        return None
    else:
        return ships[0]["id"]
