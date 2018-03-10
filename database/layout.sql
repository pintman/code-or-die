DROP TABLE IF EXISTS systems CASCADE;
DROP TABLE IF EXISTS routes CASCADE;
DROP TABLE IF EXISTS civilizations CASCADE;
DROP TABLE IF EXISTS ships CASCADE;
DROP TABLE IF EXISTS build CASCADE;
DROP TABLE IF EXISTS warp CASCADE;
DROP TABLE IF EXISTS beam_transit CASCADE;
DROP TABLE IF EXISTS ftl_transit CASCADE;
DROP TABLE IF EXISTS attack CASCADE;

DROP VIEW IF EXISTS transit;

DROP TYPE IF EXISTS TRANSIT_TYPE CASCADE;
DROP TYPE IF EXISTS SYSTEM_STATUS CASCADE;
DROP TYPE IF EXISTS BEAM_MODE CASCADE;

CREATE TYPE TRANSIT_TYPE AS ENUM ('beam', 'ftl');
CREATE TYPE SYSTEM_STATUS AS ENUM ('active', 'destroyed');
CREATE TYPE BEAM_MODE AS ENUM ('transit', 'repair');


CREATE TABLE IF NOT EXISTS civilizations (
  id        SERIAL PRIMARY KEY,
  name      TEXT,
  homeworld INTEGER,
  key       TEXT
);

CREATE TABLE IF NOT EXISTS systems (
  id         SERIAL PRIMARY KEY,
  status     SYSTEM_STATUS NOT NULL DEFAULT 'active' :: SYSTEM_STATUS,
  mode       BEAM_MODE     NOT NULL DEFAULT 'transit' :: BEAM_MODE,
  controller INTEGER                DEFAULT NULL,
  production INTEGER                DEFAULT 1 CHECK (production > 0),
  tuning     INTEGER       NOT NULL DEFAULT 0,
  names      TEXT ARRAY             DEFAULT '{}',
  orders     JSONB                  DEFAULT '[]',
  historical_tuning INTEGER ARRAY DEFAULT '{}',
  tuning_destinations INTEGER ARRAY DEFAULT '{}'
) WITH OIDS;

CREATE TABLE IF NOT EXISTS routes (
  id          SERIAL PRIMARY KEY,
  origin      INTEGER NOT NULL REFERENCES systems (id),
  destination INTEGER NOT NULL REFERENCES systems (id) CHECK (destination > origin),
  distance    INTEGER NOT NULL CHECK (distance > 0)
);


ALTER TABLE systems
  ADD FOREIGN KEY (controller) REFERENCES civilizations (id);

ALTER TABLE civilizations
  ADD FOREIGN KEY (homeworld) REFERENCES systems (id);


CREATE TABLE IF NOT EXISTS ships (
  id       SERIAL PRIMARY KEY,
  shipyard INTEGER NOT NULL REFERENCES systems (id),
  location INTEGER REFERENCES systems (id),
  flag     INTEGER NOT NULL REFERENCES civilizations (id),
  orders   JSONB DEFAULT '[]'
);


CREATE TABLE IF NOT EXISTS build (
  id       SERIAL PRIMARY KEY,
  system   INTEGER                  NOT NULL REFERENCES systems (id),
  owner    INTEGER                  NOT NULL REFERENCES civilizations (id),
  quantity INTEGER                  NOT NULL CHECK (quantity > 0),
  time     TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);


CREATE TABLE IF NOT EXISTS warp (
  id          SERIAL PRIMARY KEY,
  origin      INTEGER                  NOT NULL REFERENCES systems (id),
  destination INTEGER                  NOT NULL REFERENCES systems (id),
  magnitude   INTEGER                  NOT NULL,
  time        TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);


CREATE TABLE IF NOT EXISTS beam_transit (
  id          SERIAL PRIMARY KEY,
  ship        INTEGER                  NOT NULL REFERENCES ships (id),
  origin      INTEGER                  NOT NULL REFERENCES systems (id),
  destination INTEGER                  NOT NULL REFERENCES systems (id),
  tuning      INTEGER                  NOT NULL,
  time        TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);


CREATE TABLE IF NOT EXISTS ftl_transit (
  id          SERIAL PRIMARY KEY,
  ship        INTEGER                  NOT NULL REFERENCES ships (id),
  origin      INTEGER                  NOT NULL REFERENCES systems (id),
  destination INTEGER                  NOT NULL REFERENCES systems (id),
  time        TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);


CREATE OR REPLACE VIEW transit AS (
  SELECT
    'beam_transit' :: REGCLASS AS type,
    id,
    ship,
    origin,
    destination,
    tuning,
    time
  FROM beam_transit
  UNION
  SELECT
    'ftl_transit' :: REGCLASS AS type,
    id,
    ship,
    origin,
    destination,
    NULL                      AS tuning,
    time
  FROM ftl_transit
);

CREATE TABLE IF NOT EXISTS attack (
  id     SERIAL PRIMARY KEY,
  ship   INTEGER                  NOT NULL REFERENCES ships (id),
  target INTEGER REFERENCES civilizations (id),
  time   TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);