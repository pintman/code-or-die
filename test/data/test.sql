TRUNCATE TABLE attack, beam_transit, build, civilizations, ftl_transit, routes, ships, systems, warp;

INSERT INTO systems (id, names) VALUES
  (1, '{}'),
  (2, '{}'),
  (3, '{"home", "venus"}'),
  (4, '{"war"}');
ALTER SEQUENCE ships_id_seq RESTART 4;


INSERT INTO routes (origin, destination, distance) VALUES
  (1, 4, 1),
  (2, 4, 2),
  (3, 4, 5);
ALTER SEQUENCE routes_id_seq RESTART 3;

INSERT INTO civilizations (id, name, homeworld, key) VALUES
  (1, 'earth', 1, 'key1'),
  (2, 'mars', 2, 'key2'),
  (3, 'venus', 3, 'key3');
ALTER SEQUENCE civilizations_id_seq RESTART 3;

INSERT INTO ships (id, shipyard, location, flag) VALUES
  (1, 1, 1, 1),
  (2, 1, 1, 1),
  (3, 1, 4, 1),
  (4, 3, 4, 3);
ALTER SEQUENCE ships_id_seq RESTART 5;

UPDATE systems
SET controller = 1
WHERE systems.id IN (1, 4);

UPDATE systems
SET controller = 2
WHERE systems.id IN(2);

UPDATE systems
SET controller = 3
WHERE systems.id IN(3);