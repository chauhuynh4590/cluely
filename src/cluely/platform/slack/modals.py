"""Block Kit modal views for the Slack translation shortcut."""

from __future__ import annotations

import json


def language_selection_modal(
    original_text: str,
    channel_id: str,
    message_ts: str,
) -> dict:
    """Return a Block Kit modal view for choosing a target language."""
    metadata = json.dumps({
        "text": original_text,
        "channel": channel_id,
        "ts": message_ts,
    })
    return {
        "type": "modal",
        "callback_id": "translate_message_submit",
        "title": {"type": "plain_text", "text": "Translate Message"},
        "submit": {"type": "plain_text", "text": "Translate"},
        "close": {"type": "plain_text", "text": "Cancel"},
        "private_metadata": metadata,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Original message:*\n> {original_text[:500]}",
                },
            },
            {
                "type": "input",
                "block_id": "language_block",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "language_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "e.g. es, fr, ja, de, zh",
                    },
                },
                "label": {
                    "type": "plain_text",
                    "text": "Target language (ISO code)",
                },
            },
        ],
    }


def error_modal(message: str) -> dict:
    """Return a simple error modal view."""
    return {
        "type": "modal",
        "title": {"type": "plain_text", "text": "Translation Error"},
        "close": {"type": "plain_text", "text": "OK"},
        "blocks": [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f":warning: {message}"},
            },
        ],
    }
