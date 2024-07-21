import sqlite3
from contextlib import contextmanager
from dataclasses import asdict
from functools import wraps
from sqlite3 import Connection as _sqlite_connection
from typing import Generator

import psycopg
from custom_types import DSLType
from psycopg import ClientCursor
from psycopg import Connection as _pg_connection
from psycopg.rows import dict_row

dsl = DSLType()


@contextmanager
def conn_context(db_path: str) -> Generator[_sqlite_connection, None, None]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def pg_context(dsl: DSLType) -> Generator[_pg_connection, None, None]:
    conn = psycopg.connect(**asdict(dsl))
    conn.row_factory = dict_row  # pyright: ignore[]
    conn.cursor_factory = ClientCursor
    try:
        yield conn
    finally:
        conn.close()


def connection(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        with conn_context("db.sqlite") as sqlite_conn, pg_context(dsl) as pg_conn:
            kwargs["sql_cursor"] = sqlite_conn.cursor()
            kwargs["pg_cursor"] = pg_conn.cursor()
            return fn(self, *args, **kwargs)

    return wrapper
