import re

import requests
from bs4 import BeautifulSoup

from main.domain.exceptions.api_exceptions import ApiConnexionException, ApiConnexionRefused, ApiConnexionDataNotFound
from main.infrastructure.api.base_album_adapter import BaseAlbumAdapter


class BdGestAdapter(BaseAlbumAdapter):
    SEARCH_URL = "https://www.bedetheque.com/search/albums"
    BANDEAU_CLASS = "bandeau-info album panier"
    IMAGE_CLASS = "bandeau-image album"
    BS_FEATURE = 'html.parser'

    def __str__(self) -> str:
        return "BdGestRepository"

    def get_infos(self, isbn: int) -> dict[str, str | float | int]:
        informations = {}
        url = self.get_url(isbn)

        html = self.get_html(url)
        soup = BeautifulSoup(html, self.BS_FEATURE)

        # Extraction du titre
        self._extract_title(soup, informations, isbn)

        # Extraction des informations sur les auteurs
        self._extract_authors(soup, informations, isbn)

        # Extraction des informations supplémentaires
        self._extract_additional_info(soup, informations, isbn)

        # Extraction le prix
        self._extract_price(soup, informations, isbn)

        # Image
        self._extract_image(soup, informations, isbn)

        # Synopsis
        self._extract_synopsis(soup, informations, isbn)

        # Date de publication
        self._parse_publication_date(informations, isbn)

        self.logging_repository.info(str(informations), extra={"isbn": isbn})
        return informations

    def _extract_title(self, soup: BeautifulSoup, informations: dict, isbn: int) -> None:
        """ Extraire les informations du titre """
        full_title = self._get_input(soup, "AltTitle")
        if full_title:
            pattern = r'-([^-\s]+)-'
            match = re.search(pattern, full_title)

            if not match:
                raise ValueError("Format de titre invalide : le numéro de tome est introuvable")

            # Découpe aux positions trouvées
            tome = match.group(1)
            serie = full_title[:match.start()].strip()
            album = full_title[match.end():].strip()
            if tome:
                informations["Numéro"] = tome
            if serie:
                informations["Série"] = serie
            if album:
                informations["Album"] = album
        else:
            self.logging_repository.warning("Impossible d'extraire le titre", extra={"isbn": isbn})
        return None

    def _extract_authors(self, soup: BeautifulSoup, informations: dict, isbn: int) -> None:
        """ Extraire les informations supplémentaires """
        keys = ['Scénario', 'Dessin', 'Couleurs']
        album_tag = soup.find("div", class_=self.BANDEAU_CLASS)
        if not album_tag:
            self.logging_repository.warning("Informations supplémentaires non trouvées", extra={"isbn": isbn})
            return

        sub_title = album_tag.find("h3")
        if not sub_title:
            self.logging_repository.warning("Éditeur non trouvé", extra={"isbn": isbn})
            return
        editor_tag = sub_title.find('span', {"itemprop": "publisher"})
        if not editor_tag:
            self.logging_repository.warning("Éditeur non trouvé", extra={"isbn": isbn})
            return
        informations["Éditeur"] = editor_tag.get_text()

        auteur_tag = album_tag.find("div", class_="liste-auteurs")
        if not editor_tag:
            self.logging_repository.warning("Créateurs non trouvés", extra={"isbn": isbn})
            return

        auteurs = auteur_tag.select("a")
        metiers = auteur_tag.select(".metier")

        # Remplir le dictionnaire avec les auteurs et leurs métiers
        for auteur, metier in zip(auteurs, metiers):
            nom = auteur.text.strip()
            if ", " in nom:
                name, surname = nom.split(", ")
                nom = f"{surname} {name}"

            categorie = metier.text.strip("()")  # Enlever les parenthèses
            if categorie in keys:
                if categorie in informations:
                    informations[categorie] = f"{informations[categorie]},{nom}"
                else:
                    informations[categorie] = nom

    def _extract_additional_info(self, soup: BeautifulSoup, informations: dict, isbn: int) -> None:
        """ Extraire les informations supplémentaires """

        album_tag = soup.find("div", class_=self.BANDEAU_CLASS)

        info_tag = album_tag.find("h4")
        date_tag = info_tag.find('span', {"title": "Dépot légal"}).get_text()

        # Vérifier s'il y a une date entre parenthèses (ex: 08 février 2023)
        match_precise = re.search(r"\((\d{2}) (\w+) (\d{4})\)", date_tag)

        if match_precise:
            # Si une date précise est trouvée, on la récupère
            jour, mois_fr, annee = match_precise.groups()
        else:
            # Sinon, on récupère la date générique au début (MM/YYYY)
            match_generale = re.search(r"(\d{2})/(\d{4})", date_tag)
            mois_fr, annee = match_generale.groups()
            jour = "01"  # On met par défaut le premier jour du mois

        informations['Date de publication'] = f"{annee}-{mois_fr}-{jour}"

        page_tag = info_tag.find('span', {"itemprop": "numberOfPages"}).get_text()

        try:
            informations["Pages"] = int(page_tag)
        except ValueError:
            self.logging_repository.warning(f"{page_tag} est un nombre de planches incorrect", extra={"isbn": isbn})

    def _get_input(self, soup: BeautifulSoup, id: str):
        tag = soup.find("input", {"id": id})
        if tag:
            return tag.get("value")
        else:
            return None

    def _extract_price(self, soup: BeautifulSoup, informations: dict, isbn: int) -> None:
        """ Extraire le prix """
        album_id = self._get_input(soup, "IdAlbum")
        eans = self._get_input(soup, "EANs")
        ean = self._get_input(soup, "EAN")

        if album_id and eans and ean:
            url = f"https://www.bedetheque.com/ajax/album_bdfugue/idalbum/{album_id}/idbdfugue/{ean}/id/{eans}"
            response = requests.get(url)

            if response.status_code == 200:
                result = response.json()
                if 'price' in result:
                    informations["Prix"] = float(result['price'])
        else:
            self.logging_repository.warning("Impossible d'extraire le prix", extra={"isbn": isbn})
        return None

    def _extract_image(self, soup: BeautifulSoup, informations: dict, isbn: int) -> None:
        """ Extraire l'image """
        body = soup.find("div", class_=self.IMAGE_CLASS)
        if not body:
            self.logging_repository.warning("Image non trouvée", extra={"isbn": isbn})
            return
        a_tag = body.find("a") if body else None
        if not a_tag:
            self.logging_repository.warning("Image non trouvée", extra={"isbn": isbn})
            return
        informations['Image'] = a_tag.get('href')

    def _extract_synopsis(self, soup: BeautifulSoup, informations: dict, isbn: int) -> None:
        """ Extraire le synopsis """
        album_id = self._get_input(soup, "IdAlbum")

        if album_id:
            url = f"https://www.bedetheque.com/ajax/resume/album/{album_id}"
            response = requests.get(url)

            if response.status_code == 200:
                result = response.text
                informations["Synopsis"] = result
        else:
            self.logging_repository.warning("Impossible d'extraire le synppsis", extra={"isbn": isbn})
        return None

    def get_url(self, isbn: int) -> str:
        """Trouver lien BD bdgest.fr à partir de son ISBN"""

        with requests.Session() as session:
            csrf_token = self.get_csrf_token(session)
            params = {
                "csrf_token_bel": csrf_token,
                "RechISBN": isbn
            }
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Referer": self.SEARCH_URL
            }
            response = session.get(self.SEARCH_URL, params=params, headers=headers)

            if response.status_code != 200:
                self.logging_repository.error(f"La requête a échoué. Statut de la réponse : {response.status_code}",
                                              extra={"isbn": isbn})
                raise ApiConnexionException(f"Impossible d'affiche le code html de la page {self.SEARCH_URL}",
                                            str(self))

            html = response.text

            soup = BeautifulSoup(html, self.BS_FEATURE)
            search_list = soup.find("ul", class_="search-list")

            # Trouver le premier <li> dans cette liste
            first_li = search_list.find("li") if search_list else None

            # Trouver la première balise <a> avec la classe "image-tooltip"
            a_tag = first_li.find("a", class_="image-tooltip") if first_li else None
            if a_tag:
                return a_tag.get('href')
            else:
                raise ApiConnexionDataNotFound(f"ISBN {isbn} introuvable", str(self), isbn)

    def get_html(self, url: str) -> str:
        response = requests.get(url)
        # Vérifiez si la requête a réussi
        if response.status_code == 200:
            return response.text
        else:
            self.logging_repository.error(f"La requête a échoué. Statut de la réponse : {response.status_code}")
            raise ApiConnexionException(f"Impossible d'affiche le code html de la page {url}", str(self))

    def get_csrf_token(self, session):
        """Récupère dynamiquement le token CSRF depuis la page de recherche."""
        response = session.get(self.SEARCH_URL)

        if response.status_code != 200:
            raise ApiConnexionException(f"Erreur {response.status_code} lors de l'accès au site.", str(self))

        soup = BeautifulSoup(response.text, self.BS_FEATURE)

        # Trouver le champ input contenant le token CSRF
        csrf_input = soup.find("input", {"name": "csrf_token_bel"})

        if csrf_input:
            return csrf_input["value"]
        else:
            raise ApiConnexionRefused("Impossible de récupérer le token CSRF.", str(self))
