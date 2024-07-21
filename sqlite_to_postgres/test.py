import unittest

from custom_types import LoadDataType
from tools import connection


class LoadDataTest(unittest.TestCase):
    def __init__(
        self, load_data: LoadDataType, methodName: str = "runTest", *args, **kwargs
    ) -> None:
        super().__init__(methodName)
        self.load_data = load_data

    def _format_data(self, data: dict) -> dict:
        result = {}
        for kv in dict(data).items():
            if kv[0] in [
                "created_at",
                "updated_at",
                "type",
                "description",
                "file_path",
            ]:
                if not kv[0] == "type":
                    result[kv[0]] = str(kv[1])[:19]
                if kv[0] == "movie":
                    result[kv[0]] = "MV"
                if kv[0] == "description" and kv[1] is None:
                    result[kv[0]] = ""
                if kv[0] == "file_path" and kv[1] is None:
                    result[kv[0]] = ""
            else:
                result[kv[0]] = str(kv[1])
        return result

    @connection
    def test_count(self, *args, **kwargs):
        for table in self.load_data.tables_name:
            sql_data = kwargs["sql_cursor"].execute(f"SELECT COUNT(id) FROM {table};")
            psql_data = kwargs["pg_cursor"].execute(
                f"SELECT COUNT(id) FROM {self.load_data.schema_tables}.{table};"  # pyright: ignore[]
            )

            sql_chank = sql_data.fetchall()
            psql_chank = psql_data.fetchall()

            self.assertEqual(
                tuple(sql_chank[0])[0],
                psql_chank[0].pop("count"),
            )

    @connection
    def test_content(self, *args, **kwargs):
        for table in self.load_data.tables_name:
            sql_data = kwargs["sql_cursor"].execute(
                f"SELECT * FROM {table} ORDER BY (id);"
            )
            psql_data = kwargs["pg_cursor"].execute(
                f"SELECT * FROM {self.load_data.schema_tables}.{table} ORDER BY (id);"  # pyright: ignore[]
            )

            sql_chank = sql_data.fetchmany(size=self.load_data.chank_size)
            psql_chank = psql_data.fetchmany(size=self.load_data.chank_size)

            while sql_chank:
                for row in sql_chank:
                    row1 = self._format_data(row)

                for row in psql_chank:
                    row2 = self._format_data(row)  # pyright: ignore[]

                self.assertDictEqual(row1, row2)  # pyright: ignore[]
                sql_chank = sql_data.fetchmany(size=self.load_data.chank_size)
                psql_chank = psql_data.fetchmany(size=self.load_data.chank_size)

    def test(self):
        self.test_count()
        self.test_content()
