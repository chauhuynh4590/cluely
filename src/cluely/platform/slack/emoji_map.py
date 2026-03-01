"""Mapping of Slack flag emoji names to ISO 639-1 language codes.

Slack uses country flag emoji names like 'flag-fr' or 'fr'.
We map these to language codes for the Reacjilator-style translation UX.
"""

from __future__ import annotations

# Slack flag emoji name -> ISO 639-1 language code
FLAG_TO_LANGUAGE: dict[str, str] = {
    # Common flags
    "flag-us": "en",
    "flag-gb": "en",
    "us": "en",
    "gb": "en",
    "flag-es": "es",
    "es": "es",
    "flag-fr": "fr",
    "fr": "fr",
    "flag-de": "de",
    "de": "de",
    "flag-it": "it",
    "it": "it",
    "flag-pt": "pt",
    "flag-br": "pt",
    "pt": "pt",
    "br": "pt",
    "flag-jp": "ja",
    "jp": "ja",
    "flag-kr": "ko",
    "kr": "ko",
    "flag-cn": "zh",
    "cn": "zh",
    "flag-ru": "ru",
    "ru": "ru",
    "flag-sa": "ar",
    "flag-ae": "ar",
    "flag-in": "hi",
    "in": "hi",
    "flag-th": "th",
    "th": "th",
    "flag-vn": "vi",
    "vn": "vi",
    "flag-nl": "nl",
    "nl": "nl",
    "flag-pl": "pl",
    "pl": "pl",
    "flag-tr": "tr",
    "tr": "tr",
    "flag-se": "sv",
    "se": "sv",
    "flag-dk": "da",
    "dk": "da",
    "flag-fi": "fi",
    "fi": "fi",
    "flag-no": "no",
    "no": "no",
    "flag-cz": "cs",
    "cz": "cs",
    "flag-gr": "el",
    "gr": "el",
    "flag-il": "he",
    "flag-id": "id",
    "flag-my": "ms",
    "flag-ro": "ro",
    "ro": "ro",
    "flag-ua": "uk",
    "ua": "uk",
    "flag-bg": "bg",
    "bg": "bg",
    "flag-hr": "hr",
    "hr": "hr",
    "flag-sk": "sk",
    "sk": "sk",
    "flag-si": "sl",
    "flag-ee": "et",
    "flag-lv": "lv",
    "flag-lt": "lt",
    "flag-hu": "hu",
    "hu": "hu",
}


def get_language_from_emoji(emoji_name: str) -> str | None:
    """Return the language code for a flag emoji name, or None if not recognized."""
    return FLAG_TO_LANGUAGE.get(emoji_name)
