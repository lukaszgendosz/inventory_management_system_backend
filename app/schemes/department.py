from datetime import datetime

from pydantic import BaseModel

from .generc_pagination import PaginationResponseScheme


class DepartmentCreateScheme(BaseModel):
    name: str
    
class DepartmentUpdateScheme(BaseModel):
    name: str
    
class DepartmentResponseScheme(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        'from_attributes': True
    }
    
DepartmentPaginatedResponseScheme = PaginationResponseScheme[DepartmentResponseScheme]