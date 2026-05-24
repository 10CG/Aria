# Post_Spec R1 Audit — AGGREGATE — aria-2.0-m6-{e2e-resilience, docs} (combined sister-Specs)

> **Round**: R1 combined (Phase A.2 post_spec)
> **Specs audited**: aria-2.0-m6-e2e-resilience (Spec #2, 1634 lines) + aria-2.0-m6-docs (Spec #3, 1057 lines)
> **Spec status at audit**: Draft (commit `5d85617`)
> **Audit timestamp**: 2026-05-24 UTC
> **DEC reference**: DEC-20260524-001
> **Auditors (4 parallel, combined-Spec mode)**: tech-lead-critic + qa-engineer + ai-engineer + code-reviewer
> **Aggregate verdict**: **NEEDS_FIX** (both Specs, ~25 Critical + ~35 Important raw findings; de-dup ~10 Critical themes)
> **Combined-mode validation**: 5+ X-Critical cross-Spec findings caught (BOTH-locations path drift, rubric dimension mismatch, DEC-002 non-consumption, AD-M5-11 multi-source collision, mean/median PRD-Spec contradiction) — single-Spec dispatch would have missed all of these. **Combined-mode value confirmed.**

Source reports (raw):
- `.aria/audit-reports/post_spec-R1-tl-critic-2026-05-24-aria-2.0-m6-sister-specs.md`
- `.aria/audit-reports/post_spec-R1-qa-2026-05-24-aria-2.0-m6-sister-specs.md`
- `.aria/audit-reports/post_spec-R1-ai-2026-05-24-aria-2.0-m6-sister-specs.md`
- `.aria/audit-reports/post_spec-R1-cr-2026-05-24-aria-2.0-m6-sister-specs.md`

---

## Counts (raw, before de-dup)

| Auditor | Spec #2 Verdict | Spec #3 Verdict | Cross-Spec Critical | Per-Spec Critical | Per-Spec Important |
|---------|-----------------|-----------------|---------------------|-------------------|---------------------|
| tech-lead-critic | NEEDS_FIX | NEEDS_FIX | 2 (X-C-tl-1/2) | 1 + 3 | 4 + 4 |
| qa-engineer | NEEDS_FIX | NEEDS_FIX | 1 (C-5 BOTH) | 7 + 2 | 8 + 3 |
| code-reviewer | NEEDS_FIX | NEEDS_FIX | 1 (X-C1 path) | 1 + 2 | 6 |
| ai-engineer | NEEDS_FIX | NEEDS_FIX | 2 (C-AI-2/5) | 3 + 1 | 8 |
| **Total raw** | NEEDS_FIX | NEEDS_FIX | **6 X-C** | **~12** + **~8** | **~30** |
| **De-dup themes** | — | — | **5 X-C themes** | **6** + **5** themes | — |

---

## Critical themes (de-duplicated; ordered by cross-auditor consensus)

### X-Critical (cross-Spec)

#### **X-T1 — BOTH-locations path drift** *(tl X-C-tl-1 + cr X-C1)*

Spec #2 §C.3 uses `aria-orchestrator/evals/m6-prompt-quality/...` (full); Spec #3 §B.3.2 uses `aria-orch/...` (shorthand). Lab-shareable file in `standards/autonomous/humanized-command-patterns.md` will ship the abbreviated path → other Lab projects cloning `standards` see broken link.

**Fix**: sed Spec #3 only — replace all `aria-orch/` → `aria-orchestrator/` (file path context; not the GitHub repo nickname).

#### **X-T2 — DEC-20260524-002 (Aria #124) not consumed** *(tl X-C-tl-2)*

dev-claude2 landed `13035d8` today: brainstorm CONVERGED for Aria #124 submodule pointer regression gate (v1.29.0 block-mode). Spec #3 T-B0 standards submodule operation runbook doesn't reference this. T-B0.10 (pointer bump) could be blocked by v1.29.0 gate if standards branch not strict ancestor of master post-merge.

**Owner Q5 pre-decision (2026-05-24)**: Spec #3 T-B0.10 adds v1.29.0 gate verification + Spec #4 pre-release gate consumes it.

**Fix**: T-B0.10 add 1 line "Verify aria-plugin v1.29.0+ block-mode gate compatible BEFORE bump (per DEC-20260524-002 Aria #124)". Spec #4 will inherit at draft time.

#### **X-T3 — Mean (PRD) vs median (Specs) rubric scoring** *(ai C-AI-2)* → **OWNER Q4: Patch PRD §656 to median**

PRD §656 literal: `平均 ≥ 7/10` (mean). Spec #2 AC-5 + Spec #3 BOTH-locations use median-of-medians. Falsifiability gap (bimodal score distributions).

**Owner Q4 lock (2026-05-24)**: **Patch PRD §656 mean → median** (median more robust + lab industry convention).

**Fix**: PRD §656 single-line patch (~5min, inline + commit before Specs re-fix); Spec body cross-references updated post-patch line number.

#### **X-T4 — AD-M5-11 multi-source collision** *(tl C-tl-#3-1 + cr C2 + ai C-AI-5)* → **OWNER Q2: Use AD-M6-9 instead**

Live `architecture-decisions.md:3460-3478` reserves AD-M5-11 for "M5-spillover" topics. DEC-20260524-001 §2 line 123 cites it for "M6 docs decisions". Spec #3 claims it. Three sources tell three stories.

**Owner Q2 lock (2026-05-24)**: **Use AD-M6-9 (drop AD-M5-11 claim)**.

**Fix**: Spec #3 frontmatter + §How AD table + tasks T-B6 — replace AD-M5-11 → AD-M6-9 (~5min sed).

#### **X-T5 — Rubric dimension count mismatch** *(qa C-9)*

Spec #2 §C.2 defines 7 rubric dimensions (D1-D7); Spec #3 T-B3.2.3 specifies 5. BOTH-locations require consistency. Wc-l ≥ 200 line proxy is insufficient (repetitive content passes).

**Fix**: Align Spec #3 T-B3.2.3 to 7 dimensions; replace `wc -l >= 200` proxy with `grep -c "^### Pattern" >= 10` structural check.

---

### Critical Spec #2 (e2e-resilience)

#### **T2-1 — SQL refs non-existent columns** *(ai C-AI-1; qa SQL focus)*

TG-A SQL blocks reference `final_state`, `issue_type`, `project_name`, `title`, `created_at` — none exist in live `dispatches` schema. Live schema (per `aria_layer1/schema.sql:35-239`):
- `state` (terminal value `'S9_CLOSE'`, NOT `'S9'`)
- `state_entered_at`
- Per-state metadata in `dispatch_audit_log.payload_json` (JSON via `json_extract`)

**Impact**: AC-2 throws `sqlite3.OperationalError` on day 1.

**Fix**: Rewrite all TG-A SQL to use canonical columns. Add live-schema regression test (per `[[feedback_validator_repo_drift_guard_test]]`).

#### **T2-2 — `aria_layer1/state_machine.py` file doesn't exist** *(tl C-tl-#2-1)* → **OWNER Q1: Path B multi-file cov**

State machine logic distributed across `extension.py` + `comment_poll.py` + `reconciler.py` + `tick_runner.py`. AC-4 `pytest --cov=aria_layer1.state_machine --cov-fail-under=100` will fail (no such module).

**Owner Q1 lock (2026-05-24)**: **Path B — multi-file cov target**: `pytest --cov=aria_layer1.extension,aria_layer1.comment_poll,aria_layer1.reconciler,aria_layer1.tick_runner --cov-fail-under=100`. Zero scope creep, ~10min fix.

**Fix**: AC-4 + T-B-statemachine tasks rewrite cov target to 4 modules; remove all `aria_layer1.state_machine` references.

#### **T2-3 — AC-6 pre-flight $2 cap = Luxeno=0 paper-fix re-introduced** *(ai C-AI-6)*

`assert all(c <= 2.0 for c in costs)` trivially passes when Luxeno (current routing) returns `cost_usd=0.0` for every call. Same Spec #1 R1-C2 trap regenerated.

**Fix**: Reframe AC-6 to add structural floor + explicit non-null guard:
- `assert costs.count(None) == 0` (no null suppression)
- `assert sum(c is not None and c == 0.0 for c in costs) <= N` (zero-cost Luxeno acceptable but bounded)
- OR force Zhipu routing for pre-flight dispatches (3 explicit non-zero costs via Zhipu model selection)

Add explicit AD slot for pre-flight routing strategy.

#### **T2-4 — `is_synthetic` Mechanism B structurally invalid** *(ai C-AI-4)*

Mechanism B (`title LIKE '[DEMO-M6-%]'`) requires a `title` column — which doesn't exist (per T2-1). Lock Mechanism A (schema column) at Phase A.2; delete Mechanism B path.

**Fix**: §What A.2 P-7 block: lock Mechanism A (schema column `is_synthetic INTEGER DEFAULT 0` via migration 006); delete Mechanism B references.

#### **T2-5 — AC-1 wrong uptime metric** *(qa C-1)*

`TaskStates['aria-layer1']['StartedAt']` resets on task restart (not alloc restart). False-FAIL on legitimate 168h alloc with mid-run task restart.

**Fix**: Record `StartedAt` in Day-1 probe file as canonical clock start; compare current time against persisted value, not live API; also verify `alloc.ID` unchanged.

#### **T2-6 — AC-2 ZeroDivisionError + check order** *(qa C-2)*

`synth_count / total` runs before `total >= 10` assertion. If `total = 0`, crash with `ZeroDivisionError` (exit 2) instead of clean `[FAIL] AC-2: total S9 dispatches 0 < 10` (exit 1).

**Fix**: Reorder — assert total >= 10 first; THEN stratification queries.

---

### Critical Spec #3 (docs)

#### **T3-1 — CLAUDE.md 9 diffs self-contradict** *(tl C-tl-#3-1)*

"8+1 diffs" vs "9 diffs" vs Diff 6 says "Rules #1-#6 FROZEN" but live CLAUDE.md has 9 rules already.

**Fix**: Re-read live `/home/dev/Aria/CLAUDE.md`; rewrite Diff 1-9 enumeration anchored to existing 9-rule structure. Extend AD11 freeze scope to Rules #1-#9 if appropriate. Diff 6 → "verify only" / "no edit" status.

#### **T3-2 — Probe 1 regex extraction brittle** *(tl C-tl-#3-2; cr partial)*

Probe 1 uses `head -1` ordering — fragile to README layout changes. T-A6.1 task ordering vs T-A2.1 (README update) ambiguous.

**Fix**: Replace `head -1` with anchored regex (e.g., `grep -m1 -oP 'badge.*v\K[0-9]+\.[0-9]+\.[0-9]+'`); make Probe 1 ordering-independent.

#### **T3-3 — Plugin version SoT drift** *(tl C-tl-#3-3; cr C4)*

DEC says `v1.26.0`, live CLAUDE.md says `v1.22.0`, Spec body says `v1.27.0`, plugin.json reads `v1.27.0`. AC-3 should not hardcode.

**Fix**: AC-3 reads dynamically: `python3 -c "import json; print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])"`. Spec body acknowledge "DEC v1.26.0 was draft-time snapshot; SoT = plugin.json".

#### **T3-4 — PRD line citations drift** *(cr C3)*

Spec #2 cites §630/§634/§639; actual post-patch `a786444` content at §637/§648-651/§656. PRD line numbers shifted after Q-final-1/2 patches.

**Fix**: Provided exact replacement table from cr report. Spec #3 also cites PRD lines — verify post-patch.

#### **T3-5 — PRD §568 location conflict** *(ai C-AI-3)* → **OWNER Q3: Patch PRD §568 to follow Spec**

PRD §568 says `standards/autonomous/layer-boundary-contract.md`. Spec #3 §B.4 says `aria-orchestrator/docs/` per km M-km-R2-005 (Aria-specific should not be Lab-shareable).

**Owner Q3 lock (2026-05-24)**: **Patch PRD §568 to follow Spec** (km brainstorm insight is authoritative; PRD location guidance must catch up).

**Fix**: PRD §568 single-line patch (~10min, inline + commit before Specs re-fix).

---

## Important themes (selective; non-blocking to R2 verdict)

### Spec #2
- **I2-1** Day-3 gate AC only checks verdict line; not 3 individual conditions
- **I2-2** WAL-D scenario self-contradiction (S_FAIL + no data corruption mutually exclusive)
- **I2-3** LLM-4 (429) test single-provider; Luxeno + Zhipu have different `RateLimitError` shapes
- **I2-4** LLM-5/LLM-6 wildcard URL httpx_mock should split provider-specific test files
- **I2-5** `llm_client.complete()` referenced in §B.1 doesn't exist (actual: `silknode_client.call_llm` / `zhipu_client.call_llm`)
- **I2-6** `RateLimitError` / `ProviderUnavailableError` class names not bound to real modules
- **I2-7** `--cov-fail-under=100` not enforced in CI (add to pyproject.toml addopts)
- **I2-8** AC-7 cross-Spec file mutation risk (validate-m6-handoff.py owned by Spec #1)

### Spec #3
- **I3-1** AC-1 Rule freeze check count-based only (doesn't verify Rules #1-#6 bodies unmodified)
- **I3-2** AC-4 grep -c counts lines (not distinct probe names); name collision in description field doubles
- **I3-3** `date -d` Probe 3 GNU-only (macOS/BSD fails); replace with python3
- **I3-4** Diff 3 calls Layer 1 "Hermes + GLM"; should be "Hermes + Luxeno-routed GLM models" per 2026-05-21 redirect
- **I3-5** AC-3 hardcodes v1.27.0; should read dynamically (covered by T3-3 above)

### Cross-Spec Important
- **XI-1** BOTH-locations sequence contract not enforced (Spec #2 AC-5 grep passes even if Spec #3 file missing; Spec #3 AC-6 fails if Spec #2 corpus missing)
- **XI-2** PRD §654 (`<10min approval`) + §655 (`<20% drift error`) not covered in Specs #1/#2/#3 (defer to Spec #4 or v2.1 OOS)

---

## Owner-locked decisions (2026-05-24)

| Q | Decision | Affected findings | Spec edits |
|---|----------|-------------------|------------|
| **Q1** | Path B multi-file cov target (no extraction, no scope change) | T2-2 | Spec #2 AC-4 + T-B-statemachine tasks |
| **Q2** | AD-M6-9 (drop AD-M5-11 claim) | X-T4 | Spec #3 frontmatter + §How + tasks T-B6 |
| **Q3** | Patch PRD §568 to follow Spec (km M-km-R2-005 authoritative) | T3-5 | PRD §568 ~10min + Spec #3 ref |
| **Q4** | Patch PRD §656 mean → median | X-T3 | PRD §656 ~5min + Spec #2 AC-5 + Spec #3 BOTH-locations |
| **Q5** *(AI pre-decided)* | Spec #3 T-B0.10 adds v1.29.0 gate verify; Spec #4 pre-release inherits | X-T2 | T-B0.10 1-line + Spec #4 to consume at draft |

---

## R1 fix-pass plan

### Pre-R1-fix (mechanical PRD patches, single commit)

1. PRD §568 location patch (Q3 lock)
2. PRD §656 mean → median patch (Q4 lock)
3. Commit: `docs(prd-v2): R1 audit follow-up — §568 layer-boundary location + §656 rubric scoring metric`
4. Dual-push origin + github + 3-way SHA parity

### R1-fix dispatch (2 parallel agents)

- **Agent A: backend-architect** → Spec #2 R1 fixes (T2-1..T2-6 + I2-*, all X-T linkage)
- **Agent B: knowledge-manager** → Spec #3 R1 fixes (T3-1..T3-5 + I3-*, X-T1/T2/T4 linkage)

Both agents:
- Receive R1 aggregate (this file) + owner Q1-Q5 locked decisions
- Apply inline `R1-<theme-id> fix:` trace per `[[feedback_audit_driven_fix_conventions]]`
- Cross-coordinate via re-reading sibling Spec to ensure cross-Spec consistency
- Effort: ~30-45min each (Spec #2 more complex due to schema reality gap)

### R2 verification

After R1-fix commit, dispatch 3-agent challenge (cr + ai + tl-critic, parallel, EACH covering both Specs in one combined report) to verify:
- 10 Critical themes CLOSED (not PARTIAL/PAPER/REGRESSION)
- ≥70% reduction
- 0 new Critical introduced by fix

Target: SCOPE_OK_R2 4/4. If R2 introduces new Critical → R3 stability check (per Spec #1 precedent).

---

## Cross-references

- DEC-20260524-001: `.aria/decisions/2026-05-24-us026-m6b-brainstorm.md` (Spec #2/#3 SoT)
- DEC-20260524-002: `.aria/decisions/2026-05-24-aria-124-submodule-pointer-regression-gate.md` (T-B0.10 cross-ref source)
- Spec #1 Approved (`c29a800`): `openspec/changes/aria-2.0-m6-cost-acceptance/` (lessons baseline)
- Spec #2 Draft: `openspec/changes/aria-2.0-m6-e2e-resilience/` (R1-fix target)
- Spec #3 Draft: `openspec/changes/aria-2.0-m6-docs/` (R1-fix target)
- m5-handoff.yaml: `aria-orchestrator/docs/m5-handoff.yaml:148-172` (abi_compat)
- PRD post-patch a786444: `docs/requirements/prd-aria-v2.md` (pending Q3+Q4 patches)
- live `dispatches` schema SoT: `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/schema.sql:35-239`

---

**Aggregate authored**: 2026-05-24 (sister-Specs R1 closeout)
**Status**: R1 NEEDS_FIX → fix-in-progress (2 parallel agents post PRD patches)
**Combined-mode value**: 5 X-Critical findings caught that would have escaped single-Spec dispatch (validate methodology choice for future M-N sister-Spec audits)
