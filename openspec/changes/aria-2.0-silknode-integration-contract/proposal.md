# aria-2.0-silknode-integration-contract — silknode 集成契约 (预留 Spec)

> **Level**: Minimal (Level 2 Spec — 仅 proposal.md, 无 tasks.md)
> **Status**: Draft (预留, 等待 US-022+ 消费)
> **Created**: 2026-04-14
> **Parent Story**: (待定, 预期 [US-022](../../../docs/requirements/user-stories/US-022.md) Layer 1 Hermes fork + Layer 2 容器, M0 Spike 结论后起草)
> **Source**: [r1-legal-memo.md v1.1](../../../aria-orchestrator/docs/r1-legal-memo.md) 第 5 段"v1.1 后续人工动作" 第 2-3 项
> **Upstream Decisions**: 产品负责人 2026-04-14 澄清 (记录于 Aria 主项目 feature/aria-2.0-m0-prerequisite 分支)
> **Type**: Cross-cutting architectural constraint (不是单一功能实现, 是多个下游 Spec 必须遵守的契约)

## Why

在 US-020 T1 Legal Memo (v1.1) 的收敛过程中, 产品负责人对 Aria 2.0 的两个关键合规假设做了澄清:

1. **silknode 不落地存储 issue/code 内容** — 这是 IS-3/IS-4 降级为"合规结论"的唯一依据
2. **Aria 2.0 业务范围不处理个人信息 / 国家重要数据** — 这是 IS-4 跨境数据流不触发中国数据出境义务的前提

这两个假设当前只在 Legal Memo 里以文字形式存在, 但**它们是多个下游 Spec 必须继承的硬约束**:

- **US-022 (Layer 1 Hermes)**: 状态机设计必须与 silknode 的 "no-storage" 接口契约对齐
- **US-023 (Layer 2 容器双 provider)**: GLM provider 切换逻辑必须保留 silknode no-storage 前提, 否则 fallback 路径可能引入存储
- **US-025 (防漂移 + 审计日志)**: 4 层防漂移机制必须能检测到 silknode 侧行为漂移 (例如未来加缓存)
- **CLAUDE.md / PRD v2.0**: 业务数据分类约定需显式写入, 作为方法论级约束

如果这两个假设在 M1-M6 开发过程中被**悄悄**违反 (例如某个工程师为了性能给 silknode 加 cache), Legal Memo v1.1 的整条合规结论链 (IS-3→IS-4→无需 DPA→无数据出境义务) 会失效, 触发 Memo 失效条件, 需要重新评估。

**为什么预留为独立 Spec 而不是写进 Legal Memo 本身**: Memo 是"评估产物", 生命周期随评估时点冻结; 约束是"执行产物", 生命周期随代码库演进。两者必须分离, 否则 Memo v1.1 的结论会被后续架构变更悄悄废除而无人察觉。

## What

### 契约 1: silknode "no-storage" 硬约定

**约束文本** (to be copied verbatim into downstream specs):

> **silknode 代理 (Luxeno 品牌) 在 Aria 2.0 架构中必须保持 "API 调用透传, 不落地存储" 的行为**:
>
> - **禁止**: 在 silknode 侧对 issue body / code diff / Aria prompt / GLM response 进行任何形式的持久化 (磁盘日志 / 内存缓存 > 单次请求生命周期 / 数据库存储 / 审计日志保留)
> - **允许**: 单次请求生命周期内的内存缓冲区 (用于协议转换 / 格式适配 / 错误重试)
> - **允许**: 指标级 meta 日志 (请求次数 / 延迟 / 错误码), 前提是不含 request/response payload 内容
> - **可追溯**: 若 silknode 新增任何落地行为, **必须**触发 r1-legal-memo v1.1 失效条件, 重新评估 IS-3/IS-4 并更新 Memo 至 v2.0+

**消费位置** (下游 Spec 必须包含此约束):

- US-022 (或其继任 Spec) Layer 1 Hermes 状态机设计段的 "外部依赖接口" 章节
- US-023 (或其继任 Spec) Layer 2 双 provider 切换逻辑的 "fallback 路径约束" 章节
- US-025 防漂移机制的 L4 审计日志检查项 (silknode 行为漂移检测)
- `standards/autonomous/layer-boundary-contract.md` (若创建, PRD v2.0 §关联文档 规划)

### 契约 2: Aria 2.0 业务数据分类约束

**约束文本** (to be copied verbatim into PRD / CLAUDE.md):

> **Aria 2.0 的业务数据范围**: 仅限于技术工单 (issue body) / 代码变更 (code diff) / 方法论描述 (Aria prompt)。
>
> - **不包含**: 个人身份信息 (PII) / 支付信息 / 医疗记录 / 中国《数据安全法》定义的"重要数据" / 涉及关键信息基础设施的运维数据
> - **若未来扩展** 至包含上述任一类别 → **必须**触发 r1-legal-memo v1.1 失效条件, 重新评估 IS-4 (跨境数据流合规性), 可能触发 DPA 签署或路径重构
> - **判定权**: 由 10CG Lab 产品负责人在 PRD 修订时判定分类归属; 工程师不得自行扩展业务数据范围

**消费位置**:

- `CLAUDE.md` 新增段落 (具体位置待 US-026 修订时定)
- `docs/requirements/prd-aria-v2.md` (可能的 patch, 作为业务约束写入"产品定位"或"目标用户"段)

### 契约 3: 失效条件联动 (治理机制)

本 Spec 与 r1-legal-memo 的生命周期**双向绑定**:

- 本 Spec 被修订 (例如 silknode 允许某种新行为) → 必须同步修订 r1-legal-memo (创建 v2.0)
- r1-legal-memo 失效 (例如 expires_at 到期 或 业务范围扩展) → 必须同步审查本 Spec 的约束是否仍然适用

**audit-engine 检测点** (M4 及之后 US-025 实施时纳入):

- `silknode_storage_check`: 静态扫描 silknode 代码库, 识别潜在持久化行为 (数据库连接 / 文件写入 / 缓存库初始化), 任一命中 → pre_merge block
- `business_data_classification_check`: 静态扫描 Aria 2.0 各 Skill 的输入来源, 识别是否处理了"禁止类别", 命中 → block

这些检测点的具体实现不在本 Spec 范围, 由 US-025 承接。本 Spec 仅声明约束存在。

## Impact

**直接影响**:

- US-022 / US-023 / US-025 起草时**必须**引用本 Spec, 复制"契约文本"到各自的约束章节
- US-020 T6 (M0 Report 起草) 时, 产品负责人签字包含对本 Spec 的隐式承诺 (已由 r1-legal-memo v1.1 第 5 段建议动作 #2 和 #3 锚定)

**不变更**:

- 本 Spec **不改变** 任何已有文件 (不是代码变更 Spec, 是契约声明)
- 不消耗 M0 工时 (96.5h 预算不受影响)

**治理影响**:

- Legal Memo 失效条件机制首次获得代码级锚点 (silknode 代码库扫描 + 业务数据分类扫描)
- 未来人员 rotation 或 LLM 会话中断后, 后继者能通过本 Spec 快速理解"为什么某些行为被禁止"

## Acceptance (本 Spec 自身的验收)

本 Spec 的存在目的是**被下游 Spec 引用**, 因此验收标准不是"实现功能", 而是"约束文本被下游消费":

- [ ] **当 US-022 起草时**: 其 proposal.md 包含本 Spec 的 "契约 1" 原文引用 (允许改写表述但不允许改变约束强度)
- [ ] **当 US-023 起草时**: 其 proposal.md 的 fallback 路径章节包含本 Spec 的 "契约 1"
- [ ] **当 US-025 起草时**: 其 tasks.md 包含 `silknode_storage_check` + `business_data_classification_check` 两项 audit 检测点实现任务
- [ ] **当 PRD v2.0 / CLAUDE.md 修订时** (预期 US-026): 业务数据分类约束 (契约 2) 原文写入

当以上 4 项全部满足 → 本 Spec 状态从 Draft → Complete, 归档到 `openspec/archive/{date}-aria-2.0-silknode-integration-contract/`。

## Out of Scope (本 Spec 不做什么)

- **不做**: 审计检测点的具体实现 (由 US-025 承接)
- **不做**: silknode 代码库的实际审计 (由未来某个 PR 在 US-022+ 执行时做)
- **不做**: 业务数据分类的细则列表 (例如"什么算商业机密") — 这是 legal counsel 职责
- **不做**: 对 silknode 现状的技术验证 — Memo v1.1 的结论建立在产品负责人的**声明**上, 而非代码审计

## References

- [r1-legal-memo.md v1.1](../../../aria-orchestrator/docs/r1-legal-memo.md) — 本 Spec 的源头依据
- [US-020](../../../docs/requirements/user-stories/US-020.md) — 前置 Story, 本 Spec 由 US-020 T1 产出
- [PRD v2.0](../../../docs/requirements/prd-aria-v2.md) §R1 / §非功能需求 — 合规与容器安全
- [standards/legal/scoped-memo-template.md](../../../standards/legal/scoped-memo-template.md) — Legal Memo 模板 (本 Spec 的上游治理产物)
- [brainstorm 决策](../../../.aria/decisions/2026-04-14-aria-2.0-us020-scope.md) — US-020 切片决策
- [Agent Team 4 轮收敛](../../../.aria/decisions/2026-04-14-us020-agent-team-review.md) — 治理机制定义

## 版本历史

| Version | Date | Changes |
|---------|------|---------|
| 0.1 (Draft) | 2026-04-14 | 初版, 预留给 US-022+ 消费 |
