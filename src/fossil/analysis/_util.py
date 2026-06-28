"""Internal helpers shared by analyzers."""

from __future__ import annotations

from datetime import UTC, datetime


def days_between(earlier: datetime, later: datetime) -> float:
    """Return the number of whole-ish days between two datetimes (>= 0)."""
    a = _aware(earlier)
    b = _aware(later)
    return max(0.0, (b - a).total_seconds() / 86400.0)


def _aware(dt: datetime) -> datetime:
    """Coerce naive datetimes to UTC so subtraction never raises."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt
