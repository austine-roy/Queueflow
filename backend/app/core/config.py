"""Environment-backed application settings."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, PositiveFloat
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings. DATABASE_URL must be supplied through the environment."""

    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parents[3] / ".env", extra="ignore")

    environment: str = "development"
    app_name: str = "QueueFlow"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    frontend_origin: str = "http://localhost:5173"
    database_url: str
    default_service_rate_per_minute: PositiveFloat = Field(default=2)
    busy_threshold: float = Field(default=0.50, ge=0, le=1)
    crowded_threshold: float = Field(default=0.75, ge=0, le=1)
    critical_threshold: float = Field(default=0.90, ge=0, le=1)
    queueflow_simulation_enabled: bool = False
    queueflow_simulation_interval: PositiveFloat = Field(default=2)
    queueflow_simulation_arrival_rate: float = Field(default=18, ge=0)
    queueflow_simulation_service_rate: float = Field(default=12, ge=0)
    queueflow_simulation_record_measurements: bool = True


@lru_cache
def get_settings() -> Settings:
    """Return cached settings after validating process environment values."""

    return Settings()
