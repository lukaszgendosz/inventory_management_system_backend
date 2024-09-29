from typing import Optional 
from datetime import datetime

from pydantic import BaseModel, Field

from .status import Status
from .checkout_type import CheckoutType
from .generc_pagination import PaginationResponseScheme

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
    
    model_config = {
        'protected_namespaces': ()
    }
    
    
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
    location_id: Optional[int] = Field(default=None, examples=[None])
    company_id: Optional[int] = Field(default=None, examples=[None])
    supplier_id: Optional[int] = Field(default=None, examples=[None])
    user_id: Optional[int] = Field(default=None, examples=[None])
    
    model_config = {
        'protected_namespaces': (),
    }
    
    
class AssetResponseScheme(BaseModel):
    id : int
    name: str
    serial_number: str
    status: Status
    checkout_type: Optional[CheckoutType] = None
    purchase_date: Optional[datetime] = None
    purchase_cost: Optional[float] = None
    invoice_number: Optional[str] = None
    varrianty_expiration_date: Optional[datetime] = None
    notes: Optional[str] = Field(default=None, examples=[None])
    # model: Optional["ModelResponseScheme"] = None
    # location: Optional["LocationResponseScheme"] = None
    # company: Optional["CompanyResponseScheme"] = None
    # supplier: Optional["SupplierResponseScheme"] = None
    # user: Optional["UserResponseScheme"] = None
    
    model_config = {
        'from_attributes': True
    }
    
    
AssetPaginatedResponseScheme = PaginationResponseScheme[AssetResponseScheme]