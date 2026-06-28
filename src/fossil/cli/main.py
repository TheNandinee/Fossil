"""Fossil command-line interface.

Thin Typer wrapper over the pipeline and individual stages. The CLI does no
business logic — it only parses arguments and delegates.
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from fossil.api import GitHubClient
from fossil.classification import classify
from fossil.collection import RepositoryCollector
from fossil.config import configure_logging, get_settings
from fossil.discovery import DiscoveryEngine
from fossil.pipelines import run_weekly_excavation

app = typer.Typer(
    add_completion=False,
    help="🦴 Fossil — Digital Archaeology for Open Source.",
)
console = Console()


@app.callback()
def _setup() -> None:
    """Configure logging before any command runs."""
    configure_logging()


@app.command()
def excavate(
    limit: int = typer.Option(None, help="Number of repositories to excavate."),
    min_stars: int = typer.Option(50, help="Minimum stars to consider."),
    inactive_days: int = typer.Option(365, help="Days since last push."),
    language: str = typer.Option(None, help="Restrict to a language."),
) -> None:
    """Run a full weekly excavation cycle."""
    results = run_weekly_excavation(
        limit=limit,
        min_stars=min_stars,
        inactive_days=inactive_days,
        language=language,
    )
    table = Table(title="Excavation results")
    table.add_column("Repository")
    table.add_column("Cause")
    table.add_column("Score", justify="right")
    for c in results:
        table.add_row(c.full_name, c.cause.value, f"{c.death_score:.2f}")
    console.print(table)


@app.command()
def discover(
    min_stars: int = typer.Option(50),
    inactive_days: int = typer.Option(365),
    language: str = typer.Option(None),
    limit: int = typer.Option(10),
) -> None:
    """List candidate repositories without collecting or classifying them."""
    with GitHubClient() as client:
        candidates = DiscoveryEngine(client).discover(
            min_stars=min_stars,
            inactive_days=inactive_days,
            language=language,
            limit=limit,
        )
    for c in candidates:
        console.print(f"[bold]{c.full_name}[/] ⭐{c.stars}")


@app.command()
def autopsy(full_name: str = typer.Argument(..., help="owner/name")) -> None:
    """Collect and classify a single repository, printing the verdict."""
    with GitHubClient() as client:
        snapshot = RepositoryCollector(client).collect(full_name)
    result = classify(snapshot)
    console.print(f"[bold]{result.full_name}[/]")
    console.print(f"Cause:      [red]{result.cause.value}[/]")
    console.print(f"Death score: {result.death_score:.2f}")
    console.print(f"Confidence:  {result.confidence:.0%}")
    for e in result.supporting_evidence:
        console.print(f"  • [{e.severity.value}] {e.summary}")


@app.command()
def config() -> None:
    """Print the resolved (non-secret) configuration."""
    s = get_settings()
    console.print(f"API URL:        {s.github_api_url}")
    console.print(f"Token present:  {bool(s.github_token)}")
    console.print(f"Reports/run:    {s.reports_per_run}")
    console.print(f"Data dir:       {s.data_dir}")


if __name__ == "__main__":
    app()
