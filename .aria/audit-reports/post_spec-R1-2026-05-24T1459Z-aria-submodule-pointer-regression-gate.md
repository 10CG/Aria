# Post-Spec R1 Audit — aria-submodule-pointer-regression-gate

> **Spec**: [openspec/changes/aria-submodule-pointer-regression-gate/](../../openspec/changes/aria-submodule-pointer-regression-gate/)
> **Checkpoint**: post_spec (Phase A.2)
> **Round**: R1
> **Date**: 2026-05-24T~14:59Z
> **Agents (4 parallel)**: tech-lead + backend-architect + qa + knowledge-manager
> **Aggregate verdict**: PASS_WITH_WARNINGS unanimous (4/4)
> **Total issues**: 4 Critical + 19 Important + 20 Minor

---

## Verdict Matrix

| Agent | Verdict | Critical | Important | Minor |
|---|---|---|---|---|
| tech-lead | PASS_WITH_WARNINGS | 3 | 5 | 5 |
| backend-architect | PASS_WITH_WARNINGS | 0 | 5 | 6 |
| qa | PASS_WITH_WARNINGS | 0 | 4 | 6 |
| knowledge-manager | PASS_WITH_WARNINGS | 1 | 5 | 3 |
| **Total (after de-dup themes)** | **PASS_WITH_WARNINGS** | **4** | **~15** | **~15** |

---

## Critical Issues (must fix in Rev1)

### C-tl-1: §C.2.5 numbering collision

**Source**: tech-lead R1
**Issue**: `aria/skills/phase-c-integrator/SKILL.md` ALREADY defines §C.2.5 = "Multi-Remote Push Enforcement" (v1.15.0+). Spec proposes new §C.2.5 = "Submodule Pointer Regression Gate". Hard naming collision — Spec describes an edit that cannot apply cleanly.

**Fix options**:
- (A) Insert new gate as §C.2.4.5 (sub-step between C.2.4 and existing C.2.5)
- (B) Renumber: new gate = C.2.5, existing C.2.5 = C.2.6, existing C.2.6 = C.2.7 (cascade)
- (C) Use a different section name entirely

**Recommended**: (A) — minimal-cascade insertion as C.2.4.5. Pre-merge gates naturally form a sub-step group below C.2.4.

### C-tl-2: Pre-merge placement explicit

**Source**: tech-lead R1
**Issue**: §What says "after Rule #8 CI gate, before merge execution". Tasks T-gate-1 only says "after §C.2.4" without locking out post-merge runners (e.g., existing C.2.5 Multi-Remote Push runs POST-merge).

**Fix**: Explicit "before branch-manager merge API call" hook point spec'd in proposal.md §What A + tasks.md T-gate-1.

### C-tl-3: `aria/cron/` directory + proposal/tasks contradiction

**Source**: tech-lead R1
**Issue**:
- `aria/cron/` directory does NOT exist in aria-plugin repo
- proposal.md §C says "weekly periodic GitHub Actions / Forgejo Actions cron in `10CG/Aria`" (main Aria repo)
- tasks.md T-tripwire-2 says draft `aria/cron/submodule-gate-tripwire.sh` (aria-plugin repo)
- **Contradiction between proposal and tasks**

**Fix**: Pick one — most likely `.forgejo/workflows/submodule-gate-tripwire.yml` in main `10CG/Aria` repo (which already has `.forgejo/workflows/` per submodule pointer review). Update BOTH proposal.md and tasks.md to consistent path.

### C-km-1: 3 broken memory cross-references

**Source**: knowledge-manager R1 (verified via Read tool against memory dir)
**Issue**: Spec cites these memory entries that do NOT exist in `/home/dev/.claude/projects/-home-dev-Aria/memory/`:
- `feedback_brainstorm_forcing_function_unified_anchor`
- `feedback_brainstorm_owner_escalation_discipline`
- `feedback_paper_fix_antipattern`

These are cited as DEC + Spec foundational memory entries but the actual files don't exist. Affects:
- proposal.md §Cross-references "Brainstorm pattern memory"
- DEC-20260524-002 §8 "Cross-references" + §9

**Fix options**:
- (A) Add tasks.md T-memory entry to CREATE these 3 memory files in Phase D as part of session closure
- (B) Remove the broken refs from Spec; cite only DEC §9 prose content directly
- **(C) Recommended**: Verify if those memories are queued-for-write (Phase D D.3 of brainstorm cycle, not yet shipped). If so, mark them in Spec as "(to be created Phase D)" — accurate, not deceptive. The 4th cited memory (`feedback_post_spec_audit_pragmatic_convergence`) IS in MEMORY.md per knowledge-manager verification.

---

## Important Issues (themes consolidated)

### Bash spec mechanical bugs (backend-architect)

- **I-ba-1**: `git fetch origin master` fetches a single branch ref, does NOT update `origin/master` remote-tracking ref. Refspec assertion is structurally broken. Fix: use bare `git fetch origin` OR explicit `git fetch origin refs/heads/master:refs/remotes/origin/master`.
- **I-ba-2**: BEFORE/AFTER capture ordering wrong in proposal.md pseudocode (both reads happen AFTER fetch → always equal). Tasks.md T-gate-3 correctly sequences before/after, but proposal.md text is misleading.
- **I-ba-3**: First-run edge case (no `origin/master` local ref yet) — `git fetch origin master` returns exit 128, not the structured "fetch failed" diagnostic spec promises.

### Other Important (selected high-priority)

- **I-ba-4**: Commit trailer regex uses Unicode `→` (U+2192) — fragile in non-UTF-8 locales (LANG=C/POSIX). Add ASCII `->` alternative.
- **I-ba-5**: Performance budget claim "<500ms per submodule" not defensible for CI cold-path (per-submodule fetch ~300ms-2000ms × 3 submodules = ~900ms-6000ms).
- **I-tl-1**: Telemetry retention policy undefined for 4 JSON files.
- **I-tl-3**: `wait_recoverable` classifier via stderr regex is "as fragile as dropped grep" (AD-FOLLOWUP-1 prohibits). Recommend bounded retries (3 × exponential) then always escalate as terminal.
- **I-tl-4**: Rule #9 handoff trigger not pre-evaluated; with ~15h spanning 2-3 sessions, at least one will trigger handoff.
- **I-tl-5**: Multi-terminal coordination — must claim `aria/skills/phase-c-integrator/SKILL.md` via Layer L before Phase B edits.
- **I-qa-1**: Detached HEAD submodule untested — add T-replay-10 or extend T-replay-7.
- **I-qa-2**: T-replay-8 "submodule removed" has imprecise assertions ("appropriate path-removed handling" = implementer discretion).
- **I-qa-3**: Zero-activity 14d window risk — if no PRs touch submodules → 0 warn fires → false ready-to-flip. Add minimum-observation-count guard.
- **I-qa-4**: FP denominator ambiguous (total gate executions? total WOULD-BLOCK events? total PR merges?). Recommend: FP rate = FP / total WOULD-BLOCK events. Add `human_reviewed_as_fp` field to warns schema.
- **I-km-1**: Audit trajectory frontmatter missing (vs m6-cost-acceptance reference Spec).
- **I-km-2**: CHANGELOG format guide lacks reference to existing entry style (e.g., [1.27.0]).
- **I-km-3**: DEC §8 downstream path is `aria-submodule-pointer-gate` (typo), actual is `aria-submodule-pointer-regression-gate`. Cross-ref note needed.
- **I-km-4**: `aria/metrics/` directory existence not verified — JSON appends will silently fail if missing.
- **I-km-5**: `wait_recoverable` classifier mechanism: Spec assumes implicit knowledge of workflow-runner; add 2 example patterns inline (`Could not resolve host` transient / `Authentication failed` terminal).

---

## Minor Issues (selected)

(15 Minor items total — see individual agent outputs for full list)

- AD-FOLLOWUP-1..5 prefix non-standard, not inline-tagged in §What
- Effort baseline header/§Effort mismatch (~9h vs ~15h)
- Predecessor Spec link path inconsistency (aria/openspec vs openspec)
- ARIA_SUBMODULE_GATE_MODE env var lacks `.aria/config.json` mapping pattern
- T-rule6 0.5h likely understated → ~1h
- M-ba-3: telemetry JSONL vs array — mandate JSONL for race-safety
- M-ba-4 / M-ba-5: T-replay-4/9 mock mechanism unspecified — recommend deterministic pre-staged fixture
- M-ba-6: Forgejo PR label fetcher local vs CI fallback policy
- M-qa-2: Override audit log file mode/JSONL specification
- M-qa-3: Tripwire cron last_run_timestamp tracking for outage detection
- M-qa-4: Telemetry retention policy annotation
- M-qa-5: SHA normalization in trailer parser (short vs full)
- M-qa-6: Phase D ownership for post-ship monitor unassigned
- M-km-1: Two-session strategy mismatch between proposal and tasks
- M-km-2: ai-engineer R2 contribution not referenced in §How (cite as unified anchor source)
- M-km-3: proposal.md Next step "Level 2 OR Level 3" ambiguity — clarify Level 3 baseline

---

## Cross-cutting positive findings

(R1 not all negatives — agents flagged structural strengths)

- **Methodology compliance**: Rule #5 ✓, Rule #6 deterministic substitute ✓, Rule #8 pattern correctly extended (modulo C-tl-1 collision), 向后兼容 honored via 2-phase rollout ✓
- **DEC quality**: brainstorm trajectory exceptional (R2 双反转 + ai-engineer 第三路径 + 4/4 R3 ACCEPT) — Spec faithfully implements §4 final choice
- **AI-DDD alignment**: knowledge-manager judged "AI-DDD 可读性高水准示范" — §Why incident replay + §What architecture diagram = self-contained for fresh AI reader
- **5-deliverable bundling**: acceptable as single change unit (share rollout fate); not over-bundled
- **URL drift (R7) "out of scope"**: defensible — supply-chain threat model orthogonal; tripwire #3 catches bypass

---

## Rev1 action items (consolidated)

**Must do (Critical)**:
1. Fix §C.2.5 numbering — insert as §C.2.4.5 (recommended) OR cascade renumber
2. Lock pre-merge placement explicit ("before branch-manager merge API call")
3. Resolve proposal vs tasks contradiction on tripwire cron location — choose one (recommended: `.forgejo/workflows/` in main 10CG/Aria)
4. Fix 3 broken memory cross-references — mark as "(to be created Phase D)" OR remove refs OR add T-memory task

**Should do (Important high-impact)**:
5. Fix Bash spec bugs I-ba-1 (use `git fetch origin`), I-ba-2 (correct BEFORE/AFTER ordering in pseudocode)
6. Add ASCII `->` alternative to trailer regex
7. Realistic performance budget (acknowledge CI cold-path 1-5s)
8. Add minimum-observation-count guard (I-qa-3) — flip requires ≥N gate executions OR explicit OpenSpec defer
9. Specify FP denominator + add `human_reviewed_as_fp` field (I-qa-4)
10. Add T-memory task for 3 missing memory files OR scrub references
11. Add Layer L claim step in Phase B.1 (I-tl-5)
12. Add `aria/metrics/` directory existence check / create step (I-km-4)
13. Add audit trajectory frontmatter section (I-km-1) — populated after R2 converge
14. Specify `wait_recoverable` bounded-retries pattern (I-tl-3) instead of stderr regex classifier

**Nice to have (Minor — batch in single Rev1 commit)**:
15-30. All remaining Minor items (style, polish, inline annotations)

---

## R2 expectation

Per `feedback_post_spec_audit_pragmatic_convergence` + `feedback_post_spec_audit_two_round_pragmatic_for_l2`:
- Rev1 addresses 4 Critical + top ~10 Important + batch Minors
- R2 audit (3-4 agents): expect verdict shift to PASS_WITH_WARNINGS unanimous + 0 new Critical
- If R2 surfaces NEW Critical (Aria scope creep / fundamental flaw missed in R1) → R3 needed
- Otherwise: CONVERGED at R2 (Level 2/3 pragmatic baseline)

Estimated Rev1 effort: ~1-1.5h (Spec editing only, no code)
Estimated R2 audit: ~45min (3-4 agents parallel)
Total Phase A.2 remaining: ~2h

---

**Audit completed**: 2026-05-24T~14:59Z
**Aggregator**: orchestrator (Claude Opus 4.7 1M context)
**Next**: Phase A.2 Rev1 (fix 4 Critical + selected Important) → R2 audit
