"""Weekly excavation pipeline: the top-level orchestrator."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from fossil.api import GitHubClient
from fossil.classification import classify
from fossil.collection import RepositoryCollector
from fossil.config import get_logger, get_settings
from fossil.core.exceptions import FossilError
from fossil.discovery import DiscoveryEngine
from fossil.models import Classification
from fossil.reporting import (
    render_readme,
    render_repository_report,
    render_weekly_report,
)
from fossil.storage import read_model, snapshot_path, write_model

logger = get_logger(__name__)


def run_weekly_excavation(
    *,
    limit: int | None = None,
    min_stars: int = 50,
    inactive_days: int = 365,
    language: str | None = None,
) -> list[Classification]:
    """Run one full excavation cycle and write all artifacts to disk."""
    settings = get_settings()
    limit = limit or settings.reports_per_run
    week = datetime.now(UTC).strftime("%Y-W%V")

    new_classifications: list[Classification] = []
    with GitHubClient() as client:
        discovery = DiscoveryEngine(client)
        collector = RepositoryCollector(client)

        seen = _load_seen(settings.normalized_dir)
        candidates = discovery.discover(
            min_stars=min_stars,
            inactive_days=inactive_days,
            language=language,
            limit=limit,
            seen=seen,
        )

        for candidate in candidates:
            try:
                snapshot = collector.collect(candidate.full_name)
            except FossilError as exc:
                logger.warning("Skipping %s: %s", candidate.full_name, exc)
                continue

            write_model(
                snapshot,
                snapshot_path(settings.normalized_dir, snapshot.full_name),
            )
            classification = classify(snapshot)
            new_classifications.append(classification)

            # Persist classification alongside snapshot
            clf_path = (
                settings.normalized_dir
                / f"{snapshot.full_name.replace('/', '__')}_classification.json"
            )
            write_model(classification, clf_path)

            report = render_repository_report(classification, snapshot)
            _write_text(
                settings.reports_dir
                / "repositories"
                / f"{snapshot.full_name.replace('/', '__')}.md",
                report,
            )

    if new_classifications:
        weekly = render_weekly_report(week, new_classifications)
        _write_text(settings.reports_dir / "weekly" / f"{week}.md", weekly)

    # Always regenerate README from ALL accumulated classifications
    all_classifications = _load_all_classifications(settings.normalized_dir)
    _regenerate_readme(settings.reports_dir, all_classifications)

    logger.info(
        "Excavation complete: %d new reports (%d total)",
        len(new_classifications),
        len(all_classifications),
    )
    return new_classifications


def _load_seen(normalized_dir: Path) -> set[str]:
    if not normalized_dir.exists():
        return set()
    # Only snapshot files (not _classification.json)
    return {
        p.stem.replace("__", "/")
        for p in normalized_dir.glob("*.json")
        if "_classification" not in p.stem
    }


def _load_all_classifications(normalized_dir: Path) -> list[Classification]:
    """Load every persisted classification from disk."""
    results: list[Classification] = []
    if not normalized_dir.exists():
        return results
    for file in sorted(normalized_dir.glob("*_classification.json")):
        try:
            results.append(read_model(Classification, file))
        except Exception as exc:
            logger.warning("Could not load classification %s: %s", file, exc)
    return results


def _regenerate_readme(
    reports_dir: Path, all_classifications: list[Classification]
) -> None:
    readme = render_readme(all_classifications)
    _write_text(reports_dir.parent / "README.md", readme)


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
