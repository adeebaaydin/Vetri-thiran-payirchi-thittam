from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "PocketSmart AI"

    secret_key: str = "change-this-secret-key"

    database_url: str = "sqlite:///./pocketsmart.db"

    google_api_key: str | None = None

    gemini_model: str = "gemini-2.5-flash"

    ai_enabled: bool = True

    max_upload_mb: int = 5

    allowed_origins: list[str] = [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ]

    session_cookie: str = "pocketsmart_session"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()