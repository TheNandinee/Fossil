"""Pydantic schemas shared across every pipeline stage."""

from __future__ import annotations

from fossil.models.candidate import Candidate
from fossil.models.classification import Classification, DeathCause
from fossil.models.evidence import (
    AnalysisResult,
    Evidence,
    MetricSet,
    Severity,
)
from fossil.models.repository import (
    Commit,
    Contributor,
    Issue,
    Release,
    RepositorySnapshot,
)

__all__ = [
    "AnalysisResult",
    "Candidate",
    "Classification",
    "Commit",
    "Contributor",
    "DeathCause",
    "Evidence",
    "Issue",
    "MetricSet",
    "Release",
    "RepositorySnapshot",
    "Severity",
]
