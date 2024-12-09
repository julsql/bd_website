import logging

from config.settings import LOGS_FILE


class AppLogger(logging.Logger):
    def __init__(self, name):
        super().__init__(name)

    def _log_with_isbn(self, level, msg, args, **kwargs):
        # Vérifier s'il y a 'isbn' dans 'extra' et l'ajouter au message
        isbn = kwargs.get('isbn', '')
        msg = f"{msg} - {isbn}" if isbn else msg
        super()._log(level, msg, args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._log_with_isbn(logging.INFO, msg, args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._log_with_isbn(logging.DEBUG, msg, args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._log_with_isbn(logging.WARNING, msg, args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._log_with_isbn(logging.ERROR, msg, args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._log_with_isbn(logging.CRITICAL, msg, args, **kwargs)

logging.setLoggerClass(AppLogger)
logger = logging.getLogger("app_logger")

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=LOGS_FILE
)