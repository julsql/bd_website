import os

from main.core.domain.model.attachment import Attachment
from main.core.domain.model.attachments import Attachments
from main.core.domain.ports.repositories.attachments_repository import AttachmentsRepository
from main.core.infrastructure.persistence.database.models.bd import BD
from main.core.infrastructure.persistence.file.filesystem_adapter import count_images_in_directory
from main.core.infrastructure.persistence.file.paths import SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER


class AttachmentsAdapter(AttachmentsRepository):
    def __init__(self, signed_copy_path: str = SIGNED_COPY_FOLDER,
                 exlibris_path: str = EXLIBRIS_FOLDER):
        self.signed_copy_path = signed_copy_path
        self.exlibris_path = exlibris_path

    def get_attachments(self, path: str) -> Attachments:
        image_folder = path
        infos = []
        if image_folder and os.path.exists(image_folder):
            for item in os.listdir(image_folder):
                item_path = os.path.join(image_folder, item)

                # Vérifiez si l'élément est un répertoire
                if os.path.isdir(item_path):
                    isbn = item
                    nb_attachments = count_images_in_directory(item_path)
                    result = BD.objects.filter(isbn=isbn).values('album', 'number', 'series').first()
                    if result is None:
                        attachment = Attachment(
                            isbn=int(isbn), title="", number="", series="", total=nb_attachments
                        )
                        infos.append(attachment)
                    else:
                        attachment = Attachment(
                            isbn=int(isbn),
                            title=result["album"],
                            number=result["number"],
                            series=result["series"],
                            total=nb_attachments
                        )
                        infos.append(attachment)

        return Attachments(attachments_list=infos)
