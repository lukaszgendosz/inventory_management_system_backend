from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    
class Department(Base):
    __tablename__ = 'departments'
    
    name: Mapped[str] = mapped_column(nullable=False, unique=False)
    
    users: Mapped[list['User']] = relationship("User", backref="departments")
