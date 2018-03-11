from test.fixtures import db
from app import add_order_to_ship
from database.mechanics import army_sizes_at_system
from mechanics.attack import process_attacks
import pg


def test_attack(db):
    def add_ships_to_system(system, civ, num_ships, attack_targets):
        if not attack_targets:
            orders = []
        else:
            orders = [{"order": "attack", "team": attack_targets}]

        for _ in range(num_ships):
            db.query_formatted("INSERT INTO ships (shipyard, location, flag, orders) "
                               "VALUES (1, %s, %s, %s)", (system, civ, pg.jsonencode(orders)))

    add_ships_to_system(system=4, civ=1, num_ships=2, attack_targets=[3])

    assert army_sizes_at_system(db, 4) == {"earth": 3, "venus": 1}
    # 1/3 ^ 10 is small enough to guarantee that venus's ship is destroyed
    for i in range(10):
        process_attacks(db)
    assert army_sizes_at_system(db, 4) == {"earth": 3}

    # Create system 5
    db.query("INSERT INTO systems(id) VALUES (5)")

    add_ships_to_system(system=5, civ=1, num_ships=100, attack_targets=[3])
    add_ships_to_system(system=5, civ=3, num_ships=100, attack_targets=[1])
    assert army_sizes_at_system(db, 5) == {"earth": 100, "venus": 100}

    process_attacks(db)
    assert army_sizes_at_system(db, 5)["earth"] < 90
    assert army_sizes_at_system(db, 5)["venus"] < 90
