from datetime import datetime
from database.mechanics import *


def process_transits(db):
    for transit in get_transits(db):
        if transit_is_done(db, transit, datetime.timestamp(datetime.now())):
            finish_transit(db, transit)
    return True


def transit_is_done(db, transit, time):
    return transit["type"] is "beam_transit" or \
           (time - transit["time"]) >= travel_time(db, transit)


def travel_time(db, transit):
    return get_route_distance(db, transit["origin"], transit["destination"])


def finish_transit(db, transit):
    remove_transit(db, transit["id"], transit["type"])
    set_ship_location(db, transit["ship"], transit["destination"])
