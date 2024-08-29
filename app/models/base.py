from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Column, TIMESTAMP, Integer
from sqlalchemy import func
from datetime import datetime


class Base(DeclarativeBase):
    id: Mapped[int]  = mapped_column(primary_key=True, nullable=False, unique= True, autoincrement = True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
