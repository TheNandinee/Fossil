"""Repository data collector.

Pulls everything Fossil needs about one repository through the GitHub client and
assembles a single normalized :class:`RepositorySnapshot`.
"""

from __future__ import annotations

from datetime import UTC, datetime

from fossil.api import GitHubClient
from fossil.collection.parsers import (
    parse_commit,
    parse_contributor,
    parse_issue,
    parse_release,
)
from fossil.config import get_logger
from fossil.core.exceptions import NotFoundError
from fossil.models import Contributor, RepositorySnapshot

logger = get_logger(__name__)


class RepositoryCollector:
    """Collect and normalize all data for a single repository."""

    def __init__(
        self,
        client: GitHubClient,
        *,
        max_commits: int = 100,
        max_issues: int = 100,
        max_contributors: int = 100,
    ) -> None:
        self._client = client
        self._max_commits = max_commits
        self._max_issues = max_issues
        self._max_contributors = max_contributors

    def collect(self, full_name: str) -> RepositorySnapshot:
        """Collect a full snapshot for ``owner/name``."""
        logger.info("Collecting %s", full_name)
        repo = self._client.get(f"/repos/{full_name}")

        commits = [
            parse_commit(c)
            for c in self._client.paginate(
                f"/repos/{full_name}/commits", max_items=self._max_commits
            )
        ]
        issues = [
            parse_issue(i)
            for i in self._client.paginate(
                f"/repos/{full_name}/issues",
                params={"state": "all"},
                max_items=self._max_issues,
            )
        ]
        contributors = self._collect_contributors(full_name)
        releases = [
            parse_release(r)
            for r in self._client.paginate(f"/repos/{full_name}/releases", max_items=50)
        ]

        owner_name = full_name.split("/", 1)
        return RepositorySnapshot(
            full_name=full_name,
            owner=owner_name[0],
            name=owner_name[1] if len(owner_name) > 1 else full_name,
            url=repo.get("html_url", f"https://github.com/{full_name}"),
            description=repo.get("description"),
            primary_language=repo.get("language"),
            topics=repo.get("topics", []),
            license_spdx=(repo.get("license") or {}).get("spdx_id"),
            is_archived=repo.get("archived", False),
            is_fork=repo.get("fork", False),
            stars=repo.get("stargazers_count", 0),
            forks=repo.get("forks_count", 0),
            open_issues=repo.get("open_issues_count", 0),
            created_at=_parse_dt(repo.get("created_at")),
            pushed_at=_parse_dt_opt(repo.get("pushed_at")),
            updated_at=_parse_dt_opt(repo.get("updated_at")),
            commits=commits,
            issues=issues,
            contributors=contributors,
            releases=releases,
            collected_at=datetime.now(UTC),
        )

    def _collect_contributors(self, full_name: str) -> list[Contributor]:
        try:
            return [
                parse_contributor(c)
                for c in self._client.paginate(
                    f"/repos/{full_name}/contributors",
                    max_items=self._max_contributors,
                )
            ]
        except NotFoundError:
            return []


def _parse_dt(value: str | None) -> datetime:
    if not value:
        return datetime.now(UTC)
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _parse_dt_opt(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
