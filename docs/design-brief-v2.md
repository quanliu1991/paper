# 推理 Infra 研究雷达 · 设计 brief v2

> 来源：2026-10-16 对话。用户以「四问加深法」（出自 [How to be more ambitious](../notes/papers/2026-10-16-ambitious-with-models.md) 的 Depth prompt）要求重写知识库整体设计：更深入，而不是更大。
> 状态：设计定稿，未实施。本文档是新版设计的单一事实源；README/AGENTS/scripts 均未改动，落地项见文末。

---

# 题目：推理 Infra 研究雷达 —— 一台判断可被现实检验的知识系统

## 使命（先于一切功能）

本系统存在的目的：让维护者在任意时刻能对推理 infra 领域回答三类问题——
决策类（「我的场景该用什么」）、地图类（「某子方向有哪些路线、什么在取代什么」）、
前沿类（「什么在升温、什么在退潮」）。所有环节的设计只服务于这三类问题的回答质量，
不能改变行为的产出一律删除。

## 信息源（原始层，一手优先）

- 每日：arXiv 全文（含附录）+ HF Daily（保留现状）
- 每周：系统会议 proceedings 直采（OSDI/SOSP/MLSys/ASPLOS/EuroSys/ATC + ISCA/MICRO）；
  vLLM/SGLang/TensorRT-LLM 的 CHANGELOG 与 RFC issue（工业采纳先于论文）
- 每篇深读：全文 + 证明/附录 + OpenReview 审稿（如有）+ GitHub 活跃度与复现 issue
  + 前向引用 T0 快照（存档，供 90 天后回测）
- 原始抓取快照不可变存储（data/raw/）；markdown 一律从数据生成，
  禁止从 markdown 反解析数据（make_digest 改为从 index/归档数据源生成）

## 作业标准（每个环节配一个可运行的检验）

1. 收录 = 关键词通道 ∪ 嵌入通道（SPECTER2 类向量 + 子方向锚点论文集，存 duckdb），
   双通道各自记命中来源
2. 召回审计（月度）：维护 gold set（当月领域公认重要论文：顶会 best paper/高引/被引擎合入），
   算 recall@pipeline；每篇漏报归因到环节（关键词缺口/源头缺口/评分缺口）并修正
3. 评分一致性：infra 分打分隔周重评 κ ≥ 0.7；Agent 打分三采样多数票
4. 预测台账：每条 ⭐ 精选落账一条可检验预言（90 天内被引 ≥N / 被主流引擎合入 /
   复现成功），到期自动回测，digest 附 Brier 校准报告
5. Claim-evidence 分账：精读笔记每个关键数字标注证据等级——
   [论文自述] / [第三方 benchmark] / [自测复现]；没有独立证据的数字不许进 insights 笔记
6. 学习产出：glossary 术语升级为 FSRS 调度，每周检索练习测验；
   测验正确率（而非阅读量）是学习环节的唯一 KPI
7. 推荐：全部曝光落盘，双周 precision@k；偏好分加不确定性探索项防回环；
   曝光分布月报随 digest 出

## 外部验证（除维护者与 Agent 之外的裁判）

1. 领域未来：前向引用、被主流推理引擎实际合入
2. 第三方测量：MLPerf Inference、自机 microbenchmark（scripts/repro 标准负载）
3. 历史回测：gold-set recall 趋势、精选台账校准曲线
4. 学习测验：术语与跨论文关系的隔期检索正确率
5. 社区：insights 笔记按季度外发，同行反馈归档

## 边界（防「更大」）

- 不新增目录、不新增每日产出物；新要求一律替换现有环节而非叠加
- 每日 Agent 时间预算不变；新增周/月任务占用 digest 时段
- 每个采集的指标必须挂在某个决策上，否则不采集

---

## 四问摘要（重写的依据）

1. **顶尖专家会做而原设计没要求的**：先写验收标准再写功能；审漏不只审收（gold-set recall 回测）；跳出二手策展找一手源头；claim 与 evidence 分开记账；精选当预测记账并到期回测；测学习产出而非阅读量（检索练习）；防推荐回环；检查评分器自身一致性。
2. **最原始素材**：arXiv 全文与 LaTeX 源码、系统会议 proceedings、引擎 CHANGELOG/RFC、OpenReview 审稿、作者 talk 幻灯、MLPerf 原始数据、OpenAlex 引用图、自机 profiler trace。
3. **方法与工具**：PRISMA 式纳入标准 + κ 一致性检验、雪球法（OpenAlex/Semantic Scholar API）、SPECTER2 嵌入检索、Kleinberg burst / BERTopic 升温检测、FSRS 间隔重复、曝光日志 + precision@k、Brier 校准、标准化 microbenchmark。
4. **独立裁判**：领域未来（引用/引擎合入）、第三方测量（MLPerf/自测）、历史回测（recall/校准曲线）、学习测验正确率、社区同行。

## 未落地项（等用户逐项决定）

| 落地项 | 涉及 | 优先级建议 |
|---|---|---|
| gold-set 召回审计 | `scripts/recall_audit.py` + `data/gold-set/` | 高——先知道漏了多少 |
| 精选预测台账 | `data/claims-ledger.yaml`，digest 时回测 | 高——星标从意见变预测 |
| glossary 迁移 FSRS | `glossary/terms.yaml` 加调度字段 + 周测验 | 中 |
| 嵌入通道收录 | SPECTER2 + duckdb，并入 fetch 管线 | 中 |
| 会议与引擎直采 | 周任务：proceedings + CHANGELOG/RFC | 中 |
| claim 证据等级标注 | 精读笔记模板加字段 | 低——随下一篇笔记自然引入 |
