from dataclasses import dataclass, field
from typing import List
import os


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
    dbname: str = os.environ.get("DB_NAME", "movies_database")
    user: str = os.environ.get("DB_USER", "postgres")
    password: str = os.environ.get("DB_PASSWORD", "123qwe")
    host: str = os.environ.get("DB_HOST", "127.0.0.1")
    port: str = os.environ.get("DB_PORT", "5432")
