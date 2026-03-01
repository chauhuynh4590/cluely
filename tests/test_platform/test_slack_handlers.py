from __future__ import annotations

import json

import pytest

from cluely.platform.slack.emoji_map import get_language_from_emoji
from cluely.platform.slack.modals import error_modal, language_selection_modal
from cluely.translation.cache import CachedTranslationProvider


def test_emoji_map_known_flags():
    assert get_language_from_emoji("flag-fr") == "fr"
    assert get_language_from_emoji("flag-jp") == "ja"
    assert get_language_from_emoji("flag-es") == "es"
    assert get_language_from_emoji("flag-us") == "en"
    assert get_language_from_emoji("flag-de") == "de"
    assert get_language_from_emoji("flag-cn") == "zh"


def test_emoji_map_short_codes():
    assert get_language_from_emoji("fr") == "fr"
    assert get_language_from_emoji("jp") == "ja"
    assert get_language_from_emoji("es") == "es"


def test_emoji_map_unknown():
    assert get_language_from_emoji("thumbsup") is None
    assert get_language_from_emoji("smile") is None


def test_language_selection_modal():
    modal = language_selection_modal("Hello world", "C123", "1234567890.123456")
    assert modal["type"] == "modal"
    assert modal["callback_id"] == "translate_message_submit"
    metadata = json.loads(modal["private_metadata"])
    assert metadata["text"] == "Hello world"
    assert metadata["channel"] == "C123"
    assert metadata["ts"] == "1234567890.123456"


def test_error_modal():
    modal = error_modal("Something went wrong")
    assert modal["type"] == "modal"
    assert "Something went wrong" in modal["blocks"][0]["text"]["text"]


@pytest.mark.asyncio
async def test_cache_provider(fake_provider):
    cached = CachedTranslationProvider(fake_provider, max_size=5)
    result1 = await cached.translate("hello", target_language="es")
    result2 = await cached.translate("hello", target_language="es")
    assert result1.translated_text == result2.translated_text

    # Different target should give different result
    result3 = await cached.translate("hello", target_language="fr")
    assert result3.target_language == "fr"


@pytest.mark.asyncio
async def test_cache_eviction(fake_provider):
    cached = CachedTranslationProvider(fake_provider, max_size=2)
    await cached.translate("a", target_language="es")
    await cached.translate("b", target_language="es")
    await cached.translate("c", target_language="es")  # evicts "a"
    # Cache should have "b" and "c" now
    assert len(cached._cache) == 2
