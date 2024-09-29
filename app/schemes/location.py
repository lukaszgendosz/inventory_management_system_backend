from datetime import datetime

from pydantic import BaseModel

from .generc_pagination import PaginationResponseScheme


class LocationCreateScheme(BaseModel):
    name: str


class LocationUpdateScheme(BaseModel):
    name: str


class LocationResponseScheme(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


LocationPaginatedResponseScheme = PaginationResponseScheme[LocationResponseScheme]
