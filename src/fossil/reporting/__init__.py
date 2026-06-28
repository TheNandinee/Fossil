"""Reporting layer: structured data -> Markdown."""

from __future__ import annotations

from fossil.reporting.readme import render_readme
from fossil.reporting.renderer import (
    render_repository_report,
    render_weekly_report,
)

__all__ = [
    "render_readme",
    "render_repository_report",
    "render_weekly_report",
]
