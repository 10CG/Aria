# Aria 2.0 M6 Spec #4 — Release Closeout (pre-release gates orchestrator + archive trigger)

> **Level**: 2 (Minimal — single net-new orchestrator script + 5 net-new gate primitives + 4-directory archive runner; no schema changes, no submodule-internal changes, no cross-cutting refactor)
> **Status**: Draft (Phase A.1 — 2026-05-25 起草 by tech-lead agent; 待 Phase A.2 audit)
> **Change ID**: `aria-2.0-m6-release-closeout`
> **Parent US**: [US-026](../../../docs/requirements/user-stories/US-026.md)
> **Parent PRD**: [prd-aria-v2.md §M6](../../../docs/requirements/prd-aria-v2.md) (Week 26-30, post `a786444` + `e884e62` patches, §637-660 量化/定性指标)
> **Predecessor Specs (Spec #4 gates on outputs of all three)**:
>   - [aria-2.0-m6-cost-acceptance](../aria-2.0-m6-cost-acceptance/proposal.md) (Spec #1, Approved `c29a800` 2026-05-24; G-1 consumes `validate-m6-handoff.py`)
>   - [aria-2.0-m6-e2e-resilience](../aria-2.0-m6-e2e-resilience/proposal.md) (Spec #2, Approved 2026-05-24; G-2 consumes `check-m6-e2e-acceptance.py`)
>   - [aria-2.0-m6-docs](../aria-2.0-m6-docs/proposal.md) (Spec #3, Approved 2026-05-24; G-3 consumes CLAUDE.md v2.0 + state-checks 3 probes — TG-DOCS-A only; TG-DOCS-B v2.0.1-deferrable per Q-final-1 Menu C is NOT in Spec #4's release-gate scope)
> **Successor Specs**: **none** — Spec #4 is the M6 terminal Spec. After Spec #4 Phase D archive runner executes, all 4 M6 Specs move to `openspec/archive/` and M6 closes.
> **Brainstorm Source**: [.aria/decisions/2026-05-24-us026-m6b-brainstorm.md](../../../.aria/decisions/2026-05-24-us026-m6b-brainstorm.md) (DEC-20260524-001 Q-final-1 Menu C lock — Spec #4 as RED/ABORT pre-release gates; CONVERGED 2026-05-24)
> **Effort baseline**: ~10h impl baseline (T-A2 orchestrator ~3h + T-A3 tests ~3h + T-A4 archive runner ~1.5h + T-A5 docs ~1h + T-A1 scaffolding ~0.5h + T-A6 memory candidate ~0.5h + ~0.5h buffer). Single SoT per `[[feedback_spec_v2_body_propagation_2pass]]`; cited identically in frontmatter + §Effort baseline + tasks.md.
> **AD allocation reservation**: **AD-M6-10**, **AD-M6-11**, and **AD-M6-12** are reserved for this Spec #4. AD-M6-10 = orchestrator exit code aggregation contract. AD-M6-11 = atomic-archive 4-directory transactional pattern. AD-M6-12 = secret rotation buffer threshold (21d RED / 14d ABORT) calibration. Spec #1 holds AD-M6-1/2/3; Spec #2 holds AD-M6-4/5/6; Spec #3 holds AD-M6-7/8/9. (per DEC-20260524-001 §2 AD-M6-* allocation lock 2026-05-24)
> **Authored by**: Claude Opus 4.7 via `aria:tech-lead` agent, 2026-05-25

---

## Why

M6 ships three independently-Approved Specs (#1 cost-acceptance / #2 e2e-resilience / #3 docs) plus a hard-coded set of release-hygiene checks that span all three plus 5 net-new dimensions that no single sibling Spec owns. Without an orchestrator that consumes all sibling acceptance outputs and adds the cross-cutting gates, the v2.0.0 ship decision is reduced to "owner manually runs ~8 scripts + 5 ad-hoc grep checks and hopes nothing was missed" — a textbook paper-fix antipattern per `[[feedback_paper_fix_antipattern]]`.

**Four release-hygiene problems Spec #4 closes**:

1. **No top-level PASS/RED/ABORT verdict**: Spec #1 emits its own exit codes (0/1/2), Spec #2 emits per-`--tg-{a,b,c}` exit codes, Spec #3 ships 3 state-checks probes — but there is no single command that says "ship or not". Owner needs `python3 aria-orchestrator/acceptance/check-m6-release-readiness.py` → exit 0/1/2 with structured per-gate report.

2. **Secret rotation hard cap 2026-08-02 has no automated buffer warning**: per `[[project_secret_rotation_deferred_2026-05-02]]`, the partial rotation deadline is hard-capped at 2026-08-02 (9-key carry-forward debt). If M6 ships within `<14d` of that cap, owner has no slack to rotate secrets post-release — a foreseeable cliff. Spec #4 G-4 surfaces this as `<21d → RED` (informational warn) / `<14d → ABORT` (hard block).

3. **5-files SemVer drift would silently break Plugin Compatibility**: CLAUDE.md "版本发布检查清单" lists 5 files (plugin.json SoT + 4 derived) that must all match. Per `[[feedback_plugin_version_drift_multiple_sources]]`, drift between these has been observed mid-session (v1.22.0 stale in CLAUDE.md while plugin.json = v1.27.0). Without an automated probe, manual bump errors silently propagate to market consumers. G-7 catches this pre-ship.

4. **Submodule pointer drift + Forgejo Discussion URL liveness + archive-trigger eligibility are orthogonal "loose ends"**: Each of these would either degrade release credibility (G-5 submodule misalignment → market consumers fetch broken pointers), break documented promises (G-6 FAQ URL 404 after Spec #3 ships release notes citing it), or cause out-of-order archives (G-8 sibling already archived → Spec #4 cannot orchestrate). They share orchestrator infrastructure but no single sibling owns them.

**Gate role in M6 sequencing**: Spec #4 runs **AFTER** Specs #1+#2+#3 implementation complete (gates all of them). Per DEC-20260524-001 Q-final-1 Menu C: Spec #4 is the **last** Spec in M6, sequenced strictly post-#1/#2/#3-Phase-B. Spec #4 Phase B itself takes ~10h and does NOT block on Spec #2's 7-day e2e run completion (G-2 reads Spec #2 acceptance script which can return early once 7-day window has elapsed).

---

## What

### In scope (~10h impl)

#### A. Top-level orchestrator script (~3h)

**Target file**: `/home/dev/Aria/aria-orchestrator/acceptance/check-m6-release-readiness.py` (NEW; directory created by Spec #1 T-acceptance, sibling to `check-m6-cost-acceptance.py` and `check-m6-e2e-acceptance.py`)

Python 3.9+ stdlib only (no third-party deps). Runs G-1..G-8 in sequence, aggregates per-gate exit codes, and emits a single top-level verdict.

**Per-gate output format** (stdout, one line per gate):
```
[PASS|RED|ABORT] G-N: <one-line description>
```

**Top-level verdict** (last stdout line + exit code):
```
[VERDICT] ALL_PASS  → exit 0   (every gate PASS; ship)
[VERDICT] RED       → exit 1   (≥1 RED gate, no ABORT; owner may --owner-override "<rationale>" for ship; otherwise hold)
[VERDICT] ABORT     → exit 2   (≥1 ABORT gate; no override path; hard block until remediated)
```

**Owner override semantics** (AD-M6-10):
- `--owner-override "<rationale>"` CLI flag is honored ONLY when VERDICT == RED.
- Override on VERDICT == ABORT is rejected with `[ERROR] --owner-override rejected: ABORT verdict has no override path; remediate failing gate(s)` and exit 2.
- Override rationale string is required (non-empty); empty rationale rejected with exit 2.
- Override usage is logged into the summary report (§A.4 below) with timestamp + rationale verbatim.

**Summary report** (`.aria/m6-release-readiness/{YYYY-MM-DDTHHMMSSZ}-report.md`):
- Filename uses `datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')` (RFC-3339-ish but filename-safe — no colons).
- Idempotent on repeat run: each invocation writes a NEW timestamped file (does not overwrite); directory accumulates audit trail per `[[feedback_audit_driven_fix_conventions]]`.
- Content: per-gate verdict + raw subprocess stdout/stderr captured + top-level verdict + override usage (if any) + invocation arguments.

#### B. Gate G-1..G-3: sibling consumption (~1h, part of A2.x impl above)

Spec #4 does NOT re-implement sibling logic. G-1..G-3 are thin subprocess wrappers around sibling-delivered scripts; Spec #4 only judges exit code propagation.

| Gate | Sibling source | Evidence script | PASS condition | RED/ABORT logic |
|------|----------------|-----------------|----------------|-----------------|
| G-1 cost-acceptance | Spec #1 AC-6 + AC-7 + AC-9 | `python3 aria-orchestrator/docs/validate-m6-handoff.py --all` | exit 0 | exit 1 → RED ; exit 2 → ABORT |
| G-2 e2e-resilience | Spec #2 AC-1 + AC-3 + AC-5 (7d uptime + 6 crash modes + humanized median ≥7) | `python3 aria-orchestrator/acceptance/check-m6-e2e-acceptance.py --all` | exit 0 | exit 1 → RED ; exit 2 → ABORT |
| G-3 docs | Spec #3 AC-1 + AC-4 (CLAUDE.md v2.0 + 3 state-checks probes registered) | (a) CLAUDE.md grep `**版本**: 2.0.0` + `两层 AI 分工` + `Aria 2.0 运行时` + (b) state-checks.yaml YAML parse → assert all 3 `m6-*` probe names present | both (a) and (b) pass | either grep failure → RED ; YAML parse error → ABORT |

**G-1 detail**: Spec #1 `validate-m6-handoff.py` ships `--check-abi-compat`, `--check-3-day-history`, `--check-cost-method-enum`, `--check-pricing-freshness`. Spec #1 §AC-6 requires `--check-abi-compat` exit 0; §AC-7 requires `--check-3-day-history` exit 0; §AC-9 requires the acceptance script side. The `--all` mega-flag is a Spec #1-side addition that Spec #4 expects (per Spec #4 Risk R-M6CL-2: if Spec #1 ships without `--all`, Spec #4 G-1 falls back to invoking 4 individual flags + ANDing exit codes — Phase B kick verify probe catches this in T-A2.2).

**G-2 detail**: Spec #2 `check-m6-e2e-acceptance.py` ships `--tg-a` / `--tg-b` / `--tg-c`. The `--all` flag aggregates all three. Spec #4 G-2 invokes `--all`.

**G-3 detail**: Per Spec #3 §A.6, 3 state-checks probes are `m6-version-badge-match`, `m6-claude-md-version`, `m6-arch-doc-stale`. Per Spec #3 §AC-4 the YAML-parse check is the authoritative gate; Spec #4 G-3 reuses Spec #3's exact YAML-parse logic.

#### C. Gate G-4: secret rotation buffer (~0.5h, threaded into A2.5)

**Source**: `[[project_secret_rotation_deferred_2026-05-02]]` 2026-05-20 updated → original 4-key + new 5-key partial rotation, hard cap **2026-08-02**.

**Logic**:
```python
from datetime import date, datetime, timezone
import os

HARD_CAP = date(2026, 8, 2)
override = os.environ.get('M6_RELEASE_TODAY_OVERRIDE')  # YYYY-MM-DD for tests
today = date.fromisoformat(override) if override else datetime.now(timezone.utc).date()
buffer_days = (HARD_CAP - today).days

if buffer_days >= 21:
    print(f"[PASS] G-4: secret rotation buffer {buffer_days}d (cap {HARD_CAP.isoformat()})")
elif buffer_days >= 14:
    print(f"[RED] G-4: secret rotation buffer {buffer_days}d < 21d (cap {HARD_CAP.isoformat()}); owner advisory")
else:
    print(f"[ABORT] G-4: secret rotation buffer {buffer_days}d < 14d (cap {HARD_CAP.isoformat()}); rotate before release")
```

**Boundary semantics** (binary-falsifiable):
- `buffer_days >= 21` → PASS (green)
- `14 <= buffer_days < 21` → RED (informational warn — owner may override)
- `buffer_days < 14` → ABORT (hard block — no override; owner must rotate or extend cap)

**Date injection for tests**: `M6_RELEASE_TODAY_OVERRIDE=YYYY-MM-DD` environment variable, parsed via `date.fromisoformat()`. Test fixtures use this for 3-boundary coverage per AC-3.

#### D. Gate G-5: submodule pointer pre-release probe (~0.5h, threaded into A2.6)

**Submodules covered** (per `.gitmodules` enumeration at Phase B time): `aria/` + `standards/` + `aria-orchestrator/` (if present as submodule; if `aria-orchestrator/` is a working-tree subdirectory of main repo per current layout, it is skipped in G-5 with a `[PASS] G-5: aria-orchestrator skipped (in-tree, not submodule)` line).

**Logic per submodule**:
1. Read submodule pointer SHA: `git -C <main_repo> ls-tree HEAD <submodule_path>` → extract SHA.
2. Read submodule's default-branch HEAD on its primary remote: `git -C <submodule_path> ls-remote origin HEAD` → extract SHA (or use `git rev-parse master` if `--use-local-master` flag is set, fallback for offline).
3. Pointer matches remote default-branch HEAD → PASS; mismatch → ABORT.

**Detached HEAD detection**: if `git -C <submodule_path> symbolic-ref HEAD` returns non-zero (detached state), emit `[ABORT] G-5: <submodule> in detached HEAD state; checkout master before release`.

**Why ABORT (not RED)**: per `[[feedback_submodule_branch_before_archive]]` + `[[feedback_submodule_regression_pitfall]]`, submodule pointer drift at release time has been observed as silent regression source (2026-05-23 PR #123 incident, origin of Aria #124 Spec). Pre-release is the wrong place to ship a drift warning — it must hard-block.

#### E. Gate G-6: Forgejo Discussion URL liveness (~0.5h, threaded into A2.7)

**Source**: per Spec #3 §A.5 line 160 — "Spec #4 (`aria-2.0-m6-release-closeout`) will verify the actual Forgejo Discussion URL. This Spec verifies the FAQ text exists in the release notes file (Spec #4 verifies URL liveness)."

**Logic**:
1. Parse `docs/release-notes-v2.0.0.md` (created by Spec #3 §A.3). Locate "Forgejo Discussion FAQ" section. Extract first URL matching `https://forgejo\.10cg\.pub/...` regex.
2. If URL not found (Spec #3 §A.3 didn't include one yet): emit `[RED] G-6: Forgejo Discussion URL not yet posted in release notes; owner action`. No ABORT — Spec #3 §A.3 only mandates the FAQ TEXT (`grep -q "Forgejo Discussion FAQ"`), not the URL itself, which is owner-action post-Spec #3 ship.
3. If URL found: probe via `forgejo` CLI wrapper. **No PAT / no token in test fixtures** per `[[feedback_secrets_never_in_conversation]]`. Use:
   ```bash
   forgejo GET "<path-extracted-from-URL>" --silent --fail
   ```
   (`forgejo` wrapper handles auth from `/home/dev/.npm-global/bin/forgejo` env injection; Spec #4 never reads PAT). Exit 0 → PASS; non-zero → RED with stderr captured.

**Why RED (not ABORT)**: Discussion URL is a deliverable-promise check, not a release-blocker. Release can ship without the URL live (e.g., owner posts it 1h after release tag). Hard-blocking would create a chicken-and-egg deadlock with the FAQ post timing.

#### F. Gate G-7: 5-files SemVer synchronization (~0.5h, threaded into A2.8)

**Source of Truth**: `aria/.claude-plugin/plugin.json` `version` field per CLAUDE.md "版本发布检查清单" §真理来源.

**Derived files** (must all match SoT string):

| # | File | Field/Pattern | Read method |
|---|------|---------------|-------------|
| 1 | `aria/.claude-plugin/plugin.json` | `version` JSON key | `json.load(open(...))['version']` (SoT) |
| 2 | `aria/.claude-plugin/marketplace.json` | top-level `version` + `plugins[0].version` | `json.load(...)['version']` AND `[...]['plugins'][0]['version']` |
| 3 | `aria/VERSION` | top-level `version` field (single-line YAML at file end: `version: X.Y.Z` per current aria/VERSION format observed) | `re.search(r'^version:\s*(\S+)', ...)` last match |
| 4 | `aria/CHANGELOG.md` | top entry `## [X.Y.Z]` | first regex match `^## \[(\d+\.\d+\.\d+)\]` |
| 5 | `aria/README.md` | `**Version**: X.Y.Z` | first regex match `^\*\*Version\*\*:\s*(\S+)` |

**Plus main project**: `/home/dev/Aria/VERSION` declares `aria (子模块) ` plugin version row. Parse via regex `aria \(子模块\)\s*\|\s*v?(\S+)` first match.

**At M6 ship**: SoT version is expected to be `v2.0.0` (aria-plugin bumps to v2.0.0 alongside Aria 2.0 main repo — but see Spec #3 §A.3 Plugin Compatibility caveat: actually aria-plugin stays on v1.27.x stream per docs; Spec #4 G-7 verifies INTERNAL consistency across the 5+1 files, NOT a hardcoded expected version. PASS condition is "all 6 strings equal", not "all equal to a fixed value").

**Why ABORT**: Plugin Compatibility / market consumer correctness depends on these files being consistent. Manual bump error → ABORT until fixed.

#### G. Gate G-8: archive trigger eligibility (~0.5h, threaded into A2.9)

**Purpose**: Prevent out-of-order archive runs (e.g., if owner manually archives Spec #1 before Spec #4 runs, Spec #4 Phase D archive step would find #1 already in `openspec/archive/` and break the 4-directory atomic move semantics).

**Logic**:
```python
import pathlib
CHANGES = pathlib.Path('openspec/changes')
ARCHIVE = pathlib.Path('openspec/archive')
REQUIRED_SIBLINGS = [
    'aria-2.0-m6-cost-acceptance',
    'aria-2.0-m6-e2e-resilience',
    'aria-2.0-m6-docs',
]
for sibling in REQUIRED_SIBLINGS:
    if not (CHANGES / sibling).is_dir():
        # ABORT: sibling missing from changes/ → either never existed, or pre-archived
        # Probe archive/ for pre-archive evidence
        prearchived = list(ARCHIVE.glob(f'*-{sibling}'))
        if prearchived:
            print(f'[ABORT] G-8: {sibling} already archived ({prearchived[0]}); Spec #4 out-of-order')
        else:
            print(f'[ABORT] G-8: {sibling} missing from openspec/changes/ and openspec/archive/')
```

**PASS condition**: All 3 sibling directories present in `openspec/changes/` AND no pre-archive evidence in `openspec/archive/`. Spec #4 itself (`aria-2.0-m6-release-closeout`) is expected to be in `changes/` (running its own Phase B), which is checked separately (orchestrator script's own location).

#### H. Phase D archive runner (~1.5h, separate sub-script)

**Target file**: `/home/dev/Aria/aria-orchestrator/acceptance/m6-archive-runner.py` (NEW)

**Sequence** (atomic — either all 4 move OR none move):
1. Precondition: invoke `check-m6-release-readiness.py` → must exit 0 (ALL_PASS). If exit 1 (RED) with owner-override env var set, accept; if exit 2 (ABORT), refuse and exit 2.
2. Compute archive date: `today = datetime.now(timezone.utc).strftime('%Y-%m-%d')`.
3. Plan moves: each of `aria-2.0-m6-{cost-acceptance,e2e-resilience,docs,release-closeout}` from `openspec/changes/X/` to `openspec/archive/{today}-X/`.
4. **Dry-run mode** (`--dry-run`): print planned 4 moves with absolute paths, exit 0 without filesystem mutation. Per `[[feedback_schema_migration_3_safeguard_pattern]]` adapted (3-safeguard pattern for prod schema migrations) — dry-run is the equivalent safeguard for archive moves.
5. **Atomic execute** (`--execute`): use Python `pathlib.Path.rename()` per directory. If any rename fails mid-sequence, attempt rollback (rename completed-moves back to `changes/`). Log per-move success/failure to summary report.
6. Post-move: append archive record to summary report; update US-026 status from `in_progress` → `done` via `aria/skills/progress-updater` invocation (or document as owner-action if invocation is OOS — per OOS-5).

**Atomicity guarantee** (AD-M6-11): on filesystem failure mid-sequence, rollback restores the pre-execute state for completed moves. The script CANNOT guarantee true POSIX atomicity across 4 separate `rename()` syscalls (kernel-level), but it guarantees "best-effort transactional rollback" which is the closest stdlib-only approximation. Documented as known limitation in AD-M6-11.

#### I. Cross-references in sibling Spec "Successor" sections (~0.5h, T-A5.2)

Sibling Specs already have a "Successor" frontmatter pointing at Spec #4 (per Spec #3 line 22, Spec #1 line 682, Spec #2 frontmatter). Spec #4 Phase B adds NO modifications to sibling Spec proposals (they're Approved + sealed). Cross-reference enrichment instead happens in CLAUDE.md "版本发布检查清单" section (T-A5.3) — adds a link to `check-m6-release-readiness.py` as the canonical pre-release gate orchestrator.

### Out of scope (explicit drops per DEC Q-final-1 Menu C + Phase A.1 boundary)

| ID | Description | Drop reason |
|----|-------------|-------------|
| OOS-1 | Actual git tag creation / `aria-plugin v2.0.0` ship / 主项目 `v2.0.0` ship | Owner manual action post-Spec #4 PASS. Spec #4 only emits the verdict; the act of tagging + pushing is OOS. |
| OOS-2 | Layer 1 / Layer 2 cost gate trip alerting | Owned by Spec #1 §D (Feishu webhook + 80% threshold). Spec #4 only invokes Spec #1 acceptance script and reads exit code; does NOT re-implement alarm logic. |
| OOS-3 | Secret rotation execution | Owner action per `[[project_secret_rotation_deferred_2026-05-02]]`. Spec #4 G-4 only emits buffer warning / hard-block; does NOT rotate any credential. |
| OOS-4 | Forgejo Discussion content authoring (FAQ posting) | Owned by Spec #3 §A.5 (text drafting) + owner action (actual posting). Spec #4 G-6 only verifies URL liveness if URL present. |
| OOS-5 | US-026 status mutation via `aria:progress-updater` skill invocation | If skill invocation from inside Python script is non-trivial (skill is markdown-based, normally invoked from Claude Code session), this becomes an owner-manual step. Spec #4 archive runner prints the recommended UPM diff but does NOT execute it. To be locked at Phase A.2 (Q-A2-1 candidate). |
| OOS-6 | TG-DOCS-B (Spec #3 architecture deliverables, v2.0.1-deferrable) | Per Q-final-1 Menu C: TG-DOCS-B may ship as v2.0.1. Spec #4 G-3 gates ONLY on TG-DOCS-A deliverables (CLAUDE.md v2.0 + 3 state-checks probes). TG-DOCS-B completeness is not a Spec #4 concern. |
| OOS-7 | Forgejo Issue closure (e.g., M6 tracking issue if open) | Owner manual action. Spec #4 emits recommendation in summary report; does NOT call Forgejo API. |
| OOS-8 | Cross-project ripple checks (SilkNode / Kairos consumer impact verification) | Single-project (Aria) ship gate only. Cross-project impact is M7+ concern. |
| OOS-9 | Forgejo Discussion URL re-write if 404 | G-6 emits RED; Spec #4 does NOT rewrite the release notes URL. Owner fixes manually + re-runs. |
| OOS-10 | Submodule pointer auto-correction on G-5 drift | G-5 emits ABORT; Spec #4 does NOT `git submodule update --remote` automatically. Owner fixes via Aria #124 regression-gate runbook + re-runs. |

---

## Constraints

### Spec #4 runs AFTER Specs #1+#2+#3 Phase B complete (sequential, not parallel)

Per DEC Q-final-1 Menu C + Spec #4 frontmatter "Predecessor Specs" list. Spec #4 Phase A.2 audit can run in parallel with sibling Phase B (paper review), but Spec #4 Phase B impl MUST sequence after all 3 siblings' Phase B ships, because G-1..G-3 directly invoke sibling-delivered binaries.

**Phase B kick verify probe** (per `[[feedback_per_spec_assumption_recheck]]` + `[[feedback_probe_first_scope_reframe]]`):

Before Phase B.2.1 (T-A2.2 implementation), owner must verify the 5 assumptions listed in §Assumptions below.

### Python 3.9+ stdlib only

No third-party Python deps (no requests, no PyYAML — use built-in `yaml` if available OR fall back to JSON parse for state-checks.yaml... actually yaml is NOT stdlib; therefore G-3 YAML parse must shell out to `python3 -c "import yaml; ..."` which assumes PyYAML on the host. If PyYAML is not on the host, G-3 falls back to grep-based name presence check (Spec #3 §AC-4 evidence first part). Decision recorded as note in AD-M6-10.).

**Resolution** (Phase A.1 lock): Spec #4 G-3 uses **grep-based name presence check** as the primary (per-probe `grep -qF "name: \"${probe}\""` from Spec #3 §AC-4 evidence first half). The PyYAML structural check is an OPTIONAL second pass only if PyYAML is available on the host (`importlib.util.find_spec('yaml')` non-None). This keeps Spec #4 stdlib-only.

### Backward-compatible per Aria principle "向后兼容"

Spec #4 introduces no breaking changes. It is purely additive: new script files in `aria-orchestrator/acceptance/`, new artifact directory `.aria/m6-release-readiness/`, new entry in CLAUDE.md "版本发布检查清单" pointing at the orchestrator.

### Sibling Spec scripts assumed byte-exact at Phase B kick

Phase B verification (per §Assumptions A-1..A-3 below) confirms script paths and CLI flag contracts. If sibling renames a script during Phase B, the verify probe catches it and Phase B kick is held.

### Linux-only

Spec #1 + #2 + #3 all target Linux (Nomad alloc / `aria-orchestrator/` runtime). Spec #4 follows the same constraint. macOS/Windows compat is not required.

---

## Assumptions

Per `[[feedback_per_spec_assumption_recheck]]`: Phase B kick (T-A2.1 start) requires owner to verify these 5 assumptions hold. If any fails, raise to owner before continuing.

| # | Assumption | Verifiable when | Verification command |
|---|------------|-----------------|---------------------|
| A-1 | Spec #1 `validate-m6-handoff.py` exists at `aria-orchestrator/docs/validate-m6-handoff.py` AND accepts `--all` flag | Spec #1 Phase B end | `python3 aria-orchestrator/docs/validate-m6-handoff.py --all --help` exits 0 OR exits 2 with stdout containing `--all` (subargparse hint) |
| A-2 | Spec #2 `check-m6-e2e-acceptance.py` exists at `aria-orchestrator/acceptance/check-m6-e2e-acceptance.py` AND accepts `--all` flag aggregating `--tg-a/b/c` | Spec #2 Phase B end | `python3 aria-orchestrator/acceptance/check-m6-e2e-acceptance.py --all --help` exits 0 OR stdout shows `--all` |
| A-3 | Spec #3 ships CLAUDE.md v2.0 with version field `**版本**: 2.0.0` AND state-checks.yaml contains 3 probe names | Spec #3 Phase C.2 merge | `grep -q '\*\*版本\*\*: 2.0.0' CLAUDE.md && grep -qF 'm6-version-badge-match' .aria/state-checks.yaml && grep -qF 'm6-claude-md-version' .aria/state-checks.yaml && grep -qF 'm6-arch-doc-stale' .aria/state-checks.yaml` exits 0 |
| A-4 | `aria/.claude-plugin/plugin.json` `version` field is readable as canonical SoT | Always (currently `v1.27.0` per `c7e611f` submodule bump) | `python3 -c "import json; print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])"` prints a SemVer |
| A-5 | `/home/dev/.npm-global/bin/forgejo` CLI wrapper exists AND can be invoked without PAT in env (auth is wrapper-managed) | Phase B kick | `forgejo --help` exits 0 (basic command availability check; full auth check is owner-side) |

**Falsifiability gates per assumption**: A-1 falsifies if `--all` flag is absent → fallback strategy (G-1 invokes 4 individual flags + ANDs). A-2 similar fallback. A-3 falsifies if grep returns non-zero → block Phase B start. A-4 falsifies if plugin.json is corrupt → G-7 ABORT. A-5 falsifies if forgejo wrapper missing → G-6 RED with `forgejo CLI unavailable, manual URL check required`.

---

## How

### Technical approach

```
                          owner runs:
                  python3 aria-orchestrator/acceptance/check-m6-release-readiness.py
                                          │
                                          ▼
                  ┌───────────────────────────────────────────┐
                  │      G-1..G-8 sequential execution        │
                  │                                           │
                  │  G-1: subprocess validate-m6-handoff.py   │  ← Spec #1
                  │  G-2: subprocess check-m6-e2e-...py       │  ← Spec #2
                  │  G-3: grep CLAUDE.md + state-checks.yaml  │  ← Spec #3
                  │  G-4: date arith vs 2026-08-02 cap        │  ← project_secret_rotation_deferred
                  │  G-5: git ls-tree HEAD vs git ls-remote   │  ← .gitmodules enum
                  │  G-6: forgejo GET <url-from-release-notes>│  ← Spec #3 §A.5 deferred
                  │  G-7: 5-files SemVer string match         │  ← CLAUDE.md release checklist
                  │  G-8: ls openspec/{changes,archive}/      │  ← archive ordering
                  └───────────────┬───────────────────────────┘
                                  │ per-gate exit code aggregation
                                  ▼
                  ┌───────────────────────────────────────────┐
                  │  Verdict: ALL_PASS / RED / ABORT          │
                  │  + summary report                         │
                  │  → .aria/m6-release-readiness/{ts}.md    │
                  └───────────────┬───────────────────────────┘
                                  │
                                  ▼
                  ┌───────────────────────────────────────────┐
                  │  Optional: m6-archive-runner.py --execute │
                  │   - precondition: readiness exit 0        │
                  │   - 4 atomic moves to openspec/archive/   │
                  │   - rollback on partial failure           │
                  │   - emit US-026 done recommendation       │
                  └───────────────────────────────────────────┘
```

### Key design decisions (AD-M6-10..AD-M6-12)

| ID | Topic | Decision |
|----|-------|----------|
| AD-M6-10 | Orchestrator exit code aggregation contract | Three-state verdict (ALL_PASS 0 / RED 1 / ABORT 2). RED honors `--owner-override "<rationale>"` with non-empty rationale + audit-log entry. ABORT rejects override (hard block). Per-gate stdout `[PASS\|RED\|ABORT] G-N: <msg>` format. Summary report idempotent (timestamped filename, accumulates trail). |
| AD-M6-11 | Atomic 4-directory archive transactional pattern | Use `pathlib.Path.rename()` per move. Track completed moves in an in-memory list; on any failure, attempt rollback by reverse-renaming completed moves back to `openspec/changes/`. Known limitation (documented): not POSIX-atomic across 4 syscalls; best-effort transactional. Dry-run mode (`--dry-run`) prints planned moves without filesystem mutation. |
| AD-M6-12 | Secret rotation buffer threshold calibration | Thresholds locked at 21d RED / 14d ABORT based on owner-acknowledged rotation time-to-execute (~7-14d real-world delay between "decide to rotate" → "all 9 credentials rotated and tested" per 2026-05-20 rotation R3 evidence). 14d ABORT leaves owner exactly half the worst-case rotation lead-time. 21d RED is one full rotation cycle of advance warning. Re-calibration would require new Spec + DEC. |

---

## Acceptance criteria

All criteria are binary-falsifiable per `[[feedback_falsifiable_evidence_for_binary_acceptance]]`. No subjective language. Each criterion cites concrete verifiable evidence.

### AC-1 — orchestrator script exists + binary exit code 0/1/2

**Evidence**:
```bash
[ -f aria-orchestrator/acceptance/check-m6-release-readiness.py ] || exit 1
python3 aria-orchestrator/acceptance/check-m6-release-readiness.py --help
# must exit 0; stdout must contain "ALL_PASS", "RED", "ABORT", "--owner-override", "--dry-run" (help text mentions all CLI surface)
```

Three-state verdict contract: exit 0 = ALL_PASS, exit 1 = RED, exit 2 = ABORT. No other exit codes. Verified by AC-2 / AC-9 boundary scenarios.

### AC-2 — G-1..G-3 sibling consumption gates wired correctly

**Evidence** (3 scenarios per gate, 9 fixtures total):
- `test_G1_PASS`: fixture where `validate-m6-handoff.py` returns exit 0 → orchestrator reports `[PASS] G-1`.
- `test_G1_FAIL_RED`: fixture where `validate-m6-handoff.py` returns exit 1 → orchestrator reports `[RED] G-1`.
- `test_G1_FAIL_ABORT`: fixture where `validate-m6-handoff.py` returns exit 2 → orchestrator reports `[ABORT] G-1`.
- Same triple for G-2 (mock `check-m6-e2e-acceptance.py`).
- Same triple for G-3 (mock state-checks.yaml + CLAUDE.md combos).

Mocking strategy per `[[feedback_test_mock_pattern_hides_prod_bug]]`: mock the subprocess call at the transport layer (`subprocess.run` return value), NOT the gate evaluation logic itself. Mock layer = SDK-equivalent (Python subprocess boundary).

### AC-3 — G-4 secret rotation buffer: 3 boundary tests

**Evidence**:
```bash
# Test 1: 21d+ buffer (PASS)
M6_RELEASE_TODAY_OVERRIDE=2026-07-10 python3 ... check-m6-release-readiness.py --only-gate G-4
# stdout contains "[PASS] G-4", exit 0 (if only G-4 run; orchestrator overall verdict depends on other gates if --only-gate not supported, alternative: --gates G-4 selector)

# Test 2: 14-20d buffer (RED)
M6_RELEASE_TODAY_OVERRIDE=2026-07-22 python3 ... check-m6-release-readiness.py --only-gate G-4
# stdout contains "[RED] G-4", exit 1

# Test 3: <14d buffer (ABORT)
M6_RELEASE_TODAY_OVERRIDE=2026-07-28 python3 ... check-m6-release-readiness.py --only-gate G-4
# stdout contains "[ABORT] G-4", exit 2
```

Boundary semantics: PASS condition is `buffer_days >= 21`; RED condition is `14 <= buffer_days < 21`; ABORT condition is `buffer_days < 14`. Verified at exact boundaries (21d / 20d / 14d / 13d).

### AC-4 — G-5 submodule pointer probe: 3 scenarios

**Evidence**:
- `test_G5_PASS_aligned`: fixture git repo with submodule pointer == remote default-branch HEAD → orchestrator reports `[PASS] G-5`.
- `test_G5_ABORT_misaligned`: fixture with stale submodule pointer (one commit behind remote) → orchestrator reports `[ABORT] G-5: <submodule> pointer <stale-sha> != remote master <fresh-sha>`.
- `test_G5_ABORT_detached`: fixture with submodule in detached HEAD state → orchestrator reports `[ABORT] G-5: <submodule> in detached HEAD state`.

Test fixtures use `tempfile.TemporaryDirectory()` + `subprocess.run(['git', 'init', ...])` to construct synthetic repo states. No live remote dependency.

### AC-5 — G-6 Forgejo Discussion URL liveness: 2 scenarios

**Evidence**:
- `test_G6_PASS_url_200`: release-notes-v2.0.0.md contains `https://forgejo.10cg.pub/10CG/Aria/issues/...`; mock `forgejo` wrapper returns exit 0 → orchestrator reports `[PASS] G-6`.
- `test_G6_RED_url_404`: same URL; mock `forgejo` wrapper returns non-zero → orchestrator reports `[RED] G-6: Forgejo URL <url> returned non-zero exit (likely 404 / offline / auth fail); manual verify`.
- `test_G6_RED_no_url`: release-notes-v2.0.0.md missing FAQ URL → orchestrator reports `[RED] G-6: Forgejo Discussion URL not yet posted in release notes; owner action`.

**Secret hygiene** per `[[feedback_secrets_never_in_conversation]]`: test fixtures contain NO Forgejo PAT strings, NO token literals. Mock layer mocks the `forgejo` wrapper's subprocess invocation, not auth internals.

### AC-6 — G-7 5-files sync probe: 2 scenarios

**Evidence**:
- `test_G7_PASS_all_match`: fixture where plugin.json + marketplace.json (top + plugins[0]) + VERSION + CHANGELOG.md (top entry) + README.md + 主项目 VERSION all show `2.0.0` → orchestrator reports `[PASS] G-7`.
- `test_G7_ABORT_one_stale`: fixture where plugin.json = `2.0.0` but CHANGELOG.md top entry = `1.27.0` → orchestrator reports `[ABORT] G-7: drift detected (CHANGELOG.md=1.27.0 != SoT=2.0.0)` with explicit per-file diff.

The SoT is `plugin.json`; all other files are compared against it (NOT against a hardcoded expected version).

### AC-7 — G-8 archive trigger ordering: 2 scenarios

**Evidence**:
- `test_G8_PASS_all_active`: fixture where `openspec/changes/` contains all 3 sibling directories AND `openspec/archive/` contains no `*-aria-2.0-m6-*` directories → orchestrator reports `[PASS] G-8`.
- `test_G8_ABORT_prearchived`: fixture where `openspec/changes/aria-2.0-m6-cost-acceptance/` is absent BUT `openspec/archive/2026-05-30-aria-2.0-m6-cost-acceptance/` exists → orchestrator reports `[ABORT] G-8: aria-2.0-m6-cost-acceptance already archived; Spec #4 out-of-order`.

### AC-8 — Summary report writes correctly + idempotent on repeat run

**Evidence**:
```bash
rm -rf .aria/m6-release-readiness/
python3 aria-orchestrator/acceptance/check-m6-release-readiness.py
ls .aria/m6-release-readiness/ | wc -l  # must return 1

# Idempotency: repeat run → new file, original preserved
sleep 1  # ensure timestamp differs
python3 aria-orchestrator/acceptance/check-m6-release-readiness.py
ls .aria/m6-release-readiness/ | wc -l  # must return 2 (both files present)
```

Filename format: `{YYYY-MM-DDTHHMMSSZ}-report.md` (e.g., `2026-05-25T143012Z-report.md`). UTC timestamp via `datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')` (no colons → filename-safe across all filesystems).

### AC-9 — Owner override env var honored for RED but rejected for ABORT

**Evidence**:
```bash
# Setup: fixture where one gate emits RED, no gate emits ABORT
python3 ... check-m6-release-readiness.py --owner-override "ack: known issue, manual verify done"
# exit 0 (override accepted on RED; "VERDICT" line reads "[VERDICT] RED → SHIP (owner-override)")

# Setup: fixture where one gate emits ABORT
python3 ... check-m6-release-readiness.py --owner-override "ack: rotate later"
# exit 2 (override rejected on ABORT)
# stderr contains "[ERROR] --owner-override rejected: ABORT verdict has no override path"
```

Edge cases:
- Empty rationale (`--owner-override ""`) → exit 2 with `[ERROR] --owner-override rationale must be non-empty`.
- Missing rationale (`--owner-override` no arg) → argparse rejects with non-zero exit.
- RED + override → summary report includes verbatim rationale + timestamp.

### AC-10 — Phase D archive runner: 4 directories moved atomically OR none moved

**Evidence**:
- `test_archive_PASS`: fixture with all 4 sibling+self Spec dirs in `openspec/changes/`; readiness exits 0 → archive runner with `--execute` moves all 4 to `openspec/archive/{today}-*` AND `openspec/changes/aria-2.0-m6-*` is now empty.
- `test_archive_ABORT_no_partial`: simulate filesystem failure on the 3rd of 4 renames (mock `pathlib.Path.rename` to raise on the 3rd call) → archive runner rolls back: first 2 moves reversed, last 2 never attempted, final state matches pre-execute state.
- `test_archive_dry_run`: `--dry-run` flag → stdout prints 4 planned moves; filesystem unchanged.
- Precondition test: `test_archive_REFUSES_on_ABORT_verdict`: readiness exits 2 → archive runner refuses with `[ERROR] readiness verdict ABORT; archive refused` and exits 2.

Per `[[feedback_schema_migration_3_safeguard_pattern]]` adapted: dry-run is the migration-equivalent safeguard for archive moves; rollback is the integrity-check equivalent.

---

## Risks

| ID | Risk | Severity | Mitigation |
|----|------|----------|------------|
| R-M6CL-1 | Secret rotation buffer drift — if M6 ship slips past plan, G-4 fires `<14d ABORT` before owner can rotate the 9-key carry-forward (per `[[project_secret_rotation_deferred_2026-05-02]]`) | Medium | Owner pre-emptively rotates secrets if calendar projection shows ship date < 2026-07-12 (21d before cap). G-4 RED window at 14-20d gives 2-week advance warning. Hard cap 2026-08-02 is owner-set; re-calibration requires new Spec. |
| R-M6CL-2 | Sibling script path drift — Spec #1 / #2 / #3 rename scripts during Phase B implementation, breaking G-1 / G-2 / G-3 subprocess invocations | Medium | Phase B kick verify probe (T-A2.0) tests all 3 script paths + CLI flag contracts BEFORE T-A2.2 implementation. Failed verify → owner escalation. Per `[[feedback_per_spec_assumption_recheck]]` + `[[feedback_scaffold_helpers_drift_without_callers]]`. |
| R-M6CL-3 | Forgejo Discussion URL race — Spec #3 §A.5 only mandates FAQ TEXT in release notes; actual URL is owner-action post-Spec #3 ship. If Spec #4 runs before Spec #3 §A.5 owner-action complete, G-6 emits RED (which is correct, but may confuse "is M6 ready?" reading) | Low | G-6 emits RED (not ABORT) precisely because URL absence is expected mid-window. G-8 archive trigger eligibility ensures Spec #4 runs AFTER sibling Phase B; FAQ posting is OOS-4 explicit. RED→ship path with `--owner-override "FAQ URL pending owner post"` is the documented release path. |
| R-M6CL-4 | 5-files SemVer string drift — manual bump error in any of 6 surfaces (plugin.json + 4 derived + 主项目 VERSION) → G-7 ABORT | Medium | Pre-bump owner uses CLAUDE.md release checklist as authoritative procedure. G-7 ABORT is the correct response (catch drift pre-ship). Mitigation is documentation, not script — Spec #4 is the catcher, not the preventer. |
| R-M6CL-5 | Atomic archive on filesystem failure — mid-rename crash leaves N archived + 4-N active, post-rollback (if rollback also fails) leaves inconsistent state | Medium | Dry-run mode (T-A4.3) lets owner inspect planned moves before execute. Rollback in `--execute` is best-effort transactional. AD-M6-11 documents known limitation (not POSIX-atomic across 4 syscalls). T-A4.4 pytest covers mock fs-failure mid-move. |
| R-M6CL-6 | PyYAML not on host → G-3 YAML structural check unavailable | Low | Per §Constraints + AD-M6-10 fallback: G-3 primary path is grep-based name presence (stdlib-only); YAML structural is OPTIONAL second pass gated by `importlib.util.find_spec('yaml')`. No hard dependency on PyYAML. |
| R-M6CL-7 | Spec #4 self-archives mid-orchestration — Spec #4 invokes itself archive while still running | Low | Archive runner is a SEPARATE script from orchestrator. Owner explicitly invokes archive runner after readiness PASS. Spec #4 orchestrator never invokes its own archive. Reduces footgun risk. |
| R-M6CL-8 | `forgejo` CLI wrapper not on PATH at Phase B / production run time → G-6 always RED | Low | A-5 verify probe at Phase B kick. If wrapper missing, document workaround in summary report: "manual URL check required, paste curl status here". Wrapper path `/home/dev/.npm-global/bin/forgejo` is the canonical install location per CLAUDE.md "Forgejo API (PR Operations)" section. |

---

## Effort baseline

```
A.1 Scaffolding (mkdir + .gitkeep + .gitignore)                   ~0.5h
A.2 Orchestrator script (G-1..G-8 + aggregator + override)        ~3h
A.3 Pytest suite (10 ACs × boundary scenarios)                    ~3h
A.4 Phase D archive runner (atomic 4-dir + dry-run + rollback)    ~1.5h
A.5 Docs (artifact dir README + CLAUDE.md checklist link)         ~1h
A.6 Memory candidate entry (deferred to Phase D, not now)         ~0.5h
─────────────────────────────────────────────────────────────────────
Subtotal AI-implementable                                          ~9.5h
+ Buffer (unforeseen integration friction)                         ~0.5h
─────────────────────────────────────────────────────────────────────
Total                                                              ~10h
```

Single SoT per `[[feedback_spec_v2_body_propagation_2pass]]`: ~10h cited identically in frontmatter line 22 + this section + tasks.md line 7.

Owner manual action (post-Phase B, not in B.2):
- Set Forgejo Discussion URL in release-notes-v2.0.0.md after FAQ post (closes G-6 RED → PASS path).
- Decide ship vs hold on RED verdict (use `--owner-override` if shipping).
- Execute archive runner with `--execute` once orchestrator returns exit 0 (or RED + override).
- Tag aria-plugin / 主项目 / standards as applicable (OOS-1, owner-only).

---

## Dependencies

| Dependency | Direction | Notes |
|------------|-----------|-------|
| Spec #1 `aria-2.0-m6-cost-acceptance` Phase B complete | Upstream (hard) | G-1 invokes `validate-m6-handoff.py --all`. Phase B kick verify (A-1). |
| Spec #2 `aria-2.0-m6-e2e-resilience` Phase B complete | Upstream (hard) | G-2 invokes `check-m6-e2e-acceptance.py --all`. Phase B kick verify (A-2). |
| Spec #3 `aria-2.0-m6-docs` Phase C.2 complete (TG-DOCS-A only) | Upstream (hard) | G-3 reads CLAUDE.md v2.0 + state-checks.yaml. Phase B kick verify (A-3). |
| `aria/.claude-plugin/plugin.json` `version` field | Upstream (read-only SoT) | G-7 derives expected SemVer from this. |
| `forgejo` CLI wrapper at `/home/dev/.npm-global/bin/forgejo` | Infrastructure (host-managed) | G-6 invokes wrapper subprocess. A-5 verify. Falls back to RED on absence. |
| `.gitmodules` enumeration | Infrastructure | G-5 reads to discover submodules in scope (`aria/`, `standards/`, possibly `aria-orchestrator/`). |
| `aria-orchestrator/acceptance/` directory existence | Upstream (Spec #1 creates) | Spec #4 script lives here as sibling to Spec #1/#2 acceptance scripts. |
| `[[project_secret_rotation_deferred_2026-05-02]]` (memory entry, 2026-05-20 updated) | Upstream (source of hard cap 2026-08-02) | G-4 hardcodes `HARD_CAP = date(2026, 8, 2)` from this. Re-cap = new Spec. |

---

## Cross-references

**Predecessors (Spec #4 gates on all three)**:
- [aria-2.0-m6-cost-acceptance/proposal.md](../aria-2.0-m6-cost-acceptance/proposal.md) — Spec #1, Approved `c29a800`. G-1 invokes Spec #1 §F `validate-m6-handoff.py`. Spec #1 §AC-6/7/9 are the sub-checks G-1 aggregates.
- [aria-2.0-m6-e2e-resilience/proposal.md](../aria-2.0-m6-e2e-resilience/proposal.md) — Spec #2, Approved. G-2 invokes Spec #2 §What scripts. Spec #2 §AC-1/3/5 cover 7d uptime + 6 crash modes + humanized median ≥7 (PRD §639 D1-D7 rubric).
- [aria-2.0-m6-docs/proposal.md](../aria-2.0-m6-docs/proposal.md) — Spec #3, Approved. G-3 reads §A.1 (CLAUDE.md v2.0) + §A.6 (3 state-checks probes). Spec #3 §A.5 line 160 explicitly hands off Forgejo URL liveness to Spec #4 (G-6).

**Complementary but disjoint scope** (NOT a Spec #4 dependency):
- [aria-submodule-pointer-regression-gate/proposal.md](../aria-submodule-pointer-regression-gate/proposal.md) — Aria #124 Spec, parallel track in aria-plugin v1.28.0→v1.29.0. Targets `phase-c-integrator` Skill C.2.4.5 sub-step (PR-time gate). Spec #4 G-5 targets release-time submodule pointer probe (different surface). Both conceptually concerned with submodule drift; G-5 reuses the same `[[feedback_submodule_branch_before_archive]]` + `[[feedback_submodule_regression_pitfall]]` lessons but no code/Skill dependency between them.

**Decisions**:
- [.aria/decisions/2026-05-24-us026-m6b-brainstorm.md](../../../.aria/decisions/2026-05-24-us026-m6b-brainstorm.md) — DEC-20260524-001 Q-final-1 Menu C lock (Spec #4 as RED/ABORT pre-release gates, last in M6 sequence).

**PRD references**:
- [docs/requirements/prd-aria-v2.md §M6](../../../docs/requirements/prd-aria-v2.md) lines 637-660 — M6 量化/定性指标 (定量: 7d uptime / 6 crash modes / cost gates; 定性: humanized median ≥7).
- PRD lines 430-441 — M6 reframe lock (post `a786444` + `e884e62` patches).

**Memory entries**:
- `[[feedback_falsifiable_evidence_for_binary_acceptance]]` — every AC cites concrete verifiable metric; AC-3/4/5/6/7/9 use boundary scenarios for falsifiability.
- `[[feedback_paper_fix_antipattern]]` — Spec #4 ships code + test + doc 三位一体 (orchestrator code + 10 AC pytest fixtures + CLAUDE.md checklist doc link); no doc-only "advisory".
- `[[feedback_per_spec_assumption_recheck]]` — §Assumptions A-1..A-5 are explicitly verified at Phase B kick (T-A2.0 probe).
- `[[feedback_probe_first_scope_reframe]]` — Phase B precondition probe is mandatory; without it, G-1..G-3 subprocess calls would silently break on sibling script rename.
- `[[feedback_schema_migration_slot_draft_time_verify]]` — sibling script paths byte-exact verified at draft time (Phase A.1) against Spec #1/#2/#3 proposal text grep.
- `[[feedback_secrets_never_in_conversation]]` — G-6 uses `forgejo` wrapper subprocess; test fixtures contain NO PAT / NO token literals.
- `[[feedback_test_mock_pattern_hides_prod_bug]]` — AC-2 mock strategy: mock subprocess transport boundary, NOT gate evaluation logic.
- `[[feedback_submodule_branch_before_archive]]` — G-5 + G-8 enforce this lesson at release time.
- `[[feedback_submodule_regression_pitfall]]` — G-5 origin (2026-05-23 PR #123 incident lessons applied at release-time surface).
- `[[feedback_schema_migration_3_safeguard_pattern]]` — adapted for archive runner: dry-run + execute + rollback (3 safeguards) parallel to backup + dry-run + apply + integrity-check.
- `[[feedback_plugin_version_drift_multiple_sources]]` — G-7 is the direct catcher for this drift pattern.
- `[[feedback_audit_driven_fix_conventions]]` — summary report timestamps accumulate audit trail.
- `[[feedback_scaffold_helpers_drift_without_callers]]` — sibling script verification at T-A2.0 catches rename drift before it reaches Phase B impl.
- `[[feedback_phase_budget_compounding]]` — ~10h impl baseline is conservative; Phase B trajectory expected ~9-10h (Level 2 single-script scope; no cross-cutting).
- `[[feedback_spec_v2_body_propagation_2pass]]` — effort SoT cited identically in frontmatter + §Effort baseline + tasks.md.
- `[[project_secret_rotation_deferred_2026-05-02]]` — G-4 hard cap 2026-08-02 source (2026-05-20 update: 9-key carry-forward, original 4 + new 5).
- `[[feedback_release_phase_d_5_files_synchronization]]` — G-7 5-files SoT pattern source (if this memory exists; otherwise this is a NEW candidate to write during Phase D per T-A6.1).
- `[[feedback_pre_release_orchestrator_gate_pattern]]` — NEW candidate memory entry, deferred to Phase D write per T-A6.1.

---

> **Phase A.1 Spec drafting complete 2026-05-25.** Ready for Phase A.2 audit (multi-agent post_spec convergence). Audit collapse may be considered if R2 4/4 SCOPE_OK + R1 critical 100% closed + ≥70% reduction per `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]`.
