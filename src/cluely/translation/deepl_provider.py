from __future__ import annotations

import asyncio
import logging

from deep_translator import DeeplTranslator
from deep_translator.exceptions import (
    AuthorizationException,
    LanguageNotSupportedException,
    TranslationNotFound,
)

from cluely.translation.base import TranslationError, TranslationProvider, TranslationResult

logger = logging.getLogger(__name__)


class DeepLProvider(TranslationProvider):
    """DeepL translation provider via deep-translator."""

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    @property
    def name(self) -> str:
        return "deepl"

    def supported_languages(self) -> list[str]:
        return [
            "bg", "cs", "da", "de", "el", "en", "es", "et", "fi", "fr",
            "hu", "id", "it", "ja", "ko", "lt", "lv", "nb", "nl", "pl",
            "pt", "ro", "ru", "sk", "sl", "sv", "tr", "uk", "zh",
        ]

    async def translate(
        self,
        text: str,
        target_language: str,
        source_language: str | None = None,
    ) -> TranslationResult:
        src = source_language or "auto"
        try:
            translator = DeeplTranslator(
                api_key=self._api_key,
                source=src,
                target=target_language,
            )
            translated = await asyncio.to_thread(translator.translate, text)
        except AuthorizationException as exc:
            raise TranslationError(f"DeepL auth failed: {exc}") from exc
        except LanguageNotSupportedException as exc:
            raise TranslationError(f"Unsupported language: {exc}") from exc
        except TranslationNotFound as exc:
            raise TranslationError(f"Translation not found: {exc}") from exc
        except Exception as exc:
            logger.exception("DeepL translation failed")
            raise TranslationError(f"DeepL error: {exc}") from exc

        return TranslationResult(
            original_text=text,
            translated_text=translated,
            source_language=source_language or "auto",
            target_language=target_language,
            provider_name=self.name,
        )
