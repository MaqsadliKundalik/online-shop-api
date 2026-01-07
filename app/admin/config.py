from fastapi_admin.app import app as admin_app
from fastapi import FastAPI
from fastapi_admin.providers.login import UsernamePasswordProvider
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings
from app.models.user import AdminUser
from fastapi_admin.resources import Model
from app.models.category import Category
from app.models.product import Product


async def create_admin(app: FastAPI):
    admin_engine = create_async_engine(settings.DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://"))
    admin_session = async_sessionmaker(bind=admin_engine)

    await admin_app.configure(
        logo_url="https://fastapi-admin.github.io/img/logo.png",
        template_folders=["templates"],
        provider=UsernamePasswordProvider(
            admin_model=AdminUser,
            session_maker=admin_session,
        ),
        engine=admin_engine,
    )

    admin_app.register_resource(Model(AdminUser))
    admin_app.register_resource(Model(Category))
    admin_app.register_resource(Model(Product))
