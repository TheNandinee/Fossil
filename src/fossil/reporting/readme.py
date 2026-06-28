"""README generator: regenerate the repository's front page from data."""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime

from fossil.models import Classification

_HEADER = """# 🦴 Fossil

**Fossil is an automated archaeology tool for open-source software.** Every week it discovers GitHub repositories that have gone quiet, runs a measurable evidence pipeline over their commit history, contributor patterns, issue responsiveness, and release cadence — and produces a structured verdict explaining exactly why each one stopped evolving.

No opinions. No AI guessing. Every conclusion traces back to a number.

![autopsies](https://img.shields.io/badge/autopsies-{count}-blue)
![updated](https://img.shields.io/badge/updated-{date}-green)
[![Weekly Excavation](https://github.com/TheNandinee/Fossil/actions/workflows/weekly.yml/badge.svg)](https://github.com/TheNandinee/Fossil/actions/workflows/weekly.yml)

## 🔬 How it works

Each repository goes through a four-stage pipeline:

1. **Discovery** — GitHub search for inactive public repos above a star threshold
2. **Collection** — commits, issues, contributors, and releases pulled via the API
3. **Analysis** — pure, deterministic analyzers emit structured `Evidence` objects
4. **Classification** — a weighted death score and a cause from a controlled taxonomy

All data is stored as plain JSON. Every report is reproducible from disk alone.

## 🤝 Contributing

Want to excavate your own repositories or improve Fossil? Contributions are welcome.

### Run locally

```bash
git clone https://github.com/TheNandinee/Fossil.git
cd Fossil

uv sync
echo "GITHUB_TOKEN=ghp_yourtoken" > .env

uv run fossil excavate --limit 5
```

### Run the GitHub Action

The **Weekly Excavation** workflow can be triggered manually by repository maintainers.

If you've forked Fossil, enable GitHub Actions in your fork and trigger:

**Actions → Weekly Excavation → Run workflow**

### Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Open a Pull Request.

Bug fixes, new excavation strategies, provider integrations, performance improvements, and documentation updates are all welcome.

"""


def render_readme(all_classifications: list[Classification]) -> str:
    count = len(all_classifications)
    today = datetime.now(UTC).date().isoformat().replace("-", "_")
    lines = [_HEADER.format(count=count, date=today)]

    ranked = sorted(all_classifications, key=lambda c: c.death_score, reverse=True)

    lines.append("## 🕳️ Excavations\n")
    lines.append("| # | Repository | Cause | Death score |")
    lines.append("| ---: | --- | --- | ---: |")
    for i, c in enumerate(ranked, 1):
        link = f"reports/repositories/{c.full_name.replace('/', '__')}.md"
        lines.append(
            f"| {i} | [{c.full_name}]({link}) | `{c.cause.value}` "
            f"| {c.death_score:.2f} |"
        )

    causes = Counter(c.cause.value for c in all_classifications)
    lines.append("\n## ⚰️ Most common causes of death\n")
    for cause, n in causes.most_common():
        lines.append(f"- `{cause}`: {n}")

    lines.append(f"\n**Total projects excavated: {count}**\n")

    lines.append("\n## 🤖 Automation\n")
    lines.append(
        "This README and every report are regenerated automatically by "
        "GitHub Actions. No human writes these conclusions; each one traces "
        "back to measurable repository signals.\n"
    )
    return "\n".join(lines) + "\n"
