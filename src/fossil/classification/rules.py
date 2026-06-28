"""Rule-based cause assignment.

Given the death score and feature vector, pick the single most defensible cause
from the taxonomy. Rules are ordered by specificity; the first match wins.
"""

from __future__ import annotations

from fossil.models import DeathCause, RepositorySnapshot


def assign_cause(
    snapshot: RepositorySnapshot,
    features: dict[str, float],
    death_score: float,
) -> DeathCause:
    """Return the most defensible cause of death for a repository."""
    if snapshot.is_archived:
        return DeathCause.INTENTIONALLY_ARCHIVED

    days_commit = features.get("commits.days_since_last_commit", 0.0)
    commit_count = features.get("commits.commit_count_window", 0.0)
    top_share = features.get("contributors.top_contributor_share", 0.0)
    contributor_count = features.get("contributors.contributor_count", 0.0)

    # Never really got going: very few commits, old, low engagement.
    if commit_count <= 10 and snapshot.stars < 10 and days_commit >= 365:
        return DeathCause.NEVER_LAUNCHED

    if death_score < 0.35:
        return DeathCause.ACTIVE

    if 0.35 <= death_score < 0.6:
        return DeathCause.DORMANT

    # Genuinely abandoned territory (score >= 0.6).
    if contributor_count <= 1 or top_share >= 0.9:
        return DeathCause.BUS_FACTOR_COLLAPSE

    if days_commit >= 365:
        return DeathCause.MAINTAINER_ABANDONMENT

    return DeathCause.UNKNOWN
