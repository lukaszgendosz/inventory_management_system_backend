from datetime import datetime

from pydantic import BaseModel

from .generc_pagination import PaginationResponseScheme


class CompanyCreateScheme(BaseModel):
    name: str


class CompanyUpdateScheme(BaseModel):
    name: str


class CompanyResponseScheme(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


CompanyPaginatedResponseScheme = PaginationResponseScheme[CompanyResponseScheme]
