# 🦴 Fossil

**Fossil is an automated archaeology tool for open-source software.** Every week it discovers GitHub repositories that have gone quiet, runs a measurable evidence pipeline over their commit history, contributor patterns, issue responsiveness, and release cadence — and produces a structured verdict explaining exactly why each one stopped evolving.

No opinions. No AI guessing. Every conclusion traces back to a number.

![autopsies](https://img.shields.io/badge/autopsies-21-blue)
![updated](https://img.shields.io/badge/updated-2026_06_28-green)
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


## 🕳️ Excavations

| # | Repository | Cause | Death score |
| ---: | --- | --- | ---: |
| 1 | [answershuto/learnVue](reports/repositories/answershuto__learnVue.md) | `maintainer_abandonment` | 0.95 |
| 2 | [fighting41love/funNLP](reports/repositories/fighting41love__funNLP.md) | `maintainer_abandonment` | 0.94 |
| 3 | [xingshaocheng/architect-awesome](reports/repositories/xingshaocheng__architect-awesome.md) | `maintainer_abandonment` | 0.94 |
| 4 | [datastacktv/data-engineer-roadmap](reports/repositories/datastacktv__data-engineer-roadmap.md) | `maintainer_abandonment` | 0.94 |
| 5 | [zalandoresearch/fashion-mnist](reports/repositories/zalandoresearch__fashion-mnist.md) | `maintainer_abandonment` | 0.93 |
| 6 | [GrowingGit/GitHub-Chinese-Top-Charts](reports/repositories/GrowingGit__GitHub-Chinese-Top-Charts.md) | `bus_factor_collapse` | 0.91 |
| 7 | [justjavac/free-programming-books-zh_CN](reports/repositories/justjavac__free-programming-books-zh_CN.md) | `maintainer_abandonment` | 0.90 |
| 8 | [nvbn/thefuck](reports/repositories/nvbn__thefuck.md) | `maintainer_abandonment` | 0.89 |
| 9 | [PanJiaChen/vue-element-admin](reports/repositories/PanJiaChen__vue-element-admin.md) | `maintainer_abandonment` | 0.87 |
| 10 | [necolas/normalize.css](reports/repositories/necolas__normalize.css.md) | `maintainer_abandonment` | 0.85 |
| 11 | [prakhar1989/awesome-courses](reports/repositories/prakhar1989__awesome-courses.md) | `maintainer_abandonment` | 0.85 |
| 12 | [ryanmcdermott/clean-code-javascript](reports/repositories/ryanmcdermott__clean-code-javascript.md) | `maintainer_abandonment` | 0.84 |
| 13 | [tiimgreen/github-cheat-sheet](reports/repositories/tiimgreen__github-cheat-sheet.md) | `maintainer_abandonment` | 0.82 |
| 14 | [jlevy/the-art-of-command-line](reports/repositories/jlevy__the-art-of-command-line.md) | `maintainer_abandonment` | 0.81 |
| 15 | [animate-css/animate.css](reports/repositories/animate-css__animate.css.md) | `maintainer_abandonment` | 0.80 |
| 16 | [scutan90/DeepLearning-500-questions](reports/repositories/scutan90__DeepLearning-500-questions.md) | `maintainer_abandonment` | 0.80 |
| 17 | [CompVis/stable-diffusion](reports/repositories/CompVis__stable-diffusion.md) | `maintainer_abandonment` | 0.76 |
| 18 | [resume/resume.github.com](reports/repositories/resume__resume.github.com.md) | `maintainer_abandonment` | 0.72 |
| 19 | [react/create-react-app](reports/repositories/react__create-react-app.md) | `maintainer_abandonment` | 0.64 |
| 20 | [ByteByteGoHq/system-design-101](reports/repositories/ByteByteGoHq__system-design-101.md) | `dormant` | 0.51 |
| 21 | [deepseek-ai/DeepSeek-R1](reports/repositories/deepseek-ai__DeepSeek-R1.md) | `dormant` | 0.45 |

## ⚰️ Most common causes of death

- `maintainer_abandonment`: 18
- `dormant`: 2
- `bus_factor_collapse`: 1

**Total projects excavated: 21**


## 🤖 Automation

This README and every report are regenerated automatically by GitHub Actions. No human writes these conclusions; each one traces back to measurable repository signals.

