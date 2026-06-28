"""Feature extraction: flatten analysis metrics into one feature vector.

Features are plain numbers derived only from analyzer metrics. Keeping feature
extraction separate from scoring means a future ML model can consume the exact
same vector the rule-based scorer uses.
"""

from __future__ import annotations

from fossil.models import AnalysisResult, RepositorySnapshot


def extract_features(
    snapshot: RepositorySnapshot,
    analyses: list[AnalysisResult],
) -> dict[str, float]:
    """Merge every analyzer's metrics into a single flat dict."""
    features: dict[str, float] = {}
    for result in analyses:
        for key, value in result.metrics.metrics.items():
            features[f"{result.analyzer}.{key}"] = value

    features["meta.stars"] = float(snapshot.stars)
    features["meta.forks"] = float(snapshot.forks)
    features["meta.is_archived"] = 1.0 if snapshot.is_archived else 0.0
    return features
