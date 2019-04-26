CREATE TABLE plants (
  id INTEGER PRIMARY KEY,
  name text
);

CREATE TABLE watering_stats (
  id INTEGER PRIMARY KEY,
  timestamp INTEGER,
  duration REAL,
  plant INTEGER,
  FOREIGN KEY (plant) REFERENCES plants (id)
);

CREATE TABLE dryness_data (
  id INTEGER PRIMARY KEY,
  timestamp INTEGER,
  dryness INTEGER,
  plant INTEGER,
  FOREIGN KEY (plant) REFERENCES plants (id)
);
