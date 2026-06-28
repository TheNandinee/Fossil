"""Analyzer registry and runner.

The registry decouples *which* analyzers exist from the code that runs them.
Adding a new analyzer is a one-line change here and requires no edits to the
pipeline — satisfying the open/closed principle.
"""

from __future__ import annotations

from fossil.analysis.base import Analyzer
from fossil.analysis.commits import CommitActivityAnalyzer
from fossil.analysis.contributors import ContributorAnalyzer
from fossil.analysis.issues import IssueResponsivenessAnalyzer
from fossil.analysis.releases import ReleaseAnalyzer
from fossil.config import get_logger
from fossil.models import AnalysisResult, RepositorySnapshot

logger = get_logger(__name__)


def default_analyzers() -> list[Analyzer]:
    """Return the default analyzer set, in deterministic order."""
    return [
        CommitActivityAnalyzer(),
        ContributorAnalyzer(),
        IssueResponsivenessAnalyzer(),
        ReleaseAnalyzer(),
    ]


def run_analyzers(
    snapshot: RepositorySnapshot,
    analyzers: list[Analyzer] | None = None,
) -> list[AnalysisResult]:
    """Run every analyzer against a snapshot and collect results."""
    analyzers = analyzers if analyzers is not None else default_analyzers()
    results: list[AnalysisResult] = []
    for analyzer in analyzers:
        logger.debug("Running analyzer %s on %s", analyzer.name, snapshot.full_name)
        results.append(analyzer.analyze(snapshot))
    return results
