from __future__ import annotations

from abc import ABC, abstractmethod

from cluely.storage.models import ChannelConfig


class SettingsStore(ABC):
    """Abstract base class for channel settings persistence."""

    @abstractmethod
    async def initialize(self) -> None: ...

    @abstractmethod
    async def get_channel_config(self, channel_id: str) -> ChannelConfig | None: ...

    @abstractmethod
    async def set_channel_config(
        self, channel_id: str, target_language: str, platform: str = "slack"
    ) -> None: ...

    @abstractmethod
    async def delete_channel_config(self, channel_id: str) -> None: ...

    @abstractmethod
    async def list_channel_configs(self) -> list[ChannelConfig]: ...
