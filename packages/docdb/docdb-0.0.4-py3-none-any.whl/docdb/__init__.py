import sqlite3
import json
import time
from uuid import uuid4
from typing import Iterable, List

class PKNotInDocument(Exception):
    pass

class UUIDNotInDocument(Exception):
    pass

class InvalidDocumentID(Exception):
    pass

class InvalidCollectionMethod(Exception):
    pass

class InvalidOperator(Exception):
    pass

class Collection:
    """ the collection object """
    def __init__(self, database_name: str, collection_name: str, pk: str = None):
        self.conn = sqlite3.connect(database_name)
        self.name = collection_name
        self.pk = pk
    
    @property
    def documents(self) -> Iterable[dict]:
        cur = self.conn.cursor()
        return [json.loads(x[0]) for x in cur.execute(f""" SELECT body FROM {self.name};""")]

    def get(self, uuid) -> dict:
        cur = self.conn.cursor()
        results = []
        for doc in cur.execute(f""" SELECT body FROM {self.name} WHERE uuid = '{uuid}';"""):
            results.append(doc[0])
        return json.loads(results[0])
    
    def bulk_get(self, uuids: List[str]) -> List[dict]:
        cur = self.conn.cursor()
        results = []
        args = ','.join(f'"{i}"' for i in uuids)
        results = [json.loads(x[0]) for x in cur.execute(f"SELECT body FROM {self.name} WHERE uuid IN ({args})")]
        self.conn.commit()
        return results

    def insert(self, document: dict, options: dict = {}) -> dict:
        """ insert a single document into the collection """
        # NOTE: 100k records ~ 30s on Dan's MBP
        cur = self.conn.cursor()
        id = str(uuid4())
        now = time.time()
        if '_id' in document.keys():
            raise InvalidCollectionMethod("cannot 'insert' a document with an existing _id field. Use update or bulk_update instead.")
        document['_id'] = id
        cur.execute(f"INSERT INTO {self.name} VALUES ('{id}', '{json.dumps(document)}', '{now}', '{now}')")
        # NOTE: this handles inserting the primary key into our meta table
        if self.pk is not None:
            if self.pk not in document.keys():
                raise PKNotInDocument(f"the pk was not found in the document (pk = '{self.pk}')")
            else:
                k = self.pk
                v = document.get(self.pk)
                if type(v) == int or self._isint(v):
                    cur.execute(f"INSERT INTO {self.name}_meta VALUES ('{id}', '{k}', 'int', '', '{v}', '', '{k}:{v}', '{now}', '{now}')")
                elif type(v) == float or self._isfloat(v):
                    cur.execute(f"INSERT INTO {self.name}_meta VALUES ('{id}', '{k}', 'real', '', '', '{v}', '{k}:{v}', '{now}', '{now}')")
                else:
                    cur.execute(f"INSERT INTO {self.name}_meta VALUES ('{id}', '{k}', 'str', '{v}', '', '', '{k}:{v}', '{now}', '{now}')")
        
        # NOTE: this handles inserting the secondary index data into our meta table
        if 'secondary_indexes' in options.keys():
            for si in options.get('secondary_indexes'):
                k = si
                v = document.get(si, None)
                if v is not None:
                    if type(v) == int or self._isint(v):
                        cur.execute(f"INSERT INTO {self.name}_meta VALUES ('{id}', '{k}', 'int', '', '{v}', '', '{k}:{v}:{id}', '{now}', '{now}')")
                    elif type(v) == float or self._isfloat(v):
                        cur.execute(f"INSERT INTO {self.name}_meta VALUES ('{id}', '{k}', 'real', '', '', '{v}', '{k}:{v}:{id}', '{now}', '{now}')")
                    else:
                        cur.execute(f"INSERT INTO {self.name}_meta VALUES ('{id}', '{k}', 'str', '{v}', '', '', '{k}:{v}:{id}', '{now}', '{now}')")

        self.conn.commit()
        return {"uuid": id}

    def bulk_insert(self, documents: List[dict], options: dict = {}) -> dict:
        count = 0
        cur = self.conn.cursor()
        for document in documents:
            count += 1
            id = str(uuid4())
            now = time.time()
            if '_id' in document.keys():
                raise InvalidCollectionMethod("cannot 'bulk_insert' a document with an existing _id field. Use update or bulk_update instead.")
            document['_id'] = id
            cur.execute(f"INSERT INTO {self.name} VALUES ('{id}', '{json.dumps(document)}', '{now}', '{now}')")
            # NOTE: this handles inserting the primary key into our meta table
            if self.pk is not None:
                if self.pk not in document.keys():
                    raise PKNotInDocument(f"the pk was not found in the document (pk = '{self.pk}')")
                else:
                    k = self.pk
                    v = document.get(self.pk)
                    if type(v) == int or self._isint(v):
                        cur.execute(f"INSERT INTO {self.name}_meta VALUES ('{id}', '{k}', 'int', '', '{v}', '', '{k}:{v}', '{now}', '{now}')")
                    elif type(v) == float or self._isfloat(v):
                        cur.execute(f"INSERT INTO {self.name}_meta VALUES ('{id}', '{k}', 'real', '', '', '{v}', '{k}:{v}', '{now}', '{now}')")
                    else:
                        cur.execute(f"INSERT INTO {self.name}_meta VALUES ('{id}', '{k}', 'str', '{v}', '', '', '{k}:{v}', '{now}', '{now}')")
            
            # NOTE: this handles inserting the secondary index data into our meta table
            if 'secondary_indexes' in options.keys():
                for si in options.get('secondary_indexes'):
                    k = si
                    v = document.get(si, None)
                    if v is not None:
                        if type(v) == int or self._isint(v):
                            cur.execute(f"INSERT INTO {self.name}_meta VALUES ('{id}', '{k}', 'int', '', '{v}', '', '{k}:{v}:{id}', '{now}', '{now}')")
                        elif type(v) == float or self._isfloat(v):
                            cur.execute(f"INSERT INTO {self.name}_meta VALUES ('{id}', '{k}', 'real', '', '', '{v}', '{k}:{v}:{id}', '{now}', '{now}')")
                        else:
                            cur.execute(f"INSERT INTO {self.name}_meta VALUES ('{id}', '{k}', 'str', '{v}', '', '', '{k}:{v}:{id}', '{now}', '{now}')")
        self.conn.commit()
        return {"documents_inserted_count": count}

    def update(self, document: dict, options: dict = {}) -> dict:
        id = document.get('_id', None)
        if id is None:
            raise InvalidDocumentID("the provided document has no _id field")
        cur = self.conn.cursor()
        now = time.time()
        cur.execute(f"""
        UPDATE {self.name} 
        SET body = '{json.dumps(document)}', 
            date_updated = '{now}' 
        WHERE uuid = '{id}';""")

        # NOTE: this handles inserting the primary key into our meta table        
        if self.pk is not None:
            if self.pk not in document.keys():
                raise PKNotInDocument(f"the pk was not found in the document (pk = '{self.pk}')")
            else:
                k = self.pk
                v = document.get(self.pk)
                if type(v) == int or self._isint(v):
                    count = cur.execute(f"""
                    UPDATE {self.name}_meta 
                    SET key = '{k}',
                    value_int = '{v}',
                    value_real = '',
                    value_str = '',
                    composite = '{k}:{v}',
                    date_updated = '{now}'
                    WHERE uuid = '{id}';""").rowcount

                elif type(v) == float or self._isfloat(v):
                    count = cur.execute(f"""
                    UPDATE {self.name}_meta 
                    SET key = '{k}',
                    value_int = '',
                    value_real = '{v}',
                    value_str = '',
                    composite = '{k}:{v}',
                    date_updated = '{now}'
                    WHERE uuid = '{id}';""").rowcount

                else:
                    count = cur.execute(f"""
                    UPDATE {self.name}_meta 
                    SET key = '{k}',
                    value_int = '',
                    value_real = '',
                    value_str = '{v}',
                    composite = '{k}:{v}',
                    date_updated = '{now}'
                    WHERE uuid = '{id}';""").rowcount
        
        # NOTE: this handles inserting the secondary index data into our meta table
        if 'secondary_indexes' in options.keys():
            if self.pk is not None:
                cur.execute(f"DELETE FROM {self.name}_meta WHERE uuid = '{id}' AND key != '{self.pk}'")
            else:
                cur.execute(f"DELETE FROM {self.name}_meta WHERE uuid = '{id}'")
            for si in options.get('secondary_indexes'):
                k = si
                v = document.get(si, None)
                if v is not None:
                    if type(v) == int or self._isint(v):
                        cur.execute(f"INSERT INTO {self.name}_meta VALUES ('{id}', '{k}', 'int', '', '{v}', '', '{k}:{v}:{id}', '{now}', '{now}')")
                    elif type(v) == float or self._isfloat(v):
                        cur.execute(f"INSERT INTO {self.name}_meta VALUES ('{id}', '{k}', 'real', '', '', '{v}', '{k}:{v}:{id}', '{now}', '{now}')")
                    else:
                        cur.execute(f"INSERT INTO {self.name}_meta VALUES ('{id}', '{k}', 'str', '{v}', '', '', '{k}:{v}:{id}', '{now}', '{now}')")

        self.conn.commit()
        return {"documents_updated_count": count}
    
    # TODO: FINISH THIS...
    def bulk_update(self, documents: List[dict]) -> dict:
        count = 0
        cur = self.conn.cursor()
        for document in documents:
            count += 1
            id = document.get('_id', None)
            if not id:
                raise InvalidDocumentID(f"the provided document has no _id field: {json.dumps(document)}")
            now = time.time()
            cur.execute(f"""
                UPDATE {self.name}
                SET body = '{json.dumps(document)}',
                date_updated = '{now}'
                WHERE uuid = '{id}';""")
            if self.pk in document.keys():
                k = self.pk
                v = document.get(k)
                cur.execute(f"""
                    UPDATE {self.name}_meta
                    SET key = '{k}',
                    value = '{v}',
                    composite = '{k}:{v}', 
                    date_updated = '{now}' 
                    WHERE uuid = '{id}';""")
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
    
    def _isfloat(self, x):
        try:
            a = float(x)
        except (TypeError, ValueError):
            return False
        else:
            return True

    def _isint(self, x):
        try:
            a = float(x)
            b = int(a)
        except (TypeError, ValueError):
            return False
        else:
            return a == b
    
    def _statement_to_sql(self, key, op, val) -> str:
        """ constructs the sql statement for a query """
        valid_ops = ['lt', 'gt', 'lte', 'gte', 'eq', 'sw', 'ew', 'in', '!sw', '!ew', '!eq', '!in', 'bt', '!bt']
        statement = None
        if type(val) == int or self._isint(val):
            typ = "int"
        elif type(val) == float or self._isfloat(val):
            typ = "real"
        else:
            typ = "str"
        if op not in valid_ops:
            raise InvalidOperator(f"'{op}' is not a valid operator")
        if op == 'lt':
            statement = f"key = '{key}' AND value_{typ} < '{val}'"
        elif op == 'gt':
            statement = f"key = '{key}' AND value_{typ} > '{val}'"
        elif op == 'lte':
            statement = f"key = '{key}' AND value_{typ} <= '{val}'"
        elif op == 'gte':
            statement = f"key = '{key}' AND value_{typ} >= '{val}'"
        elif op == 'eq':
            statement = f"key = '{key}' AND value_{typ} = '{val}'"
        elif op == '!eq':
            statement = f"key = '{key}' AND value_{typ} != '{val}'"
        elif op == 'sw':
            statement = f"key = '{key}' AND value_{typ} LIKE '{val}%'"
        elif op == 'ew':
            statement = f"key = '{key}' AND value_{typ} LIKE '%{val}'"
        elif op == 'in':
            statement = f"key = '{key}' AND value_{typ} LIKE '%{val}%'"
        elif op == '!sw':
            statement = f"key = '{key}' AND value_{typ} NOT LIKE '{val}%'"
        elif op == '!ew':
            statement = f"key = '{key}' AND value_{typ} NOT LIKE '%{val}'"
        elif op == '!in':
            statement = f"key = '{key}' AND value_{typ} NOT LIKE '%{val}%'"
        elif op == 'bt':
            s, e = val.split(',')
            if type(s) == int or self._isint(s):
                typ = "int"
            elif type(s) == float or self._isfloat(s):
                typ = "real"
            else:
                typ = "str"
            statement = f"key = '{key}' AND value_{typ} BETWEEN '{s}' AND '{e}'"
        elif op == '!bt':
            s, e = val.split(',')
            if type(s) == int or self._isint(s):
                typ = "int"
            elif type(s) == float or self._isfloat(s):
                typ = "real"
            else:
                typ = "str"
            statement = f"key = '{key}' AND value_{typ} NOT BETWEEN '{s.strip()}' AND '{e.strip()}'"
        return statement

    def query(self, exprs: List[str]) -> dict:
        """ a lightweight query interface """
        cur = self.conn.cursor()
        statements = []
        for expr in exprs:
            if expr == '&':
                statements.append('AND')
            elif expr == '|':
                statements.append('OR')
            else:
                k, o, v = expr.split(':')
                statements.append(self._statement_to_sql(k, o, v))
        statement = " ".join(statements)
        return [json.loads(doc[0]) for doc in cur.execute(f"SELECT body FROM {self.name} WHERE uuid IN (SELECT DISTINCT uuid FROM {self.name}_meta WHERE {statement});")]

class Engine:
    """ the lightweight document engine """

    def __init__(self, database_name: str):
        # NOTE: this will automatically create the database file if it doesn't exist.
        self.db_name = database_name
        self.conn = sqlite3.connect(database_name)
        cur = self.conn.cursor()
        self.collections = [x[0] for x in cur.execute(""" SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '%_meta';""")]
    
    def collection(self, collection_name: str, pk: str = None):
        """ create a new collection """
        cur = self.conn.cursor()
        if collection_name not in self.collections:
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
                uuid BLOB NOT NULL
            , "key" TEXT NOT NULL
            , "type" TEXT NOT NULL
            , value_str TEXT NULL
            , value_int INTEGER NULL
            , value_real REAL NULL
            , composite TEXT NOT NULL
            , date_created INTEGER NOT NULL
            , date_updated INTEGER NOT NULL
            , UNIQUE(composite)
            );
            """)
            self.conn.commit()
        return Collection(self.db_name, collection_name, pk)
    
    def delete_collection(self, collection_name: str):
        """ delete the entire collection (HARD DELETE) """
        cur = self.conn.cursor()
        cur.execute(f"DROP TABLE {collection_name};")
        cur.execute(f"DROP TABLE {collection_name}_meta;")
        return True

