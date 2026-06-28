# 🦴 Fossil

**Fossil is an automated archaeology tool for open-source software.** Every week it discovers GitHub repositories that have gone quiet, runs a measurable evidence pipeline over their commit history, contributor patterns, issue responsiveness, and release cadence — and produces a structured verdict explaining exactly why each one stopped evolving.

No opinions. No AI guessing. Every conclusion traces back to a number.

![autopsies](https://img.shields.io/badge/autopsies-34-blue)
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
| 1 | [tangyudi/Ai-Learn](reports/repositories/tangyudi__Ai-Learn.md) | `bus_factor_collapse` | 1.00 |
| 2 | [wong2/chatgpt-google-extension](reports/repositories/wong2__chatgpt-google-extension.md) | `bus_factor_collapse` | 0.97 |
| 3 | [pxb1988/dex2jar](reports/repositories/pxb1988__dex2jar.md) | `bus_factor_collapse` | 0.96 |
| 4 | [ttroy50/cmake-examples](reports/repositories/ttroy50__cmake-examples.md) | `maintainer_abandonment` | 0.95 |
| 5 | [answershuto/learnVue](reports/repositories/answershuto__learnVue.md) | `maintainer_abandonment` | 0.95 |
| 6 | [fighting41love/funNLP](reports/repositories/fighting41love__funNLP.md) | `maintainer_abandonment` | 0.94 |
| 7 | [xingshaocheng/architect-awesome](reports/repositories/xingshaocheng__architect-awesome.md) | `maintainer_abandonment` | 0.94 |
| 8 | [datastacktv/data-engineer-roadmap](reports/repositories/datastacktv__data-engineer-roadmap.md) | `maintainer_abandonment` | 0.94 |
| 9 | [zalandoresearch/fashion-mnist](reports/repositories/zalandoresearch__fashion-mnist.md) | `maintainer_abandonment` | 0.93 |
| 10 | [GrowingGit/GitHub-Chinese-Top-Charts](reports/repositories/GrowingGit__GitHub-Chinese-Top-Charts.md) | `bus_factor_collapse` | 0.91 |
| 11 | [francistao/LearningNotes](reports/repositories/francistao__LearningNotes.md) | `maintainer_abandonment` | 0.91 |
| 12 | [dennybritz/reinforcement-learning](reports/repositories/dennybritz__reinforcement-learning.md) | `maintainer_abandonment` | 0.90 |
| 13 | [justjavac/free-programming-books-zh_CN](reports/repositories/justjavac__free-programming-books-zh_CN.md) | `maintainer_abandonment` | 0.90 |
| 14 | [chiraggude/awesome-laravel](reports/repositories/chiraggude__awesome-laravel.md) | `maintainer_abandonment` | 0.89 |
| 15 | [nvbn/thefuck](reports/repositories/nvbn__thefuck.md) | `maintainer_abandonment` | 0.89 |
| 16 | [eligrey/FileSaver.js](reports/repositories/eligrey__FileSaver.js.md) | `maintainer_abandonment` | 0.87 |
| 17 | [PanJiaChen/vue-element-admin](reports/repositories/PanJiaChen__vue-element-admin.md) | `maintainer_abandonment` | 0.87 |
| 18 | [necolas/normalize.css](reports/repositories/necolas__normalize.css.md) | `maintainer_abandonment` | 0.85 |
| 19 | [prakhar1989/awesome-courses](reports/repositories/prakhar1989__awesome-courses.md) | `maintainer_abandonment` | 0.85 |
| 20 | [pytube/pytube](reports/repositories/pytube__pytube.md) | `maintainer_abandonment` | 0.85 |
| 21 | [ryanmcdermott/clean-code-javascript](reports/repositories/ryanmcdermott__clean-code-javascript.md) | `maintainer_abandonment` | 0.84 |
| 22 | [tiimgreen/github-cheat-sheet](reports/repositories/tiimgreen__github-cheat-sheet.md) | `maintainer_abandonment` | 0.82 |
| 23 | [TypeStrong/ts-node](reports/repositories/TypeStrong__ts-node.md) | `maintainer_abandonment` | 0.82 |
| 24 | [seemoo-lab/openhaystack](reports/repositories/seemoo-lab__openhaystack.md) | `maintainer_abandonment` | 0.81 |
| 25 | [jlevy/the-art-of-command-line](reports/repositories/jlevy__the-art-of-command-line.md) | `maintainer_abandonment` | 0.81 |
| 26 | [animate-css/animate.css](reports/repositories/animate-css__animate.css.md) | `maintainer_abandonment` | 0.80 |
| 27 | [scutan90/DeepLearning-500-questions](reports/repositories/scutan90__DeepLearning-500-questions.md) | `maintainer_abandonment` | 0.80 |
| 28 | [CompVis/stable-diffusion](reports/repositories/CompVis__stable-diffusion.md) | `maintainer_abandonment` | 0.76 |
| 29 | [resume/resume.github.com](reports/repositories/resume__resume.github.com.md) | `maintainer_abandonment` | 0.72 |
| 30 | [react/create-react-app](reports/repositories/react__create-react-app.md) | `maintainer_abandonment` | 0.64 |
| 31 | [Rudrabha/Wav2Lip](reports/repositories/Rudrabha__Wav2Lip.md) | `dormant` | 0.52 |
| 32 | [ByteByteGoHq/system-design-101](reports/repositories/ByteByteGoHq__system-design-101.md) | `dormant` | 0.51 |
| 33 | [deepseek-ai/DeepSeek-R1](reports/repositories/deepseek-ai__DeepSeek-R1.md) | `dormant` | 0.45 |
| 34 | [anthropics/courses](reports/repositories/anthropics__courses.md) | `dormant` | 0.36 |

## ⚰️ Most common causes of death

- `maintainer_abandonment`: 26
- `dormant`: 4
- `bus_factor_collapse`: 4

**Total projects excavated: 34**


## 🤖 Automation

This README and every report are regenerated automatically by GitHub Actions. No human writes these conclusions; each one traces back to measurable repository signals.

