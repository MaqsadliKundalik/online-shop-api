from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Online Shop"
    DEBUG: bool = True
    SECRET_KEY: str
    # Hozircha SQLite
    DATABASE_URL: str = "sqlite:///./db.sqlite3"
    class Config:
        env_file = ".env"


settings = Settings()
