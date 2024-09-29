from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from .generc_pagination import PaginationResponseScheme


class ManufacturerCreateScheme(BaseModel):
    name: str
    support_url: Optional[str] = None
    support_phone: Optional[str] = None
    support_email: Optional[str] = None


class ManufacturerUpdateScheme(BaseModel):
    name: Optional[str] = None
    support_url: Optional[str] = None
    support_phone: Optional[str] = None
    support_email: Optional[str] = None


class ManufacturerResponseScheme(BaseModel):
    id: int
    name: str
    support_url: Optional[str] = None
    support_phone: Optional[str] = None
    support_email: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


ManufacturerPaginatedResponseScheme = PaginationResponseScheme[ManufacturerResponseScheme]
