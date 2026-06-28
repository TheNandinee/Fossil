"""Weekly excavation pipeline: the top-level orchestrator.

Discovery -> Collection -> Classification -> Rendering -> README.
"""

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
from fossil.storage import (
    read_model,
    snapshot_path,
    write_model,
)

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

    classifications: list[Classification] = []

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

            write_model(
                classification,
                settings.normalized_dir
                / f"{snapshot.full_name.replace('/', '__')}_classification.json",
            )

            classifications.append(classification)

            report = render_repository_report(classification, snapshot)

            _write_text(
                settings.reports_dir
                / "repositories"
                / f"{snapshot.full_name.replace('/', '__')}.md",
                report,
            )

    if classifications:
        weekly_path = settings.reports_dir / "weekly" / f"{week}.md"

        new_section = render_weekly_report(
            datetime.now(UTC).isoformat(),
            classifications,
        )

        if weekly_path.exists():
            existing = weekly_path.read_text(encoding="utf-8")
            weekly = existing.rstrip() + "\n\n---\n\n" + new_section
        else:
            weekly = new_section

        _write_text(weekly_path, weekly)

        all_classifications: list[Classification] = []

        for file in sorted(settings.normalized_dir.glob("*_classification.json")):
            all_classifications.append(read_model(Classification, file))

        _regenerate_readme(
            settings.reports_dir,
            all_classifications,
        )

    logger.info("Excavation complete: %d reports", len(classifications))
    return classifications


def _load_seen(normalized_dir: Path) -> set[str]:
    if not normalized_dir.exists():
        return set()

    return {p.stem.replace("__", "/") for p in normalized_dir.glob("*.json")}


def _regenerate_readme(
    reports_dir: Path,
    all_classifications: list[Classification],
) -> None:
    readme = render_readme(all_classifications)
    _write_text(reports_dir.parent / "README.md", readme)


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
