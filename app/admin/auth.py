# app/admin/auth.py
from sqlalchemy import select
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.db.session import SessionLocal
from app.models.user import AdminUser


class AdminAuth(AuthenticationBackend):
    """
    SQLAdmin uchun oddiy session-based autentifikatsiya.
    """

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if not username or not password:
            return False

        db = SessionLocal()
        try:
            stmt = select(AdminUser).where(AdminUser.username == username)
            user: AdminUser | None = db.execute(stmt).scalar_one_or_none()
            if user and user.verify_password(password):
                # session ichiga faqat user_id saqlaymiz
                request.session.update({"admin_user_id": user.id})
                return True
        finally:
            db.close()

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        # Sessionda admin_user_id bo‘lsa – login qilingan
        return bool(request.session.get("admin_user_id"))
