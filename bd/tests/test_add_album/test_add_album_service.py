import unittest

from common.logger_in_memory import LoggerInMemory
from common.sheet_in_memory import SheetInMemory
from main.application.usecases.album.add_album_service import AddAlbumService
from main.domain.exceptions.album_exceptions import AlbumAlreadyExistsException, AlbumNotFoundException
from tests.album_data_set import ASTERIX_ISBN, ASTERIX
from tests.test_add_album.internal.bd_in_memory import BdInMemory


class TestAddAlbumService(unittest.TestCase):
    NB_COLUMN = 21

    @classmethod
    def setUpClass(cls) -> None:
        # Before all
        cls.sheet_repository = SheetInMemory()
        cls.logging_repository = LoggerInMemory()
        cls.bd_repository = BdInMemory("AddAlbumBdRepository", ASTERIX)
        cls.service = AddAlbumService([cls.bd_repository], cls.sheet_repository, cls.logging_repository)

    def tearDown(self) -> None:
        # After each
        self.sheet_repository.clear()

    def test_convert_list_from_dict_empty_value_successfully(self) -> None:
        liste = self.service.map_to_list({
            'Album': '', 'Couleurs': '', 'Date de publication': '',
            'Dessin': '', 'Édition': '', 'ISBN': '', 'Image': '',
            'Numéro': '', 'Pages': '', 'Prix': '', 'Scénario': '',
            'Emplacement': '', 'Synopsis': '', 'Série': '', 'Éditeur': ''})
        self.assertEqual([""] * self.NB_COLUMN, liste)

    def test_convert_list_from_dict_successfully(self) -> None:
        liste = self.service.map_to_list({
            'Album': 'a', 'Couleurs': 'a', 'Date de publication': 'a',
            'Dessin': 'a', 'Édition': 'a', 'ISBN': 'a', 'Image': 'a',
            'Numéro': 'a', 'Pages': 'a', 'Prix': 'a', 'Scénario': 'a',
            'Synopsis': 'a', 'Série': 'a', 'Éditeur': 'a'})
        self.assertEqual(
            ["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "", "a", "", "", "", "", "", "", "a", "a"],
            liste)

    def test_raise_error_convert_list_from_empty_dict(self) -> None:
        with self.assertRaises(IndexError):
            self.service.map_to_list({})

    def test_add_album_successfully(self) -> None:
        self.assertEqual(ASTERIX, self.service.main(ASTERIX_ISBN))

    def test_raise_error_on_duplicate_isbn(self) -> None:
        self.service.main(ASTERIX_ISBN)
        with self.assertRaises(AlbumAlreadyExistsException):
            self.service.main(ASTERIX_ISBN)

    def test_raise_error_get_info_from_incorrect_isbn(self) -> None:
        with self.assertRaises(AlbumNotFoundException):
            self.service.main(0)


if __name__ == '__main__':
    unittest.main()
