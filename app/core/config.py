from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    UPLOAD_DIR: str = "uploads"
    SECRET_KEY: str

    DEFAULT_EXPIRY_MINUTES: int = 60
    MIN_EXPIRY_MINUTES: int = 5
    MAX_EXPIRY_MINUTES: int = 10080

    class Config:
        env_file = ".env"

settings = Settings()