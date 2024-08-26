from app.models.base_class import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey

class User(Base):
    __tablename__ = 'users'
    
    email = Column(String(255), nullable=True, unique=True)
    username = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    notes = Column(Text, nullable=True)
    location_id = Column(Integer, nullable=True)
    company_id = Column(Integer, nullable=True)
    department_id = Column(Integer, nullable=True)
    last_login = Column(TIMESTAMP, nullable=True)
    activated = Column(Boolean, nullable=False, default=True)



