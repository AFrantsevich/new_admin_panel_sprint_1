from dataclasses import dataclass, field
from typing import List


@dataclass
class LoadDataType:
    schema_tables: str = "content"
    tables_name: List[str] = field(
        default_factory=lambda: [
            "person",
            "genre",
            "film_work",
            "genre_film_work",
            "person_film_work",
        ]
    )
    chank_size: int = 4


@dataclass
class DSLType:
    dbname: str = "movies_database"
    user: str = "postgres"
    password: str = "123qwe"
    host: str = "127.0.0.1"
    port: int = 5432
