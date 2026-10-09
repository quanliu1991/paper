# AGENTS.md — AI 论文知识库 Agent 工作规范

本仓库是每日更新的 AI 前沿论文知识库，重点沉淀**推理（Reasoning）**方向。Agent 每天 21:00 被定时唤醒，按 `.cursor/prompts/daily-paper.md` 执行每日任务。本文件定义产出格式与规则。

## 目录职责

| 路径 | 职责 |
|---|---|
| `scripts/fetch_papers.py` | 抓取 HF Daily Papers + arXiv 关键词，输出 `data/pending/YYYY-MM-DD.json` |
| `data/index.json` | 已收录论文索引（arXiv ID 主键，去重用） |
| `daily/YYYY/MM/YYYY-MM-DD.md` | 每日速览（推理类单独成节排最前） |
| `topics/<topic>/papers.md` | 长期主题归档（重点论文） |
| `topics/reasoning/notes/` | Top 推理论文深度笔记 |
| `README.md` | 知识库说明 + 最近 7 天速览链接 |

## 每日速览模板（daily/YYYY/MM/DD.md）

```markdown
# AI 论文日报 · YYYY-MM-DD

> 收录 N 篇（精选 ⭐ M 篇 · 推理相关 K 篇）· [HuggingFace Daily](https://huggingface.co/papers)

## 🧠 推理 Reasoning（K 篇）

### 1. ⭐ 论文标题（upvotes: NN）
- **一句话**：中文一句话总结
- **方法**：核心方法/思路
- **结果**：关键结果或贡献
- **链接**：[arXiv](...) · 推理相关性: 5/5

（…每篇同格式…）

## 📚 其他方向（按主题分组：模型 / 训练 / 智能体 / 应用）

### 模型架构
- **标题** — 一句话总结 [arXiv](...)

## 💎 今日 Top 深读
- [笔记标题](../topics/reasoning/notes/YYYY-MM-DD-xxx.md) — 一句话说明为何值得深读
```

规则：
- 推理节内按「精选+推理分」降序；其他节每篇一行速记（**标题 — 一句话总结**）。
- 全部中文速读，术语保留英文（如 test-time scaling、RLHF）。
- upvotes 为 HF 社区热度，`⭐` = upvotes ≥ 10 或命中推理关键词。

## 主题归档模板（topics/<topic>/papers.md 追加条目）

仅归档**重点论文**（推理相关性 ≥ 4，或精选且推理相关）：

```markdown
### YYYY-MM-DD · 标题 ⭐
> [arXiv](...) · upvotes: NN · 推理相关性: 5/5 · 子方向: test-time-scaling

一句话总结。核心方法与关键结果（2-3 句）。
```

- 追加到对应主题文件的**对应子方向小节**下（reasoning 按子方向分节，见文件内标题）。
- 条目按日期倒序插入（最新在最上）。

## 深度笔记模板（topics/reasoning/notes/YYYY-MM-DD-slug.md）

```markdown
# 标题

> [arXiv](...) · YYYY-MM-DD · upvotes: NN · 子方向: xx

## 背景与动机
## 方法
## 实验/结果
## 启发（对我们工作的借鉴）
## 局限
```

基于 WebFetch 抓取 arXiv abs 页（摘要+元信息），必要时抓 HTML 全文。每日最多 3-5 篇（upvotes 最高 + 推理分最高的优先）。

## data/index.json 格式

```json
{
  "papers": {
    "2610.08077": {
      "title": "...",
      "date_added": "YYYY-MM-DD",
      "topics": ["reasoning"],
      "reasoning_score": 5,
      "upvotes": 42
    }
  }
}
```

每分析完一篇即写入（arXiv ID 主键）。fetch 脚本据此去重。

## 推理相关性评分标准（0-5）

| 分 | 标准 |
|---|---|
| 5 | 核心主题就是推理能力提升/评测（test-time scaling、RL 训推理、CoT 方法、验证器等） |
| 4 | 推理是主要组件之一（agent 里的推理规划、训练中的推理数据合成等） |
| 3 | 涉及但非核心（应用中用到推理模型的某个环节） |
| 2 | 弱相关（评测、安全等间接相关） |
| 1 | 基本无关 |
| 0 | 无关 |

## Git 规范

- 每日任务结束：`bash scripts/git_commit.sh "daily: YYYY-MM-DD（N 篇，推理 K 篇）"` 然后 `bash scripts/git_push.sh`。
- **禁止**直接在命令行写 `git commit`（Cursor shell 集成会注入 --trailer，本机 git 2.24 不支持）；**禁止** force push。
- remote 走 SSH over 443（`ssh://git@ssh.github.com:443/...`），22 端口不可用。
- push 失败脚本会自动 pull --rebase 重试；仍失败则下次任务开始时先处理。
- **不要**提交 `data/pending/`（已在 .gitignore）。

## 归档写入安全（必须遵守）

- `topics/*/papers.md` 与 `data/index.json` 是**多日累积文件**：只能**插入/追加**新条目，**禁止全文件重写**。
- 编辑归档前必须先重新 Read 最新文件内容（不要用会话早期读到的旧缓存），插入位置按日期倒序。
- 新的一天条目插在对应子方向节内、同日期或更早日期条目之上。
- 若发现文件内容异常变短/丢失，停止写入并报告，不要继续覆盖。

## 主题与子方向定义

主题：`reasoning`（推理）、`models`（模型架构）、`training`（训练方法）、`agents`（智能体）、`applications`（应用与评测）——详见 `config/keywords.yaml`。

推理子方向：test-time-scaling / rl-for-reasoning / chain-of-thought / verification-reward / efficient-reasoning / reasoning-other。

## 异常处理

- HF/arXiv API 失败：脚本已内置 warn + 降级（空列表），照常产出（哪怕 0 篇也写当日速览说明情况）。
- 当日 0 篇新增（全部已收录）：写一行说明即可，不要重复归档。
- WebFetch 失败：笔记降级为仅基于摘要，标注「仅摘要分析」。
