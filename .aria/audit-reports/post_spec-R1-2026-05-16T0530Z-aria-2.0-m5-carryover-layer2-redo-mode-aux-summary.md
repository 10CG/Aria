---
checkpoint: post_spec
mode: convergence
round: R1
converged: false
oscillation: false
verdict: FAIL
timestamp: 2026-05-16T05:30Z
spec_id: aria-2.0-m5-carryover-layer2-redo-mode-aux
context: openspec/changes/aria-2.0-m5-carryover-layer2-redo-mode-aux/
agents: [backend-architect, qa-engineer, code-reviewer, ai-engineer]
total_findings: ~37
new_critical_count: 6
---

# R1 post_spec Audit — Spec Y v1

## Verdict: FAIL → substantial R2 rewrite required (parallel to Spec X R1→v2 pattern)

## CRITICAL findings (cross-agent consensus, 6 items)

| ID | Source(s) | Issue | Spec X precedent |
|----|-----------|-------|------------------|
| **CRIT-1** | qa C1+H3, backend C1 | `_handle_s5_pr_created` does NOT EXIST in current state machine. Layer 1 binds pr_id via `_handle_s6_review::find_or_create_pr` (extension.py:2567), which uses `aria/{issue_id}` branch convention NOT `aria/redo-*`. Spec Y assumes architecture that doesn't exist. result.json never read by Layer 1 currently. | Similar to Spec X C1 (bash vs Python reality drift) — Spec Y assumed architecture without verifying Layer 1 reality. |
| **CRIT-2** | qa C2+H6, backend H1, ai-14 | `python3 -m aria_layer1.commit_validator validate` invocation broken: (a) aria_layer1 Python pkg NOT in Layer 2 Node-base image (Spec X R1 C4 established this); (b) commit_validator.py has NO `__main__.py` or argparse CLI — only library function `validate_commit_message()`. Both must be fixed OR commit_validator shell-ported. | Spec X R1 C4 resolved same Python-in-bash-image tension by choosing pure bash + curl+jq. Spec Y reverts this lesson. |
| **CRIT-3** | ai-1 | `REWORK_ROUND` env var NEVER propagated to Layer 2. `_handle_s4_launch` writes only 4 keys; HCL meta_optional declares only 4. Spec Y T2.6 fallback `${REWORK_ROUND:-1}` will always render `round 1` regardless of actual round (silent semantic bug). **Also latent in Spec X already shipped** (modes/changes.sh:174,256). | Spec X retroactive latent bug surfaced; Spec Y must add REWORK_ROUND as 5th meta_optional key + extend AD-M5-3 contract to 5 keys. |
| **CRIT-4** | ai-2 | `spec_drift_input_fetcher` return signature wrong shape. Spec Y T4.4 says `SpecDriftInputs(proposal_text, pr_diff, spec_id, pr_id)` 4-tuple, but `reconciler.py:1014` unpacks `(spec_what, spec_accept, pr_diff)` 3-tuple of pre-sliced sections. Full-impl will break reconciler at runtime. | Spec Y missed reading reconciler caller contract. |
| **CRIT-5** | code-reviewer C1 | T7.2 AD-M5-3 append says `"append '2026-05-XX Spec Y impl complete...'"` but does NOT explicitly state "preserve existing 2026-05-16 Spec X line". Risk of agent REPLACING Spec X line (which itself was the R2 C2 fix in Spec X). | Spec X R2 C2 established immutable append-only convention; Spec Y must repeat guard literally. |
| **CRIT-6** | qa H4 | Migration number collision: `005_schema_v4_drop_inline_uq.sql` ALREADY EXISTS (M5 T1.5). Spec Y T0.1 proposes `005_schema_v4.1_additive.sql` → file collision. Must renumber to **006**. | Spec Y didn't check existing migrations dir before assigning number. |

## HIGH findings (single-agent or partial overlap, ~13 items)

### backend-architect HIGH
- **H1**: OS-3 partial state risk — comment posted + PATCH state=closed fails → permanent inconsistent state (audit warn only, no compensating action)
- **H2**: spec_id derivation contract undefined — "if can derive from issue body or env" not implementable; need explicit source (new NOMAD_META_SPEC_ID? Layer 1 inject?)
- **H3**: AD-M5-10 #5 risk_tier dual-write — Spec Y proposal doesn't confirm redo dispatch row INSERT path preserves `risk_tier='always'` literal write
- **H4**: Layer 2 image v11 build dependency uncertainty — image rebuild + Python pkg install vs shell-port unresolved

### qa-engineer HIGH (in addition to CRIT)
- **H5**: OS-3 unenumerated failure modes (parent PR already closed, comment success + PATCH fail partial, rework_of resolves to null pr_id)
- **H6**: OS-4 fetches `openspec/changes/<spec_id>/proposal.md` from master — after Spec archives, path moves to `openspec/archive/<date>-<spec_id>/`, returning 404
- **H7**: Regression count "51 bash" not enumerated with executable commands (Spec X T6.3 had explicit `bash docker/aria-runner/tests/...` enumeration)

### code-reviewer IMPORTANT (9 items)
- **C3-C10**: D5 bash acknowledgment understated / §What A-G vs T0-T8 mapping mismatch / AD line range citations missing / Conv Commits examples need own enumeration (not reuse Spec X) / OS-4 classified wrong layer in Level header / image v11 task placeholder missing / Out of Scope inheritance ambiguity / lib/ extraction decision "consider" needs lock

### ai-engineer HIGH
- **AI-3**: AD-M5-3 prompt lock is mode-agnostic; Spec Y narrowing redo to no-diff sections is undeclared AD deviation (need explicit AD-M5-3 narrowing update or cite different brainstorm decision)
- **AI-4**: T5.1 claude rewrite is NEW LLM call class — no model declared, no cost analysis, no risk row (3 retries × 2 modes × N dispatches = unbounded opus calls)
- **AI-5**: Redo prompt char budget undeclared (Spec X 240K cap is for changes; redo with ~14K realistic vs unbounded malicious issue body)
- **AI-6**: Prompt §3 "supersedes" reference format unspecified
- **AI-7**: claude -p commit_message extraction directive missing in T2.6 (Spec X T4.3 R2 F1 fix not inherited)

## MEDIUM (~10 items, deferred to R2/R3 or B.2 implementation)
- Redo branch name race (same-second timestamp collision)
- git commit --amend in retry loop force-push lease staleness
- Spec_id race for multiple concurrent redo dispatches
- End-to-end test gap (no full redo flow integration test)
- Drift-guard test references wrong migration filename
- spec_drift LLM token budget for proposal + diff (glm-air 128K window)
- Commit-lint timeout hardcoded 60s vs Spec X env-var pattern
- redo prompts/redo.tpl template file declaration missing
- rework_round cap shared changes+redo modes UX semantic
- lib/forgejo-helpers.sh extraction decision left "consider"

## LOW (~8 items)
- Forgejo PAT write scope (PR create requires write, Spec X only read)
- T-deploy v10→v11 image sequencing
- chore(redo-N) vs chore(rework-N) scope naming inconsistency
- Test file path collision check needed in B.2
- T0+T1 schema scope inside "Spec Y = redo-mode + aux" — accepted bundling per D2
- Memory references — verify `feedback_agent_team_for_level1` added
- Effort math: T0 (1h) + T8 (book-keeping) omitted from "~19h AI-runnable" status line (off by ~1h)
- Test count "~23 cases" claim should be enumerable

## R2 fix scope (substantial — parallel to Spec X v2 rewrite magnitude)

R2 must address all 6 CRITICAL + ~13 HIGH = ~19 surgical items. Estimated effort:
- Architecture decisions to lock: 4 (spec_id source, commit_validator path, S5/S6 binding, image rebuild)
- New tasks to add: T-pre REWORK_ROUND propagation, T0 renumber to 006, T2 prompts/redo.tpl declaration
- Existing tasks to refine: T2.6/T2.9 contract specificity, T3.x failure mode enumeration, T4.4 signature fix, T5.x Python-vs-shell decision propagation, T6.x test enumeration + regression commands, T7.2 AD-append guard literal, T8.1 Conv Commits examples enumeration

## Cross-agent agentId references (for SendMessage continuation)
- backend-architect R1: acb96f6596bfca066
- qa-engineer R1: a82c6516e35b279e9
- code-reviewer R1: a61f003d68b6f79f9
- ai-engineer R1: a72163c174b9329c8

## Convergence prognosis

Per `feedback_audit_convergence_pattern`:
- Spec X R1: 73 findings → R2: 20 (73% reduction critical+high 87%) → R3: 6 stability
- Spec Y R1: ~37 findings expected R2: ~10 → R3: stable (~2-3 rounds)

Phase A.2 R2 work parallel to Spec X v2 rewrite — substantial proposal + tasks restructure required.

**Recommendation**: Given context budget consumed by R1 audit + Spec Y is similar magnitude to Spec X R1 finding, R2 fix iteration in NEXT session would be more efficient (fresh context window). Current session has shipped Spec X full cycle + Spec Y Phase A.1 + R1 audit — substantial already.
