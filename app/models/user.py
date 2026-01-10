from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from passlib.hash import bcrypt

from app.db.base import Base
from passlib.hash import pbkdf2_sha256 


class AdminUser(Base):
    __tablename__ = "admin_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=True)

    def verify_password(self, raw: str) -> bool:
        try:
            return pbkdf2_sha256.verify(raw, self.password)
        except ValueError:
            # Hash noto'g'ri formatda bo'lsa (masalan, oddiy tekst), login rad etiladi
            return False

    def __repr__(self) -> str:
        return f"<AdminUser {self.username}>"
