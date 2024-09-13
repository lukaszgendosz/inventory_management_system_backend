from datetime import datetime

from pydantic import BaseModel

class LocationCreateScheme(BaseModel):
    name: str
    
class LocationUpdateScheme(BaseModel):
    name: str
    
class LocationResponseScheme(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime