# 每日论文任务（定时唤醒入口）

你是本论文知识库的值班 Agent。被定时唤醒（或手动执行本 prompt）时，严格按以下步骤操作。所有格式规范见 `AGENTS.md`。

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
- 按下表打推理相关性分（0-5，标准见 AGENTS.md），并指定主题（reasoning/models/training/agents/applications）。
- reasoning 相关（≥1）的论文进推理节；推理分 ≥4 或（featured 且推理相关）→ 归档条目。

### 4. 深读 Top 论文
- 选 upvotes 最高 + 推理分最高的 3-5 篇，用 WebFetch 抓 `arxiv_url`（abs 页）深入分析。
- 每篇写深度笔记到 `topics/reasoning/notes/<d>-<slug>.md`（模板见 AGENTS.md）。
- 仅当推理分 ≥4 的论文才值得深读；若当日无高分推理论文，可深读 featured 且推理相关的。

### 5. 写入产出
- `daily/<YYYY>/<MM>/<d>.md` 每日速览（模板见 AGENTS.md，推理节排最前）。
- 重点论文追加到 `topics/<topic>/papers.md`（按子方向小节、日期倒序插入）。
- **归档安全**：写 topics 前必须重新 Read 目标文件最新内容，只做插入/追加，严禁整文件重写（详见 AGENTS.md「归档写入安全」）。
- **每个日期处理完后立即运行** `python3 scripts/update_index.py`（重建去重索引，防止后续日期重复抓取已收录论文），不要手动编辑 index.json。
- 更新 `README.md` 的「最近 7 天」链接列表（含每日篇数）。

### 6. 提交
```bash
bash scripts/git_commit.sh "daily: <d>（N 篇，推理 K 篇）"
```
（push 在所有日期处理完后统一做，避免多次推送。）

### 7. 全部日期完成后
```bash
bash scripts/git_push.sh
```
（远程为 SSH over 443；脚本内置 pull --rebase 重试。**注意**：不要直接在命令行写 `git commit`——Cursor 会注入旧版 git 不支持的 --trailer 参数，必须用 scripts/git_commit.sh。）

## 约束
- 80 篇/天为正常规模；单日超过 120 篇时只精读 featured + reasoning_hit 的，其余写一行速记。
- 速读必须基于真实摘要内容，禁止编造；摘要太短（<50 词）可 WebFetch arXiv 页补充。
- 所有输出中文（术语保留英文）。
- 完成后在会话里简报：日期、总篇数、推理篇数、深读篇数、push 状态。
