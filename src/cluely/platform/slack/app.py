from __future__ import annotations

import logging

from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.async_app import AsyncApp

from cluely.config import Settings
from cluely.platform.base import ChatPlatform
from cluely.platform.slack.commands import register_commands
from cluely.platform.slack.events import register_events
from cluely.platform.slack.shortcuts import register_shortcuts
from cluely.storage.base import SettingsStore
from cluely.translation.base import TranslationProvider

logger = logging.getLogger(__name__)


class SlackPlatform(ChatPlatform):
    """Slack integration using slack-bolt AsyncApp with Socket Mode."""

    def __init__(
        self,
        translation_provider: TranslationProvider,
        settings_store: SettingsStore,
        settings: Settings,
    ) -> None:
        super().__init__(translation_provider, settings_store)
        self._settings = settings
        self.bolt_app = AsyncApp(
            token=settings.slack_bot_token,
            signing_secret=settings.slack_signing_secret or None,
        )
        self._handler: AsyncSocketModeHandler | None = None

        # Register all handlers
        register_commands(self.bolt_app, self.translator, self.store)
        register_events(self.bolt_app, self.translator, self.store)
        register_shortcuts(self.bolt_app, self.translator)

        # Global error handler
        @self.bolt_app.error
        async def handle_error(error, body, logger):
            logger.error("Slack app error: %s\nBody: %s", error, body)

    async def start(self) -> None:
        logger.info("Starting Slack bot in Socket Mode...")
        self._handler = AsyncSocketModeHandler(
            self.bolt_app, self._settings.slack_app_token
        )
        await self._handler.start_async()

    async def stop(self) -> None:
        if self._handler:
            logger.info("Stopping Slack bot...")
            await self._handler.close_async()
