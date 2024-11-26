from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .asset import Asset


class Company(Base):
    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(nullable=False, unique=False)

    users: Mapped[list["User"]] = relationship("User", backref="companies", lazy="joined")
    assets: Mapped[list["Asset"]] = relationship("Asset", backref="companies", lazy="joined")
