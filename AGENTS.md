# AGENTS.md — AI 论文知识库 Agent 工作规范

本仓库是每日更新的 AI 前沿论文知识库，重点沉淀**推理 Infra（inference/serving）**方向。Agent 每天 21:00 被定时唤醒，按 `.cursor/prompts/daily-paper.md` 执行每日任务。本文件定义产出格式与规则。

> **「推理」口径**：指 AI Infra 的模型推理与 serving——推理服务系统、KV cache、投机解码、量化压缩、并行调度、MoE 推理、长上下文/VLM serving、推理集群与编译。**不是**思维链/认知推理（那类归入 `topics/reasoning/` 普通主题）。

## 目录职责

| 路径 | 职责 |
|---|---|
| `scripts/fetch_papers.py` | 抓取 HF Daily Papers + arXiv 关键词，输出 `data/pending/YYYY-MM-DD.json` |
| `data/index.json` | 已收录论文索引（arXiv ID 主键，去重用） |
| `daily/YYYY/MM/YYYY-MM-DD.md` | 每日速览（推理 Infra 类单独成节排最前；保留 90 天后清理） |
| `topics/inference/papers.md` | ★ 重点专题：推理 Infra 归档（按子方向分节） |
| `topics/<topic>/papers.md` | 其他主题归档（models/training/reasoning/agents/applications） |
| `digest/YYYY-MM.md` | 月度压缩层：当月 infra 精选 + 趋势 + 新术语（一年后只看这层也够） |
| `reading-list.md` | 待读队列：用户加入，每日任务消化优先级最高的 1-2 篇 |
| `glossary/terms.yaml` | 个人术语词典（known/learning/unknown 分级） |
| `glossary/profile.md` | 个人知识画像（领域雷达 + 成长轨迹，月度更新） |
| `notes/papers/` | 单篇精读笔记（含复现要点） |
| `notes/insights/` | 主题式知识结晶（跨论文方法地图） |
| `profile/interests.yaml` | 兴趣配置：子方向权重、每日深读/队列消化上限 |
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
- [笔记标题](../notes/papers/YYYY-MM-DD-xxx.md) — 一句话说明为何值得深读

## 📖 今日新词
- **术语**（level）：一句话解释（learning/unknown 术语集中区；known 不列）
```

规则：
- 推理 Infra 节内按「精选+infra 分」降序；其他节每篇一行速记（**标题 — 一句话总结**）。
- 全部中文速读，术语保留英文（如 KV cache、speculative decoding、PagedAttention）。
- **术语渲染**：按 glossary/terms.yaml 的 level——known 裸奔；learning/unknown 当日首次出现带括号一句话解释；尾部「今日新词」节集中列出（详见 AGENTS.md「术语渲染规则」）。
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

## 术语渲染规则（glossary 驱动）

每日速览与笔记写作时，对领域术语按 `glossary/terms.yaml` 的 level 处理：

- **known**：直接使用，不解释（用户已熟悉）。
- **learning / unknown**：当日速览中**首次出现**时带一句话括号解释，如「PagedAttention（分页管理 KV cache 的显存技术）」；之后裸奔。
- 每日速览尾部加「📖 今日新词」小节：集中列出当日出现的 learning/unknown 术语及解释（从 terms.yaml 取）。
- 遇到未收录的领域核心术语（当日 ≥2 篇论文涉及）：自动追加到 terms.yaml（level: learning，附一句话解释与相关子方向）。
- **用户口头校正**（对话中）：「这词我熟」→ 改 known；「这个词不懂」→ 改 unknown 并当场解释。精读笔记中标注「新学到的术语」也同步入表。
- 术语等级调整后无需重写旧速览，只影响后续产出。

## 待读队列处理（reading-list.md）

- 每日任务（步骤 4.5）：读 `reading-list.md`，取状态 pending 中优先级最高（同优先级按日期先到先做）的 N 篇（N=`profile/interests.yaml` 的 `daily_queue_reads`，默认 2）执行精读流程（WebFetch arXiv abs/HTML → `notes/papers/YYYY-MM-DD-<slug>.md`，模板见 notes/papers/README.md）。
- 完成后：reading-list 该行状态改 done、笔记列填链接；当日速览「💎 今日深读」节引用该笔记。
- 用户在对话中说「把 X 加入待读」：查 arXiv ID/标题（可从 index.json 或当日数据找），追加行（状态 pending，优先级默认 2，用户指定则用之）。
- 对话中说「精读 X」：**立即**执行精读流程（不等每日任务），产出同上。
- **精读时必须缓存全文**：WebFetch 后把全文写入 `notes/papers/.fulltext/<arxiv-id>.txt`（git 忽略），后续追问直接读缓存。
- **追问处理**：用户对精读笔记追问时，读 `.fulltext/` 缓存（无则补抓）作答，答案引用论文具体章节；有价值的 Q&A 追加到笔记 `## Q&A` 节（详见 notes/papers/README.md「追问处理规范」）。

## 精读追问机制（notes/papers/ 配套）

三层体验，按摩擦从低到高：

### 层 1：IDE 划线即时问答（零沉淀）

用户在 IDE 中**选中笔记任意文字**直接在对话框提问（如「这段的 step desynchronization 到底怎么导致快模型空转？」）。Agent 直接回答，不改文件。适合临时解惑。

### 层 2：笔记内 ❓ 追问标记（持久沉淀）

用户对笔记内容不懂时，让 Agent 在笔记中标记追问点（说「这段我标记疑问：<问题>」或自己在笔记中加 `> ❓ **Q:** 问题`）。标记格式：

```markdown
> ❓ **Q:** 步失同步为什么不能靠同步锁解决？（2026-10-10）
```

Agent 回答后**原位展开为问答对**（保留原问题，永不删除用户的问题）：

```markdown
> ❓ **Q:** 步失同步为什么不能靠同步锁解决？（2026-10-10）
>
> **A:** 同步锁会让所有模型每步等最慢者，恰好放大了要解决的问题——快模型跟着慢模型的节奏空转。TokenRouter 的思路是根本不同步：每个模型自治 subserver 各跑各的批，请求像消息一样在模型间流转（route-send-receive），快模型不用等慢模型。（2026-10-10 答）
```

规则：
- 问答原位保留在笔记中（不是单独 FAQ 文件）——**笔记即学习轨迹**。
- 回答中用到的新术语同步 glossary/terms.yaml。
- 若回答较长（>10 行），正文展开放笔记末尾「## 深入问答」节，原位留锚点链接。

### 层 3：对话深挖（可升级为层 2）

用户在对话中连续追问。若某轮回答值得保留，Agent 主动建议：「这段解释要沉淀到笔记的 ❓ 区吗？」用户确认后按层 2 写回。

### Agent 行为规范

- 回答追问前**先 Read 笔记最新内容**（对齐上下文，防止答非所问）。
- 精读笔记生成时，主动在「启发与局限」后追加一节「## 疑问清单（Agent 主动提出）」：列 2-3 个值得深挖的开放问题（如「KV 状态跨模型不共享，长上下文切换的开销多大？」），供用户挑选追问。
- 追问答案涉及代码细节时，WebFetch 论文 HTML 版对应章节再回答，不凭空编造。
- 每日任务（步骤 4.6）：扫描 notes/papers/ 未回答的 ❓（有 Q 无 A），Agent 尝试回答（WebFetch 补料后），仍无法回答的标注「待论文开源/待实测」。

## 月度 digest 任务（每月 1 日的每日任务附加步骤）

- 触发：每日任务开始时检查当天是否为当月 1 日（或 digest/ 缺上月文件）。
- 流程：
  1. `python3 scripts/make_digest.py --month <上月YYYY-MM> --clean` 生成草稿（含当月 infra 归档全量 + 超期 daily 清理）。
  2. Agent 润色草稿为 `digest/<YYYY-MM>.md`：补「子方向趋势」（如「本月投机解码 5 篇，主流路线从 draft-model 转向 draft-tree」）与「新术语」节（当月 terms.yaml 新增项）。
  3. 更新 `glossary/profile.md`：按当月 terms level 变化 + 精读记录更新领域雷达与成长轨迹。
  4. insights 检查：某子方向归档累计 ≥5 篇且无对应 `notes/insights/<主题>.md` → 新建主题笔记骨架。
- `daily/` 保留 90 天；超期由脚本 `--clean` 删除（git 历史永久可查，README 已说明查法）。

## insights 主题笔记规范

- 命名：`notes/insights/<子方向或主题>-<视角>.md`（如 `kv-cache-landscape.md`、`spec-decoding-comparison.md`）。
- front-matter 必含 `来源论文: [arXiv IDs]` 与 `更新: 日期`，保证可溯源。
- 内容结构：问题定义 / 方法流派对比 / 演进脉络 / 个人观点 / 待验证问题。是**知识结晶**不是论文流水。
- 更新时机：月度 digest 任务；或用户对话中要求「总结一下 X 方向」。
