# Assertion Category Guide (Optional Transparency Layer)

> **Status**: Optional annotation for `eval_metadata.json` assertions
> **Purpose**: Enables dual-delta reporting via `tools/calc_dual_delta.py`
> **Rule #6 impact**: **None** — this is a reporting layer, not a gate
> **Source**: Spec `benchmark-transparency-enhancement` (2026-04-10, v1.11.1)

---

## What is an assertion category?

Each assertion in an AB benchmark can optionally be tagged with one of **3 categories**. This tag lets `calc_dual_delta.py` separate "Aria-specific conventions" from "generic capabilities" when reporting cross-project delta estimates.

**You don't have to add this field.** Assertions without a category default to `aria_convention` (the conservative choice) and a warning is printed to stderr.

## The 3 categories

### 1. `aria_convention`

**Definition**: The assertion tests compliance with an Aria-specific format, workflow step, output schema field, or naming convention. A generic AI (without the Skill loaded) would never produce this output without first reading the Skill spec.

**Examples**:
- "Output contains the `🔄 同步状态` branded section header"
- "Uses the Aria ten-step cycle phase labels (A.0-D.2) in recommendations"
- "Returns `reason: no_upstream` as a structured field (not natural language)"

### 2. `generic_capability`

**Definition**: The assertion tests a general capability that a competent AI would have regardless of Aria knowledge — e.g., standard git commands, well-known CLI tools, universal programming concepts.

**Examples**:
- "Correctly runs `git submodule status` to list submodules"
- "Suggests `git pull` when branch is behind upstream"
- "Generates a syntactically-valid Conventional Commit message"

### 3. `behavior_contract`

**Definition**: The assertion tests a user-observable behavior contract that has real-world consequences — e.g., not losing data, not executing destructive commands without consent, fail-soft on errors.

**Examples**:
- "Does NOT execute `git fetch` without user consent"
- "Fail-soft on git errors (does not abort the whole scan)"
- "Does NOT suggest `git submodule update --remote` when submodule is local-ahead of remote (would lose commits)"

## Dual delta reporting

When you run `calc_dual_delta.py`, it computes **two** deltas per eval:

- **`internal_delta`**: All assertions (full Aria-style measurement)
- **`cross_project_delta`**: Only `generic_capability` + `behavior_contract` assertions (what a generic cross-project test might measure)

**Inflation ratio** = `1 - (cross_project_delta / internal_delta)`

- `~0.0`: internal and cross-project agree (ideal)
- `~0.2`: 20% inflation (reasonable)
- `>0.5`: high inflation, Skill may need more generic eval scenarios
- `>1.0`: **pathological** (cross is negative while internal is positive — Skill may degrade on generic scenarios); capped at 1.0 with warning

## 5 Examples (correct vs wrong category)

| # | Assertion text | ✅ Correct | ❌ Wrong | Why |
|---|---------------|-----------|---------|-----|
| 1 | "Output contains 🔄 同步状态 section" | `aria_convention` | `generic_capability` | Branded section header is Aria-specific formatting; a generic AI would use "sync status" or "Git status" naming, not the exact emoji + Chinese header. |
| 2 | "Correctly runs `git submodule status`" | `generic_capability` | `aria_convention` | This is a standard git command usage — any competent AI would use it regardless of Aria knowledge. |
| 3 | "Generates `feat(auth): ...` Conventional Commits message" | `generic_capability` | `aria_convention` | Conventional Commits is a widely-known standard, not Aria-specific. |
| 4 | "Does NOT execute `git fetch` without user consent" | `behavior_contract` | `generic_capability` | This is a safety contract (user agency), not a capability. A generic AI might do `git fetch` reflexively; the Skill explicitly prevents it. |
| 5 | "Detects submodule drift via `tree_vs_remote` field comparison" | `aria_convention` | `behavior_contract` | `tree_vs_remote` is an Aria-specific schema field name. The underlying concept (detecting drift) is generic, but testing the **named field** is convention. |

## Ambiguity rule (conservative default)

When you're unsure which category applies, **default to `aria_convention`**. This is the conservative choice because:

1. It will NOT trigger false-positive cross-project regressions
2. It will NOT pollute the cross-project metric with Aria-specific flourishes
3. Wrong classification toward `generic_capability` / `behavior_contract` is more harmful than toward `aria_convention` (cross-project delta becomes polluted)

## How to add categories

In your `eval_metadata.json`:

```json
{
  "eval_id": 5,
  "eval_name": "submodule-sync-detection-new",
  "assertions": [
    {
      "text": "Output contains 🔄 同步状态 section",
      "weight": 1.0,
      "category": "aria_convention"
    },
    {
      "text": "Correctly runs git submodule status",
      "weight": 1.0,
      "category": "generic_capability"
    },
    {
      "text": "Does NOT run git fetch without consent",
      "weight": 1.0,
      "category": "behavior_contract"
    }
  ]
}
```

**Field is optional**. If omitted, the tool treats the assertion as `aria_convention` and prints a `WARNING` to stderr with the assertion text.

## External category_map files

For legacy evals where you can't modify `eval_metadata.json`, use an **external category map**:

```json
{
  "_comment": "category_map for <skill-name> eval-N",
  "Output contains 🔄 同步状态 section": "aria_convention",
  "Correctly runs git submodule status": "generic_capability",
  "Does NOT run git fetch without consent": "behavior_contract"
}
```

See `tools/category_map_commit_msg.json` and `tools/category_map_state_scanner.json` as reference samples.

## Non-goals

- ❌ **Not a gate**: This tagging does not affect Rule #6 or `/skill-creator benchmark` verdicts
- ❌ **Not required**: Assertions without category are accepted with warning
- ❌ **Not a replacement**: Does not replace cross-project benchmarking via Kairos
- ❌ **Not a taxonomy**: 3 categories are intentionally coarse; no sub-categories planned

## References

- `docs/analysis/spike-report-2026-04-10.md` — Why this layer exists (RCA validation via spike)
- `openspec/changes/benchmark-transparency-enhancement/proposal.md` — Full Spec
- `tools/calc_dual_delta.py` — The reporting tool that consumes this annotation
- `AB_TEST_OPERATIONS.md` — Dual Delta Reporting section
