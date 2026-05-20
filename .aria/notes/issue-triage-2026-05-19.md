# Aria Open Issue Triage — 2026-05-19

> **Trigger**: Session post-M5 prep work (v11 addendum + HCL registry-lock shipped); owner asked to triage issue backlog before deciding next direction.
> **Method**: forgejo API + body/label inspection; no spec/code changes; mutation = close + label only.

## Before / After

| | Count |
|--|--|
| Open before triage | 27 |
| **Closed (stale)** | **12** (#96, #62, #63, #64-#72) |
| **Re-labeled** | **3** (#61+#73 +bug; #95 -aria-auto) |
| Open after triage | **15** |
| **Tier 1 sister-bundle shipped (v1.21.4)** | **#61 + #73 closed** (2026-05-20, aria-plugin PR #51) |
| **Open after v1.21.4** | **13** |

All 12 closes posted a uniform "synthetic dispatch acceptance artifact, milestone archived" comment with handoff cross-reference. Reopenable if historical reference needed.

---

## Remaining 15 — recommended priority for next AI-runnable sessions

> Sorted by (a) scope clarity (b) AI-actionability (c) value cohesion within thematic family.

### ~~🟢 Tier 1 — small/medium bugs ready to ship (sister-bundle candidates)~~ ✅ SHIPPED 2026-05-20

| # | Label | Status |
|---|-------|--------|
| **#61** | bug | ✅ Closed by v1.21.4 (`_common.py:_run` encoding=utf-8 + errors=replace + UnicodeDecodeError catch) |
| **#73** | bug | ✅ Closed by v1.21.4 (`_status.py:_normalize_status` new transitional family → `implemented`; #101 incidental migration was insufficient — `pending` symptom broke `requirements.py:56` priority_items surface) |

**Actual ship**: ~2h, 9-step Phase A→D, aria-plugin PR #51, +14 regression tests, 460/460 + 15/15 smoke PASS. **Forgejo open count**: 15 → 13.

### 🟡 Tier 2 — state-scanner thematic enhancement family

| # | Scope | Estimate |
|---|-------|----------|
| **#90** | surface in-progress `tasks.md` inline carry-forward annotations | Level 2 spec; ~6-8h |
| **#89** | surface mid-implementation carry-forward (companion to #90) | Level 2 spec; ~4-6h |
| **#79** | mid-implementation spec-drift detection trigger (post_spec mini-audit) | Level 2-3; ~8-12h |
| **#58** | 3 Skill improvements based on real-world hotfix (state-scanner/audit-engine/phase-a-planner) | Level 2; ~6h |

**Path**: One Spec absorbing #89+#90, or three Level 2 patches if shipped piecemeal. #58 is independent.

### 🟡 Tier 3 — secret/Rule #7 family (本 session 接轨)

| # | Scope | Estimate |
|---|-------|----------|
| **#84** | Secret-hygiene PreToolUse hook enforcement (#78 path 3) | Level 2-3; ~8-12h |
| **#107** | bundle PreToolUse hook as aria-init default | depends on #84; ~3-4h after |

**Path**: #84 first (defines the hook), then #107 (distribution). Single Spec absorbing both is cleaner.

### 🟡 Tier 4 — audit rubric refinements

| # | Scope | Estimate |
|---|-------|----------|
| **#54** | post_spec rubric: data availability check for historical/external data assertions | Level 1-2; ~3-4h |
| **#95** | R1/R2 audit framework-convention checker (SilkNode 2026-05-09 教训) | Level 3; ~12-16h (cross-framework abstraction) |

### 🔵 Tier 5 — proposals / discussion (need owner OD before AI work)

| # | Nature | Notes |
|---|--------|-------|
| **#59** | aria-orchestrator v2.0 三档 dispatch payload proposal | Discussion → Spec if accepted |
| **#111** | M2-coordination Aether build-container 程序化可调用 | Discussion → coord with Aether team |
| **#104** | expose Claude Code context usage to skills/agents | Discussion, proposal stage |

### 🔵 Tier 6 — large features / 远期

| # | Notes |
|---|-------|
| **#5** | Pulse 集成 (Matrix + Conduit + Element) — feature, large |
| **#32** | tdd-enforcer Level 3 security RED/GREEN commit enforcement |

---

## Recommended next session sequence

> Updated 2026-05-20 post-v1.21.4 ship + multi-terminal-coordination Spec emergence (另一终端 active scope on aria submodule).

1. ~~**Ship Tier 1 patch v1.21.4** (#61 + #73 bundle)~~ ✅ DONE 2026-05-20
2. **Owner-gated: O1 (T-deploy v11) + O2 (Tier-1 live LLM)** — unblocks US-025 close
3. **Tier 5 Forgejo discussion** (#59 / #104 / #111) — pure metadata, zero git mutation, safe regardless of multi-terminal Spec state
4. **Tier 2/3/4 (state-scanner / secret-hygiene / audit-rubric)** — **defer until `multi-terminal-coordination` Spec ships**. All these touch aria submodule (state-scanner Skill / hooks / SKILL.md), high conflict-rebase risk with their Phase B implementation. Re-evaluate after MT-1 ships.
5. **US-026 M6b kickoff** — still blocked by US-025 close gate (O1+O2)

---

## Source actions log

| Issue | Action | API |
|-------|--------|-----|
| #62, #63, #64-#72, #96 (×12) | Closed with comment | POST /comments + PATCH state=closed |
| #61 | Added `bug` label | POST /labels [2] |
| #73 | Added `bug` label | POST /labels [2] |
| #95 | Removed `aria-auto` label | DELETE /labels/27 |

Raw issue snapshot: `.aria/notes/issues-triage-raw.json` (27-row JSON, kept for audit trail; can be deleted after this triage is referenced).

---

**Generated**: 2026-05-19 by AI triage step (auto-runnable, owner-OD'd close-set + label changes)
**Pre-flight gate (Rule #8)**: N/A — no commits required for this triage (forgejo API mutations are issue-state only, not git history)
