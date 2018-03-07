TRUNCATE TABLE attack, beam_transit, build, civilizations, ftl_transit, routes, ships, systems, warp;

INSERT INTO systems VALUES
  (1),
  (2);

INSERT INTO systems (id, names) VALUES
  (3, '{"home", "venus"}'),
  (4, '{"war"}');


INSERT INTO routes (origin, destination, distance) VALUES
  (1, 4, 1),
  (2, 4, 2),
  (3, 4, 5);

INSERT INTO civilizations (id, name, homeworld, key) VALUES
  (1, 'earth', 1, 'key1'),
  (2, 'mars', 2, 'key2'),
  (3, 'venus', 3, 'key3');

INSERT INTO ships (shipyard, location, flag) VALUES
  (1, 1, 1),
  (1, 1, 1),
  (1, 4, 1),
  (3, 4, 1);


UPDATE systems
SET controller = 1
WHERE systems.id IN (1, 4);

UPDATE systems
SET controller = 2
WHERE systems.id IN(2);

UPDATE systems
SET controller = 3
WHERE systems.id IN(3);