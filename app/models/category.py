from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    unit_type: Mapped[str] = mapped_column(String(20))  # "piece" yoki "weight"

    def __repr__(self) -> str:
        return f"<Category {self.name}>"
