# 模型架构 · 论文归档

> 新架构（MoE、线性注意力、SSM 等）、模型设计。条目按日期倒序。

## Papers

### 2026-10-09 · TokenRouter: Efficient Serving System for Token-Level LLM Routing ⭐
> [arXiv](https://arxiv.org/abs/2610.12242) · upvotes: 0

token 级路由 LLM 推理的高效 serving 系统，异步子服务 + 延迟批调度，解码吞吐提升 2.01-64.15x

### 2026-10-09 · Multi-Agent Egocentric World Model（ME-World） ⭐
> [arXiv](https://arxiv.org/abs/2610.12299) · upvotes: 0

多智能体第一人称世界模型，共享 token 序列联合去噪多路 ego 视频流，保持跨视角动作与共享环境一致性

### 2026-10-09 · OuroWorld ⭐
> [arXiv](https://arxiv.org/abs/2610.12461) · upvotes: 0

免 mask 把任意静态 3DGS 场景变成无缝循环、视角自由的 3D 动态 cinemagraph

### 2026-10-09 · MC-Sparse ⭐
> [arXiv](https://arxiv.org/abs/2610.06801) · upvotes: 0

训练无关的 DiT 稀疏注意力：精确概率选 KV token + 元数据跨去噪步复用，1.8-2.3x 去噪加速

### 2026-10-09 · SparseDecoding ⭐
> [arXiv](https://arxiv.org/abs/2610.12327) · upvotes: 0

面向解码分布对齐的 LLM 剪枝（自回归生成激活做校准）+ N:M SpMV 内核，A100 上 1.48x 解码加速

### 2026-10-09 · LEGO: A Lifting-Free Approach for Exocentric-to-Egocentric Video Generation ⭐
> [arXiv](https://arxiv.org/abs/2610.12442) · upvotes: 0

免深度/点云的提升，学习式视图合成器直接渲染 ego 视角作扩散条件

### 2026-10-09 · SparseEngine ⭐
> [arXiv](https://arxiv.org/abs/2609.39068) · upvotes: 0

sparse-first 推理引擎：统一生命周期契约支持 15 种稀疏方法，agent 基准端到端 2x 加速

### 2026-10-09 · V-CoLA ⭐
> [arXiv](https://arxiv.org/abs/2610.11251) · upvotes: 0

线性注意力 VLM 的训练无关视觉 token 压缩：唯一性感知重要性 + 自适应合并，50% token 保 99.5% 性能

### 2026-10-09 · Retrieval-Centric Deep Learning（RCDL） ⭐
> [arXiv](https://arxiv.org/abs/2610.03858) · upvotes: 0

每个数据点存 KV、推理时注意力检索重组的增长型神经网络，建立核化注意力的函数梯度学习规则

### 2026-10-09 · Chaos in the Text ⭐
> [arXiv](https://arxiv.org/abs/2610.11816) · upvotes: 0

混合模态检索器的文本偏好导致 V 型性能曲线，Trident 用多正例视图 InfoNCE 平衡模态偏差

### 2026-10-09 · EDiS ⭐
> [arXiv](https://arxiv.org/abs/2610.09059) · upvotes: 0

边不相交子图一次分解缓存、逐 epoch 重组的 GNN 稀疏化框架，19 基准均值最优

### 2026-10-09 · SpaceFlow ⭐
> [arXiv](https://arxiv.org/abs/2610.12399) · upvotes: 0

训练无关的局部可控 3D 生成：几何基元按部件指定控制强度，兼得几何保真与生成自由

### 2026-10-09 · SPW-Nav ⭐
> [arXiv](https://arxiv.org/abs/2610.08941) · upvotes: 0

流式全景世界模型：单张全景实时生成 1 分钟 2K 360° 视频，理解移动指令并即时切换

### 2026-10-08 · STEPQuant: When and Where Errors Matter in Delta-Rule Recurrent State Quantization ⭐
> [arXiv](https://arxiv.org/abs/2609.38169) · upvotes: 0

按误差的时间寿命与空间影响自适应分配精度的 Delta-rule 递归状态时空量化框架，破解线性注意力 serving 显存瓶颈

### 2026-10-08 · Long-WAM: Scaling the Context of World-Action Models ⭐
> [arXiv](https://arxiv.org/abs/2610.10528) · upvotes: 0

自回归预训练让世界-动作模型真正"用上"长历史：GR-1 上上下文 0→19.2s 使成功率 63.3%→78.7%，双向预训练无净收益

### 2026-10-08 · GRACE: Generation-aware latent compression for efficient video generation ⭐
> [arXiv](https://arxiv.org/abs/2610.10524) · upvotes: 0

生成感知的两阶段 latent 压缩，让高压缩视频 autoencoder 与已训 DiT 兼容并加速视频扩散生成

### 2026-10-08 · SGF+: Decoupling Gradient Flows for Autoregressive Video Generation ⭐
> [arXiv](https://arxiv.org/abs/2610.10429) · upvotes: 0

为上下文写入与去噪分配独立参数、经因果注意力交互，解耦系统性负对齐的梯度冲突，同时提升画质与时序一致性

### 2026-10-08 · Tetris3D: 3D Scene Generation With Objects That Fit Together ⭐
> [arXiv](https://arxiv.org/abs/2610.10539) · upvotes: 0

以邻域物体几何与物理关系为条件的单图 3D 场景重建，附 1.2M 物理交互场景数据集 ComOb

### 2026-10-08 · WorldSonus: Bringing Sound to Worlds ⭐
> [arXiv](https://arxiv.org/abs/2610.08760) · upvotes: 0

流式因果 AR 扩散为世界模型实时配音（RTF 0.41），支持中途声音指令与场景几何对齐的立体声

### 2026-10-08 · Mechanics of Long-Context Hybrid Models Part 1.1: From Hybrid Attention to Hybrid Position ⭐
> [arXiv](https://arxiv.org/abs/2610.10114) · upvotes: 0

揭示混合注意力"跷跷板效应"：线性注意力混合更受益于上下文扩展、滑窗混合更擅长度外推，根源在位置归纳偏置差异

### 2026-10-08 · Recurrent Looped Transformer ⭐
> [arXiv](https://arxiv.org/abs/2610.07591) · upvotes: 0

并行编码器 + 循环解码器分层让每 token 计算路径随序列增长：parity 外推 256 bit 全对、S5 置换追踪 97%（基线 Transformer <1%）

### 2026-10-08 · NAMVIS: Next-Scale Autoregressive Multi-View Image Synthesis ⭐
> [arXiv](https://arxiv.org/abs/2610.04722) · upvotes: 0

免扩散的 next-scale 自回归多视角合成，多尺度投影位姿编码锚定相机几何

### 2026-10-08 · Mobile-4DGS: Unified Static-Dynamic Real-time Mobile Gaussian Splatting ⭐
> [arXiv](https://arxiv.org/abs/2610.05289) · upvotes: 0

镜面能量聚合 + 属性条件 SH 增强 + 多视角 alpha 增密剪枝，移动端静态-动态统一实时高斯渲染

### 2026-10-08 · QuadTok: Quadtree Visual Tokenizer for Autoregressive Image Generation ⭐
> [arXiv](https://arxiv.org/abs/2610.10497) · upvotes: 0

四叉树 tokenizer 按视觉复杂度自适应分配容量，ImageNet 省 10% token 且树结构天然支持自回归生成

### 2026-10-08 · Iris-3B: Going Beyond the Latent with Pixel-Space Diffusion Training, Conversion and Fine-Tuning ⭐
> [arXiv](https://arxiv.org/abs/2610.09450) · upvotes: 0

从零预训练 3B 像素空间 T2I 并转换 FLUX.2 Klein，发现像素空间生成先验在深度估计/复原下游并无显著优势

### 2026-10-07 · DuoMatching: Joint-Marginal Distribution Matching for Few-Step Video Generation ⭐
> [arXiv](https://arxiv.org/abs/2610.03543) · upvotes: 0

联合-边缘分布匹配蒸馏让少步流式视频生成质量与语义对齐双升，人类偏好率超 80%

### 2026-10-07 · Kinematic MeanFlow: One-Step Action Generation Policy for Robotic Foundation Models ⭐
> [arXiv](https://arxiv.org/abs/2610.00864) · upvotes: 0

运动学恒等式解耦 MeanFlow 时间导数，机器人策略一步动作生成，动作头延迟降 67.5–74.4%

### 2026-10-07 · UNREAL: Unifying Retrieval and Long-Context with a Single Model ⭐
> [arXiv](https://arxiv.org/abs/2610.08463) · upvotes: 0

单模型内部机制统一语料检索与长上下文证据选择，新增参数 <500K，HotpotQA recall 49.1%→73.2%

### 2026-10-07 · Adaptive Latent Capacity for World Models ⭐
> [arXiv](https://arxiv.org/abs/2609.32921) · upvotes: 0

JEPA 世界模型将预测信息集中于潜表征前缀并自适应前缀长度，规划成功率更高

### 2026-10-07 · SlimWise: Decoupling Expert Pruning Across Prefill and Decode for Efficient MoE Serving ⭐
> [arXiv](https://arxiv.org/abs/2609.34117) · upvotes: 0

prefill 用全模型、decode 用剪枝模型并直接复用 KV cache，解码吞吐最高 1.81x

### 2026-10-07 · Learning Functional Subspaces for Neural Network Compression ⭐
> [arXiv](https://arxiv.org/abs/2609.40127) · upvotes: 0

端到端学习各层丢弃子空间的低秩压缩 LSP，-70% 压缩下 Llama-2-7B 困惑度 10.9（最强基线 13.3）

### 2026-10-07 · Learning to Read the Contextual Tokens in Diffusion Transformers ⭐
> [arXiv](https://arxiv.org/abs/2610.06844) · upvotes: 0

瓶颈网络把 MM-DiT 上下文 token 映射进 LLM 实现自然语言「审问」，Contextual Alignment 进一步提升生成质量

### 2026-10-07 · HLA: Expressive Hybrid Linear Attention via Chunk-Wise Dynamic Mixing ⭐
> [arXiv](https://arxiv.org/abs/2610.05842) · upvotes: 0

查询依赖的 chunk 级混合线性注意力，LongBench-V2 最高 +5.57 点且外推至训练长度之外

### 2026-10-07 · Towards In-Parameter Memory Augmentation for Large Language Models ⭐
> [arXiv](https://arxiv.org/abs/2610.08630) · upvotes: 0

部署时「参数化记忆」增强 LLM 的综述：按参数位置×获取时间两轴组织领域与开放问题

### 2026-10-07 · DistScene: Object-to-Scene Distillation for 3D Scene Generation ⭐
> [arXiv](https://arxiv.org/abs/2610.06960) · upvotes: 0

环境+对象联合建模与对象到场景蒸馏，单图组合式 3D 场景生成空间一致性更佳

### 2026-10-07 · Accent Analogy Guidance: More Speaker Similarity at Equal Accent in Cross-Lingual Voice Cloning ⭐
> [arXiv](https://arxiv.org/abs/2609.29123) · upvotes: 0

训练免费的口音类比引导项消除跨语言语音克隆口音泄漏，同等口音下说话人相似度更高

### 2026-10-07 · Building Rome from a Single Image ⭐
> [arXiv](https://arxiv.org/abs/2610.08790) · upvotes: 0

改造对象中心 3D 生成器 + 自适应分块 + 约 4,000 室外场景合成，单图室内外场景重建全面超基线

### 2026-10-07 · ALIVE: Interaction-Aligned Object Insertion for First-Frame-Guided Video Editing ⭐
> [arXiv](https://arxiv.org/abs/2610.08779) · upvotes: 0

首帧引导的视频物体插入学会「活」的交互，35,800 编辑对 + VLM 交互引导

### 2026-10-07 · DeCoPrune: Efficient KV-Cache Pruning for Autoregressive Video Diffusion via Denoising Consistency ⭐
> [arXiv](https://arxiv.org/abs/2609.39096) · upvotes: 0

去噪难度作为 token 价值信号剪 KV cache，剪 85% 历史仍保持近 FullKV 长程召回、续写提速 4x+

### 2026-10-06 · Kandinsky 6.0 Video: Foundation Models for Synchronized Video and Audio Generation ⭐
> [arXiv](https://arxiv.org/abs/2610.05608) · upvotes: 0

双流 CrossDiT 音视频同步生成基础模型（Lite 3B / Pro 29B，5s 44kHz 含唇形同步，可超分至 Full-HD）

### 2026-10-06 · ALoDLM: Adaptively Looped Diffusion Language Models ⭐
> [arXiv](https://arxiv.org/abs/2610.04198) · upvotes: 0

扩散语言模型按 token 难度自适应分配循环计算深度，缓解统一深度的算力-难度错配

### 2026-10-06 · Representation-Space MMD for Diffusion Language Models ⭐
> [arXiv](https://arxiv.org/abs/2610.06648) · upvotes: 0

在冻结 DLM 特征空间最小化 MMD 的后训练方法，免全采样轨迹与辅助模型

### 2026-10-06 · Towards Looped Models Done Right, Part II: Rethinking at Fixed Points ⭐
> [arXiv](https://arxiv.org/abs/2610.06833) · upvotes: 0

在不动点处重思考循环模型：截断反传、终态 KV 共享、prefill 提速 1.79x、RL 梯度提速 2x

### 2026-10-06 · Data Unlearning via Inverse Distillation ⭐
> [arXiv](https://arxiv.org/abs/2609.36099) · upvotes: 0

逆蒸馏遗忘：把多步匹配模型蒸馏为单步生成器的同时抑制遗忘集输出

### 2026-10-06 · HLA-WM: Hybrid Linear Attention for Long-Horizon Video World Models ⭐
> [arXiv](https://arxiv.org/abs/2610.05739) · upvotes: 0

免训练混合线性注意力：几何引导检索 + 循环线性状态，缓解 GDN 长程遗忘

### 2026-10-06 · RealtimeWAM: One-Step Asynchronous World Action Models ⭐
> [arXiv](https://arxiv.org/abs/2610.06617) · upvotes: 0

单步动作生成 + 异步推理的世界-动作模型，TACD 蒸馏补局部-全局误差差

### 2026-10-06 · Prism: Dynamic Sparse Attention for Native 2K Joint Video-Audio Generation Model Training ⭐
> [arXiv](https://arxiv.org/abs/2610.05416) · upvotes: 0

时空宏区动态稀疏注意力，原生 2K 音视频联合生成训练

### 2026-10-06 · How to Loop MoE: Flatten the Experts, Untie the Attention ⭐
> [arXiv](https://arxiv.org/abs/2609.35751) · upvotes: 0

Foil：压平专家（层数减半、每层专家翻倍、过两遍）+ 解绑注意力，MoE 循环化的正确姿势

### 2026-10-06 · LiFT: Loop Flow Transformers ⭐
> [arXiv](https://arxiv.org/abs/2610.05538) · upvotes: 0

循环流 Transformer：每个循环步回归直线路径上的目标点，可外推远超训练深度

### 2026-10-06 · Empirical Variational Autoencoder ⭐
> [arXiv](https://arxiv.org/abs/2610.06545) · upvotes: 0

用训练数据经验学习自回归潜先验（仅加一个线性层），缓解 VAE 先验-后验 gap

### 2026-10-06 · PaLoRA: Paced Low-Rank Adaptation for Continual Learning ⭐
> [arXiv](https://arxiv.org/abs/2610.04226) · upvotes: 0

持续学习 LoRA 的更新幅度约束应随历史知识有效秩自适应增大，而非固定小学习率

### 2026-10-06 · LLM-as-Jev: LLMs Are Already Jev-Style Decision Models ⭐
> [arXiv](https://arxiv.org/abs/2610.02076) · upvotes: 0

LLM 天生就是决策模型：括号数字 token 的 next-token 概率即可免训练输出校准的选项分布

### 2026-10-06 · Periscope: Extending Frozen Language Models Beyond Their Context Window ⭐
> [arXiv](https://arxiv.org/abs/2610.04047) · upvotes: 0

冻结模型 K×K 网格局部/跨步扫描 + log-odds 读出，W 窗口覆盖 W²/c token 并免费得到证据图

### 2026-10-05 · FrameMorrow ⭐
> [arXiv](https://arxiv.org/abs/2609.38839) · upvotes: 0

前瞻 token 预测未来信息需求、据此挑选历史帧的长视频生成选择器，5 基准 11 模型一致性提升

### 2026-10-05 · ProWAM: World Action Modeling with Progressive Visual Planning ⭐
> [arXiv](https://arxiv.org/abs/2610.02508) · upvotes: 0

联合预测动作与稀疏视觉子目标序列，LIBERO-Plus 85.8% SOTA、真机零样本 70.0%

### 2026-10-05 · NAVA-WAM: Native Action-Prior Learning from Videos ⭐
> [arXiv](https://arxiv.org/abs/2610.03391) · upvotes: 0

观测视频直接预训练动作策略的原生动作先验学习，免表征-控制间接迁移

### 2026-10-05 · PointWAM: 3D World Action Modeling for Dexterous Robotic Manipulation ⭐
> [arXiv](https://arxiv.org/abs/2610.02840) · upvotes: 0

场景与手部解耦为共享时空坐标系的 3D 点云轨迹预测，人类视频预训练提升 DexJoCo 56.9pp

### 2026-10-05 · PDE-JEPA ⭐
> [arXiv](https://arxiv.org/abs/2609.34715) · upvotes: 0

掩码潜空间预测 + 几何投影器对齐演化几何的参数化 PDE 动力学表征学习，OOD 平均提升 51.4%

### 2026-10-05 · Triadic Linear Attention ⭐
> [arXiv](https://arxiv.org/abs/2609.36529) · upvotes: 0

三阶张量状态（key×key×value 三重外积）把线性注意力状态扩 E 倍仅加两个投影，长上下文建模与召回大幅改善

### 2026-10-05 · MinkowskiPE ⭐
> [arXiv](https://arxiv.org/abs/2609.33804) · upvotes: 0

洛伦兹变换参数化的时空联合位置编码，注意力只依赖相对时空位移，分子动力学与视频预测双赛道最佳

### 2026-10-05 · OctLLM (Octrees as an Explicit 3D Language) ⭐
> [arXiv](https://arxiv.org/abs/2610.02388) · upvotes: 0

八叉树占据 token 作为显式 3D 语言 + 独立分支加 3D 容量不动语言通路，图生 3D FID 降 17.4%

### 2026-10-05 · LVMT: Video Mask Transformer for Long-term Video Segmentation ⭐
> [arXiv](https://arxiv.org/abs/2609.34895) · upvotes: 0

GRU 时序传播自适应选择记忆 + 截断查询传播支持长视频训练，六基准 SOTA 且快 10 倍

### 2026-10-05 · Looped MoE (LOOM) ⭐
> [arXiv](https://arxiv.org/abs/2610.01153) · upvotes: 0

残差缩放 + 嵌入重注入 + 每循环独立路由器，循环 MoE 稳定扩展到 9–12 循环，1.7B 模型 ppl 9.62→7.77

### 2026-10-05 · HelixWorld ⭐
> [arXiv](https://arxiv.org/abs/2609.38123) · upvotes: 0

视觉与相机锚定空间立体声原生协同演化的实时交互视听世界模型，单 GPU 24FPS

### 2026-10-05 · QuantWM ⭐
> [arXiv](https://arxiv.org/abs/2609.26425) · upvotes: 0

保注意力 logits 与时空 token 选择的免训练 2-bit KV 量化，视频世界模型时序闪烁显著缓解

### 2026-10-05 · World Embedding Benchmark ⭐
> [arXiv](https://arxiv.org/abs/2610.03632) · upvotes: 0

8,000 例物理仿真视频 + 仿真派生标注，区分跨模态物理对齐与定量物理信息可恢复性
