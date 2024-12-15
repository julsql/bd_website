from typing import Dict
import os
from django.conf import settings

from main.core.common.database.internal.bd_model import BD


class AttachmentsService:
    def main(self) -> Dict[str, str]:
        signed_copies, signed_copy_sum = self.dedicaces()
        exlibris, exlibris_sum = self.exlibris()
        return {'signed_copies': signed_copies, 'signed_copy_sum': signed_copy_sum,
                'exlibris': exlibris, 'exlibris_sum': exlibris_sum}

    def dedicaces(self):
        image_dir = os.path.join(settings.BASE_DIR, "main/static/main/images/dedicaces")
        infos = []
        dedicaces_sum = 0
        for item in os.listdir(image_dir):
            item_path = os.path.join(image_dir, item)

            # Vérifiez si l'élément est un répertoire
            if os.path.isdir(item_path):
                isbn = item
                nb_dedicace = self.count_images_in_directory(item_path)
                result = BD.objects.filter(isbn=isbn).values('album', 'number', 'series').first()
                dedicaces_sum += nb_dedicace
                if result is None:
                    infos.append({'isbn': isbn, 'album': "", 'number': "", 'series': "",
                                  'signes_copy_range': range(1, nb_dedicace + 1), 'signed_copy': nb_dedicace})
                else:

                    infos.append({'isbn': isbn, 'album': result["album"], 'number': result["number"], 'series': result["series"],
                                  'signes_copy_range': range(1, nb_dedicace + 1), 'signed_copy': nb_dedicace})
        return infos, dedicaces_sum


    def exlibris(self):
        image_dir = os.path.join(settings.BASE_DIR, "main/static/main/images/exlibris")
        infos = []
        exlibris_sum = 0
        for item in os.listdir(image_dir):
            item_path = os.path.join(image_dir, item)

            # Vérifiez si l'élément est un répertoire
            if os.path.isdir(item_path):
                isbn = item
                nb_exlibris = self.count_images_in_directory(item_path)
                result = BD.objects.filter(isbn=isbn).values('album', 'number', 'series').first()
                exlibris_sum += nb_exlibris
                if result is None:
                    infos.append({'isbn': isbn, 'album': "", 'number': "", 'series': "",
                                  'ex_libris_range': range(1, nb_exlibris + 1), 'ex_libris': nb_exlibris})
                else:
                    infos.append({'isbn': isbn, 'album': result["album"], 'number': result["number"], 'series': result["series"],
                                  'ex_libris_range': range(1, nb_exlibris + 1), 'ex_libris': nb_exlibris})
        return infos, exlibris_sum


    def count_images_in_directory(self, directory_path):
        if not os.path.isdir(directory_path):
            return 0

        image_count = 0
        allowed_image_extensions = ".jpeg"

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_extension = os.path.splitext(file)[1].lower()
                if file_extension == allowed_image_extensions:
                    image_count += 1

        return image_count
