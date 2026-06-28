from fossil.classification import classify
from fossil.models import RepositorySnapshot
from fossil.reporting import (
    render_readme,
    render_repository_report,
    render_weekly_report,
)


def test_reports_render(abandoned_snapshot: RepositorySnapshot) -> None:
    c = classify(abandoned_snapshot)
    assert "Autopsy" in render_repository_report(c, abandoned_snapshot)
    assert "Weekly" in render_weekly_report("2026-W26", [c])
    assert "Fossil" in render_readme([c])
