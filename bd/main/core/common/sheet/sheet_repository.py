from abc import ABC, abstractmethod
from typing import List


class SheetRepository(ABC):
    @abstractmethod
    def open(self, doc_name: str, sheet_name: str = None) -> None:
        pass

    @abstractmethod
    def append(self, liste: List) -> None:
        pass

    @abstractmethod
    def get(self, i: int, j: int) -> str:
        pass

    @abstractmethod
    def get_line(self, i: int) -> List:
        pass

    @abstractmethod
    def get_column(self, j: int) -> List:
        pass

    @abstractmethod
    def get_size(self) -> (int, int):
        pass

    @abstractmethod
    def get_all(self) -> List:
        pass

    @abstractmethod
    def set(self, valeur: str, i: int, j: int) -> None:
        pass

    @abstractmethod
    def set_line(self, valeur: List, i: int) -> None:
        pass

    @abstractmethod
    def set_column(self, valeur: List, j: int, offset: int) -> None:
        pass

    @abstractmethod
    def delete_row(self, i: int) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def double(self, isbn: int) -> bool:
        pass
