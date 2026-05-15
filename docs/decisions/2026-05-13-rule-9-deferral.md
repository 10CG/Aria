# Decision: Rule #9 (Issue Triage SOP enforcement) — Deferred

> **Status**: Deferred (not added in cycle `aria-issue-triage-sop`)
> **Decision date**: 2026-05-13
> **Decision authority**: Owner (simonfish), audit-engine R1 unanimous endorsement
> **Cycle**: aria-issue-triage-sop
> **Related Spec**: `openspec/changes/aria-issue-triage-sop/proposal.md` §Open Questions Q2

---

## Decision

Rule #9 (forcing issue triage SOP execution before any fix-cycle response) is
**NOT added to CLAUDE.md** in this cycle. The 6-step issue triage SOP ships as:

- **Convention SOT**: `standards/conventions/issue-triage.md` — advisory guidance, same shelf as `git-commit.md`.
- **Skill**: `aria/skills/issue-triage/SKILL.md` + `scripts/triage.py` — `/issue-triage` trigger for opt-in use.
- **No CLAUDE.md non-negotiable rule** — current ruleset remains 8 rules (#1-#8).

A future cycle `aria-issue-triage-rule9-add` may revisit, gated on upgrade triggers below.

---

## Context

- 2026-05-13 triage of Forgejo Aria [#101](https://forgejo.10cg.pub/10CG/Aria/issues/101) surfaced a missing standard process: jumping to solution recommendation without version / code / in-flight / reproduction verification produced a `partial-repro` (2/4 hit rate, not the reported 4/4).
- Cycle `aria-issue-triage-sop` formalizes a 6-step SOP (read → version → code path → git log → in-flight → reproduction → verdict).
- Open Question Q2 in the proposal asked: should CLAUDE.md gain a Rule #9 enforcing this SOP before any issue-driven fix cycle?
- R1 audit (3/3 unanimous, see audit footprint below) recommended **defer**; this memo formalizes that decision.

---

## Rationale

### Aria precedent: non-negotiable rules are incident-driven

CLAUDE.md Rules #1-#8 share a pattern. The two most recent (#7, #8) were
formalized only after a documented production incident. Earlier rules
(#1-#5) crystallized accumulated convention pain (OpenSpec scaffolding,
ten-step-cycle drift); #6 was driven by benchmark-runner divergence (Aria
self-evidence). The triage SOP has, today, neither incident class.

| Rule | Subject | Trigger evidence | Date |
|------|---------|------------------|------|
| #1 | All requirement changes must have OpenSpec | accumulated Spec drift across early cycles | early |
| #2 | Ten-step cycle cannot skip Phase A | repeated "act-before-understand" anti-pattern | early |
| #3 | Docs & code must co-evolve | architecture-docs-stale incidents | early |
| #4 | Conventional Commits | commit-msg quality drift | early |
| #5 | Change location boundary (project, not `standards/`) | `aria-standards` shared-submodule pollution | 2026-Q1 |
| #6 | Skill benchmark must use `/skill-creator` | self-built runner divergence (Aria self-evidence) | 2026-Q2 |
| #7 | Secret-hygiene redirect output | Forgejo Aria #78 (4 keys via `nomad inspect`) + truffle-hound #4 (4 keys via Python subprocess inherit stdio) | 2026-05-02 |
| #8 | Pre-merge gate (`aether ci status --in-flight`) | Forgejo SilkNode PR-321 cancelled main PR-322 CI Run #3161 (459s deploy obs loss) | 2026-05-02 |

Issue-triage SOP status as of decision:

- **Single dogfood data point**: Forgejo Aria #101 — the cycle's own trigger.
- **Zero documented "missed-triage" failure**: no recorded case where lack of triage SOP caused a fix cycle to mis-target a non-issue, duplicate in-flight work, or miss a fixed-in-X.
- **Skill is v1.0 and unbenchmarked at decision time** (T8 skill-creator AB benchmark runs later in this cycle).

Hardcoding Rule #9 now would (a) ossify a not-yet-validated Skill, (b) create
friction on skip-eligible cases (docs-only PRs, typo fixes, "thanks will look"
acks), and (c) invert Aria's incident-driven precedent.

### Cost asymmetry

The cost of deferring Rule #9 is bounded and reversible: maintainers may skip
triage on a real issue → fix-cycle wastes work → that single incident becomes
the counter-incident signal that promotes Rule #9. The cost of premature
Rule #9 is unbounded: every issue interaction (including the cheap ones the
SOP itself flags skip-eligible) pays the SOP tax, and rolling back a
non-negotiable rule once published damages the credibility of the rule list
itself (Rules #1-#8 have never been retracted; that invariant is load-bearing
for the "non-negotiable" semantic).

### Why not split the difference (warning-level rule)

A middle path — adding Rule #9 as "SHOULD invoke `/issue-triage`, with
documented exceptions" — was considered and rejected. CLAUDE.md
non-negotiable rules use MUST semantics; introducing SHOULD-level rules
creates a two-tier ruleset and forces every future rule to declare its tier.
The convention doc at `standards/conventions/issue-triage.md` already
provides the SHOULD-level surface; CLAUDE.md should remain MUST-only.

### Counterfactual

If Rule #9 were added now:

| Variant | Effect | Why not |
|---------|--------|---------|
| Strict ("must invoke `/issue-triage` before any issue-driven action") | Every issue interaction gates on Skill execution; ack messages, docs-only fixes, typo PRs all blocked | Over-trigger on cases the SOP itself flags as skip-eligible |
| Advisory ("should invoke `/issue-triage` when…") | Close to current `standards/conventions/issue-triage.md` posture but adds CLAUDE.md surface area | Marginal value over the convention doc; dilutes the "non-negotiable" semantic of the existing 8 rules |

Both variants harden a process before its first benchmark report. Aria's
small-step principle (Rule #2 spirit) and Rule #6 (benchmark-before-trust)
both argue for deferral.

---

## Upgrade triggers

Reconsider Rule #9 in a follow-on cycle `aria-issue-triage-rule9-add` when
**BOTH** conditions hold:

| # | Condition | Measurement |
|---|-----------|-------------|
| 1 | **Dogfood signal**: ≥3 issues triaged via `/issue-triage` Skill with verdicts recorded | `aria/skills/issue-triage/dogfood-log.md` (or equivalent) lists ≥3 entries with verdict ∈ {`confirmed`, `partial-repro`, `not-reproducible`, `fixed-in-X`, `duplicate-of-#N`, `needs-info`, `wont-fix`}; ≥1 entry should be `partial-repro` / `duplicate-of-#N` / `fixed-in-X` (i.e., the Skill caught something a naive read would have missed) |
| 2 | **Counter-incident**: ≥1 documented case where triage was skipped and produced wasted work | Forgejo Aria issue or `.aria/decisions/` memo records: maintainer (human or AI) bypassed `/issue-triage`, opened a fix cycle, and the cycle hit one of: wrong target / duplicate of in-flight work / fixed-in-X miss / non-reproducible chasing |

Both signals are required:

- Signal 1 alone shows tool value but not enforcement need (Skill can stay advisory).
- Signal 2 alone may be a one-off / outlier; promoting to non-negotiable rule needs corroborating tool maturity.

Upgrade cycle naming: `aria-issue-triage-rule9-add` (predictable Spec ID for future search).

---

## Decision authority

- **Owner**: simonfish (uni.concept.wzfq@gmail.com), per Aria solo-lab governance (AD-M0-9: owner = decision authority = PR approver).
- **Supporting evidence**: audit-engine R1 unanimous endorsement (3/3 agents PASS_WITH_WARNINGS on the deferral decision itself; CLOSED in Q2 of proposal §Open Questions).
- **Sign-off mechanism**: PR approval on the cycle's collective T6 commit; this memo file is the durable artifact.

---

## Out of scope for this memo

- The 6-step SOP itself (lives in `standards/conventions/issue-triage.md`).
- Skill implementation details (see `aria/skills/issue-triage/SKILL.md` + `scripts/triage.py`).
- Specific wording of Rule #9 (deferred until upgrade triggers fire; drafting in follow-on cycle).
- Webhook / auto-trigger infrastructure (Spec Q4: M1 manual-only; webhook needs `aria-runner-bot`, separate cycle).

---

## References

| Type | Path / link |
|------|-------------|
| Spec | `openspec/changes/aria-issue-triage-sop/proposal.md` (Open Q2) |
| Spec tasks | `openspec/changes/aria-issue-triage-sop/tasks.md` §T6 |
| Convention SOT | `standards/conventions/issue-triage.md` |
| Skill | `aria/skills/issue-triage/SKILL.md` |
| Audit R1 | `.aria/audit-reports/post_spec-R1-2026-05-13T0030Z-aria-issue-triage-sop.md` (PASS_WITH_WARNINGS, 3/3 unanimous) |
| Audit R2 | `.aria/audit-reports/post_spec-R2-2026-05-13T0130Z-aria-issue-triage-sop.md` (SCOPE_OK_R2, 29/29 R1 CLOSED) |
| Trigger issue | https://forgejo.10cg.pub/10CG/Aria/issues/101 |
| Canonical case study | https://forgejo.10cg.pub/10CG/Aria/issues/101#issuecomment-5972 |
| Current CLAUDE.md rules (#1-#8) | `/home/dev/Aria/CLAUDE.md` §不可协商规则 |
| Precedent: deferred decision with renewal criteria | `.aria/decisions/2026-05-07-silknode-contract-archive-with-deferred-acceptance.md` |
| Precedent: incident-driven Rule #7 | Forgejo Aria #78 + `standards/conventions/secret-hygiene.md` |
| Precedent: incident-driven Rule #8 | Forgejo Aria #60 + `aria/skills/phase-c-integrator/SKILL.md` §C.2.4 |

---

## Version history

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-05-13 | Initial memo. Rule #9 deferred. Upgrade triggers (dogfood ≥3 + counter-incident ≥1) recorded. Authored under T6 of cycle `aria-issue-triage-sop`. |
