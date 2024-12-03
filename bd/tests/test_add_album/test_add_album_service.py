import unittest

from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.add_album_service import AddAlbumService
from tests.test_add_album.data.album_data_set import ASTERIX_ISBN, ASTERIX
from tests.test_add_album.internal.bd_in_memory import BdInMemory
from tests.test_add_album.internal.sheet_in_memory import SheetInMemory


class TestAddAlbumService(unittest.TestCase):
    NB_COLUMN = 20

    @classmethod
    def setUpClass(cls):
        cls.sheet_repository = SheetInMemory()
        cls.bd_repository = BdInMemory()

    def tearDown(self):
        # After each
        self.sheet_repository.delete_row(0)

    def test_convert_list_from_dict_empty_value_successfully(self):
        self.service = AddAlbumService(0, [self.bd_repository], self.sheet_repository)
        liste = self.service.map_to_list({
            'Album': '', 'Couleurs': '', 'Date de publication': '',
            'Dessin': '', 'Édition': '', 'ISBN': '', 'Image': '',
            'Numéro': '', 'Pages': '', 'Prix': '', 'Scénario': '',
            'Synopsis': '', 'Série': '', 'Éditeur': ''})
        self.assertEqual([""] * self.NB_COLUMN, liste)

    def test_convert_list_from_dict_successfully(self):
        self.service = AddAlbumService(0, [self.bd_repository], self.sheet_repository)
        liste = self.service.map_to_list({
                'Album': 'a', 'Couleurs': 'a', 'Date de publication': 'a',
                'Dessin': 'a', 'Édition': 'a', 'ISBN': 'a', 'Image': 'a',
                'Numéro': 'a', 'Pages': 'a', 'Prix': 'a', 'Scénario': 'a',
                'Synopsis': 'a', 'Série': 'a', 'Éditeur': 'a'})
        self.assertEqual(["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "", "a", "", "", "", "", "", "a", "a"],
                         liste)

    def test_raise_error_convert_list_from_empty_dict(self):
        with self.assertRaises(IndexError):
            self.service.map_to_list({})

    def test_add_album_successfully(self):
        self.service = AddAlbumService(ASTERIX, [self.bd_repository], self.sheet_repository)
        self.assertEqual(ASTERIX, self.service.main())

    def test_raise_error_on_duplicate_isbn(self):
        self.service = AddAlbumService(ASTERIX, [self.bd_repository], self.sheet_repository)
        self.service.main()
        with self.assertRaises(AddAlbumError):
            self.service.main()

    def test_raise_error_get_info_from_incorrect_isbn(self):
        self.service = AddAlbumService(0, [self.bd_repository], self.sheet_repository)
        with self.assertRaises(AddAlbumError):
            self.service.main()


if __name__ == '__main__':
    unittest.main()