from main.domain.exceptions.album_exceptions import AlbumNotFoundException
from main.domain.ports.repositories.album_repository import AlbumRepository


class BdInMemory(AlbumRepository):

    def __init__(self, name: str, data: dict) -> None:
        self.name = name
        self.data = {int(data.get('ISBN', '0')): data}

    def get_infos(self, isbn: int) -> dict[str, str | float | int]:
        if isbn in self.data:
            return self.data[isbn]
        else:
            raise AlbumNotFoundException(f"Aucun album trouvé avec l'isbn {isbn}")

    def get_url(self, isbn: int) -> str:
        return f"http://mock-{self.name}.com/{isbn}"

    def get_html(self, url: str) -> str:
        return "<html><body><h1>Mock</h1></body></html>"

    def __str__(self) -> str:
        return self.name
