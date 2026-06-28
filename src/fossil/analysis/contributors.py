"""Contributor analyzer: bus factor and maintainer concentration."""

from __future__ import annotations

from fossil.analysis.base import Analyzer
from fossil.models import (
    AnalysisResult,
    Evidence,
    MetricSet,
    RepositorySnapshot,
    Severity,
)


class ContributorAnalyzer(Analyzer):
    """Measures how concentrated authorship is among contributors."""

    name = "contributors"

    def analyze(self, snapshot: RepositorySnapshot) -> AnalysisResult:
        evidence: list[Evidence] = []
        metrics: dict[str, float] = {}

        contributors = sorted(
            snapshot.contributors, key=lambda c: c.contributions, reverse=True
        )
        total = sum(c.contributions for c in contributors)
        metrics["contributor_count"] = float(len(contributors))
        metrics["total_contributions"] = float(total)

        if not contributors or total == 0:
            evidence.append(
                Evidence(
                    analyzer=self.name,
                    code="no_contributor_data",
                    summary="No contributor data available",
                    severity=Severity.LOW,
                )
            )
            return AnalysisResult(
                analyzer=self.name,
                evidence=evidence,
                metrics=MetricSet(analyzer=self.name, metrics=metrics),
            )

        top = contributors[0]
        top_share = top.contributions / total
        metrics["top_contributor_share"] = round(top_share, 3)

        if len(contributors) == 1:
            evidence.append(
                Evidence(
                    analyzer=self.name,
                    code="single_maintainer",
                    summary="Project has a single contributor (bus factor 1)",
                    severity=Severity.HIGH,
                    value=1,
                )
            )
        elif top_share >= 0.9:
            evidence.append(
                Evidence(
                    analyzer=self.name,
                    code="high_concentration",
                    summary=(
                        f"Top contributor authored {top_share * 100:.0f}% of work"
                    ),
                    severity=Severity.MEDIUM,
                    value=round(top_share, 3),
                    unit="share",
                )
            )

        return AnalysisResult(
            analyzer=self.name,
            evidence=evidence,
            metrics=MetricSet(analyzer=self.name, metrics=metrics),
        )
