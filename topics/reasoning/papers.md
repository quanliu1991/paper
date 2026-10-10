# 认知推理 · 论文归档

> 思维链、test-time scaling、RL 训推理、验证与奖励等**认知推理**方向（非重点专题——本库「推理」指 AI Infra 的 inference/serving，见 `topics/inference/`）。条目按日期倒序，收录认知推理相关性 ≥4 或精选论文。子方向定义见 `config/keywords.yaml`。

## Test-time Scaling

### 2026-10-09 · InfiLoop: Scaling to Tens of Thousands of Test-Time Iterations with Loop-Native Attention Residuals ⭐
> [arXiv](https://arxiv.org/abs/2610.11570) · upvotes: 2 · 推理相关性: 5/5 · 子方向: test-time-scaling

给 looped Transformer 配原生残差连接，使 test-time 迭代可扩至数万步而不退化：内容加权 + 可学习时间衰减维持递归状态的流动汇总，流式递归使聚合记忆恒定。7M 参数模型 Sudoku-Extreme 达 97.9%、ARC-AGI-2 pass@2 13.6%，超 20000 有效步仍在提升。

### 2026-10-09 · SanSi: A Looped Typed Decision Model for System 1.5 Thinking ⭐
> [arXiv](https://arxiv.org/abs/2610.07730) · upvotes: 7 · 推理相关性: 5/5 · 子方向: test-time-scaling

不生成 token、靠循环迭代隐藏状态再读出的「System 1.5」类型化决策模型：每个 loop 后按 proper scoring rule 训练选项概率，单模型覆盖 1-8 loop 全预算。59 来源 10027 道决策达 72.0%（比同构非循环高 13.5 点），loop 可外推未见深度；作无金标 RL judge 把生成器 F1 提高 7.7 点。

### 2026-10-08 · From Pareto to Preference: Personalized Test-Time Scaling via Amortized Agentic Policy Discovery ⭐
> [arXiv](https://arxiv.org/abs/2610.09684) · upvotes: 16 · 推理相关性: 5/5 · 子方向: test-time-scaling

把个性化 test-time scaling 形式化为发现最大化用户多维需求（精度/延迟/成本联合）满足率的可执行控制器。PersonTTS 用需求匹配的控制器初始化 + 源蒸馏的程序性指导摊销式复用跨用户搜索经验；AIME 与 HMMT 上联合需求满足率大幅超强 TTS 基线，经验复用进一步提升策略质量并显著降低发现时间与成本。

### 2026-10-08 · Inherit-MAS: Test-Time Evolution of Multi-Agent Systems through Workflow and Execution Inheritance ⭐
> [arXiv](https://arxiv.org/abs/2610.02396) · upvotes: 5 · 推理相关性: 4/5 · 子方向: test-time-scaling

测试时进化多智能体系统时在 workflow 与执行两层显式继承：workflow 继承自最近完整候选并剪除无用节点，执行继承仅在请求与上下文完全匹配时复用存储结果，避免大改扰动有效组件与重复计算。GPT-4o-mini 工人下 WorkBench 55.4%、HotpotQA FullWiki 49.7% joint F1，超 EvoAgent/EvoMAS/TacoMAS，执行继承省 worker token 29.1%/34.6%。

### 2026-10-06 · Self-Generated Feedback Destabilizes Test-Time Training: A Causal Decomposition of Long-Horizon Adaptation ⭐
> [arXiv](https://arxiv.org/abs/2610.05076) · upvotes: 25 · 推理相关性: 4/5 · 子方向: test-time-scaling

因果分解证明 test-time training 从自己生成的文本学习会自我 destabilize：128K token 流上三组匹配对照（Fixed Generation / Recorded Replay / 配对单步比较）定位损伤来自「读劣化文本」与「在劣化文本上更新」的复合。冻结生成模型即可消除 125M/760M 模型上 98%+ 的损伤——问题出在自举反馈而非更新机制本身。

### 2026-10-06 · ASCENT: Online Test-Time Training of Long-Horizon Agents via Self-Distillation of Verified Experience ⭐
> [arXiv](https://arxiv.org/abs/2610.05303) · upvotes: 23 · 推理相关性: 4/5 · 子方向: test-time-scaling

部署期在线 test-time training（OaTTT 设定，单遍执行任务流）：agent 用「带验证结果的自身轨迹」自蒸馏更新权重。直接模仿/强化单次尝试的 token 会 destabilize 策略，ASCENT 改用验证过的经验做自蒸馏使权重更新跨任务持久，长程 agent 任务流上持续在线提升，优于反思/记忆/技能文本等 in-context 适配。

### 2026-10-05 · From Uncertainty to Action: Learning to Steer LLM Agents ⭐
> [arXiv](https://arxiv.org/abs/2610.09115v1) · upvotes: 0 · 推理相关性: 4/5 · 子方向: test-time-scaling

不确定性能识别失败轨迹却定位不了该干预的步：对 1,864 条轨迹每个非终步用四种机制分别干预并跑完，构建 stepwise outcome table，VoS 监视器据此离线/在线学出各步「干预价值」，harm-budgeted 触发器限制对成功轨迹的扰动比例。12/12 设置平均 +7.8pp 胜无干预执行，11/12 胜最强不确定性触发基线（平均 +2.9pp）。

## RL for Reasoning

### 2026-10-09 · MiMo-V2.6: Scaling Reinforcement Learning Towards Self-Improvement ⭐
> [arXiv](https://arxiv.org/abs/2610.11959) · upvotes: 46 · 推理相关性: 4/5 · 子方向: rl-for-reasoning

全模态模型沿三轴 scaling RL 算力：大批量异步训练（上下文 1M、每步 2.7-3.7B token）、更多样环境（code/general/visual/cyber + agent harness）、groupwise agentic grading 提供更准奖励。冻结 MoE router + 多层 reward hacking 防御，开源训练动态、RL 环境与框架。

### 2026-10-09 · ReSPO: Reshaped Sequence Policy Optimization for Gradient Starvation in Off-Policy Learning ⭐
> [arXiv](https://arxiv.org/abs/2609.35433) · upvotes: 7 · 推理相关性: 5/5 · 子方向: rl-for-reasoning

发现 RLVR rollout 复用中 clipping 的符号相关梯度饥饿：压制低重要性尾部欠生成的正样本、放任高权重尾部过生成的负样本主导。ReSPO 用 α-divergence 变分目标导出的平滑双分支序列级核替代 clipping，在 dense/MoE Qwen3 上加速早期优化、提升最终训练分与 held-out 基准表现。

### 2026-10-09 · GPD: Distilling Routed 3D Privilege for Spatial Reasoning in Vision-Language Models ⭐
> [arXiv](https://arxiv.org/abs/2610.12355) · upvotes: 1 · 推理相关性: 5/5 · 子方向: rl-for-reasoning

把深度/语义/BEV 几何线索按问题路由给教师作特权信息，privileged KL 只作用于错误轨迹并增强 GRPO，蒸馏出纯 RGB 部署的空间推理 VLM。4B backbone 上 VSI-Bench 57.1、四基准均值 37.6，超 GRPO 与答案特权 OPSD。

### 2026-10-09 · SpatialOPSD: Self-Distilling Spatial Intelligence from Verified Coding Agent Traces ⭐
> [arXiv](https://arxiv.org/abs/2610.11366) · upvotes: 6 · 推理相关性: 5/5 · 子方向: rl-for-reasoning

把空间 coding agent 的验证执行轨迹当特权信息做 on-policy 自蒸馏，让 MLLM 免工具内化空间 CoT；Repetition-Aware Distillation（重复掩码 + unlikelihood 正则）防特权信息泄漏。平均准确率超 SFT 与 GRPO，空间与 OOD 数据集均更优。

### 2026-10-09 · ZCPO: When KL Regularization Misfires in Group Policy Optimization ⭐
> [arXiv](https://arxiv.org/abs/2610.12161v1) · upvotes: 0 · 推理相关性: 5/5 · 子方向: rl-for-reasoning

拆解群体策略优化中 KL 正则的七种失效模式（clipping 后残余更新、KL 随长度增长与贡献失衡、集中于少数 token 等）；ZCPO 用条件 KL 测相对漂移校准组内奖励系数并并入代理目标，数学推理实验与消融验证有效。

### 2026-10-09 · Alpha-Stabler: Unveiling the Geometry of RLVR in LLMs via Trainable Vectors ⭐
> [arXiv](https://arxiv.org/abs/2609.34344) · upvotes: 0 · 推理相关性: 5/5 · 子方向: rl-for-reasoning

用向量转向发现 RLVR 增益存在于激活空间的低维有效流形，有效控制方向位于主子空间的低方差补集；Alpha-Stabler 用 Predictor 监控主子空间侵入预警塌缩、Controller 反传中剥离主子空间梯度分量。5 LLM × 6 可验证奖励任务验证，稳定训练 2000 步并一致提升 RL 增益。

### 2026-10-08 · Self-Retrospection Distillation: Turning Post-hoc Experiences into Prior Foresight ⭐
> [arXiv](https://arxiv.org/abs/2610.08077) · upvotes: 115 · 推理相关性: 5/5 · 子方向: rl-for-reasoning

把事后轨迹经验（hindsight）蒸馏为交互前的预见（foresight），补足 RLVR 在 reward 无区分度时消失的学习信号。SRD 用已完成轨迹揭示的「本可预知的信息与应避开的陷阱」监督同一策略的 trajectory-blind foresight，foresight 仅作训练目标、推理时无需显式生成。10 个工具增强推理/长程 agentic 任务上较 RLVR 与自蒸馏基线最高 +24.2pp；2B 规模下 98% rollout 组全失败（RLVR 训至 0%），加 SRD 达 60.6%。

### 2026-10-08 · Questioning the Questions: Sustaining Self-Evolution in Reasoning Models ⭐
> [arXiv](https://arxiv.org/abs/2610.04299) · upvotes: 68 · 推理相关性: 5/5 · 子方向: rl-for-reasoning

诊断自进化推理模型退化的两大病灶——无效问题占比随轮次上升、数学等价问题被词面查重漏掉导致多样性坍缩。R-Quest 训练 solver 识别并拒绝无效问题，其判断引导 questioner 奖励与训练数据过滤；冻结基座模型比较采样问题对提供 novelty 反馈。12 个数学/通用推理/代码基准上持续最优，十轮自进化稳定增益并在最后一轮达峰，超 R-Zero 17.32 分。

### 2026-10-08 · Semifactual Credit-Augmented Policy Optimization ⭐
> [arXiv](https://arxiv.org/abs/2609.40360) · upvotes: 37 · 推理相关性: 5/5 · 子方向: rl-for-reasoning

发现 RLVR 训出的推理模型对任务无关 prompt 特征高度敏感，提出 GRPO 因果变体 SCAPO：semifactual 干预（保持题目与答案不变）下测量固定回复的 token 概率漂移，归一化稳定性分数在训练早期压低不稳定 token 的 advantage。Qwen3-4B/1.7B-Base 上 AIME 2024-26 较 GRPO +5.63/+4.17pp，两个规模下多数数学基准与全部 OOD 基准最佳。

### 2026-10-08 · Gains and Collapse in On-Policy Distillation: A Reinforcement Learning Perspective ⭐
> [arXiv](https://arxiv.org/abs/2610.03185) · upvotes: 29 · 推理相关性: 4/5 · 子方向: rl-for-reasoning

从 RL 视角解释 on-policy distillation 为何既带来增益又坍缩成超长重复生成：教师是隐式奖励模型，偏好与质量对齐时让正确回答更易采样但不扩展能力边界，偏好失配时放大超长重复 rollout（reward hacking）。训练中 masking 不健康响应与 SFT 初始化均有效缓解坍缩——OPD 的关键在教师评估学生 rollout 的可靠性而非其生成能力。

### 2026-10-08 · On-Policy Distillation with Negative-Policy Rollouts ⭐
> [arXiv](https://arxiv.org/abs/2610.07874) · upvotes: 17 · 推理相关性: 4/5 · 子方向: rl-for-reasoning

师生分布重叠不足时正向蒸馏信号不够：NP-OPD 在 rollout 阶段引入低能力「负策略」，其 rollout 持续供应「负策略偏好于教师」的 token，使其全程暴露在教师监督下。不改蒸馏奖励公式、保留正向教师监督，跨模型规模、生成模式、推理域与 OPD 变体全面改进，有效抑制负策略偏好的 token 并把学生推离负策略。

### 2026-10-07 · Rethinking Cross-Tokenizer On-Policy Distillation: From Alignment Coverage to Supervision Reliability ⭐
> [arXiv](https://arxiv.org/abs/2610.08448) · upvotes: 177 · 推理相关性: 4/5 · 子方向: rl-for-reasoning

跨 tokenizer 的 on-policy 蒸馏中，扩大词表对齐覆盖不如提升监督可靠性：分析发现严格 1:1 对齐组已覆盖大多数 student token，将 reverse KL 限制在共享词表的 student top-16 子集上计算，紧凑监督反而更有效。三组异构师生对（数学推理+代码生成）上精度与全词表 OPD 相当、优于跨 tokenizer 基线；额外加 span log-prob MSE 监督实现全覆盖反而掉点。

### 2026-10-07 · DiffGate: Difficulty-Gated Teacher Guidance for On-Policy Distillation ⭐
> [arXiv](https://arxiv.org/abs/2610.04596) · upvotes: 16 · 推理相关性: 4/5 · 子方向: rl-for-reasoning

GRPO 与难度门控教师指导结合：outcome-gated 目标把教师监督仅施加于失败轨迹、按组难度缩放、平滑有界以防极端师生偏差，verifier 决定哪些轨迹接受 OPD 监督，互补 OPD 的稠密 token 级信号与组相对奖励的结果级信号。Qwen3-0.6B/1.7B 代码 avg@8 较匹配 GRPO +1.7/+1.8 点，四个模型-域设置 pass@8 全部提升。

### 2026-10-07 · Rationale-Guided Policy Optimization: Learning to Reason with Adaptive Rationale Scaffolding ⭐
> [arXiv](https://arxiv.org/abs/2610.07342) · upvotes: 13 · 推理相关性: 5/5 · 子方向: rl-for-reasoning

把 ground-truth rationale 当作临时脚手架的自适应策略优化，缓解 RL 推理训练的 reward sparsity：RGPO 按模型当前能力自适应利用 rationale 辅助生成更优回答，仅将高奖励的模型自生成解迁移回无引导设定，不要求 off-policy 数据与 RL 任务同格式。语言与视觉语言推理设定下均稳定超越 RLVR 基线，消融证实自适应引导是增益关键。

### 2026-10-07 · OPD Before RL: Warm-Starting Rubric-Based RL with On-Policy Distillation ⭐
> [arXiv](https://arxiv.org/abs/2610.02781) · upvotes: 10 · 推理相关性: 4/5 · 子方向: rl-for-reasoning

rubric 先作特权教师上下文做 on-policy 蒸馏、再作 RL reward 的两阶段训练：RP-OPD 阶段无 rubric 学生匹配 rubric-aware 教师的 next-token 分布获得稠密 token 级监督，第二阶段 RL 直接优化 rubric reward 突破蒸馏平台期。HealthBench/ResearchQA/RubricHub Science 上得分最高；SFT+RL 基线出现 reward hacking 而本方法几乎未见。

### 2026-10-07 · Harness-Aware Distillation for Small Language Model Agents ⭐
> [arXiv](https://arxiv.org/abs/2610.02858) · upvotes: 10 · 推理相关性: 4/5 · 子方向: rl-for-reasoning

harness 感知蒸馏——只蒸馏教师超出 harness 的增量能力：用动作偏好对比教师有无 harness 信息时的行为，配有效性校验丢弃矛盾偏好对，与 on-policy 蒸馏互补且无需任务奖励或成功标签。多个长程 agent benchmark 上超越 on-policy 蒸馏基线，更少陷入无效循环、更多从错误恢复。

### 2026-10-06 · LoGRA: Scaling LLM Reinforcement Learning with Low-Rank Gradient Sketches ⭐
> [arXiv](https://arxiv.org/abs/2610.06647) · upvotes: 120 · 推理相关性: 4/5 · 子方向: rl-for-reasoning

用低秩梯度草图大幅降低 LLM RL 后训练显存：草图保留有效学习信号，同一压缩表示同时支持模型更新与策略同步，配合 predicted-KL 步长控制在应用每次更新前预估策略漂移并自适应调整步幅。推理任务上平均训练显存最多降 45.7% 且性能不损，单八卡节点稳定训练 27B 模型 1100+ 步（dense Adam 直接 OOM）。

### 2026-10-06 · Decoupling Exploration from Optimization in RLVR ⭐
> [arXiv](https://arxiv.org/abs/2610.10536) · upvotes: 0 · 推理相关性: 5/5 · 子方向: rl-for-reasoning

把「探索新推理策略」与「优化策略」解耦：ExpDis 训练带 novelty bonus 的 explorer 策略，按正确性与质量过滤其轨迹后蒸馏给不带 novelty bonus 的 student，循环迭代。能发现先验之外的新推理策略，且不出现直接加 novelty bonus 时的质量退化。

### 2026-10-06 · VICO: Visual Environments Co-Evolving for Vision-Language Model Reasoning ⭐
> [arXiv](https://arxiv.org/abs/2610.10782) · upvotes: 0 · 推理相关性: 4/5 · 子方向: rl-for-reasoning

RLVR 后训练不应只进化 actor，还要让视觉环境共同进化——否则任务难度漂出学习前沿、信号坍缩。EnvRewriter 与 actor 联合训练：编辑可验证的图像侧结构（场景图、图表、保护区域掩码）并重渲染，产出标签有效、难度按 pass-rate 奖励校准到 actor 当前能力的样本，训练信号持续再生、VLM 推理性能持续提升。

### 2026-10-06 · A Good Self-Teacher Meets the Student Where They Are: Joint On-Policy Learning and Teaching ⭐
> [arXiv](https://arxiv.org/abs/2610.10447) · upvotes: 0 · 推理相关性: 4/5 · 子方向: rl-for-reasoning

特权信息加持的「自我教师」可能走学生学不了的捷径，监督反而失配——好教师要贴着学生当前水平教。分析 privileged-conditioning 自蒸馏的失配问题后提出联合 on-policy 学习与教学机制，保证蒸馏更新确实改进学生；在成功轨迹稀少、代价高昂的困难长程任务上稳定优于朴素 OPD/自蒸馏。

### 2026-10-06 · Stochastic Teacher Intervention for Agentic On-Policy Distillation ⭐
> [arXiv](https://arxiv.org/abs/2610.10878) · upvotes: 0 · 推理相关性: 4/5 · 子方向: rl-for-reasoning

多轮 agent 任务中学生早期错误会把轨迹带离教师分布、令 token 级监督失效。STI-OPD 按 teacher-student policy discrepancy 随机触发教师干预，用教师动作替换学生动作使后续观测回到教师 rollout 分布附近、最大化监督获取；多轮 agentic OPD 的稳定性与最终性能显著提升。

### 2026-10-05 · Does Learning Protein Folding Generalize to Broader Reasoning? ⭐
> [arXiv](https://arxiv.org/abs/2609.38879) · upvotes: 120 · 推理相关性: 5/5 · 子方向: rl-for-reasoning

蛋白质折叠这类非语言、结构密集的科学数据可作为后训练监督源，系统性提升 LLM 通用推理能力。构建 FoldingCorpus 蛋白质 QA 数据集与 Fold2Reason 训练配方，通过「语言头预测离散结构答案 + 共享表征解码连续 3D 几何」两种互补信号做后训练；FoldBench 结构预测得分为 Qwen3.5-9B 的 2.7-3.5 倍，空间/图/科学/通用 10 项推理基准全部正收益（宏平均 45.09%→48.33%）。

### 2026-10-05 · Scaling Trajectories for Complex Tasks through Recursive Self-Rewrite ⭐
> [arXiv](https://arxiv.org/abs/2610.02826) · upvotes: 103 · 推理相关性: 4/5 · 子方向: rl-for-reasoning

把多样 harness 辅助获得的成功轨迹递归重写为通用 harness 下的可复用训练轨迹：planner 把流程提取为 runbook、critic 筛查 verifier/答案泄漏并引导递归修订、executor 在全新沙箱执行，用 Qwen-3.8-27B 自举 11,094 条重写轨迹做 SFT。Terminal-Bench 2 pass@3 57.0%→74.2%、TB4 1.5%→9.1%、自建 TB-Hard 39.0%→63.0%，长程 process reward 0.21→0.29。

### 2026-10-05 · Pivot-SD: Efficient Self-Distillation for Masked Diffusion Language Models ⭐
> [arXiv](https://arxiv.org/abs/2610.03665) · upvotes: 62 · 推理相关性: 5/5 · 子方向: rl-for-reasoning

只监督去噪过程中「高影响力的关键提交（pivot）」即可高效后训练扩散语言模型：用信息增益（对剩余 mask 位置的不确定度削减）挑选 pivot，成功轨迹的 pivot 用交叉熵、失败轨迹用 targeted unlikelihood，其余 token 不动。LLaDA-8B-Instruct 在数学/代码基准上超越全序列 SFT 与等算力 diffusion RL 基线，200 道题就能涨点。

### 2026-10-05 · Language Models that Play Chess and Explain Their Moves ⭐
> [arXiv](https://arxiv.org/abs/2610.03695) · upvotes: 37 · 推理相关性: 5/5 · 子方向: rl-for-reasoning

4B 参数 chess-language 模型 Queen 同时达到大师级棋力与流畅解释：encoder-decoder 架构（静默专家棋类 encoder + 指令微调 LM）经 cross-attention 连接，用自然语言版 Bellman update 迭代蒸馏——分析候选走子后局面并蒸馏回模型。7 轮迭代 Elo 1782→2697，解释流畅度接近 GPT-5.6-Sol(high)，700 Elo 优势碾压所有前沿模型。

### 2026-10-05 · CM-DPO: Constraint-Margin Direct Preference Optimization for LLM Planning ⭐
> [arXiv](https://arxiv.org/abs/2610.09219v1) · upvotes: 0 · 推理相关性: 5/5 · 子方向: rl-for-reasoning

用符号 verifier 导出的连续约束违反幅度替代 DPO 二元偏好信号（$1 与 $1000 的预算超支不再等权），字典序目标分离硬/软约束；SynPlan-R 用程序化约束画像（DCCG）+ 推理教师最小编辑蒸馏（RT-MED）造无偏偏好对。8B 模型 TravelPlanner/NaturalPlan 89.2% pass、93.4% solve，13 倍低延迟，OOD PlanBench 超 GPT-4o 9.2pp。

### 2026-10-05 · GraphOPD: Graph-Augmented On-Policy Distillation for LLM Agents ⭐
> [arXiv](https://arxiv.org/abs/2610.08959v1) · upvotes: 0 · 推理相关性: 4/5 · 子方向: rl-for-reasoning

修正「最高分歧步蒸馏在多轮 agent 上失效」的问题：从环境自身状态变化读出「哪步使能了哪步」构建步骤依赖图，以随机游走平稳分布打分，与 teacher-student 分歧信号融合为轨迹相对 mask，聚焦每条 rollout 最值得监督的步骤。ALFWorld/WebShop/SearchQA 上超最强基线至多 +5.8pp，executed-replay 审计显示结构 credit 分数远高于随机地追踪真实因果影响。

### 2026-10-05 · On KL-Regularized Policy Optimization ⭐
> [arXiv](https://arxiv.org/abs/2610.08963v1) · upvotes: 0 · 推理相关性: 4/5 · 子方向: rl-for-reasoning

把 KL 正则锚在采样器上的策略优化框架 KLPO：正则化改进步有闭式 Gibbs 解，在采样器自身轨迹上最小二乘拟合 log-ratio 最优性条件，采样器概率经 log-ratio 进入、无需重要性权重，单 rollout 免 critic。统一 SPPO/GPO/REBEL/BPO 为特例，蒙特卡洛 KL 估计保持梯度无偏，并导出 top-K/二元近似的精确 KL gap。

## Chain-of-Thought

### 2026-10-09 · Cited but Not Consulted: A Counterfactual Audit of Legal Chain-of-Thought Faithfulness ⭐
> [arXiv](https://arxiv.org/abs/2610.12361v1) · upvotes: 0 · 推理相关性: 5/5 · 子方向: chain-of-thought

反事实审计法律 CoT 忠实性：固定案情替换模型所指法律权威，7 个开源模型上指名正确率 66.7-100%，但换权威后判决改变比例远不一致（CaseHOLD 仅 0-21.7%）；对抗指令合规率（73.3-96.4%）远超判决敏感度——引用是依赖关系的劣质代理，生成解释不可直接当审计凭据。

### 2026-10-07 · Making LLMs Say What They Think: Measuring and Improving CoT-Interpretability Alignment ⭐
> [arXiv](https://arxiv.org/abs/2609.38972) · upvotes: 16 · 推理相关性: 5/5 · 子方向: chain-of-thought

提出 CIA 指标量化 CoT 叙述与模型内部计算的忠实一致度：用可解释性工具检测内部推理策略、与 CoT 文本比对，再以任务精度 + 参数化忠实性信号为 reward 做后训练。三个 LLM、三任务上 CIA 仅 44.8-75.9%；后训练后 CoT 参数化忠实性大幅提升且任务精度不降。

### 2026-10-06 · What Matters for Latent Reasoning with Flow Matching ⭐
> [arXiv](https://arxiv.org/abs/2610.06666) · upvotes: 13 · 推理相关性: 5/5 · 子方向: chain-of-thought

给「潜在推理」（连续空间思考）立下五条标准——有用、多样、可解释、可随算力精化、高效：批判现有方法的捷径学习、显式 CoT 蒸馏进权重、逐 token 模仿等缺陷，系统研究学习到的潜空间中 flow matching 的关键训练选择。Flow-based 潜在推理在精度-效率权衡上优于显式 CoT 的替代方案。

### 2026-10-06 · Invariant-Measure Reasoners: Stable Representations for Latent Reasoning ⭐
> [arXiv](https://arxiv.org/abs/2610.10996) · upvotes: 0 · 推理相关性: 5/5 · 子方向: chain-of-thought

循环式潜在推理的潜状态在递归更新下只收敛到状态空间紧集而非不动点，用「不变测度」替代单点状态做预测可让推理跨深度稳定：ImR 以预测头输出在不变测度下的期望为预测，且可仅微调预测头实现，不同递归深度下预测稳定性显著提升。

### 2026-10-06 · Reasoning-Token Spikes Under Prompted Untruthful Responding in Large Language Models ⭐
> [arXiv](https://arxiv.org/abs/2610.10405) · upvotes: 0 · 推理相关性: 4/5 · 子方向: chain-of-thought

被诱导说谎时推理模型会「多想」：基于认知负荷理论，3 个推理模型 × 210 道多选题（分析/描述/规范推理 × 道德/非道德域）实验发现说谎伴随明显的 reasoning token 数量激增。可作不依赖 trace 内容的低带宽欺骗检测信号，为 CoT 可能不可读/不忠实的未来提供侧信道监控方案。

### 2026-10-05 · The Dichotomy Between Pattern Recognition and Step-by-Step Reasoning ⭐
> [arXiv](https://arxiv.org/abs/2610.09186v1) · upvotes: 0 · 推理相关性: 5/5 · 子方向: chain-of-thought

模式识别与逐步推理是同一光谱的两端：若下一 token 只依赖最近 c 个 token，推理轨迹即 De Bruijn 图上 DAG 子图的路径，学「边」远比学「轨迹」样本高效（transformer 所需样本量与边数呈幂律）。状态频繁（小 c）准确率高但对扰动脆弱，中等状态密度平衡准确率与鲁棒性；Qwen3-14B/32B 在 GSM8K 等基准用 <15% 长度的滑窗注意力仍保留 >75% 准确率。

### 2026-10-05 · EgoLAP: Learning from Egocentric Human Data through Language-Action Reasoning ⭐
> [arXiv](https://arxiv.org/abs/2610.08726v1) · upvotes: 0 · 推理相关性: 4/5 · 子方向: chain-of-thought

用语言化动作链思考（language-action CoT）桥接具身差，第一人称人类数据可直接预训练 VLA 机器人策略：把运动意图表达为结构化、时间抽象的语言动作，配扎根于场景几何/物理/可供性的 motion-level reasoning，人类与机器人轨迹共享同一动作 CoT 空间。真实世界任务进度均值 80.1%，为替代动作表示的 2.3 倍；motion-level reasoning 优于 subtask/object-box/visual-trace 复合格式。

### 2026-10-05 · Algorithmic Scratchpads and Curriculum Staging for Arithmetic Reasoning in Tiny Transformers ⭐
> [arXiv](https://arxiv.org/abs/2610.09003v1) · upvotes: 0 · 推理相关性: 5/5 · 子方向: chain-of-thought

在 10.6M 参数的 Tiny Transformer 上，「数位逐级」的 scratchpad 形制 + 四阶段课程让单位数除法从 4.0% 升到 86.7%：定位序列 packing（梯度饥饿致 40%→1% 崩塌）、语言预训练必要（否则 ≤2%）、RoPE/RMSNorm/SwiGLU/MoE 架构原语三大基础。Digit-by-Digit Long Division scratchpad 后 held-out 4000 题准确率 86.7%；FOIL 乘法 scratchpad 因强制单步九项连加而失败，未见 4 位操作数归零、无缓冲训练灾难性遗忘。

## Verification & Reward

### 2026-10-06 · ProgressCompass: Embodied Progress Reward Models Are Lost Without the Right Context ⭐
> [arXiv](https://arxiv.org/abs/2609.36684) · upvotes: 20 · 推理相关性: 4/5 · 子方向: verification-reward

长程具身任务中，进度奖励模型（PRM）离开正确上下文就会「迷路」：ContextProgress-Bench（24 个操作任务/120 episodes）覆盖 State Recall / Context Fusion / Full Autonomy 三档设定，考察 PRM 作为 dense reward、verifier、monitor 的表现。现有 PRM 在进度信息需要历史上下文时显著失效，为长任务验证器设计指明方向。

### 2026-10-05 · LexReward: A Taxonomy-Driven Reward Framework for Legal Language Models ⭐
> [arXiv](https://arxiv.org/abs/2609.39071) · upvotes: 64 · 推理相关性: 4/5 · 子方向: verification-reward

按 Style/Element/Chain 三维度分类法为法律 LLM 构建可解释的细粒度 reward 体系：为每个维度制定 rubric（法律推理链评估 order/completeness/correctness/non-redundancy），构造偏好数据做 DPO 与 reward model 训练，再用维度 reward model 做 RL。rubric reward 可靠区分法律回答质量，各维度 DPO/RL 全面提升，且 reward 时无需参考答案。

### 2026-10-05 · VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks ⭐
> [arXiv](https://arxiv.org/abs/2610.00972) · upvotes: 58 · 推理相关性: 5/5 · 子方向: verification-reward

把生成器 LLM 变成带工作区、证据工具与可复用验证技能的 agentic verifier，规模化长程任务验证。基于「分歧常暴露正确答案、共识可能掩盖错误」的发现，用 disagreement resolver 对竞争性声明做环境证据核查、consensus challenger 主动测试共同声明并搜寻遗漏需求；5 个长程基准 × 2 个前沿模型上选择得分最高，证据回溯修订带来 +6.2/+6.4pp 增益，开源约 2.6 万条 rollouts。

### 2026-10-05 · MetaRubric: Learning to Reward for Rubric-Based Reinforcement Learning ⭐
> [arXiv](https://arxiv.org/abs/2610.02824) · upvotes: 33 · 推理相关性: 5/5 · 子方向: verification-reward

用反事实 prompt 对消除 rubric judge 的「Vacuous Credit」（信息缺失仍给高分、可反转 GRPO 优势符号）：MetaRubric 交替「证据感知策略优化」与「响应引导的 rubric 自适应」，仅当响应含满足准则的充分证据才给 credit，并按阶段边界调整准则权重。多骨干上 PubMedQA 较静态 judge GRPO 提升 6.00-20.40pp，HealthBench-Hard 与两个多模态医疗基准再涨。

### 2026-10-05 · Verify Less, Evolve More: Training Idea-Level Critics for Verification-Efficient ML Evolving Agents ⭐
> [arXiv](https://arxiv.org/abs/2610.08993v1) · upvotes: 0 · 推理相关性: 5/5 · 子方向: verification-reward

训练「点子级 critic」预测 ML 改动是否有效，帮自进化 agent 把昂贵实证验证集中到最有希望的候选上：SFT（Gemini-3.1-Pro 合成高质量 critique）+ GRPO 提升 critic 预测精度，critic 兼任推理时筛选器与策略训练的 learned reward model。静态点子评估超 Gemini-3.1-Pro，同验证预算下最终解更优，作为 reward model 为不确定案例保留实证验证、同资源下策略更新量大增。

### 2026-10-05 · VeriFine: Scaling Verification for Self-Improvement in Embodied Reasoning ⭐
> [arXiv](https://arxiv.org/abs/2610.08761v1) · upvotes: 0 · 推理相关性: 5/5 · 子方向: verification-reward

策略-课程-裁判协同进化让具身推理的自提升不再被固定 judge 卡死：Policy Improvement Loop 用 rubric judge 诊断复发失败、构建自适应课程；验证瓶颈时 Judge Improvement Loop 选择性查询人类并对 judge 做 coactive calibration。驾驶与机器人导航任务上，RL/SFT 两路都实现策略与裁判能力的持续自提升。

### 2026-10-05 · Where Does Retrieval-Based Open-Ended Evaluation Fail? ⭐
> [arXiv](https://arxiv.org/abs/2609.30467) · upvotes: 22 · 推理相关性: 4/5 · 子方向: verification-reward

检索式开放题事实性评测的失败可分解为检索端五维质量错误与验证端六步推理错误：以 MedExpert 开放题为案例构建双重分类法，LLM-as-Judge 流水线规模化标注证据质量与 verifier 推理错误，跨 4 种检索法 × 6 个前沿 verifier 压力测试。扩大模型规模、增加 reasoning effort、扩展权威网络源、医疗微调均无法解决这些失败模式——是 retrieve-then-verify 范式在开放医疗场景的根本局限。

## Efficient Reasoning

### 2026-10-05 · Efficient Reasoning Training Does Not Always Harm CoT Faithfulness and Monitorability ⭐
> [arXiv](https://arxiv.org/abs/2610.03509) · upvotes: 17 · 推理相关性: 5/5 · 子方向: efficient-reasoning

高效推理训练对 CoT 忠实性与可监控性的影响不同：用固定预算/逐样本长度目标/组相对长度奖励三种长度压力方式微调多模型，评估 CoT faithfulness（相关输入上的决策一致性）与 monitorability（干预是否在 CoT 中体现）。忠实性多数场景下降（主要源于一致性变差），但可监控性出奇稳健——即使 CoT 大幅变短，模型仍持续承认干预对答案的影响。

### 2026-10-05 · TAP: Efficient Long-Horizon Agent Pruning via Trajectory-Anchored Recovery ⭐
> [arXiv](https://arxiv.org/abs/2610.09074v1) · upvotes: 0 · 推理相关性: 4/5 · 子方向: efficient-reasoning

结构剪枝 + 轨迹锚定恢复首次成功压缩 RL 训练的 long-horizon agent：TAP 交互锚定教师轨迹、学生自生成每个 reasoning-action 响应，冻结教师监督学生响应前缀，用恢复目标梯度在恢复中学生上重打通道分、迭代选择连接 evolving policy。剪掉 60% FFN 通道后 ALFWorld/WebShop 分别保留 99.2%/88.0% 成功率，单成功任务 GPU 时间降约 22%/17%。

## Others

### 2026-10-09 · Learn2Play Bench: How Well Do LLM Agents Learn from Experience in Unfamiliar Environments? ⭐
> [arXiv](https://arxiv.org/abs/2610.08215) · upvotes: 108 · 推理相关性: 4/5 · 子方向: reasoning-other

用规则全新/反直觉的文字游戏区分「交互学习」与「既有知识推理」：完整保留动作反馈记录比总结成规则更利于学习，顶尖人类峰值仍高于 agent，固定 backbone 下换 harness 可降本增效。

### 2026-10-09 · RISEBench++: Reasoning-Informed Visual Editing ⭐
> [arXiv](https://arxiv.org/abs/2610.12343) · upvotes: 12 · 推理相关性: 4/5 · 子方向: reasoning-other

首个推理驱动视觉编辑 benchmark：六维推理（时间/因果/空间/逻辑/反事实/混合）层级分类、1000 例中英标注；training-free 的 RISE-Agent 集成推理规划 + 工具执行 + verifier 精修。58 个方案中最强仅 56.6% 准确率。

### 2026-10-09 · SpaceCast-Bench: Evaluating Predictive Spatial Reasoning in Vision-Language Models ⭐
> [arXiv](https://arxiv.org/abs/2610.12402) · upvotes: 6 · 推理相关性: 5/5 · 子方向: reasoning-other

首个预测性空间推理 benchmark：observe-transform-infer 框架下三层级任务（静态感知/局部预测/全局预测）。21 模型最强仅 58.0%（人类 87.2%）；程序化数据微调把 Qwen3-VL-4B 从 34.0% 提到 65.7% 且六个 OOD 基准平均提升。

### 2026-10-09 · On-Policy Distillation Teaches New Skills but Not New Knowledge ⭐
> [arXiv](https://arxiv.org/abs/2610.09639) · upvotes: 1 · 推理相关性: 5/5 · 子方向: reasoning-other

受控实验证明 reverse-KL on-policy 蒸馏可靠迁移组合技能但极少迁移事实知识：换 forward KL 恢复事实迁移，student rollout 专益多步推理执行——OPD 不扩展参数化知识，而是教模型组织已有知识。

### 2026-10-09 · GeoReform: Reflective Formalization Evolution for Multimodal Geometry Problem Solving ⭐
> [arXiv](https://arxiv.org/abs/2610.12391v1) · upvotes: 0 · 推理相关性: 5/5 · 子方向: reasoning-other

把几何形式化当作可优化策略而非固定解析器输出：执行推理管线→收集失败→诊断表示缺陷→变异形式化策略。Geometry3K 上 Qwen3VL-2B 42.0%→56.0%；关键在组织支持下游推理的表示，而非抽取更多事实。

### 2026-10-09 · Learning to Plan by Looking Back: Hindsight Hierarchies for Training Reasoning Models ⭐
> [arXiv](https://arxiv.org/abs/2610.12168v1) · upvotes: 0 · 推理相关性: 5/5 · 子方向: reasoning-other

自改进闭环：联合训练「凭空想思路」「从已知解反推思路」「用思路解题」三能力，交替「反推→监督」循环；给出形式化规约与 Lean 定理证明实例，实证评估留作未来工作。

### 2026-10-09 · MASS: Recursive Self-Improvement through Multi-Agent Self-Supervision ⭐
> [arXiv](https://arxiv.org/abs/2610.12176v1) · upvotes: 0 · 推理相关性: 4/5 · 子方向: reasoning-other

单模型自举进化多智能体 workflow 再自蒸馏：结构护栏约束的进化搜索发现角色分工与信息路由，与自生成轨迹 SFT 交替。Qwen3.6-27B 两轮后四个开放基准每 token 性能 1.2-1.6x；多智能体轨迹训练效率更高。

### 2026-10-09 · SGUID: Selecting a Compact Skill Bank for Model-Skill Co-Evolution ⭐
> [arXiv](https://arxiv.org/abs/2610.12367v1) · upvotes: 0 · 推理相关性: 4/5 · 子方向: reasoning-other

检索技能不到 25% 有蒸馏价值：SGUID 只保留训练中持续产生有效学习信号的技能，6 个精选技能匹敌全库蒸馏（库大至 11x），支持多轮模型-技能共同进化，不过滤直接更新反而掉点。

### 2026-10-09 · UTT: Universal Textual Teaching for LLMs ⭐
> [arXiv](https://arxiv.org/abs/2610.12114v1) · upvotes: 0 · 推理相关性: 4/5 · 子方向: reasoning-other

零参数更新的知识蒸馏：师生知识差距经多角色迭代（学生做题/Prompter 转指令/教师示范/Synthesizer 沉淀）蒸馏成可复用自然语言 Primer。KernelBench 9.4%→48.6%、数学推理 27.6%→51.7%，Primer 可跨学生泛化。

### 2026-10-09 · ARC: A Reasoning Recipe for Robot Foundation Models ⭐
> [arXiv](https://arxiv.org/abs/2610.12386v1) · upvotes: 0 · 推理相关性: 4/5 · 子方向: reasoning-other

扎根下一步动作、解释因果结构（为何合适、产生何效果）的推理轨迹 + 从既有演示自动标注（ARC-Trace-DROID）+ 架构定制微调。RoboLab-Reasoning-50 提升最高 50 点，真机把 π0.5 成功率提高 82.2 点。

### 2026-10-09 · WOVEN: Weaving Visual World Modeling into Multimodal LLMs ⭐
> [arXiv](https://arxiv.org/abs/2610.12417v1) · upvotes: 0 · 推理相关性: 4/5 · 子方向: reasoning-other

视觉转移推理作为可复用训练原语：36076 例按场景/动作/推理类型组织；38 个前沿 MLLM 呈系统性短板；~2000 条子集即提升 26 个外部基准中的 22 个（最高 27.3 点），配方为按推理操作选监督、偏好更大视觉状态变化。

### 2026-10-09 · FlowMem: Recompose and Refine Latent Reasoning Flows for VLA Models ⭐
> [arXiv](https://arxiv.org/abs/2610.12090v1) · upvotes: 0 · 推理相关性: 4/5 · 子方向: reasoning-other

把 VLA 成功的 latent 推理计算存成记忆，按情境动态检索重组兼容片段成推理路线，再用当前视觉/本体感觉证据精炼后条件动作生成。RoboMME 48.0%、LIBERO-Plus 77.3%，分别超无记忆策略 1.7/4.1 点。

### 2026-10-09 · Looking Inside LLMs: Small-World Connectivity as a Signature of Reasoning Performance ⭐
> [arXiv](https://arxiv.org/abs/2610.12304v1) · upvotes: 0 · 推理相关性: 4/5 · 子方向: reasoning-other

注意力头功能图的小世界指数（SWI）与流体推理一致正相关；重要头呈高 core、低 bridge 分数，据此提出 Small-World Allocation 剪枝分配，6 个 LLM 上更好保持小世界组织与性能（WikiText 困惑度最多降 20%）。

### 2026-10-09 · grasp: Learning Probabilistic Logic Programs with Functional Gradient Guided Language Models ⭐
> [arXiv](https://arxiv.org/abs/2610.12303v1) · upvotes: 0 · 推理相关性: 4/5 · 子方向: reasoning-other

神经符号归纳推理：概率逻辑程序学习被表述为函数梯度提升，一阶规则作弱学习器、LLM 作假设生成 oracle 替代组合搜索；保留 boosting 保证与符号可解释性，四个关系基准超纯符号/神经/LLM 基线。

### 2026-10-09 · Perception Test 2026: Challenge Summary and Extension to City-scale Audio-Visual Reasoning ⭐
> [arXiv](https://arxiv.org/abs/2610.12081v1) · upvotes: 0 · 推理相关性: 4/5 · 子方向: reasoning-other

ECCV 2026 第四届挑战赛新增城市级步行视频轨道（KilometerAudio/KilometerVision）：复杂空间与多模态推理靠昂贵 agentic pipeline 可解，多模态模型单打独斗仍难——为推理系统的工程化路线提供证据。

### 2026-10-08 · VepAgent: Bridging Causal-Transition via Tool-Augmented Reinforcement Learning for Video Event Prediction ⭐
> [arXiv](https://arxiv.org/abs/2610.06293) · upvotes: 54 · 推理相关性: 4/5 · 子方向: reasoning-other

用因果转移推理 + 工具增强 RL 做视频事件预测，显式建模「终端观测态→未来事件」的逻辑推进而非被动外推历史：构建 FutureBench-4K CoT 数据 SFT 桥接未观测中间状态的因果逻辑缺口，状态跟踪/帧检索/区域放大工具库在推理时补全时空证据，复合奖励联合优化预测精度、因果一致性与可靠先验。FutureBench 与 NEPBench 上 SOTA，显著超过更大的 MLLM。

### 2026-10-07 · Selection-Based Structured Reasoning: Toward Efficient Multimodal Search Agents ⭐
> [arXiv](https://arxiv.org/abs/2610.01892) · upvotes: 17 · 推理相关性: 4/5 · 子方向: reasoning-other

把多模态 agent 的自由生成式推理改为从预定义候选中「选择」：SSR 将高频高层推理表示为可复用自然语言候选，按上下文似然选择（teacher-forced prefill 并行打分、共享上下文 KV cache），无需辅助任务头。2B/4B 模型在七个多模态搜索 benchmark 上成功率与同规模领先搜索 agent 相当，per-turn 推理延迟降低 90% 以上、单题总推理延迟降 28-54%。

### 2026-10-07 · GUI-HARVEST: Self-Improving GUI Agents through Evidence-Driven Harness Evolution ⭐
> [arXiv](https://arxiv.org/abs/2610.00948) · upvotes: 13 · 推理相关性: 4/5 · 子方向: reasoning-other

自动优化 GUI agent 的可执行 harness，冻结骨干模型即可持续自我改进：将模型输出与执行动作对齐前后截图以定位行为证据，同任务重复运行构成联合证据单元，跨任务归并为可复用 harness 代码编辑（先预测后验证）。OSWorld-Verified 六个骨干 held-out 一致提升（Qwen3-VL-32B +12.33 点），冻结 harness 迁移使 GPT-5 在 WindowsAgentArena +13.87 点。

### 2026-10-07 · DiVeR: Decision-Critical Verifier Learning for VLA Test-Time Scaling ⭐
> [arXiv](https://arxiv.org/abs/2610.04933) · upvotes: 12 · 推理相关性: 5/5 · 子方向: reasoning-other

按「决策关键性」重加权 verifier 学习，让 VLA 策略的 verifier 引导 test-time scaling 更有效：从采样动作表征的离散度估计状态决策关键性，verifier 训练聚焦动作选择真正影响下游结果的状态，无需步级标注或额外环境交互。LIBERO、RoboCasa 与 Franka 真机实验上一致提升任务成功率，verifier 推理开销可忽略。

### 2026-10-06 · OmniReasoning: Pushing the Limits of Audio-Visual Joint Reasoning ⭐
> [arXiv](https://arxiv.org/abs/2609.39490) · upvotes: 27 · 推理相关性: 5/5 · 子方向: reasoning-other

音视频联合推理的 benchmark + 数据引擎 + 学习方法三件套：OmniReasoningBench（1150 道多选/开放题，音频与视觉证据缺一不可），OmniQA 引擎自动构造带时间戳线索链的证据型 QA 并指导思维过程标注，配套学习方法激发联合推理。系统量化并有效提升现有统一全模态模型的音视频联合推理能力。

### 2026-10-06 · Base Models Can Reason By Taking a Cue From Training Data ⭐
> [arXiv](https://arxiv.org/abs/2610.06851) · upvotes: 23 · 推理相关性: 5/5 · 子方向: reasoning-other

固定起始 token 提示就能让 base model 追平 RL 训练版的数学/代码推理——推理行为源自训练数据中的 token 关联：分析起始 token（如 `.\n\nOkay`、`Alright,`）与后续推理行为的关联，对训练数据做因果干预可把任意词改造成有效推理提示或删除既有提示的效应。Olmo-3-7B 的 MATH-500 pass@1 从 42% 提到 78%，Qwen3-14B 从 72% 到 87%；RL 的作用很大程度上只是让这些提示更可能出现。

### 2026-10-06 · The Missing Primitive: Diagnosing and Repairing Mathematical Reasoning in Large Language Models ⭐
> [arXiv](https://arxiv.org/abs/2610.02191) · upvotes: 14 · 推理相关性: 5/5 · 子方向: reasoning-other

用「数学原语」四维诊断 LLM 数学理解：提出 Mathematical Primitive 概念，沿 Discovery / Generation / Digestion / Execution 四维构建 benchmark 系统诊断，再据诊断结果指导 post-training 修复。Discovery（发现）是最大瓶颈，答案正确率掩盖了能力剖面差异；诊断修复定位数学推理的结构性短板，解锁大量潜在执行容量。

### 2026-10-06 · PHRBench: A Behavioral Evaluation of Post-Hallucination Reasoning in LLMs ⭐
> [arXiv](https://arxiv.org/abs/2610.10455) · upvotes: 0 · 推理相关性: 4/5 · 子方向: reasoning-other

行为学评测 LLM 如何消化上下文中混入的幻觉前提：4820 个受控实例 × 18 个模型，从 Hallucination Compliance / Avoidance / Heuristic Correction 三维独立刻画推理轨迹（与最终对错解耦）。合规、回避与启发式纠正常见，真正「成功纠错且答对」的轨迹稀少且与模型规模等因素相关，定义并量化「insightful trajectory」。

### 2026-10-05 · RealCompanion: Benchmarking Human Understanding from Reasoning over Longitudinal Real-World Conversations ⭐
> [arXiv](https://arxiv.org/abs/2610.01780) · upvotes: 276 · 推理相关性: 4/5 · 子方向: reasoning-other

用 10 段真实人机长期陪伴对话（27,218 条消息、最长 120 天）构建首个真实关系基准，系统评测 AI 陪伴系统的「理解人」能力：发布对话原文及派生的 profile/persona/ground truth/问题集四类文件，每个 chat 标签都附带逐步核验过的 reasoning trace。简单 recency 窗口即可覆盖 95.9% 探针问题；没有任何检测器能在真实消息上判断「何时需要记忆」；三个 agent 系统以 31 倍成本差重建出同等质量的 persona。

### 2026-10-05 · MotorMind: Scaffolding General Vision Language Models for Zero-Shot Robot Manipulation ⭐
> [arXiv](https://arxiv.org/abs/2609.38078) · upvotes: 111 · 推理相关性: 4/5 · 子方向: reasoning-other

通用 VLM 借助中层动作表示 + 异步执行 harness，无需动作专家或 grounding 工具即可零样本操纵机器人：把 VLM 提出的 mid-level actions 连接到确定性机器人控制与反馈回路，配异步监控与后台记忆更新，VLM 直接从观察推理、发出动作并根据执行反馈持续适应。LIBERO-PRO 基础套件 66.7%、扰动下 53.8%（先前零样本方法至多 13.3%/19.2%），真实 xArm6 平均 95% 成功。

### 2026-10-05 · Science or Slop?: Benchmarking and Mitigating Scientific Slop in AI-Generated Papers ⭐
> [arXiv](https://arxiv.org/abs/2610.00531) · upvotes: 59 · 推理相关性: 4/5 · 子方向: reasoning-other

AI 生成论文的「slop」在于连接各部分的科学推理断裂：从 Structure/Argument/Artifacts 三方面提出 6 项度量，构建 SciSlopBench（390 篇 AI 论文+配对人类论文），SciSlopHarness 只在实验记录支持处修订 slop。配对识别准确率 85.9%（Binoculars 68.7%）；slop 与 ICLR 评分负相关；harness 将 AI-人类差距再缩小 63%。

### 2026-10-05 · Multilingual GSM-Symbolic: What determines capability transfer across languages? ⭐
> [arXiv](https://arxiv.org/abs/2610.03367) · upvotes: 51 · 推理相关性: 4/5 · 子方向: reasoning-other

用 30,000 道跨 15 语言配对的符号化数学题，量化跨语言能力迁移的决定因素：符号模板生成百万级变体防过拟合，联合回归估计各因素 β 值并预测未见语言表现。框架解释 92% 的语言间方差；模型规模 > 语言资源 > 推理能力 > 类型学距离，32B 模型 Marathi 表现 ≈ 10B 模型英语表现；模型规模与 reasoning 缩小低/高资源语言差距（β=-0.27/-0.20）。

### 2026-10-05 · ProAR: Learning Prospective Reasoning with Autoregressive Video Models ⭐
> [arXiv](https://arxiv.org/abs/2610.03664) · upvotes: 32 · 推理相关性: 4/5 · 子方向: reasoning-other

给自回归视频生成装上「目标帧前瞻」，把短视的 next-chunk 预测改造成目标导向推理过程：非对称 attention mask 把 goal-frame 预测融入 AR 循环（目标帧引导中间态生成而不被其干扰）+ 未来表征自对齐（teacher-forcing 一次前向提取干净未来表征，轻量 predictor 对齐）。多项视觉推理基准持续提升，仅用 25% 训练步数超过全训 AR 基线，可迁移到具身推理。

### 2026-10-05 · Skill2Real: Agentic Skill Learning for Zero-Shot Sim-to-Real Robot Manipulation ⭐
> [arXiv](https://arxiv.org/abs/2610.02788) · upvotes: 18 · 推理相关性: 4/5 · 子方向: reasoning-other

PVG 循环让 GPT-5.6 在仿真中学习可执行技能并零样本迁移真机：Proposer-Verifier-Governor 循环用特权仿真证据诊断结果、验证技能更新，Cerebellum 学局部操作技能、Brain 学任务级组合，均经共享 API 落地。LIBERO-Pro Long 成功率 2.0%→56.3%，冻结的 LIBERO-90 技能在 4 个真实任务上均值完成度 78.75%；去掉 Verifier/Governor 分别掉 17.3/13.3pp。

### 2026-10-05 · SAUCE: Sequential Probabilistic Uncertainty Estimation for Parallel Multi-Agent Reasoning Systems ⭐
> [arXiv](https://arxiv.org/abs/2610.08901v1) · upvotes: 0 · 推理相关性: 4/5 · 子方向: reasoning-other

把并行多 agent 推理系统的置信度建模为对潜在系统级信念的序贯推断，免训练即可校准：SAUCE 通过滤波式更新聚合轮级一致性与生成不确定性信号，跨轮演化系统级信念。5 骨干 × 5 基准 × 2 MAS 协议上，误分类检测、选择性预测、校准全面优于 log-likelihood 与 MAS 专用基线。

### 2026-10-05 · U-Space: Uncovering When and Why Uncertainty Arises in Language Models ⭐
> [arXiv](https://arxiv.org/abs/2610.09087v1) · upvotes: 0 · 推理相关性: 4/5 · 子方向: reasoning-other

在残差空间找回「怀疑/确信」语义锚点方向，构建免训练、免正确性标签、token 级可解释的不确定性地图：识别 doubt/certainty 语义锚点，把 unembedding 方向映回残差空间并正交合成基，U-Lens 把每个 token 状态投影到基上得 token 级不确定性图或聚合标量分。推理基准上置信分数超既有基线（标准与长度控制评估下均然），比有监督估计器迁移更稳。

### 2026-10-05 · Frozen Models, Evolving Expertise: Model-Agnostic Learning from Deployment Experience for Multimodal Medical AI ⭐
> [arXiv](https://arxiv.org/abs/2610.09146v1) · upvotes: 0 · 推理相关性: 4/5 · 子方向: reasoning-other

冻结模型也能从部署经验持续进化：模型无关框架以三类外部专业知识（Skill 引导推理与工具使用、Knowledge Memory、Multimodal KB）赋能冻结 LLM/VLM，验证策略保证更新只在新案例有帮助且不伤旧案例时保留。6 基准 × 4 模型上医疗任务最多 +34.2%，可泛化到未见案例、免优化迁移到其他模型、非医疗域也有效。

### 2026-10-05 · CASK: Whose Memory Is It? Scope-Aware Commit Rules for Long-Term LLM Memory ⭐
> [arXiv](https://arxiv.org/abs/2610.09008v1) · upvotes: 0 · 推理相关性: 5/5 · 子方向: reasoning-other

LLM 已内在携带「话语所有权」因果信号，CASK commit 规则保留它，让共享世界事实入长期记忆、临时内容留在原 scope，杜绝「考虑过的计划日后当真」：识别 deliberation 中的 world/branch/speaker 所有权，发现直接存内部坐标不可靠（等价表示坐标漂移），改为保留表达所有权的稳定关系作为 scoping keys。受控长对话冲突与工具 agent 轨迹上改善记忆准入、防止临时内容污染后续答案。

### 2026-10-05 · Noise Your Prompt: Noising Conditioning Tokens in Continuous Diffusion Language Models ⭐
> [arXiv](https://arxiv.org/abs/2610.09145v2) · upvotes: 0 · 推理相关性: 5/5 · 子方向: reasoning-other

训练时给条件 prompt token 也加噪这一「单行改动」，让连续扩散 LM 的组合推理大幅泛化：打破「条件 token 保持干净」的惯例，对 conditioning prompt token 同步加噪，默认零额外推理开销，还附赠 classifier-free guidance 式引导采样灵活性。Sudoku/N-Queens 等组合推理任务显著提升且难题收益最大（Sudoku Hard 3.73%→24.65%）；Gigaword 摘要质量可测提升，但开放对话等 NL 任务不迁移。

### 2026-10-05 · Humanity's Sixth Sense: Benchmarking Intuitive Visual Reasoning in Multimodal Models ⭐
> [arXiv](https://arxiv.org/abs/2610.08966v2) · upvotes: 0 · 推理相关性: 5/5 · 子方向: reasoning-other

人类「一眼即知」的直觉视觉推理（过去成因、未来轨迹、社交权力、隐性规则）上，最强 MLLM 53.6% vs 人类 93.1%：HSS 基准覆盖图像与视频，按结构化分类法组织，每题配人类撰写的探针提示，考察时间/空间/社交/抽象四类隐式结构推断，另探索动态视觉操纵的 agentic 设置。GPT-6-astra 最大推理努力下仍仅 53.6%；agentic 视觉操纵缩窄但不消除差距。

### 2026-10-05 · RACER: Reflective Agent Coupling Query Interpretation and Tool-Based Retrieval for Frame Selection in Long Video Understanding ⭐
> [arXiv](https://arxiv.org/abs/2610.08954v1) · upvotes: 0 · 推理相关性: 4/5 · 子方向: reasoning-other

轻量 Vid-LLM 负责查询解释、嵌入模型负责证据检索的反思循环，免训练解决长视频帧选择的双鸿沟：任务分解视角定位相似度法的 Query Comprehension Gap 与判断法的 Interpretation-Selection Gap，Vid-LLM 把复杂查询改写为显式子查询，检索工具定位证据帧，反馈形成反思迭代。多基准上持续提升长视频理解，弱组件经 agentic 组合也能增强强 Vid-LLM。

### 2026-10-05 · Spatial Memory Intelligence: Endowing World Models with Understanding-Driven Long-Term Memory ⭐
> [arXiv](https://arxiv.org/abs/2610.02521) · upvotes: 57 · 推理相关性: 3/5 · 子方向: reasoning-other

用理解模型（MLLM）管理长视频世界模型的长期空间记忆：SMI 框架引入空间聚类、簇内稀疏化、动作感知检索、可靠性感知过滤四个协调操作，系统化管理世界模型的长程空间上下文。跨多个世界模型骨干与基准，记忆稀疏度、生成稳定性、空间一致性全面改善。
