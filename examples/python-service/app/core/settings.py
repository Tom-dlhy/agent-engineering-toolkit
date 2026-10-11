from functools import lru_cache
from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="APP_", extra="ignore"
    )
    external_api_url: AnyHttpUrl
    external_api_timeout: float = Field(default=5.0, gt=0, le=60)

@lru_cache
def get_settings() -> Settings:
    return Settings()
