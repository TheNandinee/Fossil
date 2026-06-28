"""Classification layer: evidence -> cause of death."""

from __future__ import annotations

from fossil.classification.classifier import classify
from fossil.classification.features import extract_features
from fossil.classification.scoring import compute_death_score

__all__ = ["classify", "compute_death_score", "extract_features"]
