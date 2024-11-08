from typing import Optional, Any

from pydantic import BaseModel, EmailStr, field_validator, Field
from fastapi import UploadFile

from .role_enum import Role
from .department import DepartmentResponseScheme
from .location import LocationResponseScheme
from .company import CompanyResponseScheme
from .generc_pagination import PaginationResponseScheme
from .generic_params import GenericFilterParams


class UserCreateScheme(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    role: Role
    username: Optional[str] = ""
    notes: Optional[str] = ""
    location_id: Optional[int] = Field(default=None, examples=[None])
    company_id: Optional[int] = Field(default=None, examples=[None])
    department_id: Optional[int] = Field(default=None, examples=[None])
    is_active: Optional[bool] = Field(default=True, examples=[True])

    @field_validator("password")
    def validate_password(cls, v):
        password_lenght = 12
        if len(v) < password_lenght:
            raise ValueError(f"Password must be at least {password_lenght} characters long.")

        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter.")

        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter.")

        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit.")

        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?/`~" for c in v):
            raise ValueError("Password must contain at least one special character.")
        return v


class UserUpdateScheme(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[Role] = None
    notes: Optional[str] = None
    location_id: Optional[int] = Field(default=None, examples=[None])
    company_id: Optional[int] = Field(default=None, examples=[None])
    department_id: Optional[int] = Field(default=None, examples=[None])


class UserResponseScheme(BaseModel):
    id: int
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    role: Role
    notes: Optional[str] = None
    company: Optional[CompanyResponseScheme] = None
    location: Optional[LocationResponseScheme] = None
    department: Optional[DepartmentResponseScheme] = None
    is_active: bool

    class Config:
        from_attributes = True


class UserLoginScheme(BaseModel):
    email: EmailStr
    password: str


class UserParamsScheme(GenericFilterParams):
    is_active: list[bool] = Field(default=[])
    company_id: list[int] = Field(default=[])
    location_id: list[int] = Field(default=[])
    role: list[Role] = Field(default=[])


UserPaginatedResponseScheme = PaginationResponseScheme[UserResponseScheme]
