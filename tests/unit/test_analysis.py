from fossil.analysis import run_analyzers
from fossil.models import RepositorySnapshot


def test_analyzers_emit_evidence(abandoned_snapshot: RepositorySnapshot) -> None:
    results = run_analyzers(abandoned_snapshot)
    names = {r.analyzer for r in results}
    assert names == {"commits", "contributors", "issues", "releases"}
    assert any(e for r in results for e in r.evidence)


def test_commit_recency_is_measured(abandoned_snapshot: RepositorySnapshot) -> None:
    results = {r.analyzer: r for r in run_analyzers(abandoned_snapshot)}
    metrics = results["commits"].metrics.metrics
    assert metrics["days_since_last_commit"] > 365
