from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "Recall Meeting Intelligence API"
    app_env: str = "development"
    database_url: str = "sqlite:///./meeting_intelligence.db"
    cors_origins: str = "http://localhost:3000,http://localhost:3001"

    @property
    def origins(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
