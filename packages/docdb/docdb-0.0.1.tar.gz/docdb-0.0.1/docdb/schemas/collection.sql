CREATE TABLE collection_1 (
    uuid BLOB NOT NULL PRIMARY KEY
  , body BLOB
  , date_created INTEGER
  , date_updated INTEGER
  , size INTEGER GENERATED ALWAYS AS (length(body)) STORED
);
