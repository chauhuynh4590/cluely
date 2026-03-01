from __future__ import annotations

import asyncio
import logging
import signal

from cluely.config import Settings
from cluely.platform.slack.app import SlackPlatform
from cluely.storage.sqlite_store import SQLiteSettingsStore
from cluely.translation.registry import create_provider

logger = logging.getLogger(__name__)


async def run() -> None:
    settings = Settings()

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    # Initialize storage
    store = SQLiteSettingsStore(db_path=settings.database_path)
    await store.initialize()
    logger.info("Storage initialized (db: %s)", settings.database_path)

    # Create translation provider
    provider = create_provider(settings)
    logger.info("Translation provider: %s", provider.name)

    # Create and start the Slack platform
    platform = SlackPlatform(
        translation_provider=provider,
        settings_store=store,
        settings=settings,
    )

    # Graceful shutdown on SIGTERM/SIGINT
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            sig, lambda: asyncio.create_task(_shutdown(platform))
        )

    logger.info("Cluely is starting...")
    await platform.start()


async def _shutdown(platform) -> None:
    logger.info("Shutting down gracefully...")
    await platform.stop()
    asyncio.get_running_loop().stop()


def main() -> None:
    try:
        asyncio.run(run())
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    main()
