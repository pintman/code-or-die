"""Functions related to team management"""

from database.civilizations import get_civ, set_civ_key, civ_systems


def set_token_for_team(db, old_key, new_key):
    return set_civ_key(db, get_civ(db, old_key), new_key)


def systems_for_team(db, key):
    return civ_systems(db, key)