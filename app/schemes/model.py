from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemes.generic_params import GenericFilterParams

from .generc_pagination import PaginationResponseScheme
from .manufacturer import ManufacturerResponseScheme


class ModelConfigScheme(BaseModel):
    model_config = {"from_attributes": True, "protected_namespaces": ()}


class ModelCreateScheme(ModelConfigScheme):
    name: str
    model_number: Optional[str] = None
    notes: Optional[str] = None
    manufacturer_id: Optional[int] = Field(default=None, examples=[None])


class ModelUpdateScheme(ModelConfigScheme):
    name: Optional[str] = None
    model_number: Optional[str] = None
    notes: Optional[str] = None
    manufacturer_id: Optional[int] = Field(default=None, examples=[None])


class ModelResponseScheme(ModelConfigScheme):
    id: int
    name: str
    model_number: Optional[str] = None
    notes: Optional[str] = None
    manufacturer: Optional[ManufacturerResponseScheme] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ModelParamsScheme(GenericFilterParams):
    manufacturer_id: list[int] = Field(default=[])


ModelPaginatedResponseScheme = PaginationResponseScheme[ModelResponseScheme]
