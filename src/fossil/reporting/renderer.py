"""Markdown rendering. Templates are the *only* place report layout lives.

Renderers are pure transformations over structured data: they never compute
metrics, never call GitHub, and never classify.
"""

from __future__ import annotations

from collections import Counter

from jinja2 import Environment, PackageLoader, select_autoescape

from fossil.models import Classification, RepositorySnapshot

_env = Environment(
    loader=PackageLoader("fossil.reporting", "templates"),
    autoescape=select_autoescape(enabled_extensions=()),
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=True,
)


def render_repository_report(
    classification: Classification, snapshot: RepositorySnapshot
) -> str:
    """Render a single repository's autopsy as Markdown."""
    template = _env.get_template("repository.md.j2")
    return template.render(c=classification, snapshot=snapshot)


def render_weekly_report(week: str, classifications: list[Classification]) -> str:
    """Render the weekly summary report as Markdown."""
    cause_counts = Counter(c.cause.value for c in classifications)
    template = _env.get_template("weekly.md.j2")
    return template.render(
        week=week,
        classifications=classifications,
        cause_counts=dict(cause_counts),
    )
