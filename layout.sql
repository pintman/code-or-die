DROP TYPE IF EXISTS SYSTEM_STATUS CASCADE;
CREATE TYPE SYSTEM_STATUS AS ENUM ('active', 'destroyed');


DROP TYPE IF EXISTS BEAM_MODE CASCADE;
CREATE TYPE BEAM_MODE AS ENUM ('transit', 'repair');


DROP TYPE IF EXISTS TUNING_PARAMS CASCADE;
CREATE TYPE TUNING_PARAMS AS (
  real INTEGER, imag INTEGER
);


DROP TABLE IF EXISTS systems CASCADE;
CREATE TABLE IF NOT EXISTS systems (
  id         SERIAL PRIMARY KEY,
  status     SYSTEM_STATUS NOT NULL DEFAULT 'active' :: SYSTEM_STATUS,
  mode       BEAM_MODE     NOT NULL DEFAULT 'transit' :: BEAM_MODE,
  controller INTEGER                DEFAULT NULL,
  production INTEGER                DEFAULT 1 CHECK (production > 0),
  tuning     TUNING_PARAMS NOT NULL DEFAULT ROW (0, 0) :: TUNING_PARAMS
) WITH OIDS;


DROP TABLE IF EXISTS routes CASCADE;
CREATE TABLE IF NOT EXISTS routes (
  id          SERIAL PRIMARY KEY,
  origin      INTEGER NOT NULL REFERENCES systems (id),
  destination INTEGER NOT NULL REFERENCES systems (id),
  distance    INTEGER NOT NULL CHECK (distance > 0)
);


DROP TABLE IF EXISTS civilizations CASCADE;
CREATE TABLE IF NOT EXISTS civilizations (
  id        SERIAL PRIMARY KEY,
  name      TEXT    NOT NULL,
  homeworld INTEGER NOT NULL REFERENCES systems (id),
  token     TEXT    NOT NULL
) WITH OIDS;


ALTER TABLE systems
  ADD FOREIGN KEY (controller) REFERENCES civilizations (id);


DROP TYPE IF EXISTS SHIP_STATUS;
CREATE TYPE SHIP_STATUS AS ENUM ('active', 'destroyed');


DROP TABLE IF EXISTS ships CASCADE;
CREATE TABLE IF NOT EXISTS ships (
  id       SERIAL PRIMARY KEY,
  shipyard INTEGER NOT NULL REFERENCES systems (id),
  location INTEGER REFERENCES systems (id),
  flag     INTEGER NOT NULL REFERENCES civilizations (id)
) WITH OIDS;


DROP TABLE IF EXISTS civilizations CASCADE;
CREATE TABLE IF NOT EXISTS civilizations (
  id           SERIAL PRIMARY KEY,
  namer        INTEGER NOT NULL REFERENCES civilizations (id),
  civilization INTEGER NOT NULL REFERENCES civilizations (id),
  name         TEXT    NOT NULL
);


DROP TABLE IF EXISTS systems CASCADE;
CREATE TABLE IF NOT EXISTS systems (
  id     SERIAL PRIMARY KEY,
  namer  INTEGER NOT NULL REFERENCES civilizations (id),
  system INTEGER NOT NULL REFERENCES systems (id),
  name   TEXT    NOT NULL
);


DROP TABLE IF EXISTS ships CASCADE;
CREATE TABLE IF NOT EXISTS ships (
  id    SERIAL PRIMARY KEY,
  namer INTEGER NOT NULL REFERENCES civilizations (id),
  ship  INTEGER NOT NULL REFERENCES ships (id),
  name  TEXT    NOT NULL
);


DROP TYPE IF EXISTS ORDER_STATUS CASCADE;
CREATE TYPE ORDER_STATUS AS ENUM ('pending');


DROP TABLE IF EXISTS systems CASCADE;
CREATE TABLE IF NOT EXISTS systems (
  id      SERIAL PRIMARY KEY,
  system  INTEGER      NOT NULL REFERENCES systems (id),
  status  ORDER_STATUS NOT NULL DEFAULT 'pending' :: ORDER_STATUS,
  payload JSONB        NOT NULL
);


DROP TABLE IF EXISTS ships CASCADE;
CREATE TABLE IF NOT EXISTS ships (
  id      SERIAL PRIMARY KEY,
  ship    INTEGER      NOT NULL REFERENCES ships (id),
  status  ORDER_STATUS NOT NULL DEFAULT 'pending' :: ORDER_STATUS,
  payload JSONB        NOT NULL
);


DROP TABLE IF EXISTS build CASCADE;
CREATE TABLE IF NOT EXISTS build (
  id       SERIAL PRIMARY KEY,
  system   INTEGER                  NOT NULL REFERENCES systems (id),
  owner    INTEGER                  NOT NULL REFERENCES civilizations (id),
  quantity INTEGER                  NOT NULL CHECK (quantity > 0),
  time     TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

DROP TABLE IF EXISTS warp CASCADE;
CREATE TABLE IF NOT EXISTS warp (
  id          SERIAL PRIMARY KEY,
  origin      INTEGER                  NOT NULL REFERENCES systems (id),
  destination INTEGER                  NOT NULL REFERENCES systems (id),
  magnitude   INTEGER                  NOT NULL,
  time        TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

DROP TABLE IF EXISTS beam_transit CASCADE;
CREATE TABLE IF NOT EXISTS beam_transit (
  id          SERIAL PRIMARY KEY,
  ship        INTEGER                  NOT NULL REFERENCES ships (id),
  origin      INTEGER                  NOT NULL REFERENCES systems (id),
  destination INTEGER                  NOT NULL REFERENCES systems (id),
  tuning      TUNING_PARAMS            NOT NULL,
  time        TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

DROP TABLE IF EXISTS ftl_transit CASCADE;
CREATE TABLE IF NOT EXISTS ftl_transit (
  id          SERIAL PRIMARY KEY,
  ship        INTEGER                  NOT NULL REFERENCES ships (id),
  origin      INTEGER                  NOT NULL REFERENCES systems (id),
  destination INTEGER                  NOT NULL REFERENCES systems (id),
  time        TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);


DROP TYPE IF EXISTS TRANSIT_TYPE CASCADE;
CREATE TYPE TRANSIT_TYPE AS ENUM ('beam', 'ftl');


DROP VIEW IF EXISTS transit;
CREATE OR REPLACE VIEW transit AS (
  SELECT
    'beam_transit' :: REGCLASS AS type,
    ship,
    origin,
    destination,
    tuning,
    time
  FROM beam_transit
  UNION
  SELECT
    'ftl_transit' :: REGCLASS AS type,
    ship,
    origin,
    destination,
    NULL                      AS tuning,
    time
  FROM ftl_transit
);


DROP TABLE IF EXISTS attack CASCADE;
CREATE TABLE IF NOT EXISTS attack (
  id   SERIAL PRIMARY KEY,
  ship INTEGER                  NOT NULL REFERENCES ships (id),
  time TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);