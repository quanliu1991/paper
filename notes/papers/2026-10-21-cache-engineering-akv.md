---
论文: Cache Engineering for Agents
arxiv: 2610.28577
日期: 2026-10-21
子方向: kv-cache
状态: 精读完成
---

# Cache Engineering for Agents（AKV：让 agent 直接管理自己的 KV cache）

> 原文：[abs](https://arxiv.org/abs/2610.28577) · [HTML](https://arxiv.org/html/2610.28577v1) · 代码：[thu-nics/AKV](https://github.com/thu-nics/AKV)

## 背景与动机

agent 跑长任务时，对话历史像滚雪球一样越滚越长——每轮工具调用都往上下文里塞东西。KV cache 读取占了 API 成本的 82.4%（论文 Figure 14 实测）。现在的解决办法是「上下文工程」：到了长度阈值就把旧历史摘要掉。但这有个隐藏代价——你改了前面的文本，后面所有已缓存的 KV 全部作废，必须重算 re-prefill。摘要触发得早，重算成本高；触发得晚，信息挤爆上下文伤害准确率。这是个两难。

更根本的问题：为什么要在**文本层**动刀？agent 真正想控制的是**注意力能看到什么**。文本只是载体，KV cache 才是模型实际消费的东西。作者的核心洞察：直接在 cache 层操作——把不要的 KV 条目从注意力里排除掉，保留的条目原地复用，一行重算都不用。

![三种范式对比](../assets/2610.28577-fig1-context-vs-cache.svg)

（Figure 1：full-context 全保留 / context engineering 改文本重算 / cache engineering 只动 cache 不动文本。注意保留的 KV 里还残留着被丢弃历史的信息——这是 drop 的一个隐藏红利。）

## 方法

三个 cache 原语：

- `append(x)`：常规操作，新 token 的 KV 入 cache
- `drop(P)`：把选中位置的 KV 从**后续注意力**中排除——逻辑 token 序列不变、保留条目的位置编码不变
- `repos`：给保留的 key 重排位置编码（RoPE 旋转 K←R(q)R(p)⁻¹K，V 不动），并重置后续 append 的起始索引

`repos` 解决的是位置耗尽问题：drop 不减小逻辑位置索引，任务跑久了索引照样顶到模型上限；用 RoPE 旋转把保留 key 压缩到 0..r-1，不用重算。

**关键难点——cache 状态是历史依赖的**。同样保留 B、C 两个 token，C 的 KV 可能是「看着 A 算出来的」也可能是「没看 A 算出来的」，取决于 drop 发生在 append C 之前还是之后。所以**token 前缀不再唯一决定 cache 状态**，radix tree 的前缀匹配会错误复用不同操作历史下的状态——这直接打破了现有 serving 系统（vLLM/SGLang radix cache）的正确性假设。

**AKV serving 引擎**三件套：
1. **扩展 radix tree**：在 drop/repos 触发点插入 drop node / reposition node，前缀匹配同时比对 token 前缀和操作前缀；repos 的复用走「复制 + key 旋转」而非重算
2. **drop-aware 驱逐**：被 drop 的 KV 优先驱逐；驱逐只清数据保留树节点（placeholder），子孙仍可寻址
3. **segment-batch attention**：恢复缺失状态时把 query 按 drop/repos 边界切段，各段用各自的可见性和位置编码，**一次前向**恢复全部缺失状态（FFN 不切段，避免权重重复读取）

接口层面保持 stateless：请求里 messages 给完整逻辑序列，可选 cache 字段给操作序列（operate-after 语法），服务器内部管理一切状态。

## 实验

主策略非常朴素：**tool-response rolling drop**——保留最近 12 轮工具响应 + 全部推理消息的 KV，旧的滚动丢弃。三个模型（GPT-OSS-120B / MiniMax-M2.7 / MiroThinker-1.7-Mini）× 四个基准（BCP / GAIA-Text / SWE-Verified / xbench-DS）：

| 方法 | 平均通过率 | 平均成本 |
|---|---|---|
| Standard（96K 阈值摘要） | 基线 | 基线 |
| Text Engineering（48K 阈值） | −0.3~−8.7% | −7% |
| AKV rolling drop | **+1.3~+2.1%** | **−27.7%** |

成本降 27.7%（原 1 小时 4 角的活现在 3 角）的同时分数反而涨——因为 rolling drop 渐进丢弃，不像摘要那样在阈值处断崖式丢信息（48K~96K 区间 Text Engineering 准确率最低，正好卡在它的摘要阈值上）。

Serving 侧（SWE-Verified Top-80，8×A800，SGLang 基座）：
- 峰值吞吐：输入 1.53×、输出 1.18×（C=14 时输入 51837 vs 12767 tokens/s）
- P95 请求延迟 1.51× 加速（108.86s → 28.49s @C=14）；高并发下 Standard 因 KV 容量压力反复 re-prefill 严重退化，AKV 优势拉大
- decode 提速来源拆解：full-attention 时间 −59.8%（活动上下文变短，KV 读取和注意力计算都少了）

![吞吐对比](../assets/2610.28577-fig-throughput.svg)

两个加分项：RSI 自我改进 cache 策略再降 7.1% 成本；把 cache 管理暴露成工具（Cache-As-Tool）让 agent 自己决定何时丢什么，两个模型上拿到最高分（61.0% / 64.0%）。

![decode 延迟拆解](../assets/2610.28577-fig-decode-breakdown.svg)

## 复现要点

- 代码：https://github.com/thu-nics/AKV（基于 SGLang v0.5.20，Triton attention backend）
- 硬件：8×A800-80GB（prefill 4 + decode 4，TP4），BF16 权重
- 关键配置：KV page size = 1 token/page；chunked prefill 8192；retention K=12 轮工具响应；repos 阈值对齐 Standard 摘要阈值（96K）
- 最小复现路径：AKV 仓库 + GPT-OSS-120B + mini-SWE-agent 跑 SWE-Verified 前 100 任务，对比 Standard 摘要基线
- 注意：radix tree 的 drop node 逻辑是正确性关键，自己实现时容易在「同 token 前缀不同操作历史」上出错

## 启发与局限

- 「context engineering vs cache engineering」的框架提得很准：一个在符号层动刀（代价是 KV 失效），一个在状态层动刀（代价是 serving 复杂度）。这与 AgentPerfBench 的 snowballing effect 观察直接呼应——agent 负载的 KV 压力本质是每轮追加历史造成的，cache engineering 给了第一性解法
- drop 后保留 KV 仍携带被丢历史的信息（类似 attention sink / latent collaboration 的观察），说明 drop 未必丢信息——这是个值得深挖的现象
- 局限：只支持 full-attention 模型（linear attention 的 recurrent state 不适用，作者留给未来）；策略本身还是手工设计的 rolling drop 为主，RSI 改进幅度有限；upvotes 45（10-22 数据）说明社区已经注意到它
- 与 SideQuest/IntentKV/AgentKV 等 concurrent 工作的差异在 serving 集成：那些工作做 eviction 策略，AKV 做的是策略无关的操作接口 + 正确的跨请求复用

## 疑问清单

1. repos 的 key 旋转在长任务上累积多次后，数值误差会不会影响生成质量？（论文只说「有限精度变换可能引入舍入误差」，没给量化）
2. drop node 让 radix tree 分叉变多，树本身的内存与匹配开销在高并发多 agent 会话下如何扩展？
3. rolling drop K=12 是全局常数——不同任务（浏览 vs 编码）的最优 K 应该差很多，Cache-As-Tool 版本是否已经隐式解决了这个问题？

## 新学到的术语（同步到 glossary/terms.yaml）

- Cache Engineering（cache 工程）
- History Dependence（cache 状态的历史依赖）
- Segment-batch Attention（分段批量注意力）
- Drop-aware Eviction（drop 感知驱逐）
