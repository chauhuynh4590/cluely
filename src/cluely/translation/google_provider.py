from __future__ import annotations

import asyncio
import logging

from deep_translator import GoogleTranslator
from deep_translator.exceptions import (
    LanguageNotSupportedException,
    TranslationNotFound,
)

from cluely.translation.base import TranslationError, TranslationProvider, TranslationResult

logger = logging.getLogger(__name__)


class GoogleProvider(TranslationProvider):
    """Google Translate provider via deep-translator (free, no API key)."""

    @property
    def name(self) -> str:
        return "google"

    def supported_languages(self) -> list[str]:
        return list(GoogleTranslator().get_supported_languages(as_dict=True).values())

    async def translate(
        self,
        text: str,
        target_language: str,
        source_language: str | None = None,
    ) -> TranslationResult:
        src = source_language or "auto"
        try:
            translator = GoogleTranslator(source=src, target=target_language)
            translated = await asyncio.to_thread(translator.translate, text)
        except LanguageNotSupportedException as exc:
            raise TranslationError(f"Unsupported language: {exc}") from exc
        except TranslationNotFound as exc:
            raise TranslationError(f"Translation not found: {exc}") from exc
        except Exception as exc:
            logger.exception("Google Translate failed")
            raise TranslationError(f"Google Translate error: {exc}") from exc

        detected_source = source_language or "auto"
        return TranslationResult(
            original_text=text,
            translated_text=translated,
            source_language=detected_source,
            target_language=target_language,
            provider_name=self.name,
        )
