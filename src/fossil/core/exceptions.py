"""Project-wide exception hierarchy.

A single base class lets callers catch every Fossil-specific error with one
``except FossilError`` while still allowing fine-grained handling.
"""

from __future__ import annotations


class FossilError(Exception):
    """Base class for all Fossil errors."""


class ConfigError(FossilError):
    """Raised when configuration is missing or invalid."""


class GitHubAPIError(FossilError):
    """Raised when the GitHub API returns an unrecoverable error."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class RateLimitError(GitHubAPIError):
    """Raised when the GitHub rate limit is exhausted."""


class NotFoundError(GitHubAPIError):
    """Raised when a requested GitHub resource does not exist (404)."""


class StorageError(FossilError):
    """Raised when reading or writing persisted data fails."""
