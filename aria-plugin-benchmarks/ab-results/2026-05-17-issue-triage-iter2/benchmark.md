# issue-triage iteration-2 benchmark — 2026-05-17

**Skill**: issue-triage | **Baseline**: v1.0.0 (pre-anti-hand-author) | **With-skill**: v1.1.0 (iteration-2 anti-hand-author)
**Evals**: 4 (3 reused from 2026-05-13 + 1 fresh non-contextualized aria-#95)
**Primary metric**: D3 schema conformance (was 0/3 with_skill in 2026-05-13)

## Results (n=4 per config)

| Metric | with_skill v1.1.0 | old_skill v1.0.0 | Delta |
|--------|-------------------|------------------|-------|
| D1 JSON output | 4/4 | 4/4 | 0 |
| D2 triage-comment.md | 4/4 | 4/4 | 0 |
| **D3 schema conformance** | **0/4** | **0/4** | **0** |
| D4 canonical enums (lenient grader) | 4/4 | 3/4 | +1 (non-discriminating, see notes) |
| D5 multi-artifact | 4/4 | 4/4 | 0 |
| **script_produced (ran triage.py)** | **4/4** | **4/4** | **0** |

| Cost | with_skill | old_skill |
|------|-----------|-----------|
| Mean tokens | 48,392 | 50,204 |
| Mean duration | 135.4s | 129.8s |

## Headline finding: iteration-2 fixed the WRONG root cause

**The 2026-05-13 benchmark's D3 diagnosis was wrong for Opus 4.7.** It attributed D3 0/3 to "agents hand-wrote JSON instead of running scripts/triage.py, missing steps.step1_issue.body". This benchmark **disproves that hypothesis**:

- `script_produced`: **8/8** — every agent (both v1.0.0 AND v1.1.0) ran `scripts/triage.py` (exit 0 or 10) and produced script-generated JSON. **Zero hand-authoring.**
- Even the **v1.0.0 baseline** agents explicitly cited "Step 0 hard constraint" — the pre-existing line-72 不可协商 wording was already sufficient for Opus 4.7.
- The anti-hand-author strengthening (iteration-2) is therefore **defense-in-depth with 0 behavioral effect on Opus 4.7** — D3 is identical 0/4 for both configs.

**The real D3 root cause**: schema violations are 100% in **AI-filled Stage 3 fields** (the mechanical triage.py skeleton is schema-valid; the AI fills verdict/severity/recommended_action + Step 6 repro cases with non-canonical values):

| eval | config | actual D3 failure |
|------|--------|-------------------|
| 1 | ws v1.1.0 | `verdict: "already-fixed"` (schema enum: confirmed/partial-repro/not-reproducible/**fixed-in-X**/duplicate-of-#N/needs-info/wont-fix) |
| 1 | os v1.0.0 | `verdict: "fixed-in-1.20.0"` (should be literal `fixed-in-X`) |
| 2 | ws | `repro.cases[0]` missing required `case_id` |
| 2 | os | `verdict: "fixed"` (not in enum) |
| 3 | ws+os | `severity: "medium"` (schema enum: critical/**major**/minor/trivial — no "medium") |
| 4 | ws | `verdict: "enhancement"` (not in enum) |
| 4 | os | `severity: "medium"` |

The AI consistently invents *reasonable-sounding* values (`medium` severity, `already-fixed`/`enhancement` verdict, `schedule`/`open-spec` action) that are NOT in the strict schema enums. SKILL.md Stage 3 does not inline the canonical enums at the fill point — it points to `standards/conventions/issue-triage.md §Verdict dictionary` (a separate file the agent doesn't reliably open).

## D4 grader caveat (non-discriminating)

D4 in this run used a **lenient** accepted-set in `grade.py` (included `medium`, `already-fixed`, `schedule`). It is non-discriminating vs the schema and should be **discarded** — the schema (D3) is the real enum authority. The schema enum is strictly:
- verdict: `confirmed | partial-repro | not-reproducible | fixed-in-X | duplicate-of-#N | needs-info | wont-fix`
- severity: `critical | major | minor | trivial`
- recommended_action: `hotfix | next-cycle | backlog | close`

## Rule #6 verdict

**iteration-2 does NOT close D3.** Anti-hand-author is valid (0 regression, 8/8 script_produced confirms triage.py adoption is solid on Opus 4.7) but addresses a non-existent failure mode for this model. **D3 requires iteration-3** targeting Stage 3 enum drift + repro case_id, not hand-authoring.

## Recommendation → iteration-3

1. SKILL.md Stage 3: **inline the exact schema enums** at the verdict/severity/recommended_action fill step (don't defer to a separate conventions file)
2. SKILL.md Step 6: require `case_id` in every repro case (cite schema `ReproCase.required`)
3. Consider: `triage.py` validates the *final* report (post AI-fill) against the schema before allowing comment synthesis — mechanical enforcement beats instruction
4. Keep iteration-2 anti-hand-author as-is (defense-in-depth, no harm)

---

# iteration-2 (re-benchmark with v1.2.0 — iteration-3 real fix)

**With-skill**: v1.2.0 (Stage 3 inline schema enum table + Step 6 case_id + Stage 3.5 self-check)
**Baseline**: v1.0.0 (same snapshot, unchanged)

| Metric | with_skill v1.2.0 | old_skill v1.0.0 |
|--------|-------------------|------------------|
| D1 JSON output | 4/4 | 4/4 |
| D2 triage-comment.md | 4/4 | 4/4 |
| **D3 schema conformance** | **4/4** ✅ | **1/4** |
| D4 canonical enums (schema-strict grader) | 4/4 | 1/4 |
| D5 multi-artifact | 4/4 | 4/4 |
| script_produced | 4/4 | 4/4 |

| Cost | with_skill v1.2.0 | old_skill v1.0.0 |
|------|-------------------|------------------|
| Mean tokens | 52,306 | 50,985 |
| Mean duration | 127.4s | 105.4s |

## Conclusive delta — the real fix lands

| | with_skill | baseline v1.0.0 |
|--|-----------|-----------------|
| iteration-1 (v1.1.0 anti-hand-author) | D3 **0/4** | D3 0/4 |
| iteration-2 (v1.2.0 inline enum + self-check) | D3 **4/4** ✅ | D3 1/4 |

**D3 0/4 → 4/4 with_skill.** The 2026-05-13 D3 regression is now genuinely closed. The delta is attributable to iteration-3 (inline schema enum table at Stage 3 fill point + Stage 3.5 mechanical self-check + Step 6 case_id requirement), NOT iteration-2 anti-hand-author (which had measurably zero effect on D3 — confirming the original root-cause diagnosis was wrong for Opus 4.7).

Baseline v1.0.0 stays 1/4 (eval-4 happened to pick enum-valid words by luck; eval-1/2/3 still invent `fixed-in-v1.20.0` / `medium` / `moderate`). This proves the failure is real and the fix is causal, not eval drift.

## Root-cause learning (for methodology memory)

A benchmark's own root-cause *diagnosis* can be wrong. The 2026-05-13 benchmark observed D3 0/3 and attributed it to hand-authoring. iteration-2 tested that hypothesis directly and **disproved it** (script_produced 8/8). Only by validating the hypothesis (not just the metric) did the real cause surface: AI free-texts schema-enum fields with plausible-but-invalid values when the enums aren't inlined at the fill point. **Lesson: when re-benchmarking a carry-forward fix, test the *diagnosis*, not just re-measure the metric.**

## Rule #6 verdict (capability-type Skill, 不可协商)

**PASS.** v1.2.0 closes D3 (0/4 → 4/4) with a causal, baseline-controlled delta. Ship as **v1.21.3**. iteration-2 anti-hand-author retained as defense-in-depth (0 regression, 0 harm; valid for weaker models / future drift even though no-op on Opus 4.7).
