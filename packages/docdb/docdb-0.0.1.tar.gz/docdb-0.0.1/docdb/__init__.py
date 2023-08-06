import sqlite3
import json
import time
from uuid import uuid4
from typing import Iterable, List

class PKNotInDocument(Exception):
    pass

class UUIDNotInDocument(Exception):
    pass

class Collection:
    """ the collection instance """
    def __init__(self, database_name: str, collection_name: str, pk: str = None):
        self.conn = sqlite3.connect(database_name)
        self.name = collection_name
        self.pk = pk
    
    @property
    def documents(self) -> Iterable[dict]:
        cur = self.conn.cursor()
        yield [json.loads(x[0]) for x in cur.execute(f""" SELECT body FROM {self.name};""")]

    def get(self, uuid) -> dict:
        cur = self.conn.cursor()
        results = []
        for doc in cur.execute(f""" SELECT body FROM {self.name} WHERE uuid = '{uuid}';"""):
            results.append(doc[0])
        return dict(json.loads(results[0]))
    
    def bulk_get(self, uuids: List[str]) -> List[dict]:
        cur = self.conn.cursor()
        results = []
        args = ','.join(f'"{i}"' for i in uuids)
        results = [json.loads(x[0]) for x in cur.execute(f"SELECT body FROM {self.name} WHERE uuid IN ({args})")]
        self.conn.commit()
        return results

    def insert(self, document: dict) -> dict:
        """ insert a single document into the collection """
        # NOTE: 100k records ~ 30s on Dan's MBP
        cur = self.conn.cursor()
        id = str(uuid4())
        now = time.time()
        cur.execute(f"INSERT INTO {self.name} VALUES ('{id}', '{json.dumps(document)}', '{now}', '{now}')")
        if self.pk is not None:
            if self.pk not in document.keys():
                raise PKNotInDocument(f"the pk was not found in the document (pk = '{self.pk}')")
            else:
                k = self.pk
                v = document.get(self.pk)
                cur.execute(f"INSERT INTO {self.name}_meta VALUES ('{id}', '{k}', '{v}', '{k}:{v}', '{now}', '{now}')")
        self.conn.commit()
        return {"uuid": id}

    def bulk_insert(self, documents: List[dict]) -> dict:
        count = 0
        cur = self.conn.cursor()
        for document in documents:
            count += 1
            id = str(uuid4())
            now = time.time()
            cur.execute(f"INSERT INTO {self.name} VALUES ('{id}', '{json.dumps(document)}', '{now}', '{now}')")
            if self.pk is not None:
                if self.pk not in document.keys():
                    raise PKNotInDocument(f"the pk was not found in the document (pk = '{self.pk}')")
                else:
                    k = self.pk
                    v = document.get(self.pk)
                    cur.execute(f"INSERT INTO {self.name}_meta VALUES ('{id}', '{k}', '{v}', '{k}:{v}', '{now}', '{now}')")
        self.conn.commit()
        return {"documents_inserted_count": count}

    def update(self, uuid, document: dict) -> dict:
        cur = self.conn.cursor()
        now = time.time()
        cur.execute(f"""
        UPDATE {self.name} 
        SET body = '{json.dumps(document)}', 
            date_updated = '{now}' 
        WHERE uuid = '{uuid}';""")

        if self.pk in document.keys():
            k = self.pk
            v = document.get(k)
            count = cur.execute(f"""
                UPDATE {self.name}_meta
                SET key = '{k}',
                value = '{v}',
                composite = '{k}:{v}', 
                date_updated = '{now}' 
                WHERE uuid = '{uuid}';""").rowcount

        self.conn.commit()
        return {"documents_updated_count": count}

    def bulk_update(self, documents: List[dict]) -> dict:
        count = 0
        cur = self.conn.cursor()
        for document in documents:
            count += 1
            uuid = document.get('uuid', None)
            del document['uuid']
            if not uuid:
                raise UUIDNotInDocument("a valid uuid is required in each document for a bulk update")
            now = time.time()
            cur.execute(f"""
                UPDATE {self.name}
                SET body = '{json.dumps(document)}',
                date_updated = '{now}'
                WHERE uuid = '{uuid}';""")
            if self.pk in document.keys():
                k = self.pk
                v = document.get(k)
                cur.execute(f"""
                    UPDATE {self.name}_meta
                    SET key = '{k}',
                    value = '{v}',
                    composite = '{k}:{v}', 
                    date_updated = '{now}' 
                    WHERE uuid = '{uuid}';""")
        self.conn.commit()
        return {"documents_updated_count": count}

    def delete(self, id: str) -> dict:
        cur = self.conn.cursor()
        count = cur.execute(f"DELETE FROM {self.name} WHERE uuid = '{id}';").rowcount
        count += cur.execute(f"DELETE FROM {self.name}_meta WHERE uuid = '{id}';").rowcount
        self.conn.commit()
        return {"documents_deleted_count": count / 2}

    def bulk_delete(self, uuids: List[str]) -> dict:
        cur = self.conn.cursor()
        args = ','.join(f'"{i}"' for i in uuids)
        count = cur.execute(f"DELETE FROM {self.name} WHERE uuid IN ({args})").rowcount
        count += cur.execute(f"DELETE FROM {self.name}_meta WHERE uuid IN ({args})").rowcount
        self.conn.commit()
        return {"documents_deleted_count": count / 2}

class Engine:
    """ the lightweight document engine """

    def __init__(self, database_name: str):
        # NOTE: this will automatically create the database file if it doesn't exist.
        self.db_name = database_name
        self.conn = sqlite3.connect(database_name)
        cur = self.conn.cursor()
        self.tables = [x[0] for x in cur.execute(""" SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '%_meta';""")]
    
    def collection(self, collection_name: str, pk: str = None):
        """ create a new collection """
        cur = self.conn.cursor()
        if collection_name not in self.tables:
            cur.execute(f"""
            CREATE TABLE {collection_name} (
                uuid BLOB NOT NULL PRIMARY KEY
            , body TEXT
            , date_created INTEGER
            , date_updated INTEGER
            , size INTEGER GENERATED ALWAYS AS (length(body)) STORED
            );
            """)
            cur.execute(f"""
            CREATE TABLE {collection_name}_meta (
                uuid BLOB NOT NULL PRIMARY KEY
            , "key" TEXT NOT NULL
            , value TEXT NOT NULL
            , composite TEXT
            , date_created INTEGER NOT NULL
            , date_updated INTEGER NOT NULL
            , UNIQUE(composite)
            );
            """)
            self.conn.commit()
        return Collection(self.db_name, collection_name, pk)
    
    def delete_collection(self, collection_name: str):
        """ delete the entire collection (HARD DELETE) """
        pass
