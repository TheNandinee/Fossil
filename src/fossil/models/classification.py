"""Classification models: causes of death and the final verdict."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field

from fossil.models.evidence import AnalysisResult, Evidence


class DeathCause(StrEnum):
    """The controlled taxonomy of abandonment causes (see docs/taxonomy)."""

    ACTIVE = "active"
    DORMANT = "dormant"
    MAINTAINER_ABANDONMENT = "maintainer_abandonment"
    BUS_FACTOR_COLLAPSE = "bus_factor_collapse"
    SUPERSEDED = "superseded"
    NEVER_LAUNCHED = "never_launched"
    COMMUNITY_COLLAPSE = "community_collapse"
    INTENTIONALLY_ARCHIVED = "intentionally_archived"
    UNKNOWN = "unknown"


class Classification(BaseModel):
    """The final, evidence-backed verdict for one repository."""

    full_name: str
    cause: DeathCause
    confidence: float = Field(ge=0.0, le=1.0)
    death_score: float = Field(ge=0.0, le=1.0)  # 0 = healthy, 1 = dead
    supporting_evidence: list[Evidence] = Field(default_factory=list)
    analyses: list[AnalysisResult] = Field(default_factory=list)
    # Optional natural-language autopsy written by the LLM from the evidence.
    narrative: str | None = None
