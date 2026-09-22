from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    cors_origins: str = "http://localhost:3000"

    groq_api_key: str = ""
    groq_model: str = "openai/gpt-oss-120b"

    openweather_api_key: str = ""

    cache_ttl_seconds: int = 600

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
