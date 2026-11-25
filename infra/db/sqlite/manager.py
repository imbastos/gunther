import sqlite3
from typing import Iterable

from core.exceptions.db import DatabaseConnectionError


class SqliteManager:
    """Gerenciador de conexão com o banco de dados SQLite"""

    def __init__(self, db_path: str):
        self.__db_path = db_path
        self.__connection = None

    def __enter__(self):
        self.__connection = sqlite3.connect(self.__db_path)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type is None:
                self.__connection.commit()
            else:
                self.__connection.rollback()
        finally:
            self.__connection.close()
            self.__connection = None

    def __ensure_connection(self) -> sqlite3.Connection:
        if self.__connection is None:
            raise DatabaseConnectionError()
        return self.__connection

    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        conn = self.__ensure_connection()
        return conn.execute(query, params)

    def execute_many(self, query: str, params_seq: Iterable) -> sqlite3.Cursor:
        conn = self.__ensure_connection()
        return conn.executemany(query, params_seq)

    def fetch_all(self, query: str, params: tuple = ()) -> list[tuple]:
        return self.execute(query, params).fetchall()

    def fetch_one(self, query: str, params: tuple = ()) -> tuple | None:
        return self.execute(query, params).fetchone()

    def insert_many(self, table: str, rows: list) -> None:
        if not rows:
            return

        columns = ", ".join(f'"{col}"' for col in rows[0])
        placeholders = ", ".join(f":{col}" for col in rows[0])
        query = f"INSERT OR IGNORE INTO {table} ({columns}) VALUES ({placeholders})"

        self.execute_many(query, rows)
