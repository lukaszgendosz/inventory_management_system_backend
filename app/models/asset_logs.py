from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.schemes import EventType
from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .asset import Asset


class AssetLogs(Base):
    __tablename__ = "asset_logs"

    event_type: Mapped[EventType] = mapped_column(nullable=False)
    updated_values: Mapped[dict] = mapped_column(JSONB, nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True, default=None)
    user: Mapped["User"] = relationship(back_populates="asset_logs", lazy="joined")

    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), nullable=True, default=None)
    asset: Mapped["Asset"] = relationship(back_populates="asset_logs", lazy="joined")
