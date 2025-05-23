from main.domain.ports.repositories.logger_repository import LoggerRepository


class LoggingService:
    def __init__(self, logger: LoggerRepository):
        self._logger = logger

    def info(self, message: str, **kwargs) -> None:
        self._logger.info(message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        self._logger.warning(message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        self._logger.error(message, **kwargs)

    def debug(self, message: str, **kwargs) -> None:
        self._logger.debug(message, **kwargs)
