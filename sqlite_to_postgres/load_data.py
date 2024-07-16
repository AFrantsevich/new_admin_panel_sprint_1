import sqlite3
from typing import List, Tuple

from custom_types import LoadDataType

from test import LoadDataTest
from tools import connection


class QueryManager:
    def __init__(self) -> None:
        self.base_query = "INSERT INTO {}.{} {} VALUES ({}) ON CONFLICT {} DO NOTHING;"
        self.on_conflict_types = {}

    def make_query(
        self, schema_table: str, table_name: str, table_columns: Tuple[str, ...]
    ) -> str:
        values = "%s, " * (len(table_columns) - 1) + "%s"

        query = self.base_query.format(
            schema_table,
            table_name,
            table_columns,
            values,
            self.on_conflict_types.get(table_name, "(id)"),
        )
        return query.replace("'", "")


class SQLiteLoader:
    def __init__(self, cursor) -> None:
        self.cursor = cursor

    def make_select(self, table_name: str) -> None:
        self.cursor.execute(f"SELECT * FROM {table_name};")

    def parse_chanks_to_columns(self, chanks: List[sqlite3.Row]) -> Tuple[str, ...]:
        return tuple(dict(chanks[0]).keys())

    def parse_chanks_to_volume(
        self, chanks: List[sqlite3.Row]
    ) -> List[Tuple[str, ...]]:
        result = []

        for chank in chanks:
            chank = dict(chank)
            if chank.get("type", False):
                if chank["type"] == "movie":
                    chank["type"] = "MV"
            result.append(tuple(chank.values()))
        return result

    def get_chanks(self, chank_size: int) -> List[sqlite3.Row]:
        data = self.cursor.fetchmany(size=chank_size)
        return data


class PostgresLoader:
    def __init__(self) -> None:
        self.sql_loader = SQLiteLoader
        self.query_manager = QueryManager()

    @connection
    def load_data(self, load_data: LoadDataType, *args, **kwargs) -> None:
        sql_loader = self.sql_loader(kwargs["sql_cursor"])

        for table_name in load_data.tables_name:
            sql_loader.make_select(table_name)
            chanks = sql_loader.get_chanks(load_data.chank_size)
            columns = sql_loader.parse_chanks_to_columns(chanks)
            query = self.query_manager.make_query(
                load_data.schema_tables, table_name, columns
            )

            while chanks:
                data = sql_loader.parse_chanks_to_volume(chanks)
                kwargs["pg_cursor"].executemany(
                    query,  # pyright: ignore[]
                    data,
                )
                chanks = sql_loader.get_chanks(load_data.chank_size)


if __name__ == "__main__":
    load_data = LoadDataType()

    loader = PostgresLoader()
    loader.load_data(load_data)  # pyright: ignore[]

    LoadDataTest(load_data).test()
