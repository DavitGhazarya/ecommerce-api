from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DATABASE_URL: str = (
        "postgresql://postgres:password@localhost:5432/ecommerce_db"
    )

    SECRET_KEY: str = "change-this-to-a-random-secret-string"

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    PROJECT_NAME: str = "E-commerce API"


    SMTP_HOST: str | None = None

    SMTP_PORT: int | None = None

    EMAIL_USER: str | None = None

    EMAIL_PASSWORD: str | None = None


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
