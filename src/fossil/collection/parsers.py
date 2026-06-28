"""Parse raw GitHub JSON into normalized models.

This is the *only* place raw GitHub payloads are interpreted. Keeping parsing
isolated means a GitHub schema change touches one file.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from fossil.models import Commit, Contributor, Issue, Release


def _dt(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def parse_commit(raw: dict[str, Any]) -> Commit:
    commit = raw.get("commit", {})
    author = commit.get("author", {}) or {}
    gh_author = raw.get("author") or {}
    return Commit(
        sha=raw.get("sha", ""),
        author_login=gh_author.get("login"),
        authored_at=_dt(author.get("date")) or datetime.now(),
        message=(commit.get("message") or "").splitlines()[0][:200],
    )


def parse_issue(raw: dict[str, Any]) -> Issue:
    return Issue(
        number=raw.get("number", 0),
        title=raw.get("title", "")[:200],
        state=raw.get("state", "open"),
        is_pull_request="pull_request" in raw,
        created_at=_dt(raw.get("created_at")) or datetime.now(),
        closed_at=_dt(raw.get("closed_at")),
    )


def parse_contributor(raw: dict[str, Any]) -> Contributor:
    return Contributor(
        login=raw.get("login", "unknown"),
        contributions=raw.get("contributions", 0),
    )


def parse_release(raw: dict[str, Any]) -> Release:
    return Release(
        tag=raw.get("tag_name", ""),
        published_at=_dt(raw.get("published_at")),
    )
