# app/models/cart.py
from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Hozircha user system yo'q, shuning uchun session_id yoki guest_id saqlasa bo'ladi
    session_id: Mapped[str | None] = mapped_column(String(100), nullable=True)

    status: Mapped[str] = mapped_column(
        String(20), default="open"
    )  # open, ordered, abandoned

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    items: Mapped[list["CartItem"]] = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Cart id={self.id} status={self.status}>"


class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    quantity: Mapped[int] = mapped_column(Integer, default=1)
    unit_price: Mapped[int] = mapped_column(Integer)  # so'm

    cart: Mapped["Cart"] = relationship("Cart", back_populates="items")
    product = relationship("Product")  # oddiy relationship

    def __repr__(self) -> str:
        return f"<CartItem cart_id={self.cart_id} product_id={self.product_id}>"

    @property
    def image(self):
        if self.product:
            return self.product.image
        return None
