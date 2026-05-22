# post_spec Audit (aggregate) — state-scanner-status-extraction-range

> **Checkpoint**: post_spec · **Mode**: convergence · **Spec**: `state-scanner-status-extraction-range`
> **Trigger**: Forgejo aria-plugin #50 · **Date**: 2026-05-21
> **Team**: aria:tech-lead / backend-architect / qa-engineer / code-reviewer / knowledge-manager (5-agent, per `.aria/config.json` teams.post_spec)
> **Verdict**: **PASS** (CONVERGED after R1→R2→R3)

---

## Convergence trajectory

| Round | Agents | Findings | 结果 |
|-------|--------|----------|------|
| R1 | 5 | 1 Critical + ~10 Important + ~15 Minor | 5/5 SPEC_NEEDS_REVISION |
| R2 | 5 | 全 R1 findings RESOLVED;3 NEW (1 Important + 2 Minor/Medium) | 4/5 CONVERGED,qa-engineer NEEDS_R3 |
| R3 | 2 (qa-engineer + code-reviewer,定向) | 全 R2 NEW RESOLVED;0 new Critical/Important | 2/2 CONVERGED |

R3 为定向收敛轮 — 仅续 R2 有 open finding 的 2 个视角 (qa-engineer 的 NEW-QA-1/2/3、code-reviewer 的 NEW-IM-1/MN-1/MN-2);其余 3 视角 R2 已 CONVERGED 且 R3 改动 (T3/T4 additive test-list) 不触及其关切域。

## R1 关键 findings (已全部闭合)

- **CR-1 (Critical)**: soft_error 数据流契约断点 — Design note option (a) 接不通 (`_normalize_status` 丢弃 bool) + `_status_lifecycle_head` 不接受 None 会运行时 crash。→ R2 收敛为 **option (b)**: 新增 `_status_field_overlong()` 瘦谓词,`_normalize_status` 签名不变,None-guard 覆盖 collector 独立调用路径。
- **#73 回归保护缺失** (TL-1/TL-6/QA-3): `TestStatusNormalizationIssue73Fix` 8 test 未纳入回归范围 → 5 处补入。
- **T3 决策悬空** (TL-2/IM-3/QA-6/BA-6): "待 audit 收敛" placeholder → 本 audit 收敛为 option (b) 并写回 proposal/tasks。
- **分隔符覆盖面** (BA-1/BA-2/IM-1): comma 文档化排除 / em-dash 变体 + ASCII hyphen → regex `\s*[—–]\s*|\s-\s|[;；。]`。

## R2 NEW findings (R3 已闭合)

- NEW-IM-1 (Important): #73 短语跨分隔符无 test 锚点 → T4 加 `"implementation — complete"` 钉死 case。
- NEW-QA-3 (Medium): `requirements.py` soft_error e2e 未覆盖 → T4 加 `collect_requirements()` e2e。
- NEW-QA-2 (Low-Med): 分号/句号 case 缺预期值 → 补 `"Approved; Phase A done"→approved` / `"WIP。Phase A done"→unknown`。
- NEW-MN-1/MN-2: f-string `{d.name}` + requirements.py 接入位置约束 → 已写明。

## 结论

Spec (proposal.md + tasks.md) 经 3 轮 5-agent convergence 审计达成收敛,Status → Approved,可进入 Phase B 实施。设计方向 (下游截断 + `raw_status`/`status` 职责分离 + option (b) soft_error 通道) 经全员确认正确。
