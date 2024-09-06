from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .user import User

from app.models.base import Base

class Token(Base):
    __tablename__ = 'tokens'
    
    token: Mapped[str]  = mapped_column(nullable=False, unique= True)
    
    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # user: Mapped["User"] = relationship("User", back_populates="related_models",)



