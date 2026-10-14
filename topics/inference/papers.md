# 推理 Infra · 论文归档（★ 重点专题）

> AI Infra 推理方向：serving 系统、KV cache、投机解码、量化压缩、并行调度、MoE 推理、长上下文/VLM serving、推理集群与编译。条目按日期倒序，仅收录 infra 相关性 ≥4。

## Serving 系统

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

## MoE 推理

### 2026-10-07 · SlimWise: Decoupling Expert Pruning Across Prefill and Decode for Efficient MoE Serving ⭐
> [arXiv](https://arxiv.org/abs/2609.34117) · upvotes: 14 · infra 相关性: 5/5 · 子方向: moe-inference

按 prefill/decode 阶段解耦 MoE 专家剪枝的 serving 框架：prefill 保留全量模型（避免牺牲 compute-bound 阶段质量），decode 用剪枝模型并直接复用 prefill 生成的 KV cache、无需转换。训练无关的 KV cache 交接缩小精度差距，再加低成本蒸馏（只更新少量参数）让 decoder 适应全量模型 KV cache；基于 vLLM 实现，支持 PD 分离与 PD 同置两种部署。Qwen3.6-35B-A3B 上 50% 专家剪枝时 decode 吞吐最高提升 1.81x，精度损失极小。


## 长上下文与 VLM

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

