from typing import Optional

from .patterns import IS_JBL


def is_typo(text: str) -> Optional[int]:
    """Since some surnames are not properly fetched, are nuanced, or have bad spelling, get the primary key on match of the given text"""
    return possible_pattern(text) or bad_spelling(text)


def bad_spelling(text: str):
    if text == "Ynares-Satiago":
        return 145  # Ynares-Santiago
    elif text == "Bellosiillo":
        return 127  # Bellosillo
    elif text == "Ferran":
        return 111  # Fernan
    elif text == "John":
        return 23  # Fernan
    elif text == "Avancea'A":
        return 18
    return None


def possible_pattern(text: str) -> Optional[int]:
    if IS_JBL.search(text):
        return 64
    elif "Bengzon" in text.title():
        return 76
    elif "Bautista" in text.title():
        return 59
    elif "Reyes, A." in text.title():
        return 177
    elif "A. Reyes" in text.title():
        return 177
    elif "Reyes, R.T." in text.title():
        return 159
    return None
