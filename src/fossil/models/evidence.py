"""Evidence and metric models — the heart of Fossil's explainability.

Every analyzer emits a list of :class:`Evidence` items. An evidence item is a
single, human-readable, measurable observation about a repository. Conclusions
elsewhere in the system must trace back to evidence; nothing is asserted
without a measurement behind it.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class Severity(StrEnum):
    """How strongly an observation points toward abandonment."""

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Evidence(BaseModel):
    """One measurable observation produced by an analyzer."""

    analyzer: str  # which analyzer produced this (e.g. "commits")
    code: str  # stable machine code, e.g. "no_recent_commits"
    summary: str  # human sentence, e.g. "No commits in 912 days"
    severity: Severity = Severity.INFO
    value: float | int | str | None = None  # the underlying measurement
    unit: str | None = None  # e.g. "days", "percent"


class MetricSet(BaseModel):
    """Structured numeric metrics for one analyzer.

    Kept separate from :class:`Evidence` so downstream consumers can do math on
    raw numbers (e.g. predictive models) without parsing prose.
    """

    analyzer: str
    metrics: dict[str, float] = Field(default_factory=dict)


class AnalysisResult(BaseModel):
    """The combined output of a single analyzer."""

    analyzer: str
    evidence: list[Evidence] = Field(default_factory=list)
    metrics: MetricSet
