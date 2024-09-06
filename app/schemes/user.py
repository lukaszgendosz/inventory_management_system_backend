from pydantic import BaseModel, EmailStr, field_validator
from fastapi.exceptions import RequestValidationError
from typing import Optional

class UserCreateScheme(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    password: str
    notes: Optional[str] = None
    location_id: Optional[int] = None
    company_id: Optional[int] = None
    department_id: Optional[int] = None
    
    @field_validator('password')
    def validate_password(cls, v):
        password_lenght = 12
        if len(v) < password_lenght:
            raise ValueError(f'Password must be at least {password_lenght} characters long.')

        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter.')

        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter.')

        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit.')

        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?/`~' for c in v):
            raise ValueError('Password must contain at least one special character.')
        return v
    
class UserUpdateScheme(BaseModel):
    email: EmailStr
    first_name: str
    last_name: Optional[str]
    notes: Optional[str] = None
    location_id: Optional[int] = None
    company_id: Optional[int] = None
    department_id: Optional[int] = None


class UserResponseScheme(BaseModel):
    id : int
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    notes: Optional[str] = None
    location_id: Optional[int] = None
    company_id: Optional[int] = None
    department_id: Optional[int] = None
    is_active: bool
    
    class Config:
        from_attributes=True
        
class UserLoginScheme(BaseModel):
    email: EmailStr
    password: str