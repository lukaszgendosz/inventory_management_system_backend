from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemes.generic_params import GenericFilterParams

from .constraints import Status
from .checkout_type import CheckoutType
from .generc_pagination import PaginationResponseScheme
from .model import ModelResponseScheme
from .location import LocationResponseScheme
from .company import CompanyResponseScheme
from .supplier import SupplierResponseScheme
from .user import UserResponseScheme


class AssetCreateScheme(BaseModel):
    name: Optional[str]
    serial_number: str
    status: Status
    checkout_type: Optional[CheckoutType] = None
    purchase_date: Optional[datetime] = None
    purchase_cost: Optional[float] = None
    invoice_number: Optional[str] = None
    varrianty_expiration_date: Optional[datetime] = None
    notes: Optional[str] = Field(default=None, examples=[None])
    model_id: Optional[int] = Field(default=None, examples=[None])
    location_id: Optional[int] = Field(default=None, examples=[None])
    company_id: Optional[int] = Field(default=None, examples=[None])
    supplier_id: Optional[int] = Field(default=None, examples=[None])
    user_id: Optional[int] = Field(default=None, examples=[None])

    model_config = {"protected_namespaces": ()}


class AssetUpdateScheme(BaseModel):
    name: Optional[str] = None
    serial_number: Optional[str] = None
    status: Optional[Status] = None
    checkout_type: Optional[CheckoutType] = None
    purchase_date: Optional[datetime] = None
    purchase_cost: Optional[float] = None
    invoice_number: Optional[str] = None
    varrianty_expiration_date: Optional[datetime] = None
    notes: Optional[str] = Field(default=None, examples=[None])
    model_id: Optional[int] = Field(default=None, examples=[None])
    supplier_id: Optional[int] = Field(default=None, examples=[None])
    location_id: Optional[int] = Field(default=None, examples=[None])
    company_id: Optional[int] = Field(default=None, examples=[None])
    user_id: Optional[int] = Field(default=None, examples=[None])

    model_config = {
        "protected_namespaces": (),
    }


class AssetResponseScheme(BaseModel):
    id: int
    name: str
    serial_number: str
    status: Status
    checkout_type: Optional[CheckoutType] = None
    purchase_date: Optional[datetime] = None
    purchase_cost: Optional[float] = None
    invoice_number: Optional[str] = None
    varrianty_expiration_date: Optional[datetime] = None
    notes: Optional[str] = Field(default=None, examples=[None])
    model: Optional["ModelResponseScheme"] = None
    company: Optional["CompanyResponseScheme"] = None
    supplier: Optional["SupplierResponseScheme"] = None
    user: Optional["UserResponseScheme"] = None
    asset: Optional["AssetResponseScheme"] = None
    location: Optional["LocationResponseScheme"] = None

    model_config = {"from_attributes": True}


class AssetParamsScheme(GenericFilterParams):
    serial_number: list[str] = Field(default=[])
    company_id: list[int] = Field(default=[])
    location_id: list[int] = Field(default=[])
    model_id: list[int] = Field(default=[])
    supplier_id: list[int] = Field(default=[])
    manufacturer_id: list[int] = Field(default=[])
    user_id: list[int] = Field(default=[])
    status: list[Status] = Field(default=[])

    model_config = {"protected_namespaces": ()}


class AssetExportScheme(BaseModel):
    id: int
    name: str
    serial_number: str
    status: Status
    checkout_to: Optional[str] = None
    purchase_date: Optional[datetime] = None
    purchase_cost: Optional[float] = None
    invoice_number: Optional[str] = None
    varrianty_expiration_date: Optional[datetime] = None
    user_email: Optional[str] = None
    supplier_name: Optional[str] = None
    company_name: Optional[str] = None
    location_name: Optional[str] = None
    model_name: Optional[str] = None
    manufacturer_name: Optional[str] = None
    notes: Optional[str] = Field(default=None, examples=[None])

    model_config = {"from_attributes": True, "protected_namespaces": ()}


AssetPaginatedResponseScheme = PaginationResponseScheme[AssetResponseScheme]
