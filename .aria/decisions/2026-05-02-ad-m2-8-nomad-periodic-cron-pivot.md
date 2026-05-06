---
id: AD-M2-8
title: Nomad periodic job replaces hermes cron for Layer 1 tick scheduling
date: 2026-05-02
status: accepted
supersedes: parts of T1.3 / T6.1 (hermes cron registration assumption)
relates_to: AD-M2-7 (Option A pip-install), OD-10 (T1 AD3 deviation)
---

# AD-M2-8 — Nomad Periodic Job for Layer 1 Cron

## Decision

The `aria_layer1_tick` cron is scheduled by a dedicated **Nomad periodic
job** (`aria-orchestrator/deploy/aria-layer1-cron.nomad.hcl`), not by
hermes cron registry as originally specified in T1.3 / T6.1.

The hermes plugin (`aria-layer1`) remains loaded inside the
`aria-orchestrator` service for diagnostics and future skill-based
integration, but does **NOT** register itself with hermes cron.

## Context

T1.7 deploy on light-1 (2026-05-02) discovered that the hermes cron CLI
contract is fundamentally different from what M2 spec assumed:

| Spec / code assumption | Actual hermes 0.5.0+ contract |
|---|---|
| `hermes cron create --id X --command Y --interval Z` | `hermes cron create <schedule> [prompt] --skill SKILL` |
| Arbitrary `python -m ...` invocation | LLM prompts OR registered hermes skills only |
| Hook fires at gateway start | `on_session_start` fires only on first user chat |

The original T1.3 + T6.1 design relied on three assumptions, all wrong:
1. hermes cron accepts arbitrary commands (no — prompts/skills only)
2. `on_session_start` fires when hermes gateway starts (no — first chat)
3. `hermes cron create` flags `--id`, `--command`, `--interval` exist (no)

Reshaping Layer 1 as a hermes skill is a non-trivial refactor (skill
contract is LLM-prompt-driven, our state machine is deterministic Python),
better suited to M3 once US-023 begins.

## Choice

**B. Nomad periodic job** (chosen)

Pros:
- Decouples cron from hermes lifecycle entirely — hermes API churn does
  not break Layer 1 scheduling.
- Clean operational story: `aether status aria-layer1-cron` /
  `nomad job periodic force aria-layer1-cron` for E2E demo.
- Aligns with M2 dogfood "0 hermes core mods" intent (AD-M2-7 still holds).
- Same host volume + Nomad var path → 0 secret duplication.
- ~30min implementation; T15 E2E unblocked immediately.

Cons:
- Two Nomad job objects to manage (aria-orchestrator service + aria-layer1-cron periodic).
- Hermes plugin lifecycle (`on_session_start`) becomes vestigial for M2 — kept
  for M3 skill-pivot path.

## Alternatives considered

**A. Register Layer 1 as hermes skill** — deferred to M3 (US-023).
Reason: hermes skill contract assumes LLM-prompt invocation; our state
machine is deterministic Python. Wrapping it in a "no-op LLM call" skill
adds latency + LLM cost per tick, contrary to OD-9 cost intent.

**C. cron prompt that shells out** — rejected.
Reason: every tick costs an LLM call (~$0.001-0.01 / call × 24/day × 365
= ~$10-100/year just for triggering). Unjustifiable for deterministic
work.

## Implementation

1. New `deploy/aria-layer1-cron.nomad.hcl`:
   - `type = "batch"` + `periodic { cron = "0 * * * *" }`
   - `prohibit_overlap = true` (matches T3.3 advisory lock semantic)
   - raw_exec on light-1 (same node as aria-orchestrator)
   - Same env injection from `nomad/jobs/aria-orchestrator` (LUXENO + FEISHU)

2. `aria_layer1/__init__.py:register()`:
   - Remove load-time cron registration call
   - Keep `on_session_start` hook installed as no-op (hermes lifecycle compat)
   - Log message updated to point to Nomad periodic HCL

3. `extension.py:on_session_start()` and `_register_with_hermes_scheduler()`
   remain in source (untouched) — they're still the M3 skill-pivot path.
   Just no longer invoked at plugin load.

## Validation gate

- `aether dev run aria-layer1-cron.nomad.hcl --name aria-layer1-cron` → success
- `aether status aria-layer1-cron` → Type=periodic, status=running
- `nomad job periodic force aria-layer1-cron` → triggers immediate child job
- Child job alloc completes with exit 0 + stdout `{"processed": ..., "failed": 0}`

## Rollback

- `aether dev destroy aria-layer1-cron --yes`
- (aria-orchestrator service unaffected)

## M3 carry-over

When US-023 (M3) lands, evaluate:
- Refactor `tick_runner` as a hermes skill that wraps the deterministic
  state machine, OR
- Keep Nomad periodic as canonical scheduler + hermes plugin only as
  skill-exposed entry-point for ad-hoc human queries

Decision deferred to M3 brainstorm.

## References

- T1.7 deploy session 2026-05-02 (this conversation)
- AD-M2-7 (`aria-orchestrator/docs/architecture-decisions.md`)
- OD-10 (`.aria/decisions/2026-05-02-od-10-t1-ad3-deviation-finding.md`)
- hermes_cli/main.py (cron CLI definition, validates contract)
- hermes_cli/run_agent.py:6529 (on_session_start fires per chat session)
