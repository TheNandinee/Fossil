"""Shared pytest fixtures."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from fossil.models import (
    Commit,
    Contributor,
    Issue,
    Release,
    RepositorySnapshot,
)


@pytest.fixture
def now() -> datetime:
    return datetime(2026, 6, 28, tzinfo=UTC)


@pytest.fixture
def abandoned_snapshot(now: datetime) -> RepositorySnapshot:
    old = now - timedelta(days=900)
    return RepositorySnapshot(
        full_name="ghost/abandoned-lib",
        owner="ghost",
        name="abandoned-lib",
        url="https://github.com/ghost/abandoned-lib",
        description="A once-promising library nobody maintains.",
        primary_language="Python",
        stars=420,
        forks=37,
        open_issues=15,
        created_at=now - timedelta(days=2000),
        pushed_at=old,
        updated_at=old,
        commits=[
            Commit(sha=f"s{i}", author_login="solo", authored_at=old) for i in range(8)
        ],
        issues=[
            Issue(
                number=i,
                state="open",
                created_at=now - timedelta(days=600),
                first_response_at=now - timedelta(days=500),
            )
            for i in range(5)
        ],
        contributors=[
            Contributor(login="solo", contributions=96),
            Contributor(login="helper", contributions=4),
        ],
        releases=[Release(tag="v1.0", published_at=old)],
        collected_at=now,
    )
