---
论文: AgentPerfBench: A Benchmarking and Evaluation Suite for Inference Performance of Agentic LLMs
arxiv: 2609.34683
日期: 2026-10-21
子方向: serving-system
状态: 精读完成
---

# AgentPerfBench：agentic 负载的推理基准

> 原文：[abs](https://arxiv.org/abs/2609.34683) · [PDF](https://arxiv.org/pdf/2609.34683) · [HTML](https://arxiv.org/html/2609.34683v1)

## 背景与动机

现在的推理硬件和 serving 引擎优化基本都拿「聊天机器人」负载当考卷：MLPerf 考单轮问答，vLLM/SGLang 自带 benchmark 用 ShareGPT 或固定长度随机 token。但真实世界里跑得越来越多的 agentic 负载，SWE-Bench 编码 agent、TerminalBench 终端 agent、OSWorld 计算机操作 agent——是另一种动物：**几十上百轮的多轮会话，上下文像滚雪球一样每轮追加**，输入输出比完全不同。

用错的考卷会得出错的结论。论文给了一个直观的数字：LLaMA-3.1-70B 在 H100 上，从聊天负载换成编码 agent 负载，TTFT（首 token 延迟）从 239ms 涨到 1139ms（4.8 倍），TPOT 涨 1.5 倍——同一块硬件、同一个模型，只因负载形态变了。88 轮的 SWE-Bench 会话把上下文滚过 32K token 后，单轮中位 TTFT 是聊天的 7 倍（433ms vs 62ms）。现有基准完全看不见这些差距。

三个具体缺口：

1. **没有公开基准覆盖 agentic 形态**（多轮 + 工具调用 + 长上下文增长）
2. **ISL/OSL 当固定参数**，不从真实 trace 的分布采样（InferenceX 用任意固定长度随机 token 填充，丢掉了真实负载的统计结构）
3. **只报单一工作点**：MLPerf Server 固定 Poisson 到达率、vLLM/SGLang 默认固定并发，都不扫到饱和——硬件真实容量测不出来

## 方法

### 工作负载面：trace 驱动的 profile

六个 canonical profile，全部来自真实基准的 trace（Table 2）：

| 负载 | 来源 | 会话类型 | ISL 中位 | OSL 中位 | 轮数中位 |
|---|---|---|---|---|---|
| 单轮聊天 | ShareGPT | 单轮 | 187 | 299 | 1 |
| 聊天会话 | ShareGPT | 多轮 | 1,291 | 169 | 10 |
| 编码 agent | SWE-Bench | 多轮 | 9,995 | 32 | 85 |
| 终端 agent | TerminalBench | 多轮 | 7,811 | 31 | 61 |
| 计算机操作 | OSWorld | 多轮 | 1,399 | 85 | 8 |

注意编码 agent 的形态：**输入输出比 355:1**（一万 token 进、32 个 token 出），跟聊天的一位数比例完全两个世界。这就是 agentic 负载的签名——prefill 占绝对主导。

两种实例化方式：

- **Trace replay**：逐字重放源 trace 的请求序列
- **Synthetic distributional**：从拟合的 per-turn ISL/OSL/轮数分布采样，随机 token 填充——便宜的等价物（序列长度和批调度决定 TTFT/TPOT，token 内容不影响 serving 行为）

### 一个坑：合成 replay 必须感知 prefix cache

B.1 的 ablation 很有教育意义。合成 trace 要复现真实 serving 行为，光匹配 token 数不够：vLLM 的 automatic prefix caching（APC）会改变行为。独立前缀的合成会话在深轮次（10-19 轮）E2EL 误差高达 31.1% MAPE；关掉 APC 降到 11.7%；**共享 1024-token 前缀后降到 3.2%**。结论：多轮 agent 会话天然共享指令前缀，合成负载必须把这个结构造出来，否则 prefix cache 的命中行为完全失真。这跟知识库里 GraphTok 的观察（agentic 负载反复重发几乎不变的超长上下文）互为印证。

### 测量方法：饱和点而非单点

闭环并发扫描：并发 C 下最多同时放 C 个请求，一个完成立刻放下一个。多轮 profile 每个槽位按轮序推进会话，保留上下文滚雪球效应。**饱和点 C\*** 定义为 req/s 不再上升（|d(req/s)/dC| < ε）的并发——所有指标只在饱和点报告。

headline 指标用 req/s 而不是 output-token/s，理由很实际：高 ISL 请求要长 prefill 但只产很少 token，token 吞吐会掩盖 agentic gap。

### 分析工具：多维 roofline

两个解析量（沿用 Zhao & Liu 2026 的形式化）：

- **OI（operational intensity）**= FLOPs/DRAM bytes。prefill 的 L=ISL 推向计算瓶颈渐近线；decode 的 L=1 贴着带宽瓶颈地板。H100 的 ridge point = 989 TFLOP/s ÷ 3,352 GB/s = **295 FLOP/byte**
- **CF（capacity footprint）**= 每 concurrent request 的 DRAM 字节（权重分摊 + KV cache）。超过 HBM 容量就必须降批/paging/驱逐

再配上 14.8 万条 per-kernel NCU profile 落地验证。关键卖点：OI/CF 只依赖模型架构和 token 统计，**不需要跑 serving 就能对新硬件做瓶颈分类**——硅还没流片就能算。

## 关键图表

![agentic 负载对比](../assets/2609.34683-fig1-agentic-contrast.svg)

*Fig 1（[arXiv HTML](https://arxiv.org/html/2609.34683v1)）：LLaMA-3.1-70B@2×H100。左：token 用量——编码 agent ISL/OSL≈355:1，prefill 主导；中：CF 随并发增长，长上下文 profile 越过 160GB HBM 预算而聊天不会；右：serving OI——聊天停在 51，编码 agent 冲到 2,366，跨过 H100 ridge（295）。*

![方法论对比](../assets/2609.34683-fig3-methodology.svg)

*Fig 3：与现有基准的能力对比——agentic 负载、多轮、NCU profiling、饱和测量、开源 trace 全部独有。*

![逐组件 OI/CF 分解](../assets/2609.34683-fig2-perlayer-oicf.svg)

*Fig 2：LLaMA-3.1-8B 单层分解。左：prefill 投影 GEMM 全部越过 ridge（计算瓶颈），attention/elementwise 双阶段带宽瓶颈；右：decode 吞吐天花板 vs CF——32K 上下文在 C≈14 就撞 80GB HBM 墙。*

![多轮 roofline](../assets/2609.34683-fig4-roofline.svg)

*Fig 4：多轮 serving roofline（LLaMA-3.1-8B@H100, C=1-80）。聊天始终带宽瓶颈（0.6× ridge），编码 agent 8.2× ridge 计算瓶颈。*

## 实验

### 饱和点上的 agentic gap（Table 4, H100, vLLM, prefix caching on）

| 模型 | 负载 | TTFT 中位 | TPOT | req/s |
|---|---|---|---|---|
| LLaMA-3.1-8B | 聊天 | 343ms | 9.4 | 13.5 |
| | 编码 agent | **11,719ms**（34×） | 227.3（24×） | 2.4（-82%） |
| | 终端 agent | 6,889ms | 197.2 | 3.0 |
| | 计算机操作 | 1,037ms | 22.8 | 6.5 |
| gpt-oss-20b | 聊天 | 267ms | 8.8 | 15.3 |
| | 编码 agent | 2,224ms | 17.1 | 16.5 |
| gpt-oss-120b | 聊天 | 224ms | 13.6 | 11.0 |
| | 编码 agent | 2,072ms | 25.5 | 13.6 |

LLaMA-3.1-8B 上编码 agent 的 TTFT 涨 34 倍、吞吐掉 82%——同一块 H100，负载形态决定生死。MoE 的 gpt-oss 系列差距温和些（TTFT ~8-9 倍）但依然显著。

### 缩放行为分化（Table 5, C=200 → 320）

63 组配对的聊天负载中位 **+11%**（33 组仍涨超 10%）——聊天还没到饱和，大批量继续受益。66 组 agentic 负载里 41 组已平台期、**15 组掉超 10%**（最惨 -76%）：KV 容量压力下，agentic 负载过饱和后不升反降。单工作点基准完全看不到这条分岔。

### Roofline 定位（Table 12/13/14）

- OI 分层：聊天 181（0.6× ridge，带宽瓶颈）→ 计算机操作 886（3.0×）→ 终端 1,809（6.1×）→ **编码 agent 2,409（8.2×，计算瓶颈）**，最高差 13 倍
- 逐阶段 OI gap：prefill/decode 差 **8×（聊天）到 28×（编码 agent）**——机制是滚雪球把 ISL 推大，prefill GEMM 越过 ridge，而 decode 的 OI 只由并发决定
- 逐组件：prefill 投影聚合 OI 2,500（占建模层延迟 81.8%），decode 投影 78；attention/elementwise 双阶段都带宽瓶颈
- 容量墙：LLaMA-3.1-8B 单 H100，512-token 上下文 C≈850 才满；32K 上下文 **C≈14 就撞墙**，128K 上下文 C≈3

### 最终结论：双重压力

Agentic 负载同时踩两个坑：**prefill 计算瓶颈 + decode 容量瓶颈**，正好在 roofline 两侧。作者据此论证这是 prefill-decode 分离（PDD）的天然候选——统一 serving 把计算瓶颈的 prefill 和带宽/容量瓶颈的 decode 挤在同一硬件上，分离部署应得可观收益。

## 复现要点

- **代码/数据**：论文称开源（HuggingFace 数据集 5 个配置 + 基准脚本），但匿名评审中链接未放出——待 camera-ready
- **硬件**：4 平台（H100-80G / A100-40G / RTX 3090 / 2080Ti），TP 1-8
- **软件**：vLLM v0.19.0/0.19.1 + SGLang v0.5.9，CUDA 12.8，NCU 2024.3.2
- **数据集构成**：3,197 条 sweep 行（trace_replay 2,932 + synthetic 265）+ 148,077 条 NCU kernel 记录 + 37 条逐层验证行
- **关键配置**：闭环并发扫描到饱和；bf16（gpt-oss 用 MXFP4 权重）；prefix caching 开启
- **最小复现路径**：拿 vLLM + SWE-Bench trace（公开），按 Table 2 的 ISL/OSL/轮数分布造合成负载，扫并发找饱和点，对比聊天负载的 TTFT 差距——核心结论（4.8×/34× gap）应该半天能复现个量级

## 启发与局限

这篇是知识库里 agentic serving 线（GraphTok → DLite → CarryOn → KV Residency）缺失的一块拼图：**把「agentic 负载不一样」从定性观察变成可测量的基准**。几个启发：

1. **负载形态决定硬件结论**。买卡/选引擎的评测如果还用聊天负载，对 agentic 部署就是刻舟求剑。355:1 的 ISL/OSL 比是编码 agent 的签名，评测集必须含这种形态
2. **饱和点测量应该成为惯例**。单工作点数字会被 KV 容量压力下的吞吐坍塌骗到（Table 5 的 -76%）
3. **OI/CF 解析分类不需要跑实验**——只依赖架构和 token 统计，新硬件发布时拿 spec sheet 就能预判瓶颈在哪侧，这个方法论比基准本身更有通用价值
4. **合成负载必须感知 prefix 结构**（B.1），否则 prefix cache 行为失真——任何想造 agentic 合成 trace 的人都该知道这个坑

局限作者自己说了三条：单机 TP 测量（没覆盖多机 PP 的跨节点通信）；多轮会话被 32K 上下文上限截断（滚雪球效应是**下界**，128K 部署会更夸张）；没有直接测服务端的 KV 驱逐/压缩/冷缓存重算。另有一条我自己的保留：trace 来源是 SWE-Bench/TerminalBench/OSWorld 的会话，这些是「跑基准的 agent」而不是生产 agent——生产环境的工具输出分布（日志、检索结果）可能更长更乱，真实 agentic gap 或许还要更大。

## 疑问清单

1. **饱和点 C\* 的判定鲁棒性如何？** |d(req/s)/dC|<ε 的 ε 取值、扫描步长，在不同硬件平台上会不会得出不同的 C\*？论文没给敏感性分析
2. **prefix-aware 合成的 1024-token 共享前缀是编码 agent 特有的吗？** OSWorld 的多模态工具输出（截图）转 token 后的前缀结构与 SWE-Bench 的代码上下文差异很大，一个统一前缀长度会不会在计算机操作负载上失真？
3. **MoE 的 gap 为什么显著更小？** gpt-oss-20b 编码 agent TTFT 只涨 8.3 倍（vs dense 的 34 倍）——是 MXFP4 权重让 prefill 带宽更宽松，还是 MoE 的稀疏激活天然适配高 ISL？论文没拆解
4. **PDD 收益预测能量化吗？** 论文论证了 agentic 是 PDD 候选但没给分离后的预估数字——用他们的 OI/CF 框架能不能直接算出分离部署的理论上限？

## 新学到的术语（同步到 glossary/terms.yaml）

- Snowballing effect（滚雪球效应）
- Operational Intensity / Capacity Footprint（OI/CF）
- Saturation-based measurement（饱和点测量）
- APC（automatic prefix caching）——已有 prefix caching 条目，此条为其 vLLM 实现名
