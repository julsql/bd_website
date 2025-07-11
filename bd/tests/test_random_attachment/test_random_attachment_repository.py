import os
import sys
import tempfile
import unittest

import django

from main.core.domain.model.attachment_type import AttachmentType
from main.core.infrastructure.persistence.file.paths import SIGNED_COPY_PATH, EXLIBRIS_PATH
from main.core.infrastructure.persistence.file.random_attachment_adapter import RandomAttachmentAdapter

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


class TestRandomAttachmentRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.temp_dir = tempfile.TemporaryDirectory()

        collection_id = 1
        # Création des chemins temporaires
        cls.SIGNED_COPY_FOLDER = os.path.join(cls.temp_dir.name, SIGNED_COPY_PATH(collection_id))
        cls.EXLIBRIS_FOLDER = os.path.join(cls.temp_dir.name, EXLIBRIS_PATH(collection_id))

        # Création des dossiers nécessaires
        os.makedirs(cls.SIGNED_COPY_FOLDER, exist_ok=True)
        os.makedirs(cls.EXLIBRIS_FOLDER, exist_ok=True)

        cls.repository = RandomAttachmentAdapter()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_dir.cleanup()
        super().tearDownClass()

    def setUp(self) -> None:
        super().setUp()
        # Nettoyage des dossiers temporaires
        for folder in [self.SIGNED_COPY_FOLDER, self.EXLIBRIS_FOLDER]:
            for root, dirs, files in os.walk(folder, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

    def create_test_image(self, base_folder: str, isbn: str, filename: str) -> str:
        """Utilitaire pour créer une image de test"""
        album_folder = os.path.join(base_folder, isbn)
        os.makedirs(album_folder, exist_ok=True)
        image_path = os.path.join(album_folder, filename)
        with open(image_path, 'w') as f:
            f.write("test image content")
        return image_path

    def test_get_all_images_path_empty_directories(self):
        # Act
        result = self.repository.get_all_images_path([self.SIGNED_COPY_FOLDER, self.EXLIBRIS_FOLDER])

        # Assert
        self.assertEqual([], result)

    def test_get_all_images_path_with_images(self):
        # Arrange
        self.create_test_image(self.SIGNED_COPY_FOLDER, "12345", "test1.jpg")
        self.create_test_image(self.EXLIBRIS_FOLDER, "67890", "test2.png")

        # Act
        result = self.repository.get_all_images_path([self.SIGNED_COPY_FOLDER, self.EXLIBRIS_FOLDER])

        # Assert
        self.assertEqual(2, len(result))
        self.assertTrue(any("12345" in path for path in result))
        self.assertTrue(any("67890" in path for path in result))

    def test_get_all_images_path_invalid_directory(self):
        # Act
        result = self.repository.get_all_images_path(["/invalid/path"])

        # Assert
        self.assertEqual([], result)

    def test_get_all_images_path_filters_non_images(self):
        # Arrange
        album_folder = os.path.join(self.SIGNED_COPY_FOLDER, "12345")
        os.makedirs(album_folder, exist_ok=True)
        with open(os.path.join(album_folder, "test.txt"), 'w') as f:
            f.write("not an image")
        self.create_test_image(self.SIGNED_COPY_FOLDER, "12345", "valid.jpg")

        # Act
        result = self.repository.get_all_images_path([self.SIGNED_COPY_FOLDER])

        # Assert
        self.assertEqual(1, len(result))
        self.assertTrue(result[0].endswith("valid.jpg"))

    def test_get_random_attachment_empty_list(self):
        # Act/Assert
        with self.assertRaises(IndexError):
            self.repository.get_random_attachment([])

    def test_get_random_attachment_single_image(self):
        # Arrange
        image_path = "dedicaces/12345/test.jpg"

        # Act
        banner = self.repository.get_random_attachment([image_path])

        # Assert
        self.assertTrue(banner.path.endswith(image_path))
        self.assertEqual(12345, banner.isbn)
        self.assertEqual(AttachmentType.SIGNED_COPY, banner.type)

    def test_get_random_attachment_maintains_structure(self):
        # Arrange
        test_images = [
            "dedicaces/12345/test1.jpg",
            "exlibris/67890/test2.jpg"
        ]

        # Act
        results = set()
        for _ in range(10):  # Plusieurs essais pour tester le caractère aléatoire
            banner = self.repository.get_random_attachment(test_images)
            results.add(banner)

        # Assert
        self.assertLessEqual(len(results), 2)  # Il ne devrait pas y avoir plus de résultats que d'images
        for banner in results:
            self.assertTrue(any(banner.path.endswith(img) for img in test_images))
            self.assertIn(banner.isbn, [12345, 67890])
            self.assertIn(banner.type, [AttachmentType.SIGNED_COPY, AttachmentType.EXLIBRIS])

    def test_list_files_in_subdirectories_valid_extensions(self):
        # Arrange
        extensions = ['.jpg', '.jpeg', '.png']
        for ext in extensions:
            self.create_test_image(self.SIGNED_COPY_FOLDER, "12345", f"test{ext}")

        # Act
        result = self.repository.list_files_in_subdirectories(self.SIGNED_COPY_FOLDER)

        # Assert
        self.assertEqual(len(extensions), len(result))
        for file in result:
            self.assertTrue(any(file.lower().endswith(ext) for ext in extensions))


if __name__ == '__main__':
    unittest.main()
