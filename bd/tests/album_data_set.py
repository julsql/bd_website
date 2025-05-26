from main.domain.model.bd import BD
from tests.test_add_album.album_large_data_set import ASTERIX_DATA

# Structures de données communes
COLUMN_HEADERS = {
    'SHEET': [
        "ISBN", "Album", "Numéro", "Série", "Scénariste", "Dessinateur", "Couleur",
        "Éditeur", "Date de parution", "Édition", "Nombre de planches", "Cote",
        "Prix d'achat", "Année d'achat", "Lieu d'achat", "Tirage de tête",
        "Dédicace", "Ex Libris", "Emplacement", "Synopsis", "Image"
    ],
    'DATABASE': [
        'isbn', 'album', 'number', 'series', 'writer', 'illustrator', 'colorist',
        'publisher', 'publication_date', 'edition', 'number_of_pages', 'rating',
        'purchase_price', 'year_of_purchase', 'place_of_purchase', 'deluxe_edition',
        "localisation", 'synopsis', 'image'
    ],
}

# Données consolidées
ASTERIX = ASTERIX_DATA['BDPHILE']
ASTERIX_ALBUM = BD.from_album(ASTERIX)

# Formats de liste
ASTERIX_LIST = [str(val) if val else "" for val in ASTERIX_ALBUM.to_list()]

# Format base de données
ALBUM_EXEMPLE = ASTERIX_ALBUM.copy()
ALBUM_EXEMPLE.rating = 10.0
ALBUM_EXEMPLE.year_of_purchase = 2025
ALBUM_EXEMPLE.place_of_purchase = "Lyon"

# Formats de dictionnaire
ALBUM_EXEMPLE_DICT = ALBUM_EXEMPLE.to_dict()

# Lignes des données
FIRST_LINE_SHEET = COLUMN_HEADERS["SHEET"]
FIRST_LINE_DATABASE = COLUMN_HEADERS["DATABASE"]
