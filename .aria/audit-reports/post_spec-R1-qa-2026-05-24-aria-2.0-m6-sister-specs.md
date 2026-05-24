# Post-Spec R1 QA Audit — Combined Spec #2 + Spec #3 (2026-05-24)

> **Role**: qa-engineer (R1, combined-Spec mode)
> **Specs audited**: `aria-2.0-m6-e2e-resilience` (Spec #2) + `aria-2.0-m6-docs` (Spec #3)
> **Commit**: `5d85617`
> **Methodology**: stress-test AC falsifiability + test coverage + edge cases + production failure modes
> **Memory refs**: `[[feedback_falsifiable_evidence_for_binary_acceptance]]`, `[[feedback_mock_layer_per_failure_semantic]]`, `[[feedback_pre_draft_bug_hunt_discipline]]`, `[[feedback_validator_repo_drift_guard_test]]`

---

## Summary verdict

| Category | Spec #2 | Spec #3 | Combined |
|----------|---------|---------|---------|
| Critical | 6 | 3 | **9** |
| Important | 6 | 5 | **11** |
| Observation | 2 | 1 | 3 |

**R1 verdict**: NEEDS_FIX — critical findings require AC rewording before Phase A.3 agent allocation. Six of the nine critical items have exact rewordings proposed below; Phase B implementers cannot produce binary evidence for the current text.

---

## CRITICAL FINDINGS

### C-1 [Spec #2 AC-1] — Nomad API `StartedAt` vs actual uptime: wrong metric on restart

**Location**: proposal.md §A.1, tasks.md A-uptime-1, AC-1

**Finding**: The uptime check reads `data['TaskStates']['aria-layer1']['StartedAt']` from the Nomad alloc status JSON. `StartedAt` reflects the last task restart within the same alloc, not the alloc creation time. If the alloc restarts the aria-layer1 task (e.g., after a crash recovery) mid-run, `StartedAt` resets to the restart time. A 7-day alloc that had a task restart on Day 6 would show `StartedAt` = ~24h ago and would **fail AC-1** even though the alloc (and most of the run) was continuous.

More critically, `StartedAt` is also the correct field to use for detecting a task-level restart — but the Spec frames it as "alloc uptime" which implies the full 168-hour window. The distinction matters: alloc uptime (alloc ID stable) ≠ task uptime (StartedAt continuous).

**Binary-PASS risk**: false-FAIL on legitimate 168h runs with transient task restarts; false-PASS on alloc restarts that created a new alloc ID with StartedAt near Day-0 of a re-run.

**Exact reword for AC-1 evidence block**:

Replace the existing uptime check with a two-tier verification:

```python
# Tier 1: alloc existence (not restarted mid-run)
alloc_id = open('.aria/probes/m6-alloc-id.txt').read().strip()
result = subprocess.run(
    ['nomad', 'alloc', 'status', alloc_id, '-json'],
    capture_output=True, text=True, timeout=30
)
data = json.loads(result.stdout)
# Tier 2: task start time for the ORIGINAL Day-1 probe
# Owner records StartedAt in m6-7d-day-1.md at Day-1 start.
# AC-1 reads it from day-1 probe (source of truth), NOT from live API.
day1_probe = open('.aria/probes/m6-7d-day-1.md').read()
started_at_str = re.search(r'StartedAt:\s*(.+)', day1_probe).group(1).strip()
started_at = datetime.fromisoformat(started_at_str)
uptime_s = (datetime.now(timezone.utc) - started_at).total_seconds()
assert uptime_s >= 604800, f"FAIL AC-1: uptime {uptime_s/3600:.1f}h < 168h"
# Also verify alloc ID has not changed (no full restart)
assert data['ID'] == alloc_id, f"FAIL AC-1: alloc ID changed — full restart detected"
```

Add to AC-1 evidence: "Day-1 probe `StartedAt` line is the canonical clock start; live API confirms same alloc ID still active."

---

### C-2 [Spec #2 AC-2] — Dispatch count boundary: exactly 9 dispatches is silent gap

**Location**: proposal.md §A.2, AC-2, tasks.md A-dispatch-4

**Finding**: The Spec says `total >= 10` (PASS) vs `total < 10` (FAIL). The boundary is correctly specified as `>=`. However, tasks.md A-dispatch-4 writes the unit test fixture as "9 total → FAIL" which is correct. The problem is the **synthetic cap SQL** has a division-by-zero risk: if `total2 = 0` (no S9 dispatches at all), `synth_count / total2` raises `ZeroDivisionError` before the `>= 10` check fires. The acceptance script could crash with exit 2 (infrastructure error) when it should emit `[FAIL] AC-2: total S9 dispatches 0 < 10`.

Additionally, the stratification check for `('bug', 'feature', 'stale')` runs three separate queries. If total = 9, the stratification queries may all return >= 1 (e.g., 3 bug + 3 feature + 3 stale = 9 total), and the stratification loop passes before the total count assertion fires. The **order of checks in the acceptance script matters**: total count must be asserted BEFORE stratification to prevent misleading partial-PASS output.

**Exact reword for AC-2 acceptance code** (add guard before synthetic cap):

```python
total = cur.fetchone()[0]
if total == 0:
    print(f"[FAIL] AC-2: total S9 dispatches 0 < 10")
    sys.exit(1)
assert total >= 10, f"FAIL AC-2: total S9 dispatches {total} < 10"
# Only then proceed to synthetic cap check (denominator guaranteed > 0)
```

Add to tasks.md A-dispatch-4: "Fixture with total=0 → exit 1 `[FAIL] AC-2: total S9 dispatches 0 < 10` (not ZeroDivisionError exit 2)."

---

### C-3 [Spec #2 AC-3 / TG-B] — LLM-4 provider specificity gap: only Zhipu or Luxeno tested, not both

**Location**: proposal.md §B.1 (LLM-4 row), tasks.md B-llm-1

**Finding**: LLM-4 covers "429 rate-limit mid-transition (S2/S3/S6 LLM call)". Per `[[project_glm_routing_luxeno]]`, Layer 1 uses Luxeno and Layer 2 uses Zhipu — two different provider SDK clients. The mock `llm_client.complete()` raises `RateLimitError(retry_after=30)` but the Spec does not specify which provider's `llm_client` is under test. If `test_crash_llm4.py` only mocks the Layer 2 (Zhipu) client, the Layer 1 (Luxeno) 429 path is untested. These are different code paths with different SDK adapter implementations.

The mock-layer-per-mode matrix says "SDK boundary (`llm_client.complete()` raises `RateLimitError`)" without specifying which of the two clients. With two providers, this is an underspecified test.

**Binary-PASS risk**: test passes against one provider's client; the other provider's client has a different `RateLimitError` attribute shape or different retry logic, hiding a real production bug per `[[feedback_test_mock_pattern_hides_prod_bug]]`.

**Exact reword for §B.1 LLM-4 row and tasks.md B-llm-1**:

Replace the single LLM-4 test with two sub-tests:
- `test_crash_llm4_layer2_zhipu`: mock `aria_layer1.llm_client.ZhipuClient.complete` (Layer 2 path, S3/S6 calls).
- `test_crash_llm4_layer1_luxeno`: mock `aria_layer1.llm_client.LuxenoClient.complete` (Layer 1 path, S2 calls — triage/planning LLM).

Each mock uses the exact `RateLimitError` subclass from that provider's SDK adapter. AC-3 evidence must show both test functions present in `test_crash_llm4.py`.

Alternatively, if the codebase uses a single unified `LLMClient` interface that routes to both providers, the Spec must cite that interface class explicitly and explain why a single mock is sufficient (with a `# provider-unified-ok: <reason>` comment in the test file).

---

### C-4 [Spec #2 AC-4] — `--cov-fail-under=100` not tied to CI execution: wishful coverage

**Location**: proposal.md §B.3, AC-4, tasks.md B-sm-4

**Finding**: AC-4 evidence is:
```bash
pytest ... --cov=aria_layer1.state_machine --cov-fail-under=100
```
The Spec specifies this as the evidence command but does not mandate that it runs in CI (no `pytest.ini`, `setup.cfg`, or `pyproject.toml` `addopts` requirement). Per `[[feedback_falsifiable_evidence_for_binary_acceptance]]`, an AC that can only be verified by manually running a command is not binary-falsifiable in PR review context.

More critically: `--cov=aria_layer1.state_machine` measures coverage of the `state_machine` module, but `test_state_machine_stochastic_replay.py` tests S2/S3/S6 transitions which are in the stochastic path. If the stochastic tests mock `llm_client.complete()` and branch into the same `state_machine.py` code, the 100% target may depend on stochastic tests covering deterministic branches. This creates a coverage interdependency that should be explicit.

**Exact reword for AC-4**:

Add to AC-4:

"This command must be added to `aria-orchestrator/pyproject.toml` (or `setup.cfg`) under `[tool.pytest.ini_options]` so it runs automatically on every `pytest` invocation in CI:
```toml
[tool.pytest.ini_options]
addopts = '--cov=aria_layer1.state_machine --cov-fail-under=100 --cov-report=term-missing'
```
Binary-PASS requires CI green (not manual run only). If the `addopts` approach conflicts with other test configurations, add a dedicated `pytest.ini` or `tox.ini` target.

Additionally, add a task in tasks.md T-B-sm-coverage: verify coverage does NOT drop below 100% when `test_state_machine_stochastic_replay.py` is excluded from the run:
```bash
pytest aria-orchestrator/tests/test_state_machine_deterministic.py \
  --cov=aria_layer1.state_machine --cov-fail-under=100
```
This confirms deterministic tests alone provide 100% coverage of deterministic paths, not relying on stochastic test side effects."

---

### C-5 [Spec #2 AC-5 + Spec #3 AC-6] — BOTH-locations cross-ref: shipping order creates AC-5 false-FAIL

**Location**: Spec #2 proposal.md §C.3, AC-5; Spec #3 proposal.md §B.3.2; both Dependencies sections

**Finding**: Spec #2 AC-5 includes:
```bash
grep -l "humanized-command-patterns.md" aria-orchestrator/evals/m6-prompt-quality/corpus/sample-*.md | wc -l
# must output 10
```
This grep looks for a reference to `standards/autonomous/humanized-command-patterns.md`. But the file `standards/autonomous/humanized-command-patterns.md` is created by **Spec #3 TG-DOCS-B** — which is v2.0.1-deferrable. If TG-DOCS-B slips to v2.0.1, `humanized-command-patterns.md` does not exist during Spec #2 Phase C verification.

Result: Spec #2 AC-5 as written only checks for a **string reference** in the sample files (the file referenced need not exist). The cross-ref footer template in tasks.md C-corpus-3 hardcodes the path string. So AC-5 grep will **pass** even if Spec #3 TG-DOCS-B has not shipped — because it checks for the string, not the file's existence. This is actually not a false-FAIL risk but a **false-PASS** risk: AC-5 passes without verifying the referenced file is real.

However, the inverse problem exists for Spec #3 AC-6:
```bash
grep -q "aria-orch/evals/m6-prompt-quality" standards/autonomous/humanized-command-patterns.md
```
This will fail if Spec #2 TG-C has not yet committed the corpus directory. Spec #3 AC-6 has an implicit dependency on Spec #2 TG-C completing first.

The Spec #2 Dependencies section says "shipping Spec #2 TG-C before Spec #3 TG-DOCS-B is preferred but not strictly blocking" — but does not resolve the AC-6 dependency problem.

**Exact reword**:

In Spec #2 AC-5, add a conditional check:
```bash
# If Spec #3 TG-DOCS-B has shipped, also verify file existence:
if [ -f "standards/autonomous/humanized-command-patterns.md" ]; then
  echo "[INFO] AC-5: Spec #3 TG-DOCS-B shipped — file existence confirmed"
else
  echo "[WARN] AC-5: Spec #3 TG-DOCS-B not yet shipped — cross-ref string present, file pending"
fi
```

In Spec #3 AC-6, add: "This AC verification must run AFTER Spec #2 TG-C corpus directory is committed. If `aria-orchestrator/evals/m6-prompt-quality/` does not yet exist, substitute: `echo 'WARN AC-6: Spec #2 TG-C corpus not yet committed — cross-ref path pending'` (non-failing WARN). AC-6 final PASS requires the full grep to succeed."

Document the verified sequencing contract: "Spec #2 TG-C corpus templates can be committed before TG-A E2E run completes (they are empty templates). Spec #3 AC-6 may be run after those templates are committed."

---

### C-6 [Spec #2 AC-7] — Double-implementation risk: who ships `validate-m6-handoff.py`?

**Location**: Spec #2 proposal.md §A.7, AC-7; Spec #1 proposal.md (reference)

**Finding**: Spec #2 AC-7 says:
```bash
python3 aria-orchestrator/docs/validate-m6-handoff.py --check-abi-compat
```
And: "The validate-m6-handoff.py script (Spec #1, already shipped) must have a **paired test triple**."

Spec #2 Dependencies section says: "`aria-orchestrator/docs/validate-m6-handoff.py` — Upstream (Spec #1 deliverable); must be shipped by Spec #1 before TG-A Phase B completes."

This is partially clear, but §A.7 says Spec #2 "must have a paired test triple" which implies Spec #2 ADDS test triple tests to the script. However, the script itself was shipped by Spec #1. The ownership boundary is:
- Spec #1 owns: the script file and its existing `--check-abi-compat` flag implementation.
- Spec #2 adds: 3 new unit tests in `test_validate_m6_handoff_tga_compat.py`.

What is undefined: does Spec #2 need to ADD any new `--check-abi-compat` sub-checks to the script (for the migration-005 triggers), or only add tests? If Spec #2 adds checks to a Spec #1 file without declaring it, this is an undeclared cross-Spec mutation.

Per tasks.md A-acceptance-2, Spec #2 also adds `--check-abi-compat` sub-check invocation to `check-m6-e2e-acceptance.py` (a Spec #2 NEW file). This is fine. But A-validate-1 Test 3 calls `validate-m6-handoff.py --check-abi-compat` and asserts all 5 promise IDs appear in stdout. If Spec #1's existing script already covers all 5 promise IDs, this test works. If not, Spec #2's test will fail against Spec #1's script unless Spec #2 also modifies the script — which is undeclared.

**Exact reword for §A.7**:

Add explicit ownership statement:

"Spec #2 DOES NOT modify `validate-m6-handoff.py`. It only adds 3 unit tests in `test_validate_m6_handoff_tga_compat.py` that call the existing script. If Spec #1's `--check-abi-compat` flag does not already output all 5 promise IDs, that is a Spec #1 defect (fix before Spec #2 Phase B). Phase B precondition gate: before writing paired test triple, run `python3 aria-orchestrator/docs/validate-m6-handoff.py --check-abi-compat` manually and confirm all 5 promise IDs appear in stdout. If not: STOP and open a defect against Spec #1."

Add to tasks.md A-infra-1 checklist: "Run validate-m6-handoff.py --check-abi-compat manually and confirm 5 promise IDs in stdout before any TG-A code begins."

---

### C-7 [Spec #3 AC-1] — `grep -c "Rule #" CLAUDE.md >= 9` is insufficient for Diff 6 freeze compliance

**Location**: Spec #3 proposal.md §A.1, AC-1

**Finding**: AC-1 evidence uses `grep -c "Rule #" CLAUDE.md` and expects `>= 9`. The Spec author notes in §Risks R-M6D-1 that this check is "necessary but not sufficient." This acknowledgment is correct but the AC itself as written does not provide a sufficient binary check. The AC can return 9 even if Rules #1-#6 bodies were modified (additions or edits to rule body text), as long as the "Rule #" string still appears 9 times.

Diff 6 is a hard constraint (AD11): "Rules #1-#6 text body is FROZEN." The AC for this constraint must be FROZEN-text-preserving, not just count-based.

More specifically, `grep -q "**版本**: 2.0.0" CLAUDE.md` in the AC uses double-asterisks inside a shell string. In bash, `grep -q "**版本**: 2.0.0"` will interpret `**` as a glob pattern if the shell expands it, or pass it literally if quoted. The double-asterisks are markdown bold syntax. If `grep` is called via `bash -c`, the `**` may not be literal. This is a portability trap.

**Exact reword for AC-1**:

Replace the five-command AC-1 evidence block with:

```bash
# 1. Rule count (necessary, not sufficient)
RULE_COUNT=$(grep -c "^## 规则 #\|Rule #" CLAUDE.md || true)
[ "$RULE_COUNT" -ge 9 ] || { echo "FAIL AC-1: only $RULE_COUNT Rule # occurrences"; exit 1; }

# 2. Version bump (escape markdown asterisks correctly)
grep -qF '**版本**: 2.0.0' CLAUDE.md || { echo "FAIL AC-1: version not bumped to 2.0.0"; exit 1; }

# 3. New section presence
grep -qF '两层 AI 分工' CLAUDE.md || { echo "FAIL AC-1: Diff 3 not applied"; exit 1; }
grep -qF 'Aria 2.0 运行时' CLAUDE.md || { echo "FAIL AC-1: Diff 7 not applied"; exit 1; }
grep -qF 'aria-orchestrator' CLAUDE.md || { echo "FAIL AC-1: Diff 4 not applied"; exit 1; }

# 4. AD11 freeze verification (binary-falsifiable for Rules #1-#6)
git diff HEAD -- CLAUDE.md | grep "^[-]" | grep -E "规则 #[1-6]|Rule #[1-6]" \
  && { echo "FAIL AC-1: Rules #1-#6 text modified (AD11 violation)"; exit 1; }
echo "PASS AC-1"
```

Note: the `git diff HEAD` check assumes CLAUDE.md v2.0 is the working-tree version and HEAD is the pre-edit commit. This must run at Phase B.2 verification, not at Phase C (by which time HEAD will have moved). Add to tasks.md T-A1.6: "Record the HEAD commit SHA before starting Diff 1 edits in `.aria/probes/m6-claudemd-pre-edit-sha.txt`. AC-1 diff check uses this SHA, not HEAD."

---

### C-8 [Spec #3 AC-4] — state-checks.yaml probe count: additive vs replacement ambiguity

**Location**: Spec #3 proposal.md §A.6, AC-4, tasks.md T-A6.4

**Finding**: AC-4 checks:
```bash
grep -c "m6-version-badge-match\|m6-claude-md-version\|m6-arch-doc-stale" .aria/state-checks.yaml
# must return 3
```

This grep pattern matches each probe name once. But `grep -c` counts the number of **lines** containing the pattern (one match per line, not per pattern term). If the file has two lines per probe entry (e.g., name appears in both `name:` field and `description:` field), the count could return 6, not 3. Conversely, if a probe entry is malformed and the name appears 0 times, the count is wrong without revealing which probe is missing.

The Python yaml-parse check below is better but AC-4 text says "must return 3" for the `grep -c` command, which is an unreliable gate.

Additionally, the AC checks for exactly 3 named probes but does not check the **total count** of probes in the file. If the 3 new probes replace 3 existing probes (rather than appending), the count would still be 3. The intent is additive (3 new probes added to existing checks). This should be verified explicitly.

**Exact reword for AC-4**:

Replace the grep-c check:
```bash
# Check by unique name occurrence (not line count):
for probe in m6-version-badge-match m6-claude-md-version m6-arch-doc-stale; do
  grep -qF "name: \"${probe}\"" .aria/state-checks.yaml \
    || { echo "FAIL AC-4: probe ${probe} not found in state-checks.yaml"; exit 1; }
done
echo "PASS AC-4: all 3 M6 probes present"
```

Keep the Python yaml-parse check as the canonical gate. Remove the `grep -c` count check or demote it to a comment.

Add to AC-4 evidence: "Verify probe count is additive: `python3 -c \"import yaml; data=yaml.safe_load(open('.aria/state-checks.yaml')); print(len(data['checks']))\"` must return the pre-existing count plus 3."

---

### C-9 [Spec #3 AC-6 + Spec #2 AC-5] — humanized-command-patterns.md line count proxy is misleading

**Location**: Spec #3 proposal.md §B.3.2, AC-6; Spec #2 AC-5

**Finding**: Spec #3 AC-6 uses `wc -l < standards/autonomous/humanized-command-patterns.md >= 200` as "rough proxy for ≥10 patterns at ~15-20 lines each." The Spec acknowledges it is a proxy, but does not provide a structural verification. It is possible to produce a 200-line file with 10 single-sentence "patterns" and extensive blank lines or repetitive headers, passing AC-6 without providing substantive content.

More critically, Spec #3 B.3.2 in tasks.md says the rubric section should include "scoring dimensions (naturalness / actionability / context-completeness / brevity / tone-appropriateness)" — 5 dimensions. But Spec #2 C.2 defines the rubric as 7 dimensions: D1-D7 (Naturalness, Specificity, Tone, Completeness, Conciseness, Technical accuracy, Autonomy footprint). The BOTH-locations design means the same rubric must appear consistently in both files. If Spec #3 B.3.2 (tasks.md T-B3.2.3) documents only 5 of the 7 dimensions, the Lab-shareable pattern guide is inconsistent with the scoring rubric used in Spec #2 TG-C corpus.

**Exact reword for AC-6 and tasks.md T-B3.2**:

Replace line count proxy with structural check:
```bash
# Verify ≥10 pattern headings (each pattern starts with '### Pattern')
PATTERN_COUNT=$(grep -c "^### Pattern" standards/autonomous/humanized-command-patterns.md)
[ "$PATTERN_COUNT" -ge 10 ] \
  || { echo "FAIL AC-6: only $PATTERN_COUNT pattern headings (need ≥10)"; exit 1; }
# Keep line count as secondary gate
[ "$(wc -l < standards/autonomous/humanized-command-patterns.md)" -ge 200 ] \
  || { echo "FAIL AC-6: file < 200 lines"; exit 1; }
echo "PASS AC-6"
```

Update tasks.md T-B3.2.3 to specify 7 rubric dimensions matching Spec #2 §C.2 exactly: D1 Naturalness, D2 Specificity, D3 Tone appropriateness, D4 Completeness, D5 Conciseness, D6 Technical accuracy, D7 Autonomy footprint. The Spec #3 tasks.md currently lists only 5 dimensions — this is an inconsistency that must be fixed before Phase B.

---

## IMPORTANT FINDINGS

### I-1 [Spec #2 AC-1 / A.4] — Day-3 gate: AND vs OR not specified for the 3 conditions

**Location**: proposal.md §A.4, tasks.md A-uptime-3

**Finding**: The Day-3 health gate has 3 conditions: (1) ≥1 S0→S9 cycle, (2) S_FAIL rate ≤50%, (3) no stuck >4h. The Spec says "If any gate condition fails at Day-3, the owner MUST pause the 7d run." This implies AND semantics (all 3 must pass). The implementation in tasks.md A-uptime-3 `check_day3_health_gate()` correctly implements AND semantics.

However, AC-1 only checks: `Day-3 gate verdict: PASS` exists in Day-3 probe file. It does not verify which of the 3 conditions was individually checked. If the Day-3 probe file was manually written with `Day-3 gate verdict: PASS` without running the logic (or using the probe script), it is an unverified assertion.

**Reword**: Add to AC-1: "The Day-3 probe file must contain all three condition lines filled with YES/NO AND the gate verdict line. Binary check:
```bash
grep -E '≥1 complete S0→S9 cycle: YES' .aria/probes/m6-7d-day-3.md && \
grep -E 'S_FAIL rate ≤50%: YES' .aria/probes/m6-7d-day-3.md && \
grep -E 'No stuck >4h: YES' .aria/probes/m6-7d-day-3.md && \
grep -E 'Day-3 gate verdict: PASS' .aria/probes/m6-7d-day-3.md
```
All four greps must succeed."

---

### I-2 [Spec #2 AC-5] — Median of medians computation: ties not deterministic

**Location**: proposal.md §C.2, tasks.md C-scores-2

**Finding**: The acceptance script computes `corpus_median = statistics.median(medians)` where `medians` is a list of 10 per-sample medians. With 10 values, `statistics.median()` returns the mean of the 5th and 6th values when sorted. This is correct. However, the per-sample median also uses `statistics.median()` on 7 dimension scores. With 7 values, `statistics.median()` returns the 4th value when sorted — exact integer. No floating-point issues.

The actual risk is: what if a score file has a dimension score of "10" written as "10 " (trailing space) or "10/10" (with a slash)? The regex `r'\|\s*D\d\s*\|[^|]+\|\s*(\d+)\s*\|'` would fail to match "10/10" and raise `AssertionError: Expected 7 scores`. This is a brittle parser that produces `exit 2` (infrastructure error) rather than `exit 1` (data error), masking what is actually a content format violation.

**Reword**: Add to tasks.md C-scores-1 score template: "Score values must be plain integers (0-10) with no unit suffix, fraction notation, or qualifying text. Example: `| D1 | Naturalness | 8 |` not `| D1 | Naturalness | 8/10 |`." Add a parser robustness test to C-acceptance-2/3: "fixture with '8/10' score format → exit 1 with format error message (not exit 2 AssertionError)."

---

### I-3 [Spec #2 AC-6] — Pre-flight log parser brittleness: regex assumes `cost_usd:` key format

**Location**: proposal.md AC-6, tasks.md A-dispatch-5

**Finding**: AC-6 uses:
```python
costs = [float(m) for m in re.findall(r'cost_usd:\s*([\d.]+)', content)]
assert len(costs) == 3
```
This regex requires exactly the format `cost_usd: 1.23`. The pre-flight log template in tasks.md A-dispatch-5 includes `cost_usd` as a field name, but the template format uses plain markdown, not YAML. If the owner writes `cost_usd: $1.50` (with dollar sign) or `cost_usd: 1.50 USD`, the regex fails to extract the float and `len(costs) < 3` triggers a false-FAIL.

**Reword**: Specify the exact format constraint in the pre-flight log template:
```markdown
- **cost_usd**: 1.23   ← must be a bare decimal number, no $ sign, no units
```
And harden the AC-6 regex: `re.findall(r'cost_usd:\s*\$?([\d.]+)', content)` to tolerate an optional `$` prefix. Also add: "If `len(costs) != 3`, exit 1 with `[FAIL] AC-6: expected 3 cost_usd entries, found N — check log format`."

---

### I-4 [Spec #2 TG-B] — WAL-D test semantic gap: SQLite WAL auto-recreation is version-dependent

**Location**: proposal.md §B.2 (WAL-D), tasks.md B-infra-3

**Finding**: WAL-D assertion is: "SQLite reopens WAL-mode DB without WAL; behaviour depends on SQLite WAL mode; test asserts no data corruption visible to subsequent clean connection." But the expected log entry is `{"event": "wal_fault", "scenario": "WAL-D", "recovery": "wal_auto_recreated"}` — which implies the recovery handler knows the WAL was deleted and classifies it as `wal_auto_recreated`.

The problem: if the WAL file is deleted while no connection holds it, SQLite will auto-recreate it on next open — this is correct behaviour, not a fault. The state machine would NOT necessarily enter S_FAIL for WAL-D (unlike WAL-A/B/C). The test cannot assert `state machine → S_FAIL` for WAL-D without contradicting the "no data corruption" assertion. These two assertions are contradictory: if state machine → S_FAIL, it means data access failed; if no corruption visible, it means data access succeeded.

**Reword**: Clarify in §B.2 WAL-D that the expected outcome is: "No state machine S_FAIL; data integrity confirmed; log entry is INFORMATIONAL not ERROR. Test asserts: (a) state machine continues normally (NOT S_FAIL), (b) subsequent clean connection can read all pre-WAL-delete data, (c) log entry `{\"event\": \"wal_checked\", \"scenario\": \"WAL-D\", \"recovery\": \"wal_auto_recreated\", \"severity\": \"info\"}`." This requires fixing the WAL-D expected outcome column from "behaviour depends on SQLite WAL mode" to a concrete, version-consistent assertion: "SQLite 3.7+ auto-recreates WAL on next open; test targets Python 3.9+ runtime which includes SQLite 3.38+ bundled. Assert no exception raised on open."

---

### I-5 [Spec #3] — T-B0 submodule runbook: step 5 failure handling absent

**Location**: Spec #3 proposal.md §B.3 (P-10), tasks.md T-B0

**Finding**: T-B0 runbook has 10 sequential steps. Step T-B0.7 is "Owner action: merge the feature branch in the standards repo. Wait for merge confirmation." If T-B0.6 push fails (authentication error, branch protection rule, remote rejection), there is no error handling instruction. The next step (T-B0.8) assumes push succeeded. If push fails silently or is retried without recognizing the failure, T-B0.8 `git -C standards checkout master && git -C standards pull` will not contain the autonomous/ files, and T-B0.10 `git add standards` will stage the OLD pointer.

Per `[[feedback_submodule_regression_pitfall]]`: concurrent Spec landing + stale submodule pointer is a known risk.

**Reword**: Add after T-B0.6: "Verify push succeeded: `git -C standards log --oneline origin/feat/autonomous-docs -1` must show the commit from T-B0.5. If push failed: diagnose auth/PAT scope, fix, retry. Do NOT proceed to T-B0.7 until push is confirmed." Add after T-B0.8: "Verify pull succeeded: `git -C standards log --oneline -1` must show the same SHA as `git -C standards log --oneline origin/master -1`. If not: STOP."

---

### I-6 [Spec #3] — Probe 3 (arch-doc-stale) date parsing: GNU date vs BSD date portability

**Location**: Spec #3 proposal.md §A.6 (Probe 3), tasks.md T-A6.3

**Finding**: Probe 3 uses `date -d "$LAST" +%s` for date arithmetic. `date -d` is GNU coreutils syntax; it does NOT work on BSD/macOS `date` (which uses `date -j -f "%Y-%m-%d" "$LAST" +%s`). The Spec platform constraint says "Linux only" (Nomad alloc Python 3.9+), but the probe runs on the developer's workstation via state-scanner. If the developer uses macOS, the probe fails immediately with `date: illegal option -- d`.

**Reword**: Replace `date -d "$LAST" +%s` with a Python one-liner (portable across platforms per the Spec's existing use of python3 in other probes):
```yaml
command: |
  LAST=$(grep -oP '(?<=\*\*Last Updated\*\*: )\d{4}-\d{2}-\d{2}' docs/architecture/system-architecture.md | head -1)
  [ -z "$LAST" ] && { echo "MISSING Last Updated header"; exit 1; }
  python3 -c "
from datetime import date
last = date.fromisoformat('$LAST')
age = (date.today() - last).days
print(f'OK age={age}d') if age < 90 else exit(f'STALE age={age}d (threshold=90d)')
" || exit 1
```
Add note: "POSIX `date -d` is GNU-only. Use python3 for cross-platform date arithmetic in all state-checks probes."

---

### I-7 [Spec #2 + Spec #3] — AD-M6-8 reserved slot: risk of non-retirement creating false completeness signal

**Location**: Spec #3 proposal.md §Key design decisions AD-M6-8, tasks.md T-B6.3

**Finding**: AD-M6-8 is explicitly RESERVED at Phase A with the instruction "fill or retire by Phase C". Per `[[feedback_ad_slot_backfill_checkpoint]]` this is standard practice. However, tasks.md T-B6.3 provides a complete "retired" text template that can be copy-pasted. If the implementer uses this template without considering whether a Phase B decision actually materialized, the retirement becomes a rubber stamp rather than a genuine audit. The pre-archive checklist item "AD-M6-8 is either filled with a real decision topic OR explicitly retired" is owned by the knowledge-manager agent who is also the implementation agent — there is no independent verification.

**Reword**: Add to the pre-archive checklist (tasks.md): "AD-M6-8 retirement must be reviewed by qa-engineer or tech-lead in pre-merge R1 audit, not self-signed by knowledge-manager. Add a comment to the AD-M6-8 stub: `# REQUIRES-INDEPENDENT-REVIEW: retirement must be confirmed by non-implementation agent in pre_merge audit`."

---

### I-8 [Spec #2] — is_synthetic Mechanism B fallback: acceptance SQL not patched for both mechanisms simultaneously

**Location**: proposal.md §A.2, tasks.md A-dispatch-2

**Finding**: AC-2 acceptance code is written for Mechanism A (`is_synthetic` column). tasks.md A-dispatch-2 says "If Mechanism B (title prefix): replace `is_synthetic=1` with `title LIKE '[DEMO-M6-%]'`." But the AD-M6-4 decision is deferred to Phase B, meaning the acceptance script cannot be fully written at Phase A time.

AC-2 acceptance code shows `is_synthetic=1` hardcoded. If Mechanism B is chosen, the implementer must remember to swap this in two places (synthetic cap check and stratification context). There is no compile-time guarantee they will.

**Reword**: The acceptance script should handle both mechanisms via a configuration constant:

```python
# AD-M6-4: set SYNTHETIC_MECHANISM at Phase B kickoff
SYNTHETIC_MECHANISM = 'A'  # 'A' = schema column, 'B' = title prefix
SYNTHETIC_FILTER_SQL = (
    "is_synthetic = 1" if SYNTHETIC_MECHANISM == 'A'
    else "title LIKE '[DEMO-M6-%]'"
)
```

Add to tasks.md A-dispatch-2: "Define `SYNTHETIC_MECHANISM` constant at the top of `check-m6-e2e-acceptance.py`. Phase B implementer sets this once during A-infra-2. This prevents mechanism mismatch across multiple SQL queries."

---

### I-9 [Spec #3 AC-3] — README.md badge version hardcoded to v1.27.0: becomes stale if plugin bumps during M6

**Location**: Spec #3 proposal.md §A.2, AC-3, tasks.md T-A2.1

**Finding**: AC-3 checks `grep -q "v1.27.0" README.md`. The badge is set to v1.27.0 (current as of commit `c7e611f`). But if aria-plugin releases v1.28.0 during the 4-5 week M6 window, the badge update in this Spec will be immediately stale, and AC-3 (which hardcodes "v1.27.0") will pass while README shows a stale badge.

More fundamentally, Probe 1 (`m6-version-badge-match`) already addresses ongoing drift dynamically. But AC-3 is a one-time verification that creates a static artifact checked against a hardcoded version string.

**Reword**: Replace hardcoded version in AC-3:
```bash
# Dynamic: compare README badge against plugin.json (not hardcoded)
BADGE=$(grep -oP '(?<=Plugin-v)[0-9]+\.[0-9]+\.[0-9]+' README.md | head -1)
PLUGIN=$(python3 -c "import json; print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])")
[ "$BADGE" = "$PLUGIN" ] && echo "PASS AC-3: badge=$BADGE matches plugin.json" \
  || { echo "FAIL AC-3: badge=$BADGE != plugin.json=$PLUGIN"; exit 1; }
grep -q "Aria 2.0" README.md || { echo "FAIL AC-3: Aria 2.0 cross-link absent"; exit 1; }
```
This also makes AC-3 and Probe 1 consistent in logic (they should produce the same result).

---

### I-10 [Spec #2 TG-B] — AdvancingClock DI audit scope: `datetime.now()` call inventory not committed

**Location**: proposal.md §B.3, tasks.md B-sm-1

**Finding**: tasks.md B-sm-1 says "Audit `state_machine.py` for all `datetime.now()` calls. Replace each with `self._clock.now()`." The instruction requires a post-audit comment block listing "all replaced call sites" as `[list file:line references here]`. But there is no task to VERIFY the inventory is complete before declaring TG-B done. A missed `datetime.now()` call that was not captured in the inventory would produce a flaky wall-clock test that only manifests in CI, not local runs.

**Reword**: Add to tasks.md B-sm-1:
```bash
# Verify no remaining datetime.now() calls in state_machine.py:
grep -n "datetime.now()" aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/state_machine.py
# must produce no output
```
"This grep must be added to the AC-4 verification block OR to a dedicated lint check in `pyproject.toml` (e.g., via `ruff` or `flake8` custom rule). If any `datetime.now()` calls remain, the AdvancingClock DI refactor is incomplete."

---

### I-11 [Spec #3] — CLAUDE.md version field grep: `grep -q "**版本**: 2.0.0"` uses unescaped markdown

**Location**: Spec #3 proposal.md AC-1 and tasks.md T-A1, T-A6.2, full AC sweep

**Finding**: Throughout Spec #3's AC-1 evidence, tasks.md T-A1, T-A6.2, and the full AC sweep, the command `grep -q "**版本**: 2.0.0" CLAUDE.md` is used. In bash, `**` within double quotes is NOT expanded (globbing requires unquoted context), so this is actually a literal grep for `**版本**: 2.0.0`. This works correctly.

However, probe 2 uses `grep -oP '(?<=\*\*版本\*\*: )[0-9]+\.[0-9]+\.[0-9]+' CLAUDE.md`. The Perl-compatible lookbehind `(?<=\*\*版本\*\*: )` requires the literal backslashes to be escaped in the YAML value. In YAML, the backslash is not a YAML special character in double-quoted strings but must be doubled in single-quoted YAML strings. If the YAML parser preserves the string correctly, grep -oP will receive `(?<=\*\*版本\*\*: )` as the pattern, which correctly matches after `**版本**: `.

This is a minor but real trap if YAML reserializes the probe command. The risk is low but present.

**Reword**: Use `grep -F` (fixed string) rather than `grep -P` for the version check in Probe 2:
```yaml
command: |
  VER=$(grep -oP '\*\*版本\*\*: \K[0-9]+\.[0-9]+\.[0-9]+' CLAUDE.md | head -1)
  [ "$VER" = "2.0.0" ] && echo "OK version=$VER" || { echo "DRIFT version=$VER expected 2.0.0"; exit 1; }
```
(`\K` is the Perl-compat "forget everything before here" — equivalent to lookbehind but simpler to escape in YAML.)

---

## OBSERVATIONS (non-blocking, advisory)

### O-1 [Spec #2] — Pre-flight $2 cap: per-dispatch vs total

The Spec says "≤$2 per dispatch, total ≤$6 for 3 dispatches combined." But AC-6 only checks `all(c <= 2.0 for c in costs)` — the per-dispatch cap. There is no check for the total sum. If all 3 dispatches cost exactly $2.00 each, total = $6.00 (OK). But if one costs $1.00 and another costs $3.00, the per-dispatch check fails already (correct). The total cap is redundant given the per-dispatch cap. No change needed, but the "total ≤$6" language in the Spec is misleading — consider removing it or replacing with "each individual dispatch ≤$2; no total cap check needed since 3 × $2 = $6 maximum."

### O-2 [Spec #2] — `test_crash_infra3_wal.py` "exactly 4 test functions" assertion in AC-3

AC-3 says: "`test_crash_infra3_wal.py` must contain exactly 4 test functions (one per WAL scenario WAL-A/B/C/D per P-5)." The verification is human-review only — there is no automated check in AC-3 for this count. Consider adding: `grep -c "^def test_" aria-orchestrator/tests/test_crash_infra3_wal.py` and asserting the result equals 4.

### O-3 [Spec #3] — AC-2 release notes check omits `aria-plugin 不随` from full sweep command

In the tasks.md full AC sweep (line ~404):
```bash
grep -q "Plugin Compatibility" docs/release-notes-v2.0.0.md \
  && grep -q "Forgejo Discussion FAQ" docs/release-notes-v2.0.0.md \
  && echo "AC-2 PASS"
```
The string `aria-plugin 不随` (which appears in proposal.md AC-2) is absent from the tasks.md sweep command. Minor inconsistency. Both checks should appear in both places.

---

## Cross-Spec integration gap summary

| Gap | Specs | Risk | Severity |
|-----|-------|------|----------|
| BOTH-locations: file existence vs string reference (C-5) | #2 AC-5 + #3 AC-6 | False-PASS or sequencing ambiguity | Critical |
| Spec #1 validate-m6-handoff.py ownership (C-6) | #2 AC-7 + Spec #1 | Double-implementation or silent gap | Critical |
| Rubric dimension count mismatch (C-9) | #2 §C.2 + #3 T-B3.2.3 | Lab-shareable pattern guide inconsistent with scoring corpus | Critical |
| Shipping order for standards/autonomous/ (I-5) | #3 B.3 depends on #2 TG-C templates | Submodule pointer issues if #3 ships before #2 TG-C templates committed | Important |

---

## Required actions before Phase A.3

| Priority | Finding | Action |
|----------|---------|--------|
| P0 | C-1 | Fix AC-1 uptime metric: use Day-1 probe StartedAt, not live API StartedAt |
| P0 | C-2 | Fix AC-2: add zero-division guard before synthetic cap check |
| P0 | C-3 | Fix LLM-4: specify Layer 1 vs Layer 2 provider scope in test |
| P0 | C-5 | Fix BOTH-locations AC-5/AC-6: add conditional file-existence check and sequence contract |
| P0 | C-6 | Fix AC-7: declare that Spec #2 does not modify validate-m6-handoff.py; add pre-B gate manual verification |
| P0 | C-7 | Fix AC-1 (Spec #3): add `grep -F` for version string; add `git diff HEAD` Rule #1-#6 freeze check; record pre-edit SHA |
| P0 | C-9 | Fix humanized-command-patterns.md rubric: align to 7 dimensions; add `### Pattern` heading count AC |
| P1 | C-4 | Add `--cov-fail-under=100` to pyproject.toml addopts for CI enforcement |
| P1 | C-8 | Fix AC-4: replace `grep -c` with per-name `grep -qF` loop |
| P1 | I-1 | Strengthen Day-3 gate AC: verify individual condition lines, not just verdict |
| P1 | I-4 | Fix WAL-D test: reconcile S_FAIL assertion with "no data corruption" assertion |
| P1 | I-6 | Replace `date -d` with python3 date arithmetic in Probe 3 |
| P2 | I-2, I-3, I-7, I-8, I-9, I-10, I-11 | Address per rewordings above |

---

*Audit completed 2026-05-24. Combined-Spec mode — Spec #2 and Spec #3 audited jointly against cross-Spec dependencies.*
