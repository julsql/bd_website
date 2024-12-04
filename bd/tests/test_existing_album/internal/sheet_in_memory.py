from typing import List

from main.core.common.sheet.sheet_repository import SheetRepository


class SheetInMemory(SheetRepository):
    worksheet = []
    client = {"bd": {"BD": [], "Test": []}}
    __OFFSET__ = 0

    def open(self, doc_name: str, sheet_name: str = None):
        if sheet_name is None:
            return self.client[doc_name]
        else:
            return self.client[doc_name][sheet_name]

    def append(self, liste: List):
        self.worksheet.append(liste)

    def get(self, i: int, j: int) -> str:
        i += self.__OFFSET__
        j += self.__OFFSET__
        return self.worksheet[i][j]

    def get_line(self, i: int) -> List:
        i += self.__OFFSET__
        return [self.get(i, j) for j in range(len(self.worksheet[i]))]

    def get_column(self, j: int) -> List:
        j += self.__OFFSET__

        return [row[j] for row in self.worksheet]

    def get_all(self) -> List:
        return self.worksheet

    def set(self, valeur: str, i: int, j: int):
        i += self.__OFFSET__
        j += self.__OFFSET__
        if isinstance(valeur, str):
            self.worksheet[i][j] = valeur
        else:
            raise TypeError(f"{valeur} n'est pas un type texte")

    def set_line(self, valeur: List, i: int):
        i += self.__OFFSET__
        if i < len(self.worksheet):
            if isinstance(valeur, list):
                self.worksheet[i] = valeur
            else:
                self.worksheet[i] = [valeur]

    def set_column(self, valeur: List, j: int):
        for i in range(len(self.worksheet)):
            if len(self.worksheet[i]) < j:
                self.worksheet[i][j] = valeur[i]

    def delete_row(self, i: int):
        self.set_line(["" for _ in range(26)], i)

    def double(self, isbn: int) -> bool:
        row_values = self.get_column(0)
        for cell_value in row_values:
            if str(cell_value) == str(isbn):
                return True
        return False
