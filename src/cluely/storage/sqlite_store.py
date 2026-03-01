from __future__ import annotations

from datetime import datetime, timezone

import aiosqlite

from cluely.storage.base import SettingsStore
from cluely.storage.models import ChannelConfig


class SQLiteSettingsStore(SettingsStore):
    """SQLite-backed settings store using aiosqlite for async access."""

    def __init__(self, db_path: str = "cluely.db") -> None:
        self.db_path = db_path
        self._db: aiosqlite.Connection | None = None

    async def _get_db(self) -> aiosqlite.Connection:
        if self._db is None:
            self._db = await aiosqlite.connect(self.db_path)
        return self._db

    async def initialize(self) -> None:
        db = await self._get_db()
        await db.execute("""
            CREATE TABLE IF NOT EXISTS channel_configs (
                channel_id TEXT PRIMARY KEY,
                target_language TEXT NOT NULL,
                platform TEXT NOT NULL DEFAULT 'slack',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        await db.commit()

    async def close(self) -> None:
        if self._db is not None:
            await self._db.close()
            self._db = None

    async def get_channel_config(self, channel_id: str) -> ChannelConfig | None:
        db = await self._get_db()
        cursor = await db.execute(
            "SELECT channel_id, target_language, platform, created_at, updated_at "
            "FROM channel_configs WHERE channel_id = ?",
            (channel_id,),
        )
        row = await cursor.fetchone()
        if row is None:
            return None
        return ChannelConfig(
            channel_id=row[0],
            target_language=row[1],
            platform=row[2],
            created_at=datetime.fromisoformat(row[3]),
            updated_at=datetime.fromisoformat(row[4]),
        )

    async def set_channel_config(
        self, channel_id: str, target_language: str, platform: str = "slack"
    ) -> None:
        now = datetime.now(timezone.utc).isoformat()
        db = await self._get_db()
        await db.execute(
            """
            INSERT INTO channel_configs
                (channel_id, target_language, platform, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(channel_id) DO UPDATE SET
                target_language = excluded.target_language,
                updated_at = excluded.updated_at
            """,
            (channel_id, target_language, platform, now, now),
        )
        await db.commit()

    async def delete_channel_config(self, channel_id: str) -> None:
        db = await self._get_db()
        await db.execute(
            "DELETE FROM channel_configs WHERE channel_id = ?",
            (channel_id,),
        )
        await db.commit()

    async def list_channel_configs(self) -> list[ChannelConfig]:
        db = await self._get_db()
        cursor = await db.execute(
            "SELECT channel_id, target_language, platform, created_at, updated_at "
            "FROM channel_configs"
        )
        rows = await cursor.fetchall()
        return [
            ChannelConfig(
                channel_id=row[0],
                target_language=row[1],
                platform=row[2],
                created_at=datetime.fromisoformat(row[3]),
                updated_at=datetime.fromisoformat(row[4]),
            )
            for row in rows
        ]
