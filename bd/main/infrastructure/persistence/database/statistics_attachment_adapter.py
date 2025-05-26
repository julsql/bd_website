import os

from main.core.common.data.const import SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER
from main.domain.model.statistics import Statistics
from main.domain.ports.repositories.attachment_repository import AttachmentRepository


class StatisticsAttachmentAdapter(AttachmentRepository):
    def __init__(self, dedicaces_path: str = SIGNED_COPY_FOLDER,
                 exlibris_path: str = EXLIBRIS_FOLDER):
        self.dedicaces_path = dedicaces_path
        self.exlibris_path = exlibris_path

    def get_attachment_statistics(self) -> Statistics:
        nombre_dedicaces = count_total_jpeg_images(self.dedicaces_path)
        nombre_exlibris = count_total_jpeg_images(self.exlibris_path)

        return Statistics(
            nombre_albums=0,
            nombre_pages=0,
            prix_total=0,
            nombre_editions_speciales=0,
            nombre_dedicaces=nombre_dedicaces,
            nombre_exlibris=nombre_exlibris
        )


def count_total_jpeg_images(image_folder: str) -> int:
    if not os.path.exists(image_folder):
        return 0

    total_images = 0
    for root, _, files in os.walk(image_folder):
        total_images += sum(1 for file in files if file.lower().endswith('.jpeg'))

    return total_images
