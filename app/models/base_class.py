from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, TIMESTAMP, Integer
from sqlalchemy import func


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True, nullable=False, unique= True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
