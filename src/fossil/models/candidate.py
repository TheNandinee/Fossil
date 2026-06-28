"""Discovery candidate model — a repository worth investigating."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class Candidate(BaseModel):
    """A repository surfaced by discovery, before full collection."""

    full_name: str
    url: str
    stars: int = 0
    pushed_at: datetime | None = None
    primary_language: str | None = None
    discovered_at: datetime
