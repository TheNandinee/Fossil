"""Cross-cutting abstractions: exceptions, protocols, shared contracts."""

from __future__ import annotations

from fossil.core.exceptions import (
    ConfigError,
    FossilError,
    GitHubAPIError,
    NotFoundError,
    RateLimitError,
    StorageError,
)

__all__ = [
    "ConfigError",
    "FossilError",
    "GitHubAPIError",
    "NotFoundError",
    "RateLimitError",
    "StorageError",
]
