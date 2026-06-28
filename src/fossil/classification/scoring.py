"""Death scoring: turn features into a single 0..1 abandonment score.

The score is a transparent weighted blend of normalized signals. Every weight
is explicit and documented so the verdict is auditable — no opaque model.
"""

from __future__ import annotations


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def compute_death_score(features: dict[str, float]) -> float:
    """Return a 0 (healthy) .. 1 (dead) abandonment score."""
    components: list[tuple[float, float]] = []  # (signal, weight)

    days_commit = features.get("commits.days_since_last_commit")
    if days_commit is not None:
        # 0 days -> 0, 730+ days -> 1
        components.append((_clamp(days_commit / 730.0), 0.45))

    days_release = features.get("releases.days_since_last_release")
    if days_release is not None:
        components.append((_clamp(days_release / 1095.0), 0.15))

    response = features.get("issues.median_response_days")
    if response is not None:
        components.append((_clamp(response / 90.0), 0.15))

    concentration = features.get("contributors.top_contributor_share")
    if concentration is not None:
        components.append((_clamp(concentration), 0.25))

    if not components:
        return 0.0

    total_weight = sum(weight for _, weight in components)
    weighted = sum(signal * weight for signal, weight in components)
    return round(weighted / total_weight, 3)
