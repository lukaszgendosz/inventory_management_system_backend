from typing import Optional, TYPE_CHECKING
from datetime import datetime

from pydantic import BaseModel


class DepartmentCreateScheme(BaseModel):
    name: str
    
class DepartmentUpdateScheme(BaseModel):
    name: str
    
class DepartmentResponseScheme(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


