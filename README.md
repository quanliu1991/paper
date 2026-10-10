# AI 论文知识库

每日自动更新的 AI 前沿论文知识库，重点沉淀**推理 Infra（inference/serving）**方向。由 Cursor Agent 每天 21:00 定时抓取分析（详见 [AGENTS.md](AGENTS.md)）。

> **「推理」口径**：AI Infra 的模型推理与 serving——推理服务系统、KV cache、投机解码、量化压缩、并行调度、MoE 推理、长上下文/VLM serving、推理集群。思维链等认知推理见 [topics/reasoning/](topics/reasoning/)（普通主题）。

## 数据源

- [HuggingFace Daily Papers](https://huggingface.co/papers)（社区策选，带 upvotes 热度）
- arXiv 关键词订阅（`config/keywords.yaml` 可调）

## 快速导航

| 目录 | 内容 |
|---|---|
| [daily/](daily/) | 每日速览（推理 Infra 类排最前，精选 ⭐ 置顶） |
| [topics/inference/](topics/inference/) | ★ 重点：推理 Infra 专题（serving / KV cache / 投机解码 / 量化 / 并行调度 / MoE / 长上下文 VLM） |
| [topics/inference/notes/](topics/inference/notes/) | 重点论文深度笔记 |
| [topics/models/](topics/models/) | 模型架构 |
| [topics/training/](topics/training/) | 训练方法 |
| [topics/reasoning/](topics/reasoning/) | 认知推理（CoT、test-time scaling 等） |
| [topics/agents/](topics/agents/) | 智能体 |
| [topics/applications/](topics/applications/) | 应用与评测 |

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
