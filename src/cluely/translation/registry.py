from __future__ import annotations

from cluely.config import Settings
from cluely.translation.base import TranslationProvider
from cluely.translation.cache import CachedTranslationProvider


def create_provider(settings: Settings) -> TranslationProvider:
    """Create a translation provider based on settings, wrapped with cache."""
    name = settings.translation_provider

    if name == "openai":
        from cluely.translation.openai_provider import OpenAIProvider

        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when using the openai provider")
        provider = OpenAIProvider(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
        )

    elif name == "google":
        from cluely.translation.google_provider import GoogleProvider

        provider = GoogleProvider()

    elif name == "deepl":
        from cluely.translation.deepl_provider import DeepLProvider

        if not settings.deepl_api_key:
            raise ValueError("DEEPL_API_KEY is required when using the deepl provider")
        provider = DeepLProvider(api_key=settings.deepl_api_key)

    else:
        raise ValueError(
            f"Unknown provider: {name!r}. Available: openai, google, deepl"
        )

    return CachedTranslationProvider(provider, max_size=settings.cache_max_size)
