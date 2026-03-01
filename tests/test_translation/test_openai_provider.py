from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from cluely.translation.base import TranslationError
from cluely.translation.openai_provider import OpenAIProvider


@pytest.fixture
def provider():
    return OpenAIProvider(api_key="sk-test", model="gpt-4o-mini")


def test_provider_name(provider):
    assert provider.name == "openai"


def test_supported_languages(provider):
    langs = provider.supported_languages()
    assert "en" in langs
    assert "ja" in langs


@pytest.mark.asyncio
async def test_translate_success(provider):
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = '{"translated": "Hola mundo", "source_language": "en"}'
    mock_response.choices = [mock_choice]

    with patch.object(
        provider._client.chat.completions, "create", new_callable=AsyncMock
    ) as mock_create:
        mock_create.return_value = mock_response
        result = await provider.translate("Hello world", target_language="es")

    assert result.translated_text == "Hola mundo"
    assert result.source_language == "en"
    assert result.target_language == "es"
    assert result.provider_name == "openai"


@pytest.mark.asyncio
async def test_translate_with_source_language(provider):
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = '{"translated": "Bonjour", "source_language": "en"}'
    mock_response.choices = [mock_choice]

    with patch.object(
        provider._client.chat.completions, "create", new_callable=AsyncMock
    ) as mock_create:
        mock_create.return_value = mock_response
        result = await provider.translate(
            "Hello", target_language="fr", source_language="en"
        )

    assert result.translated_text == "Bonjour"
    call_args = mock_create.call_args
    user_msg = call_args.kwargs["messages"][1]["content"]
    assert "from en" in user_msg


@pytest.mark.asyncio
async def test_translate_api_error(provider):
    from openai import APIError

    with patch.object(
        provider._client.chat.completions, "create", new_callable=AsyncMock
    ) as mock_create:
        mock_create.side_effect = APIError(
            message="API error", request=MagicMock(), body=None
        )
        with pytest.raises(TranslationError, match="OpenAI API error"):
            await provider.translate("Hello", target_language="es")
