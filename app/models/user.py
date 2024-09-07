from typing import TYPE_CHECKING

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemes.role_enum import Role
from .base import Base

if TYPE_CHECKING:
    from .department import Department
    
class User(Base):
    __tablename__ = 'users'
    
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    username: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[Role] = mapped_column(nullable=False, default=Role.USER)
    password: Mapped[str] = mapped_column(nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    location_id: Mapped[int] = mapped_column(nullable=True, default=None)
    company_id: Mapped[int] = mapped_column(nullable=True, default=None)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    



