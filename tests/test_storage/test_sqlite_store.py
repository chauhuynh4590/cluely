from __future__ import annotations

import pytest

from cluely.storage.sqlite_store import SQLiteSettingsStore


@pytest.fixture
async def store():
    s = SQLiteSettingsStore(db_path=":memory:")
    await s.initialize()
    return s


@pytest.mark.asyncio
async def test_set_and_get_config(store):
    await store.set_channel_config("C123", target_language="es")
    config = await store.get_channel_config("C123")
    assert config is not None
    assert config.channel_id == "C123"
    assert config.target_language == "es"
    assert config.platform == "slack"


@pytest.mark.asyncio
async def test_get_nonexistent_config(store):
    config = await store.get_channel_config("DOESNOTEXIST")
    assert config is None


@pytest.mark.asyncio
async def test_update_config(store):
    await store.set_channel_config("C123", target_language="es")
    await store.set_channel_config("C123", target_language="fr")
    config = await store.get_channel_config("C123")
    assert config is not None
    assert config.target_language == "fr"


@pytest.mark.asyncio
async def test_delete_config(store):
    await store.set_channel_config("C123", target_language="es")
    await store.delete_channel_config("C123")
    config = await store.get_channel_config("C123")
    assert config is None


@pytest.mark.asyncio
async def test_list_configs(store):
    await store.set_channel_config("C1", target_language="es")
    await store.set_channel_config("C2", target_language="fr")
    configs = await store.list_channel_configs()
    assert len(configs) == 2
    ids = {c.channel_id for c in configs}
    assert ids == {"C1", "C2"}
