"""Repository discovery engine."""

from __future__ import annotations

import random
from datetime import UTC, datetime, timedelta

from fossil.api import GitHubClient
from fossil.config import get_logger
from fossil.models import Candidate

logger = get_logger(__name__)


class DiscoveryEngine:
    """Find candidate repositories worth excavating."""

    def __init__(self, client: GitHubClient) -> None:
        self._client = client

    def discover(
        self,
        *,
        min_stars: int = 50,
        inactive_days: int = 365,
        language: str | None = None,
        limit: int = 50,
        seen: set[str] | None = None,
    ) -> list[Candidate]:
        seen = seen or set()
        cutoff = datetime.now(UTC) - timedelta(days=inactive_days)
        query = self._build_query(min_stars, cutoff, language)
        logger.info("Discovery query: %s", query)

        # Randomly pick a page between 1-5 to avoid always returning the same top repos
        page = random.randint(1, 5)
        logger.info("Discovery starting at page %d", page)

        candidates: list[Candidate] = []
        for item in self._client.paginate(
            "/search/repositories",
            params={"q": query, "sort": "stars", "order": "desc", "page": page},
            max_items=limit * 3,
        ):
            full_name = item.get("full_name")
            if not full_name or full_name in seen:
                continue
            candidates.append(
                Candidate(
                    full_name=full_name,
                    url=item.get("html_url", ""),
                    stars=item.get("stargazers_count", 0),
                    pushed_at=_parse_dt(item.get("pushed_at")),
                    primary_language=item.get("language"),
                    discovered_at=datetime.now(UTC),
                )
            )
            seen.add(full_name)
            if len(candidates) >= limit:
                break
        logger.info("Discovered %d candidates", len(candidates))
        return candidates

    @staticmethod
    def _build_query(min_stars: int, cutoff: datetime, language: str | None) -> str:
        parts = [
            f"stars:>={min_stars}",
            f"pushed:<{cutoff.date().isoformat()}",
            "archived:false",
            "is:public",
        ]
        if language:
            parts.append(f"language:{language}")
        return " ".join(parts)


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
