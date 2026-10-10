# AI 论文知识库

每日自动更新的 AI 前沿论文知识库，重点沉淀**推理 Infra（inference/serving）**方向。由 Cursor Agent 每天 21:00 定时抓取分析（详见 [AGENTS.md](AGENTS.md)）。

> **「推理」口径**：AI Infra 的模型推理与 serving——推理服务系统、KV cache、投机解码、量化压缩、并行调度、MoE 推理、长上下文/VLM serving、推理集群。思维链等认知推理见 [topics/reasoning/](topics/reasoning/)（普通主题）。

## 数据源

- [HuggingFace Daily Papers](https://huggingface.co/papers)（社区策选，带 upvotes 热度）
- arXiv 关键词订阅（`config/keywords.yaml` 可调）

## 快速导航

| 目录 | 内容 |
|---|---|
| [daily/](daily/) | 每日速览（推理 Infra 类排最前；保留 90 天，旧文查 git 历史） |
| [digest/](digest/) | ★ 月度回顾：infra 精选 + 趋势 + 新术语（压缩层） |
| [topics/inference/](topics/inference/) | ★ 重点：推理 Infra 归档（serving / KV cache / 投机解码 / 量化 / 并行调度 / MoE / 长上下文 VLM） |
| [notes/papers/](notes/papers/) | 单篇精读笔记（含复现要点） |
| [notes/insights/](notes/insights/) | 主题式知识结晶（跨论文方法地图） |
| [reading-list.md](reading-list.md) | 待读队列（对话中让 Agent 添加，每日自动消化） |
| [glossary/terms.yaml](glossary/terms.yaml) | 个人术语词典（熟词裸奔、生词自动解释） |
| [glossary/profile.md](glossary/profile.md) | 个人知识画像（领域雷达 + 成长轨迹） |
| [profile/interests.yaml](profile/interests.yaml) | 方向权重配置（调整每日侧重与深读上限） |
| [topics/models/](topics/models/) | 模型架构 |
| [topics/training/](topics/training/) | 训练方法 |
| [topics/reasoning/](topics/reasoning/) | 认知推理（CoT、test-time scaling 等） |
| [topics/agents/](topics/agents/) | 智能体 |
| [topics/applications/](topics/applications/) | 应用与评测 |

## 个人使用方式

- 每天扫一眼当日 `daily/`（生词自动带解释）
- 想精读：对话说「精读 X」或「把 X 加入待读」（每日 21:00 自动消化队列）
- **精读追问**：IDE 里划选笔记文字直接问（零摩擦）；或说「标记疑问：<问题>」沉淀为笔记内 ❓ 问答对（每日任务自动回答未决 ❓）；笔记的「疑问清单」节可直接说「回答疑问清单第 N 条」
- 想看积累：`topics/inference/`（论文流水）+ `notes/insights/`（方法地图）+ `digest/`（月度回顾）
- 术语错了说「这词我熟」/「这个词不懂」；画像每月自动更新
- 查 90 天前的旧速览：`git log --all -- 'daily/**'` 或问 Agent

## 最近 7 天

<!-- AGENT:每日更新此列表，最新在最上 -->
- [2026-10-09 · 76 篇](daily/2026/10/2026-10-09.md)
- [2026-10-08 · 80 篇](daily/2026/10/2026-10-08.md)
- [2026-10-07 · 80 篇](daily/2026/10/2026-10-07.md)
- [2026-10-06 · 80 篇](daily/2026/10/2026-10-06.md)
- [2026-10-05 · 80 篇](daily/2026/10/2026-10-05.md)
- 2026-10-03/04 · 周末（HuggingFace Daily 无更新）

> 注：10-05 至 10-09 五天已按新口径完成 infra 重筛——[topics/inference/](topics/inference/) 收录 34 篇 infra 4 分+ 论文（量化压缩 10 · 长上下文/VLM 7 · KV cache 6 · Serving 3 · 投机解码 2 · MoE 1 · 其他 5）。五天的 daily 速览仍为旧口径（推理节=认知推理），自 10-10 起按新口径生成；认知推理归档保留在 [topics/reasoning/](topics/reasoning/)（89 条）。

## 使用

- 查某天动态 → `daily/YYYY/MM/`
- 查某个方向的积累 → `topics/<方向>/papers.md`
- 手动触发：在 Cursor 中执行 `.cursor/prompts/daily-paper.md`
