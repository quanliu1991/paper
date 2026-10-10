# 推理 Infra · 论文归档（★ 重点专题）

> AI Infra 推理方向：serving 系统、KV cache、投机解码、量化压缩、并行调度、MoE 推理、长上下文/VLM serving、推理集群与编译。条目按日期倒序，仅收录 infra 相关性 ≥4。

## Serving 系统

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

### 2026-10-08 · DLoop: Looped Speculative Decoding ⭐
> [arXiv](https://arxiv.org/abs/2610.07659) · upvotes: 12 · infra 相关性: 5/5 · 子方向: speculative-decoding

观察到 draft 模型能力增强后 target 常一次通过全部 draft token，逐段 verification 反而带来多余的 target forward pass；提出 DLoop，在 draft 模型保持置信时连续执行多段 drafting、将累积 draft token 合并后一次验证，并用 loop-aware training 让 draft 模型适应「未验证 token 的自身隐藏状态」这一新输入分布。以额外 draft 前向为代价换取 target 前向减少，叠加 EAGLE-3、DFlash、Domino、DSpark 及 multi-token prediction 模块时 wall-clock 加速再提升 5–41%，且保持 lossless decoding。

### 2026-10-06 · Training Parallel Speculative Draft Models by Directly Minimizing Expected Decoding Rounds
> [arXiv](https://arxiv.org/abs/2610.10411v1) · upvotes: 0 · infra 相关性: 5/5 · 子方向: speculative-decoding

把投机解码建模为 Markov reward process，提出 Expected Decoding Rounds（EDR）目标——用状态占用度加权局部拒绝代价，精确等于期望解码轮数，直接优化全局解码效率，且无辅助超参；现有 block-local 代理目标忽略了「本轮起点取决于前几轮接受多少 token」的跨轮耦合。导出精确 temporal-difference 梯度支持从目标模型 rollout 做无偏随机优化，并给出共享 rollout 上的离线轮数评估器。微调 DSpark、DFly 两个 SOTA drafter 后 mean accepted length 持续提升，在数学/代码/对话 9 个基准上全面超越既有训练目标。


## 量化与压缩

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

