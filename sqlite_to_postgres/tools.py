import sqlite3
from contextlib import contextmanager
from dataclasses import asdict
from functools import wraps

import psycopg
from psycopg import ClientCursor
from psycopg.rows import dict_row

from custom_types import DSLType

dsl = DSLType()


@contextmanager
def conn_context(db_path: str):  # pyright: ignore[]
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def connection(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        with conn_context("db.sqlite") as sqlite_conn, psycopg.connect(
            **asdict(dsl),
            row_factory=dict_row,  # pyright: ignore[]
            cursor_factory=ClientCursor,
        ) as pg_conn:
            kwargs["sql_cursor"] = sqlite_conn.cursor()
            kwargs["pg_cursor"] = pg_conn.cursor()
            return fn(self, *args, **kwargs)

    return wrapper
