from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .generc_pagination import PaginationResponseScheme


class SupplierConfigScheme(BaseModel):
    model_config = {"from_attributes": True}


class SupplierResponseScheme(SupplierConfigScheme):
    id: int
    name: str
    support_url: Optional[str] = None
    support_phone: Optional[str] = None
    support_email: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class SupplierUpdateScheme(SupplierConfigScheme):
    name: Optional[str] = None
    support_url: Optional[str] = None
    support_phone: Optional[str] = None
    support_email: Optional[str] = None


class SupplierCreateScheme(SupplierConfigScheme):
    name: str
    support_url: Optional[str] = None
    support_phone: Optional[str] = None
    support_email: Optional[str] = None


SupplierPaginatedResponseScheme = PaginationResponseScheme[SupplierResponseScheme]
