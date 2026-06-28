"""README generator: regenerate the repository's front page from data.

The README is just another renderer over accumulated classifications, so the
repository front page always reflects the current state of the museum.
"""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime

from fossil.models import Classification

_HEADER = """# 🦴 Fossil

> **Digital Archaeology for Open Source.**
> Fossil automatically excavates abandoned GitHub repositories and explains,
> with measurable evidence, why they stopped evolving.

![autopsies](https://img.shields.io/badge/autopsies-{count}-blue)
![updated](https://img.shields.io/badge/updated-{date}-green)
"""


def render_readme(all_classifications: list[Classification]) -> str:
    """Build the full README.md content from every classification to date."""
    count = len(all_classifications)
    today = datetime.now(UTC).date().isoformat()
    lines = [_HEADER.format(count=count, date=today), ""]

    recent = sorted(all_classifications, key=lambda c: c.death_score, reverse=True)[:10]
    lines.append("## 🕳️ Recent excavations\n")
    lines.append("| Repository | Cause | Death score |")
    lines.append("| --- | --- | ---: |")
    for c in recent:
        link = f"reports/repositories/{c.full_name.replace('/', '__')}.md"
        lines.append(
            f"| [{c.full_name}]({link}) | `{c.cause.value}` " f"| {c.death_score:.2f} |"
        )

    causes = Counter(c.cause.value for c in all_classifications)
    lines.append("\n## ⚰️ Most common causes of death\n")
    for cause, n in causes.most_common():
        lines.append(f"- `{cause}`: {n}")

    lines.append("\n## 🤖 Automation\n")
    lines.append(
        "This README and every report are regenerated automatically by "
        "GitHub Actions. No human writes these conclusions; each one traces "
        "back to measurable repository signals.\n"
    )
    return "\n".join(lines) + "\n"
