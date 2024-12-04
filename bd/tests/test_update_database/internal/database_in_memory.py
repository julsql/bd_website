from typing import List, Dict, Any

from main.core.common.database.database_repository import DatabaseRepository


class DatabaseInMemory(DatabaseRepository):
    def __init__(self, filename: str):
        self.filename = filename
        self.database = None
        self.column_names = None

    def open(self):
        self.database = {}
        self.column_names = {}

    def create_table(self, table_name: str, column_names: List[str]) -> None:
        self.database[table_name] = []

    def insert(self, table_name: str, column_names: List[str], value: List[List[str]]) -> None:
        if len(value[0]) != len(column_names):
            raise IndexError
        print(column_names)
        for row in value:
            self.database[table_name].append({column_names[i]: row[i] for i in range(len(row))})

    def get_all(self, table_name: str) -> List[Dict[str, Any]]:
        print(self.database[table_name])
        return self.database[table_name]
