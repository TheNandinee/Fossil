"""Base contract for analyzers.

An analyzer is a pure function of a :class:`RepositorySnapshot`: given the same
snapshot it must always produce the same evidence and metrics. Analyzers never
call GitHub and never classify — they only measure.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from fossil.models import AnalysisResult, RepositorySnapshot


class Analyzer(ABC):
    """Abstract base class for all analyzers."""

    #: Stable identifier, used as the ``analyzer`` field on emitted evidence.
    name: str

    @abstractmethod
    def analyze(self, snapshot: RepositorySnapshot) -> AnalysisResult:
        """Measure one dimension of the repository and emit structured output."""
        raise NotImplementedError
