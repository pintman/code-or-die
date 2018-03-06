"""Functions related to team management"""

from database import get_civ, set_civ_key, civ_systems

def set_token_for_team(old_key, new_key):
    return set_civ_key(get_civ(old_key), new_key)


def systems_for_team(key):
    return civ_systems(key)