# 推理 Infra · 论文归档（★ 重点专题）

> AI Infra 推理方向：serving 系统、KV cache、投机解码、量化压缩、并行调度、MoE 推理、长上下文/VLM serving、推理集群与编译。条目按日期倒序，仅收录 infra 相关性 ≥4。

## Serving 系统

### 2026-10-18 · Tandem: Serving Hybrid Linear-Attention GUI Agents on Mobile NPUs ⭐
> [arXiv](https://arxiv.org/abs/2610.26660) · upvotes: 0 · infra 相关性: 5/5 · 子方向: serving-system

手机 GUI agent 每步「读屏→问模型」累积延迟，hybrid 线性注意力模型省显存但 recurrent state 复用需要检查点，而 agent 请求「保留指令、改写近期历史」的模式让为聊天续写设计的 checkpoint 策略命不中可复用前缀。Tandem 为 agent 负载重新设计 checkpoint/rollback 策略，NPU 本地 serving，延迟与内存同时优化。

### 2026-10-18 · CEMA-Router: Infrastructure-Aware Batch Routing for LLM Inference in Cloud-Edge Systems ⭐
> [arXiv](https://arxiv.org/abs/2610.26171) · upvotes: 0 · infra 相关性: 5/5 · 子方向: serving-system

云边路由的两半脱节：LLM router 逐 query 看模型质量与 token 成本，云边调度器忽略部署模型的质量差异。CEMA-Router 做 batch 级路由，联合算力、能耗、网络、质量四方权衡，异构云边系统多目标优化。

### 2026-10-17 · Conjugate Compilation: Self-Improving Agentic Co-Compilation for Speculative Decoding ⭐
> [arXiv](https://arxiv.org/abs/2610.25012) · upvotes: 0 · infra 相关性: 5/5 · 子方向: serving-system

投机解码把 draft/target 两个模型带进 serving，但分开编译让共享执行落在编译器优化边界之外。Conjugate Compilation 把投机解码重构为跨模型联合编译问题，draft 与 target 在共享执行内联合优化，agentic 自改进 co-compilation 循环持续提升 serving 吞吐。

### 2026-10-17 · Koi: Evidence-Guided, Self-Calibrating Planning for Multi-Cloud, Heterogeneous LLM Inference Fleets ⭐
> [arXiv](https://arxiv.org/abs/2610.24355) · upvotes: 0 · infra 相关性: 5/5 · 子方向: serving-system

部署一个 LLM 要在跨云/region/市场的 ~140 个变量里做决定，且最优解随负载漂移。Koi 用递归 LLM 层级提出部署假设、确定性组件预测 serving 行为提供证据，自校准闭环持续修正规划。

### 2026-10-17 · KVCompass: A Discovery Plane for Internet-Scale Prefix Cache Sharing in LLM Serving ⭐
> [arXiv](https://arxiv.org/abs/2610.24179) · upvotes: 0 · infra 相关性: 5/5 · 子方向: serving-system

同模型跨 region 部署时各 region 重复 prefill 相同热门前缀，浪费 GPU 且推高 TTFT。跨 region 复用先要发现「哪个 worker 手里有这段 KV」，而这个发现问题在结构上比常规对象查找难（非常规放置与失效模式）。KVCompass 提出互联网规模的 KV cache 发现平面。

### 2026-10-17 · ATEST: Adaptive Resource-Aware Test-Time Scaling for LLM Inference ⭐
> [arXiv](https://arxiv.org/abs/2610.25519) · upvotes: 0 · infra 相关性: 4/5 · 子方向: serving-system

TTS 的采样预算固定，但同一 query 的能耗随 GPU 争用最高涨 4.1 倍。ATEST-Online 免离线校准：增量采样 + plurality 稳定性估计 + 当前 GPU 成本联合决定「再加一个样本值不值」，资源感知的 test-time scaling。

### 2026-10-17 · System X: An LLM Decision Model That Replies from Its Own KV Cache ⭐
> [arXiv](https://arxiv.org/abs/2610.25456) · upvotes: 0 · infra 相关性: 4/5 · 子方向: serving-system

决策模型只输出选项概率，部署时需要文字回复时通常重跑 prefill。System X 给决策模型加文字回复选项，获胜或低置信时直接从决策计算的 KV cache 续写——免重复 prefill；Qwen3-0.6B+LoRA 上 JevBench 精度无统计显著变化（55.4%→54.5%，p=0.87），校准误差还降了。

### 2026-10-16 · When the KV Cache Is Slower Than the GPU: Scaling Remote KV Tiers for Context-Parallel Prefill ⭐
> [arXiv](https://arxiv.org/abs/2610.21500) · upvotes: 0 · infra 相关性: 5/5 · 子方向: serving-system

生产事故复盘：GLM-5.3（FP8 MoE+MLA）在 8×B300 上开远程 KV 层（LMCache+Valkey），16k prompt p99 从 3.96s 涨到 17.3s——命中 0.88s 比重算 0.31s 还慢。成本模型给出两个硬数字：盈亏平衡带宽 B\*=sR=2.53 GB/s（单 Valkey 实例只给 1.71），固定成本 T₀≈0.33s 意味着短于 17k token 的命中任何带宽下都不划算。修复：MLA KV 按 chunk 分片到 PCP rank（Proposition 1 证明现有 min-over-ranks 查找恰返回最长前缀）+ 每 rank 专属 Valkey（带宽 ×6.3 至 10.76 GB/s）+ 异步加载 + 三个客户端 bug 修复（含 RESP miss-key 挂死）。hit-heavy p99 83.32s→0.67s（124×），prefill 吞吐 +34%（含 FlashInfer kernel 修复），全部提上游。核心教训：recompute 是 demanding baseline，缓存层要对着 GPU 的 prefill 速率评，不是对着网络延迟。精读笔记见 [notes/papers/2026-10-16-remote-kv-tiers.md](../../notes/papers/2026-10-16-remote-kv-tiers.md)。

### 2026-10-16 · Efficient KV Cache Migration for Geo-Distributed LLM Inference ⭐
> [arXiv](https://arxiv.org/abs/2610.22172) · upvotes: 0 · infra 相关性: 4/5 · 子方向: serving-system

地理分布协同边缘计算场景的 KV cache 迁移：会话异地续接时迁移 KV 状态而非重传全量上下文，降低跨域延迟与带宽成本。

### 2026-10-16 · PriorityFEC: Deadline-Aware Streaming FEC for KV-Cache Handoff in Edge Multi-Agent Systems ⭐
> [arXiv](https://arxiv.org/abs/2610.21390) · upvotes: 0 · infra 相关性: 4/5 · 子方向: serving-system

边缘多 agent 系统的 KV handoff 丢包问题：deadline 感知的流式前向纠错，按 KV chunk 的时效性分配冗余度。

### 2026-10-14 · RadixFlow: Filling Execution Bubbles in Prefix-Cached Hybrid LLM Serving ⭐
> [arXiv](https://arxiv.org/abs/2610.18143) · upvotes: 0 · infra 相关性: 5/5 · 子方向: serving-system

混合架构（linear + full attention 混血）的 prefix cache 有隐藏陷阱：命中前缀也未必能跑——恢复分支还需要匹配边界处的 recurrent state，而它可能正被同轮 producer 分支计算。原生调度器扫到阻塞的 consumer 就终止整条等待队列扫描，head-of-line blocking 留下本可填满的空批位（execution bubble）。RadixFlow 的 state-ready traversal 只阻塞 consumer 本人、继续扫描独立分支，下轮唤醒重查；不改缓存存储与原生 state check，已集成 vLLM。五个混合模型（Qwen3.5 0.8B-27B、Nemotron-9B）平均延迟降 3-24%、轮次降 11-44%，复用率几乎不动；全注意力对照组延迟不变，证明收益确实来自混合架构依赖处理。精读笔记见 [notes/papers/2026-10-14-radixflow.md](../../notes/papers/2026-10-14-radixflow.md)。

### 2026-10-14 · Stable Token-level Scheduling for Serverless LLM Inference ⭐
> [arXiv](https://arxiv.org/abs/2610.17689) · upvotes: 0 · infra 相关性: 4/5 · 子方向: serving-system

Serverless 推理只优化 TTFT、忽视 token 间延迟（ITL）的稳定：新请求入批会打断正在进行的 decode 造成延迟尖峰。TWP（Token Window Pacing）用 ITL/队列深度/负载特征的运行时反馈闭环，在 token 级而非 batch 级调节请求准入，配合 chunked prefill 最小化干扰。真实 serverless 负载上 TTFT 稳定、P99 尾延迟显著降、ITL 波动最小化，吞吐比 ServerlessLLM 高至 45%、比常规调度器高 58%。

### 2026-10-14 · Quota-Based Aging for Prediction-Guided Scheduling in LLM Serving ⭐
> [arXiv](https://arxiv.org/abs/2610.17795) · upvotes: 0 · infra 相关性: 4/5 · 子方向: parallelism-scheduling

预测引导的短优先调度降平均延迟但会饿死长请求，无限制 aging 又会在拥塞时过度提拔。QBA 是轻量策略：预测短优先准入 + 配额约束、债务驱动的老化请求提拔，用校准自仿真轨迹的 M/G/n 排队代理解释一阶平均延迟趋势。事件驱动模拟器（decode 优先批处理、chunked prefill、token 预算、KV 安全准入）上，QBA 在激进短优先与无限制 aging 之间提供可控中间地带，保住大部分平均延迟收益的同时大幅压低长请求尾延迟。

### 2026-10-10 · Taking Tokenization off the Host for Agentic LLM Serving ⭐
> [arXiv](https://arxiv.org/abs/2610.13325) · upvotes: 0 · infra 相关性: 5/5 · 子方向: serving-system

agentic 负载反复重发几乎不变的超长上下文，prefix caching 省掉重复 prefill 后，全量 tokenization 反而成为 TTFT 的最大组成与前端 GPU 喂数瓶颈。GraphTok 把预分词、BPE 合并、token ID 拼装整条流水线做成一个可重放 CUDA Graph，bit 级复现 GPT-2/Llama 3/Qwen 2.5/DeepSeek-V3/Gemma 3 结果，短输入回落 CPU，即插即用接入 vLLM 与 NVIDIA Dynamo。100 万 GPT-2 token 编码仅 1.7–3.2ms，比最强 CPU tokenizer gigatoken 快 4.7–6.0x；vLLM 缓存命中场景平均 TTFT 降 2.1–2.4x；2s P99 目标下单 Dynamo 前端撑起 518 req/s 的 121K token 流量（默认 tokenizer 仅 18.5）。

### 2026-10-09 · TokenRouter: Efficient Serving System for Token-Level LLM Routing ⭐
> [arXiv](https://arxiv.org/abs/2610.12242) · upvotes: 87 · infra 相关性: 5/5 · 子方向: serving-system

面向 token 级 LLM 路由（token-level routing）的高效 serving 系统。核心设计是「request-centric programming, model-centric execution」：开发者从单请求视角描述路由逻辑，runtime 为每个 LLM 启动 subserver 异步分发请求，并采用 delayed-batching scheduler，其最优超参由系统的数学吞吐模型推导。在多样路由算法、负载与模型对上，解码吞吐比现有系统高 2.01–64.15x。

### 2026-10-09 · SparseEngine: Sparse-First Inference Engine
> [arXiv](https://arxiv.org/abs/2609.39068) · upvotes: 9 · infra 相关性: 5/5 · 子方向: serving-system

从零构建的 sparse-first 推理引擎，解决稀疏注意力/KV 压缩方法与现有推理引擎难以集成的问题。核心是共享生命周期契约：每种方法自管 KV 表示与计算，同时与通用 serving 基础设施协调状态迁移；支持 4 类共 15 种方法，并通过 Chain Cache 跨请求恢复 KV-eviction 状态、可控 Prefix-Cache Pruning 按 history 区域剪 KV。保持方法质量的同时，KV eviction 下吞吐提升 10x+，同并发解码比 vLLM 快 2.5x+，agent 基准端到端加速 2x+。

### 2026-10-07 · NeMo-DCR: Bit-Exact Delta-Compressed Refit for Scalable Agentic RL at Trillion-Parameter Scale ⭐
> [arXiv](https://arxiv.org/abs/2610.08430) · upvotes: 16 · infra 相关性: 4/5 · 子方向: serving-system

面向万亿参数 agentic RL 的跨集群权重同步（refit）系统：agentic RL 训练与 rollout 分离后，每步策略更新须尽快送达 rollout 集群，而 1T 全量 checkpoint 跨 AWS 区域传输需 87.5 分钟。NeMo-DCR 只发送 bit-exact 的增量权重变更（BF16 训练每步仅约 1% 权重变化），用固定仿射映射 + 可压缩 XOR 掩码投影到 checkpoint 规范坐标，由 serving runtime 原生 loader 原位应用，对象存储/relay tree 流式传输。30B-1T 模型在 3%/5% 变更率下 refit 比全量 checkpoint 参照快 12-40x，1T relay-tree refit 从 87.5 分钟降至 150 秒。


## KV Cache 与显存

### 2026-10-18 · The KV-Surgeon: Compensation-Aware Offline KV-Cache Compaction ⭐
> [arXiv](https://arxiv.org/abs/2610.25933) · upvotes: 0 · infra 相关性: 5/5 · 子方向: kv-cache

离线压缩固定上下文的 KV cache 供反复查询，难点在「删谁」。softmax 重归一化把删除决策非线性耦合——删一个条目会改变剩余所有条目的注意力权重，逐条独立打分次优。KV-Surgeon 的补偿感知删除把耦合纳入决策，与 10-16 Competitive Attention（softmax 是比赛）结论互证。

### 2026-10-17 · Understanding KV Residency in Production-Scale Agentic LLM Workloads ⭐
> [arXiv](https://arxiv.org/abs/2610.22863) · upvotes: 0 · infra 相关性: 5/5 · 子方向: kv-cache

微软 M365 四个生产负载（Deep Research / Enterprise Assistant / Coding Agent / Enterprise Chat）超 1.21 亿次模型调用的 KV 驻留画像：Deep Research 89% 调用由应用发起，上下文中位数从约 10K 涨到 68K token。agentic KV 驻留决策的一手生产数据。

### 2026-10-17 · Certified Sparse Attention via Perturbed Retrieval ⭐
> [arXiv](https://arxiv.org/abs/2610.24991) · upvotes: 0 · infra 相关性: 5/5 · 子方向: kv-cache

稀疏注意力首次带上误差保证：真实 KV cache 上现有方法的查询误差是重尾的。给每个 key 分数加独立 Exp(1) 扰动，threshold retrieval 变成按注意力权重采样；几何网格降阈值得嵌套样本 + Horvitz-Thompson 估计，全层置信界同时成立，每个 head 误差界内即停。

### 2026-10-17 · MOSAIC: Multi-Objective Search for Allocating Inference Cache Across LLM Decoder Layers ⭐
> [arXiv](https://arxiv.org/abs/2610.25431) · upvotes: 0 · infra 相关性: 5/5 · 子方向: kv-cache

SnapKV/H2O/AdaKV/L2Norm 等驱逐方法给每层发同样的 token 预算，但各层需要的 token 不同。MOSAIC 用多目标神经架构搜索学 per-layer KV 预算，一次搜索画出「平均预算 vs 任务分」权衡曲线，最优分配无需重搜即可迁移到任意目标预算——套在任何驱逐方法之上都有效。

### 2026-10-17 · TideKV: Delayed KV Eviction via Layer-Wise Chunked Prefill for Memory-Efficient Long-Context LLM Inference ⭐
> [arXiv](https://arxiv.org/abs/2610.24499) · upvotes: 0 · infra 相关性: 5/5 · 子方向: kv-cache

长上下文的显存峰值不只 decode：全量 prefill 期间要留全量 KV。在线 chunk 级驱逐省显存但每层没看完整 prompt 就选、伤质量。TideKV 用 layer-major 延迟驱逐——逐层 chunked prefill，每层看完整 prompt 后再驱逐，压掉构建期峰值同时保住驱逐质量。

### 2026-10-17 · Prism Attention: Proposal-Refined Index Sharing Mechanism for Efficient LLMs Inference ⭐
> [arXiv](https://arxiv.org/abs/2610.22985) · upvotes: 0 · infra 相关性: 5/5 · 子方向: kv-cache

token 级稀疏注意力反复重算各层索引的代价高，锚层静态共享又忽略层间演化。Prism Attention 两段式：锚层出 proposal 索引，非锚层低成本 refine 修正——介于「每层重算」与「静态复用」之间。

### 2026-10-17 · HBFSim: A Simulator for Exploring HBF in Memory Hierarchies for LLMs ⭐
> [arXiv](https://arxiv.org/abs/2610.23503) · upvotes: 64 · infra 相关性: 4/5 · 子方向: kv-cache

高带宽 Flash（HBF）提供 TB 级 GPU 本地容量、带宽接近 HBM，但 NAND 的长延迟/乱位更新/有限写寿命让效果难预测。HBFSim 是 LLM-aware 事件驱动模拟器，保留应用级内存轨迹保真度，系统评估 HBM+HBF 分层对性能与寿命的影响。

### 2026-10-16 · Close Enough is Nowhere Near: Fidelity-Consumability Decoupling in KV Caches ⭐
> [arXiv](https://arxiv.org/abs/2610.22016) · upvotes: 0 · infra 相关性: 5/5 · 子方向: kv-cache

跨模型 KV cache 零训练直换的系统性负结果：冻结 reader 只消费「自己会写出的那种 cache」（tolerable set），三组测量钉死其窄度——cosine 0.9999 已失效（而 cosine 更远的真 cache transfer 0.445，相似度把优劣排反）、28 层坏 1 层即全坏（无深度累积）、6000 真 key 库里最近的也进不去（流形成员是必要非充分）。机制是 attention softmax 竞争性：key 互相比赛而非对标阈值，微小位移翻转胜负。出路是 augmentation：reader 保留自己的 cache、把 sender 的当额外上下文 attend，query 侧 LoRA 追平 native 基线（0.695 vs 0.665）；多 sender 池 8 个仍可用。对用 cosine/MSE 证明 KV 压缩无损的工作是方法论警钟。精读笔记见 [notes/papers/2026-10-16-kv-fidelity-consumability.md](../../notes/papers/2026-10-16-kv-fidelity-consumability.md)。

### 2026-10-16 · DropKV: Decoupled Residual-Output Perturbation for Near-Optimal KV-Cache Eviction ⭐
> [arXiv](https://arxiv.org/abs/2610.22130) · upvotes: 0 · infra 相关性: 5/5 · 子方向: kv-cache

KV 驱逐的输出扰动最小化是 NP-hard 组合问题，现有方法要么数学上次优要么难以 kernel 化。DropKV 把联合驱逐决策解耦成独立逐 token 打分，在锥条件下（三个长上下文模型实测验证）获得可证明的常数因子近似保证，兼顾近最优质量与 kernel 友好实现。

### 2026-10-16 · Compression Does Not End at Selection: Post-Selection Positional Geometry for Sparse KV Caches ⭐
> [arXiv](https://arxiv.org/abs/2610.21126) · upvotes: 0 · infra 相关性: 5/5 · 子方向: kv-cache

稀疏 KV 压缩的隐藏后手：选择保留哪些 token 之后，RoPE 下被驱逐 token 留下的位置空洞仍在影响 query-key 匹配。RoPERelay 重排紧凑保序的 RoPE 坐标，逆旋转+重旋转搬迁 key 相位并同步 query 与后续生成；零重新选择、零 re-prefill、零额外预算，在固定选择器产出上直接提升答案质量。

### 2026-10-16 · Augment the Cache, Replace the Activation: A 2x2 Study of Internal-State Sharing ⭐
> [arXiv](https://arxiv.org/abs/2610.22026) · upvotes: 0 · infra 相关性: 4/5 · 子方向: kv-cache

多 agent 内部状态共享从「点对点迁移桥」（每对 agent 一座桥）重构为「发布-订阅」：agent 把内部状态发布进池子，同伴通过一个不针对任何发送者拟合的机制读取，加 agent 只加发布者。2×2 因子实验（载体 × 融合机制）发现两个选择耦合、决定因素是消费发生在哪——与同日 Fidelity 论文互证。

### 2026-10-15 · KV4-RL: Unlocking Faster Asynchronous Rollouts for RLVR with INT4 KV Cache Quantization ⭐
> [arXiv](https://arxiv.org/abs/2610.14448) · upvotes: 26 · infra 相关性: 5/5 · 子方向: kv-cache

异步 rollout 填平长尾利用率后带来结构性副作用 KV concentration：同样的 KV 处理被压进更少 decode step（浓度因子 E[max]/E[L]≥1，实测常驻 KV 体量 ×7.82、单步延迟 ×4.52），此时 KV 量化比权重量化加速大得多（KV4 前向 1.53–1.97× vs W4A16/W8A8 贴平）。但裸 INT4 rollout 即使带 TIS 修正仍让策略学坏（MATH-500 掉 5.24 分）。KV4-RL 全上下文 paged INT4（Hadamard 旋转 + 每 head affine 组，4.25 bit/元素，calibration-free）+ 有界 INT8 边车保护 attention sink（s=16）与最近窗口（w=128），双数值路径精确 softmax 合并。Qwen3-8B GRPO rollout 累计 1.80×、整迭代 1.27×，六基准均值与 BF16 差 <0.5 分。精读笔记见 [notes/papers/2026-10-15-kv4-rl.md](../../notes/papers/2026-10-15-kv4-rl.md)。

### 2026-10-15 · JSSA: Joint Subspace Sparse Attention for Efficient Long-Context Decoding ⭐
> [arXiv](https://arxiv.org/abs/2610.19026) · upvotes: 3 · infra 相关性: 5/5 · 子方向: kv-cache

token 级稀疏注意力两难：低维打分丢 query-key 结构导致排序不准，散乱 gather 又吃掉延迟收益。JSSA 学共享低维 query-key 子空间（非凸目标上界化后谱闭式解），配 GQA 布局下 gather-free 的 per-KV-head 索引注意力 kernel。GQA/hybrid 滑窗/MLA 三类模型贴近 full-KV 精度，长上下文解码延迟显著低于粗粒度稀疏基线。

### 2026-10-15 · Latent Compaction with Test-Time Training ⭐
> [arXiv](https://arxiv.org/abs/2610.20582) · upvotes: 0 · infra 相关性: 5/5 · 子方向: kv-cache

把 KV cache 当神经网络在推理时训练压缩：重建重要性 + 教师 attention + key 多样性初始化条目，先拟合 attention 输出再端到端蒸馏自全 cache 模型，模型权重全程冻结、只用文档相关通用 prompt（不碰下游问答）。RULER 32× 压缩下 96.7% 准确率（KVZip+ 40.0%），跨模型规模/家族迁移（Qwen3、MiniCPM5）。

### 2026-10-14 · BELT: BEhavior-Aligned Low-Rank KV Cache Compression with Learned Top-k Rank Allocation ⭐
> [arXiv](https://arxiv.org/abs/2610.17966) · upvotes: 0 · infra 相关性: 5/5 · 子方向: kv-cache

低秩 KV 压缩的两个老病：目标只顾 KV 重建误差不看注意力行为（softmax 后分布可能完全走样）、rank 分配一刀切。BELT 的 key 侧目标定为注意力分布 KL（而非 pre-softmax logits），Taylor+Kronecker 展开成二次目标后有闭式加权 SVD 解；rank 用可微 top-k 软门控训练 + 硬预算部署全局学出。70% 压缩下 Qwen3-32B LongBench 超最强基线 23.3 分，叠 3-bit 量化总压缩 17.8× 只掉 1.9 分；Triton kernel 下注意力模块最高 2.7×、端到端 decode 吞吐最高 3.3×。精读笔记见 [notes/papers/2026-10-14-belt.md](../../notes/papers/2026-10-14-belt.md)。

### 2026-10-14 · MultiAlloc: Budget-Aware Precision Allocation for KV Cache Quantization ⭐
> [arXiv](https://arxiv.org/abs/2610.18642) · upvotes: 0 · infra 相关性: 4/5 · 子方向: kv-cache

KV 量化压缩的真问题不是「怎么压」而是「固定显存预算下，层级精度增强与 token 级信息保留两种策略怎么分资源」。MultiAlloc 是 profiling 引导的精度分配框架，自适应地把有限量化资源在 layer-wise 精度提升与 token-wise 保留之间分配。长上下文与复杂推理场景（KV cache 显存大头）下比单一策略更优。

### 2026-10-14 · AlignPred: Error-Controlled KV Cache Compression via Alignment and Predictive Coding ⭐
> [arXiv](https://arxiv.org/abs/2610.17970) · upvotes: 0 · infra 相关性: 4/5 · 子方向: kv-cache

长时 agent 的 KV cache 要跨轮次/会话保存数小时数天，压缩需要控重建误差。AlignPred 是「对齐 + 预测编码」codec：局部正交变换把相关 head/layer 对齐到共同坐标系，token 间预测与同 token 跨 head/layer 预测结合，残差在误差受限格子上量化 + 熵编码，无学习 predictor、无编码端模式搜索。同等重建误差下存储更省、解码至少快 1.6×；SGLang HiCache 集成下持久 KV 存储省 42-72%，128K LongBench-Pro 任务分接近原生。

### 2026-10-14 · ChampionKV: Head-Wise Adaptive Budget Allocation for KV Cache Compression ⭐
> [arXiv](https://arxiv.org/abs/2610.18026) · upvotes: 0 · infra 相关性: 4/5 · 子方向: kv-cache

观察窗口类 KV 压缩器（SnapKV/PyramidKV）给各 head 统一或预设预算，忽视输入依赖的预算需求差异。ChampionKV 用观测窗口聚合注意力最大分作为注意力集中度的轻量代理：分散的 head 给大预算、集中的给小预算，加异常 head 掩码与保底预算。即插即用不改 token 选择流程，Llama3.1-70B 上收益最大且统计显著（紧预算下尤甚），7B/8B 上持平但混合。

### 2026-10-14 · Virtual Head Attention ⭐
> [arXiv](https://arxiv.org/abs/2610.17959) · upvotes: 0 · infra 相关性: 5/5 · 子方向: kv-cache

长上下文注意力设计的不可能三角：KV cache 大小、训练/prefill FLOPs、模型质量——GQA 质量好但 cache 贵，MLA/MFA 压 cache 但要么掉质量要么涨算力。VHA 用两个轻量线性操作同时改善三角：Q Premix 从减半的物理 query head 恢复虚拟 head 多样性，Linear Postmix 低秩残差融合 head 间特征；推理时可折叠回标准 GQA-2 结构，直接复用全部现有 GQA 优化。四个规模 50B token 预训练全面超 GQA 基线，KV cache 较 GQA-8 稠密规模降 4×。

### 2026-10-14 · LatentRemedy: Efficient Remedy For Non-Prefix KV Cache Reuse in Multi-Agent Systems ⭐
> [arXiv](https://arxiv.org/abs/2610.18014) · upvotes: 0 · infra 相关性: 4/5 · 子方向: kv-cache

多 agent 共享上下文复用时除了 KV 表示失配，还有目标 agent「在自己的指令下解读共享上下文」的失配。LatentRemedy 用少量任务条件 latent token 帮目标 agent 利用复用上下文免重算：MLP 把目标前缀最后隐状态映射成几个 latent token 插在复用 KV 块后与共享上下文交互，通过全 prefill 蒸馏训练。冲突任务上一致超复用基线，cache 增大时 TTFT 保持接近直接复用。

### 2026-10-14 · SparPR: Runtime KV-Cache Recovery for Resource-Constrained LLM Inference on Consumer Hardware ⭐
> [arXiv](https://arxiv.org/abs/2610.18140) · upvotes: 0 · infra 相关性: 4/5 · 子方向: kv-cache

消费级 GPU 跑 LLM 被 KV cache 卡死，SparPR（Sparse Partial Recomputation）是运行时恢复机制：不改权重、免离线训练。三个在线决策联动——query 感知的 key 块选择（历史块对当前 query 打分）、动态预算控制（按拷贝 vs 重算成本估计保留多少块）、按需局部重算与成本感知回落（保留块并成连续 span，按运行时成本比较切换稀疏重算与全量恢复）。单张 RTX 3070 Ti 8GB 笔记本上 1k/2k/4k prompt 端到端延迟降 31%/52%/63%，吞吐 1.4-2.7×，8k 任务 44 分钟跑完（FlexGen 基线超时）。

### 2026-10-14 · Kwai Summary Attention V2 Technical Report ⭐
> [arXiv](https://arxiv.org/abs/2610.18654) · upvotes: 0 · infra 相关性: 4/5 · 子方向: kv-cache

Summary-token 架构（远上下文压成每 chunk 可学习 Summary token，与 full attention 层交错）的两个瓶颈：各层压缩 chunk 窗口被迫一致、full attention 层要为 summary token 付二次方 prefill。KSA V2 发现 summary token 可兼任 KV memory 与 sparse indexer 双角色，实现更灵活的分层压缩窗口并降低 full attention 层计算。

### 2026-10-12 · QuantMLA: Function-Aligned Dual-Path Quantization for Low-Bit MLA KV Caching ⭐
> [arXiv](https://arxiv.org/abs/2609.36760) · upvotes: 1 · infra 相关性: 5/5 · 子方向: kv-cache

MLA（DeepSeek 式潜在注意力）的 cache 含内容路与 RoPE 路，低比特量化一直难做。QuantMLA 系统建模双路量化误差对注意力输出失真的不同影响（RoPE 路误差被显著放大），推导保精度的路径专属变换空间且可离线融合进权重、零在线开销；content 路以注意力输出重构为目标、RoPE 路以 QK 重构为目标并给出失真上界。首个 content+RoPE 双 INT4 联合缓存方案（4 个 MLA 模型族精度几乎不掉），content 再压 INT2 仍有竞争力；原生低比特 MLA attention kernel 融合解包与反量化，128K 物理 cache 布局压缩 3.59x，cache 压力负载整卡输出吞吐 5.17x。

### 2026-10-10 · KV-Repurpose: A Testbed for Evaluating Non-Prefix KV-Cache Reuse ⭐
> [arXiv](https://arxiv.org/abs/2610.13060) · upvotes: 0 · infra 相关性: 5/5 · 子方向: kv-cache

KV cache 复用目前基本局限于完全一致的 prompt 前缀，同一篇检索文档跟在不同 system prompt 或对话历史后面时无法复用。KV-Repurpose 是开源的 vLLM 修正版试验台，支持段级（segment-wise）非前缀 KV 复用的开发与评测，含 cache 感知段调度、prompt 构造、容量管理、负载生成与运行时监控。Zipfian RAG 负载下（20% 请求共享固定前缀），30GB 缓存时段级复用 token 命中率 63.9% vs prefix caching 3.3%；后者即便 1TB 缓存也只到 17.9%。

### 2026-10-09 · MC-Sparse: Deconstructing and Closing the Dense-Sparse Attention Gap in Diffusion Transformers ⭐
> [arXiv](https://arxiv.org/abs/2610.06801) · upvotes: 25 · infra 相关性: 5/5 · 子方向: kv-cache

面向 diffusion transformer 长序列生成（视频/高分辨率 3D）的 training-free 稀疏注意力框架，解决高稀疏度下质量退化问题。方法上逐个选取 KV token（用精确注意力概率选索引）、把相似 query 组织成 tile 对齐组以适配 GPU 执行，并将 query 组、KV 索引与稀疏-稠密残差作为元数据缓存、在后续去噪步复用。相对稠密注意力，视频生成（Minimax-H3-Base）去噪加速 1.80x、3D 资产生成加速 2.32x，质量几乎无损。

### 2026-10-07 · DeCoPrune: Efficient KV-Cache Pruning for Autoregressive Video Diffusion via Denoising Consistency
> [arXiv](https://arxiv.org/abs/2609.39096) · upvotes: 4 · infra 相关性: 5/5 · 子方向: kv-cache

自回归视频扩散的 training-free KV cache 剪枝：KV cache 随生成历史持续增长，DeCoPrune 把 cache 压缩建模为去噪一致性问题，用 token 中间干净预测与最终去噪值的偏差（去噪难度）作为其长期保留价值的 model-intrinsic 信号，高偏差 token 留入长期 cache、低偏差剪除。配套 CMBench（58 段约 1 分钟上下文 + 116 个 Reappear/Revisit 续写任务）评估长程信息保留。LingBot World v2 上剪掉 85%+ 历史 KV token 仍保持接近 FullKV 的长程召回，续写生成加速 4x+，同预算下大幅超过窗口/相似度等压缩基线。

### 2026-10-06 · Towards Looped Models Done Right, Part II: Rethinking at Fixed Points ⭐
> [arXiv](https://arxiv.org/abs/2610.06833) · upvotes: 30 · infra 相关性: 4/5 · 子方向: kv-cache

利用循环模型 recurrent state 逼近不动点的性质，系统性削减 looped model 在解码、prefill 上的开销：提出可学习深度先验（替代 Huginn 的宽先验）支持跨循环 terminal KV sharing 解码且几乎无精度损失，蒸馏学生 prefill 提速 1.79x。1.6B 规模下，学习先验 + 3x 更小 KV cache 即可匹配固定深度全量 cache 训练的下游平均精度，RL 更新也提速 2x。

### 2026-10-06 · HLA-WM: Hybrid Linear Attention for Long-Horizon Video World Models ⭐
> [arXiv](https://arxiv.org/abs/2610.05739) · upvotes: 20 · infra 相关性: 4/5 · 子方向: kv-cache

训练无关的混合线性注意力框架，解决视频世界模型中 Gated DeltaNet 长程遗忘与全量 KV cache 显存爆炸的两难：利用 GDN 仿射结构缓存紧凑 chunk 级转移摘要，按相机几何检索场景相关历史 chunk 并重组为 query 特定 recurrent state。60 秒上下文下历史状态显存较全量 KV caching 降低 12x 而吞吐最多只降 1.6%，且 60 秒 SANA-WM-Bench 六项回访一致性/相机控制指标全面提升（PSNR +0.74 dB）。

### 2026-10-06 · ResidualQuant: KV Cache Quantization for Looped Transformers with 2-Bit Residuals
> [arXiv](https://arxiv.org/abs/2610.10381v1) · upvotes: 0 · infra 相关性: 5/5 · 子方向: kv-cache

Looped Transformer 的 KV cache 随循环次数线性膨胀成为解码吞吐与 batch size 的显存瓶颈；ResidualQuant 利用各循环 KV 状态高度相似的结构，以最终循环 KV 为基准、其余循环用低精度残差表示，可量化到 INT2，并配合最小二乘缩放、旋转与循环级混合精度。理论 KV 存储降 80.7%，同显存预算下精度较 SOTA 旋转量化高至 13.0%（混合精度下接近 BF16）；RTX 5090 上固定 batch 解码吞吐提升至 2.73x，显存节省支持 2x 更大 batch，峰值吞吐提升至 4.15x。

### 2026-10-05 · QuantWM: Temporally Consistent 2-Bit KV Cache Quantization for Video World Models ⭐
> [arXiv](https://arxiv.org/abs/2609.26425) · upvotes: 18 · infra 相关性: 5/5 · 子方向: kv-cache

发现现有 2-bit KV cache 量化在视频世界模型上会引发严重时序闪烁与画质退化，且 Key 量化重建误差虽小于 Value 却造成更大输出劣化（扰动 attention logits 使 Query 选择的时空 token 漂移）。提出免训练 2-bit KV 量化框架 QuantWM：量化敏感度感知聚类（QSAC）选取 INT2 友好的 Key 质心，主子空间注意力补偿（PSAC）用低秩投影修正残余 Key 误差；在 LingBot-World-v2、HY-World 1.5 等模型上取得最高 6.20× KV cache 显存压缩，额外开销有限。


## 投机解码

### 2026-10-20 · DScout: Factorization-Guided Training and Inference for Diffusion-Drafted Speculative Decoding ⭐
> [arXiv](https://arxiv.org/abs/2610.23935) · upvotes: 5 · infra 相关性: 5/5 · 子方向: speculative-decoding

扩散 drafter 的提案容量与 MAT 涨不等于吞吐涨：验证只接受连续前缀，早拒作废后面的正确预测；每轮延迟也随容量涨。DScout 用训练与推理两侧的互补因子分解分别治理两个失效模式——一周内第二篇给接受率指标「祛魅」的工作（第一篇是 10-17 的 Acceptance Is Not Speed）。

### 2026-10-18 · ReAnchor: Reusing Rejected Verifier States for Diffusion Drafting ⭐
> [arXiv](https://arxiv.org/abs/2610.26531) · upvotes: 0 · infra 相关性: 5/5 · 子方向: speculative-decoding

块扩散 drafter 每次前向只从一个 target 生成的锚点出固定长度块，草稿延伸受限；而验证在首个拒绝点之后算出的 hidden states 通常被丢弃。ReAnchor training-free：用这些被丢弃的 verifier states 在移位位置重新锚定 drafter，并行生成多个 draft 块——与 JetSpec++ 的 foresight 同族：榨取验证阶段「顺带」的计算。

### 2026-10-17 · When Does Better Acceptance Pay? A Controlled Study of Speculative Decoding ⭐
> [arXiv](https://arxiv.org/abs/2610.24993) · upvotes: 0 · infra 相关性: 5/5 · 子方向: speculative-decoding

投机解码论文的 drafter 对比大多训练/推理条件不对齐。建立横跨训练、推理、评测的对照协议：重测已发布 checkpoint + 在共享 target 生成数据上重训六种 drafter 配方（10 基准 × 2 target），对齐后发表对比里的大差距大幅缩水——「多接受一个 token 值不值」取决于接受长度与执行延迟的权衡。

### 2026-10-17 · Acceptance Is Not Speed: Length Inflation in Training-Free Lossy Speculative Decoding ⭐
> [arXiv](https://arxiv.org/abs/2610.23818) · upvotes: 0 · infra 相关性: 5/5 · 子方向: speculative-decoding

宽松（lossy）验证接受的 token 会改变输出分布——识别 length inflation 现象：主要拉长 reasoning 轨迹，表面 accepted tokens/round 的增益大部分被完成长度增长抵消。training-free lossy 方法的真实提速要打折看。

### 2026-10-17 · DLite: History-free Speculative Decoding for Agentic AI ⭐
> [arXiv](https://arxiv.org/abs/2610.23787) · upvotes: 21 · infra 相关性: 5/5 · 子方向: speculative-decoding

agentic 负载（长且不断演化的上下文、频繁多轮）让现有 drafter 接受长度掉最多 80%，维护 drafter 历史 KV cache 又有系统开销。DLite 刻画「增长历史上下文」对 acceptance 的伤害机制并设计 history-free drafting，与 GraphTok（tokenization 卸载）同属 agentic serving 前端优化线。

### 2026-10-17 · FlashMap: Flow Map Speculative Decoding ⭐
> [arXiv](https://arxiv.org/abs/2610.24365) · upvotes: 0 · infra 相关性: 5/5 · 子方向: speculative-decoding

自回归 drafter 逐 token 起草慢，块扩散 drafter（DFlash）一次前向出整块但 token 间互相看不见。FlashMap 用连续 flow map 模型以 target hidden states 为条件生成整块草稿，建模块内依赖，接受长度与起草速度双升。

### 2026-10-17 · BS-Spec: BFP-Based Bit-Sharing for Self-Speculative LLM Decoding ⭐
> [arXiv](https://arxiv.org/abs/2610.22877) · upvotes: 0 · infra 相关性: 5/5 · 子方向: speculative-decoding

自投机解码的 draft 配置不随负载变、混合精度执行低效。BS-Spec 用 block floating point 位共享一套框架同时管 draft 构造（免独立 drafter 的 KV cache）与 LUT 驱动的负载感知混合精度执行。

### 2026-10-17 · Trajectory-Triggered Sparse Collaborative Decoding ⭐
> [arXiv](https://arxiv.org/abs/2610.23613) · upvotes: 0 · infra 相关性: 5/5 · 子方向: speculative-decoding

sparse collaborative decoding 让 drafter 生成绝大多数 token、target 只在短纠正段被调用，关键在「何时叫 target」。局部不确定性是弱触发器：熵/NLL/logit margin/top-k mass/速度特征预测失败 AUC 仅 0.50-0.53（接近瞎猜）；聚合轨迹形状特征才有区分度。

### 2026-10-17 · PV-Decoding: Progressive Verification Decoding with Decode Gating for Diffusion Language Models ⭐
> [arXiv](https://arxiv.org/abs/2610.24722) · upvotes: 0 · infra 相关性: 5/5 · 子方向: speculative-decoding

dLLM 的投机解码两难：同块内 token 相互依赖，激进接受错传、严格验证太贵。PV-Decoding 置信度驱动的渐进验证 + decode gating 控制提交节奏，安全提交成本降低。

### 2026-10-16 · LoopAhead: Speculating Ahead for Faster Decoding in Looped Language Models ⭐
> [arXiv](https://arxiv.org/abs/2610.21594) · upvotes: 0 · infra 相关性: 5/5 · 子方向: speculative-decoding

循环 Transformer 每 token 都要顺序过重复层、反复读权重，解码延迟高。LoopAhead 给不同循环深度分派互补角色：轻量 lookahead drafter 用 early-loop 状态多 token 起草，deep-loop 反馈纠正草稿方向——比现有 pipelined 自投机更长 lookahead，且不浪费算力验证错误分支。

### 2026-10-16 · HyCo: Hybrid Drafting for Cost-Efficient Mobile-Cloud Speculative Decoding ⭐
> [arXiv](https://arxiv.org/abs/2610.21436) · upvotes: 0 · infra 相关性: 5/5 · 子方向: speculative-decoding

端云投机解码的分工重构：服务器模型的 MTP 头拿到手机 NPU 上跑（出深度），SLM 一次前向出分支，服务器只回传 hidden state/embedding/KV 而不执行串行步骤。量化+受限词表+1K 窗口把两个 drafter 塞进 NPU，ε-阈值规则放松精确分布保持。Galaxy S26 Ultra over LTE/5G，服务器 GPU 时间/token 比 MTP 自投机省 38.6%（Spec-Bench）/29.2%（32K 摘要）。

### 2026-10-16 · Speculative Forcing for Efficient Autoregressive Video Generation ⭐
> [arXiv](https://arxiv.org/abs/2610.22347) · upvotes: 67 · infra 相关性: 4/5 · 子方向: speculative-decoding

投机解码方法论外溢到视频生成：少步 AR 视频生成器给每个 token 跑完整去噪是浪费——多数 token 早期就接近终值。把中间干净估计当草稿、逐 token 预测何时可安全提前接受，接受后冻结出场（KV 保留当上下文）；验证器有 training-free（相似度+稳定性）和 learned（读冻结生成器中间特征）两版。

### 2026-10-16 · Trajectory-Level Speculation with Semantic Verification for Tool-Using Agents ⭐
> [arXiv](https://arxiv.org/abs/2610.21463) · upvotes: 9 · infra 相关性: 4/5 · 子方向: speculative-decoding

工具型 agent 的轨迹级投机：起草整段工具调用序列，用语义验证（而非逐 token 匹配）判定可否跳过中间执行步骤——投机解码思想在 agent 执行层的又一迁移。

### 2026-10-15 · JetSpec++: Foresight Parallel Drafting with Self Refinements ⭐
> [arXiv](https://arxiv.org/abs/2610.19792) · upvotes: 0 · infra 相关性: 5/5 · 子方向: speculative-decoding

把起草成本赶出关键路径：大模型验证第 t 块时，draft 侧在另一张 GPU 上用 adapter 预测目标 hidden state、decoder 算结局分布 P(接受数 k, bonus a)，押注 B=16 条「世界线」预起草第 t+1 块存入 speculation cache（命中率 92.9%）；验证窗口内跑 Jacobi 自我精修 + context refresh/anchor replacement 修 prefix-blind。token 输入 + 干净前缀调度 + forward KL 是精修能力三要素。GB200 上单请求 1361 tok/s（AR 7.45×、DSpark 1.54×），τ=8.94 全面领先，输出分布严格不变；Qwen3.8-27B hybrid 上同样有效。代码开源。精读笔记见 [notes/papers/2026-10-15-jetspecpp.md](../../notes/papers/2026-10-15-jetspecpp.md)。

### 2026-10-15 · ReaDy: Recurrent States as Dynamic Context for Speculative Drafting in Hybrid Linear Attention LLMs ⭐
> [arXiv](https://arxiv.org/abs/2610.20503) · upvotes: 0 · infra 相关性: 5/5 · 子方向: speculative-decoding

hybrid 线性注意力模型的 recurrent state 天然积累历史关联，ReaDy 首个用它做投机解码上下文检索：每个 draft 位置学 query 从目标已提交 recurrent state 取补充上下文，轻量 state reader 残差注入，低秩 state 读 + 融合算子压开销；基于 DSpark 骨干两阶段适配。七个基准超越 DSpark 起草质量。

### 2026-10-15 · FOLD: Position-Free Far Memory with Local Order for Long-Context Speculative Decoding ⭐
> [arXiv](https://arxiv.org/abs/2610.20392) · upvotes: 0 · infra 相关性: 5/5 · 子方向: speculative-decoding

长上下文 drafter 免训练方案：近处保精确位置，远处全部条目共享同一位置的「far memory」，注意力 dilution 用锐化 + 总权重控制对抗；drafter 轻量故全历史注意力付得起。6 组目标-drafter 对、最多 256K token 基准上多数最佳，最好 case 加速超 AR 2×。

### 2026-10-15 · TreeSpark: Learning to Draft the Trees You Verify for Speculative Decoding ⭐
> [arXiv](https://arxiv.org/abs/2610.20175) · upvotes: 0 · infra 相关性: 5/5 · 子方向: speculative-decoding

并行 drafter 早期失配限制每块接受量，保留备选又引入父状态与候选选择缺监督。TreeSpark 扩展 DSpark 为统一训练推理框架：一次骨干前向构造父条件候选树，训练时重放展开/剪枝/装箱；survival NLL 按参考路径质量加权保留边 + capped coverage hinge 促进目标重要备选，两个目标都复用参考链分布零额外目标前向。Qwen3-4B/8B 上 τ 比 DSpark 高 23.4–31.6%，吞吐 +15.1–25.0%。

### 2026-10-14 · SP$^2$ec: Adaptive Self-Speculative Decoding for Vision-Language Models ⭐
> [arXiv](https://arxiv.org/abs/2610.18735) · upvotes: 0 · infra 相关性: 5/5 · 子方向: speculative-decoding

VLM 的多模态输入让固定训练的 drafter 吞吐不稳定，self-speculative（复用 target 模型部分结构起草）效率又取决于每个 prompt 选对 draft 配置。SP²ec 是 training-free 的 bandit 算法：利用现有 self-speculative 方法（SWIFT/KnapSpec/SpecVLM）普遍存在的「单峰吞吐模式」，在线为每个 query 自适应 draft 配置，显式最小化 wall-time regret（对应真实墙钟延迟，非接受率代理）。Qwen2.5-VL-7B 与 LLaVA-NeXT-Mistral-7B 上稳定超越原方法至 11%。

### 2026-10-12 · Contextual Correction of Parallel Drafts for Speculative Decoding ⭐
> [arXiv](https://arxiv.org/abs/2610.12570) · upvotes: 18 · infra 相关性: 5/5 · 子方向: speculative-decoding

并行 drafter（DFlash 一类）一次并行预测多个未来位置的 token，但块内 token 看不到彼此的实现身份，丢了自回归天然具备的块内依赖。DCOCO（DFlash Contextual Corrector）不提交各位置 top-1，保留多候选 token 并行评估相邻位置的上下文兼容性再做选择，轻量地恢复块内依赖。4 种 verifier × 10 基准全部最高吞吐（greedy/随机解码最高 6.6x）；4–32 并发 serving 下比最强对手快 6–23%，而串行式纠正器在高并发下反而低于不加纠正的 DFlash。

### 2026-10-10 · S$^3$R: Fast and Faithful RL Rollouts via Self-Sparse Speculative Decoding ⭐
> [arXiv](https://arxiv.org/abs/2610.13202) · upvotes: 0 · infra 相关性: 5/5 · 子方向: speculative-decoding

RLVR 长上下文训练的 rollout 生成中 attention 占解码 kernel 时间的 72–76%，但直接用稀疏注意力采样会改变训练所依赖的 response group 分布，group-relative 优化下连精确的 response 级重加权也无法恢复期望的稠密策略更新。S³R 用稀疏注意力起草 token、全注意力验证并做精确投机采样，draft 与验证共享同一策略参数免训 drafter，KV-aware 调度器限制 KV cache 反复 offload/恢复。Qwen3 长上下文数学推理端到端训练吞吐 1.35–1.39x，任务表现持平；对照的稀疏直接采样 + 训练侧修正方案训练失稳。

### 2026-10-10 · Surfing the Activation Wave: Analyzing the Information and Geometry of LLM Hidden States for Speculative Decoding ⭐
> [arXiv](https://arxiv.org/abs/2610.12939) · upvotes: 0 · infra 相关性: 4/5 · 子方向: speculative-decoding

投机解码的 draft model 从 target 哪几层取 hidden states 通常靠位置启发式（如 EAGLE3 默认 [2, N//2, N-3]）。该工作给出 principled 的层选择框架：matrix-entropy 衡量信息量、CKA 衡量冗余度，并加 token-entropy 过滤剔除低预测熵 token 的 hidden states 改善统计质量。在 EAGLE3 式投机解码上，选出的层集合优于固定默认规则，并解释了为什么某些默认选择碰巧有竞争力。

### 2026-10-08 · DLoop: Looped Speculative Decoding ⭐
> [arXiv](https://arxiv.org/abs/2610.07659) · upvotes: 12 · infra 相关性: 5/5 · 子方向: speculative-decoding

观察到 draft 模型能力增强后 target 常一次通过全部 draft token，逐段 verification 反而带来多余的 target forward pass；提出 DLoop，在 draft 模型保持置信时连续执行多段 drafting、将累积 draft token 合并后一次验证，并用 loop-aware training 让 draft 模型适应「未验证 token 的自身隐藏状态」这一新输入分布。以额外 draft 前向为代价换取 target 前向减少，叠加 EAGLE-3、DFlash、Domino、DSpark 及 multi-token prediction 模块时 wall-clock 加速再提升 5–41%，且保持 lossless decoding。

### 2026-10-06 · Training Parallel Speculative Draft Models by Directly Minimizing Expected Decoding Rounds
> [arXiv](https://arxiv.org/abs/2610.10411v1) · upvotes: 0 · infra 相关性: 5/5 · 子方向: speculative-decoding

把投机解码建模为 Markov reward process，提出 Expected Decoding Rounds（EDR）目标——用状态占用度加权局部拒绝代价，精确等于期望解码轮数，直接优化全局解码效率，且无辅助超参；现有 block-local 代理目标忽略了「本轮起点取决于前几轮接受多少 token」的跨轮耦合。导出精确 temporal-difference 梯度支持从目标模型 rollout 做无偏随机优化，并给出共享 rollout 上的离线轮数评估器。微调 DSpark、DFly 两个 SOTA drafter 后 mean accepted length 持续提升，在数学/代码/对话 9 个基准上全面超越既有训练目标。


## 量化与压缩

### 2026-10-18 · MX-Like Tensor Core for LLM Inference with NPU Integration via Hardware-Software Co-Design Exploration ⭐
> [arXiv](https://arxiv.org/abs/2610.26083) · upvotes: 0 · infra 相关性: 5/5 · 子方向: quantization-compression

MX/NVFP4 块缩放格式被广泛采用，但 shared scale × 权重 × 激活的格式组合空间没人系统扫过。软硬件协同设计探索该空间，给出 NPU 边缘部署的精度-硅面积 Pareto 前沿与 tensor core 微架构集成方案。

### 2026-10-17 · FuTransformer: FP8 prefill and INT4 decode for Llama-style inference on Hopper ⭐
> [arXiv](https://arxiv.org/abs/2610.23796) · upvotes: 0 · infra 相关性: 5/5 · 子方向: quantization-compression

prefill 算力瓶颈用 FP8、decode 带宽瓶颈用 INT4（权重+KV cache）——按阶段选精度的 CUDA 实现：CODA 的 GEMM-plus-epilogue 搬到推理，直接 KV cache 放置、RMSNorm 增益折进权重、delayed scaling FP8 输出、无 padding prefill。

### 2026-10-15 · PN-Mix: Pair-Norm Guided Mixed-Precision Key Cache Quantization for Efficient Long-Output LLM Inference ⭐
> [arXiv](https://arxiv.org/abs/2610.19605) · upvotes: 0 · infra 相关性: 5/5 · 子方向: quantization-compression

2-bit KV 量化的敏感点在 RoPE 通道对：query-key pair-norm 乘积大的通道对量化误差显著放大 logit 扰动，只看 key 统计的 saliency 会漏判。PN-Mix 在 prefill 阶段一次性识别显著通道对、解码全程复用，RoPE decoder-only LLM 上 2.26-bit 平均精度追平先前 2.32–2.39 bit 方法，Pareto 扫描到 1.5 bit 仍优雅退化。

### 2026-10-14 · Revisiting Error Feedback for Model Quantization ⭐
> [arXiv](https://arxiv.org/abs/2610.18139) · upvotes: 0 · infra 相关性: 4/5 · 子方向: quantization-compression

把因果 error-feedback 系数当量化设计变量研究：将瞬时量化误差建模为独立零均值同方差变量，构造度量依赖的迹问题设计反馈系数，形式类似固定阶 GPTQ/LDLQ 反馈并支持感知下游误差传播的 Jacobian-aware 设计。证明正定度量 H 下联合旋转-反馈迹最小值为 n·det(H)^(1/n) 并给出几何平均分解的 attain 对。实验揭示 trace 最优不必改善有限层级性能——理论最优与实际之间有缝。

### 2026-10-14 · Towards Green AI: Evaluating Energy Efficiency for Quantized LLM Inference ⭐
> [arXiv](https://arxiv.org/abs/2610.17531) · upvotes: 0 · infra 相关性: 4/5 · 子方向: quantization-compression

首个统一评估权重-only 量化推理能耗的工作：5 模型 × 10 种 PTQ × 4 种 GPU（H100/A6000/A100/L4）× 多种输入输出长度。新发现：输入足够长、输出短时量化相对全精度能效峰值；batch 增大能效优势略增但有限；EETQ/Bitsandbytes int8 等 fused-kernel 实现省能最多至 4×（vs FP32 短文本生成）且精度几乎不掉；能耗与运行时强相关——实践中延迟优化约等于能耗优化。

### 2026-10-12 · SoloQ: Calibration-Free Quantization for Diffusion Language Models ⭐
> [arXiv](https://arxiv.org/abs/2610.07121) · upvotes: 30 · infra 相关性: 5/5 · 子方向: quantization-compression

扩散语言模型（dLLM）部署贵的两处：全序列去噪反复跑计算密集前向，块扩散模型还引入访存密集的 KV cache；而现有 dLLM 后训练量化都要校准数据，激活分布还随 masking 状态与去噪步漂移。SoloQ 免校准：结构化 K-RPBH 旋转把权重/激活映到边缘分布可预测的规范基，支持分布匹配码本与 NVFP4；块扩散模型对持久 KV cache 做 commit 时量化，不扰动正在去噪的块。LLaDA/Dream/Fast-dLLM v2/Nemotron-Labs-Diffusion 上 4-bit 保精度且反超校准式基线；NVFP4 峰值显存降 2.61x、端到端加速 2.24x。

### 2026-10-09 · SparseDecoding: Decoding-Aware Pruning for Accurate and Efficient LLM Inference ⭐
> [arXiv](https://arxiv.org/abs/2610.12327) · upvotes: 19 · infra 相关性: 5/5 · 子方向: quantization-compression

解码感知的 training-free 剪枝框架，针对 memory-bound 的 LLM 解码阶段。算法上用自回归生成阶段（排除 prefill）采集的层内激活构造 Hessian 校准矩阵，消除「自然语料校准 vs 自生成分布」的偏移；系统上实现带 bitmask 索引与固定步长遍历的 N:M 稀疏矩阵-向量（SpMV）kernel，补齐解码主导算子的支持。在 Llama-3.1-8B/70B、Qwen3-14B/32B 上长文生成一致优于固定文本校准，A100 端到端解码加速最高 1.48x。

### 2026-10-09 · V-CoLA: Vision Token Compression with Linear Attention
> [arXiv](https://arxiv.org/abs/2610.11251) · upvotes: 8 · infra 相关性: 5/5 · 子方向: quantization-compression

面向线性注意力（hybrid 架构，如 Qwen3.5）VLM 的 training-free 视觉 token 压缩框架，解决 softmax 注意力时代 token 剪枝/合并方法在线性注意力下失效的问题。提出 uniqueness 感知的重要性判据挑选关键视觉 token，配合自适应 token 合并，并在实现层面兼容线性注意力的 chunk-wise 并行。仅保留 50% 视觉 token 可保持 99.5% 原性能、12.5% token 仍保 88%+，prefill 加速 1.86–6.15x。

### 2026-10-08 · STEPQuant: When and Where Errors Matter in Delta-Rule Recurrent State Quantization ⭐
> [arXiv](https://arxiv.org/abs/2609.38169) · upvotes: 107 · infra 相关性: 5/5 · 子方向: quantization-compression

针对线性注意力模型用固定大小 recurrent state 替代增长 KV cache 后、并发 serving 下 state 显存成为新瓶颈的问题，提出时空两个维度的 post-training quantization 框架 STEPQuant：按误差幅度与记忆生命周期分配精度，并基于 state 分布联合拟合 key-row / value-column scale。在 Qwen3.8-27B 与 Kimi-Linear-48B-A3B-Instruct 上 6-bit 即贴近 FP32-state 精度、4-bit 配置优于 uniform INT8；集成进 SGLang（含优化 GPU kernel）后 6-bit 实现 >5x recurrent-state 压缩，总 serving 显存最多降低 68.7%。

### 2026-10-08 · GRACE: Generation-aware latent compression for efficient video generation ⭐
> [arXiv](https://arxiv.org/abs/2610.10524) · upvotes: 75 · infra 相关性: 4/5 · 子方向: quantization-compression

通过「生成感知」的两阶段 latent 压缩加速视频扩散推理：冻结 pretrained encoder 的 base latent、学习 residual latent 补偿强压缩损失的信息，并在冻结 DiT 的特征空间中对齐压缩后 latent，再以轻量微调 + 非对称去噪适配 DiT，避免从头重训。Wan2.1-I2V-14B 的 token 数减少 8x，480x832x81 设置下延迟降低 11.1x，VBench 生成质量与压缩前持平。

### 2026-10-07 · TRACE: Rollout-Guided Quantization-Aware Training for FP4 Reinforcement Learning of MoE Language Models ⭐
> [arXiv](https://arxiv.org/abs/2610.07767) · upvotes: 101 · infra 相关性: 4/5 · 子方向: quantization-compression

面向 MoE 大模型 RL 训练的 FP4 量化框架，用 rollout 侧量化结果引导训练侧 FP4 取整决策，直接缩小 train-rollout 两条低精度执行路径的偏差。核心方法为 rollout-guided quantization-aware training 加量化信息缓存（选择性保留深层 mantissa/scale，降低存储与通信开销）。在 4 个大规模 MoE 模型上实现 FP4 weight/activation + FP4 KV-cache rollout，RL 性能与 BF16 rollout 相当，rollout 加速最高 5.4x。

### 2026-10-07 · Learning Functional Subspaces for Neural Network Compression ⭐
> [arXiv](https://arxiv.org/abs/2609.40127) · upvotes: 11 · infra 相关性: 5/5 · 子方向: quantization-compression

端到端学习每个线性层应丢弃的低秩子空间（Learnable Subspace Projections），替代激活能量/层内重构误差等忽略误差跨层传播的局部闭式压缩准则，高压缩率下性能不塌缩。投影器对齐全局目标（对稠密模型输出的 KL 或原始 loss）联合训练，训练后合并为标准低秩因子；注意力层可只缓存一个窄 latent 替代完整 K/V。-70% 压缩下 Llama-2-7B WikiText-2 困惑度 10.9（最强基线 13.3）；小 batch 解码最高快 1.6x；128K 上下文下权重+KV cache 总显存缩小 13.5x（untied 基线最多 6.5x）。

### 2026-10-06 · Data Unlearning via Inverse Distillation ⭐
> [arXiv](https://arxiv.org/abs/2609.36099) · upvotes: 27 · infra 相关性: 4/5 · 子方向: quantization-compression

把多步 flow/diffusion 生成模型蒸馏成一步学生生成器的同时完成训练数据遗忘，一并解决推理多步开销与数据残留两个问题。将蒸馏表述为 forget-set 与生成分布混合上的 min-max 目标，最优处仅恢复保留数据，且无需保留集样本、额外分类器。在 MNIST/CIFAR-10 的 flow-matching 与 score-based 设定下显著降低遗忘类生成频率并保持保留类质量。

### 2026-10-06 · RealtimeWAM: One-Step Asynchronous World Action Models ⭐
> [arXiv](https://arxiv.org/abs/2610.06617) · upvotes: 19 · infra 相关性: 5/5 · 子方向: quantization-compression

面向实时具身推理的 World Action Model 极致加速变体，同时消除专家内多步去噪迭代与专家间串行等待两大推理瓶颈。Teacher-Anchored Consistency Distillation 用冻结教师多步 rollout 端点做监督，实现精确的一步动作生成；Cross-Expert Wavefront Pipelining 通过分块共享 video KV cache 让视频/动作专家异步重叠执行。在 LIBERO/LIBERO-Plus/RoboTwin 上性能损失 <1%，H100 端到端提速最高 25x。

### 2026-10-05 · Few Bits, One Law: Toward W2A4KV2
> [arXiv](https://arxiv.org/abs/2610.09202v1) · upvotes: 0 · infra 相关性: 5/5 · 子方向: quantization-compression

提出统一量化感知训练框架 CanonQ，首次联合极低比特压缩权重/激活/KV cache（W2A4KV2）：固定旋转与能量归一化把异构张量映射到规范坐标系，使冻结高斯参考码本可跨层跨模型复用，联合训练适配三路量化耦合误差，并给出冻结码本迁移误差上界与归一化感知的精确 STE Jacobian。在 LLaMA3-1B/3B/8B 上 W2A4KV2 设定较此前 SOTA 最多降低 WikiText2 困惑度 14.28×、零样本平均准确率提升 57.9%；MobileLLM-Pro-1B 上 HumanEval pass@1 相对提升 41.7%。

### 2026-10-05 · TAP: Efficient Long-Horizon Agent Pruning via Trajectory-Anchored Recovery
> [arXiv](https://arxiv.org/abs/2610.09074v1) · upvotes: 0 · infra 相关性: 4/5 · 子方向: quantization-compression

首个面向 RL 训练智能体的结构化剪枝框架：将剪枝与高效 on-policy 恢复耦合，冻结稠密 teacher 仅监督 student 的响应前缀（缓解响应内训练-推理失配并阻止误差跨轮传播），并用恢复目标梯度迭代重打分通道重要性。剪除 60% FFN 通道后，7B 智能体在 ALFWorld/WebShop 上保留 99.2%/88.0% 任务成功率，每成功任务 GPU 时间分别降低约 22%/17%。

---


## 并行与调度

### 2026-10-16 · Exact Makespan Bounds and the GPipe Homogeneity Bias for Heterogeneous LLM Inference Pipelines ⭐
> [arXiv](https://arxiv.org/abs/2610.21815) · upvotes: 0 · infra 相关性: 5/5 · 子方向: parallelism-scheduling

异构 GPU 流水线 serving 的精确 makespan 定理：纯前向无通信下 T(M)=(M-1)τ_max+Στ_j（定理 1）；异步通信（现代 NCCL）加纯加性常数 Σd_j（定理 2）；阻塞通信下 T(M)=(M-1)σ_max+Σσ_s，通信进稳态斜率当且仅当某 d_s>τ_max-τ_s（定理 3）。经典 GPipe 同质公式在异构场景的偏差被分解为同质项 Σ(τ_max-τ_j) 与忽略通信项，为异构集群的流水线配置给出理论修正。

### 2026-10-15 · Scaling LLM Inference via Parallelism: Throughput-Latency Trade-off ⭐
> [arXiv](https://arxiv.org/abs/2610.19405) · upvotes: 0 · infra 相关性: 5/5 · 子方向: parallelism-scheduling

系统刻画 TP/PP/混合并行在 prefill（决定 TTFT）与 decode（决定 ITL）两阶段的不同 trade-off：构建不同负载组合下的 TTFT-ITL feasible sets 与 Pareto frontier，提出 parallelism operating regions 概念。结论是最优并行配置强依赖负载特征、延迟 SLO 与上下文长度，给出 SLO 感知的选择框架与长上下文可扩展性分析。

### 2026-10-15 · Delta Tokenizer: Reference-Identical Tokenization of Session Deltas and Segment-Parallelism for Long Prompts on Multicore CPUs ⭐
> [arXiv](https://arxiv.org/abs/2610.19801) · upvotes: 0 · infra 相关性: 4/5 · 子方向: serving-system

agent 每轮只追加少量文本，但 CPU tokenizer 前端每次从头重分词全对话，拖长 TTFT 还吃 CPU。Delta Tokenizer 只对增量编码：保留旧 token 序列，只重编追加文本与其可能影响的短尾，在分词器切分规则不可移动的位置精确拼接；无状态长请求按切分规则分段多核并行再拼回，结果与参考实现完全一致。长会话 TTFT 显著下降。

## MoE 推理

### 2026-10-17 · Efficient CPU-GPU collaborative MoE inference via Adaptive Expert Assignment ⭐
> [arXiv](https://arxiv.org/abs/2610.23006) · upvotes: 0 · infra 相关性: 5/5 · 子方向: moe-inference

MoE 专家内存超出 GPU 容量就要 offload，现有系统对 GPU-missed 专家要么搬上 GPU（PCIe 延迟）、要么 CPU 执行（算力瓶颈）。自适应专家分配按负载把 missed 专家动态分派到合适的执行侧，规避两种瓶颈。

### 2026-10-16 · DPA-MoE: A Runtime Precision Control Framework for MoE Inference ⭐
> [arXiv](https://arxiv.org/abs/2610.21378) · upvotes: 0 · infra 相关性: 5/5 · 子方向: moe-inference

MoE 每个被路由到的 expert 仍以固定精度执行，DPA-MoE 让 routed experts 任意精度化：SharedScale AnyBCQ 把 expert FFN 权重编码为前缀可解码分块，离线画像每个 expert 的重建残差，推理时按 live router gate 分数在线分配精度 chunk——单一编码 checkpoint 在多个有效权重预算下运行，免重训免重编码。Qwen3-30B-A3B / DeepSeekMoE-16B 上同预算的 KL 与下游精度优于均匀分配，稳态吞吐开销温和。

### 2026-10-15 · LatentLoop: Scaling Looped MoE Models with Asymmetric Compute Allocation ⭐
> [arXiv](https://arxiv.org/abs/2610.19975) · upvotes: 56 · infra 相关性: 4/5 · 子方向: moe-inference

looped MoE 两次循环角色不对称（首访 residual 系数天然小）：LatentLoop 压缩首访序列、次访保全分辨率，省下的算力加宽 hidden size；MoE 权重跨访共享 + attention 参数分离适配不同序列分辨率。1.3B–7B 15 配置（最大超 10^21 FLOPs）验证 NLL 一致更低，等 NLL 下更省算力。

### 2026-10-07 · SlimWise: Decoupling Expert Pruning Across Prefill and Decode for Efficient MoE Serving ⭐
> [arXiv](https://arxiv.org/abs/2609.34117) · upvotes: 14 · infra 相关性: 5/5 · 子方向: moe-inference

按 prefill/decode 阶段解耦 MoE 专家剪枝的 serving 框架：prefill 保留全量模型（避免牺牲 compute-bound 阶段质量），decode 用剪枝模型并直接复用 prefill 生成的 KV cache、无需转换。训练无关的 KV cache 交接缩小精度差距，再加低成本蒸馏（只更新少量参数）让 decoder 适应全量模型 KV cache；基于 vLLM 实现，支持 PD 分离与 PD 同置两种部署。Qwen3.6-35B-A3B 上 50% 专家剪枝时 decode 吞吐最高提升 1.81x，精度损失极小。


## 长上下文与 VLM

### 2026-10-20 · Remembering Has a Price: Learning Memory Worth under Resource Constraints ⭐
> [arXiv](https://arxiv.org/abs/2610.26453) · upvotes: 5 · infra 相关性: 4/5 · 子方向: long-context-vlm

资源稀缺让「记什么」本身变成高价值决策：生成/交互/记忆三重紧预算下，多个复杂终身记忆方法还不如简单检索甚至不记忆。提出 memory worth 的显式学习——负结果气质与 KV Fidelity 一脉相承。

### 2026-10-20 · MemPilot: Orchestrating On-Demand Multimodal Memory Curation for LLM Agents ⭐
> [arXiv](https://arxiv.org/abs/2610.06830) · upvotes: 21 · infra 相关性: 4/5 · 子方向: long-context-vlm

agent 记忆系统大多查询无关地预处理一切，成本高且丢掉后来才知重要的细节。MemPilot 按需策展：运行时灵活编排记忆操作，性能/成本/延迟可控。

### 2026-10-20 · KronLSTM: Kronecker Delta Rule for Long Context Linear Attention ⭐
> [arXiv](https://arxiv.org/abs/2610.26834) · upvotes: 21 · infra 相关性: 4/5 · 子方向: long-context-vlm

Kronecker delta 更新规则扩展 xLSTM 家族：矩阵记忆沿单一方向做最小侵入修订——改目标关联的同时不干扰已存信息，记忆动力学可描述为马尔可夫链，长上下文记忆干扰降低。

### 2026-10-18 · MemT-1.0: Towards Memory-Native Evolution ⭐
> [arXiv](https://arxiv.org/abs/2610.26825) · upvotes: 97 · infra 相关性: 4/5 · 子方向: long-context-vlm

记忆原生架构：Gated DeltaNet-2 的 token 级稳定记忆更新 + Mixture-of-Storage 分层存储扩容，记忆内在化为模型计算的一部分；两阶段训练（继续预训练 + 记忆指令微调）。HF up 97。

### 2026-10-17 · StreamAhead: Real-Time Streaming Video Question Answering via Adaptive Precomputation ⭐
> [arXiv](https://arxiv.org/abs/2610.25551) · upvotes: 0 · infra 相关性: 4/5 · 子方向: long-context-vlm

流式视频问答的根本权衡：视频到达时多算降低查询延迟但拖慢处理速率，延迟算则相反。查询通常只用前面几帧作证据，全量建 KV cache 浪费。自适应预计算策略动态平衡两边。

### 2026-10-17 · ReTrace: Visual Backtracking for Efficient Multimodal Large Language Models ⭐
> [arXiv](https://arxiv.org/abs/2610.25005) · upvotes: 0 · infra 相关性: 4/5 · 子方向: long-context-vlm

视觉 token 压缩在浅层剪低显著 token，把「暂时不用」与「永久删除」耦合。层间注意力分析发现 Visual Backtracking：视觉 pivot 中层会回头检索内容。压缩设计保留回溯路径，MLLM 开销降而不伤检索。

### 2026-10-17 · Improving the Expressive Power of Hybrid Sequence Models via Multi-Hop Retrieval ⭐
> [arXiv](https://arxiv.org/abs/2610.25250) · upvotes: 0 · infra 相关性: 4/5 · 子方向: long-context-vlm

混合架构中高效层（sparse attention/recurrent）依赖固定大小状态、够不到 full-attention 层维护的 KV cache。理论+实证分析多跳检索访问能买回多少表达力。

### 2026-10-14 · DoSA: Dots Sparse Attention ⭐
> [arXiv](https://arxiv.org/abs/2610.13990) · upvotes: 59 · infra 相关性: 5/5 · 子方向: long-context-vlm

稀疏注意力访问的 key 少，但找 Top-K 还是要每个 indexer head 给每个 key 打分。DoSA 是无损条件化计算的方法：Top-K 选择只需「足够证据排除候选」而非完整分数——种子集提供胜出阈值下界，非负 head 投影 + 联合残差上界定正贡献上限，激活感知聚合定负 head 扣减幅度；证书把全量打分导向仍合格的候选，精确分数过滤再省写回与选择。GPU 实现 indexer 比 SGLang 快至 2.74×（vs LiteTopK 1.69×），GLM-5.2/DeepSeek-V3.2 端到端 TTFT 提速至 1.94×/1.50×。

### 2026-10-14 · Elephant in the Fridge: Constant-Memory Frame Packing for Long Video Understanding ⭐
> [arXiv](https://arxiv.org/abs/2610.16118) · upvotes: 10 · infra 相关性: 4/5 · 子方向: long-context-vlm

小时级视频把 VLM 推向显存极限：逐帧编码 token 数随视频长度线性涨，现有 token 缩减/关键帧选择仍留着 O(n) 增长。FramePack-U 是 training-free 的帧打包框架：按帧与 prompt 的语义相似度打分 + 多样性驱动排序选帧，选定帧以不同分辨率打包进固定长度上下文窗口——把任意长视频压成固定大小视觉表示，常数显存。即插即用于现成 VLM 推理时。

### 2026-10-12 · VisionWeave: Weaving Elastic Visual Representations as a Native Capability of MLLMs ⭐
> [arXiv](https://arxiv.org/abs/2610.07987) · upvotes: 52 · infra 相关性: 4/5 · 子方向: long-context-vlm

视觉 token 该细处细、该粗处粗——把「弹性视觉表示编织」训成 MLLM 原生能力：gated spatial pooler 在共享 MRoPE 坐标内同时构造粗/细两级表示，granularity router 按内容自适应分配；纯自蒸馏训练并从 Qwen3.5-4B 扩到 Qwen3.8-27B（30K+ A100 时）。平均省 43.0% token 保留 98.9% 性能（固定 50% 剪枝基线只保 88%）；SGLang 部署吞吐 2.3x、mean TTFT 降 54.4%、TPOT 降 60.6%。

### 2026-10-12 · MixTok: Adaptive Visual Tokenization with Global 1D Tokens and Sparse 2D Refinement ⭐
> [arXiv](https://arxiv.org/abs/2610.13181) · upvotes: 11 · infra 相关性: 4/5 · 子方向: long-context-vlm

混合视觉 tokenizer：全局用紧凑 1D token、内容自适应 router 只在高细化优先级位置稀疏补 2D token 做局部精修（预算内定数量），高分位置 2D 特征替换 1D 恢复的空间特征后共享 decoder 重建。ImageNet 256² 平均约 128 content token 即达 rFID 1.195 / gFID 1.95。

### 2026-10-09 · REMORY: Learning Residual Memory for Context Compaction
> [arXiv](https://arxiv.org/abs/2610.11287) · upvotes: 2 · infra 相关性: 4/5 · 子方向: long-context-vlm

为长时程 agent 的上下文压缩（context compaction）补充「残差记忆」：在文本摘要之外，用一个神经记忆网络生成一串有界的 soft memory token（以历史+摘要为条件），追加在摘要后，让冻结 LLM 逼近全量历史下的续写效果。SummHay 上仅用 5.2% 的输入位置即接近全上下文联合得分；Qwen3.8-27B 与 GLM-5.3-Flash 在长时程 agent 基准上一致提升，BrowseComp/Terminal-Bench 2.1 上重复工具输出与工具错误显著减少。

### 2026-10-08 · Mechanics of Long-Context Hybrid Models Part 1.1: From Hybrid Attention to Hybrid Position ⭐
> [arXiv](https://arxiv.org/abs/2610.10114) · upvotes: 31 · infra 相关性: 4/5 · 子方向: long-context-vlm

系统分析 full attention 与滑动窗口（SWA）/门控线性注意力（GLA、GDN）混合架构的位置归纳偏置，发现 context extension 的「跷跷板效应」：LA 混合更受益于长上下文续训，SWA 混合在长度外推上更强；并识别出 SWA 混合的 Short-Context Learning Trap 等失效模式。提出 Sliding-Window Linear Attention，实现 16x training-free 长度外推，在 64k 上下文 NIAH-SK1 上保持 100% 准确率，为高效长上下文（省 KV cache）架构设计提供直接依据。

### 2026-10-07 · UNREAL: Unifying Retrieval and Long-Context with a Single Model ⭐
> [arXiv](https://arxiv.org/abs/2610.08463) · upvotes: 18 · infra 相关性: 4/5 · 子方向: long-context-vlm

用冻结 LLM 的内部表征统一语料检索与长上下文证据选择，单一 model-native 机制覆盖 RAG 与长上下文推理两种尺度。仅新增 <500K 可训练参数、主干不动，从内部表征直接导出 chunk 编码与检索 query。在 3B token、21M chunk 的 Wikipedia 索引上超过 SOTA retriever-reranker（HotpotQA recall 49.1%→73.2%）；长上下文任务先生成时剔除干扰 token，128K 下 NoLiMa 准确率 1.0%→24.83%，并从约 32K token 起降低 FLOPs 与 time-to-first-token，上下文越长收益越大。

### 2026-10-06 · Rethinking Long-Video Efficiency: A Joint Allocation Perspective on Frames, Pixels, and Front-End Latency ⭐
> [arXiv](https://arxiv.org/abs/2610.04318) · upvotes: 17 · infra 相关性: 4/5 · 子方向: long-context-vlm

长视频 VLM 理解的 token 预算应在帧数、分辨率间联合分配：实验发现同 token 预算下稠密低分辨率采样优于稀疏原生分辨率采样，且小时级视频的墙钟时间由前端视频解码（而非最终 token 预算）主导。LoHi 是训练无关单 pass 框架，经 VLM 原生视频/图像双通路融合稠密低清流与稀疏高清帧（I-frame 元数据或 CLIP 语义多样性选帧）。同预算下平均精度较原生分辨率基线高 10.6 个百分点，小时级视频前端解码延迟最多降 7x。

### 2026-10-06 · Periscope: Extending Frozen Language Models Beyond Their Context Window
> [arXiv](https://arxiv.org/abs/2610.04047) · upvotes: 9 · infra 相关性: 4/5 · 子方向: long-context-vlm

训练无关的长上下文推理方法：把 N 个 chunk 排成 K×K 网格，冻结模型对 K 个局部 span 与 K 个跨步 span 各问同一问题，读单 token 的 answer log-odds 得到证据图，以约 s^1.5 成本让 W 窗口模型覆盖 W²/c token。LongBench v2 上只读证据图 top-9k token 即匹配该模型 32k-1M 全部窗口读取的最好成绩，InfiniteBench（中位 150k 上下文）高出 5 分；每次仅缓存一个 probe，27B 模型在单张 80GB GPU 上可处理 4.5M token 上下文（单次前向需 296GB cache）。

### 2026-10-05 · Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling ⭐
> [arXiv](https://arxiv.org/abs/2609.36529) · upvotes: 37 · infra 相关性: 4/5 · 子方向: long-context-vlm

将线性注意力推广为三阶张量循环状态：把 key、第二 key、value 的三重外积写入 3D tensor 状态，双 key 轴与两个 query 收缩读取，E 维第二 key 即带来 E 倍状态扩容且仅增加两个投影。兼容 data-dependent forgetting、delta rule 与 chunkwise-parallel 训练；在 Gated DeltaNet 与 scalar-gated linear attention 上显著提升长上下文建模与 recall，且保持常数时间推理、优于其他扩大状态的方案。

### 2026-10-05 · HelixWorld: A Real-time Interactive Audio-Visual World Model ⭐
> [arXiv](https://arxiv.org/abs/2609.38123) · upvotes: 37 · infra 相关性: 4/5 · 子方向: long-context-vlm

首个实时交互式视听一体世界模型：视觉场景与相机 6-DoF 轨迹接地的立体声同步演化。构建真立体声、米制相机位姿的高保真数据集，预训练双向 teacher 后经在线轨迹蒸馏得到少步流式 student，在单 GPU 上以 24 FPS 维持无漂移的音视频联合 rollout，实现低延迟因果交互。


## Others

### 2026-10-20 · HSPR: Recovering Software-Agent Benchmark Scores via Hierarchical Posterior Inference ⭐
> [arXiv](https://arxiv.org/abs/2610.24611) · upvotes: 3 · infra 相关性: 3/5 · 子方向: inference-other

跑全基准贵、小子集分数不准。HSPR 组合源 agent 历史响应因子与组成功率不确定性，后验引导选题——低成本高精度恢复目标 agent 分数。

### 2026-10-20 · A Conditional No-Hair Theorem for Transformers: How Language Models Forget Their Prompt ⭐
> [arXiv](https://arxiv.org/abs/2610.24133) · upvotes: 4 · infra 相关性: 3/5 · 子方向: kv-cache

模型生成 t 个 token 后对 prompt 的记忆按幂律 t^(-α) 衰减：训练过的模型忘得快（α≈0.55-0.7），未训练的慢（α≈0.2-0.5），偏移界 O(P(log t)^(L-1))。对 KV cache 生命周期管理（老上下文还值不值得留）有直接含义。

### 2026-10-17 · ArchAgent: Agentic AI for Heterogeneous System Design Across Chip, Scale-Up, and Scale-Out Domains ⭐
> [arXiv](https://arxiv.org/abs/2610.23724) · upvotes: 0 · infra 相关性: 4/5 · 子方向: inference-other

AI/HPC 系统设计空间（GPU/数据流/RISC-V × HBM/GDDR/SRAM × NVLink/IB/UEthernet）组合爆炸。层级多 agent 框架：LLM planner 分解设计问题，子 agent 分域探索。

### 2026-10-14 · Revisiting Cauchy-Schwarz Norm Bounds for SDC Detection in LLM Inference ⭐
> [arXiv](https://arxiv.org/abs/2610.18557) · upvotes: 0 · infra 相关性: 4/5 · 子方向: inference-other

LLM 每 token 数十亿次浮点操作，硬件故障可绕过系统级检测造成 Silent Data Corruption（SDC）。ABFT 是矩阵乘防错 SOTA 但开销不小还要调阈值。CSNB（Cauchy-Schwarz 范数界）作为低开销替代：控制故障注入实验显示，稠密线性层保留 ABFT 99% 检测能力的同时验证开销降 87%、阈值确定开销降 67%；但 MoE router gate 上只保留 55%——MoE 场景仍需 ABFT。

### 2026-10-12 · PreSTO: Predictive Subtree Prefetching for Fast LLM Power Sampling ⭐
> [arXiv](https://arxiv.org/abs/2610.13171) · upvotes: 9 · infra 相关性: 4/5 · 子方向: inference-other

PowerMH（test-time 从锐化分布采样的 MH 采样器）慢在接受/拒绝决策串行：每次决策决定下一提议的起点。PreSTO 把未来 MH 结果看成接受/拒绝决策树，一次模型调用批量预取一棵子树的全部提议，沿真实路径用原 MH 接受规则走——可证明不改变 MH 转移核；再利用「MH 只走到树的稀疏近单叉区域」设计预测式遍历。7 数据集 × 5 模型，PowerMH/EntropyCut/MultiTryMH 中位加速 1.71/1.91/2.33x，模型调用少 3.9x。

### 2026-10-12 · Stateless Language Agents: Scaling Long-Horizon Automated Research ⭐
> [arXiv](https://arxiv.org/abs/2610.07625) · upvotes: 9 · infra 相关性: 4/5 · 子方向: inference-other

长时程自动化研究的两个失败根源：研究状态存在对话里（历史越滚越长）、下一步做什么由 agent 自己决定（重复劳动）。SLA 反其道：harness 持有研究状态（候选解+实验结果），每次调用重建角色专属新鲜上下文；Advisor 读全局证据派实验、并行 Worker 执行。十亿 token 预算下所有任务最佳，追平最强 kernel 基线只用 17% token；Advisor 仅耗 0.6% token。

### 2026-10-12 · MetaKernelBench: Measuring GPU Kernel Knowledge Transfer Beyond Code ⭐
> [arXiv](https://arxiv.org/abs/2610.05014) · upvotes: 11 · infra 相关性: 4/5 · 子方向: inference-other

测 GPU kernel 优化 agent 蒸馏经验的跨 DSL 复用价值：74 对只差 DSL（CuTe vs TIRx）的孪生题，agent 先解一个变体、把所学蒸馏成自然语言技能，同模型带技能解另一变体。6 模型双向配对提升 -19% 到 +29%，每个模型/方向都有 16–45% 的题回退——kernel 经验迁移并非稳赚，给「agent 记忆沉淀」热潮泼了盆冷水。

### 2026-10-09 · CARE: Certifying Acceleration for Vision-Language-Action Inference
> [arXiv](https://arxiv.org/abs/2610.08917) · upvotes: 1 · infra 相关性: 4/5 · 子方向: inference-other

为 VLA（vision-language-action）推理加速技术（action chunking、视觉 token 剪枝、flow-step 缩减等）提供带统计保证的认证选择框架：用相同初始条件的配对 rollout 定义「加速致失败」，在校准集上给出有限样本保证，使失败风险低于用户预算，然后部署最快通过认证的候选，无一合格则回退原始策略。在 LIBERO 四套件 + OpenVLA-OFT 上认证 9.0–10.8x 加速，同时（95% 置信）保证至少保留 85.8% 原策略可解回合；无保证的选择器在紧预算下最多 75% 试验超预算，CARE 全部守住。

### 2026-10-07 · Selection-Based Structured Reasoning: Toward Efficient Multimodal Search Agents ⭐
> [arXiv](https://arxiv.org/abs/2610.01892) · upvotes: 17 · infra 相关性: 4/5 · 子方向: inference-other

把多模态搜索 agent 的自由形式推理生成为对预定义推理候选的选择，用并行 prefill 打分替代自回归长推理。teacher-forced prefilling 在共享上下文 KV cache 上并行计算各候选的 token 似然，无需额外任务头。2B/4B 模型在 7 个多模态搜索 benchmark 上成功率与同规模领先搜索 agent 相当，每轮推理延迟降低 90%+，每题总推理延迟降低 28-54%。

### 2026-10-07 · Hiding Tool Latency in On-Device Cascaded Voice Agent through Speculative Execution ⭐
> [arXiv](https://arxiv.org/abs/2610.07641) · upvotes: 10 · infra 相关性: 4/5 · 子方向: inference-other

端侧级联语音 agent 在用户仍在说话时，就从部分 ASR 假设投机预测工具调用并提前执行、缓存结果，把工具延迟藏进语音接收阶段。Predictor 模块预测工具请求并投机执行，缓存输出注入 LLM prompt；规则校验只注入有效缓存（应对用户自我纠正），LLM 保留直接调用权，使延迟上界不超过基线串行流水线。Android 实机语音助手上 median time-to-first-audio 从 5.79s 降至 4.60s，标准差 3.49s→2.81s，响应延迟更可预测。

### 2026-10-06 · When to Switch: Reliable Action-Chunk Extension for Vision-Language-Action Models ⭐
> [arXiv](https://arxiv.org/abs/2610.05719) · upvotes: 31 · infra 相关性: 4/5 · 子方向: inference-other

VLA 模型昂贵的推理迫使机器人在 policy 调用间停顿，造成 stop-and-go 执行；RACE 通过延长 action chunk 减少调用次数来压低推理开销。方法上用辅助一步去噪 pass 预测子技能切换时机（transition timing），并以此为条件生成动作，使长 chunk 执行可靠。2x 长度块即超越近期 SOTA 高效 VLA 的成功率，真机上 4x 长块将空闲时间缩短约 5x，成功率仍高于同长度微调基线。

### 2026-10-06 · SearchJev: A Fast and Calibrated System-1 Model for Search Agents ⭐
> [arXiv](https://arxiv.org/abs/2610.05107) · upvotes: 23 · infra 相关性: 4/5 · 子方向: inference-other

用免自回归输出的 System-1 决策模型承接搜索 agent 的高频短决策（相关性/证据充分性/搜索动作），显著降低决策延迟：直接对候选选项打分而非生成文本，SLCD 从不确定监督中学习校准的决策概率，不确定时交由 System-2 处理。决策速度提升 5.2-5.3x、期望校准误差降 41-74%；BrowseComp-Plus 上双系统将主动搜索时间提速 3.7-4.7x，准确率还从 45% 升至最高 54%。

