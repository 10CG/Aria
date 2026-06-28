---
checkpoint: pre_merge
mode: convergence
rounds: 3
converged: true
verdict: PASS
oscillation: false
incomplete: false
drift_anchor_missing: false
drift_check_skipped: true
timestamp: 2026-06-28T12:15:57Z
spec_id: aria-2.0-m6-e2e-resilience
---

# Pre-merge 收敛审计报告 — PR #26 (M6 AC-6 false-green 修复, #146)

> **target**: aria-orchestrator PR #26 / branch `fix/m6-ac6-preflight-false-green-146`
> **engine**: audit-engine 1.0.0 (convergence mode, max_rounds=4) → agent-team-audit 3-lens
> **team**: aria:code-reviewer + aria:qa-engineer + aria:tech-lead (convergence voters)
> **verdict**: **PASS** (converged R3, unanimous) | **0 Critical / 0 Major**

## Anchor (Step 0, 固化 @ source_sha 53d541e, 审计周期内不可变)

- **primary_goal**: 修复 AC-6 pre-flight gate false-green —— 未填模板 (`dispatch_id: <id>` + `cost_usd: 0.00`) 不得通过 AC-6; 要求 3 个非占位 `dispatch_id` + 已选 provenance option (A/B/C)。
- **in_scope**: `check_preflight` + `_is_unfilled_dispatch_id` + 其单测。
- **out_of_scope**: `dispatch_id`↔`dispatches.db` 交叉核验 (#146 明确 over-reach) / 其他 AC / 实际 168h 运营跑 / 把 `cost_usd=0.0` 当占位信号 (合法订阅价)。
- drift-checker 未独立 spawn (drift_check_skipped, fail-open <warn 档); 三轮 anchor 锚定由各 lens prompt 内嵌强制, 无可执行结论越界。

## 收敛轨迹

| Round | HEAD | code-reviewer | qa-engineer | tech-lead | 全票 PASS? |
|-------|------|--------------|-------------|-----------|-----------|
| R1 | 53d541e | PASS (2 minor) | PASS (4 minor) | PASS (2 minor) | ✅ 但有可执行 minor |
| R2 | f267c97 | PASS (NONE) | **REVISE (1 真实新 bug)** | PASS (3 minor) | ❌ 非全票 |
| R3 | c5d863d | PASS (NONE) | PASS (仅 residual-by-design) | PASS (仅 residual-by-design) | ✅ **CONVERGED** |

**收敛条件**: `unanimous_pass=TRUE` (R3 3/3 PASS) AND `conclusions_stable` (R2→R3 可执行结论集 {qa-REVISE, tech-lead-broaden, tech-lead-citation} → ∅, 仅余各 lens 一致认定的 documented residual-by-design)。无振荡。

## 审计的实证价值 (为何多轮 > 单轮)

R1 三 lens **全 PASS** (仅 minor)。若止于单轮即合并, 会漏掉 **R2 qa-engineer 抓到的真实 false-PASS**:

> **R2 REVISE (qa, 真实新 bug)**: 占位检查用 `dispatch_ids[:3]` 窗口。行首 prose `dispatch_id ...` 被计入后, 把真 `<id>` 占位挤到 index≥3, `[:3]` 查不到 → 实测 `rc=0` 假绿。**这恰好重开了本 PR 要堵的 false-green。**

该 bug 是 R2 收紧解析时暴露的, Phase B code-review (单轮) + 审计 R1 均未发现。R2 落地"全量扫描"修复后, R3 三 lens 对抗复验 (含真 subprocess 探针) 确认闭合。

## 各轮发现处置 (全部 landed by main loop between rounds, 审计只审不改)

**R1 (commit 53d541e→f267c97)**:
- [qa] prose 行膨胀 false-PASS → 解析收紧为行首字段匹配。
- [qa] provenance "Selected option A: desc" 标题 false-FAIL → 要求 key 后紧跟 ':'。
- [qa/tech-lead] 裸 `id` false-reject → `_is_unfilled_dispatch_id` 要求尖括号。
- [tech-lead] PASS/docstring "REAL" 过度声称 → 软化 + 残留诚实声明。
- [cr/qa] 覆盖缺口 → 5 新测。

**R2 (commit f267c97→c5d863d)**:
- [qa REVISE] 占位检查改全量扫描 (`dispatch_ids` 不再 `[:3]`)。
- [tech-lead] `_is_unfilled_dispatch_id` 放宽到任意 `<...>` (防御纵深)。
- [tech-lead] §A.8 引用加 `#146 / Aria-repo` 消跨仓歧义。
- 2 新测 (placeholder 挤出窗口仍 FAIL / `<dispatch-id>` 变体捕获)。

## 残留 (by design, 非阻塞 — 三 lens R3 一致)

纯 prose 行 (行首 `dispatch_id naming: foo`) 仍被计入 count → 若蓄意以 3 条非占位 junk 行填充可满足 count gate。此为 #146 固有上界 (无 DB 交叉核验无法区分 junk 与真实 dispatch, 而交叉核验 = out-of-scope over-reach)。缓解: runbook Phase 0 人眼确认 + 残留已在 docstring/PASS 文案/spec §A.8 诚实披露。

## 测试 / 回归

- `python3 -m unittest tests.acceptance.test_m6_e2e_acceptance` → **42 PASS** (起始 28, 净加 14)。
- 真实空模板 `--check-preflight` → `[FAIL] AC-6` (原 false-green 闭合)。
- AC-7 abi_compat 回归 → PASS (5 promises)。

## 结论

**PASS / converged**。修复精确实现 anchor primary_goal, 无 over/under-reach, 多轮对抗暴露并闭合一处真实 false-PASS, 残留经诚实披露且有 runbook 兜底。审计层面无阻塞合并的发现。最终合并仍需人类两方评审 (self-approval 护栏)。
