---
论文: HAWK: Heterogeneity-Aware KV Cache Transfer for Efficient GPU-NPU Phase-Disaggregated LLM Inference
arxiv: 2610.29873
日期: 2026-10-21
子方向: serving-system
状态: 精读完成
---

# HAWK：GPU 干 prefill、NPU 干 decode，KV cache 跨芯片搬家不减速

> 原文：[abs](https://arxiv.org/abs/2610.29873) · 代码：作者计划开源（论文声明）

## 背景与动机

prefill 和 decode 对硬件的要求天生不对称：prefill 是大矩阵乘（GEMM），GPU tensor core 吃满（实测利用率 ~93%）；decode 是逐 token 的矩阵向量乘（GEMV），GPU tensor core 利用率掉到 ~36%，而功耗几乎不掉——GPU 跑 decode 是「烧着训练的电干着轻量的活」。

NPU 恰好反过来。Tenstorrent p150a 这类数据流架构在 decode 时少核高频（FFN 只用 8/64 核但挑离 DRAM 近的核），核利用率 79-81%（GPU 只有 12-13%），单位功耗和单位成本的 decode 吞吐分别是 GPU 的 1.39× 和 5.88×。于是想法很自然：**GPU 做 prefill、NPU 做 decode 的异构 phase disaggregation**——每种芯片干自己最擅长的事。

卡脖子的是 KV cache 搬家。GPU prefill 算完的 KV 要送到 NPU 去 decode，但两边的通信栈不通（NVIDIA 有 NIXL，NPU 各玩各的）、**张量内存布局不同**（GPU 行/列主序虚拟连续 vs NPU 按 tile 切块散到多个 DRAM 通道）。走 host 中转要 8.91× 于 GPU 直连的延迟；硬用连续 RDMA buffer 接 NPU，通道间内存失衡直接 OOM（作者实测这个 naive 方案跑不起来）。

## 方法

HAWK 三步走：

1. **打通 RDMA 路径**：GPU 侧用现成的 nvidia-peermem，NPU 侧给 Tenstorrent 驱动写一个 peer memory client（npu_acquire/get_pages/dma_map 五个回调），两边挂到同一个 Linux RDMA 栈（libibverbs）上，NIC 直访设备内存不经 host
2. **布局感知的 RDMA buffer**：NPU 侧不再用一个大连续 buffer，而是**每个 DRAM 通道一个连续 buffer**，恰好拼出目标张量布局——数据落地即可用，零重排；通道数通常 ≤10，管理开销可控
3. **传输感知的张量变换**：GPU 侧发送前先把张量重排成 `[N_npu_channel, -1, tile_chunk]` 形状——同一通道的数据在源端就攒成大块，RDMA 请求少而大；剩余的布局对齐在传输过程中自然完成。变换放在 prefill 侧做，因为 prefill 显存带宽有富余

类比：搬家不是把家具一股脑扔门口再重组（host 中转），也不是让每件家具单独跑一趟（naive 逐块映射），而是**出发前就按新房间的柜子打包、到货直接入柜**。

## 实验

硬件：4×A100 PCIe（prefill）+ 4×Tenstorrent p150a（decode），200Gbps HDR InfiniBand 互联，vLLM v0.10.0 + Mooncake Transfer Engine，Llama 3.1 70B TP4。

- **传输延迟**：KV 传输 10MB~1.28GB，GN-HAWK 与 GPU-GPU 直连（GG-Direct）差距 <1%；比 host 中转快最多 27.69×（10MB 时差距最大，实际负载 KV 通常 >10MB）
- **在线服务**：Chatbot/Summarization 两负载，90% SLO 达成点处请求速率差距仅 2.90%/5.90%；decode 吞吐差距 0.48%/7.88%
- **效率**（这是重点）：功耗效率 1.26×（67.09 → 84.48 tokens/s/kW），成本效率 **1.72×**（1.19 → 2.05 tokens/s/$1K）。对比 H100 做 decode 的 GGH-Direct：吞吐差 6.5%，但成本效率 2.73-2.76×——p150a 一块约 $1.4K，H100 市价十几倍

关键表格（Table 1）：prefill GPU 比 NPU 快 2.52×，decode 只快 1.16×，而 NPU 的 decode 功耗/成本效率反超 1.39×/5.88×——异构分工的收益来源说得非常清楚。

## 复现要点

- 硬件门槛高：需要 A100 + Tenstorrent p150a + ConnectX-6 的实机；p150a 是目前唯一软件栈开放到能改驱动的 NPU
- 软件：vLLM v0.10.0 + Tenstorrent LLM stack 插件 + nvidia-peermem + tt-kmd v2.5.0（NPU peer memory 是自己加的）
- 负载：ShareGPT（Chatbot）与 LongBench（Summarization），SLO 2000/200ms 与 15000/200ms（MLPerf 口径）
- 若无 Tenstorrent 硬件，可复现其 profiling 部分（Nsight Compute 看 prefill/decode 的 tensor core 利用率差异），验证动机章节

## 启发与局限

- Phase disaggregation 从「不同 GPU 分工」扩展到「不同芯片分工」，逻辑顺滑；真正的一手贡献是**张量布局感知的 RDMA buffer 分配**——这个思路对任何「跨设备搬张量」的场景（包括 NPU-NPU、跨云）都适用
- NPU decode 的能效数字（5.88× 成本效率）建立在 p150a 的 $1.4K 定价上，量产供货和软件成熟度是另一回事；Summarization 高负载下 TPOT 提前触 SLO（0.60 vs 0.65 req/s）说明 decode 性能差距在大 batch 下才被追平
- 与 10-18 Tandem（手机 NPU agent serving）参照：Tandem 是单机 SoC 内 CPU/NPU 协同，HAWK 是跨节点数据中心级——NPU 上桌面的路线正在从两端逼近
- 只测了 Llama 70B（Tenstorrent 软件栈模型绑定限制），MoE/MLA 模型的表现未知；MLA 的压缩 KV 传输量更小，对 HAWK 更有利

## 疑问清单

1. 每 DRAM 通道一个 buffer 的设计在 KV 持续增长（decode 期间逐 token 追加）时如何扩容——是预留还是重新分配？
2. 第一 token（首 token 整数）之外的 KV 增量传输（decode 过程中新 KV 要不要回流 GPU 做前后缀共享）论文没展开
3. p150a 32GB 内存对 70B 模型 TP4 后的 KV 容量上限是多少——成本效率优势在多长上下文下仍然成立？

## 新学到的术语（同步到 glossary/terms.yaml）

- GEMV 瓶颈（decode 的矩阵向量乘特性）
- Tensor Layout（设备特定张量内存布局）
- Peer Memory Client（把设备内存暴露给 RDMA 的驱动组件）
