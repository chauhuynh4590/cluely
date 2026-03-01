from __future__ import annotations

import logging

from slack_bolt.async_app import AsyncApp

from cluely.storage.base import SettingsStore
from cluely.translation.base import TranslationProvider

logger = logging.getLogger(__name__)


def register_commands(
    app: AsyncApp,
    translator: TranslationProvider,
    store: SettingsStore,
) -> None:
    """Register slash command handlers on the Slack app."""

    @app.command("/translate")
    async def handle_translate(ack, command, say, respond):
        await ack()

        text = (command.get("text") or "").strip()
        if not text:
            await respond(
                "Usage: `/translate <target_lang> <message>`\n"
                "Example: `/translate es Hello, how are you?`"
            )
            return

        parts = text.split(maxsplit=1)
        if len(parts) < 2:
            await respond(
                "Please provide both a target language and text.\n"
                "Example: `/translate fr Good morning`"
            )
            return

        target_lang, message = parts[0].lower(), parts[1]

        try:
            result = await translator.translate(message, target_language=target_lang)
            await say(
                text=(
                    f"*Translation ({result.source_language} \u2192 "
                    f"{result.target_language}):*\n{result.translated_text}"
                ),
            )
        except Exception as exc:
            logger.error("Translation failed: %s", exc)
            await respond(f"Translation failed: {exc}")

    @app.command("/translate-channel")
    async def handle_translate_channel(ack, command, respond):
        await ack()

        text = (command.get("text") or "").strip().lower()
        channel_id = command.get("channel_id")

        if not text:
            await respond(
                "Usage: `/translate-channel <lang>` to enable auto-translation, "
                "or `/translate-channel off` to disable."
            )
            return

        if text == "off":
            await store.delete_channel_config(channel_id)
            await respond("Auto-translation disabled for this channel.")
            return

        await store.set_channel_config(channel_id, target_language=text)
        await respond(
            f"Auto-translation enabled. Messages in this channel will be "
            f"translated to `{text}` (replied in threads)."
        )
