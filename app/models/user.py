from typing import TYPE_CHECKING

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemes.role_enum import Role
from .base import Base

if TYPE_CHECKING:
    from .department import Department
    from .location import Location
    from .company import Company
    from .asset import Asset
    from .asset_logs import AssetLogs


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[Role] = mapped_column(nullable=False, default=Role.USER)
    password: Mapped[str] = mapped_column(nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id"), nullable=True, default=None
    )
    department: Mapped["Department"] = relationship(back_populates="users", lazy="joined")

    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id"), nullable=True, default=None
    )
    location: Mapped["Location"] = relationship(back_populates="users", lazy="joined")

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=True, default=None)
    company: Mapped["Company"] = relationship(back_populates="users", lazy="joined")

    assets: Mapped[list["Asset"]] = relationship("Asset", backref="suppliers")
    asset_logs: Mapped[list["AssetLogs"]] = relationship(back_populates="user")
