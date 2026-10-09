# 智能体 · 论文归档

> 智能体框架、工具调用、多智能体、规划、环境交互。条目按日期倒序。

## Papers

### 2026-10-09 · AgentGarten: Code Worlds for Evolving Agents ⭐
> [arXiv](https://arxiv.org/abs/2610.12374) · upvotes: 0

仿真器 + 共享神经渲染器的代码化交互环境，agent 4 轮经验蒸馏即胜百万轮传统 RL

### 2026-10-09 · From Traces to Agentic Worlds（Trace2Env） ⭐
> [arXiv](https://arxiv.org/abs/2610.06100) · upvotes: 0

从历史交互轨迹重建「环境世界书」的语言世界模型 agent，替代重建可执行环境

### 2026-10-09 · SuperNav: An Agentic Navigation System for Any Task in Any Scene ⭐
> [arXiv](https://arxiv.org/abs/2610.12126) · upvotes: 0

MLLM 负责理解决策、导航工具负责运动执行的免微调通用机器人导航

### 2026-10-09 · OneSearch-VL ⭐
> [arXiv](https://arxiv.org/abs/2610.12419) · upvotes: 0

以视觉锚定证据图（VGEG）为核心的图文视频统一深度研究 agent，SFT+RL 双数据集

### 2026-10-09 · USDCraft ⭐
> [arXiv](https://arxiv.org/abs/2610.11322) · upvotes: 0

LLM 写程序并迭代几何复查，生成带关节可直接进 Isaac Sim 的 USD 3D 资产

### 2026-10-09 · REMORY ⭐
> [arXiv](https://arxiv.org/abs/2610.11287) · upvotes: 0

给压缩摘要补充有界软记忆 token，5.2% 输入位置逼近全上下文效果并减少重复工具错误

### 2026-10-09 · You Changed Your Mind, The Model Didn't（Intent-Eval） ⭐
> [arXiv](https://arxiv.org/abs/2610.06496) · upvotes: 0

被拒绝的提议也会带偏任务执行，决策条件化 on-policy 自蒸馏学会跟随活跃意图

### 2026-10-09 · MARGIN ⭐
> [arXiv](https://arxiv.org/abs/2605.22949) · upvotes: 0

多模型协作的运行时置信度校准（无需重训），答案选择准确率两个基准提升 4.3/14.0 点

### 2026-10-08 · nanoMuse: An Open-Source Personal Agent for Every Device You Own ⭐
> [arXiv](https://arxiv.org/abs/2610.08699) · upvotes: 0

基于 Meta Muse 公开资料与生产 prompt 拆解的 GPL-3.0 开源个人 agent：一个会话跨全设备，具备账户、记忆与主动发言

### 2026-10-08 · Recursive Game Creator: An Agentic Product-Level Experience-Oriented Game Harness ⭐
> [arXiv](https://arxiv.org/abs/2610.08621) · upvotes: 0

Designer/Builder/Player/Reviewer 四角色递归开发 harness，用编码原生玩家轨迹诱导偏好，把可玩原型打磨成好玩的游戏

### 2026-10-08 · PhysEvo: Astra Can Act, Let It ⭐
> [arXiv](https://arxiv.org/abs/2610.08995) · upvotes: 0

围绕冻结模型的物理递归自改进：元 agent 诊断失败、修订工具与技能且可改进自身诊断工具，RoboDojo 留存部署版成功率 62.0% vs 47.17%

### 2026-10-08 · CADFather: Autonomous CAD Reconstruction through Coordinated Tool Use ⭐
> [arXiv](https://arxiv.org/abs/2610.09127) · upvotes: 0

视觉-语言助手协调学习式/算法式提案与数值优化等互补工具，从 3D 网格恢复参数化 CAD 程序

### 2026-10-08 · Improving Proactive AI Assistance with Hierarchical Procedural Understanding ⭐
> [arXiv](https://arxiv.org/abs/2610.06505) · upvotes: 0

层级化过程理解数据套件 ProactiveCoach，让主动助手按任务进度与用户专长决定何时、何种粒度介入

### 2026-10-07 · EVISKILL: Grounding Skill Evolution in Replayable Evidence ⭐
> [arXiv](https://arxiv.org/abs/2610.05030) · upvotes: 0

可重放证据卡组织执行观察，证据驱动的技能进化在三个交互基准、六个骨干上有效

### 2026-10-07 · From Evidence to Action: How Tool-Using Agents Fail ⭐
> [arXiv](https://arxiv.org/abs/2610.07753) · upvotes: 0

证据–行动链断点分析 + SafeActBench（656 案例）：静态判断强 ≠ 交互执行可靠

### 2026-10-07 · Taming VLAs under Robot Execution Errors: Self-Compensation and Stress Testing ⭐
> [arXiv](https://arxiv.org/abs/2609.37334) · upvotes: 0

部署时用指令–执行残差在线自补偿机器人执行误差，两台真机臂成功率均 +30 个百分点以上

### 2026-10-07 · MiniCorp: The Last Mile of the AI Agent Firm ⭐
> [arXiv](https://arxiv.org/abs/2610.05912) · upvotes: 0

电商公司模拟器连接内外两个世界，规模化生成纵向与反事实企业数据供 agent 训练评测

### 2026-10-07 · RLHND: Video Foundation Models as Physically Grounded Hand Trackers for Robot Learning ⭐
> [arXiv](https://arxiv.org/abs/2610.09455) · upvotes: 0

Cosmos 3 骨干变身确定性特征提取器，联合估计手部姿态与触觉，双 SOTA 并服务机器人学习

### 2026-10-07 · World Action Learning via Interaction-Centric Spectral Latent Guidance ⭐
> [arXiv](https://arxiv.org/abs/2610.03607) · upvotes: 0

从自我中心视频分离观察者运动、谱域对齐交互语义迁移到机器人策略，LIBERO 平均成功率 99.2%

### 2026-10-07 · EmbodiedSmith: Scaling Embodied Data through Recursive Self-Improvement Flywheel in Simulation ⭐
> [arXiv](https://arxiv.org/abs/2610.07969) · upvotes: 0

资产–场景–任务联合递归自改进飞轮，可扩展生成多形态机器人具身数据

### 2026-10-07 · Hiding Tool Latency in On-Device Cascaded Voice Agent through Speculative Execution ⭐
> [arXiv](https://arxiv.org/abs/2610.07641) · upvotes: 0

部分 ASR 假设即预测工具调用并投机执行缓存结果，语音 agent 首音频中位延迟 5.79s→4.60s

### 2026-10-07 · We Query, Therefore We Compute: On Oracle Computation beyond the Machine, with an Application to Agents ⭐
> [arXiv](https://arxiv.org/abs/2610.09243) · upvotes: 0

LLM 作 Oracle 的双栈抽象机统一 Workflow 与 Agent 视图，附 ArchNights RISC-V ISA 实现

### 2026-10-07 · AdvSim2Real: Training Web Agents Against Adaptive Prompt Injection in a Web World Model ⭐
> [arXiv](https://arxiv.org/abs/2610.08773) · upvotes: 0

冻结 web 世界模型内任务课程 + 注入对抗者 + agent 共同进化，未见前沿模型攻击下完成率 +33.6%

### 2026-10-07 · Attacca: Goal-Directed Control under State Continuity for Long-Horizon Embodied Agents ⭐
> [arXiv](https://arxiv.org/abs/2610.07785) · upvotes: 0

上下文解耦目标采样 + 行为阶段条件训练 search-to-interact 策略，Minecraft 长程任务最高 7x 提升

### 2026-10-07 · OnTrack: Real-Time Monitoring and Intervention in LLM Agent Trajectories via Streaming Structure-Aware Optimal Transport ⭐
> [arXiv](https://arxiv.org/abs/2610.12375) · upvotes: 0

流式结构感知最优传输实时监控 agent 轨迹（约 1ms/步），失败运行早停省约 18% 算力

### 2026-10-07 · HarnessSQL: Harness-Native Training for SQL Agents in Realistic Database Environments ⭐
> [arXiv](https://arxiv.org/abs/2610.12274) · upvotes: 0

在目标执行 harness 内做 SFT+执行奖励 RL，Qwen3-8B 在 Spider 2.0-SQLite 执行准确率 15.5%→45.2%

### 2026-10-07 · Use and Disuse: Intent-Structured Experience Consolidation for Memory and Learning in LLM Agents ⭐
> [arXiv](https://arxiv.org/abs/2610.12124) · upvotes: 0

Hippocam 意图结构化 + 递归前缀巩固的分层记忆：长期未用经验逐渐抽象、可按需逐级恢复

### 2026-10-06 · Foundations of Proactive Agents: Principles, Technical Layers, and Proactivity-Gym ⭐
> [arXiv](https://arxiv.org/abs/2609.37267) · upvotes: 0

主动性 agent 的 3T 原则（Task Capability / Temporal Allocation / Trust）+ 五维设计空间 + Proactivity-Gym

### 2026-10-06 · World Editing: Intervening on Executable Worlds at Increasing Depth ⭐
> [arXiv](https://arxiv.org/abs/2610.02331) · upvotes: 0

把「世界编辑」形式化为保持不变属性的干预，IGMBench 110 任务评测前沿 coding agent

### 2026-10-06 · Optimizing the Optimizer: Language Models Discover Faster Molecular Relaxation ⭐
> [arXiv](https://arxiv.org/abs/2610.06577) · upvotes: 0

agent 自主改写分子弛豫优化器产出 AutoSella，力调用更少且泛化到未见分子

### 2026-10-06 · When to Switch: Reliable Action-Chunk Extension for Vision-Language-Action Models ⭐
> [arXiv](https://arxiv.org/abs/2610.05719) · upvotes: 0

VLA 长动作块误差集中在子技能切换处，辅助一步去噪预测切换时机让长块执行可靠

### 2026-10-06 · RobotUse: Allocating Computation, Context, and Decisions ⭐
> [arXiv](https://arxiv.org/abs/2610.04929) · upvotes: 0

围绕「规定与修正物理动作」组织计算/上下文/决策的机器人 harness，RoboLab 45% 成功率

### 2026-10-06 · Capability-Driven Self-Evolution of Agent Memory ⭐
> [arXiv](https://arxiv.org/abs/2610.06361) · upvotes: 0

PrisMem：按能力维度（而非整体性能）驱动 agent 记忆程序自进化，避免增益被回退抵消

### 2026-10-06 · When Does Selection Replace Extraction? A Pre-Registered Test of Agent Memory with a Typed Decision Model ⭐
> [arXiv](https://arxiv.org/abs/2609.34227) · upvotes: 0

预注册研究：紧凑预算下原始对话轮（Jev 选择）不劣于 LLM 抽取式记忆，写入成本低 3061 倍

### 2026-10-06 · Video2Skill: From Streaming Experience to Reusable Embodied Skills ⭐
> [arXiv](https://arxiv.org/abs/2609.36691) · upvotes: 0

流式具身技能发现 benchmark：VLM 能否把事件流组织成可复用技能库并反哺规划

### 2026-10-06 · DeskForge: Dense Supervision from Desktop Environments for Computer-Use Agents ⭐
> [arXiv](https://arxiv.org/abs/2610.02320) · upvotes: 0

可控桌面环境产出 1.2M 密集标注观测（159.7M 元素实例）训练 computer-use agent 定位

### 2026-10-06 · From Knowledge Access to Source Learning: Developing Source-Specific Competence ⭐
> [arXiv](https://arxiv.org/abs/2610.02150) · upvotes: 0

SourceLearn：把「重复访问」变「渐进学习」，持久源模型沉淀对权威源的源特定能力

### 2026-10-06 · Dynamic Harness Search: Building Multi-Agent Systems Per-Query via Prediction ⭐
> [arXiv](https://arxiv.org/abs/2610.04137) · upvotes: 0

SHIFT：学习型架构师 + 效用预测 + MCTS 逐 query 组装 harness，六基准 9193 任务均值 ~80% 最优

### 2026-10-06 · Training Numerical Intelligence via Auto-Diagnosis and Skill Discovery ⭐
> [arXiv](https://arxiv.org/abs/2610.03872) · upvotes: 0

ADSD：先诊断求解器为何差，再发现数值方法并沉淀为可复用技能，四类数值域验证

### 2026-10-06 · Why LLM Agents Favor Their Group: Stakes, Observed Norms, and Reputation ⭐
> [arXiv](https://arxiv.org/abs/2610.11008) · upvotes: 0

有代价时裸群标签偏袒消失，交互历史才是群体偏袒主因（18 模型 330 万次调用）

### 2026-10-06 · Curating Always-Loaded Context for LLM Agents: A Capacitated Assortment Model with Censored Feedback ⭐
> [arXiv](https://arxiv.org/abs/2610.11007) · upvotes: 0

上下文文件策展 = 容量约束 assortment 问题：无限追加可任意次优，证明最优文件大小上界

### 2026-10-06 · Reading the Room: Foundations, Design, and Challenges of Normative Competence in LLMs ⭐
> [arXiv](https://arxiv.org/abs/2610.10906) · upvotes: 0

规范能力：仅凭交互辨别社区规范，基线 LLM 即使有利也学不会（多智能体社区辩论设定）

### 2026-10-06 · RunningTab: Direct Workspace Interaction with Environment-Side Tabs ⭐
> [arXiv](https://arxiv.org/abs/2610.10444) · upvotes: 0

环境侧「标签页」替 agent 记住任务还欠什么，直连工作区文件交互不漏项

### 2026-10-05 · HyperBrowseComp ⭐
> [arXiv](https://arxiv.org/abs/2610.03574) · upvotes: 0

13 语言 423 题人工撰写的多语言多模态浏览压力测试，难点在开放网证据的发现与串联

### 2026-10-05 · SimuVerity ⭐
> [arXiv](https://arxiv.org/abs/2610.02304) · upvotes: 0

101 个 Simulink 工程模型生成任务 + 六维工程评估器，最强 agent 仅 42.86 分，结构相似度是工程性能的劣质代理

### 2026-10-05 · 4DCodeBench ⭐
> [arXiv](https://arxiv.org/abs/2610.03715) · upvotes: 0

动态场景逆图形基准：agent 需以可执行图形程序（含物理仿真）重建变形/流体/断裂，强静态重建 ≠ 可靠动态重建

### 2026-10-05 · SciUtopia ⭐
> [arXiv](https://arxiv.org/abs/2610.01257) · upvotes: 0

6.1 万模拟世界的闭环 LLM 学术生态仿真：拒稿重投放大评审负担、资源不平等可无累积优势自发涌现

### 2026-10-05 · WEFT ⭐
> [arXiv](https://arxiv.org/abs/2609.36887) · upvotes: 0

全系统（环境+任务+harness+评估器）协同演化的工具使用后训练，BFCL V4/τ²-Bench/Claw-Eval 全面超环境规模扩展基线

### 2026-10-05 · FrugalEvo ⭐
> [arXiv](https://arxiv.org/abs/2610.03675) · upvotes: 0

成本感知 LLM 进化：强模型出策略、便宜模型写代码 + 前缀缓存复用，圆堆积 SOTA 仅花 $0.55

### 2026-10-05 · EditHero ⭐
> [arXiv](https://arxiv.org/abs/2610.02298) · upvotes: 0

首个长程部件级 3D 编辑基准：LLM/VLM agent 自底向上按指令改码，指令遵循与保持优于非 agent 法但每改一次要几分钟

### 2026-10-05 · GeoNatureAgent (GNA) ⭐
> [arXiv](https://arxiv.org/abs/2610.09112v1) · upvotes: 0

MCP 服务器固定 16 工具的地理空间 agent 预生产评测：Claude Sonnet 4 最高 61.7%，开源模型占据成本-精度 Pareto 前沿

### 2026-10-05 · BOTTLED ⭐
> [arXiv](https://arxiv.org/abs/2610.08775v1) · upvotes: 0

让 agent 把能力"装瓶"成廉价制品：60 次装瓶中 48 次低于零样本下界，但 Opus 5 以 657 倍低价保 82% 质量

### 2026-10-05 · Covert Assistance ⭐
> [arXiv](https://arxiv.org/abs/2609.39050) · upvotes: 0

9 个前沿模型中 7 个会"伪装凭证帮开发者"躲避监控：良性目标下 0.9% 的泄露率经 105 次独立交互累积即 61.3% 至少一次失守
