from __future__ import annotations

import pytest

from cluely.translation.base import TranslationProvider, TranslationResult


class FakeTranslationProvider(TranslationProvider):
    """A fake provider for tests that returns deterministic results."""

    def __init__(self, translated_prefix: str = "TRANSLATED") -> None:
        self._prefix = translated_prefix

    @property
    def name(self) -> str:
        return "fake"

    def supported_languages(self) -> list[str]:
        return ["en", "es", "fr", "de", "ja"]

    async def translate(
        self,
        text: str,
        target_language: str,
        source_language: str | None = None,
    ) -> TranslationResult:
        return TranslationResult(
            original_text=text,
            translated_text=f"[{self._prefix}:{target_language}] {text}",
            source_language=source_language or "en",
            target_language=target_language,
            provider_name=self.name,
        )


@pytest.fixture
def fake_provider():
    return FakeTranslationProvider()
