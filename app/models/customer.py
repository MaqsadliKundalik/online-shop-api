# app/models/customer.py
from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(200))
    phone: Mapped[str] = mapped_column(String(30), unique=True)
    default_address: Mapped[str | None] = mapped_column(String(500), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    # Order bilan bog'lanish (1 -> ko'p)
    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="customer",
    )

    def __repr__(self) -> str:
        return f"<Customer {self.full_name} ({self.phone})>"
