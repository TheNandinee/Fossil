"""Typed, centralized application configuration.

Nothing outside this module should read ``os.environ`` directly. Every other
module imports :data:`fossil.config.settings`.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# src/fossil/config/settings.py -> config -> fossil -> src -> <root>
PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables / .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    github_token: str = Field(default="", alias="GITHUB_TOKEN")

    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_json: bool = Field(default=False, alias="LOG_JSON")

    reports_per_run: int = Field(default=3, alias="REPORTS_PER_RUN", ge=1)
    discovery_batch_size: int = Field(
        default=50, alias="DISCOVERY_BATCH_SIZE", ge=1, le=100
    )

    request_timeout: float = Field(default=30.0, alias="REQUEST_TIMEOUT", gt=0)
    max_retries: int = Field(default=5, alias="MAX_RETRIES", ge=0)
    github_api_url: str = Field(
        default="https://api.github.com", alias="GITHUB_API_URL"
    )

    data_dir: Path = Field(default=PROJECT_ROOT / "data", alias="DATA_DIR")
    reports_dir: Path = Field(default=PROJECT_ROOT / "reports", alias="REPORTS_DIR")

    @property
    def raw_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def normalized_dir(self) -> Path:
        return self.data_dir / "normalized"

    @property
    def cache_dir(self) -> Path:
        return self.data_dir / "cache"

    @property
    def checkpoints_dir(self) -> Path:
        return self.data_dir / "checkpoints"


@lru_cache
def get_settings() -> Settings:
    """Return a cached singleton ``Settings`` instance."""
    return Settings()
