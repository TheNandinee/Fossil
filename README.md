# 🦴 Fossil

**Fossil is an automated archaeology tool for open-source software.** Every week it discovers GitHub repositories that have gone quiet, runs a measurable evidence pipeline over their commit history, contributor patterns, issue responsiveness, and release cadence — and produces a structured verdict explaining exactly why each one stopped evolving.

No opinions. No AI guessing. Every conclusion traces back to a number.

![autopsies](https://img.shields.io/badge/autopsies-79-blue)
![updated](https://img.shields.io/badge/updated-2026_10_05-green)
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
| 1 | [adams549659584/go-proxy-bingai](reports/repositories/adams549659584__go-proxy-bingai.md) | `bus_factor_collapse` | 1.00 |
| 2 | [fengdu78/Data-Science-Notes](reports/repositories/fengdu78__Data-Science-Notes.md) | `bus_factor_collapse` | 1.00 |
| 3 | [tangyudi/Ai-Learn](reports/repositories/tangyudi__Ai-Learn.md) | `bus_factor_collapse` | 1.00 |
| 4 | [unknwon/go-fundamental-programming](reports/repositories/unknwon__go-fundamental-programming.md) | `bus_factor_collapse` | 1.00 |
| 5 | [MorvanZhou/tutorials](reports/repositories/MorvanZhou__tutorials.md) | `bus_factor_collapse` | 1.00 |
| 6 | [xuchengsheng/spring-reading](reports/repositories/xuchengsheng__spring-reading.md) | `bus_factor_collapse` | 1.00 |
| 7 | [donnemartin/gitsome](reports/repositories/donnemartin__gitsome.md) | `bus_factor_collapse` | 0.99 |
| 8 | [haltu/muuri](reports/repositories/haltu__muuri.md) | `bus_factor_collapse` | 0.99 |
| 9 | [forkingdog/UITableView-FDTemplateLayoutCell](reports/repositories/forkingdog__UITableView-FDTemplateLayoutCell.md) | `bus_factor_collapse` | 0.97 |
| 10 | [fastai/numerical-linear-algebra](reports/repositories/fastai__numerical-linear-algebra.md) | `bus_factor_collapse` | 0.97 |
| 11 | [wong2/chatgpt-google-extension](reports/repositories/wong2__chatgpt-google-extension.md) | `bus_factor_collapse` | 0.97 |
| 12 | [vahidk/EffectiveTensorflow](reports/repositories/vahidk__EffectiveTensorflow.md) | `bus_factor_collapse` | 0.96 |
| 13 | [jwagner/smartcrop.js](reports/repositories/jwagner__smartcrop.js.md) | `maintainer_abandonment` | 0.96 |
| 14 | [pxb1988/dex2jar](reports/repositories/pxb1988__dex2jar.md) | `bus_factor_collapse` | 0.96 |
| 15 | [zalmoxisus/redux-devtools-extension](reports/repositories/zalmoxisus__redux-devtools-extension.md) | `maintainer_abandonment` | 0.96 |
| 16 | [ttroy50/cmake-examples](reports/repositories/ttroy50__cmake-examples.md) | `maintainer_abandonment` | 0.95 |
| 17 | [answershuto/learnVue](reports/repositories/answershuto__learnVue.md) | `maintainer_abandonment` | 0.95 |
| 18 | [httpie/http-prompt](reports/repositories/httpie__http-prompt.md) | `maintainer_abandonment` | 0.94 |
| 19 | [fighting41love/funNLP](reports/repositories/fighting41love__funNLP.md) | `maintainer_abandonment` | 0.94 |
| 20 | [xingshaocheng/architect-awesome](reports/repositories/xingshaocheng__architect-awesome.md) | `maintainer_abandonment` | 0.94 |
| 21 | [oblador/react-native-animatable](reports/repositories/oblador__react-native-animatable.md) | `maintainer_abandonment` | 0.94 |
| 22 | [datastacktv/data-engineer-roadmap](reports/repositories/datastacktv__data-engineer-roadmap.md) | `maintainer_abandonment` | 0.94 |
| 23 | [gao-sun/eul](reports/repositories/gao-sun__eul.md) | `maintainer_abandonment` | 0.93 |
| 24 | [gnab/remark](reports/repositories/gnab__remark.md) | `maintainer_abandonment` | 0.93 |
| 25 | [gridsome/gridsome](reports/repositories/gridsome__gridsome.md) | `maintainer_abandonment` | 0.93 |
| 26 | [zalandoresearch/fashion-mnist](reports/repositories/zalandoresearch__fashion-mnist.md) | `maintainer_abandonment` | 0.93 |
| 27 | [TeamStuQ/skill-map](reports/repositories/TeamStuQ__skill-map.md) | `maintainer_abandonment` | 0.92 |
| 28 | [MorvanZhou/PyTorch-Tutorial](reports/repositories/MorvanZhou__PyTorch-Tutorial.md) | `maintainer_abandonment` | 0.92 |
| 29 | [skeeto/endlessh](reports/repositories/skeeto__endlessh.md) | `maintainer_abandonment` | 0.92 |
| 30 | [aalhour/awesome-compilers](reports/repositories/aalhour__awesome-compilers.md) | `maintainer_abandonment` | 0.91 |
| 31 | [GrowingGit/GitHub-Chinese-Top-Charts](reports/repositories/GrowingGit__GitHub-Chinese-Top-Charts.md) | `bus_factor_collapse` | 0.91 |
| 32 | [francistao/LearningNotes](reports/repositories/francistao__LearningNotes.md) | `maintainer_abandonment` | 0.91 |
| 33 | [paascloud/paascloud-master](reports/repositories/paascloud__paascloud-master.md) | `maintainer_abandonment` | 0.91 |
| 34 | [dennybritz/reinforcement-learning](reports/repositories/dennybritz__reinforcement-learning.md) | `maintainer_abandonment` | 0.90 |
| 35 | [justjavac/free-programming-books-zh_CN](reports/repositories/justjavac__free-programming-books-zh_CN.md) | `maintainer_abandonment` | 0.90 |
| 36 | [Bigkoo/Android-PickerView](reports/repositories/Bigkoo__Android-PickerView.md) | `maintainer_abandonment` | 0.90 |
| 37 | [zai-org/ChatGLM2-6B](reports/repositories/zai-org__ChatGLM2-6B.md) | `maintainer_abandonment` | 0.90 |
| 38 | [chenglou/react-motion](reports/repositories/chenglou__react-motion.md) | `maintainer_abandonment` | 0.89 |
| 39 | [chiraggude/awesome-laravel](reports/repositories/chiraggude__awesome-laravel.md) | `maintainer_abandonment` | 0.89 |
| 40 | [nvbn/thefuck](reports/repositories/nvbn__thefuck.md) | `maintainer_abandonment` | 0.89 |
| 41 | [jfeinstein10/SlidingMenu](reports/repositories/jfeinstein10__SlidingMenu.md) | `maintainer_abandonment` | 0.87 |
| 42 | [microsoft/Bringing-Old-Photos-Back-to-Life](reports/repositories/microsoft__Bringing-Old-Photos-Back-to-Life.md) | `maintainer_abandonment` | 0.87 |
| 43 | [eligrey/FileSaver.js](reports/repositories/eligrey__FileSaver.js.md) | `maintainer_abandonment` | 0.87 |
| 44 | [PanJiaChen/vue-element-admin](reports/repositories/PanJiaChen__vue-element-admin.md) | `maintainer_abandonment` | 0.87 |
| 45 | [CoderMJLee/MJExtension](reports/repositories/CoderMJLee__MJExtension.md) | `maintainer_abandonment` | 0.86 |
| 46 | [acdlite/react-fiber-architecture](reports/repositories/acdlite__react-fiber-architecture.md) | `maintainer_abandonment` | 0.86 |
| 47 | [bendc/frontend-guidelines](reports/repositories/bendc__frontend-guidelines.md) | `maintainer_abandonment` | 0.86 |
| 48 | [necolas/normalize.css](reports/repositories/necolas__normalize.css.md) | `maintainer_abandonment` | 0.85 |
| 49 | [CodeByZach/pace](reports/repositories/CodeByZach__pace.md) | `maintainer_abandonment` | 0.85 |
| 50 | [prakhar1989/awesome-courses](reports/repositories/prakhar1989__awesome-courses.md) | `maintainer_abandonment` | 0.85 |
| 51 | [pytube/pytube](reports/repositories/pytube__pytube.md) | `maintainer_abandonment` | 0.85 |
| 52 | [StartBootstrap/startbootstrap-sb-admin-2](reports/repositories/StartBootstrap__startbootstrap-sb-admin-2.md) | `maintainer_abandonment` | 0.84 |
| 53 | [ryanmcdermott/clean-code-javascript](reports/repositories/ryanmcdermott__clean-code-javascript.md) | `maintainer_abandonment` | 0.84 |
| 54 | [nostalgic-css/NES.css](reports/repositories/nostalgic-css__NES.css.md) | `maintainer_abandonment` | 0.83 |
| 55 | [tiimgreen/github-cheat-sheet](reports/repositories/tiimgreen__github-cheat-sheet.md) | `maintainer_abandonment` | 0.82 |
| 56 | [evilstreak/markdown-js](reports/repositories/evilstreak__markdown-js.md) | `maintainer_abandonment` | 0.82 |
| 57 | [tmux-plugins/tmux-resurrect](reports/repositories/tmux-plugins__tmux-resurrect.md) | `maintainer_abandonment` | 0.82 |
| 58 | [TypeStrong/ts-node](reports/repositories/TypeStrong__ts-node.md) | `maintainer_abandonment` | 0.82 |
| 59 | [seemoo-lab/openhaystack](reports/repositories/seemoo-lab__openhaystack.md) | `maintainer_abandonment` | 0.81 |
| 60 | [jlevy/the-art-of-command-line](reports/repositories/jlevy__the-art-of-command-line.md) | `maintainer_abandonment` | 0.81 |
| 61 | [animate-css/animate.css](reports/repositories/animate-css__animate.css.md) | `maintainer_abandonment` | 0.80 |
| 62 | [scutan90/DeepLearning-500-questions](reports/repositories/scutan90__DeepLearning-500-questions.md) | `maintainer_abandonment` | 0.80 |
| 63 | [Tencent/secguide](reports/repositories/Tencent__secguide.md) | `maintainer_abandonment` | 0.79 |
| 64 | [getumbrel/llama-gpt](reports/repositories/getumbrel__llama-gpt.md) | `maintainer_abandonment` | 0.78 |
| 65 | [visionmedia/page.js](reports/repositories/visionmedia__page.js.md) | `maintainer_abandonment` | 0.77 |
| 66 | [pingcap/talent-plan](reports/repositories/pingcap__talent-plan.md) | `maintainer_abandonment` | 0.77 |
| 67 | [alexanderepstein/Bash-Snippets](reports/repositories/alexanderepstein__Bash-Snippets.md) | `maintainer_abandonment` | 0.77 |
| 68 | [CompVis/stable-diffusion](reports/repositories/CompVis__stable-diffusion.md) | `maintainer_abandonment` | 0.76 |
| 69 | [rt2zz/redux-persist](reports/repositories/rt2zz__redux-persist.md) | `maintainer_abandonment` | 0.76 |
| 70 | [open-mmlab/mmsegmentation](reports/repositories/open-mmlab__mmsegmentation.md) | `maintainer_abandonment` | 0.75 |
| 71 | [travis-ci/travis-ci](reports/repositories/travis-ci__travis-ci.md) | `maintainer_abandonment` | 0.74 |
| 72 | [bnb/awesome-hyper](reports/repositories/bnb__awesome-hyper.md) | `maintainer_abandonment` | 0.74 |
| 73 | [resume/resume.github.com](reports/repositories/resume__resume.github.com.md) | `maintainer_abandonment` | 0.72 |
| 74 | [jamiebuilds/itsy-bitsy-data-structures](reports/repositories/jamiebuilds__itsy-bitsy-data-structures.md) | `maintainer_abandonment` | 0.72 |
| 75 | [react/create-react-app](reports/repositories/react__create-react-app.md) | `maintainer_abandonment` | 0.64 |
| 76 | [Rudrabha/Wav2Lip](reports/repositories/Rudrabha__Wav2Lip.md) | `dormant` | 0.52 |
| 77 | [ByteByteGoHq/system-design-101](reports/repositories/ByteByteGoHq__system-design-101.md) | `dormant` | 0.51 |
| 78 | [deepseek-ai/DeepSeek-R1](reports/repositories/deepseek-ai__DeepSeek-R1.md) | `dormant` | 0.45 |
| 79 | [anthropics/courses](reports/repositories/anthropics__courses.md) | `dormant` | 0.36 |

## ⚰️ Most common causes of death

- `maintainer_abandonment`: 61
- `bus_factor_collapse`: 14
- `dormant`: 4

**Total projects excavated: 79**


## 🤖 Automation

This README and every report are regenerated automatically by GitHub Actions. No human writes these conclusions; each one traces back to measurable repository signals.

