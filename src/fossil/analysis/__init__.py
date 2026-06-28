"""Analysis layer: pure, deterministic evidence producers."""

from __future__ import annotations

from fossil.analysis.base import Analyzer
from fossil.analysis.commits import CommitActivityAnalyzer
from fossil.analysis.contributors import ContributorAnalyzer
from fossil.analysis.issues import IssueResponsivenessAnalyzer
from fossil.analysis.registry import default_analyzers, run_analyzers
from fossil.analysis.releases import ReleaseAnalyzer

__all__ = [
    "Analyzer",
    "CommitActivityAnalyzer",
    "ContributorAnalyzer",
    "IssueResponsivenessAnalyzer",
    "ReleaseAnalyzer",
    "default_analyzers",
    "run_analyzers",
]
