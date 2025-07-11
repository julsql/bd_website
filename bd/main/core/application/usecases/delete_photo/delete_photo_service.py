from main.core.domain.model.attachment_type import AttachmentType
from main.core.domain.ports.repositories.delete_photo_repository import DeletePhotoRepository
from main.core.infrastructure.persistence.file.paths import SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER


class DeletePhotoService:
    def __init__(self, photo_repository: DeletePhotoRepository) -> None:
        self.repository = photo_repository

    def main(self, isbn: int, photo_id: int, photo_type: AttachmentType, collection_id: int) -> bool:
        if photo_type == AttachmentType.SIGNED_COPY:
            return self.repository.delete_photo(isbn, photo_id, SIGNED_COPY_FOLDER(collection_id))
        elif photo_type == AttachmentType.EXLIBRIS:
            return self.repository.delete_photo(isbn, photo_id, EXLIBRIS_FOLDER(collection_id))
        else:
            raise ValueError('Unknown photo type')
