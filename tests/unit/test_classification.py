from fossil.classification import classify
from fossil.models import DeathCause, RepositorySnapshot


def test_abandoned_repo_scores_high(abandoned_snapshot: RepositorySnapshot) -> None:
    result = classify(abandoned_snapshot)
    assert result.death_score > 0.6
    assert result.cause in {
        DeathCause.BUS_FACTOR_COLLAPSE,
        DeathCause.MAINTAINER_ABANDONMENT,
    }
    assert 0.0 <= result.confidence <= 1.0
    assert result.supporting_evidence
