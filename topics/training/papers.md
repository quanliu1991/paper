# 训练方法 · 论文归档

> 预训练、后训练、SFT/RLHF、数据合成、蒸馏。条目按日期倒序。

## Papers

### 2026-10-09 · SimpleICL: In-context Robot Learning Made Simple ⭐
> [arXiv](https://arxiv.org/abs/2609.38173) · upvotes: 0

机器人视觉 in-context 学习极简配方：明确问题定义 + 视觉提示编码器 + 低成本数据采集

### 2026-10-09 · Post-Training Frontier T2I Models by Composing Preference and Rubric Rewards ⭐
> [arXiv](https://arxiv.org/abs/2610.02967) · upvotes: 0

偏好奖励 + rubric 奖励组合的后训练配方，Arena 榜 Ideogram-4 达 Elo 1223.5

### 2026-10-09 · ViSkill ⭐
> [arXiv](https://arxiv.org/abs/2610.12403) · upvotes: 0

视觉原生技能卡蒸馏 + 奖励塑形的 VLM agent RL 闭环，成功率达 0.89 且快于 PPO 收敛

### 2026-10-08 · ReSAIL: Mitigating Collapse in Iterative Agent Self-Distillation ⭐
> [arXiv](https://arxiv.org/abs/2609.39306) · upvotes: 0

按特权信息改变教师预测的程度选取信息量交互步骤做蒸馏，并正则保持 PI 条件行为，缓解迭代自蒸馏跨周期坍缩

### 2026-10-08 · Q-Learning with Scalar Adjoint Matching ⭐
> [arXiv](https://arxiv.org/abs/2610.10437) · upvotes: 0

利用预训练流策略速度 Jacobian 的对角集中性，闭式标量伴随替代逐步 VJP，off-policy 微调流策略大幅降本

### 2026-10-08 · Composing What Each Teacher Learned: Multi-Teacher On-Policy Distillation through Teacher-Relative Shifts ⭐
> [arXiv](https://arxiv.org/abs/2610.10460) · upvotes: 0

多教师在线蒸馏改传"教师减基座"logit 偏移并在学生冻结初始化上重锚，剥离基座引力提升端到端迁移

### 2026-10-08 · SkillForge: Co-Evolving Skills and Agents via Dynamic Skill Lifecycles ⭐
> [arXiv](https://arxiv.org/abs/2610.09832) · upvotes: 0

技能按 trial/active/stable/retired 生命周期进化的 agentic RL，淘汰有害技能实现技能库与策略共同进化

### 2026-10-08 · Learning Multimodal Embeddings with Evidence-Aligned Readout ⭐
> [arXiv](https://arxiv.org/abs/2609.33659) · upvotes: 0

在语义证据单元边界读出状态聚合为检索嵌入，发现语义证据与自由 CoT 的尾读出效果几乎相同

### 2026-10-08 · UniSkill: Learning Actor-Aligned Skill Proposals for an Evolving Policy ⭐
> [arXiv](https://arxiv.org/abs/2610.10164) · upvotes: 0

共享策略同时交互与提议技能库编辑，对比动作反馈提供"技能-执行者对齐"信号，免额外 actor rollout 评测

### 2026-10-07 · HuatuoGPT-3: RL-Only Domain Adaptation from Base Models ⭐
> [arXiv](https://arxiv.org/abs/2610.05966) · upvotes: 0

OnePO 纯 RL 领域适配（自适应目标演化 + 教师退休），27B 版 HealthBench 70.1 超越 GPT-6 Astra

### 2026-10-07 · NeMo-DCR: Bit-Exact Delta-Compressed Refit for Scalable Agentic RL at Trillion-Parameter Scale ⭐
> [arXiv](https://arxiv.org/abs/2610.08430) · upvotes: 0

位精确 delta 压缩权重同步，1T 模型跨集群 refit 从 87.5 分钟降到 150 秒（12–40x）

### 2026-10-07 · Sherpa: Teaching LLMs to Teach Adaptively ⭐
> [arXiv](https://arxiv.org/abs/2610.08778) · upvotes: 0

多轮 RL 面向多样学生原型训练教师 LLM 适应性教学，MathTutorBench 教学分 52.5%→79.2%

### 2026-10-07 · Understanding and Enhancing Backdoor Persistency in LLM Agent Post-Training ⭐
> [arXiv](https://arxiv.org/abs/2610.07510) · upvotes: 0

供应链后门可在良性 SFT+RL 后存活，PersistBD 将攻击成功率从 20% 提至 74–76%

### 2026-10-07 · Q-Shaped Options for Hierarchical Reinforcement Learning ⭐
> [arXiv](https://arxiv.org/abs/2610.12135) · upvotes: 0

用 Q 函数塑形 options 抽象，兼顾最优控制区分与状态聚合，基线全败任务上取得非零性能

### 2026-10-06 · PerturBot: Breaking Shortcut Priors in Vision-Language-Action Models with Perturbative Training ⭐
> [arXiv](https://arxiv.org/abs/2610.04616) · upvotes: 0

任务保持的腕视扰动 + 语言/动作增强，让 VLA 无法靠模态捷径吃饭

### 2026-10-06 · Self-Supervised Keyframe Discovery for Horizon-Invariant Behavior Cloning ⭐
> [arXiv](https://arxiv.org/abs/2610.10857) · upvotes: 0

Keyframe Mnemonics：自监督发现信息关键帧作策略条件，解非马尔可夫环境长程依赖

### 2026-10-06 · QuantCode Model: Specializing Language Models for Executable Algorithmic Trading Code ⭐
> [arXiv](https://arxiv.org/abs/2609.39420) · upvotes: 0

交易框架代码续训 + agent 验证 SFT 双机制特化可执行量化策略生成

### 2026-10-06 · What Gradients Add to Text Leakage in Split Language Models ⭐
> [arXiv](https://arxiv.org/abs/2610.04128) · upvotes: 0

分割学习中梯度让 token 泄露再增 3.17pp，整篇文档精确重建率从 13.71% 跳到 37.77%

### 2026-10-05 · On-Policy Parameter Update Direction (OPSFT) ⭐
> [arXiv](https://arxiv.org/abs/2609.36659) · upvotes: 0

把 on-policy 训练识别出的参数更新方向迁移给 SFT，兼得 on-policy 泛化与 SFT 效率

### 2026-10-05 · Latent-MOPD ⭐
> [arXiv](https://arxiv.org/abs/2610.02381) · upvotes: 0

首个表征级多教师 on-policy 蒸馏：预测 + 隐状态双通道、共享投影桥接宽度、按域分组更新，9 基准全面超 token-only 基线

### 2026-10-05 · From Gradients to Capabilities: Understanding Multi-Teacher On-Policy Distillation ⭐
> [arXiv](https://arxiv.org/abs/2610.02179) · upvotes: 0

揭示 MOPD 中损失平均隐式加权长响应、Adam 一阶矩抹平教师差异、BF16 舍入掩盖小更新等机制

### 2026-10-05 · Local Support Learning ⭐
> [arXiv](https://arxiv.org/abs/2610.02126) · upvotes: 0

GMM 门控让 adapter 只在自身训练分布激活，免旧数据解决 7B LLM 多阶段灾难性遗忘

### 2026-10-05 · Rollout-Marginal Distillation (RMD) ⭐
> [arXiv](https://arxiv.org/abs/2609.37925) · upvotes: 0

AR 视频扩散中逐块独立评分校正视觉质量、视频级 DMD 恢复时序一致，长 rollout 质量远超训练视域

### 2026-10-05 · NowWAM: Denoising as Generative Adaptation for Robot Control ⭐
> [arXiv](https://arxiv.org/abs/2609.28339) · upvotes: 0

无未来目标的"当前观测去噪+动作预测"共训，LIBERO-Plus 87.7% 且训练提速 1.8 倍

### 2026-10-05 · FailBank ⭐
> [arXiv](https://arxiv.org/abs/2609.39820) · upvotes: 0

CBF 安全模块做只观察教师，运行时反馈转持久策略改进：成功率 +8.5pp、累计成本 -35.6%
