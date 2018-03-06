"""database utils"""

import pg

with open("secrets.txt") as secrets:
    dbname = secrets.readline().splitlines()[0]
    host = secrets.readline().splitlines()[0]
    port = int(secrets.readline())

db = pg.DB(dbname=dbname,
           host=host,
           port=port)

def get_civ(key):
    try:
        return db.get("civilizations", key, "key")["id"]
    except pg.DatabaseError as e:
        return None



def set_civ_key(civ_id, new_key):
    pass


def civ_systems(key):
    pass


if __name__ == "__main__":
    print(get_civ("one such key"))