from typing import Any, Optional, Sequence

from main.domain.ports.repositories.reponse_repository import ResponseRepository


class ResponseService:
    def __init__(self, response_port: ResponseRepository):
        self._response_port = response_port

    def success(self, content: str, status: int = 200) -> Any:
        return self._response_port.success(content, status)

    def forbidden(self, content: str) -> Any:
        return self._response_port.forbidden(content)

    def not_found(self, content: str) -> Any:
        return self._response_port.not_found(content)

    def method_not_allowed(
            self,
            permitted_methods: Sequence[str],
            content: Optional[str] = None
    ) -> Any:
        return self._response_port.method_not_allowed(permitted_methods, content)

    def bad_request(self, content: str) -> Any:
        return self._response_port.bad_request(content)

    def server_error(self, content: str) -> Any:
        return self._response_port.server_error(content)
