def system_to_id(db, system):
    try:
        return int(system)
    except ValueError as e:
        for entry in get_all_system_convenience_names(db):
            if system in entry["names"]:
                return entry["id"]
        return None

def get_all_system_convenience_names(db):
    return db.query("SELECT id, names FROM systems").dictresult()
