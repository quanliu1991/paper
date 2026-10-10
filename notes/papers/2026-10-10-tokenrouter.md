---
论文: TokenRouter: Efficient Serving System for Token-Level LLM Routing
arxiv: 2610.12242
日期: 2026-10-10
子方向: serving-system
状态: 精读完成
---

# TokenRouter: Efficient Serving System for Token-Level LLM Routing

> 清华 NICS 组。解决 token 级 LLM 路由（token-level routing）在现有 serving 系统上跑不起来的问题。

## 背景与动机

- LLM 路由已在生产广泛使用，但都是**粗粒度**（session/query 级）：一次请求只绑一个模型。
- 算法侧新趋势是 **token 级路由**：每个 token 都可切换模型。收益巨大——R2R 只把 5% 的 token 路由给 32B 模型（其余 1.5B 生成），就能追平 32B 质量；而 query 级路由要 40% 请求给大模型。
- 但 vLLM/SGLang 假设「一个请求始终在一个模型上」，token 级路由打破该假设，三大挑战：
  1. **步失同步（step desynchronization）**：不同模型每步延迟差异大，单批同步等待最慢者，快模型空转。
  2. **批准入延迟（batch admission delay）**：token 路由频繁换模型，请求常在目标模型正忙时到达，等下个批次入队，产生气泡、批碎片化。
  3. **实现复杂**：现有系统无 per-step 路由接口，硬改大代码库且要与 continuous batching / prefix caching 纠缠。

## 方法

核心设计原则：**request-centric programming, model-centric execution**——开发者只描述单请求视角的路由逻辑，运行时用模型中心的异步 subserver 高效执行。

三个机制：

1. **route-send-receive 编程接口**（开发者只写三个函数）：
   - `route(result)`：每步 decode 后调用，按 logits/hidden states 决定每个请求去哪个模型（0=本地继续，非 0=peer 索引）。
   - `send(req)`：委托时打包 PeerReq（请求 ID、peer 未见过的 token 后缀、位置锚点、状态）。
   - `receive(peer_req)`：收到 PeerReq 转本地格式继续解码（默认收全部 token，特殊算法可覆盖）。
   - 例：R-Stitch 在 SLM 侧用 token 熵 > τ 判断交给 LLM，并把不确定的 token 丢弃让 LLM 重新生成。

2. **解耦三环执行（decoupled tri-loop）+ handoff-resume**：
   每个 LLM 一个自治 subserver，跑三个解耦循环（client-server / decoding / inter-model），消除步失同步；handoff-resume 机制简化跨模型切换的状态转移。

3. **延迟批调度（delayed-batching scheduler）**：
   稍等一小段再入批，摊薄平均批准入延迟；最优等待超参由系统的**数学吞吐模型**推导（不是手调）。

## 实验（关键数字）

- 5 种路由算法（CITER/R2R/Co-LLM/R-Stitch/ME）、多负载与模型对上，解码吞吐比现有实现高 **2.01–64.15x**。
- 增益分解（并发 8）：纯工程优化（在官方 R2R 实现上）+1.71x，TokenRouter 整体 +2.76x。
- 严格 SLO 下吞吐比 R2R 高 **18.58x**——数学模型推导的调度超参在紧 SLO 下收益最大。
- 兼容性：对客户端是**单端点**，可 drop-in 替换单模型 serving。

## 复现要点

- **代码**：https://github.com/thu-nics/TokenRouter（开源）
- **数据集/负载**：论文用 5 种路由算法 × 多模型对（1.5B/7B/32B 级）；复现建议从 R-Stitch（熵阈值，无需训练 router）入手，模型对 Qwen2.5-1.5B + 7B。
- **关键超参**：delayed-batching 等待时长（论文用吞吐模型推导；复现可先扫 0/1/2/4ms 观察吞吐-SLO 曲线）。
- **最小复现路径**：clone → 起 SGLang 后端的两个 subserver → 跑 R-Stitch 示例 → bench 并发 8/16/32 的吞吐与 TTFT/TPOT。
- **观察指标**：吞吐、SLO 达标率（goodput）、模型间切换频率、批大小分布。

## 启发与局限

- **启发**：
  - 「算法-系统共同设计」范本：算法侧的 token 级路由理论收益，靠系统侧三招（异步 subserver / 延迟入批 / 吞吐模型调参）才兑现——这种「算法进展倒逼 serving 系统重构」的模式会反复出现（类比投机解码对系统的改造）。
  - request-centric 抽象把异步复杂性藏进 runtime，与 SGLang 的结构化生成控制流思路同源：**把策略留給开发者、把执行留给系统**。
  - 数学吞吐模型推导调度超参 > 手调，值得在其他 serving 场景复用。
- **局限**：
  - 路由信号（熵/置信度）依赖 logits，对 logits 被隐藏的 API 模型不适用。
  - 两模型为主（ME 扩展到多模型但实验有限）；跨节点（非单机多卡）场景未充分评估。
  - KV 状态跨模型不共享，handoff 只传 token 后缀——前缀缓存只在本模型内有效，长上下文跨模型切换的 KV 传输是潜在瓶颈。

## 新学到的术语

- token-level routing（token 级路由，已加入词汇表 learning）
- step desynchronization / batch admission delay（已加入 learning）
- R2R（Route-to-Reason，5% token 给大模型追平质量，已加入 learning）

## Q&A

### Q1（2026-10-10）：delayed-batching 的最优阈值 B* 具体怎么推导？为什么不直接手调一个经验值？

> 摘自论文 §4.3「Throughput-optimal threshold」（全文缓存 `.fulltext/2610.12242.txt`）：
>
> 推导方式是把路由过程建模为 **离散时间马尔可夫链（DTMC）**：给定路由算法、并发数 N、路由概率矩阵 P、每个 LLM 的单步解码延迟 L_i，模型推出吞吐关于阈值 B 的解析函数，搜索使吞吐最大的 B*（完整推导在附录 D）。
>
> 不能手调的原因是 B 存在严格的双向权衡：B 太小 → 批准入延迟大（token 路由下模型切换频繁、到达稀疏）；B 太大 → 请求困在队列、SLM 缺活干（starvation）。且最优值随负载/路由概率动态变化，经验值无法覆盖。实测该数学推导在紧 SLO 下收益最大（吞吐比 R2R 官方实现高 18.58x）。
>
> 关联：这呼应了 serving 领域「用排队论/马尔可夫模型做调度决策」的传统（如经典文献对 M/G/1 批处理的建模），值得在 notes/insights/ 里沉淀一篇「吞吐模型驱动的调度调参」主题笔记。
