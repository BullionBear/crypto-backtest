from pydantic import BaseSettings


class Settings(BaseSettings):
    # Application Config
    APP_NAME: str = "Crypto Backtest"

    # Database Config
    DATABASE_URL: str = "mongodb://localhost:27017"

    # Security Config
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()