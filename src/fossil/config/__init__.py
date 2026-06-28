"""Configuration package: single source of truth for settings and logging."""

from __future__ import annotations

from fossil.config.logging import configure_logging, get_logger
from fossil.config.settings import Settings, get_settings

settings = get_settings()

__all__ = ["Settings", "configure_logging", "get_logger", "get_settings", "settings"]
