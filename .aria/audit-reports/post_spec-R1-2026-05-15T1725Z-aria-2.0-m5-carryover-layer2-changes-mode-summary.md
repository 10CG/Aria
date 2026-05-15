---
checkpoint: post_spec
mode: convergence
round: R1
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-05-15T17:25Z
spec_id: aria-2.0-m5-carryover-layer2-changes-mode
context: openspec/changes/aria-2.0-m5-carryover-layer2-changes-mode/
agents: [backend-architect, ai-engineer, code-reviewer, qa-engineer, context-manager]
total_findings: 73
severity_breakdown:
  critical: 8
  high: 25
  medium: 27
  low: 13
---

# R1 post_spec Audit — Spec X (M5 carryover Layer 2 changes-mode)

## Overall Verdict: FAIL → R2 Required

5 agents reported BLOCK / REVISE / NEEDS_FIX. 73 findings total. Multi-agent consensus on
critical foundation drift between Spec X v1 and Layer 2 reality.

## Critical Findings (≥2 agent consensus)

### C1 — Layer 2 entrypoint is BASH, not Python (backend-architect + context-manager)

- **Spec X v1 claim**: "现有 entrypoint script 主逻辑迁入 `mode_initial.py`,零行为变更" (proposal §C, tasks T3)
- **Reality** (verified via filesystem):
  - `docker/aria-runner/entrypoint-m1.sh` = 596-line bash
  - `docker/aria-runner/entrypoint.sh` = 58-line bash
  - `docker/aria-runner/tests/` = bash fixtures (test.sh, setup.sh)
  - Dockerfile: `FROM node:20-bookworm-slim`, Claude CLI via `npm install -g`, no Python `aria_layer2_runner/` package
- **Impact**: T3 (Python refactor 3h) actually = bash dispatcher split + new mode_changes.sh (~6h, still reasonable)
- **Fix direction**: Reframe Spec X v2 as **shell-based mode dispatcher** (preserves A2 skeleton-then-fill pattern)

### C2 — AD-M5-3 status line: append-only, not replace (context-manager + backend-architect)

- **Spec X v1**: T7.3 overwrites AD-M5-3 status "DEFERRED to M6" → "in progress via Spec X"
- **Issue**: AD is immutable decision record. Replace breaks audit trail.
- **Fix**: Append "2026-05-15: Implementation in-flight via Spec X (aria-2.0-m5-carryover-layer2-changes-mode)" as new line, preserve original

### C3 — `claude -p --prompt-file <file>` flag does NOT exist (ai-engineer)

- **Spec X v1**: T4.3 invokes `claude -p --prompt-file <assembled>`
- **Reality**: `entrypoint-m1.sh:314` uses positional `claude -p "$RENDERED_PROMPT"`
- **Fix**: Match existing invocation pattern (positional or heredoc)

### C4 — `aria_layer1` Python package not in Layer 2 image (backend-architect)

- **Spec X v1**: `mode_changes.py` says "reuse `aria_layer1/forgejo_client.py` 或子集 inline"
- **Reality**: Layer 2 image only has Node + claude CLI; aria_layer1 Python pkg not installed
- **Fix**: Use existing bash + curl + jq pattern (entrypoint-m1.sh §6 already does this for issue fetch)

### C5 — 60K token cap fallback behavior contradicts across 3 docs (ai-engineer + code-reviewer)

- AD-M5-3: "fallback to redo mode + audit log warn"
- proposal §D: "fallback to redo mode... Spec X 期间报错明确 + sys.exit(2)"
- tasks T4.2: "audit log + sys.exit(2) (Spec Y ship 后改 fallback)"
- **Fix**: Lock single Spec-X-window behavior: sys.exit(2) + S_FAIL(prompt_overflow); update AD-M5-3 to clarify "Spec Y ship 后" semantic

### C6 — 'retry' mode handler routing semantically inverted (ai-engineer + backend-architect)

- **Spec X v1**: `'retry': handle_initial` aliased
- **Issue**: retry rows carry REWORK_FEEDBACK (from failure_analysis suggested_owner_action); handle_initial discards it
- **Fix**: Either (a) Layer 1 does NOT write REWORK_MODE for retry rows, OR (b) dedicate retry handler that consumes failure-analysis context

### C7 — Regression gate unenforceable (qa-engineer + code-reviewer)

- **Spec X v1**: T6.5 "现有 M5 initial mode tests all PASS" — no specific test files listed
- **Fix**: Enumerate explicit test paths + runnable pytest command

### C8 — `build_nomad_meta` MetaSizeExceeded risk (qa-engineer)

- 4KB REWORK_FEEDBACK + 5 required meta keys can exceed Nomad meta cap
- **Fix**: Add test asserting near-4KB feedback passes through

## High-severity Findings (single-agent, action required)

### From ai-engineer
- HIGH#2: tiktoken vs char×0.25 unselected (Claude tokenizer mismatch)
- HIGH#5: Layer 2 model+provider path (claude-opus via Luxeno, not M3 GLM router) not documented

### From qa-engineer
- HIGH: REWORK_FEEDBACK at exact-4KB / 4097-byte boundary untested
- HIGH: REWORK_FEEDBACK UTF-8 codepoint corruption risk at byte-slice boundary
- HIGH: Forgejo 4xx (404/403) failure modes untested (only 5xx covered)
- HIGH: git push --force-with-lease rejection (stale ref) exit-code path untested
- HIGH: HCL parameterized payload meta key inventory vs T1.3 written keys cross-check (name mismatch invisible to nomad validate)
- HIGH: spec_id schema column for Spec Y OS-4 — Spec X silent
- HIGH: T6 2h estimate insufficient for ~30 tests + 1-3 expected real bugs

### From code-reviewer
- HIGH: AD-M5-3 line range 3574-3629 spans into AD-M5-4 (correct range 3574-3613)
- HIGH: brainstorm D5 lists 3 mode keys; proposal adds 4th `'retry'` not in brainstorm
- HIGH: T7.3 patch instruction missing search target text

### From context-manager
- I1: D7 absorption — no receiving doc in US-026 / PRD
- I2: M5-OS-2/3/4/5 absorbed_by sequencing ambiguous (Spec X vs Spec Y mark timing)
- I3+I5: US-025 footer / handoff doc Spec X kickoff link missing
- I4: US-025 status line not updated to reflect multi-Spec carryover
- I6: Forgejo PAT secret-hygiene compliance unstated (Rule #7)
- I7: dual-repo (aria-orchestrator + Aria main) pre-merge gate scope (Rule #8)
- I8: Phase D.3 handoff trigger (Rule #9) not evaluated
- I9: AD-M5-3 §risk #1 mitigation explicit cross-ref missing
- I-misc: T5.5 HCL `IMAGE_SHA` described as `meta_optional` default — actually `meta_required`

## Convergence Status

- R1 conclusions_stable: N/A (no R0 to compare)
- R1 unanimous_pass: false (all 5 agents REVISE/BLOCK/NEEDS_FIX)
- → R2 required

## Next Action: R2

Author will rewrite proposal.md + tasks.md to:
1. Reframe T3 as bash mode dispatcher (split entrypoint-m1.sh)
2. Match existing claude -p invocation
3. Use bash curl + jq + envsubst (no Python aria_layer1 import)
4. Append AD-M5-3 status, not replace
5. Lock 60K overflow to sys.exit(2) S_FAIL(prompt_overflow) (Spec X window)
6. Resolve 'retry' mode (Layer 1 does not write REWORK_MODE for retry rows)
7. Enumerate explicit test paths under existing docker/aria-runner/tests/
8. Fix AD-M5-3 line range, image tag naming, US-025 status line, etc.
9. Add ~12 missing tests (UTF-8, 4xx, exit-code, MetaSizeExceeded, etc.)
10. Cross-ref Rule #7 Forgejo PAT secret-hygiene, Rule #8 dual-repo gate, Rule #9 D.3 handoff

After rewrite → R2 with same 5 agents to verify findings closed + no new critical.

## Files referenced in R1
- `/home/dev/Aria/openspec/changes/aria-2.0-m5-carryover-layer2-changes-mode/{proposal,tasks}.md`
- `/home/dev/Aria/.aria/decisions/2026-05-15-m6-brainstorm.md`
- `/home/dev/Aria/aria-orchestrator/docker/aria-runner/{entrypoint-m1.sh,entrypoint.sh,Dockerfile,tests/}`
- `/home/dev/Aria/aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/{extension.py,db.py,failure_analysis.py,forgejo_client.py}`
- `/home/dev/Aria/aria-orchestrator/nomad/jobs/aria-layer2-runner.hcl`
- `/home/dev/Aria/aria-orchestrator/docs/architecture-decisions.md` (AD-M5-3 / M5-4 / M5-6 / M5-10 / M1-7)
- `/home/dev/Aria/aria-orchestrator/docs/m5-handoff.yaml`
- `/home/dev/Aria/docs/handoff/2026-05-15-us025-m5-c2-d1-done.md`
- `/home/dev/Aria/docs/requirements/{prd-aria-v2.md, user-stories/US-025.md}`
- `/home/dev/Aria/CLAUDE.md` (Rule #5/#6/#7/#8/#9)

## Per-agent agentId references (for SendMessage continuation if needed)
- backend-architect: a94baed50b572784a
- ai-engineer: a6e4c751c46cfcb57
- code-reviewer: a4b6d59362a2c427b
- qa-engineer: a738545c000d0e88c
- context-manager: aeeb9a6695b24e8d2
