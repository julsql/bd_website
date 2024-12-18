import unittest

from main.core.existing_album.existing_album_service import ExistingAlbumService
from tests.album_data_set import ASTERIX_LIST, ASTERIX_ISBN
from main.core.common.sheet.internal.sheet_in_memory import SheetInMemory


class TestExistingAlbumService(unittest.TestCase):

    INEXISTANT_ISBN = 9791038203907

    @classmethod
    def setUpClass(cls) -> None:
        sheet_repository = SheetInMemory()
        sheet_repository.append(ASTERIX_LIST)
        cls.service = ExistingAlbumService(sheet_repository)

    def test_already_exists(self) -> None:
        self.assertTrue(self.service.main(ASTERIX_ISBN))

    def test_dont_exists(self) -> None:
        self.assertFalse(self.service.main(self.INEXISTANT_ISBN))


if __name__ == '__main__':
    unittest.main()
