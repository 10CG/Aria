# aria-2.0-m0-prerequisite — Aria 2.0 M0 前置验证与架构定稿

> **Level**: Full (Level 3 Spec)
> **Status**: Draft
> **Created**: 2026-04-14
> **Parent Story**: [US-020](../../../docs/requirements/user-stories/US-020.md)
> **Target Version**: v2.0.0-m0
> **Related Spec**: [aria-2.0-m0-spike-hermes](../../archive/2026-04-16-aria-2.0-m0-spike-hermes/proposal.md) (Spike 专项 Spec, 本 Spec 产出依赖其结论回填 AD3)
> **Source**: PRD v2.0 §M0 + Agent Team 4 轮收敛 ([review log](../../../.aria/decisions/2026-04-14-us020-agent-team-review.md))

## Why

PRD v2.0 估算 ~750h / 30 周, 核心架构基于若干未实证假设 (A1 headless plugin / A3 NFS / A5 Hermes rebase / R1 合规). 沉没成本风险: 若假设在 M2-M6 才暴露, 数百 h 需返工。

M0 的存在 = 把假设验证压到 2 周可控窗口内, 让产品负责人基于**量化数据**作出 Go/No-Go 决议。Agent Team 4 轮评审 (2 讨论组 / 1 挑战组) 后 M0 工时从 PRD 初估 80h 扩展至 96.5h, 新增的 16.5h 均为可证伪性补齐 (cloc 协议 / license 扫描 / md5 校验 / 受限范围 Legal Memo / GLM smoke 二值化 / Spike 量化阈值)。

## What

### 交付物

1. **5 项关键假设验证**
   - A1 headless `claude -p` 加载 aria-plugin (T3)
   - A3 Aether NFS + Nomad bind mount (T2)
   - R1 受限范围 Legal Memo 5 项 (T1)
   - R9 GLM 5.1 ToS 状态章节 (T1 产出 → M0 Report)
   - R10 Aether 节点归属 (T1, 条件性)

2. **AD1-AD12 架构决策收敛**
   - `aria-orchestrator/docs/architecture-decisions.md` 完整版, 含 alternatives considered
   - AD3 (Hermes fork vs 自研) 由 Spike Spec 结论回填
   - R7 (Nomad meta 64KB) 作为 M1 Layer 1→2 协议硬约定写入

3. **M0 Report + handoff schema**
   - `aria-orchestrator/docs/m0-report.md` — 产品负责人裁决依据
   - `m0-handoff.yaml` schema v1.1 (12 字段, 见 US-020 §D)
   - R9 三态签字章节

4. **治理产物**
   - `standards/legal/scoped-memo-template.md` (新增, Legal Memo 通用模板)
   - Dockerfile 构建时门控 + README WARNING block (R4-D8)
   - fixture 合成模板 `aria-plugin-benchmarks/ab-suite/glm-smoke/templates/*.j2.md` + `REVIEW.md` owner 签字 (per AD-M0-9, 1 人 + AI 场景下角色合并)

### 架构决策

| ID | 决策 | 依据 |
|---|---|---|
| **AD-M0-1** | T1 作为 Day 0-1 前置闸门 | Agent Team R1 tech-lead 建议 + R2-D2 状态机 |
| **AD-M0-2** | T1 受限范围 Legal Memo 5 项 | Round 1-4 legal-advisor 反对收敛 |
| **AD-M0-3** | Spike Report 主位置 OpenSpec 路径 | R2-D7 主从关系裁决 |
| **AD-M0-4** | 维持 PRD Go/No-Go 二元 + 平行 PRD patch | R2-D1 knowledge-manager 方案 vs tech-lead 前置修订方案 |
| **AD-M0-5** | `m0-handoff.yaml` schema 锁定 12 字段 | R4-D3 (补 glm_smoke_passed + image_sha256) |
| **AD-M0-6** | 签字统一表述 (audit trail, 非法律豁免) | R4-D7 legal 诉求 |
| **AD-M0-7** | orchestrator 裁决 = 推荐 + 24h 确认 + silent-approval | R4-D4 收回独立裁决权 |

### 非目标 (Out of Scope)

- Layer 1 状态机的具体实现 (US-022)
- Layer 2 双 provider 切换 (US-023)
- PRD §关联文档中其他 6 个架构 doc 的起草 (M1+)
- `standards/autonomous/` 目录骨架 (推迟 US-026)
- CLAUDE.md 修订正式提交 (仅 M0 产草案, 实施 US-026)

## Impact

**直接影响**:
- US-021 (M1 MVP) 的启动硬依赖本 Spec 的 Go 决议 + `prd_patch_pr` 状态
- PRD v2.0 §M0 Exit Criteria 在本 Spec 完成后触发产品负责人裁决
- CLAUDE.md 草案产出, US-026 直接消费

**间接影响**:
- 若 Spike 结论反转 AD3 → US-022 (M2) 实现路径变更
- 若 T1 升级邮件确认 → M0 时间线延后 (timebox ≤5 工作日)
- R9 pending 态触发产品负责人显式签字, audit-engine pre_merge 硬阻断机制首次应用

**Release Coupling**:
- 本 Spec 与 `aria-2.0-m0-spike-hermes` 是**并行执行, 串行归档**
- Spike Spec 先归档 (产出 Report) → 本 Spec 回填 AD3 → 本 Spec 归档
- 两 Spec 共享 `m0-handoff.yaml` schema 作为机读契约

## Acceptance Criteria

见 [US-020.md §验收标准 A/B/C/D](../../../docs/requirements/user-stories/US-020.md#验收标准-prd-m0-exit-criteria--agent-team-收敛补齐). 本 Spec 的 AC 等同 US-020 AC 但以 M0 交付物为粒度。

## 约束

- **工时硬边界**: 96.5h (Core 86.5h + Buffer 10h), 超 115h 触发 R8 评估
- **时间硬边界**: 2 weeks wall-clock, 超 3 weeks 自动 No-Go 复议
- **T4 触发阈值**: 实测 > 60h 启动评估, > 72h 强制终止 Spike
- **T3 触发阈值**: 实测 > 16h 触发 A1 失败评估
- **T1 hard precondition**: T1 完成前 T3/T4 不得启动; T1 升级邮件确认 → T3/T4 hold 至 ≤5 工作日

## References

- PRD: [docs/requirements/prd-aria-v2.md](../../../docs/requirements/prd-aria-v2.md)
- US-020: [docs/requirements/user-stories/US-020.md](../../../docs/requirements/user-stories/US-020.md)
- Brainstorm 决策: [.aria/decisions/2026-04-14-aria-2.0-us020-scope.md](../../../.aria/decisions/2026-04-14-aria-2.0-us020-scope.md)
- Agent Team 收敛: [.aria/decisions/2026-04-14-us020-agent-team-review.md](../../../.aria/decisions/2026-04-14-us020-agent-team-review.md)
- Spike Spec: [../../archive/2026-04-16-aria-2.0-m0-spike-hermes/proposal.md](../../archive/2026-04-16-aria-2.0-m0-spike-hermes/proposal.md)
