from __future__ import annotations

from abc import ABC, abstractmethod

from cluely.storage.base import SettingsStore
from cluely.translation.base import TranslationProvider


class ChatPlatform(ABC):
    """Abstract base class for chat platform integrations."""

    def __init__(
        self,
        translation_provider: TranslationProvider,
        settings_store: SettingsStore,
    ) -> None:
        self.translator = translation_provider
        self.store = settings_store

    @abstractmethod
    async def start(self) -> None: ...

    @abstractmethod
    async def stop(self) -> None: ...
