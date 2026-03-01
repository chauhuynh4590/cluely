from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class TranslationError(Exception):
    """Raised when a translation operation fails."""


@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    provider_name: str


class TranslationProvider(ABC):
    """Abstract base class for all translation providers."""

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    async def translate(
        self,
        text: str,
        target_language: str,
        source_language: str | None = None,
    ) -> TranslationResult:
        """Translate text to the target language.

        Args:
            text: The text to translate.
            target_language: ISO 639-1 language code (e.g. "es", "fr", "ja").
            source_language: Optional source language code. Auto-detects if None.

        Returns:
            TranslationResult with translated text and metadata.

        Raises:
            TranslationError: If translation fails.
        """
        ...

    @abstractmethod
    def supported_languages(self) -> list[str]:
        """Return list of supported ISO 639-1 language codes."""
        ...
