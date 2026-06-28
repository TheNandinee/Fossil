"""Commit-cadence analyzer: how recently and how often work happens."""

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


class CommitActivityAnalyzer(Analyzer):
    """Measures commit recency and long-term cadence."""

    name = "commits"

    def analyze(self, snapshot: RepositorySnapshot) -> AnalysisResult:
        evidence: list[Evidence] = []
        metrics: dict[str, float] = {}
        now = snapshot.collected_at

        commits = sorted(snapshot.commits, key=lambda c: c.authored_at)
        metrics["commit_count_window"] = float(len(commits))

        if not commits:
            evidence.append(
                Evidence(
                    analyzer=self.name,
                    code="no_commits_collected",
                    summary="No commits available in the collected window",
                    severity=Severity.MEDIUM,
                )
            )
            return AnalysisResult(
                analyzer=self.name,
                evidence=evidence,
                metrics=MetricSet(analyzer=self.name, metrics=metrics),
            )

        last = commits[-1].authored_at
        days_since_last = days_between(last, now)
        metrics["days_since_last_commit"] = round(days_since_last, 1)

        if days_since_last >= 365:
            sev = Severity.HIGH
        elif days_since_last >= 180:
            sev = Severity.MEDIUM
        elif days_since_last >= 90:
            sev = Severity.LOW
        else:
            sev = Severity.INFO
        evidence.append(
            Evidence(
                analyzer=self.name,
                code="last_commit_age",
                summary=f"Last commit was {int(days_since_last)} days ago",
                severity=sev,
                value=int(days_since_last),
                unit="days",
            )
        )

        span_days = days_between(commits[0].authored_at, last)
        if span_days > 0:
            per_month = len(commits) / (span_days / 30.0)
            metrics["commits_per_month"] = round(per_month, 2)
            evidence.append(
                Evidence(
                    analyzer=self.name,
                    code="commit_frequency",
                    summary=f"Averaged {per_month:.1f} commits/month over history",
                    severity=Severity.INFO,
                    value=round(per_month, 2),
                    unit="commits/month",
                )
            )

        return AnalysisResult(
            analyzer=self.name,
            evidence=evidence,
            metrics=MetricSet(analyzer=self.name, metrics=metrics),
        )
