from main.domain.exceptions.album_exceptions import AlbumNotFoundException
from main.domain.ports.repositories.album_repository import AlbumRepository


class BdInMemoryError(AlbumRepository):
    def __init__(self, name: str) -> None:
        self.name = name

    def get_infos(self, isbn: int) -> dict:
        return {}

    def get_url(self, isbn: int) -> str:
        return f"http://mock-{self.name}.com/{isbn}"

    def get_html(self, url: str) -> str:
        raise AlbumNotFoundException(f"Impossible d'affiche le code html de la page {url}")

    def __str__(self) -> str:
        return self.name
