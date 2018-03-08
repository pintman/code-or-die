"""Functions related to ship management"""
from ship.database import *


def get_orders_from_ship(db, key, ship):
    return get_ship_orders(db, key, ship)


def add_order_to_ship(db, key, ship, order):
    if not is_valid_ship_order(order):
        raise NotImplementedError("Invalid Order")

    orders = get_ship_orders(db, key, ship)
    orders.append(order)
    return set_ship_orders(db, key, ship, orders)


def is_valid_ship_order(order):
    if not order["order"]:
        return False

    def valid_attack():
        return order["order"] == "attack" and "civ" in order \
               and isinstance(order["civ"], list) and len(order["civ"]) > 0

    def valid_beam():
        return order["order"] == "beam" and "destination" in order and "tuning" in order

    def valid_ftl():
        return order["order"] == "ftl" and "destination" in order

    def valid_sieze():
        return order["order"] == "sieze"

    def valid_suicide():
        return order["order"] == "suicide"

    return valid_attack() or valid_beam() or valid_ftl() or valid_sieze() or valid_suicide()


def remove_all_orders_from_ship(db, key, ship):
    return set_ship_orders(db, key, ship, [])


def remove_order_from_ship(db, key, ship, order_index):
    orders = get_ship_orders(db, key, ship)
    orders.remove(orders[order_index])
    return set_ship_orders(db, key, ship, orders)


def get_ships(db, key):
    return get_all_ships(db, key)


def get_ship_info(db, key, ship):
    return get_ship(db, key, ship)
