import logging

class CustomLogger(logging.Logger):
    def __init__(self, name):
        super().__init__(name)

    def _log_with_isbn(self, level, msg, args, **kwargs):
        # Vérifier s'il y a 'isbn' dans 'extra' et l'ajouter au message
        isbn = kwargs.get('isbn', '')  # Récupérer 'isbn' si présent dans 'extra'
        # Modifier le message pour ajouter l'ISBN si nécessaire
        msg = f"{msg} - {isbn}" if isbn else msg
        # Appeler la méthode de log classique avec le message modifié
        super()._log(level, msg, args, **kwargs)

    def info(self, msg, *args, **kwargs):
        # Surcharge de la méthode info
        self._log_with_isbn(logging.INFO, msg, args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        # Surcharge de la méthode debug
        self._log_with_isbn(logging.DEBUG, msg, args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        # Surcharge de la méthode warning
        self._log_with_isbn(logging.WARNING, msg, args, **kwargs)

    def error(self, msg, *args, **kwargs):
        # Surcharge de la méthode error
        self._log_with_isbn(logging.ERROR, msg, args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        # Surcharge de la méthode critical
        self._log_with_isbn(logging.CRITICAL, msg, args, **kwargs)

# Configuration du logging avec un logger personnalisé
logging.setLoggerClass(CustomLogger)
logger = logging.getLogger("custom_logger")

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format sans 'isbn'
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='app.log'
)
