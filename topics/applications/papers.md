# 应用与评测 · 论文归档

> 下游应用、benchmark、评测方法、安全。条目按日期倒序。

## Papers

### 2026-10-09 · FreeMatching ⭐
> [arXiv](https://arxiv.org/abs/2610.12421) · upvotes: 0

通用稠密对应匹配：生成 + 语义基础表示 + 异构监督，图像编辑恒等变换下也能对齐

### 2026-10-09 · TestPrism ⭐
> [arXiv](https://arxiv.org/abs/2610.12289) · upvotes: 0

用 3000 个正误候选实现评测测试质量，Joint Success Function 指标揭穿单参考 59.67% 的虚高（实际 28.00%）

### 2026-10-09 · VibeEdit ⭐
> [arXiv](https://arxiv.org/abs/2610.12229) · upvotes: 0

画布标注式图像编辑：在图上打空间标记 + 短注，指定改哪、怎么改，免文本提示

### 2026-10-09 · Do LLMs Understand Sequential Structure? ⭐
> [arXiv](https://arxiv.org/abs/2610.04977) · upvotes: 0

受控实验显示 LLM 难以恢复潜在序列结构：行为保真可掩盖错误的生成机制

### 2026-10-09 · Compo: A Spatial Canvas Interface for Poster Generation ⭐
> [arXiv](https://arxiv.org/abs/2610.12230) · upvotes: 0

空间画布接口的海报生成：语义/身份/文本/像素四类绑定，从 prompting 走向 composing

### 2026-10-09 · CARE: Certifying Acceleration for VLA Inference ⭐
> [arXiv](https://arxiv.org/abs/2610.08917) · upvotes: 0

用配对 rollout 给 VLA 推理加速器做有限样本风险认证，认证 9-10.8x 加速且保 85.8% 任务保持率

### 2026-10-08 · UltraText Bench: A Comprehensive Bilingual Benchmark for Evaluating Visual Text Rendering in Image Generation ⭐
> [arXiv](https://arxiv.org/abs/2610.09823) · upvotes: 0

432 条中英双语 prompt、24 场景 3 难度的稠密视觉文字渲染基准，Q-Judger 评文字保真/清晰/空间/场景四维

### 2026-10-08 · DecepEval: A Benchmark for Evaluating Deception in LLM Agents ⭐
> [arXiv](https://arxiv.org/abs/2610.07967) · upvotes: 0

1,532 实例、28 职业场景的 agent 欺骗基准，以欺诈理论"欺骗钻石"量化压力/激励/机会/冲突四条件对欺骗率的诱导

### 2026-10-08 · RobotWorld: Benchmarking Multimodal Agents for Robot Use Across Diverse Tasks and Embodiments ⭐
> [arXiv](https://arxiv.org/abs/2610.10409) · upvotes: 0

84 任务跨操作/移动操作/运动/驾驶/飞行的机器人 agent 测试床：agent 能搭出分割、标定、动力学等复杂工作流但难以可靠完成

### 2026-10-08 · SWE-Game: Can Coding Agents Build the Games We Want? ⭐
> [arXiv](https://arxiv.org/abs/2609.33678) · upvotes: 0

41 个可执行 Godot 游戏上的 247 任务基准（brief/GDD/补全/修复/移植五型），六模型中 Opus5 全部任务型第一

### 2026-10-08 · Inverting Multi-Vector Visual Document Indices ⭐
> [arXiv](https://arxiv.org/abs/2610.09920) · upvotes: 0

多向量视觉文档索引可被条件生成反演：恢复 47% 单词、45% 敏感 token，作查询检索 98.4% 命中源页——向量库并不比原页安全

### 2026-10-08 · Agentic RAG Evaluation: Budget Allocation Across Questions, Trajectories, and Reads ⭐
> [arXiv](https://arxiv.org/abs/2610.05034) · upvotes: 0

HotpotQA/MuSiQue 上的评测预算分配学：同 token 预算下扩大问题覆盖比增加轨迹/读取次数更降标准误

### 2026-10-08 · AdSpark: A Large-Scale Dataset and Benchmark for Product-Centric Advertisement Video Generation ⭐
> [arXiv](https://arxiv.org/abs/2610.10047) · upvotes: 0

电商来源 30 万"参考图-prompt-视频"三元组的广告视频生成数据集与基准，含产品身份/卖点/创意计划/音频脚本结构化标注

### 2026-10-08 · SheetSage2: Coherent Lead-Sheet Transcription with Synthetic Supervision ⭐
> [arXiv](https://arxiv.org/abs/2610.05336) · upvotes: 0

合成 MIDI 监督 + 任务结构化解码 + 自回归蒸馏的统一乐谱转录，单一 AR 模型超八个基准的既有系统

### 2026-10-07 · AGO AI Quality Gate: Evidence-First Release Decisions for Retrieval-Augmented Generation ⭐
> [arXiv](https://arxiv.org/abs/2610.01218) · upvotes: 0

证据优先的 RAG 发布决策框架：四态决策 + 分层评分 + 分层 beta-binomial 门 + judge 元评估

### 2026-10-07 · World Models' Last Exam in Physics ⭐
> [arXiv](https://arxiv.org/abs/2610.08791) · upvotes: 0

40 个受控物理任务（力学/光学/流体/电磁等）测量式评测视频世界模型物理一致性，最好模型 57.76/100

### 2026-10-07 · Personal-Agent Mediated Recommendation with Cross-Platform User History ⭐
> [arXiv](https://arxiv.org/abs/2610.07588) · upvotes: 0

个人 agent 用跨平台历史调解平台推荐排序，PAMO 反事实遮蔽优化救援–伤害平衡

### 2026-10-07 · BrickBench: Evaluating Agentic Brick Design ⭐
> [arXiv](https://arxiv.org/abs/2610.12452) · upvotes: 0

agentic 乐高套装设计 benchmark：领先 agent 满足可验证物理/语义约束但不及人类设计

### 2026-10-07 · Caught in the Act: Probes Effectively Detect Sabotage and Catch Unverbalized Deception ⭐
> [arXiv](https://arxiv.org/abs/2610.12445) · upvotes: 0

跨层跨 token 聚合 probe 检测欺骗/破坏，SHADE-Arena AUC 98.8%，隐藏目标区分 AUC 达 99.7%

### 2026-10-07 · Accurate but Not Humble: Evaluating Epistemic Humility in LLM Agents under Knowledge Conflict ⭐
> [arXiv](https://arxiv.org/abs/2610.12360) · upvotes: 0

以 Identify/Solve/Escalate 三维度评测 agent 认识谦逊：高准确 ≠ 高谦逊

### 2026-10-07 · When Has a Bayesian Neural Network Sampled Enough? Adaptive Inference Time with Statistical Guarantees ⭐
> [arXiv](https://arxiv.org/abs/2610.12212) · upvotes: 0

置信序列动态决定 BNN 蒙特卡洛采样数，统计保证下降低总延迟

### 2026-10-07 · A Closer Look at Agentic BBO: Benchmarking LLM Agents for Black-Box Optimization ⭐
> [arXiv](https://arxiv.org/abs/2610.12183) · upvotes: 0

统一有限预算协议的 agentic 黑盒优化基准：五域平均超直接 LLM 法、四域超最强数值优化器

### 2026-10-06 · CANOPY: Adaptive-Granularity Evidence Compression for Multimodal RAG ⭐
> [arXiv](https://arxiv.org/abs/2610.00923) · upvotes: 0

层级上按区域自适应粒度的检索后证据压缩，免 LLM 调用剪枝

### 2026-10-06 · Rethinking Long-Video Efficiency: A Joint Allocation Perspective on Frames, Pixels, and Front-End Latency ⭐
> [arXiv](https://arxiv.org/abs/2610.04318) · upvotes: 0

LoHi：密低分辨率流 + 稀高分辨率帧单遍理解，同 token 预算下更优

### 2026-10-06 · Noise Out, Bias In: Targeted Bias Injection in Diffusion Language Models via Closed-Loop Activation Steering ⭐
> [arXiv](https://arxiv.org/abs/2610.05894) · upvotes: 0

dLLM 多步去噪过程可被 PI 控制器闭环激活转向定向注入偏见

### 2026-10-06 · Certification of Real Images through Calibrated Content Authentication ⭐
> [arXiv](https://arxiv.org/abs/2610.05870) · upvotes: 0

深伪检测器四年从 99.5% 跌到 76%、对抗扰动下崩到 2%，提出基于生成器重构一致性的认证范式

### 2026-10-06 · Whose Ground Truth? Embracing Ambiguity in Human-Centered AI ⭐
> [arXiv](https://arxiv.org/abs/2610.10805) · upvotes: 0

立场论文：人本任务应建模多解释空间，区分有意义的歧义与标注噪声

### 2026-10-06 · SOTA: Stock Options Trading Agents Guided by Option-Implied Return Distributions ⭐
> [arXiv](https://arxiv.org/abs/2610.10407) · upvotes: 0

期权隐含分布引导的 agentic 交易：策略级决策 + 确定性 resolver 应对千级合约组合

### 2026-10-05 · Source Preference in the Wild ⭐
> [arXiv](https://arxiv.org/abs/2610.03195) · upvotes: 0

LLM agent 在端到端搜索中系统性偏好特定来源：少满足一条需求的偏好来源物品仍有约 2/3 概率被选中

### 2026-10-05 · Diptych ⭐
> [arXiv](https://arxiv.org/abs/2609.39963) · upvotes: 0

用户自定义比较范围 + 结构化音频特征 + 范围特定 AI 解释的音乐制作参考监听系统，12 名音乐人实测有效

### 2026-10-05 · Collective Bias Mitigation (CBM) ⭐
> [arXiv](https://arxiv.org/abs/2610.03240) · upvotes: 0

路由 + 协作（辩论/委员会拓扑）让多 LLM 互相纠偏，年龄偏见分数 0.25→0.10

### 2026-10-05 · IdeaAnchor ⭐
> [arXiv](https://arxiv.org/abs/2610.08781v1) · upvotes: 0

结构化"论文→点子"综合规格做特权信号训练文献驱动的研究 ideation 模型，锚定训练强化创造性综合、检索增强细节展开

### 2026-10-05 · Towards Financial World Modeling ⭐
> [arXiv](https://arxiv.org/abs/2610.09048v1) · upvotes: 0

近万亿观测的 Market-1T 美股数据集 + 18 种编码器策略横评：预测性能相近的编码器对市场状态的组织方式可截然不同

### 2026-10-05 · Shared-Roadmap GNN ⭐
> [arXiv](https://arxiv.org/abs/2610.09034v1) · upvotes: 0

异构 GNN 从专家求解轨迹学共享路线图，多智能体路径规划运行时间与图规模至少降 40%
