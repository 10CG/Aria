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
> **Audit trajectory**: Phase A.2 R1 (3-agent parallel: backend-architect + qa-engineer + code-reviewer) NEEDS_FIX 3/3 (2026-05-25); R1-fix `cdd2e5e` applies 7 Critical + 12 Important findings + 3 owner Q-locks (Q1=T-A1.4 reconcile, Q2=phase-d-closer delegation, Q3=invert primary path); Phase A.2 R2 (3-agent challenge) SPLIT verdict 2 SCOPE_OK_R2 + 1 NEEDS_FIX_R2 — R1 5C closed 5/5 + 77-92% reduction; R2-fix `<R2-FIX-COMMIT-PENDING>` applies 4 new Important + 4 new Minor (I-NEW-r2-1 self-trap propagation / I-NEW-r2-2 AD-M6-10 exit code gap / I-ba-R2-1 G-4 message format / I-qa-R2-1 phase-d-closer exit 3 escalation); Phase A.2 R3 stability (1-agent scope-limited) pending per `[[feedback_3round_early_convergence]]`

---

## Why

M6 ships three independently-Approved Specs (#1 cost-acceptance / #2 e2e-resilience / #3 docs) plus a hard-coded set of release-hygiene checks that span all three plus 5 net-new dimensions that no single sibling Spec owns. Without an orchestrator that consumes all sibling acceptance outputs and adds the cross-cutting gates, the v2.0.0 ship decision is reduced to "owner manually runs ~8 scripts + 5 ad-hoc grep checks and hopes nothing was missed" — a textbook paper-fix antipattern per `[[feedback_paper_fix_antipattern]]`.

**Four release-hygiene problems Spec #4 closes**:

1. **No top-level PASS/RED/ABORT verdict**: Spec #1 emits its own exit codes (0/1/2), Spec #2 emits per-`--tg-{a,b,c}` exit codes, Spec #3 ships 3 state-checks probes — but there is no single command that says "ship or not". Owner needs `python3 aria-orchestrator/acceptance/check-m6-release-readiness.py` → exit 0/1/2 with structured per-gate report.

2. **Secret rotation hard cap 2026-08-02 has no automated buffer warning**: per `[[project_secret_rotation_deferred_2026-05-02]]`, the partial rotation deadline is hard-capped at 2026-08-02 (9-key carry-forward debt). If M6 ships within `<14d` of that cap, owner has no slack to rotate secrets post-release — a foreseeable cliff. Spec #4 G-4 surfaces this as `<21d → RED` (informational warn) / `<14d → ABORT` (hard block).

3. **6-surfaces SemVer drift would silently break Plugin Compatibility**: CLAUDE.md "版本发布检查清单" lists 5 plugin-stream files (plugin.json SoT + 4 derived) plus the main repo `/VERSION` plugin-row entry — **6 surfaces total** — that must all match. Per `[[feedback_plugin_version_drift_multiple_sources]]`, drift between these has been observed mid-session (v1.22.0 stale in CLAUDE.md while plugin.json = v1.27.0). Without an automated probe, manual bump errors silently propagate to market consumers. G-7 catches this pre-ship.

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
<!-- R1-fix C3/I-ba-1/C-qa-3/C-cr-4 (owner Q3 lock 2026-05-25): per-flag invocation is PRIMARY (siblings ship individual flags only; `--all` not contracted) -->
| G-1 cost-acceptance | Spec #1 AC-6 + AC-7 + AC-9 | `python3 aria-orchestrator/docs/validate-m6-handoff.py` invoked 4×: `--check-abi-compat`, `--check-3-day-history`, `--check-cost-method-enum`, `--check-pricing-freshness` (per-flag canonical; sibling does NOT ship `--all`) | all 4 exit 0 | any 1 (no 2) → RED ; any 2 → ABORT |
| G-2 e2e-resilience | Spec #2 AC-1 + AC-3 + AC-5 (7d uptime + 6 crash modes + humanized median ≥7) | `python3 aria-orchestrator/acceptance/check-m6-e2e-acceptance.py` invoked 3×: `--tg-a`, `--tg-b`, `--tg-c` (per-flag canonical; sibling does NOT ship `--all`) | all 3 exit 0 | any 1 (no 2) → RED ; any 2 → ABORT |
| G-3 docs | Spec #3 AC-1 + AC-4 (CLAUDE.md v2.0 + 3 state-checks probes registered) | (a) CLAUDE.md grep `**版本**: 2.0.0` + `两层 AI 分工` + `Aria 2.0 运行时` + (b) state-checks.yaml YAML parse → assert all 3 `m6-*` probe names present | both (a) and (b) pass | either grep failure → RED ; YAML parse error → ABORT |

<!-- R1-fix C3 (owner Q3 lock): G-1/G-2 primary = per-flag aggregation per `[[feedback_gate_logic_cross_spec_sot_validate]]` byte-exact rule (siblings Approved+sealed; do NOT amend) -->

**G-1 detail (per-flag canonical)**: Spec #1 `validate-m6-handoff.py` ships exactly 4 individual flags: `--check-abi-compat` (§AC-6 source) / `--check-3-day-history` (§AC-7) / `--check-cost-method-enum` (§AC-8) / `--check-pricing-freshness` (§AC-8). Spec #4 G-1 invokes ALL 4 as separate subprocesses + aggregates exit codes per `[PASS|RED|ABORT]` table above. The `--all` mega-flag is an OPTIONAL fast-path: if Spec #1 ships `--all` post-Phase B (additive amendment requires new Spec; NOT currently in sibling contract), G-1 may detect availability via `--help` grep and use it; otherwise per-flag canonical path is the only path. NO behavioral difference between canonical and `--all` aggregate.

**G-2 detail (per-flag canonical)**: Spec #2 `check-m6-e2e-acceptance.py` ships exactly 3 TG flags: `--tg-a` (AC-1 7d uptime) / `--tg-b` (AC-3 6 crash modes) / `--tg-c` (AC-5 humanized median). Spec #4 G-2 invokes ALL 3 as separate subprocesses + aggregates: `any returncode 2 → ABORT; any returncode 1 (no 2) → RED; all 0 → PASS`. The `--all` flag is OPTIONAL fast-path with same aggregation semantic.

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
elif buffer_days >= 0:
    # R2-fix I-ba-R2-1: cap-day (0d) AND positive-but-<14d ABORT share same template (with "< 14d" suffix for distinguishability)
    print(f"[ABORT] G-4: secret rotation buffer {buffer_days}d < 14d (cap {HARD_CAP.isoformat()}); rotate before release")
else:
    # R2-fix I-ba-R2-1: negative buffer (past cap) uses distinct "cap exceeded by Nd" template
    print(f"[ABORT] G-4: secret rotation buffer {buffer_days}d (cap {HARD_CAP.isoformat()}); cap exceeded by {-buffer_days} days")
```

**Note on cap-day-itself (buffer_days == 0)**: hits the `buffer_days >= 0` ABORT branch, emitting `[ABORT] G-4: secret rotation buffer 0d < 14d`. Test 5 (AC-3) asserts this message format (the `< 14d` suffix is informational; the binary verdict is correct).

**Boundary semantics** (binary-falsifiable):
- `buffer_days >= 21` → PASS (green)
- `14 <= buffer_days < 21` → RED (informational warn — owner may override)
- `buffer_days < 14` → ABORT (hard block — no override; owner must rotate or extend cap)

**Date injection for tests**: `M6_RELEASE_TODAY_OVERRIDE=YYYY-MM-DD` environment variable, parsed via `date.fromisoformat()`. Test fixtures use this for 3-boundary coverage per AC-3.

#### D. Gate G-5: submodule pointer pre-release probe (~0.5h, threaded into A2.6)

<!-- R1-fix C5 (C-cr-5): aria-orchestrator IS a submodule per .gitmodules (verified 2026-05-25); enumerate all 3 unconditionally; the in-tree special case was a draft-time misread (per `[[feedback_per_spec_assumption_recheck]]`) -->

**Submodules covered** (per `.gitmodules` enumeration at Phase B time; verified 2026-05-25 to declare exactly 3): `standards/` + `aria/` + `aria-orchestrator/`. ALL 3 are submodules; no in-tree special case. G-5 enumerates `.gitmodules` mechanically via `git config --file .gitmodules --get-regexp 'submodule\..*\.path'` and validates every entry it produces.

**Logic per submodule**:
1. Read submodule pointer SHA: `git -C <main_repo> ls-tree HEAD <submodule_path>` → extract SHA.
2. Read submodule's default-branch HEAD on its primary remote: `git -C <submodule_path> ls-remote origin HEAD` → extract SHA. <!-- R1-fix I-ba-4 (I3): drop `--use-local-master` flag — offline fallback is automatic per T-A2.6 (ls-remote failure → RED, not new CLI flag) -->
3. Pointer matches remote default-branch HEAD → PASS; mismatch → ABORT. Offline fallback (ls-remote network failure): emit `[RED] G-5: <submodule> remote unreachable; manual verify required` (RED not ABORT — allows offline ship with owner-override).

**Detached HEAD detection**: if `git -C <submodule_path> symbolic-ref HEAD` returns non-zero (detached state), emit `[ABORT] G-5: <submodule> in detached HEAD state; checkout master before release`.

**Why ABORT (not RED)**: per `[[feedback_submodule_branch_before_archive]]` + `[[feedback_submodule_regression_pitfall]]`, submodule pointer drift at release time has been observed as silent regression source (2026-05-23 PR #123 incident, origin of Aria #124 Spec). Pre-release is the wrong place to ship a drift warning — it must hard-block.

#### E. Gate G-6: Forgejo Discussion URL liveness (~0.5h, threaded into A2.7)

**Source**: per Spec #3 §A.5 line 160 — "Spec #4 (`aria-2.0-m6-release-closeout`) will verify the actual Forgejo Discussion URL. This Spec verifies the FAQ text exists in the release notes file (Spec #4 verifies URL liveness)."

<!-- R1-fix I-cr-3 (I6): G-6 RED on missing URL is EXPECTED v2.0.0 verdict (NOT exception) because Spec #3 §A.5 only mandates FAQ TEXT; URL posting is explicit owner-action OOS-4. Documented ship path: --owner-override "FAQ URL pending owner post" -->

**Logic**:
1. Parse `docs/release-notes-v2.0.0.md` (created by Spec #3 §A.3). Locate "Forgejo Discussion FAQ" section via regex `^#+\s+.*Forgejo Discussion FAQ` (loose heading-level match: Spec #3 §A.3 does not pin the heading level, can be `##` or `###` or `####`). Extract first URL matching `https://forgejo\.10cg\.pub/\S+` regex within the section body.
2. If URL not found (Spec #3 §A.3 didn't include one yet): emit `[RED] G-6: Forgejo Discussion URL not yet posted in release notes; owner action`. **No ABORT** — Spec #3 §A.3 only mandates the FAQ TEXT (`grep -q "Forgejo Discussion FAQ"`), not the URL itself, which is owner-action post-Spec #3 ship. **At v2.0.0 ship time this RED is the EXPECTED verdict**; canonical ship path uses `--owner-override "FAQ URL pending owner post"` for exit 0.
3. If URL found: probe via `forgejo` CLI wrapper. **No PAT / no token in test fixtures** per `[[feedback_secrets_never_in_conversation]]`. Use:
   ```bash
   forgejo GET "<path-extracted-from-URL>" --silent --fail
   ```
   (`forgejo` wrapper handles auth from `/home/dev/.npm-global/bin/forgejo` env injection; Spec #4 never reads PAT). Exit 0 → PASS; non-zero → RED with stderr captured.

**Why RED (not ABORT)**: Discussion URL is a deliverable-promise check, not a release-blocker. Release can ship without the URL live (e.g., owner posts it 1h after release tag). Hard-blocking would create a chicken-and-egg deadlock with the FAQ post timing.

#### F. Gate G-7: 5+1-files SemVer synchronization (6 surfaces; ~0.5h, threaded into A2.8)

<!-- R1-fix C2/I-cr-4 (I7): clarified 5 plugin-stream files + 1 main /VERSION row = 6 surfaces total. Regexes rewritten per live file format verification 2026-05-25 (aria/VERSION + aria/README.md actually use Chinese **版本** OR English **Version** in Markdown blockquote `> ` prefix, NOT YAML `version:` nor unprefixed `**Version**:`) -->

**Source of Truth**: `aria/.claude-plugin/plugin.json` `version` field per CLAUDE.md "版本发布检查清单" §真理来源.

**Derived files** (must all match SoT string; 5 plugin-stream files + 1 main repo row = **6 surfaces total**):

| # | File | Field/Pattern (verified 2026-05-25) | Read method |
|---|------|------------------------------------|-------------|
| 1 (SoT) | `aria/.claude-plugin/plugin.json` | `version` JSON key | `json.load(open(...))['version']` (SoT) |
| 2 | `aria/.claude-plugin/marketplace.json` | top-level `version` + `plugins[0].version` (BOTH must match SoT) | `json.load(...)['version']` AND `[...]['plugins'][0]['version']` |
| 3 | `aria/VERSION` | Chinese Markdown blockquote: `> **版本**: X.Y.Z` | first regex match `^>\s*\*\*版本\*\*:\s*(\d+\.\d+\.\d+)` |
| 4 | `aria/CHANGELOG.md` | top entry `## [X.Y.Z] - YYYY-MM-DD` | first regex match `^##\s+\[(\d+\.\d+\.\d+)\]` |
| 5 | `aria/README.md` | English Markdown blockquote: `> **Version**: X.Y.Z \| ...` | first regex match `^>\s*\*\*Version\*\*:\s*v?(\d+\.\d+\.\d+)` |
| 6 | `/home/dev/Aria/VERSION` (main repo) | Plugin row `\| aria (子模块) \| vX.Y.Z \| ...` | first regex match `aria \(子模块\)\s*\|\s*v?(\d+\.\d+\.\d+)` |

**Phase B pre-G-7 reconcile (T-A1.4)**: Main `/VERSION` row #6 is currently STALE at v1.23.1 (vs SoT v1.27.0 verified 2026-05-25). T-A1.4 reconciles this row to current plugin SoT BEFORE Phase B G-7 testing, ensuring G-7 has a clean baseline at first execution. Per owner Q1 lock 2026-05-25.

**At M6 ship**: SoT version may be `v2.0.0` (aria-plugin bumps alongside Aria 2.0 main repo) OR remain `v1.27.x` (per Spec #3 §A.3 Plugin Compatibility caveat). G-7 verifies INTERNAL consistency across the 6 surfaces, NOT a hardcoded expected version. PASS condition is "all 6 strings equal to SoT plugin.json `version`", not "all equal to a fixed value".

**Why ABORT**: Plugin Compatibility / market consumer correctness depends on these files being consistent. Manual bump error → ABORT until fixed. (Per `[[feedback_plugin_version_drift_multiple_sources]]` 2026-05-15 实证 — drift between these has been observed mid-session.)

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

**PASS condition**: All 3 sibling directories present in `openspec/changes/` AND no pre-archive evidence in `openspec/archive/`. <!-- R2-fix N-ba-2: wire self-check explicitly --> Spec #4 itself (`aria-2.0-m6-release-closeout`) MUST also be present in `openspec/changes/`; if absent (e.g., owner accidentally pre-archived) → ABORT with `[ABORT] G-8: aria-2.0-m6-release-closeout (self) missing from openspec/changes/; out-of-order self-archive`. The self-check is a 4th iteration of the same `is_dir()` probe loop in T-A2.9 (REQUIRED_SIBLINGS list extended with self-name).

#### H. Phase D archive runner (~1.5h, separate sub-script)

**Target file**: `/home/dev/Aria/aria-orchestrator/acceptance/m6-archive-runner.py` (NEW)

**Sequence** (atomic — either all 4 move OR none move):
1. Precondition: invoke `check-m6-release-readiness.py` forwarding `--owner-override` CLI arg (if any). Readiness exit 0 (ALL_PASS) OR exit 1 (RED) with `--owner-override "<rationale>"` propagated → accept. Readiness exit 2 (ABORT) → refuse with `[ERROR] readiness verdict ABORT; archive refused` and exit 2. <!-- R1-fix I-ba-5: clarified CLI arg propagation, not env var -->
2. Compute archive date: `today = datetime.now(timezone.utc).strftime('%Y-%m-%d')`.
3. Plan moves: each of `aria-2.0-m6-{cost-acceptance,e2e-resilience,docs,release-closeout}` from `openspec/changes/X/` to `openspec/archive/{today}-X/`.
4. **Dry-run is the DEFAULT mode**. <!-- R1-fix I-cr-6 (I8): explicit polarity reconciled with tasks.md T-A4.1 -->
   - Default behavior (no flag OR `--dry-run`): print planned 4 moves with absolute paths, exit 0 WITHOUT filesystem mutation.
   - `--execute` is REQUIRED (and explicit) to actually mutate filesystem.
   - Per `[[feedback_schema_migration_3_safeguard_pattern]]` adapted — dry-run-by-default is the equivalent safeguard for archive moves (cannot accidentally trigger 4-dir mv by omitting a flag).
5. **Atomic execute** (`--execute` explicit): use Python `pathlib.Path.rename()` per directory. If any rename fails mid-sequence, attempt rollback (rename completed-moves back to `changes/`). Log per-move success/failure to summary report. If rollback ALSO fails mid-sequence, exit with `[ERROR] inconsistent state — N moves committed, K rollbacks failed; manual intervention required` and exit 3 (NEW exit code: inconsistent-state distinct from ABORT-refuse=2).
6. Post-move: append archive record to most-recent summary report (skipped if dry-run since no report was written this invocation per N-qa-5). In `--execute` mode emit US-026 status diff RECOMMENDATION text only — does NOT execute mutation per OOS-5.
7. **Symmetric recommendation** (NEW R1-fix I-cr-5): emit Forgejo Issue closure recommendation if open M6-tracking issue detected via `forgejo` wrapper enumeration (text-only, no API call per OOS-7).

**Phase D.2 caller contract for exit codes** (R2-fix I-qa-R2-1 + I-NEW-r2-2 — explicit handling for all exit codes):

When `aria:phase-d-closer` D.2 step invokes `m6-archive-runner.py --execute`, the Skill MUST handle each exit code distinctly:

| Exit | Meaning | phase-d-closer D.2 action |
|------|---------|---------------------------|
| 0 | Archive succeeded | Proceed to D.3 (handoff per Rule #9) |
| 1 | (reserved — not emitted by archive runner) | Treat as bug; halt + escalate |
| 2 | Archive refused (readiness ABORT / RED-without-override / pre-archived destinations) | Halt D.2; surface error; do NOT retry; owner-action required |
| **3** | **Inconsistent state** (mid-move OSError + rollback ALSO failed) | **MUST halt D.2 IMMEDIATELY; surface error verbatim to owner; do NOT proceed to D.3; do NOT retry; explicit owner intervention required (likely manual fs cleanup)** |
| 20 | Hard pre-condition failure (git unavailable / MAIN_REPO_ROOT resolution) | Halt D.2; surface error; investigate environment |

The exit-3 path is the **only** non-clean exit that leaves the filesystem in an inconsistent state. `phase-d-closer` D.2 implementations MUST NOT treat exit 3 as "generic non-zero failure" — the owner-facing message must surface the partial-state details from the summary report.

**Atomicity guarantee** (AD-M6-11): on filesystem failure mid-sequence, rollback restores the pre-execute state for completed moves. The script CANNOT guarantee true POSIX atomicity across 4 separate `rename()` syscalls (kernel-level), but it guarantees "best-effort transactional rollback" which is the closest stdlib-only approximation. Documented as known limitation in AD-M6-11.

#### I. Cross-references in sibling Spec "Successor" sections (~0.5h, T-A5.2)

Sibling Specs already have a "Successor" frontmatter pointing at Spec #4 (per Spec #3 line 22, Spec #1 line 682, Spec #2 frontmatter). Spec #4 Phase B adds NO modifications to sibling Spec proposals (they're Approved + sealed). Cross-reference enrichment instead happens in CLAUDE.md "版本发布检查清单" section (T-A5.3) — adds a link to `check-m6-release-readiness.py` as the canonical pre-release gate orchestrator.

#### J. Relationship to phase-d-closer + openspec-archive Skills (NEW R1-fix, ~0.1h doc)

<!-- R1-fix I-cr-2 (I5, owner Q2 lock 2026-05-25): clarify ownership boundary between Spec #4 Python script and existing Aria Skills -->

Aria has two pre-existing canonical archivers: `aria:phase-d-closer` (Skill D.2 step) and `aria:openspec-archive` (CLI bug auto-correct). Spec #4's `m6-archive-runner.py` is **NOT a replacement** for these Skills; it is a **delegation target** invoked BY `phase-d-closer` D.2 step for M6-batch archival specifically:

```
aria:phase-d-closer D.2 (Skill)
    │
    ├── Single-Spec archive case → invokes aria:openspec-archive Skill (existing canonical)
    │
    └── M6 4-Spec batch case (new with Spec #4) →
        invokes `python3 aria-orchestrator/acceptance/m6-archive-runner.py --execute`
        (transactional 4-dir rollback that Skill markdown invocation cannot guarantee)
```

**Why a Python sibling (vs pure Skill)**:
1. **Atomicity**: 4-directory `Path.rename()` with mid-failure rollback requires programmatic control; Skill markdown only orchestrates user-confirmed prompts, not file-system-level transactional behavior.
2. **Precondition gating**: archive runner re-invokes `check-m6-release-readiness.py` as Step 1 (refuses on ABORT verdict). Embedding this precondition in Skill markdown is brittle.
3. **Reusability**: pattern is potentially reusable for M7+ multi-Spec milestone closeouts (memory candidate `feedback_pre_release_orchestrator_gate_pattern`, T-A6.1).

**Phase D.2 invocation path** (Spec #4 owner-runnable workflow):

```
$ /aria:phase-d-closer                                # D.1 + D.2 + D.3
  ↓ D.2 step detects M6 batch case (4 Specs to archive)
  ↓ executes:
$ python3 aria-orchestrator/acceptance/m6-archive-runner.py --execute
  ↓ Step 1: invokes check-m6-release-readiness.py (refuses on ABORT)
  ↓ Step 2-5: atomic 4-directory mv with rollback
  ↓ Step 6: appends archive record to most-recent readiness report
  ↓ Step 7: emits US-026 status update recommendation (OOS-5 owner-action)
  ↓ D.3 step (handoff per Rule #9) — Skill resumes
```

This means owner does NOT typically invoke `m6-archive-runner.py` directly — `phase-d-closer` orchestrates it. Direct invocation remains available for testing / recovery / debug.

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

### Mock-shape discipline (R1-fix N-cr-6)

<!-- R1-fix N-cr-6: per `[[feedback_test_mock_pattern_hides_prod_bug]]` — mock layer must align with prod-return-shape semantics -->

All AC pytest fixtures that mock subprocess invocation (AC-2 mock sibling scripts; AC-4 mock `ls-remote`; AC-5 mock `forgejo` wrapper) MUST mock at the **transport boundary** (`subprocess.run` return value: `CompletedProcess(returncode=N, stdout=..., stderr=...)`), NOT at the gate-evaluation logic itself. Mock return shape MUST mirror real prod-behavior:

- Mocked SHAs in G-5 fixtures: 40-character hex strings matching actual git pointer format (NOT empty `""` and NOT truncated `"HEAD sha refs/heads/master"`).
- Mocked exit codes: integer 0/1/2 (NOT string `"0"` and NOT None).
- Mocked stdout/stderr: bytes-decoded UTF-8 string with realistic line structure (multi-line if sibling script normally emits multi-line, not single-line dummies).

Per `[[feedback_mock_layer_per_failure_semantic]]` — mock layer per failure semantic; SDK boundary mocks ≠ HTTP transport mocks for the same fail mode.

### REPO_ROOT 2-variable resolution (R1-fix C1)

<!-- R1-fix C1 (C-ba-1 / C-qa-1, owner Q-ba-1 unilateral lock): use git rev-parse for robust resolution -->

Spec #4 orchestrator lives at `aria-orchestrator/acceptance/check-m6-release-readiness.py`. This is **two levels deep** from main repo root (`aria-orchestrator/` is a submodule per `.gitmodules`). The script declares TWO Path variables:

```python
import subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent  # aria-orchestrator/acceptance/

# ORCH_ROOT = submodule root, used for sibling subprocess cwd (G-1, G-2)
ORCH_ROOT = HERE.parent  # aria-orchestrator/

# MAIN_REPO_ROOT = main Aria repo, used for cross-repo file reads (G-3, G-5, G-7, G-8)
# Use `git rev-parse --show-toplevel` for robustness against future re-nesting / symlinks
try:
    result = subprocess.run(['git', 'rev-parse', '--show-toplevel'],
                            capture_output=True, text=True, check=True, cwd=str(HERE))
    MAIN_REPO_ROOT = Path(result.stdout.strip())
    # Sanity check: MAIN_REPO_ROOT MUST contain CLAUDE.md (Aria 主仓 signature file)
    if not (MAIN_REPO_ROOT / 'CLAUDE.md').is_file():
        # Fallback if running inside submodule: walk up one more level
        MAIN_REPO_ROOT = HERE.parent.parent
        if not (MAIN_REPO_ROOT / 'CLAUDE.md').is_file():
            print(f'[ERROR] MAIN_REPO_ROOT resolution failed: {MAIN_REPO_ROOT} missing CLAUDE.md', file=sys.stderr)
            sys.exit(20)  # hard pre-condition failure
except subprocess.CalledProcessError:
    # git missing — orchestrator cannot operate; require pre-condition
    print('[ERROR] git unavailable; M6 release readiness cannot run', file=sys.stderr)
    sys.exit(20)
```

This resolves the off-by-one error caught by C-ba-1 / C-qa-1: 5 of 8 gates need main-repo paths (CLAUDE.md, .gitmodules, release-notes-v2.0.0.md, plugin.json + 4 derived, openspec/changes/), which previously resolved silently under submodule root and would have file-missing-ABORTed every release attempt.

---

## Assumptions

Per `[[feedback_per_spec_assumption_recheck]]`: Phase B kick (T-A2.1 start) requires owner to verify these 5 assumptions hold. If any fails, raise to owner before continuing.

<!-- R1-fix C3/N-cr-1 (owner Q3 lock): per-flag is canonical primary path; falsifiability tests per-flag, not aspirational `--all` -->

| # | Assumption | Verifiable when | Verification command |
|---|------------|-----------------|---------------------|
| A-1 | Spec #1 `validate-m6-handoff.py` exists at `aria-orchestrator/docs/validate-m6-handoff.py` AND ships **4 individual flags** (`--check-abi-compat` / `--check-3-day-history` / `--check-cost-method-enum` / `--check-pricing-freshness`) per Spec #1 §AC-6/7/8 contract | Spec #1 Phase B end | `python3 aria-orchestrator/docs/validate-m6-handoff.py --help 2>&1 \| grep -qE -- '--check-abi-compat\|--check-3-day-history\|--check-cost-method-enum\|--check-pricing-freshness'` exits 0 (per-flag canonical proves availability) |
| A-2 | Spec #2 `check-m6-e2e-acceptance.py` exists at `aria-orchestrator/acceptance/check-m6-e2e-acceptance.py` AND ships **3 TG flags** (`--tg-a` / `--tg-b` / `--tg-c`) per Spec #2 AC-1/3/5 contract | Spec #2 Phase B end | `python3 aria-orchestrator/acceptance/check-m6-e2e-acceptance.py --help 2>&1 \| grep -qE -- '--tg-a\|--tg-b\|--tg-c'` exits 0 |
| A-3 | Spec #3 ships CLAUDE.md v2.0 with version field `**版本**: 2.0.0` AND state-checks.yaml contains 3 probe names | Spec #3 Phase C.2 merge | `grep -q '\*\*版本\*\*: 2.0.0' CLAUDE.md && grep -qF 'm6-version-badge-match' .aria/state-checks.yaml && grep -qF 'm6-claude-md-version' .aria/state-checks.yaml && grep -qF 'm6-arch-doc-stale' .aria/state-checks.yaml` exits 0 |
| A-4 | `aria/.claude-plugin/plugin.json` `version` field is readable as canonical SoT | Always (currently `v1.27.0` per `c7e611f` submodule bump) | `python3 -c "import json; print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])"` prints a SemVer |
| A-5 | `/home/dev/.npm-global/bin/forgejo` CLI wrapper exists AND can be invoked without PAT in env (auth is wrapper-managed) | Phase B kick | `forgejo --help` exits 0 (basic command availability check; full auth check is owner-side) |

**Falsifiability gates per assumption**: A-1/A-2 falsify if any documented flag absent from `--help` → block Phase B start (sibling script contract drift caught early per `[[feedback_scaffold_helpers_drift_without_callers]]`). A-3 falsifies if grep returns non-zero → block Phase B start. A-4 falsifies if plugin.json is corrupt → G-7 ABORT. A-5 falsifies if forgejo wrapper missing → G-6 RED with `forgejo CLI unavailable, manual URL check required`.

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
                  │  G-1: subprocess validate-m6-handoff.py   │  ← Spec #1 (per-flag ×4)
                  │  G-2: subprocess check-m6-e2e-...py       │  ← Spec #2 (per-flag ×3)
                  │  G-3: grep CLAUDE.md + state-checks.yaml  │  ← Spec #3
                  │  G-4: date arith vs 2026-08-02 cap        │  ← project_secret_rotation_deferred
                  │  G-5: git ls-tree HEAD vs git ls-remote   │  ← .gitmodules enum (3 submodules)
                  │  G-6: forgejo GET <url-from-release-notes>│  ← Spec #3 §A.5 deferred
                  │  G-7: 6-surfaces SemVer string match      │  ← CLAUDE.md release checklist (5 plugin + 1 main)
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
| AD-M6-10 | Orchestrator exit code aggregation contract | <!-- R2-fix I-NEW-r2-2 -->Three-state verdict (ALL_PASS 0 / RED 1 / ABORT 2) for the orchestrator; PLUS exit 3 (archive runner inconsistent-state, mid-move + rollback failure — emitted by `m6-archive-runner.py` only) + exit 20 (hard pre-condition failure: git unavailable / MAIN_REPO_ROOT resolution — emitted by either script). RED honors `--owner-override "<rationale>"` with non-empty rationale + audit-log entry (whitespace-only treated as empty). ABORT rejects override (hard block). Per-gate stdout `[PASS\|RED\|ABORT] G-N: <msg>` format. Summary report idempotent (timestamped filename, accumulates trail). `phase-d-closer` D.2 caller contract for exit 3 = MUST halt + surface verbatim + no auto-retry (per §H Phase D.2 caller contract table). |
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
# must exit 0; stdout must contain "ALL_PASS", "RED", "ABORT", "--owner-override", "--dry-run", "--gates" (help text mentions all CLI surface) <!-- R2-fix N-qa-3: --gates added -->
```

<!-- R2-fix I-NEW-r2-2: exit code contract amended for exit 3 (archive runner inconsistent-state) + exit 20 (hard pre-condition failure) introduced by R1-fix -->
Exit code contract:
- 0 = ALL_PASS (or RED→0 with `--owner-override`)
- 1 = RED (no override; hold)
- 2 = ABORT (hard block) OR archive runner refusal (readiness ABORT / RED-without-override / pre-archived destinations)
- 3 = archive runner inconsistent-state (rollback failure; manual intervention required) — emitted by `m6-archive-runner.py` only, NOT by `check-m6-release-readiness.py`
- 20 = hard pre-condition failure (git unavailable / MAIN_REPO_ROOT resolution failure) — emitted by either script

Verified by AC-2 / AC-9 / AC-10 boundary scenarios. The orchestrator (`check-m6-release-readiness.py`) emits 0/1/2/20 only; the archive runner (`m6-archive-runner.py`) emits 0/2/3/20 only. Exit 1 is exclusive to orchestrator. Exit 3 is exclusive to archive runner.

### AC-2 — G-1..G-3 sibling consumption gates wired correctly

**Evidence** (3 scenarios per gate, 9 fixtures total):
- `test_G1_PASS`: fixture where `validate-m6-handoff.py` returns exit 0 → orchestrator reports `[PASS] G-1`.
- `test_G1_FAIL_RED`: fixture where `validate-m6-handoff.py` returns exit 1 → orchestrator reports `[RED] G-1`.
- `test_G1_FAIL_ABORT`: fixture where `validate-m6-handoff.py` returns exit 2 → orchestrator reports `[ABORT] G-1`.
- Same triple for G-2 (mock `check-m6-e2e-acceptance.py`).
- Same triple for G-3 (mock state-checks.yaml + CLAUDE.md combos).

Mocking strategy per `[[feedback_test_mock_pattern_hides_prod_bug]]`: mock the subprocess call at the transport layer (`subprocess.run` return value), NOT the gate evaluation logic itself. Mock layer = SDK-equivalent (Python subprocess boundary).

### AC-3 — G-4 secret rotation buffer: 6 boundary + edge tests

<!-- R1-fix C4 (C-qa-2): dates corrected to match tasks.md T-A3.4 (proposal previously had 2026-07-22 = 11d ABORT, mislabeled RED; 2026-07-28 = 5d ABORT, mislabeled 13d).
     R1-fix I1 (I-ba-3/I-qa-5): `--only-gate G-4` → `--gates G-4` flag name unified.
     R1-fix N-qa-2: cap-day-itself test added. -->

**Evidence** (6 boundary tests; `--gates G-4` selector isolates G-4 from other gates):
```bash
# Test 1: 21d boundary (PASS, hits exact PASS/RED boundary)
M6_RELEASE_TODAY_OVERRIDE=2026-07-12 python3 ... check-m6-release-readiness.py --gates G-4
# stdout contains "[PASS] G-4: secret rotation buffer 21d", exit 0

# Test 2: 20d (RED, just below PASS boundary)
M6_RELEASE_TODAY_OVERRIDE=2026-07-13 python3 ... check-m6-release-readiness.py --gates G-4
# stdout contains "[RED] G-4: secret rotation buffer 20d < 21d", exit 1

# Test 3: 14d (RED, at exact RED/ABORT boundary)
M6_RELEASE_TODAY_OVERRIDE=2026-07-19 python3 ... check-m6-release-readiness.py --gates G-4
# stdout contains "[RED] G-4: secret rotation buffer 14d < 21d", exit 1

# Test 4: 13d (ABORT, just below RED boundary)
M6_RELEASE_TODAY_OVERRIDE=2026-07-20 python3 ... check-m6-release-readiness.py --gates G-4
# stdout contains "[ABORT] G-4: secret rotation buffer 13d < 14d", exit 2

# Test 5: cap-day-itself (ABORT, buffer_days=0)
M6_RELEASE_TODAY_OVERRIDE=2026-08-02 python3 ... check-m6-release-readiness.py --gates G-4
# stdout contains "[ABORT] G-4: secret rotation buffer 0d" (NOT "cap exceeded by 0 days"), exit 2

# Test 6: past-cap (ABORT, buffer_days<0)
M6_RELEASE_TODAY_OVERRIDE=2026-08-10 python3 ... check-m6-release-readiness.py --gates G-4
# stdout contains "[ABORT] G-4: ... cap exceeded by 8 days", exit 2
```

Boundary semantics: PASS condition is `buffer_days >= 21`; RED condition is `14 <= buffer_days < 21`; ABORT condition is `buffer_days < 14` (inclusive of `buffer_days == 0` cap-day and `buffer_days < 0` past-cap). Verified at exact boundaries (21d / 20d / 14d / 13d) + 2 edge cases (0d cap-day / past-cap negative). Date arithmetic in UTC via `datetime.now(timezone.utc).date()` (operators running near 00:00 UTC may observe boundary shift; documented in §C).

### AC-4 — G-5 submodule pointer probe: 3 scenarios

**Evidence**:
- `test_G5_PASS_aligned`: fixture git repo with submodule pointer == remote default-branch HEAD → orchestrator reports `[PASS] G-5`.
- `test_G5_ABORT_misaligned`: fixture with stale submodule pointer (one commit behind remote) → orchestrator reports `[ABORT] G-5: <submodule> pointer <stale-sha> != remote master <fresh-sha>`.
- `test_G5_ABORT_detached`: fixture with submodule in detached HEAD state → orchestrator reports `[ABORT] G-5: <submodule> in detached HEAD state`.

Test fixtures use `tempfile.TemporaryDirectory()` + `subprocess.run(['git', 'init', ...])` to construct synthetic repo states. No live remote dependency.

### AC-5 — G-6 Forgejo Discussion URL liveness: 3 scenarios + meta-test

<!-- R1-fix I-qa-2 (I10): PAT meta-test reframe (Forgejo PATs lack unique prefix; old `forgejo_pat_\w+` regex tautologically passes) -->

**Evidence**:
- `test_G6_PASS_url_200`: release-notes-v2.0.0.md contains `https://forgejo.10cg.pub/10CG/Aria/issues/...`; mock `subprocess.run` for `forgejo GET <path>` returns `CompletedProcess(returncode=0, stdout='{"id":42,...}', stderr='')` → orchestrator reports `[PASS] G-6`. Summary report contains stderr (empty) but NOT stdout (per G-6 stderr-only capture).
- `test_G6_RED_url_404`: same URL; mock returns `CompletedProcess(returncode=22, stdout='', stderr='HTTP/1.1 404 Not Found')` → orchestrator reports `[RED] G-6: Forgejo URL <url> returned non-zero exit (likely 404 / offline / auth fail); manual verify`.
- `test_G6_RED_no_url`: release-notes-v2.0.0.md missing FAQ URL → orchestrator reports `[RED] G-6: Forgejo Discussion URL not yet posted in release notes; owner action`.

**Secret hygiene meta-test** per `[[feedback_secrets_never_in_conversation]]` (reframed per R1-fix I-qa-2):
- Test fixtures MUST NOT reference env vars known to carry credentials. Meta-test enumerates all `*.py` files in `aria-orchestrator/tests/acceptance/` directory (R2-fix I-qa-2 PARTIAL closure: `fixture_file` now explicitly scoped to `pathlib.Path(__file__).parent.glob('*.py')`); for each: `assert all(env_ref not in open(fixture_file).read() for env_ref in ['FORGEJO_TOKEN', 'ARIA_PAT', 'FORGEJO_PAT', 'GH_TOKEN', 'GITHUB_TOKEN'])`.
- Test fixtures MUST NOT call `forgejo` subprocess live; ALL `subprocess.run` invocations for `forgejo` in test scope are monkey-patched (mocked at transport boundary). `assert isinstance(subprocess.run, unittest.mock.MagicMock)` during test execution.
- Fixture mock return values use placeholder URLs (e.g., `https://forgejo.10cg.pub/10CG/Aria/issues/999`) NOT live URLs.
- Summary report writer (T-A2.11) MUST capture G-6 **stderr only** (NOT stdout) — assertion: `assert 'auth_header_redacted' not in report_content AND forgejo_wrapper_stdout NOT in report_content`. Per `[[feedback_nomad_inspect_secret_leak]]` + `[[feedback_secret_guard_plugin_upstream_dogfood]]` — Forgejo wrapper stdout may contain auth headers; never persists to git-tracked report.

### AC-6 — G-7 6-surfaces sync probe: 5 scenarios

<!-- R1-fix I-qa-1 (I9): added 3 scenarios (marketplace[0] stale, plugin.json missing, multi-stale).
     R1-fix I-cr-4 (I7): clarified "6 surfaces" (5 plugin-stream + 1 main /VERSION row). -->

**Evidence** (6 surfaces = plugin.json SoT + marketplace.json [top + plugins[0]] + aria/VERSION + aria/CHANGELOG.md + aria/README.md + 主项目/VERSION row):
- `test_G7_PASS_all_match`: fixture where all 6 surfaces show `2.0.0` → orchestrator reports `[PASS] G-7`.
- `test_G7_ABORT_one_stale`: fixture where plugin.json = `2.0.0` but CHANGELOG.md top entry = `1.27.0` → orchestrator reports `[ABORT] G-7: drift detected (CHANGELOG.md=1.27.0 != SoT=2.0.0)` with explicit per-file diff.
- `test_G7_ABORT_marketplace_plugins0_stale`: fixture where marketplace.json top-level `version` = `2.0.0` but `plugins[0].version` = `1.27.0` → orchestrator reports `[ABORT] G-7: drift detected (marketplace.json plugins[0].version=1.27.0 != SoT=2.0.0)` (verifies nested-path correctness).
- `test_G7_ABORT_plugin_json_missing`: fixture where `aria/.claude-plugin/plugin.json` is absent OR unparseable → orchestrator reports `[ABORT] G-7: SoT plugin.json missing OR unparseable; cannot derive expected version`.
- `test_G7_ABORT_multi_stale`: fixture where CHANGELOG.md AND README.md AND main /VERSION are ALL stale (3 of 6 surfaces drifted) → orchestrator reports `[ABORT] G-7` listing ALL 3 stale files in the per-file diff (not just the first).

The SoT is `plugin.json`; all other surfaces are compared against it (NOT against a hardcoded expected version).

### AC-7 — G-8 archive trigger ordering: 2 scenarios

**Evidence**:
- `test_G8_PASS_all_active`: fixture where `openspec/changes/` contains all 3 sibling directories AND `openspec/archive/` contains no `*-aria-2.0-m6-*` directories → orchestrator reports `[PASS] G-8`.
- `test_G8_ABORT_prearchived`: fixture where `openspec/changes/aria-2.0-m6-cost-acceptance/` is absent BUT `openspec/archive/2026-05-30-aria-2.0-m6-cost-acceptance/` exists → orchestrator reports `[ABORT] G-8: aria-2.0-m6-cost-acceptance already archived; Spec #4 out-of-order`.
- `test_G8_ABORT_totally_missing` (R2-fix N-qa-6): fixture where `aria-2.0-m6-cost-acceptance` is absent from BOTH `openspec/changes/` AND `openspec/archive/` (never existed / accidentally deleted) → orchestrator reports `[ABORT] G-8: aria-2.0-m6-cost-acceptance missing from openspec/changes/ and openspec/archive/`.
- `test_G8_ABORT_self_missing` (R2-fix N-ba-2): fixture where `openspec/changes/aria-2.0-m6-release-closeout/` (self) is absent → orchestrator reports `[ABORT] G-8: aria-2.0-m6-release-closeout (self) missing from openspec/changes/; out-of-order self-archive`.

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

### AC-9 — Owner override CLI flag honored for RED but rejected for ABORT
<!-- R2-fix N-NEW-r2-1: heading fixed from "env var" to "CLI flag" (mechanism is `--owner-override` argparse arg, not environment variable) -->

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
- Whitespace-only rationale (`--owner-override "   "` 3 spaces) → exit 2 with `[ERROR] --owner-override rationale must be non-empty (whitespace-only is treated as empty)`. <!-- R1-fix N-qa-4 -->
- Missing rationale (`--owner-override` no arg) → argparse rejects with non-zero exit.
- RED + override → summary report includes verbatim rationale + timestamp.

Implementation MUST use `rationale.strip()` for the non-empty check (per N-qa-4) so whitespace-only rationale is rejected. Rationale shell-metachar sanitization is OOS (rationale string is captured-and-logged, never `eval`'d or `subprocess`'d).

### AC-10 — Phase D archive runner: 4 directories moved atomically OR none moved (with idempotency + double-rollback coverage)

<!-- R1-fix I-qa-3 (I11): added idempotency + rollback-also-fails scenarios -->

**Evidence**:
- `test_archive_PASS`: fixture with all 4 sibling+self Spec dirs in `openspec/changes/`; readiness exits 0 → archive runner with `--execute` moves all 4 to `openspec/archive/{today}-*` AND `openspec/changes/aria-2.0-m6-*` is now empty.
- `test_archive_ABORT_no_partial`: simulate filesystem failure on the 3rd of 4 renames (mock `pathlib.Path.rename` to raise on the 3rd call) → archive runner rolls back: first 2 moves reversed, last 2 never attempted, final state matches pre-execute state.
- `test_archive_IDEMPOTENT`: invoke `--execute` twice on already-archived state → second invocation detects destinations already exist; exits non-zero (3 or distinct error code) with `[ERROR] N of 4 destinations already exist; archive runner refuses to overwrite (already archived?)`. NO mutation; NO silent rename; NO `FileNotFoundError` crash.
- `test_archive_ROLLBACK_also_fails`: mock both the forward 3rd rename AND a rollback rename to raise `OSError` (double-mock pattern) → script exits with exit code 3 (`[ERROR] inconsistent state — N moves committed, K rollbacks failed; manual intervention required`) instead of unhandled exception crash. Inconsistent-state final state documented in summary report.
- `test_archive_dry_run`: invoke without `--execute` (default = dry-run per I-cr-6 fix) → stdout prints 4 planned moves; filesystem unchanged; NO summary report written (skipped per N-qa-5).
- Precondition test: `test_archive_REFUSES_on_ABORT_verdict`: readiness exits 2 → archive runner refuses with `[ERROR] readiness verdict ABORT; archive refused` and exits 2.
- Precondition test: `test_archive_proceeds_on_RED_with_override`: readiness exits 1 + `--owner-override "ack"` → archive runner forwards override + proceeds.
- Precondition test: `test_archive_REFUSES_on_RED_without_override`: readiness exits 1 + no `--owner-override` → archive runner refuses (RED-without-override is hold).

Per `[[feedback_schema_migration_3_safeguard_pattern]]` adapted: dry-run is the migration-equivalent safeguard for archive moves; rollback is the integrity-check equivalent. Idempotency + double-rollback coverage closes the residual risk window (R-M6CL-5).

---

## Risks

| ID | Risk | Severity | Mitigation |
|----|------|----------|------------|
| R-M6CL-1 | Secret rotation buffer drift — if M6 ship slips past plan, G-4 fires `<14d ABORT` before owner can rotate the 9-key carry-forward (per `[[project_secret_rotation_deferred_2026-05-02]]`) | Medium | Owner pre-emptively rotates secrets if calendar projection shows ship date < 2026-07-12 (21d before cap). G-4 RED window at 14-20d gives 2-week advance warning. Hard cap 2026-08-02 is owner-set; re-calibration requires new Spec. |
| R-M6CL-2 | Sibling script path drift — Spec #1 / #2 / #3 rename scripts during Phase B implementation, breaking G-1 / G-2 / G-3 subprocess invocations | Medium | Phase B kick verify probe (T-A2.0) tests all 3 script paths + CLI flag contracts BEFORE T-A2.2 implementation. Failed verify → owner escalation. Per `[[feedback_per_spec_assumption_recheck]]` + `[[feedback_scaffold_helpers_drift_without_callers]]`. |
| R-M6CL-3 | Forgejo Discussion URL race — Spec #3 §A.5 only mandates FAQ TEXT in release notes; actual URL is owner-action post-Spec #3 ship. If Spec #4 runs before Spec #3 §A.5 owner-action complete, G-6 emits RED (which is correct, but may confuse "is M6 ready?" reading) | Low | G-6 emits RED (not ABORT) precisely because URL absence is expected mid-window. G-8 archive trigger eligibility ensures Spec #4 runs AFTER sibling Phase B; FAQ posting is OOS-4 explicit. RED→ship path with `--owner-override "FAQ URL pending owner post"` is the documented release path. |
| R-M6CL-4 | 6-surfaces SemVer string drift — manual bump error in any of 6 surfaces (plugin.json SoT + 4 derived plugin-stream files + 主项目 /VERSION row) → G-7 ABORT | Medium | Pre-bump owner uses CLAUDE.md release checklist as authoritative procedure. G-7 ABORT is the correct response (catch drift pre-ship). Mitigation is documentation, not script — Spec #4 is the catcher, not the preventer. |
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
| Spec #1 `aria-2.0-m6-cost-acceptance` Phase B complete | Upstream (hard) | G-1 invokes `validate-m6-handoff.py` per-flag (4 calls: `--check-abi-compat` / `--check-3-day-history` / `--check-cost-method-enum` / `--check-pricing-freshness`). Per-flag canonical per owner Q3 lock 2026-05-25. Phase B kick verify (A-1). |
| Spec #2 `aria-2.0-m6-e2e-resilience` Phase B complete | Upstream (hard) | G-2 invokes `check-m6-e2e-acceptance.py` per-flag (3 calls: `--tg-a` / `--tg-b` / `--tg-c`). Per-flag canonical per owner Q3 lock. Phase B kick verify (A-2). |
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
- `[[feedback_mock_layer_per_failure_semantic]]` — Mock-shape discipline in §Constraints (R1-fix N-cr-6).
- `[[feedback_nomad_inspect_secret_leak]]` — G-6 stdout suppression rationale (R1-fix C6).
- `[[feedback_secret_guard_plugin_upstream_dogfood]]` — G-6 stdout suppression rationale (R1-fix C6).
- `[[feedback_scaffold_helpers_drift_without_callers]]` — A-1/A-2 falsifiability rationale (sibling script flag drift caught at Phase B kick).

**NEW candidate memory entries** (NOT yet existing; T-A6.1 writes at Phase D if Phase B impl proves pattern useful):
- `feedback_pre_release_orchestrator_gate_pattern` — Spec #4 design pattern source for M7+ release closeout reuse.
- `feedback_release_phase_d_5_files_synchronization` — G-7 6-surfaces SoT pattern (5 plugin-stream + 1 main /VERSION).

<!-- R1-fix I-cr-1: previously listed as if existing; now correctly marked NEW candidates with conditional write decision at Phase D. -->

---

> **Phase A.1 Spec drafting complete 2026-05-25 + R1-fix applied 2026-05-25.** Ready for Phase A.2 R2 audit (3-agent challenge: tech-lead-critic + qa-engineer + code-reviewer per `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]`). Audit collapse default per memory: R2 4/4 SCOPE_OK + R1 critical 100% closed + ≥70% reduction → collapse R3.
