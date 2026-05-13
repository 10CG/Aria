# state-scanner Rule #6 benchmark — issue #101 fix (iteration 1)

**Date**: 2026-05-13
**Cycle**: `aria-issue-101-status-normalize`
**Modification scope**: `aria/skills/state-scanner/scripts/collectors/_status.py::_normalize_status` — word-boundary regex + reorder priority + add `implemented` token
**Framing**: Deterministic bug fix — AB measures pre-fix vs post-fix unit test pass rate (NOT with-skill vs without-skill which is the wrong metric for deterministic logic changes)

## Result

| Metric | pre-fix | post-fix | Delta |
|---|---|---|---|
| **Test pass rate** | 3/13 = 23.1% | 13/13 = 100% | **+77pp** |
| Cases recovered | — | 10 | — |
| Live verify pending_archive false positives | 4 | 0 | -4 (100% reduction) |
| Existing test regression | — | 0/414 | ✅ no regression |

## Rule #6 verdict: **PASS**

Delta +77pp on pass rate + 0 regression on 414 pre-existing tests + live verify shows pending_archive false positives eliminated (4 → 0).

## Test breakdown

### Pre-fix failures (10 cases)

1. `test_issue101_docs_marketplace_adaptation` — Bug 1: "Approved (...) — Phase A done" returns `done` not `approved`
2. `test_issue101_existing_data_migration` — Bug 2: "Implemented (...)" returns `unknown` not `implemented`
3. `test_issue101_pricing_status_marketplace_redo` — Bug 2 (same family)
4. `test_issue101_terms_of_service_and_attribution` — Bug 1: "DRAFT pending ... done" returns `done` not `pending`
5. `test_positive_regression_in_progress_with_done_shadow` — "In Progress (50% done)" returns `done` not `in_progress`
6. `test_positive_regression_ready_with_done_shadow` — "ready (Phase A done)" returns `done` not `ready`
7. `test_positive_regression_single_token_states` — "Implemented" single token returns `unknown` not `implemented`
8. `test_shadow_inactive_not_active` — "Inactive — superseded" returns `active` not `unknown` (pre-existing latent bug surfaced by audit)
9. `test_shadow_incomplete_not_complete` — "Incomplete" returns `done` not `unknown` (pre-existing latent bug)
10. `test_shadow_unimplemented_not_implemented` — would fail under naive substring fix; word-boundary regex prevents

### Pre-fix passing (3 cases by happenstance, not by design)

1. `test_empty_string_is_unknown` — empty string returns `unknown` regardless of code path
2. `test_implemented_does_not_trigger_pending_archive` — `assertNotEqual("Implemented", "done")` passes because pre-fix returns `unknown` ≠ `done` (true incidentally)
3. `test_ordering_approved_before_implemented` — "Approved (Implemented)" matches `approved` first in pre-fix order (`approved` happened to be checked before missing `implemented`)

## Live verification

Pre-fix `python3 aria/skills/state-scanner/scripts/scan.py` output for Aria itself:
```json
{
  "openspec": {
    "pending_archive": [
      {"id": "docs-marketplace-adaptation", "reason": "Status=done still in changes/"},
      {"id": "existing-data-migration", "reason": "Status=done still in changes/"},
      {"id": "pricing-status-marketplace-redo", "reason": "Status=done still in changes/"},
      {"id": "terms-of-service-and-attribution", "reason": "Status=done still in changes/"}
    ]
  }
}
```

Post-fix:
```json
{
  "openspec": {
    "pending_archive": []
  }
}
```

## Framing note (Rule #6 application to deterministic fixes)

This cycle modifies state-scanner Skill **logic** (collector code), not Skill **description** or LLM-prompt. The original `/skill-creator` benchmark framing measures "with-skill vs without-skill" capability delta on LLM tasks — that's the right metric for LLM-prompt skills.

For deterministic code logic fixes, the right AB is **pre-fix vs post-fix correctness** measured via unit test + live scan. This benchmark applies that framing. Precedent: `aria-issue-triage-sop` iteration-1 (2026-05-13) established that "structure vs capability" framing differs by skill type; this benchmark extends to "correctness vs capability" for deterministic code modifications.

Both framings satisfy Rule #6's intent: "verify the modification has positive value before merge".

## References

- Spec: `openspec/changes/aria-issue-101-status-normalize/proposal.md`
- Triage source: Forgejo Aria #101 (manual triage comment-5972 + AI dogfood comment-6019)
- Precedent benchmark: `aria-plugin-benchmarks/ab-results/2026-05-13-issue-triage/` (SOP/structure framing)
- Test suite: `aria/skills/state-scanner/tests/test_openspec.py::TestStatusNormalizationIssue101Fix` (13 cases)
