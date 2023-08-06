CREATE TABLE collection_1_meta (
    uuid BLOB NOT NULL PRIMARY KEY
  , "key" TEXT NOT NULL
  , value TEXT NOT NULL
  , composite TEXT NOT NULL
  , date_created INTEGER NOT NULL
  , date_updated INTEGER NOT NULL
);
