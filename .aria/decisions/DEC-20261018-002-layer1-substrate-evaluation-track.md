# 决策: DEC-20261018-002 — Layer 1 底座评估轨立项 (Hermes vs pi durable 等)

> **日期**: 2026-10-18 | **模式**: problem (与 DEC-20261018-001 同场 brainstorm 衍生)
> **参与者**: owner (simonfish) 提出并裁定立项 | **状态**: Confirmed (立项记录, **不预置结论**)

## 背景

owner 在 issue-ops 设计讨论 (DEC-20261018-001) 中提出: 现役 Layer 1 底座 Hermes 可能已非最新最优, **pi durable 是当前关注的更好 bot 底座候选**; 且 issue-ops 能力族的产品定位本质是对 aria-runner 的能力面升级。同场裁定已确保: issue-groomer 等动词刻意底座中立 (harness-agnostic 脚本核 + JSON 契约), reply 两档拆分使「便宜底座先跑 ops 面」成为可竞争结构。本 DEC 仅记录**评估轨立项**事实与框架, 评估结论以未来新 DEC 落地。

## 约束条件

| 类型 | 约束 | 影响 |
|------|------|------|
| 诚实边界 | 本 session 对 pi durable **无一手了解** (首次从 owner 处得知), 未做任何实测 | 本 DEC 不含对 pi durable 的任何能力断言; 候选地位仅记录 owner 关注 |
| 架构 | Layer 1 现役栈 = Hermes + Luxeno-routed glm-4.5-air (AD1-AD12 owner 批准) | 换底座 = AD 级架构决策修订, 须新 DEC + owner 裁定, 非本 DEC 范围 |
| 时机 | M6 在制 (Blocker 3 卡 4 owner/infra 门; Blocker 4 Luxeno 延迟) | 评估轨与 M6 在制轨**互不阻塞**; 评估结论不追溯影响已批 AD 的在制执行 |
| 解耦 | DEC-20261018-001 (issue-groomer) 零底座依赖 | 两轨独立推进, 评估不阻塞 groomer MVP |

## 考虑的方案

| 方案 | 描述 | 状态 |
|------|------|------|
| A. 不评估, 维持 Hermes | 零成本, 但放弃 owner 关注的更优底座可能 | 否决 (owner 明确关注 pi durable) |
| B. 直接换底座 | 跳过评估 | 否决 (AD 级决策须证据先行; 且 pi durable 无一手评估) |
| **C. 立项评估轨** | 判据先行, 产出对比证据, 结论另立 DEC | **选定** |

## 最终选择

**方案 C**。评估框架 (草案, 评估时细化):

1. **评估维度**: durable execution 语义与可靠性 · 多 harness 适配成本 (能否直接调 aria 脚本核吃 JSON 契约 — DEC-001 的可移植面即测试面) · 与 Layer L coordination (claim/ref, phase1_gate) 接驳 · 迁移面与共存期设计 (Hermes 在役期间双跑? 灰度?) · 成本模型 (接 M6 cost-model-telemetry 维度) · 维护活跃度与社区。
2. **试点面**: 优先 ops-tier 动词 (issue-ops 的轻档: 收录告知/打标) — 低风险可先行, 不押注 dev-tier。
3. **产出**: 对比证据 + 结论 DEC (含 AD 修订案) → owner 裁定。
4. **执行主体**: 待 owner 指派/排期 (本 DEC 不指定)。

## 理由

1. 底座选择是 runtime 层最高杠杆决策之一, 值得显式评估轨而非顺带决定;
2. DEC-001 的底座中立设计使评估成本显著降低 (契约已稳定, 换底座不返工能力面);
3. 立项记录防止「关注了但没排期」的静默丢失 (owner 原话: 先记录这个事情)。

## 风险与缓解

| 风险 | 缓解 |
|------|------|
| 评估轨长期悬置无结论 | 评估框架已定; 里程碑式推进 (维度清单→试点→结论 DEC) |
| 与 M6/M7 时机门纠缠 | 本 DEC 显式解耦声明; 评估结论影响的是 M7+ 的 fleet 执行主体, 不影响 M6 在制 |
| pi durable 信息面变化 | 评估时重做一手调研, 本 DEC 不固化其能力画像 |
