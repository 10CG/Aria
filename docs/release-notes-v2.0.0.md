# Aria v2.0.0 Release Notes

> **Status**: In Progress (M6 execution phase; TG-DOCS-B architecture docs may ship as v2.0.1 per Q-final-1 Menu C)
> **Date**: 2026-05-27
> **Main Repo**: https://github.com/10CG/Aria
> **Plugin Repo**: https://github.com/10CG/aria-plugin

---

## Plugin Compatibility — aria-plugin 不随 Aria 2.0 同 bump

aria-plugin (the Claude Code plugin that provides Aria's Skills and Agents) follows its own **independent versioning stream** (currently v1.28.0). It is **NOT bumped to v2.0** when Aria main repo releases v2.0.0.

**Semantic boundary**:

| Component | Version at v2.0.0 release | What it contains |
|-----------|--------------------------|-----------------|
| **Aria main repo** | v2.0.0 | Methodology definition + autonomous runtime (`aria-orchestrator`) |
| **aria-plugin** | v1.28.x (independent) | Interactive Skills + Agents used in Claude Code sessions |

**For plugin users**: no action needed. Projects using aria-plugin for interactive AI-DDD collaboration do not need to do anything when Aria 2.0 releases. The plugin version you have installed continues to work unchanged.

**Why independent versioning?** The Aria main repo version tracks the methodology maturity and autonomous runtime milestones (M0-M6). The plugin version tracks interactive tooling capability (Skills, Agents, benchmarks). These are decoupled by design: the plugin can ship patches and features on its own cadence without being blocked by runtime milestones, and vice versa.

---

## Highlights — M1-M5 Delivery Summary

Aria 2.0 v2.0.0 ships the first production-grade **autonomous execution layer** on top of the proven v1.x methodology.

### Layer 1/2 Architecture (M1 + M2)

Two-layer AI execution model:
- **Layer 1 (AI PM)**: Hermes + Luxeno-routed GLM models. Handles triage, dispatch, and merge approval via Feishu human gate (S7_AWAITING_MERGE is the single human gate in the loop, per AD10).
- **Layer 2 (AI Engineer)**: aria-runner container + Claude Code + aria-plugin. Executes the full ten-step cycle autonomously.

Communication between layers uses **humanized YAML commands** (natural language) — not structured RPC. This design (AD1 + AD6) ensures Layer 1 commands are human-readable and auditable.

### Dispatch Loop (M2)

State machine S0-S9 + S_FAIL implemented in aria-orchestrator. Proven with 268 tests across 156h of development. The dispatch loop handles GitHub issue triage → spec creation → branch dispatch → code review → merge approval.

### Crash Recovery + Reconciler (M3 + M4)

- **Crash recovery**: aria-runner containers restart after failure and resume from last known state (M3).
- **Reconciler**: detects drift between Layer 1 state and Layer 2 actual state; auto-reconciles orphaned tasks (M4, ~22h vs 60h budget, ×0.42 efficiency gain).

### Cost Tracking (Spec #1)

Locked `cost.json` schema (`metered_usd`, `subscription_usd`, `freshness_ts`) for cross-layer cost tracking. See `aria-orchestrator/docs/layer-boundary-contract.md`.

### E2E Resilience (M5 + Spec #2)

Replay + reconciler + drift-review loop audited and production-hardened. 793 tests passing. Cost routing verified end-to-end.

---

## Migration Notes

**Non-migration**: there are no breaking changes for interactive Aria methodology users.

- The ten-step cycle, OpenSpec format, and nine non-negotiable rules are **unchanged**.
- The aria-plugin Skills and Agents are **unchanged** (plugin does not bump to v2.0).
- The `standards/` submodule conventions are **unchanged**.
- The `aria-orchestrator/` autonomous runtime is an **additive internal layer** (10CG Lab only).

If you use Aria interactively via Claude Code + aria-plugin, v2.0.0 of the main repo is a documentation and architecture milestone — it does not require you to change anything.

**TG-DOCS-B note**: Architecture documentation updates (system-architecture.md v2.0, version-scheme.md, standards/autonomous/) may ship as v2.0.1 if the 5-week calendar slips per Q-final-1 Menu C. This is an owner decision gate. The CLAUDE.md v2.0 update and state-checks probes ship with v2.0.0 unconditionally.

---

## Known Limitations

1. **TG-DOCS-B architecture docs** (`docs/architecture/system-architecture.md` v2.0, `docs/architecture/version-scheme.md`, `standards/autonomous/`) may ship as **v2.0.1** if the 5-week calendar is tight (per Q-final-1 Menu C owner gate). The `m6-arch-doc-stale` state-check probe will fire as a `warning` (non-blocking) during this window.

2. **aria-fleet three-layer architecture** (generic / workspace / instance) is a post-M6 item. Brainstorm decision D1-D6 Approved 2026-05-27. Not in v2.0.0 scope.

3. **Layer 2 cost routing** to Luxeno (GLM via aria-layer1) requires the `ZHIPU_API_KEY` Nomad variable to be configured. See `.aria/notes/` for routing documentation.

---

## Forgejo Discussion FAQ

> **Owner action required**: Post this section as a Forgejo Discussion thread after Spec #4 (`aria-2.0-m6-release-closeout`) tags v2.0.0. Spec #4 will verify the Discussion URL liveness. The text below is the canonical FAQ for the thread.

---

**Q: Does aria-plugin need updating when Aria 2.0 releases?**

A: No. aria-plugin follows its own independent version stream. When Aria main repo releases v2.0.0, the plugin remains at v1.28.x (or whatever version you have installed). There is no required upgrade. Your existing `aria@10CG-aria-plugin` installation continues to work.

---

**Q: What changed in Aria 2.0 vs 1.x?**

A: Aria 2.0 adds an autonomous execution runtime (`aria-orchestrator`) on top of the v1.x methodology. The methodology itself (ten-step cycle, OpenSpec, nine non-negotiable rules) is unchanged. The plugin's interactive Skills and Agents are unchanged. The new layer is an internal 10CG Lab infrastructure that validates the methodology works in unattended (no human in the loop except one merge gate) scenarios.

Summary of additions:
- `aria-orchestrator/`: Layer 1 (AI PM) + Layer 2 (AI Engineer) dispatch infrastructure
- State machine S0-S9 with one human gate (S7_AWAITING_MERGE via Feishu)
- Crash recovery, reconciler, cost tracking, E2E resilience (M1-M5 delivery)

---

**Q: Who is Aria 2.0 for?**

A: The **autonomous runtime** (`aria-orchestrator`) is for 10CG Lab internal projects only. It is not released as a public framework. The **Aria plugin** (aria-plugin v1.28.x) remains universally available for any project using Claude Code. If you use the plugin for interactive AI-DDD collaboration, Aria 2.0 does not change anything for you — the methodology is the same, and the plugin is the same.

---

**Q: I'm using aria-plugin v1.27.x. Should I upgrade to v1.28.x?**

A: Plugin upgrades are independent of the Aria v2.0.0 milestone. Check the [aria-plugin CHANGELOG](https://github.com/10CG/aria-plugin/blob/master/CHANGELOG.md) for what's in v1.28.x and upgrade at your own pace. The v2.0.0 release of the main repo does not require any specific plugin version.
