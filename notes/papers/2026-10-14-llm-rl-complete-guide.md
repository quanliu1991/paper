---
论文: Reinforcement Learning for LLMs: The Complete Guide
链接: https://cameronrwolfe.substack.com/p/llm-rl
日期: 2026-10-14
子方向: training
状态: 精读完成（博客长文，全文已缓存 .fulltext/llm-rl-complete-guide.txt）
---

# Reinforcement Learning for LLMs: The Complete Guide

> 原文：[Substack · Cameron R. Wolfe](https://cameronrwolfe.substack.com/p/llm-rl)（2026-08-24 发布）

> 不是论文，是一篇按教科书标准写的 RL 综述长文：从 RL 第一性原理一路推到 2026 年的前沿（GSPO/DAPO/TIS/CISPO、agentic RL）。指令跟随、对齐、推理模型这三波浪潮的共同底座都是 RL，这篇把底座到塔尖一次性讲完。全文图片网络不通抓不到，关键图表按原文文字描述重绘。

## 背景与动机

RL 对 LLM 的意义容易被低估：它不是锦上添花的后训练步骤，而是三类关键能力的来源——指令跟随（InstructGPT 起）、对齐与安全、以及推理能力（DeepSeek-R1（用纯 RL 激励出推理能力的模型，不需要 SFT 冷启动的版本叫 R1-Zero）这波）。今天还没解决的问题——reasoning、知识工作、agent、token 效率、可靠性——主流路线仍然是 RL。

这篇文章的独特价值是把散落在十几个 deep dive 里的内容串成一条线：基础形式化 → 策略梯度全家桶 → GRPO 补丁生态 → 前沿议题，每节都带 PyTorch 伪代码。读它等于把 RL 后训练的「为什么」一次性补齐。

## 方法

### 先把 RL 的词翻译成 LLM 的词

RL 的原始设定是 agent 在环境里试错，做对了拿奖励。映射到 LLM 出奇地干净：

| RL 术语 | LLM 对应 |
|---|---|
| policy（策略，agent 的大脑） | 被训练的 LLM 本身 |
| 初始状态 | prompt |
| action | 一个 token（MDP 式）或整条 completion（bandit 式） |
| 状态 | prompt + 已生成的 token（转移是确定性的，就是拼接） |
| trajectory | 整条生成 |
| reward | 整条答案的对错分（outcome）或中间步骤的分（process） |

两种建模方式各有信徒：REINFORCE/RLOO 常用 bandit 式（整条回答算一个动作，答案对了整条加分），PPO 用 MDP 式（每个 token 一个动作，逐 token 算 advantage（优势函数：这个动作比该状态下平均预期好多少，`A = Q - V`））。reward 粒度上 outcome 是主流——答案对给 1 分——但信号稀疏，一整条推理只有最后一个数字告诉你对没对；process reward 能在中间步骤打分，credit assignment 更细但更难做。

奖励从哪来是另一条分岔线：

- **RLHF**（基于人类反馈的 RL）：先收集大量「同题两答案谁好」的偏好数据，训一个带回归头的 reward model 打分。灵活，但模型可能学会骗打分器。
- **RLVR**（可验证奖励的 RL）：数学题字符串比对答案、代码题跑单测。确定性打分，几乎没有 reward hacking（奖励作弊：模型学会的不是把题做对，而是让打分器给分——比如格式上蹭对答案）的空间，所以能撑起大规模训练。DeepSeek-R1-Zero 明确弃用神经 reward model 就是为了避开它。

训练循环就两步，反复交替：rollout（用当前模型采样一批答案并打分）→ policy update（按目标函数更新权重）。

### 三个公共零件：KL、importance ratio、advantage

后面所有算法的差异，基本都在这三个零件的用法上。

**KL 惩罚是缰绳**。优化目标 = 最大化奖励 − β·KL(当前策略 ‖ 参考策略)。没有它，模型会为了讨好打分器跑成一个不像自己的东西（胡言乱语刷分）。实现上有两条路：减进 reward（PPO 默认，算一次就固定）或加进 loss（GRPO 原版，梯度能流过）。精确算 KL 要比全词表分布，太贵；实践中用采样估计器——只看实际生成的那个 token 在两个模型下的 logprob 差。k1 = logprob 差（无偏但方差大，还能是负的）；k3 = exp(−logratio) − (−logratio) − 1（非负、方差更低，GRPO 选它）。值得注意的是脚注 5：reasoning 模型的大规模 RL 越来越不用 KL 了——训练目标就是要模型大变，锚死在参考模型上反而碍事。

**Importance ratio 是新旧策略的汇率**。一批 rollout 采样完之后策略更新了，旧数据在新策略下的概率要乘 `π_θ/π_old` 修正，这就是 importance sampling。PPO/GRPO 的 clip、TIS 的截断、GSPO 的序列级重构，全都围绕这个比值做文章。

**Advantage 是学习的信号**。直接拿 return 当信号方差太大；减去一个与动作无关的 baseline 不改变期望（EGLP 引理）但显著降方差。拿 value 函数当 baseline 就得到 advantage——直观理解是「这次比平时预期好多少」，好比看相对班级平均分而不是看绝对分数。

### VPG → REINFORCE：一切的地基

VPG 的形式一行说完：`∇ log π(a|s) × ψ`。ψ 是正的就把这个动作的概率往上推，负的往下压——像带实习生：说对的话多鼓励几句，说砸的话下次少说。整条流水线最核心的结构就是这个，后面所有算法都没跳出它。

REINFORCE 是 VPG 的 Monte Carlo 落地：采一批 rollout、算 return、乘 logprob、平均。严格 on-policy（数据和被优化策略同源），所以不需要 importance ratio。伪代码里最值得注意的细节：不是手写梯度，而是构造一个负梯度等于策略梯度的 loss 交给 autodiff——PPO/GRPO 全是这个套路。降方差靠轻量 baseline（批平均或滑动平均），不用 critic。

### PPO：critic + clip

REINFORCE 的 Monte Carlo 估计方差高，训练不稳。PPO 的两级跳：

1. **换更聪明的 baseline**：训一个 critic（价值模型，LLM 骨干 + 标量头，逐 token 预测预期回报）来估 V(s)，advantage = G − V(s)。critic 与 policy 同时训练（actor-critic 框架），用 MSE 回归 loss。critic 是 on-policy 的——它必须跟着 policy 一起变，这是它和 reward model（RL 期间冻结）的本质区别。
2. **允许数据复用但不许走太远**：TRPO 用 KL 硬约束（信任域）保证单调改进，但约束优化难解；PPO 把硬约束换成 clip——importance ratio 超出 `[1−ε, 1+ε]` 就掐梯度。取 clipped 和 unclipped 目标的最小值，是个悲观下界：动作概率朝有利方向动过头时梯度归零，朝不利方向动不设防。四种象限（A 正负 × ratio 高低）值得对着原文图过一遍，一句话版：**clip 只拦「锦上添花」，不拦「落井下石」**。

advantage 估计实践标配 GAE（广义优势估计：把 1 步到 N 步的 TD 残差估计按指数权重 λ 混在一起，在偏差和方差之间调旋钮，常用 λ=0.95）——短视估计偏差大方差小，长视反之，GAE 一锅加权平均。

PPO 全家福的代价是显存：policy、reference、critic、reward model 四个模型，其中两个在训练。bf16 下推理约 2GB/1B 参数，训练约 16GB/1B（梯度 + 优化器状态 + 激活）——反向传播峰值可达推理的 12×。Qwen-3-32B 光推理就 60-70GB。

### GRPO：扔掉 critic

DeepSeekMath 提出的动机很实在：critic 太贵了。GRPO 的替代方案是同一 prompt 采样 G 条 completion 组成一个组，组内 z-score 当 advantage：`(r_i − mean) / std`。好比同一道题让八个学生各写一版互相改卷——高于组平均的加分，低于的减分，不需要一个「标准预期」。序列级 advantage 广播到该 completion 的所有 token，但 loss 仍是 token 级、带 PPO 式 clip，KL（k3）挪进 loss。

代价是每个 prompt 要多采样（一个 completion 构造不出组内基线），rollout 侧多花钱换训练侧砍掉一整个待训练模型——省下的是最贵的那种显存。某种意义上 GRPO = RLOO 的组基线 + PPO 的 clip 外壳。

### GRPO++：规模化的补丁

R1 开源后大家复现不动，补丁潮涌现。共同点：不重造轮子，只修细节——而细节在规模上就是生死。

- **GSPO**（Qwen3 采用）：importance ratio 从 token 级改序列级——token 概率比的几何平均（log 域求和）。长序列上 token 级 ratio 方差大、单个 token 能主导 loss，序列级 clip 对长 completion 和大 MoE 稳得多。
- **DAPO**：一组四件套。clip-higher（上限 ε=0.28 > 下限 0.2）防 entropy collapse——普通 clip 会压制低概率的探索性 token，模型越来越确定、越来越死板；dynamic sampling 把全对/全错的组（advantage 全零、白占 batch）过滤掉继续采样到满批；token 级 loss 聚合（原来的「先序列内平均再批平均」让长回答的每个 token 权重变小，模型倾向于啰嗦）；overlong filtering + 软长度惩罚（超长截断的答案分数不可靠，别硬罚）。
- **Dr. GRPO**：两处去偏。序列 loss 除以固定常数 MAX_TOKENS 而不是序列长度（解耦长度与梯度贡献）；advantage 去掉 std 分母（std 对「太难/太易」的题趋零，advantage 爆炸）。副产品是回答不再人为冗长。
- **TIS**：修的是 infra 引擎不一致。现代 RL 训练里 rollout 走 vLLM/SGLang（还常 int8/fp8 低精度），更新走 FSDP/DeepSpeed——同一份权重，两个引擎吐出的 token 概率有系统性差异，且很难靠对齐实现消掉。TIS 在梯度表达式里乘一个 learner/sampler 概率比并截断上限 ρ，一行修正换来稳定性大改善，已被 verl 和 OpenInstruct 采纳。注意它和 PPO ratio 的分工：PPO ratio 管策略过期，TIS ratio 管引擎差异——即使权重完全相同它也存在。
- **CISPO**（MiniMax-M1）：发现 PPO 式 clip 有个隐性伤害——推理轨迹里的「分叉 token」（"wait"、"aha" 这类反思词）在基座里概率低、第一次更新后概率暴涨触发 clip，从此梯度归零，而它们恰恰是稳定 entropy 和可扩展 RL 的关键。M1 每批做 16 次更新，被 mask 的关键 token 损失更大。CISPO 把 clip 后的 ratio 变成 stop-gradient 权重：贡献封顶但不归零。

### 关键图表

原文图（网络不通无法下载，按文中描述重绘，锚点可对照原文）：

**算法演进总表**（综合自「From Policy Gradients to Frontier RL」总结节）：

| 算法 | advantage 来源 | 数据复用 | KL 位置 | 关键取舍 |
|---|---|---|---|---|
| REINFORCE | return − 批平均 baseline | 无（严格 on-policy） | 可选，reward | 最简单，方差高 |
| PPO | critic 估 V，GAE | 有，clip 保护 | reward（默认） | 稳但 4 模型 2 训练，贵 |
| GRPO | 组内 z-score | 有，PPO 式 clip | loss（k3） | 扔 critic，rollout 多采样换训练省显存 |
| GSPO | 同 GRPO | 序列级 ratio+clip | 同 GRPO | 长 MoE 稳（Qwen3 用） |
| DAPO | 同 GRPO | 同 + dynamic sampling | 同 GRPO | 反 entropy collapse / 长度偏 / 空组 |
| Dr. GRPO | 均值差（无 std） | 同 GRPO | 同 GRPO | 去长度偏 + 难度偏，回答更省 token |
| TIS | 任意 | × 引擎修正比 ρ | — | 修 vLLM↔DeepSpeed 概率差 |
| CISPO | REINFORCE 式 | clip 后 stop-grad 权重 | — | 稀有反思 token 不丢梯度 |

**RL 训练系统的双引擎结构**（TIS 节描述重绘）：

```
            ┌─────────────────┐
   prompts →│ 推理引擎 (sampler) │→ rollouts + 打分
            │ vLLM / SGLang     │   （int8/fp8，占大头算力）
            └────────┬────────┘
                     │ stale / 概率不一致 ← TIS 修正点
                     ▼
            ┌─────────────────┐
            │ 训练引擎 (learner) │→ policy updates
            │ FSDP / DeepSpeed │   （PPO/GRPO + clip）
            └────────┬────────┘
                     │ 权重同步（refit）
                     └────────→ 回到 sampler
```

> 大规模 RL 的算力大头在 rollout 一侧——这也是 RL 训练和推理 Infra 的交汇点：引擎概率一致性、权重同步速度（见归档里 NeMo-DCR 的 bit-exact delta 压缩 refit）、异步 stale 数据处理，全是 serving 侧问题的变形。

## 值得记住的数字

（综述文没有实验节，摘文中散落的关键数字）

- **显存**：bf16 推理 ~2GB/1B 参数，训练 ~16GB/1B；反传峰值可达推理的 12×；Qwen-3-32B 推理 60-70GB。
- **超参惯例**：clip ε=0.2（DAPO 上限 0.28）；GAE λ=0.95；LLM 后训练通常有限视界 + γ=1；PPO/GRPO 每批 2-4 次更新（MiniMax-M1 例外，16 次——这正是 CISPO 的动机）。
- **KL 趋势**：reasoning 模型的大规模 RL 越来越不用 KL 惩罚（脚注 5）。
- **on-policy 的价值**：on-policy RL 顺序学新任务接近多任务训练的性能且基本不遗忘旧能力；SFT 学新忘旧。抗遗忘的机制解释是 on-policy 训练的分布漂移（对初始模型的 KL）天然小。

## 延伸阅读路径

（无代码可复现，给深挖路线；文中每节都链到对应的 deep dive）

1. 基础+伪代码跟写：本文 + [RLHF Book (Nathan Lambert)](https://rlhfbook.com/) 对照读
2. PPO 细节：作者系列《PPO for LLMs: A Guide for Normal People》（2025-10-27）
3. GRPO 全家桶：《GRPO++: Tricks for Making RL Actually Work》（2026-01-05）
4. 一手论文：TRPO (1506.02438 → 实为 arXiv:1502.05477)、PPO (1707.06347)、GAE (1506.02438)、DeepSeekMath/GRPO (2402.03300)、DeepSeek-R1 (2501.12948)、GSPO (2507.18071)、DAPO (2503.14476)、Dr. GRPO (2503.20783)、MiniMax-M1 (2506.13585)
5. TIS 是博客形式：Feng Yao, "Your efficient RL framework secretly brings you off-policy rl training"（2025-08）

## 启发与局限

- **算法演进的真实逻辑是「约束的迁移」**：TRPO 把约束放 KL 上，PPO 挪到 clip，GRPO 把约束的承担者从 critic 换成组基线，DAPO/Dr. GRPO 修约束的副作用（entropy、长度、难度），TIS/CISPO 修约束的失效场景（引擎差、稀有 token）。看懂这条线，新算法出来只需要问「它把哪个约束挪到哪了」。
- **对推理 Infra 视角最有价值的是 TIS 一节**：它把「同一权重、不同引擎、不同精度 → token 概率不一致」这个 serving 工程问题抬成了训练正确性问题。凡是做 RL 训练系统的人（rollout 集群、refit、混合精度推理）都该知道这个坑。反过来，RL 训练系统对推理引擎的需求（低精度高吞吐 rollout + 概率可对齐）是 serving 方向的长期需求源。
- **reward 设计的分寸**：RLVR 因为防作弊才撑得起规模——这个因果（不是「可验证所以方便」，而是「不可被骗所以敢放大规模」）值得记住。rubric-based reward（给开放任务生成 prompt 专属的评分清单，LLM judge 逐条打分再聚合）是把它推广到写作/科研这类不可验证域的当前主流尝试。
- 局限：本文是 2026-08 的快照，agentic RL 一节只给了模式清单（mask 环境token、异步、环境编排、process reward）没有深入；多轮/工具调用场景的 credit assignment 仍是开放问题。另外全文以 DeepSeek 系谱为主轴，OpenAI 系（如新的 online DPO 变体）着墨少。

## 疑问清单

1. TIS 的截断上限 ρ 怎么选？token 级和序列级 TIS 的 bias-variance 拐点在什么序列长度/模型规模上反转？文中只说「没有明显赢家」。
2. DAPO 的 dynamic sampling 在训练早期（模型弱、全错组占比高）会不会把采样成本推到不可接受？过滤比例随训练进程的曲线文中没给。
3. on-policy RL 抗遗忘的 KL 解释（分布漂移小所以不忘）与 reasoning 模型大规模 RL 弃用 KL 惩罚的趋势是否矛盾——不用缰绳之后，长程 RL 训练的分布漂移怎么控制？

## 新学到的术语

- **RLHF**（learning）：基于人类反馈的 RL，偏好数据训 reward model 打分；灵活但可被 reward hacking
- **RLVR**（learning）：可验证奖励的 RL，规则验证器（答案匹配/单测）打分，防作弊支撑大规模训练
- **Advantage（优势函数）**（learning）：`A = Q − V`，动作比状态平均预期好多少；策略梯度的核心学习信号
- **GAE（广义优势估计）**（learning）：不同步数的 TD 优势估计按 λ 指数加权混合，调偏差-方差，常用 λ=0.95
- **Reward Hacking（奖励作弊）**（learning）：模型学会骗打分器而非把任务做对；神经 reward model 的固有风险
- **Clip（PPO/GRPO 截断）**（learning）：importance ratio 限制在 `[1−ε, 1+ε]`，拦「锦上添花」不拦「落井下石」的悲观下界
- **GSPO**（learning）：序列级（几何平均）importance ratio + clip 的 GRPO 变体，Qwen3 训练采用，长序列/大 MoE 更稳
- **DAPO**（learning）：GRPO 补丁套餐——clip-higher、dynamic sampling、token 级聚合、overlong filtering
- **TIS（截断重要性采样）**（learning）：修训练引擎与推理引擎 token 概率不一致的 importance 修正，verl/OpenInstruct 已内置
- **CISPO**（learning）：clip 后 ratio 做 stop-gradient 权重而非梯度归零，保护 "wait"/"aha" 等稀有反思 token，MiniMax-M1 采用
