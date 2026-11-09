import datetime
from uuid import uuid4
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))


class Notification(Base):
    __tablename__ = "notifications"

    order_id: Mapped[str]
    message: Mapped[str]
    send_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )