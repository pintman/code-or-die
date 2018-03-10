from make_app import make_app
from flask import request, jsonify
import json
from civilization.operations import *
from system.operations import *
from ship.operations import *
from mechanics.transit import process_transits

from apscheduler.schedulers.background import BackgroundScheduler

app = make_app()


def extract_key(request):
    try:
        return request.headers["api-key"]
    except KeyError or IndexError as e:
        return None


@app.route("/", methods=["GET"])
def _rules_summary():
    with open("README.md") as rules:
        return "\n".join(rules.readlines(-1))


@app.route("/set-api-key", methods=["POST"])
def _set_token_for_team():
    old_key = extract_key(request)
    new_key = request.get_json(force=True)["new-api-key"]
    return jsonify(set_token_for_team(app.db, old_key, new_key))


@app.route("/systems", methods=["GET"])
def _systems_for_team():
    key = extract_key(request)
    return jsonify(systems_for_team(app.db, key))


@app.route("/systems/<system>", methods=["GET"])
def _system_info(system):
    key = extract_key(request)
    return jsonify(system_info(app.db, key, system))


@app.route("/systems/names/<system>", methods=["GET"])
def _get_system_convenience_names(system):
    return jsonify(get_system_convenience_names(app.db, system))


@app.route("/systems/<system>/add-name/<new_convenience_name>", methods=["POST"])
def _add_convenience_name(system, new_convenience_name):
    return jsonify(add_convenience_name(app.db, system, new_convenience_name))


@app.route("/system/<system>/orders", methods=["GET", "POST", "DELETE"])
def _system_orders(system):
    key = extract_key(request)
    if request.method == "GET":
        return jsonify(system_orders(app.db, key, system))
    if request.method == "POST":
        order = request.get_json(force=True)
        return jsonify(add_order_to_system(app.db, key, system, order))
    if request.method == "DELETE":
        return jsonify(remove_all_orders_from_system(app.db, key, system))


@app.route("/system/<system>/orders/<int:order_index>", methods=["DELETE"])
def _remove_order_from_system(system, order_index):
    key = extract_key(request)
    return jsonify(remove_order_from_system(app.db, key, system, order_index))


@app.route("/ship/<ship>/orders", methods=["GET", "POST", "DELETE"])
def _remove_all_orders_from_ship(ship):
    key = extract_key(request)
    if request.method == "GET":
        return jsonify(get_orders_from_ship(app.db, key, ship))
    elif request.method == "POST":
        order = request.get_json(force=True)
        return jsonify(add_order_to_ship(app.db, key, ship, order))
    elif request.method == "DELETE":
        return jsonify(remove_all_orders_from_ship(app.db, key, ship))


@app.route("/system/<ship>/orders/<int:order_index>", methods=["DELETE"])
def _remove_order_from_ship(ship, order_index):
    key = extract_key(request)
    return jsonify(remove_order_from_ship(app.db, key, ship, order_index))


@app.route("/ships", methods=["GET"])
def _get_ships():
    key = extract_key(request)
    return jsonify(get_ships(app.db, key))


@app.route("/ship/<int:ship_id>")
def _get_ship_info(ship_id):
    key = extract_key(request)
    return jsonify(get_ship_info(app.db, key, ship_id))


if __name__ == "__main__":
    import functools

    # Set up the main game loop
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: process_transits(app.db), 'interval', minutes=1)
    # scheduler.add_job(process_ship_orders, 'interval', seconds=5)
    # scheduler.add_job(process_system_orders, 'interval', minutes=1)
    scheduler.start()
    # Launch the api
    app.run()
