from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Online Shop"
    DEBUG: bool = True
    SECRET_KEY: str = "default-secret-key-change-in-production-123456789"
    BASE_URL: str = "https://tbozoz.uz"
    DATABASE_URL: str = "sqlite:///./test.db"
    class Config:
        env_file = ".env"


settings = Settings()
