from __future__ import annotations

import json
import logging

from slack_bolt.async_app import AsyncApp

from cluely.platform.slack.modals import error_modal, language_selection_modal
from cluely.translation.base import TranslationProvider

logger = logging.getLogger(__name__)


def register_shortcuts(
    app: AsyncApp,
    translator: TranslationProvider,
) -> None:
    """Register message shortcut and view submission handlers."""

    @app.shortcut("translate_message")
    async def handle_translate_shortcut(ack, shortcut, client):
        await ack()

        message = shortcut.get("message", {})
        text = (message.get("text") or "").strip()
        channel_id = shortcut.get("channel", {}).get("id", "")
        trigger_id = shortcut.get("trigger_id")
        message_ts = message.get("ts", "")

        if not text:
            await client.views_open(
                trigger_id=trigger_id,
                view=error_modal("No text found in this message."),
            )
            return

        await client.views_open(
            trigger_id=trigger_id,
            view=language_selection_modal(text, channel_id, message_ts),
        )

    @app.view("translate_message_submit")
    async def handle_modal_submit(ack, view, client):
        await ack()

        values = view.get("state", {}).get("values", {})
        target_lang = (
            values.get("language_block", {})
            .get("language_input", {})
            .get("value", "")
            .strip()
            .lower()
        )
        metadata_str = view.get("private_metadata", "{}")
        try:
            metadata = json.loads(metadata_str)
        except json.JSONDecodeError:
            logger.error("Invalid modal metadata: %s", metadata_str)
            return

        original_text = metadata.get("text", "")
        channel_id = metadata.get("channel", "")
        user_id = view.get("user", {}).get("id") if isinstance(view.get("user"), dict) else ""

        if not original_text or not target_lang:
            return

        try:
            result = await translator.translate(original_text, target_language=target_lang)
            await client.chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                text=(
                    f"*Translation ({result.source_language} \u2192 "
                    f"{result.target_language}):*\n{result.translated_text}"
                ),
            )
        except Exception as exc:
            logger.error("Shortcut translation failed: %s", exc)
