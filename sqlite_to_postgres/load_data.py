import sqlite3
from typing import List, Tuple

from custom_types import LoadDataType
from psycopg.abc import Query

from test import LoadDataTest
from tools import conn_context, pg_context, _sqlite_connection, _pg_connection, dsl


class QueryManager:
    def __init__(self) -> None:
        self.base_query = "INSERT INTO {}.{} {} VALUES ({}) ON CONFLICT {} DO NOTHING;"
        self.on_conflict_types = {}

    def make_query(
        self, schema_table: str, table_name: str, table_columns: Tuple[str, ...]
    ) -> Query:
        values = "%s, " * (len(table_columns) - 1) + "%s"

        query = self.base_query.format(
            schema_table,
            table_name,
            table_columns,
            values,
            self.on_conflict_types.get(table_name, "(id)"),
        )
        return query.replace("'", "")  # pyright: ignore[]


class SQLiteLoader:
    def __init__(self, connection: _sqlite_connection) -> None:
        self.connection = connection
        self.cursor = self.connection.cursor()

    def make_select(self, table_name: str) -> None:
        self.cursor.execute(f"SELECT * FROM {table_name};")

    @staticmethod
    def parse_chunks_to_columns(chanks: List[sqlite3.Row]) -> Tuple[str, ...]:
        return tuple(dict(chanks[0]).keys())

    @staticmethod
    def parse_chunks_to_volume(chunks: List[sqlite3.Row]) -> List[Tuple[str, ...]]:
        result = []

        for chunk in chunks:
            chunk = dict(chunk)
            if chunk.get("type", False):
                if chunk["type"] == "movie":
                    chunk["type"] = "MV"
            if chunk.get("description", False) is None:
                chunk["description"] = ""
            if chunk.get("file_path", False) is None:
                chunk["file_path"] = ""
            result.append(tuple(chunk.values()))
        return result

    def get_chunks(self, chunk_size: int) -> List[sqlite3.Row]:
        return self.cursor.fetchmany(size=chunk_size)


class PostgresSaver:
    def __init__(self, pg_conn: _pg_connection) -> None:
        self.pg_conn = pg_conn
        self.cursor = self.pg_conn.cursor()

    def save_data(self, query: Query, data: List[Tuple]) -> None:
        self.cursor.executemany(query, data)
        self.pg_conn.commit()


def load_from_sqlite(connection: _sqlite_connection, pg_conn: _pg_connection) -> None:
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)
    query_manager = QueryManager()

    for table_name in load_data.tables_name:
        sqlite_loader.make_select(table_name)
        chunks = sqlite_loader.get_chunks(load_data.chank_size)
        columns = sqlite_loader.parse_chunks_to_columns(chunks)
        query = query_manager.make_query(load_data.schema_tables, table_name, columns)

        while chunks:
            data = sqlite_loader.parse_chunks_to_volume(chunks)
            postgres_saver.save_data(
                query,
                data,
            )
            chunks = sqlite_loader.get_chunks(load_data.chank_size)


if __name__ == "__main__":
    load_data = LoadDataType()
    with conn_context("db.sqlite") as sqlite_conn, pg_context(dsl) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
    LoadDataTest(load_data).test()
