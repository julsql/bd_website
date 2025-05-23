from abc import ABC

from main.domain.ports.repositories.album_repository import AlbumRepository
from main.domain.ports.repositories.logger_repository import LoggerRepository
from main.infrastructure.api.internal.date_parser_service import DateParserService


class BaseAlbumAdapter(AlbumRepository, ABC):
    def __init__(self, logging_repository: LoggerRepository):
        self.logging_repository = logging_repository

    def _parse_publication_date(self, informations: dict, isbn: int) -> None:
        date_string = informations.get("Date de publication", "")
        if date_string:
            parsed_date = DateParserService.parse_date(date_string)
            if parsed_date:
                informations["Date de publication"] = parsed_date
            else:
                self.logging_repository.warning(
                    f"Problème de parsing de la date: {date_string}",
                    isbn=isbn
                )
