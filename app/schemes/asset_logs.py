from typing import TYPE_CHECKING, Optional, Any
from datetime import datetime

from pydantic import BaseModel

from .constraints import EventType

from .asset import AssetResponseScheme, UserResponseScheme


class AssetLogsResponseScheme(BaseModel):
    id: int
    event_type: EventType
    updated_values: Optional[dict] = None
    user: UserResponseScheme
    asset: AssetResponseScheme
    created_at: datetime


class AssetLogsPaginatedResponseScheme(BaseModel):
    items: list[AssetLogsResponseScheme]
    total: int


class AssetLogsCreateScheme(BaseModel):
    event_type: EventType
    updated_values: Optional[dict] = None
    user_id: int
    asset_id: int
