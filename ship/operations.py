"""Functions related to ship management"""
from ship.database import *

def get_orders_from_ship(db, key, ship):
    return get_ship_orders(db, key, ship)


def add_order_to_ship(db, key, ship, order):
    orders = get_ship_orders(db, key, ship)
    orders.append(order)

    return set_ship_orders(db, key, ship, orders)


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
