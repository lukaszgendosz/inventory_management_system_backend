from datetime import datetime

from pydantic import BaseModel


class CompanyCreateScheme(BaseModel):
    name: str
    
class CompanyUpdateScheme(BaseModel):
    name: str
    
class CompanyResponseScheme(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime