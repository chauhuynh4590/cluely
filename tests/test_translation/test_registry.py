from __future__ import annotations

import pytest

from cluely.config import Settings
from cluely.translation.cache import CachedTranslationProvider
from cluely.translation.registry import create_provider


def test_create_google_provider():
    settings = Settings(slack_bot_token="x", slack_app_token="x", translation_provider="google")
    provider = create_provider(settings)
    assert isinstance(provider, CachedTranslationProvider)
    assert "google" in provider.name


def test_create_openai_provider():
    settings = Settings(
        slack_bot_token="x",
        slack_app_token="x",
        translation_provider="openai",
        openai_api_key="sk-test",
    )
    provider = create_provider(settings)
    assert isinstance(provider, CachedTranslationProvider)
    assert "openai" in provider.name


def test_create_openai_provider_missing_key():
    settings = Settings(
        slack_bot_token="x", slack_app_token="x", translation_provider="openai"
    )
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        create_provider(settings)


def test_create_deepl_provider_missing_key():
    settings = Settings(
        slack_bot_token="x", slack_app_token="x", translation_provider="deepl"
    )
    with pytest.raises(ValueError, match="DEEPL_API_KEY"):
        create_provider(settings)


def test_create_unknown_provider():
    settings = Settings(
        slack_bot_token="x", slack_app_token="x", translation_provider="nope"
    )
    with pytest.raises(ValueError, match="Unknown provider"):
        create_provider(settings)
