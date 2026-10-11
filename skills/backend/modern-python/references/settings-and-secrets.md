# Pydantic Settings v2 and fail-fast application configuration

**Read when:** building centralized configuration with env, dotenv, validation, cache and credentials.

~~~python
from functools import lru_cache
from typing import Literal
from pydantic import AnyHttpUrl, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8",
        env_prefix="APP_", extra="ignore"
    )
    environment: Literal["development", "staging", "production"] = "development"
    external_api_url: AnyHttpUrl  # deliberately required
    external_api_timeout: float = Field(default=5, gt=0, le=120)
    external_api_token: SecretStr | None = None

@lru_cache
def get_settings() -> Settings:
    return Settings()
~~~

The env prefix above expects APP_EXTERNAL_API_URL, not EXTERNAL_API_URL. Match .env.example and deployment config exactly. Environment variables override dotenv. Extra ignore is reasonable for a shared local env file but can hide misspellings; choose extra forbid when strict dedicated settings are possible.

## Ownership and lifecycle
Load once at startup/lifespan and inject via composition root; unit tests can override settings or clear cached factory. Permanent caching is unsuitable for expiring credentials or per-tenant config. Prefer cloud workload identity (AWS IAM role, Azure managed identity, GCP ADC) over permanent API keys. SecretStr helps avoid incidental repr exposure but is not encryption.

## Negative tests
Unset required var -> validation error before serving; invalid timeout/environment rejects; env overrides dotenv; test config override not contaminated by cache; secrets absent from logs/errors; no calls to arbitrary user-controlled URL (SSRF allowlist).

## Operational cautions
A .env file is not a production secret store; never commit it. Log only sanitized selected settings. Dynamic secret rotation requires its own credential lifecycle, not cached static values.

Official: https://docs.pydantic.dev/latest/concepts/pydantic_settings/ and https://pydantic.dev/docs/validation/2.12/concepts/pydantic_settings/ .
