from __future__ import annotations

import logging

from slack_bolt.async_app import AsyncApp

from cluely.platform.slack.emoji_map import get_language_from_emoji
from cluely.storage.base import SettingsStore
from cluely.translation.base import TranslationProvider

logger = logging.getLogger(__name__)


def register_events(
    app: AsyncApp,
    translator: TranslationProvider,
    store: SettingsStore,
) -> None:
    """Register message and reaction event handlers on the Slack app."""

    @app.event("message")
    async def handle_message(event, client):
        """Auto-translate messages in channels with auto-translate enabled."""
        subtype = event.get("subtype")
        if subtype is not None:
            return

        channel_id = event.get("channel")
        text = (event.get("text") or "").strip()

        if not text or not channel_id:
            return

        config = await store.get_channel_config(channel_id)
        if config is None:
            return

        target_lang = config.target_language
        try:
            result = await translator.translate(text, target_language=target_lang)
            if result.source_language == result.target_language:
                return
            await client.chat_postMessage(
                channel=channel_id,
                thread_ts=event.get("ts"),
                text=(
                    f"_{result.translated_text}_ "
                    f"({result.source_language} \u2192 {result.target_language})"
                ),
            )
        except Exception as exc:
            logger.error("Auto-translate failed for channel %s: %s", channel_id, exc)

    @app.event("reaction_added")
    async def handle_reaction(event, client):
        """Translate a message when a flag emoji reaction is added."""
        reaction = event.get("reaction", "")
        target_lang = get_language_from_emoji(reaction)
        if target_lang is None:
            return

        item = event.get("item", {})
        channel_id = item.get("channel")
        message_ts = item.get("ts")
        if not channel_id or not message_ts:
            return

        # Fetch the original message text
        try:
            resp = await client.conversations_history(
                channel=channel_id,
                latest=message_ts,
                limit=1,
                inclusive=True,
            )
            messages = resp.get("messages", [])
            if not messages:
                return
            text = (messages[0].get("text") or "").strip()
            if not text:
                return
        except Exception as exc:
            logger.error("Failed to fetch message for reaction translate: %s", exc)
            return

        try:
            result = await translator.translate(text, target_language=target_lang)
            await client.chat_postMessage(
                channel=channel_id,
                thread_ts=message_ts,
                text=(
                    f"*Translation ({result.source_language} \u2192 "
                    f"{result.target_language}):*\n{result.translated_text}"
                ),
            )
        except Exception as exc:
            logger.error("Reaction-based translation failed: %s", exc)
