import os
import sys
import unittest
from datetime import date

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from main.core.infrastructure.persistence.database.random_album_adapter import RandomAlbumAdapter
from main.core.domain.model.album import Album
from main.models import AppUser
from main.core.infrastructure.persistence.database.models.bd import BD
from main.core.infrastructure.persistence.database.models.collection import Collection


class TestRandomAlbumConnexion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.repository = RandomAlbumAdapter()

        user = AppUser.objects.get(username="admin")
        cls.collection = Collection.objects.get(accounts=user)
        cls.collection_id = cls.collection.id

    def setUp(self):
        # Nettoyage de la base avant chaque test
        BD.objects.filter(collection=self.collection).delete()

        self.bd1 = {
            'isbn': 123456789,
            'album': "Astérix le Gaulois",
            'number': "1",
            'series': "Astérix",
            'writer': "René Goscinny",
            'illustrator': "Albert Uderzo",
            'image': "asterix.jpg",
            'publication_date': date(1961, 10, 29),
            'purchase_price': 15.0,
            'number_of_pages': 48,
            'edition': "Standard",
            'synopsis': "Les aventures d'Astérix",
            'deluxe_edition': False
        }
        self.bd2 = {
            'isbn': 987654321,
            'album': "Tintin au Tibet",
            'number': "20",
            'series': "Les aventures de Tintin",
            'writer': "Hergé",
            'illustrator': "Hergé",
            'image': "tintin.jpg",
            'publication_date': date(1960, 1, 1),
            'purchase_price': 20.99,
            'number_of_pages': 62,
            'edition': "Deluxe",
            'synopsis': "Tintin part au Tibet",
            'deluxe_edition': False
        }

        # Création de données de test
        BD.objects.create(
            **self.bd1,
            collection=self.collection
        )

        BD.objects.create(
            **self.bd2,
            collection=self.collection
        )

    def tearDown(self):
        BD.objects.filter(collection=self.collection).delete()

    def test_get_random_album_empty_database(self):
        # Arrange
        BD.objects.filter(collection=self.collection).delete()

        # Act
        result = self.repository.get_random_album(self.collection_id)

        # Assert
        self.assertTrue(result.is_empty())

    def test_get_random_album_returns_dict_with_correct_fields(self):
        # Act
        result = self.repository.get_random_album(self.collection_id)

        # Assert
        self.assertIsInstance(result, Album)

    def test_get_random_album_integer_price(self):
        # Arrange
        BD.objects.filter(collection=self.collection).delete()
        BD.objects.create(
            isbn="111111111",
            album="Test Album",
            purchase_price=25.0,
            deluxe_edition=False,
            collection=self.collection
        )

        # Act
        result = self.repository.get_random_album(self.collection_id)

        # Assert
        self.assertEqual(25, result.purchase_price)

    def test_get_random_album_float_price(self):
        # Arrange
        BD.objects.filter(collection=self.collection).delete()
        BD.objects.create(
            isbn="111111111",
            album="Test Album",
            purchase_price=25.99,
            deluxe_edition=False,
            collection=self.collection
        )

        # Act
        result = self.repository.get_random_album(self.collection_id)

        # Assert
        self.assertEqual(25.99, float(result.purchase_price))

    def test_get_random_album_returns_valid_data(self):
        # Act
        result = self.repository.get_random_album(self.collection_id)

        # Assert
        self.assertIn(result.isbn, [123456789, 987654321])
        if result.isbn == self.bd1['isbn']:
            bd = self.bd1
        else:
            bd = self.bd2

        self.assertEqual(bd['album'], result.title)
        self.assertEqual(bd['number'], result.number)
        self.assertEqual(bd['series'], result.series)
        self.assertEqual(bd['writer'], result.writer)
        self.assertEqual(bd['illustrator'], result.illustrator)
        self.assertEqual(bd['image'], result.image)
        self.assertEqual(bd['publication_date'], result.publication_date)
        self.assertEqual(bd['purchase_price'], float(result.purchase_price))
        self.assertEqual(bd['number_of_pages'], result.number_of_pages)
        self.assertEqual(bd['edition'], result.edition)
        self.assertEqual(bd['synopsis'], result.synopsis)


if __name__ == '__main__':
    unittest.main()
