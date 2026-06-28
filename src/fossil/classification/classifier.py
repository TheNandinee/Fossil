"""Classifier: orchestrate features -> score -> cause -> verdict."""

from __future__ import annotations

from fossil.analysis import run_analyzers
from fossil.classification.features import extract_features
from fossil.classification.rules import assign_cause
from fossil.classification.scoring import compute_death_score
from fossil.config import get_logger
from fossil.models import (
    AnalysisResult,
    Classification,
    DeathCause,
    Evidence,
    RepositorySnapshot,
    Severity,
)

logger = get_logger(__name__)

_SEVERITY_RANK = {
    Severity.HIGH: 3,
    Severity.MEDIUM: 2,
    Severity.LOW: 1,
    Severity.INFO: 0,
}


def _select_supporting_evidence(
    analyses: list[AnalysisResult], limit: int = 6
) -> list[Evidence]:
    """Pick the strongest evidence items across all analyzers."""
    all_evidence = [e for r in analyses for e in r.evidence]
    all_evidence.sort(key=lambda e: _SEVERITY_RANK[e.severity], reverse=True)
    return all_evidence[:limit]


def _confidence(death_score: float, cause: DeathCause) -> float:
    """Confidence is higher the further the score is from the 0.5 boundary."""
    if cause in (DeathCause.UNKNOWN,):
        return 0.4
    return round(0.5 + abs(death_score - 0.5), 2)


def classify(snapshot: RepositorySnapshot) -> Classification:
    """Produce a full, evidence-backed classification for a snapshot."""
    analyses = run_analyzers(snapshot)
    features = extract_features(snapshot, analyses)
    death_score = compute_death_score(features)
    cause = assign_cause(snapshot, features, death_score)
    confidence = _confidence(death_score, cause)
    evidence = _select_supporting_evidence(analyses)

    logger.info(
        "Classified %s -> %s (score=%.2f, conf=%.2f)",
        snapshot.full_name,
        cause.value,
        death_score,
        confidence,
    )

    return Classification(
        full_name=snapshot.full_name,
        cause=cause,
        confidence=confidence,
        death_score=death_score,
        supporting_evidence=evidence,
        analyses=analyses,
    )
