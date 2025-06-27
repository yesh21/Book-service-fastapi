from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./bookreviews.db"

    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_ttl: int = 300  # 5 minutes

    # Application
    app_name: str = "Book Review Service"
    debug: bool = False

    # Logging
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
