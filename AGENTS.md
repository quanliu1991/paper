# AGENTS.md — AI 论文知识库 Agent 工作规范

本仓库是每日更新的 AI 前沿论文知识库，重点沉淀**推理 Infra（inference/serving）**方向。Agent 每天 21:00 被定时唤醒，按 `.cursor/prompts/daily-paper.md` 执行每日任务。本文件定义产出格式与规则。

> **「推理」口径**：指 AI Infra 的模型推理与 serving——推理服务系统、KV cache、投机解码、量化压缩、并行调度、MoE 推理、长上下文/VLM serving、推理集群与编译。**不是**思维链/认知推理（那类归入 `topics/reasoning/` 普通主题）。

## 目录职责

| 路径 | 职责 |
|---|---|
| `scripts/fetch_papers.py` | 抓取 HF Daily Papers + arXiv 关键词，输出 `data/pending/YYYY-MM-DD.json` |
| `data/index.json` | 已收录论文索引（arXiv ID 主键，去重用） |
| `daily/YYYY/MM/YYYY-MM-DD.md` | 每日速览（推理 Infra 类单独成节排最前） |
| `topics/inference/papers.md` | ★ 重点专题：推理 Infra 归档（按子方向分节） |
| `topics/<topic>/papers.md` | 其他主题归档（models/training/reasoning/agents/applications） |
| `README.md` | 知识库说明 + 最近 7 天速览链接 |

## 每日速览模板（daily/YYYY/MM/DD.md）

```markdown
# AI 论文日报 · YYYY-MM-DD

> 收录 N 篇（精选 ⭐ M 篇 · 推理 Infra K 篇）· [HuggingFace Daily](https://huggingface.co/papers)

## 🚀 推理 Infra（K 篇）

### 1. ⭐ 论文标题（upvotes: NN）
- **一句话**：中文一句话总结
- **方法**：核心方法/思路
- **结果**：关键结果（吞吐/延迟/显存数字）
- **链接**：[arXiv](...) · infra 相关性: 5/5 · 子方向: kv-cache

（…每篇同格式…）

## 📚 其他方向（按主题分组：模型 / 训练 / 认知推理 / 智能体 / 应用）

### 模型架构
- **标题** — 一句话总结 [arXiv](...)

## 💎 今日 Top 深读
- [笔记标题](../topics/inference/notes/YYYY-MM-DD-xxx.md) — 一句话说明为何值得深读
```

规则：
- 推理 Infra 节内按「精选+infra 分」降序；其他节每篇一行速记（**标题 — 一句话总结**）。
- 全部中文速读，术语保留英文（如 KV cache、speculative decoding、PagedAttention）。
- upvotes 为 HF 社区热度，`⭐` = upvotes ≥ 10 或命中 infra 关键词。
- 思维链/认知推理类论文（CoT、test-time scaling 等）放「认知推理」普通节，不进推理 Infra 节。

## 主题归档模板（topics/<topic>/papers.md 追加条目）

推理 Infra 专题归档**infra 相关性 ≥4** 的论文到 `topics/inference/papers.md` 对应子方向小节；其他主题归档精选重点：

```markdown
### YYYY-MM-DD · 标题 ⭐
> [arXiv](...) · upvotes: NN · infra 相关性: 5/5 · 子方向: kv-cache

一句话总结。核心方法与关键结果（2-3 句，含关键数字）。
```

- 追加到对应主题文件的**对应小节**下。
- 条目按日期倒序插入（最新在最上）。

## 推理 Infra 子方向（topics/inference/papers.md 分节）

serving-system（serving 系统/引擎/集群）/ kv-cache（KV cache 与显存管理）/ speculative-decoding（投机解码与小模型加速）/ quantization-compression（量化/剪枝/蒸馏压缩）/ parallelism-scheduling（并行策略与请求调度）/ moe-inference（MoE 推理与 expert 并行）/ long-context-vlm（长上下文与 VLM serving）/ inference-other。

## data/index.json 格式

```json
{
  "papers": {
    "2610.08077": {
      "title": "...",
      "date_added": "YYYY-MM-DD",
      "source": "hf_daily",
      "upvotes": 42,
      "infra_hit": true,
      "arxiv_url": "..."
    }
  }
}
```

由 `python3 scripts/update_index.py` 从各日 pending JSON 自动重建，**禁止手动编辑**。fetch 脚本据此去重。

## infra 相关性评分标准（0-5）

| 分 | 标准 |
|---|---|
| 5 | 核心贡献就是推理系统/加速（serving 引擎、KV cache 优化、投机解码、量化方法、并行/调度、推理编译、推理集群） |
| 4 | 推理效率是主要组件之一（模型工作中的推理加速部分、VLM/长上下文 serving、MoE 推理部署） |
| 3 | 涉及但非核心（训练方法中讨论推理开销、agent 系统的 serving 层） |
| 2 | 弱相关（用到推理 benchmark、提及效率） |
| 1 | 基本无关 |
| 0 | 无关 |

## Git 规范

- 每日任务结束：`bash scripts/git_commit.sh "daily: YYYY-MM-DD（N 篇，推理 Infra K 篇）"` 然后 `bash scripts/git_push.sh`。
- **禁止**直接在命令行写 `git commit`（Cursor shell 集成会注入 --trailer，本机 git 2.24 不支持）；**禁止** force push。
- remote 走 SSH over 443（`ssh://git@ssh.github.com:443/...`），22 端口不可用。
- push 失败脚本会自动 pull --rebase 重试；仍失败则下次任务开始时先处理。
- **不要**提交 `data/pending/`（已在 .gitignore）。

## 归档写入安全（必须遵守）

- `topics/*/papers.md` 与 `data/index.json` 是**多日累积文件**：只能**插入/追加**新条目，**禁止全文件重写**。
- 编辑归档前必须先重新 Read 最新文件内容（不要用会话早期读到的旧缓存），插入位置按日期倒序。
- 新的一天条目插在对应子方向节内、同日期或更早日期条目之上。
- 若发现文件内容异常变短/丢失，停止写入并报告，不要继续覆盖。

## 异常处理

- HF/arXiv API 失败：脚本已内置 warn + 降级（空列表），照常产出（哪怕 0 篇也写当日速览说明情况）。
- 当日 0 篇新增（全部已收录）：写一行说明即可，不要重复归档。
- WebFetch 失败：笔记降级为仅基于摘要，标注「仅摘要分析」。
