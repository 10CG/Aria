# post_spec audit (R1+R2 consolidated) — concurrent-track-proactive-coordination

> **Checkpoint**: post_spec | **Mode**: convergence (Level 2) | **Change**: `concurrent-track-proactive-coordination` (#133)
> **Status**: **未收敛** — banked 2026-05-30 待下次 Rev2 + scope 重构
> **Panel**: aria:tech-lead (scope/reuse) + aria:qa-engineer (AC falsifiability) + aria:code-reviewer (feasibility)
> **Trajectory**: R1 NEEDS_FIX (3/3) → Rev1 → R2 1 NEEDS_FIX + 2 PASS_WITH_WARNINGS (未收敛)

---

## Meta-lesson (本 cycle 最大产出)

审计**两轮**把同一 class 缺陷 —— **Spec 引用未读码就假设的数据形状(created_at-class)** —— 在代码写之前全部拦下:
- **R1**: proposal 假设 `tracks_multibranch.collision_type` 字段存在 → 实际不存在(只在设计文档 `layer-l-integration.md:23,69` + renderer-local)。
- **R2**: Rev1 假设 `_classify_collision` 输入是 `tracks[]` → 实际是 `list[ClaimRecord]`(reconcile 输出);且假设 phase1_gate 与切口2 共享 collision 字段 → 实际 phase1_gate 读独立的 claim YAML refs。

同 session 的 M6 created_at hotfix(`feedback_shipped_archived_spec_can_be_nonfunctional_on_prod` / `feedback_spec_reuse_data_source_must_match_actual_access`)在此 **二次 + 三次实证**:起草者反复假设数据可达性,multi-agent 独立 verify-against-code 反复拦截。**audit 的核心价值 = 强制 verify 复用声明的实际可达性 + ref 语义,不止存在性。**

---

## R1 (NEEDS_FIX, 3/3)

| Sev | Finding | Evidence |
|---|---|---|
| **C1** (3/3) | `tracks_multibranch.collision_type` 字段不存在 (created_at-class) | collector 只产 `exists/tracks/branches_scanned/legacy_count/errors`;collision 仅 renderer-local `_classify_collision`(名 `collision_kind`),不入 snapshot;`collision_type`/`has_collision` 只在 `layer-l-integration.md:23,69` 设计文档 |
| **C2** (qa) | `coordination.enabled` 是 config 键非 snapshot 字段 | `.aria/config.json` `state_scanner.coordination.enabled`;查找路径未指定 |
| I1-I7 | default-branch 解析未定 / fetch 复用语义混淆 / disjointness 未显式 / UPM 检测机制未定 / behind>0 假阳性 / self-serial 未排除 / AC-3 负向不可测 | 见 Rev1 changelog |

→ **Rev1** 闭合全部(见 proposal Rev1 changelog)。

## R2 (未收敛 — 1 NEEDS_FIX + 2 PASS_WITH_WARNINGS)

**tech-lead: NEEDS_FIX**(code-reviewer N1 独立佐证 phase1_gate 点):
- **C1 NOT-CLOSED**: `_classify_collision(claims: list[ClaimRecord])` 真实输入非 `tracks[]`;真实管线 `tracks[] → _track_to_claim_record(可 raise) → reconcile_all → _classify_collision`。迁移含整条 reconcile 链,非"抽函数"。
- **I3 NOT-CLOSED (架构性)**: phase1_gate (`phase1_gate.py:401-415`) 读 `read_claims()` = claim YAML refs `refs/aria/claims/*`,与 snapshot `tracks_multibranch`(handoff frontmatter 重建)独立数据源、独立生命周期。"两路径共享 collision 字段"物理不成立;disjointness 仅靠 `enabled` 互斥。
- **N2**: Level 2 边界击穿 → 建议拆 collision-field-persistence 独立 Spec。
- N3: `_track_to_claim_record` 是 lossy approximation(advisory/visual),持久化后被切口1 当半决策输入,语义错配。

**qa: PASS_WITH_WARNINGS** — 7 R1 findings Spec 层闭合;`upm.source_file` 真实存在(`upm.py:326+`)✅;NEW minor:AC-1 缺 `source_file==null` null-guard / AC-4 `enabled==true` 侧 fixture 未定 / `collision.kind!=none & behind>0 & 非UPM` 中间态 smoke 缺。

**code-reviewer: PASS_WITH_WARNINGS** — C1/C2 closed;3 citation 不准:(I1) `symbolic-ref` 应 cite `sync.py:114` 非 :37-41(rev-parse);(I2) `git.py:167` ahead/behind 锁 `@{upstream}` 不能直接调,只复用 `rev-list --left-right` pattern;(C1) input `tracks[]` vs `ClaimRecord`。N1: phase1_gate 不读 collision 字段,"单一源"夸大。coordination_fetch error_kind enum 5 值 VERIFIED 可复用 ✅。

---

## 下次 Rev2 待办

见 proposal §R2-CARRY(6 项:scope 重构拆子 Spec / 修 collision 迁移描述 / 删 phase1_gate 共享字段说法 / 修 3 citation / qa null-guard+smoke / AC-4 注明 out-of-scope)。

**收敛状态**: R2 未达 (需 NEEDS_FIX→闭合 + 0 new Critical + 稳定轮)。banked,下次 fresh session Rev2。
