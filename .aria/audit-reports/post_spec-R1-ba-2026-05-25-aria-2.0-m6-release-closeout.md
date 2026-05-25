# Phase A.2 R1 audit — backend-architect — aria-2.0-m6-release-closeout

> **Spec commit**: `98218fb`
> **Audit date**: 2026-05-25
> **Agent**: aria:backend-architect (Opus 4.7 sub-agent)
> **Audit perspective**: orchestrator architecture / subprocess semantics / gate composition / atomic archive runner

## Verdict
**NEEDS_FIX**

## Summary

The Spec is architecturally well-structured — eight sequenced gates, three-state exit aggregation, rollback-tracked archive runner, and secret-hygiene-aware G-6 design are all sound. However, two Critical defects will cause runtime failures across the majority of gates before a single line of real acceptance logic executes: (1) the REPO_ROOT resolution pattern is wrong for a script that lives inside the `aria-orchestrator` submodule and must read main-repo files, and (2) two of G-7's five file-parsing regexes are verified to return zero matches against the actual on-disk file formats. Fix these two before Phase B implementation begins or every gate touching the filesystem will fail silently with parse-error ABORTs.

## Critical findings

| ID | Location | Issue | Recommended fix |
|----|----------|-------|-----------------|
| C-ba-1 | tasks.md:50; proposal.md §A/D/F/G/E | REPO_ROOT off-by-one level for cross-repo file reads (G-3/G-5/G-7/G-8). `HERE.parent` = `aria-orchestrator/` (submodule root), but main repo files live at `HERE.parent.parent`. | Declare `ORCH_ROOT = HERE.parent` + `MAIN_REPO_ROOT = HERE.parent.parent`. Use ORCH_ROOT for G-1/G-2 subprocess cwd; MAIN_REPO_ROOT for G-3/G-5/G-7/G-8 path reads. |
| C-ba-2 | proposal.md §F lines 154/156 + tasks.md T-A2.8 | G-7 `aria/VERSION` and `aria/README.md` regexes don't match actual formats. Actual: `> **版本**: 1.27.0` (Chinese Markdown blockquote). Spec assumes YAML `version:` and English `**Version**:`. Both return None → guaranteed ABORT parse-failure. | Fix regexes: `aria/VERSION` → `\*\*版本\*\*:\s*([\d.]+)`; `aria/README.md` → `\*\*Version\*\*:\s*v?([0-9]+\.[0-9]+\.[0-9]+)` (drop `^` anchor; aria/README.md uses English in some sections — need owner verify). |

## Important findings

| ID | Location | Issue | Recommended fix |
|----|----------|-------|-----------------|
| I-ba-1 | proposal.md §B G-1/G-2 + A-1/A-2 + tasks T-A2.2/T-A2.3 | `--all` flag not contracted by sibling Specs (grep verified: Spec #1 has 4 individual flags only; Spec #2 has 3 `--tg-*` flags only). Primary path is aspirational. | Invert primary/fallback: make per-flag invocation primary, `--all` optional fast-path. |
| I-ba-2 | tasks.md T-A2.3 last bullet | G-2 fallback aggregation logic ambiguous ("same mapping" undefined). | Add explicit aggregation sentence: 3 separate subprocesses, any returncode 2 → ABORT, any 1 (no 2) → RED, all 0 → PASS. |
| I-ba-3 | proposal.md AC-3 vs tasks.md T-A2.1 | `--only-gate G-4` (AC-3 evidence) vs `--gates G-N[,G-M,...]` (T-A2.1 argparse) — flag name collision. | Unify on `--gates` (composable). Update AC-3 evidence. |
| I-ba-4 | proposal.md §D step 2 vs tasks.md T-A2.6 last bullet | G-5 offline fallback contradicts: proposal says `--use-local-master` flag; tasks says automatic RED-on-ls-remote-failure. | Pick tasks.md (simpler, no new CLI flag). Remove `--use-local-master` from proposal §D step 2. |
| I-ba-5 | proposal.md §H step 1 | Says "owner-override env var" but mechanism is CLI `--owner-override` arg. | Fix proposal §H step 1 language to "CLI arg propagation". |
| I-ba-6 | proposal.md §A line 69 + tasks T-A2.7 vs T-A2.11 | G-6 stdout suppression (auth headers) contradicts T-A2.11 "full stdout/stderr" — secret-leak path into git-tracked report. | T-A2.11 explicit per-gate capture: G-1..G-5/G-7/G-8 stdout+stderr; G-6 stderr-only. |

## Minor findings

| ID | Location | Issue | Recommended fix |
|----|----------|-------|-----------------|
| N-ba-1 | proposal.md §C G-4 today computation | UTC assumption correct but not documented. | Add one sentence: today computed in UTC; near-midnight boundary explained. |
| N-ba-2 | proposal.md §G G-8 PASS condition | G-8 doesn't verify Spec #4's own directory presence. | Add self-check: `(CHANGES / 'aria-2.0-m6-release-closeout').is_dir()`. |
| N-ba-3 | tasks.md T-A4.3 | 3-second sleep on `--execute` has no test escape hatch. | Add env var `M6_ARCHIVE_NO_COUNTDOWN`. |
| N-ba-4 | tasks.md T-A3.4 | G-4 boundary tests don't specify gate isolation (G-1..G-3 would fail). | Use `--gates G-4` selector after I-ba-3 flag-name resolution. |

## Q-escalations

| Q | Question |
|---|----------|
| Q-ba-1 | Should `MAIN_REPO_ROOT` be `git rev-parse --show-toplevel` (robust) or `HERE.parent.parent` (simpler)? |
| Q-ba-2 | Spec #3 OOS-6 says state-checks.yaml submodule probe is Spec #4 scope. Add as separate state-checks entry, or G-5 sufficient? |

---

**Audit trail**: `[[feedback_audit_driven_fix_conventions]]` — inline R1-fix references in proposal/tasks with `<!-- R1-C-ba-N fix: ... -->` comments + report ID in commit message for traceability.
