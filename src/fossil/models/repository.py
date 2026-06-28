"""Normalized GitHub repository data models.

These are the typed, source-of-truth representations the rest of the pipeline
consumes. Raw GitHub JSON is parsed into these models exactly once, in the
collection layer; nothing downstream touches raw API responses.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class Commit(BaseModel):
    """A single commit, reduced to the fields Fossil reasons about."""

    sha: str
    author_login: str | None = None
    authored_at: datetime
    message: str = ""


class Issue(BaseModel):
    """A GitHub issue or pull request (GitHub treats PRs as issues)."""

    number: int
    title: str = ""
    state: str
    is_pull_request: bool = False
    created_at: datetime
    closed_at: datetime | None = None
    first_response_at: datetime | None = None


class Contributor(BaseModel):
    """A contributor and their commit count."""

    login: str
    contributions: int = 0


class Release(BaseModel):
    """A published release or tag."""

    tag: str
    published_at: datetime | None = None


class RepositorySnapshot(BaseModel):
    """A complete, normalized snapshot of one repository at collection time.

    This is the single input to the analysis layer. It is fully serializable,
    so a snapshot can be archived and re-analyzed deterministically later.
    """

    # Identity
    full_name: str  # "owner/name"
    owner: str
    name: str
    url: str

    # Descriptive metadata
    description: str | None = None
    primary_language: str | None = None
    topics: list[str] = Field(default_factory=list)
    license_spdx: str | None = None
    is_archived: bool = False
    is_fork: bool = False

    # Headline counts
    stars: int = 0
    forks: int = 0
    open_issues: int = 0

    # Lifecycle timestamps
    created_at: datetime
    pushed_at: datetime | None = None
    updated_at: datetime | None = None

    # Collected detail (may be truncated to a window by the collector)
    commits: list[Commit] = Field(default_factory=list)
    issues: list[Issue] = Field(default_factory=list)
    contributors: list[Contributor] = Field(default_factory=list)
    releases: list[Release] = Field(default_factory=list)

    # Provenance
    collected_at: datetime

    @property
    def has_readme(self) -> bool:
        return bool(self.description)
