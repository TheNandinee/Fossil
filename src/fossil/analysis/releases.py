"""Release analyzer: cadence of published releases."""

from __future__ import annotations

from fossil.analysis._util import days_between
from fossil.analysis.base import Analyzer
from fossil.models import (
    AnalysisResult,
    Evidence,
    MetricSet,
    RepositorySnapshot,
    Severity,
)


class ReleaseAnalyzer(Analyzer):
    """Measures recency of the most recent release."""

    name = "releases"

    def analyze(self, snapshot: RepositorySnapshot) -> AnalysisResult:
        evidence: list[Evidence] = []
        metrics: dict[str, float] = {}
        now = snapshot.collected_at

        dated = [r for r in snapshot.releases if r.published_at is not None]
        metrics["release_count"] = float(len(snapshot.releases))

        if not dated:
            evidence.append(
                Evidence(
                    analyzer=self.name,
                    code="no_releases",
                    summary="Project has never published a dated release",
                    severity=Severity.LOW,
                )
            )
            return AnalysisResult(
                analyzer=self.name,
                evidence=evidence,
                metrics=MetricSet(analyzer=self.name, metrics=metrics),
            )

        latest = max(r.published_at for r in dated if r.published_at)
        days = days_between(latest, now)
        metrics["days_since_last_release"] = round(days, 1)
        sev = (
            Severity.HIGH
            if days >= 730
            else Severity.MEDIUM
            if days >= 365
            else Severity.INFO
        )
        evidence.append(
            Evidence(
                analyzer=self.name,
                code="last_release_age",
                summary=f"Last release was {days / 365:.1f} years ago",
                severity=sev,
                value=int(days),
                unit="days",
            )
        )
        return AnalysisResult(
            analyzer=self.name,
            evidence=evidence,
            metrics=MetricSet(analyzer=self.name, metrics=metrics),
        )
