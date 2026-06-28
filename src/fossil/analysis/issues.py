"""Issue analyzer: responsiveness and backlog health."""

from __future__ import annotations

from statistics import median

from fossil.analysis._util import days_between
from fossil.analysis.base import Analyzer
from fossil.models import (
    AnalysisResult,
    Evidence,
    MetricSet,
    RepositorySnapshot,
    Severity,
)


class IssueResponsivenessAnalyzer(Analyzer):
    """Measures how quickly issues are responded to and closed."""

    name = "issues"

    def analyze(self, snapshot: RepositorySnapshot) -> AnalysisResult:
        evidence: list[Evidence] = []
        metrics: dict[str, float] = {}

        issues = [i for i in snapshot.issues if not i.is_pull_request]
        open_issues = [i for i in issues if i.state == "open"]
        metrics["issue_count"] = float(len(issues))
        metrics["open_issue_count"] = float(len(open_issues))

        response_lags = [
            days_between(i.created_at, i.first_response_at)
            for i in issues
            if i.first_response_at is not None
        ]
        if response_lags:
            med = median(response_lags)
            metrics["median_response_days"] = round(med, 1)
            sev = (
                Severity.HIGH
                if med >= 30
                else Severity.MEDIUM
                if med >= 7
                else Severity.INFO
            )
            evidence.append(
                Evidence(
                    analyzer=self.name,
                    code="median_response_time",
                    summary=f"Median first response to issues: {med:.0f} days",
                    severity=sev,
                    value=round(med, 1),
                    unit="days",
                )
            )

        if issues and not response_lags:
            evidence.append(
                Evidence(
                    analyzer=self.name,
                    code="no_responses",
                    summary="Issues exist but none received any response",
                    severity=Severity.HIGH,
                )
            )

        return AnalysisResult(
            analyzer=self.name,
            evidence=evidence,
            metrics=MetricSet(analyzer=self.name, metrics=metrics),
        )
