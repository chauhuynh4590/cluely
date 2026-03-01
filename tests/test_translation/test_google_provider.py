from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from cluely.translation.base import TranslationError
from cluely.translation.google_provider import GoogleProvider


@pytest.fixture
def provider():
    return GoogleProvider()


def test_provider_name(provider):
    assert provider.name == "google"


def test_supported_languages(provider):
    langs = provider.supported_languages()
    assert isinstance(langs, list)
    assert len(langs) > 0


@pytest.mark.asyncio
async def test_translate_success(provider):
    with patch("cluely.translation.google_provider.GoogleTranslator") as mock_cls:
        mock_translator = MagicMock()
        mock_translator.translate.return_value = "Hola mundo"
        mock_cls.return_value = mock_translator

        result = await provider.translate("Hello world", target_language="es")

    assert result.translated_text == "Hola mundo"
    assert result.target_language == "es"
    assert result.original_text == "Hello world"
    assert result.provider_name == "google"


@pytest.mark.asyncio
async def test_translate_with_source_language(provider):
    with patch("cluely.translation.google_provider.GoogleTranslator") as mock_cls:
        mock_translator = MagicMock()
        mock_translator.translate.return_value = "Bonjour le monde"
        mock_cls.return_value = mock_translator

        result = await provider.translate(
            "Hello world", target_language="fr", source_language="en"
        )

    assert result.translated_text == "Bonjour le monde"
    assert result.source_language == "en"
    mock_cls.assert_called_once_with(source="en", target="fr")


@pytest.mark.asyncio
async def test_translate_error(provider):
    with patch("cluely.translation.google_provider.GoogleTranslator") as mock_cls:
        mock_translator = MagicMock()
        mock_translator.translate.side_effect = Exception("network error")
        mock_cls.return_value = mock_translator

        with pytest.raises(TranslationError, match="Google Translate error"):
            await provider.translate("Hello", target_language="es")
