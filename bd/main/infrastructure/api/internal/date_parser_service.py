import re
from datetime import datetime
from typing import Optional


class DateParserService:
    MONTH_MAPPING = {
        "janv": "01", "janvier": "01",
        "févr": "02", "fev": "02", "février": "02",
        "mars": "03",
        "avr": "04", "avril": "04",
        "mai": "05",
        "juin": "06",
        "juil": "07", "juillet": "07",
        "août": "08", "aout": "08",
        "sept": "09", "septembre": "09",
        "oct": "10", "octobre": "10",
        "nov": "11", "novembre": "11",
        "déc": "12", "décembre": "12"
    }

    MONTH_TRANSLATIONS = {
        "janvier": "January",
        "février": "February",
        "fevrier": "February",
        "mars": "March",
        "avril": "April",
        "mai": "May",
        "juin": "June",
        "juillet": "July",
        "août": "August",
        "aout": "August",
        "septembre": "September",
        "octobre": "October",
        "novembre": "November",
        "décembre": "December",
        "decembre": "December",
    }

    @classmethod
    def parse_date(cls, date_string: str) -> Optional[str]:
        """Parse une date en format standardisé YYYY-MM-DD"""
        if not date_string:
            return None

        # Format YYYY-MM-DD
        try:
            return datetime.strptime(date_string, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            pass

        # Format YYYY-MM
        try:
            return datetime.strptime(date_string, "%Y-%m").strftime("%Y-%m-01")
        except ValueError:
            pass

        # Format YYYY
        if re.match(r'^\d{4}$', date_string):
            return f"{date_string}-01-01"

        # Format français avec point (8 févr. 2023)
        if '.' in date_string:
            try:
                jour, mois, annee = date_string.replace('.', '').split()
                mois_lower = mois.lower()
                if mois_lower in cls.MONTH_MAPPING:
                    return f"{annee}-{cls.MONTH_MAPPING[mois_lower]}-{int(jour):02d}"
            except (ValueError, KeyError):
                pass

        # Essayer avec la traduction en anglais pour dateutil.parser
        translated_date = cls._translate_month(date_string)
        try:
            from dateutil.parser import parse
            parsed_date = parse(translated_date, dayfirst=True, fuzzy=True)

            if re.match(r'^\d{4}$', date_string):
                return f"{parsed_date.year}-01-01"
            elif re.match(r'^\d{4}-\d{1,2}$', date_string) or len(date_string.split()) == 2:
                return f"{parsed_date.year}-{parsed_date.month:02d}-01"
            else:
                return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            return None

    @classmethod
    def _translate_month(cls, date: str) -> str:
        """Traduit les mois français en anglais pour le parsing"""
        date_lower = date.lower()
        for fr_month, en_month in cls.MONTH_TRANSLATIONS.items():
            if fr_month in date_lower:
                return date_lower.replace(fr_month, en_month)
        return date
