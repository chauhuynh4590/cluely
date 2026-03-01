from __future__ import annotations

from collections import OrderedDict

from cluely.translation.base import TranslationProvider, TranslationResult


class CachedTranslationProvider(TranslationProvider):
    """Wraps any TranslationProvider with an LRU cache to reduce API calls."""

    def __init__(self, provider: TranslationProvider, max_size: int = 1000) -> None:
        self._provider = provider
        self._max_size = max_size
        self._cache: OrderedDict[str, TranslationResult] = OrderedDict()

    @property
    def name(self) -> str:
        return f"cached:{self._provider.name}"

    def supported_languages(self) -> list[str]:
        return self._provider.supported_languages()

    def _cache_key(
        self, text: str, target_language: str, source_language: str | None
    ) -> str:
        return f"{source_language or 'auto'}:{target_language}:{text}"

    async def translate(
        self,
        text: str,
        target_language: str,
        source_language: str | None = None,
    ) -> TranslationResult:
        key = self._cache_key(text, target_language, source_language)

        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]

        result = await self._provider.translate(text, target_language, source_language)
        self._cache[key] = result

        if len(self._cache) > self._max_size:
            self._cache.popitem(last=False)

        return result

    def clear(self) -> None:
        self._cache.clear()
