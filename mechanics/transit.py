from datetime import datetime
from database.key_access import get_transits, get_route_distance

def process_transits(db):
    finished_transits = []
    for transit in get_transits(db):
        if transit_is_done(db, transit):
            finish_transit(db, transit)
    return True

def transit_is_done(db, transit):
    return transit["type"] is "beam_transit" or \
           (datetime.timestamp(datetime.now()) - transit["time"]) >= transit_time(db, transit)


def transit_time(db, transit):
    return get_route_distance(db, transit["origin"], transit["destination"])


def finish_transit(db, transit):
    remove_transit(db, transit["id"])
    set_ship_location(db, transit["ship"], transit["destination"])