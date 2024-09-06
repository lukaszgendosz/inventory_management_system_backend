from app.models.base import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = 'users'
    
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    username: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    location_id: Mapped[int] = mapped_column(nullable=True)
    company_id: Mapped[int] = mapped_column(nullable=True)
    department_id: Mapped[int] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=True, default=True)



