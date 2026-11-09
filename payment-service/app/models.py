import datetime
from uuid import uuid4
from sqlalchemy import String, func, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))

class PaymentORM(Base):
    __tablename__ = "payments"

    order_id: Mapped[str]
    status: Mapped[str]
    amount: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )