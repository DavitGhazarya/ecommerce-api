from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/ecommerce_db"
    SECRET_KEY: str = "change-this-to-a-random-secret-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    PROJECT_NAME: str = "E-commerce API"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
