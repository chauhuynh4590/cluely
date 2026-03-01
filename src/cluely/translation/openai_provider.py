from __future__ import annotations

import json
import logging

from openai import APIError, AsyncOpenAI, RateLimitError

from cluely.translation.base import TranslationError, TranslationProvider, TranslationResult

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """\
You are a professional translator. You will be given text to translate.
Respond with a JSON object containing exactly two keys:
- "translated": the translated text (preserve formatting and tone)
- "source_language": the ISO 639-1 code of the detected source language

Output ONLY valid JSON, nothing else."""


class OpenAIProvider(TranslationProvider):
    """OpenAI LLM-based translation provider for high-quality, context-aware translations."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini") -> None:
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model

    @property
    def name(self) -> str:
        return "openai"

    def supported_languages(self) -> list[str]:
        # LLMs support virtually all languages; return common ones
        return [
            "en", "es", "fr", "de", "it", "pt", "nl", "ru", "zh", "ja",
            "ko", "ar", "hi", "th", "vi", "pl", "tr", "sv", "da", "fi",
            "no", "cs", "el", "he", "id", "ms", "ro", "uk", "bg", "hr",
            "sk", "sl", "et", "lv", "lt", "hu",
        ]

    async def translate(
        self,
        text: str,
        target_language: str,
        source_language: str | None = None,
    ) -> TranslationResult:
        user_msg = f"Translate the following text to {target_language}:\n\n{text}"
        if source_language:
            user_msg = (
                f"Translate the following text from {source_language} "
                f"to {target_language}:\n\n{text}"
            )

        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                ],
                temperature=0.1,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content or "{}"
            data = json.loads(content)
            translated = data.get("translated", content)
            detected = data.get("source_language", source_language or "unknown")
        except (RateLimitError, APIError) as exc:
            raise TranslationError(f"OpenAI API error: {exc}") from exc
        except json.JSONDecodeError:
            raise TranslationError("OpenAI returned invalid JSON")
        except Exception as exc:
            logger.exception("OpenAI translation failed")
            raise TranslationError(f"OpenAI error: {exc}") from exc

        return TranslationResult(
            original_text=text,
            translated_text=translated,
            source_language=detected,
            target_language=target_language,
            provider_name=self.name,
        )
