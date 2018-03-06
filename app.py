from flask import Flask, request
from team import *
from system import *
from ship import *

app = Flask(__name__)


def extract_key(request):
    return request.headers["api-key"]


@app.route("/", methods=["GET"])
# Returns a summary of the rules, including available API endpoints
def _rules_summary():
    with open("README.md") as rules:
        return rules


@app.route("reset-api-key/<new_key>", methods=["POST"])
# Updates the ket for a team
def _set_token_for_team(new_key):
    old_key = extract_key(request)
    return set_token_for_team(old_key, new_key)


@app.route("/systems", methods=["GET"])
def _systems_for_team():
    key = extract_key(request)
    return systems_for_team(key)


@app.route("/systems/<system>", methods=["GET"])
def _system_info(system):
    key = extract_key(request)
    return system_info(key, system)


def _system_info_from_id(system_id):
    return system_info_from_id(system_id)


def _system_info_from_name(system_name):
    return system_info_from_name(system_name)


@app.route("systems/names", methods=["GET"])
def _get_system_convenience_names():
    return get_system_convenience_names()


@app.route("systems/<system:system>/<new_convenience_name>", methods=["POST"])
def _add_convenience_name(system, new_convenience_name):
    return add_convenience_name(system, new_convenience_name)


@app.route("system/<system>/orders", methods=["GET", "POST"])
def _system_orders(system):
    return system_orders(system)


@app.route("system/<system>/orders/", methods=["DELETE"])
def _remove_all_orders_from_system(system, order_index):
    return remove_all_orders_from_system(system, order_index)


@app.route("system/<system>/orders/<order_index>", methods=["DELETE"])
def _remove_order_from_system(system, order_index):
    return remove_order_from_system(system, order_index)


@app.route("ship/<ship>/orders/", methods=["DELETE"])
def _remove_all_orders_from_ship(ship, order_index):
    return remove_all_orders_from_ship(ship, order_index)


@app.route("system/<ship>/orders/<order_index>", methods=["DELETE"])
def _remove_order_from_ship(ship, order_index):
    return remove_order_from_ship(ship, order_index)


@app.route("ships", methods=["GET"])
def _get_ships():
    return get_ships()


@app.route("ship/<int:ship_id>")
def _get_ship_info(ship_id):
    return get_ship_info(ship_id)


if __name__ == "__main__":
    app.run()
