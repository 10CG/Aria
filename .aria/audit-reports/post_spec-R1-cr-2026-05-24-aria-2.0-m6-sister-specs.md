# Phase A.2 post_spec R1 audit — code-reviewer (combined sister Specs #2 + #3)

> **Date**: 2026-05-24
> **Reviewer**: code-reviewer agent (Combined sister-Spec R1 mode)
> **Scope**: Spec #2 `aria-2.0-m6-e2e-resilience` + Spec #3 `aria-2.0-m6-docs` at commit `5d85617`
> **Sister-Spec rationale**: drafted in parallel; cross-Spec consistency is high-priority
> **Verdict**: **NEEDS_FIX** — 4 Critical (3 cross-Spec + 1 Spec #3) + 6 Important + 4 Minor

---

## Phase 1: Specification Compliance — FAIL → Critical defects below

The two Specs are structurally well-formed and largely align with DEC-20260524-001. However, **cross-Spec coordination defects** (path notation divergence, broken BOTH-locations reciprocal cross-ref, two contradictory AD-M5-11 claims) require correction before Approved.

---

## Critical (must fix — blocks Approved)

### C1. [CROSS-SPEC] BOTH-locations path notation divergence: `aria-orch/evals/` vs `aria-orchestrator/evals/`

**Files**:
- Spec #2 `proposal.md:357, 360, 409, 411, 418, 424, 687-695, 810` — uses **`aria-orchestrator/evals/m6-prompt-quality/`** (full directory name)
- Spec #2 `tasks.md:551, 554, 565, 582, 594, 651, 656, 660, 664, 673, 681` — uses **`aria-orchestrator/evals/m6-prompt-quality/`**
- Spec #3 `proposal.md:263, 264, 451, 560` — uses **`aria-orch/evals/m6-prompt-quality/`** (abbreviated)
- Spec #3 `tasks.md:250, 274, 284, 285, 292, 432` — uses **`aria-orch/evals/m6-prompt-quality/`**

**Why it matters**:
The real on-disk path is `/home/dev/Aria/aria-orchestrator/` (verified via `ls -d /home/dev/Aria/aria-orch*`). There is no `aria-orch/` directory. Spec #3's AC-6 (proposal line 451 + tasks line 432) greps the file for `aria-orch/evals/m6-prompt-quality` — that string will be embedded literally per T-B3.2.4-T-B3.2.6 (tasks line 274, 284, 285), but it is a broken path. Anyone clicking that cross-reference will get a 404. The BOTH-locations design is undermined.

Even worse: Spec #2's reciprocal cross-ref written into the corpus footers (tasks line 582 + 681) uses the relative path `../../../../standards/autonomous/humanized-command-patterns.md` — which is correct from `aria-orchestrator/evals/m6-prompt-quality/corpus/sample-NN.md` (4 levels up = `/home/dev/Aria/standards/`). Spec #3 has the path-notation bug, not Spec #2.

**How to fix** (in Spec #3 ONLY):
Global replace in `openspec/changes/aria-2.0-m6-docs/proposal.md` and `openspec/changes/aria-2.0-m6-docs/tasks.md`:

```
s|aria-orch/evals/m6-prompt-quality|aria-orchestrator/evals/m6-prompt-quality|g
```

Specific spots:
- Spec #3 proposal.md:263 — `aria-orch/evals/m6-prompt-quality/corpus/sample-{01..10}.md` → `aria-orchestrator/evals/...`
- Spec #3 proposal.md:264 (×2 occurrences) → same
- Spec #3 proposal.md:451 (AC-6 grep target) → same
- Spec #3 proposal.md:560 (dependencies table) → same
- Spec #3 tasks.md:250 (P-11 content boundary header) → same
- Spec #3 tasks.md:274 (Lab-shareable header to be written into file) → same
- Spec #3 tasks.md:284 (BOTH-Locations Design Note text to be written) → same
- Spec #3 tasks.md:285 (See-also cross-ref text) → same
- Spec #3 tasks.md:292 (AC-6 grep) → same
- Spec #3 tasks.md:432 (Full-AC-sweep grep) → same

Owner choice: alternatively, if `aria-orch/` is the intended consumer-friendly alias, then Spec #3 must also propose a symlink task (`ln -s aria-orchestrator aria-orch`) — but this would need an AD slot decision; the simpler fix is path correction.

---

### C2. [CROSS-SPEC] AD-M5-11 claim collides with live live architecture-decisions.md reservation rationale

**Files**:
- Spec #3 `proposal.md:12` — claims AD-M5-11 "(pre-existing M5 RESERVED slot)" "is claimed by this Spec for M6 docs architectural decisions"
- Spec #3 `proposal.md:296-301, 374, 542` — assigns AD-M5-11 to `standards/autonomous/` namespace creation decision
- Spec #3 `tasks.md:8, 368-372` — Decided state with M6 docs decision content
- Live `aria-orchestrator/docs/architecture-decisions.md:3460-3478` — actual AD-M5-11 reservation reads: "M5 spec drafter 可在 M5 closeout 之后, M6 kickoff 前发现需补充的 **M5-spillover decision** (e.g. observed-in-production issue 需在 M5 文档 retroactive 记录)"
- M5 archive `openspec/archive/2026-05-23-aria-2.0-m5-replay-reconciler-drift-review-loop-audit/proposal.md:169` — different content: "AD-M5-11 | T-deploy schema migration v3→v4 3-safeguard inline (per R2 fix QA-4)"
- DEC `2026-05-24-us026-m6b-brainstorm.md:123` — says "AD-M5-11 RESERVED slot 用于 M6 docs decisions" — matches Spec #3 intent
- DEC line 128 — "AD-M5-11: pre-existing M5 reserved slot for M6 docs (Spec #3 may use)" — supports Spec #3

**Why it matters**:
Three independent sources tell three stories:
1. **DEC** (Spec #3 cites): AD-M5-11 reserved for M6 docs decisions ✓
2. **Live architecture-decisions.md** (the SoT per `[[feedback_validator_repo_drift_guard_test]]`): reserved for M5-spillover decisions only
3. **M5 archive proposal.md**: lists AD-M5-11 as "T-deploy schema migration v3→v4 3-safeguard"

The audit pattern `[[feedback_spec_frontmatter_reflects_reality]]` requires the live SoT to be the authority. Spec #3 cannot claim AD-M5-11 for `standards/autonomous/` namespace without first either (a) updating the live AD-M5-11 reservation text to acknowledge M6 docs use as a valid scope, OR (b) using a fresh AD-M6-* slot (e.g. AD-M6-9, since Spec #3 only uses AD-M6-7/8).

**How to fix** (pick one):
- **Option A (preferred)**: Update Spec #3 to use **AD-M6-9** instead of claiming AD-M5-11. Phase B implementer adds AD-M6-9 to architecture-decisions.md normally. Spec #3 frontmatter line 12 and T-B6 must change `AD-M5-11` → `AD-M6-9`.
- **Option B**: Add a Phase B subtask (T-B6.0) that explicitly modifies the live AD-M5-11 reservation rationale at architecture-decisions.md:3478 to read "AD-M5-11 reserved for M5-spillover decisions OR M6 docs architectural decisions (per DEC-20260524-001 §2)". Document this redefinition in the AD-M5-11 body itself with a "Note: reservation scope expanded 2026-05-24 per Spec #3".

Spec #3 currently does neither. The AC-10 grep `grep -q "AD-M5-11"` passes only because the slot heading already exists — but the existing content is unrelated to M6 docs and would still pass grep. This is paper compliance per `[[feedback_paper_fix_antipattern]]`.

---

### C3. [CROSS-SPEC] PRD line citations are off by 10-20 lines (frontmatter drift after `a786444` patch)

**Files**:
- Spec #2 `proposal.md:7` — cites "PRD `a786444` PRD patch, §638-646" (Cost gate)
- Spec #2 `proposal.md:30` — cites "PRD §630 requires a sustained 168-hour window"
- Spec #2 `proposal.md:39` — cites "PRD §634 enumerates 3 infra crash modes"
- Spec #2 `proposal.md:42` — cites "PRD §634 sub-clauses"
- Spec #2 `proposal.md:47-50` — cites "PRD §639 rubric"
- Spec #2 `proposal.md:278, 745, 832, 833` — cites "PRD §634" or "§639"

**Actual PRD line locations** (verified via `awk 'NR>=630 && NR<=660'`):
- §630 = blank
- §631 = `### M1 验证 (基线)` (NOT 7-day, M6)
- §634 = "Dockerfile 可构建" (M1, NOT WAL crash modes)
- §637 = `### M6 验证 (发版前)` (header)
- §639 = `**定量指标**:` (NOT rubric)
- §642-646 = Cost gate dual-track (matches Spec #2 cite for cost gate)
- §648-651 = Crash recovery 3 modes (NOT §634)
- §651 = WAL truncation (NOT §634)
- §656 = `拟人命令质量 (人工评分, 10 samples 平均 ≥ 7/10)` (rubric line, NOT §639)

**Why it matters**:
Per `[[feedback_spec_frontmatter_reflects_reality]]` and `[[feedback_spec_v2_body_propagation_2pass]]`: every cross-ref must be byte-accurate or it fails audit trust. Future readers (and AC verification scripts) following "PRD §634" will land on Dockerfile content, not WAL. The error pattern suggests Spec #2 drafted against a pre-patch PRD numbering and was not re-verified after `a786444`.

**How to fix** (Spec #2 only, Spec #3 doesn't cite PRD lines):
Apply these exact replacements in Spec #2 `proposal.md`:

| Current cite | Correct cite | Locations |
|--------------|--------------|-----------|
| PRD §630 (7-day uptime) | PRD §637 + §640 | line 30 |
| PRD §634 (WAL/crash modes) | PRD §648-651 | lines 39, 42, 278, 745, 832 |
| PRD §639 (rubric) | PRD §656 | lines 47, 50, 833 |
| PRD §638-646 (cost gate) | PRD §642-646 | line 7 |

Recommended: change line 7 from `(§638-646)` to `(§642-646)` and add `(crash recovery: §648-651; rubric: §656)`. Then in body, replace `§634` and `§639` per table above.

---

### C4. [SPEC #3] Diff 9 plugin-version delta is inconsistent: v1.22.0 (live CLAUDE.md) vs v1.26.0 (DEC) vs v1.27.0 (Spec #3)

**Files**:
- Live `CLAUDE.md:434` — `插件版本: v1.22.0`
- DEC `2026-05-24-us026-m6b-brainstorm.md:109` — "Diff 9 增量: Rule #7/#8/#9 + 插件版本 catch-up v1.26.0"
- Spec #3 `proposal.md:23, 74, 86, 90, 102, 225, 411-413` — "v1.22.0 → v1.27.0", "must reference v1.27.0"
- Actual live plugin `aria/.claude-plugin/plugin.json` — version `1.27.0` ✓ (verified via Python json)
- Submodule bump commit `c7e611f` — "bump aria pointer to v1.27.0 (1b8ec3f)" ✓

**Why it matters**:
DEC says v1.26.0; Spec #3 says v1.27.0. The live plugin is v1.27.0 (correct), so Spec #3's target is RIGHT but its source-of-truth claim "per DEC" is OFF (DEC was drafted before c7e611f bump). Per `[[feedback_spec_frontmatter_reflects_reality]]`: if the Spec disagrees with the DEC, the Spec must explicitly note the deviation.

**How to fix** (Spec #3 ONLY):
Add a one-line note after `proposal.md:23` (Problem 1 paragraph):
```
> Note: DEC §2 line 109 originally said v1.26.0; v1.27.0 is the live value (per submodule bump c7e611f post-DEC). Spec #3 tracks live plugin.json as SoT per [[feedback_spec_frontmatter_reflects_reality]].
```

Then `proposal.md:74` already says "per commit `c7e611f`" — verify same commit also referenced in `proposal.md:86`. ✓ (line 86 already says "per commit `c7e611f` submodule bump to `1b8ec3f`").

This is C4 (Critical) rather than Important because Spec #3 R1 audit grep will surface DEC vs Spec disagreement and block Approved if drift isn't explicitly acknowledged.

---

## Important (should fix — before Phase B kickoff)

### I1. [CROSS-SPEC] Audit trajectory placeholder asymmetric: Spec #2 has it, Spec #3 does not

**Files**:
- Spec #2 `proposal.md:20-22` — has frontmatter audit trajectory placeholder:
  ```
  > **Audit trajectory**:
  >   - Phase A.2 R1 pending (post_spec 4-agent parallel audit)
  >   <!-- R1 audit aggregate to be inserted here after Phase A.2 -->
  ```
- Spec #3 — has NO equivalent frontmatter clause.

**Why it matters**:
Per Spec #1's R1-R2 audit pattern (`feedback_audit_driven_fix_conventions` + Spec #1 final frontmatter 6-line audit trajectory entries), both sister Specs should start identical. R1 audit aggregate insertion ergonomics suffer if Spec #3 has no placeholder.

**How to fix** (Spec #3 only):
Insert after Spec #3 `proposal.md:14` (after the Sibling Spec parallel-draft line), before `**Successor**`:
```
> **Audit trajectory**:
>   - Phase A.2 R1 pending (post_spec 4-agent parallel audit — combined sister-Spec mode with #2)
>   <!-- R1 audit aggregate to be inserted here after Phase A.2 -->
```

---

### I2. [CROSS-SPEC] Inline R1-XX fix-trail trace pattern not reserved in either Spec

**Files**: Neither Spec mentions "R1-XX fix:" inline trace pattern, despite drafter promise.

**Why it matters**:
Per `[[feedback_audit_driven_fix_conventions]]`: post-R1 fix passes embed inline `<!-- R1-N1-cr fix: <one-line description> -->` traces at edit sites so the audit-to-fix chain stays auditable. Drafter report (per task prompt) claimed Spec #2 mentions "fix-trail pattern reserved for upcoming R1 audit" — grep found 0 matches.

**How to fix** (BOTH Specs):
Add to §Constraints section in both proposal.md:
```
### Audit fix-trail trace pattern

Post-R1 fix passes must embed inline traces at each fix site using:
`<!-- R1-<ID>-<agent> fix: <one-line description> -->`
where `<ID>` matches the R1 audit report finding ID and `<agent>` is one of {tl, ba, qa, km, cr, ai}.
Audit aggregate frontmatter table (inserted after R1 completes) cross-references each trace
back to its R1 finding row. Per `[[feedback_audit_driven_fix_conventions]]`.
```

---

### I3. [SPEC #2] §C.3 cross-ref relative path depth (4 `../`) needs verify

**File**: Spec #2 `proposal.md:418` + `tasks.md:582, 681`
```markdown
*Cross-reference: [standards/autonomous/humanized-command-patterns.md](../../../../standards/autonomous/humanized-command-patterns.md)
```

**Why it matters**:
From `aria-orchestrator/evals/m6-prompt-quality/corpus/sample-NN.md`, the path to `/home/dev/Aria/standards/`:
- `corpus/` → `m6-prompt-quality/` (1 up)
- → `evals/` (2 up)
- → `aria-orchestrator/` (3 up)
- → `/home/dev/Aria/` (4 up)

So `../../../../standards/autonomous/humanized-command-patterns.md` = correct ✓

But the analogous link from `aria-orchestrator/docs/layer-boundary-contract.md` (Spec #3 B.4) would need `../../standards/...`, not the same depth. Spec #3 tasks.md line 313 says "Cross-reference `standards/autonomous/humanized-command-patterns.md` for curated examples" but does NOT specify the relative path format. Minor risk of broken links in B.4.

**How to fix** (Spec #3):
Add to T-B4.3 (tasks.md:313):
```
Use relative path `../../standards/autonomous/humanized-command-patterns.md` from `aria-orchestrator/docs/layer-boundary-contract.md`. Verify with `realpath` or by clicking the rendered link.
```

---

### I4. [SPEC #2] Effort baseline arithmetic: midpoints sum to 27.5h, frontmatter says 29h

**File**: Spec #2 `proposal.md:11, 749-792`

**Why it matters**:
Sum of midpoints in §Effort baseline body:
- TG-A: 1+2+1+0.5+1.5+0.5+1+0.5+1 = 9h (subtotal says 9-10h)
- TG-B: 2+1+1+2+0.5+0.5+0.5+2.5+1.5+1 = 12.5h (subtotal says 12.5-13h)
- TG-C: 1+2+1.5+0.5+0.5+0.5 = 6h ✓
- Sum of midpoints: 9 + 12.5 + 6 = **27.5h**, but body says "≈ 29h"

Per `[[feedback_spec_v2_body_propagation_2pass]]`: the body sum must match the frontmatter h declaration. Tasks.md TG overview table (line 30-44) sums to 28h + 1h Q-NEW-1 = 29h. The gap is in proposal.md §Effort baseline.

**How to fix** (Spec #2):
Either (a) bump TG-A items to total 10h instead of 9h (add 0.5-1h somewhere), or (b) update §Effort baseline body to read "≈ 27.5-29h" and frontmatter to "~28h impl (~9h TG-A + ~12.5h TG-B + ~6h TG-C + ~0.5h buffer)". Recommended (b).

---

### I5. [SPEC #3] AC-6 has malformed compound bash logic — fails-open on file missing

**File**: Spec #3 `proposal.md:446-454`
```bash
[ -f standards/autonomous/decision-autonomy-matrix.md ] \
  && [ -f standards/autonomous/humanized-command-patterns.md ] \
  && grep -q "Lab-shareable" standards/autonomous/decision-autonomy-matrix.md \
  && grep -q "Lab-shareable" standards/autonomous/humanized-command-patterns.md \
  && grep -q "aria-orch/evals/m6-prompt-quality" standards/autonomous/humanized-command-patterns.md \
  && exit 0
# Minimum line count for humanized-command-patterns.md:
[ $(wc -l < standards/autonomous/humanized-command-patterns.md) -ge 200 ] && exit 0
```

**Why it matters**:
The first `&& exit 0` only fires on full success. If a file is missing, control falls through to `wc -l < <missing-file>` which produces 0 (stderr "No such file"), causing the second test to fail. Then script exits with the last command's exit status — likely 1 from the `[`, but `exit 0` doesn't fire either. The structure suggests intent of "AND both checks must pass" but is written as two independent checks.

Per `[[feedback_falsifiable_evidence_for_binary_acceptance]]`: ACs must produce deterministic PASS/FAIL signals.

**How to fix** (Spec #3):
Rewrite AC-6 as a single compound test:
```bash
[ -f standards/autonomous/decision-autonomy-matrix.md ] \
  && [ -f standards/autonomous/humanized-command-patterns.md ] \
  && grep -q "Lab-shareable" standards/autonomous/decision-autonomy-matrix.md \
  && grep -q "Lab-shareable" standards/autonomous/humanized-command-patterns.md \
  && grep -q "aria-orchestrator/evals/m6-prompt-quality" standards/autonomous/humanized-command-patterns.md \
  && [ "$(wc -l < standards/autonomous/humanized-command-patterns.md)" -ge 200 ] \
  && echo "PASS AC-6" && exit 0
echo "FAIL AC-6" && exit 1
```
(Also incorporates C1 path fix.)

---

### I6. [SPEC #3] T-B0 submodule sequence T-B0.4 has forward-reference loop with T-B3

**File**: Spec #3 `tasks.md:171, 297-299`
```
- [ ] T-B0.4 Implement T-B3 (create files in `standards/autonomous/`). Return here after T-B3 subtasks complete.
...
- [ ] T-B3.3.1 Return to T-B0.5 and complete the commit + push + merge + pointer bump sequence.
```

**Why it matters**:
The runbook has a circular reference: T-B0.4 → T-B3 → T-B3.3.1 → T-B0.5. This is intentional, but it violates `[[feedback_validator_repo_drift_guard_test]]` discipline of executable runbook ordering — a Phase B implementer reading the file linearly might not realize T-B0.4 is a pause point. Idempotency notes per step also missing (only T-B0.10 mentions verification; T-B0.5/.6/.7/.8 don't say "if already done, skip").

**How to fix** (Spec #3):
1. Rename T-B0 to `T-B0.A` (pre-B3) and T-B0.5-.10 to `T-B0.B` (post-B3). Make it explicit:
   ```
   ### T-B0.A: Standards submodule setup (run BEFORE T-B3) (~0.1h)
   ### T-B0.B: Standards submodule commit + bump (run AFTER T-B3 file creation) (~0.4h)
   ```
2. Add idempotency note to T-B0.A.1: "If `feat/autonomous-docs` branch already exists, `git -C standards checkout feat/autonomous-docs` instead of creating."
3. Add to T-B3.3: "Prerequisite: T-B3.1 and T-B3.2 files exist and are committed locally in standards submodule (T-B0.A.5 complete)."

---

## Minor (nice to have)

### M1. [CROSS-SPEC] Spec #2 cites m5-handoff.yaml "lines 151-172" — line 172 is blank

**File**: Spec #2 `proposal.md:12, 819`

m5-handoff.yaml lines 151-171 contain the 5 promises (verified). Line 172 is blank separator before next section. Citing "151-172" includes a blank line — semantically harmless but pedantically inaccurate.

**Fix**: change `(lines 151-172` → `(lines 151-171` in both Spec #2 spots.

### M2. [SPEC #3] DEC §2 line 22 "AI-DDD 方法论" doc not explicit in Spec #3

DEC §1 Q4 high-level scope mentions "AI-DDD 方法论" doc, but DEC §2 detailed Spec #3 scope list does not. Spec #3 absorbs this into CLAUDE.md Diffs 1-2 (which redefine 项目本质 to include AI-DDD methodology). Acceptable, but worth a §What note: "Note: The 'AI-DDD methodology doc' mentioned in DEC §1 Q4 is delivered via CLAUDE.md Diff 1-3 + Diff 7 (new §Aria 2.0 运行时 chapter)."

**Fix**: Add the note above as a §What footnote.

### M3. [SPEC #2] Tasks.md line 7 effort header drops "Phase A audit overhead ~1h"

Spec #2 proposal.md frontmatter line 11 says "Phase A audit overhead ~1h (not impl) — single SoT". Spec #2 tasks.md line 7 (Estimated total) doesn't mention Phase A overhead. Per `[[feedback_spec_v2_body_propagation_2pass]]` single SoT: the audit overhead should appear in both frontmatters or neither.

**Fix**: Add to tasks.md line 7: `(~29h impl + ~1h Phase A audit overhead, separately tracked)`.

### M4. [SPEC #3] PRD §553 line cite verification

Spec #3 `proposal.md:582` cites "PRD §553 — decision autonomy matrix rationale". Per `awk` verify (not re-run here, but should verify): if PRD line numbering also drifted after `a786444`, this cite may be off.

**Fix**: Phase B implementer must verify §553 line content during T-B3.1.4 drafting; if drifted, update the cite.

---

## Strengths

### What both Specs do well

1. **DEC §2 ↔ §What mapping**: Both Specs map almost 1:1 to DEC §2 Spec #N detailed scope. No scope creep, minimal drops (only DEC Q4 high-level "AI-DDD methodology doc" is absorbed via CLAUDE.md, which is a reasonable interpretation).

2. **AD-M6 allocation coherence**: Spec #1 holds AD-M6-1/2/3 (confirmed Approved in c29a800), Spec #2 holds AD-M6-4/5/6 (frontmatter line 18, body §How table line 549, slot Decided content), Spec #3 holds AD-M6-7/8 (frontmatter line 12, body line 375-376). No slot overlap. Each "claimed" slot has actual content (AD-M6-8 is correctly Reserved-with-retire-checkpoint per `[[feedback_ad_slot_backfill_checkpoint]]`).

3. **REPO_ROOT canonical pattern (Spec #2)**: All Python script tasks in `tasks.md` correctly use `HERE = Path(__file__).resolve().parent; REPO_ROOT = HERE.parent` per Spec #1 R2-C-tl-N1 lesson. 5 occurrences (lines 107-108, 151-152, 269-270, 287-288). REPO_ROOT pattern §Constraints block at proposal.md:451-473 explicitly documents the `.parent.parent` antipattern. Excellent dogfood of prior R2 audit finding.

4. **provider_cost_model SoT (Spec #2)**: §Constraints line 477-480 codifies "There is NO `provider` column. Any SQL that filters by provider type must use `WHERE provider_cost_model = '<value>'`". Tasks.md line 164 reinforces. Zero `WHERE provider = '<value>'` callsites in the proposal/tasks. Spec #1 R1-C1 lesson properly carried forward.

5. **Mock-layer matrix completeness (Spec #2)**: Exactly 6 rows verified (Infra-1/2/3 + LLM-4/5/6), 4 SDK + 2 HTTP per Q-NEW-1 hybrid. Mock-shape discipline cite `[[feedback_test_mock_pattern_hides_prod_bug]]` + `[[feedback_mock_layer_per_failure_semantic]]` per row in §B.1.

6. **CLAUDE.md Rule #5 compliance**: Both Specs at `openspec/changes/aria-2.0-m6-*/` (project /openspec/, NOT standards/openspec/). ✓

7. **CLAUDE.md 9 diffs vs reality (Spec #3)**: Verified all 9 diff targets exist in live CLAUDE.md:
   - Diff 1 target = lines 1-7 (项目本质/核心假设/版本) ✓
   - Diff 2 target = §项目定位 §研究目标 (lines 32-37) ✓
   - Diff 3 target = §核心概念 §十步循环 (lines 40-66) ✓
   - Diff 4 target = §信息地图 子模块表 (lines 124-129) ✓
   - Diff 5 target = §技术约束 (lines 208-227) ✓
   - Diff 6 NO-OP — Rules #1-#6 (lines 347-378) preserved verbatim ✓ (verified by reading them)
   - Diff 7 target = after §不可协商规则 (line 426+, before final block) ✓
   - Diff 8 target = §项目状态 (lines 429-437) ✓
   - Diff 9 target = top-level 版本 (line 5) ✓
   All anchors exist.

8. **state-checks.yaml 3 probes additive**: Verified existing checks `issue-cache-freshness` + `silknode-contract-deferral-expiry` (2 entries). New probes `m6-version-badge-match` / `m6-claude-md-version` / `m6-arch-doc-stale` are name-collision-free. YAML syntax each probe is valid (verified by structure). Each probe has both PASS and FAIL test rationale in T-A6.1-.3.

9. **Lab-shareable vs Aria-specific boundary in P-11**: Spec #3 expresses the rule clearly:
   - proposal.md:300-301 — "Lab-shareable patterns benefit from being in the shared standards submodule; Aria-specific contracts would pollute standards/ with Aria internals"
   - tasks.md:308 — "<!-- Aria-specific: this file is NOT Lab-shareable. It belongs in aria-orchestrator/docs/, not in standards/. Per km M-km-R2-005 decision recorded in AD-M5-11. -->"
   The boundary is enforced via file header AND header comment in source. Good defense-in-depth.

10. **TG-DOCS-B v2.0.1-deferrable as 1st-class clause**: Spec #3 frontmatter line 11 (front-and-center), reinforced at lines 198 (§What header), 331 (§Constraints), and within release notes T-A3.5 (tasks.md:88). Not buried in prose. ✓

11. **Memory refs all resolve**: 15/15 `[[name]]` refs in both Specs exist in `/home/dev/.claude/projects/-home-dev-Aria/memory/` (verified by file existence check). Zero broken refs.

12. **CLAUDE.md Rule #8 compliance**: Neither Spec proposes "merge to master without aether ci status check" in Phase C tasks. ✓

13. **Status enum clean**: All 4 files frontmatter show `Status: Draft` with NO parenthetical annotation (per Spec #1 I-R1-5 lesson). ✓

14. **c29a800 sibling-Spec citation accuracy**: Verified `git log --oneline c29a800 -1` → "feat(openspec): Spec #1 aria-2.0-m6-cost-acceptance CONVERGED Approved". Both Specs cite this correctly.

15. **m5-handoff.yaml line 155 citation (Spec #2)**: While the 155 reference is technically the enforcement line of promise #1 (not the promise header), the cite matches DEC §7 precedent (DEC also cites line 155). Self-consistent across DEC + Spec #2.

---

## Recommendations

1. **Adopt Path canonical form across all M6 Specs**: Use `aria-orchestrator/` (full) consistently. Add an entry to `[[feedback_spec_v2_body_propagation_2pass]]` memory: "Cross-Spec path notation: choose one canonical form (full vs abbreviated) and grep-enforce."

2. **Cross-Spec audit add-on**: When sister Specs are drafted in parallel, a 5-min "path token diff" should be run between proposal.md files. Specifically: `comm -3 <(grep -oE 'aria-orch[^\s)]*' Spec2.md | sort -u) <(grep -oE 'aria-orch[^\s)]*' Spec3.md | sort -u)` would have surfaced C1 in seconds.

3. **AD-M5-11 redefinition memo**: If Option B (Spec #3 C2 fix) chosen, write a 1-line memo in `aria-orchestrator/docs/architecture-decisions.md:3478` AD-M5-11 body: "Reservation scope expanded 2026-05-24 per Spec #3 (M6 docs decisions valid scope; see AD-M6-7 sibling)." Otherwise prefer Option A (use AD-M6-9).

4. **PRD line citation freezing**: Add a Phase A precision item to the M6 brainstorm follow-up: "Any PRD line cite in M6 Specs must be re-verified against current PRD at Spec Approve time, since PRD `a786444` patch shifted line numbers ±5-15 lines." This pattern will recur in Spec #4.

5. **Consider sister-Spec joint audit-trajectory section**: A combined Spec #2 + #3 audit trajectory table inserted in both frontmatters could enable cross-audit cross-reference (e.g., "R1-cr-C1 affects both Specs").

---

## Assessment

**Can the Specs proceed to R2?**: **Yes**, after C1-C4 are fixed (Critical, ~30-45min to apply).

**Rationale**: The core scope, structure, AD allocation, REPO_ROOT pattern, mock-layer matrix, memory ref linkage, and DEC §2 mapping are sound. The defects are all cross-reference / cross-Spec coordination issues — exactly the class of defect combined R1 audit is designed to surface. None are structural; all have specific exact-replacement fixes proposed above. Effort to fix Critical = ~30-45min (mostly mechanical sed). Important fixes ~1h. Total R1 turnaround estimate: ~1.5-2h pre-R2.

**Reviewer recommendation**: Apply C1 (sed s|aria-orch|aria-orchestrator|g in Spec #3 only) + C2 (switch to AD-M6-9 in Spec #3) + C3 (PRD line citation table replacements in Spec #2) + C4 (DEC v1.26 vs Spec v1.27 deviation note in Spec #3) before R2 dispatch.

---

**Audit completed**: 2026-05-24
**Reviewer**: code-reviewer (R1, combined sister-Spec mode)
**Time budget consumed**: ~18min
**Next**: Aggregate with tl/ba/qa/ai R1 reports → R1 audit aggregate → fix-pass → R2
