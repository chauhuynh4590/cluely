from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ChannelConfig:
    channel_id: str
    target_language: str
    platform: str
    created_at: datetime
    updated_at: datetime
