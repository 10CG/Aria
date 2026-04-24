---
checkpoint: pre_merge
round: 2
timestamp: "2026-04-24T00:20Z"
spec: state-scanner-mechanical-enforcement
pr_main: https://forgejo.10cg.pub/10CG/Aria/pulls/33
pr_submodule: https://forgejo.10cg.pub/10CG/aria-plugin/pulls/20
verdict_distribution:
  MERGE_WITH_REVISIONS: 2
  conditional_pass: 2
anchor_alignment_distribution:
  full: 4
drift_guard_distribution:
  stayed_on_anchor_true: 4
  scope_expansion_false: 4
r1_revision_acceptance:
  R1-I3_cli_exclusive: 4_accepted
  R1-I4_uncommitted_count_dedup: 4_accepted
  R1-I5_normalize_status_lifecycle: 4_accepted
  R1-I6_audit_bool_parse: 3_accepted_1_insufficient
  R1-I7_extract_status_heading: 4_accepted
  R1-C5_schema_stub: 4_accepted
  R1-M1_tasks_checkbox_sync: 4_accepted
  R1-C6_revisions_divergence_doc: 4_accepted
converged: false
---

# Round 2 pre_merge Aggregated Findings

## Drift Guard (4/4 一致)

- r1_revisions_stayed_on_anchor: **true** (all 4 agents)
- scope_expansion_detected: **false** (all 4 agents)
- Anchor alignment: **full** (4/4)

## R1 Tier 1 Revisions Status

31/32 革新条目被 accepted (4 agents × 8 revisions = 32 total). 仅 1 条 backend-architect 标 "insufficient":

- **R1-I6 bool coerce**: 3 accepted / 1 insufficient (BA 指出 YAML 1.1 扩展 bool `1/0/on/off` 未处理). **R2 决策**: 保留当前实现 (audit report 实战仅用 true/false/yes/no), 在 T6 测试时明示 `1/0/on/off` 为 out-of-scope.

## R2 New Findings (4 个, 按严重度去重后)

| ID | 严重度 | 共识 | 修复 |
|---|---|---|---|
| R2-TL3 / R2-NF1 | important (TL/QA 双发现) | docstring drift: `collect_requirements` by_status 5-key 与 R1-I5 新 3-state 扩展不一致 | scan.py docstring 已更新为 open-ended map |
| R2-CR1 | important (code-reviewer) | R1 Tier 1 revisions 未 commit, 按 Aria C.1 → C.2 顺序必须先 commit | 已 commit `b5f4c76` (aria submodule) |
| R2-N2 | medium (backend-arch) | `_collect_upstream` shallow 返回 `configured: None` 违反 bool 类型契约 | 改为 `False` |
| R2-N3 | low (backend-arch) | `change_count` 与 `uncommitted_count` 在 MM 文件下不一致 | set dedup 对齐 |

另 3 个 minor (TL-R2-2, R2-CR-2/3, N1, NF-2/3): 皆延后至 T3-T10 处理, 不阻塞 R2 → R3 迭代。

## R1 Carried-Over (Tier 2, 不在本 PR scope)

| ID | 状态 |
|---|---|
| R1-C1 Phase 1.13/1.14 缺席 | deferred T3, planned multi-session |
| R1-C2 0/9 AC | deferred T3-T10 |
| R1-C3 SKILL.md Step 0 | deferred T5.1 |
| R1-C4 T6 测试 + T10 benchmark | deferred T6/T10 |
| R1-I1 additive-change rule | partially addressed (schema.md stub 固化), T4.1 细化 |
| R1-I2 exit code contract | partially addressed (schema.md stub 固化), T5.3 SKILL.md 吸收 |

**qa-engineer 立场**: 4 Tier 2 critical 仍是 blocker, 坚持 "DO NOT MERGE" 直到 T3-T10 完整。
**tech-lead / backend-architect / code-reviewer 立场**: Tier 2 是 planned-deferral (Spec 多 session 交付), 不在本 PR scope, 本 PR 按 T1.1-T2.5 scope 合理 merge (分阶段交付模式)。
**分歧**: 3/4 agent 支持 scope-bounded merge (不等 T3-T10), 1/4 坚持 full-AC merge。

## R2 决议

- **R2 → R3**: 应用 R2 new findings (4 条) 后进 R3 稳定性轮
- **R3 期望**: 如果 R3 findings ⊆ R2 剩余未 fix (即本 session 内能修完的都修完), 且 drift guard 仍 clean → 收敛, 准备 merge
- **Tier 2 Critical (R1-C1~C4) 作为 merge 条件的独立决议**: 由用户在 R3 收敛后决定采用 "scope-bounded merge now" 或 "等 T3-T10 full-AC merge"

R3 审计将评估:
1. R2 4 条 new finding 是否已完成 (docstring / commit / N2 / N3)
2. 是否产生新 finding (预期 ≤0)
3. 与 R2 finding set 的字节对比 (严格收敛判定)
