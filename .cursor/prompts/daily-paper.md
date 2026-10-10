# 每日论文任务（定时唤醒入口）

你是本论文知识库的值班 Agent。被定时唤醒（或手动执行本 prompt）时，严格按以下步骤操作。所有格式规范见 `AGENTS.md`。

> **「推理」口径**：AI Infra 的推理（inference/serving）——serving 系统、KV cache、投机解码、量化、并行调度、MoE 推理、长上下文/VLM serving。思维链/认知推理类论文归「认知推理」普通主题。

工作目录：仓库根目录（本文件所在处）。

## 步骤

### 1. 补齐缺失日期
- 看 `daily/` 下最新速览日期 `D_last`（没有则用 7 天前）。
- 对每个缺失日期 `d`（从 D_last+1 到今天，含今天）依次执行步骤 2-6。
- 判断「已处理」：`daily/<YYYY>/<MM>/<d>.md` 存在即视为该日已处理，跳过。

### 2. 抓取
```bash
python3 scripts/fetch_papers.py --date <d>
```

### 3. 分析（对 data/pending/<d>.json 中每篇论文）
- 读标题+摘要，生成中文速读：一句话总结 / 核心方法 / 关键结果。
- 按下表打 infra 相关性分（0-5，标准见 AGENTS.md），并指定主题（inference/models/training/reasoning/agents/applications）。
- infra 相关（≥1）的论文进「🚀 推理 Infra」节；infra 分 ≥4 → 归档到 `topics/inference/papers.md`。
- 思维链/认知推理论文（CoT、test-time scaling、RL 训推理）→ 「认知推理」普通节，重点者归档 `topics/reasoning/papers.md`。

### 4. 深读 Top 论文
- 选 upvotes 最高 + infra 分最高的 3-5 篇（上限 `profile/interests.yaml` 的 `daily_deep_reads`，子方向按权重倾斜），用 WebFetch 抓 `arxiv_url`（abs 页）深入分析。
- **关键图表**：curl 抓 `https://arxiv.org/html/<arxiv_id>` 提取 `<figure>` 块（图片 URL 相对路径需拼 `https://arxiv.org/html/<arxiv_id>v<N>/` 前缀）；位图下载到 `notes/papers/assets/<arxiv_id>-fig<N>-<slug>.png` 嵌入笔记；SVG/matplotlib 图给 arXiv HTML 锚点链接（`https://arxiv.org/html/<id>#<fig_id>`）；关键数据表转 markdown 表格。
- 每篇写深度笔记到 `notes/papers/<d>-<slug>.md`（模板见 notes/papers/README.md，必含「复现要点」节）。
- **抓取后把全文缓存到 `notes/papers/.fulltext/<arxiv-id>.txt`**（供用户后续追问，秒级读取）。
- 仅当 infra 分 ≥4 的论文才值得深读；若当日无高分 infra 论文，可深读 featured 且 infra 相关的。

### 4.5 消化待读队列（reading-list.md）
- 读 reading-list.md，取 pending 中优先级最高的 N 篇（N=interests.yaml 的 daily_queue_reads，默认 2），执行与步骤 4 相同的精读流程。
- 完成后该行改 done、填笔记链接；当日速览「💎 今日深读」引用。
- 若当日抓取数据里出现与队列某篇相同的 arXiv ID，一并处理（去重）。

### 4.6 回答笔记中的未决追问
- 扫描 notes/papers/*.md 中 `> ❓ **Q:**` 且尚无 **A:** 的条目。
- 按 AGENTS.md「精读追问机制」回答：可答的原位展开为问答对；涉及论文细节先 WebFetch 对应章节；无法回答的标注「待论文开源/待实测」。
- 新术语同步 glossary/terms.yaml。

### 5. 写入产出
- `daily/<YYYY>/<MM>/<d>.md` 每日速览（模板见 AGENTS.md，推理 Infra 节排最前，尾部「📖 今日新词」节按术语渲染规则生成）。
- 重点论文追加到 `topics/<topic>/papers.md`（按子方向小节、日期倒序插入）。
- **归档安全**：写 topics 前必须重新 Read 目标文件最新内容，只做插入/追加，严禁整文件重写（详见 AGENTS.md「归档写入安全」）。
- **每个日期处理完后立即运行** `python3 scripts/update_index.py`（重建去重索引，防止后续日期重复抓取已收录论文），不要手动编辑 index.json。
- 更新 `README.md` 的「最近 7 天」链接列表（含每日篇数）。
- **术语维护**：当日出现 ≥2 篇论文共用的未收录核心术语 → 追加 glossary/terms.yaml（level: learning）。

### 5.5 月度任务（仅当今天是当月 1 日，或 digest/ 缺上月文件）
- 按 AGENTS.md「月度 digest 任务」执行：make_digest.py 生成草稿并润色、更新 glossary/profile.md、检查 insights 主题笔记缺口。

### 6. 提交
```bash
bash scripts/git_commit.sh "daily: <d>（N 篇，推理 Infra K 篇）"
```
（push 在所有日期处理完后统一做，避免多次推送。）

### 7. 全部日期完成后
```bash
bash scripts/git_push.sh
```
（远程为 SSH over 443；脚本内置 pull --rebase 重试。**注意**：不要直接在命令行写 `git commit`——Cursor 会注入旧版 git 不支持的 --trailer 参数，必须用 scripts/git_commit.sh。）

## 约束
- **白话表达（最高优先级）**：所有产出以普通人能听懂的方式描述，术语首次出现配日常类比（如 KV cache=草稿纸、投机解码=实习生起草老板审批），数字要翻译（64x → 原 1 小时的活现在 1 分钟）；详见 AGENTS.md「表达总规范」。
- 80 篇/天为正常规模；单日超过 120 篇时只精读 featured + infra_hit 的，其余写一行速记。
- 速读必须基于真实摘要内容，禁止编造；摘要太短（<50 词）可 WebFetch arXiv 页补充。
- 所有输出中文（术语保留英文），**术语按 glossary/terms.yaml level 渲染**（详见 AGENTS.md「术语渲染规则」）。
- infra 关键词命中但内容明显无关（如医学 inference）→ 低分 1-2 并标注，不入重点节。
- 完成后在会话里简报：日期、总篇数、infra 篇数、深读篇数、队列消化篇数、push 状态。
