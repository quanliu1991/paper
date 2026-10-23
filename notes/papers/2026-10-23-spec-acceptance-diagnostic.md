---
论文: Speculative Acceptance Does Not Decay with Position: A Full-Length Diagnostic on Long Chain-of-Thought with Independent Drafts
arxiv: 2610.30644
日期: 2026-10-23
子方向: speculative-decoding
状态: 精读完成
---

# 投机接受率不随位置衰减：1.78M 轮验证推翻一个行业叙事

> 原文：[abs](https://arxiv.org/abs/2610.30644)

## 背景与动机

行业里流传一个叙事：「CoT 越长，投机解码接受率越低」——Test-Time Speculation 报告 EAGLE-3/DFlash/PARD 等训练型 drafter 在 ~20K token 后接受长度趋近 1（等于没加速），DSpark、SharpDraft 等新设计都预设了这个「衰减」并针对性求解。

但作者戳穿了证据链的漏洞：**所有直接证据都来自「训练出来的 drafter」，而它们的离线训练序列远短于推理长度**——衰减可能纯粹是「长度外推失败」（训练-推理长度错配），不是位置本身的规律。文献自己也承认这个解释。缺的是一个干净对照：**没有训练长度错配的独立 draft-target 对，在长 CoT 上的接受率轨迹**——从没有人测过。

## 方法

纯测量+诊断工作，设计四个配置隔离变量：

- MATH-500 全部 500 题（不是采样），greedy 和 Leviathan sampling 两种解码
- 两个**独立** draft（都没在 target 输出上训练过）：同家族 DeepSeek-R1-Distill-Qwen-1.5B + 跨家族 Qwen2.5-1.5B-Instruct，target 是 DeepSeek-R1-Distill-Qwen-7B
- 共 **≈1.78M 轮验证**，每轮记录位置、draft token、target 预测、（采样模式下）双方完整分布
- **within-problem 配对检验**去掉题目难度构成偏差；隔离 greedy 模式下的「复读病」病理（重复生成虚高长位置接受率）

## 实验

- **核心结论**：排除复读病后，四个配置里接受率都**不随位置衰减**（greedy 0-8K、采样 0-12K 支持域内）；反而轨迹后半段显著略高于前半段（跨家族配置效应更大）
- **熵才是失败轴**：可见统计量（argmax 一致率）在采样模式下降解，但真实期望接受概率 α 不降——温度扫描直接分离两个统计量，衰减是 argmax 的「可见性伪影」
- 拒绝高精度集中在**反思触发词**（wait/however/check）上——决策点熵高，不是位置晚
- **干预证伪**：三臂 LoRA 轨迹对齐（uniform/reflection-marked/entropy-weighted）500 题上 MAL 零提升——轨迹拟合不是正确的对齐目标，应该直接优化接受判据本身

## 复现要点

- 无代码，但方法完全可复刻：DeepSeek 系模型 + MATH-500 + per-round 记录脚本；1.78M 轮的 7B×1.5B 推理量是主要成本
- 关键方法学礼物：**within-problem 配对检验**与**复读病隔离**应该成为后续所有接受率测量的标准操作——位置构成效应（难题先生成短轨迹提前退出）会系统性污染跨位置比较
- 「argmax 一致 ≠ 期望接受概率」的区分对所有采样模式投机解码评测都适用

## 启发与局限

- 这是对「长度外推失败」假说的补刀：训练型 drafter 的衰减是**训练问题**（离线短序列 vs 在线长序列），不是解码动力学的内在规律——修 drafter 训练数据长度比设计新解码结构更对症
- 与昨天 RCSD（10-22 收录：用推理时接受/拒绝序列构造偏好对做 RL）、D-PAL（分布级损失）方向一致且更彻底：既然拒绝集中在高熵反思点，接受判据导向的目标函数（而非轨迹级蒸馏）才是正道
- 与 RIFT（同日）互补：RIFT 修 draft 的 KV 腐化（记忆侧），本文修 draft 的对齐目标（训练侧），两者叠加空间大
- 局限：独立 draft 的绝对 MAL 本身不高（否则行业不会去训 drafter），「不衰减」不等于「够好」；只测了 12K 内，超长（100K+）域外未覆盖；单 target 家族

## 疑问清单

1. 反思触发词上的失败能否用「反思点旁路」解决——draft 遇到 wait/however 直接放弃起草、交还 target 自回归一步？（工程上零训练成本，文中三臂 LoRA 没试这条）
2. 训练型 drafter（EAGLE-3）在复读病隔离后的「真实衰减曲线」长什么样？本文只给了独立 draft 基线，补上这个对照才能彻底钉死长度外推解释
3. 跨家族配置「后半段更高」的效应比同家族大——是分布差异带来的低基数效应还是真实规律？

## 新学到的术语（同步到 glossary/terms.yaml）

- 长度外推失败（Length-Extrapolation Account）
- 可见性伪影（Argmax Visibility Artifact）
- 反思触发词（Reflection Trigger Tokens）
