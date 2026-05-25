# M6 Spec #4 Tasks — Release Closeout (pre-release gates orchestrator + archive trigger)

> **Spec**: [aria-2.0-m6-release-closeout](./proposal.md)
> **Level**: 2 (Minimal)
> **Status**: Draft (Phase A.1)
> **Brainstorm Source**: [.aria/decisions/2026-05-24-us026-m6b-brainstorm.md](../../../.aria/decisions/2026-05-24-us026-m6b-brainstorm.md) (DEC-20260524-001 Q-final-1 Menu C)
> **Estimated total**: ~10h impl (single SoT per `[[feedback_spec_v2_body_propagation_2pass]]`; cited identically in proposal §Effort baseline + frontmatter)
> **Agent**: backend-architect (primary; tech-lead-critic for Phase A.2; qa-engineer for AC pytest design review)
> **Sequencing constraint**: Phase B MUST start AFTER Spec #1 + #2 + #3 all complete Phase C.2 merge (their acceptance scripts must exist on disk for G-1..G-3 to invoke). Phase A.2 audit can overlap with sibling Phase B.

---

## Task Group Overview

| Group | Topic | Scope ref | Est |
|-------|-------|-----------|-----|
| T-A1 | Scaffolding (mkdir, .gitkeep, .gitignore, B-kick verify probe) | §What A + §Assumptions | ~0.5h |
| T-A2 | Orchestrator script G-1..G-8 + aggregator + owner-override | §What A-G | ~3h |
| T-A3 | Pytest suite (AC-1 through AC-10 with boundary scenarios) | §Acceptance | ~3h |
| T-A4 | Phase D archive runner (atomic 4-dir + dry-run + rollback) | §What H + AD-M6-11 | ~1.5h |
| T-A5 | Docs (artifact dir README + CLAUDE.md checklist link) | §What I + Cross-references | ~1h |
| T-A6 | Memory candidate entry (deferred to Phase D, not now) | §Risks + Memory entries | ~0.5h |

---

## T-A1 — Scaffolding (~0.5h)

- [ ] 1.1 Create directory `.aria/m6-release-readiness/` with empty `.gitkeep` file. Commit message: `chore(m6-release-closeout): scaffold .aria/m6-release-readiness/ artifact directory`. Sub-step: verify the directory does not pre-exist (avoid clobbering accidental owner-created file).

- [ ] 1.2 Add `.aria/m6-release-readiness/*.md` to `.gitignore` exclusion list IF report files should NOT be tracked. Decision (Phase A.1 default): **track the reports** (audit trail value per `[[feedback_audit_driven_fix_conventions]]`); therefore NO `.gitignore` entry needed. The `.gitkeep` file is the only tracked initial content. (Revisit at Phase A.2 if owner prefers untracked.)

- [ ] 1.3 Phase B kick verify probe (per `[[feedback_per_spec_assumption_recheck]]` + §Assumptions A-1..A-5): create a one-off script `aria-orchestrator/acceptance/m6-release-closeout-verify-assumptions.sh` (NOT committed; runs once at B-kick) that exercises all 5 assumptions:
  - A-1: `python3 aria-orchestrator/docs/validate-m6-handoff.py --all --help`
  - A-2: `python3 aria-orchestrator/acceptance/check-m6-e2e-acceptance.py --all --help`
  - A-3: `grep -q '\*\*版本\*\*: 2.0.0' CLAUDE.md && grep -qF 'm6-version-badge-match' .aria/state-checks.yaml && grep -qF 'm6-claude-md-version' .aria/state-checks.yaml && grep -qF 'm6-arch-doc-stale' .aria/state-checks.yaml`
  - A-4: `python3 -c "import json; print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])"`
  - A-5: `forgejo --help`

  Any failure → STOP, escalate to owner. Per `[[feedback_probe_first_scope_reframe]]`. Script is throwaway (delete after green run); evidence captured in Phase B opening commit message.

---

## T-A2 — Orchestrator script (~3h)

<!-- Per §What A + §How diagram: G-1..G-8 sequential, three-state verdict, summary report -->

- [ ] 2.1 Create skeleton `aria-orchestrator/acceptance/check-m6-release-readiness.py`:
  - Python 3.9+ stdlib only (no PyYAML / requests / etc).
  - Argparse: `--owner-override "<rationale>"` (str, default None), `--dry-run` (bool, default False, propagated to summary-report write path), `--gates G-N[,G-M,...]` (optional gate selector for tests; default = run all 8).
  - Resolve `HERE = Path(__file__).resolve().parent; REPO_ROOT = HERE.parent` mirroring `validate-m5-handoff.py:40-41` (canonical 2-level pattern per `[[feedback_per_spec_assumption_recheck]]` — DO NOT hardcode `/home/dev/Aria/`).
  - Top-level `main()` runs G-1..G-8 in sequence, accumulates per-gate verdict list, aggregates, writes summary, exits 0/1/2.
  - Stub each G-N as a function `gate_N(...)` returning `(verdict_str, message_str)` tuple where verdict ∈ {"PASS", "RED", "ABORT"}.

- [ ] 2.2 Implement `gate_1_cost_acceptance()`:
  - Subprocess invoke `python3 aria-orchestrator/docs/validate-m6-handoff.py --all` via `subprocess.run(..., capture_output=True, text=True, timeout=60)`.
  - Exit 0 → PASS; exit 1 → RED; exit 2 → ABORT; any other exit → ABORT with `unexpected exit code N` message.
  - If `--all` flag unsupported (returncode 2 + stderr contains `unrecognized arguments`), fall back to 4 individual flags AND their exit codes: `--check-abi-compat`, `--check-3-day-history`, `--check-cost-method-enum`, `--check-pricing-freshness`. All 0 → PASS; any 1 → RED; any 2 → ABORT.
  - Capture stdout/stderr verbatim → summary report.

- [ ] 2.3 Implement `gate_2_e2e_resilience()`:
  - Subprocess invoke `python3 aria-orchestrator/acceptance/check-m6-e2e-acceptance.py --all` similar pattern.
  - Fallback to `--tg-a` / `--tg-b` / `--tg-c` if `--all` unsupported.
  - Same exit-code-to-verdict mapping.

- [ ] 2.4 Implement `gate_3_docs()`:
  - **Primary check (stdlib-only)**: grep CLAUDE.md for `**版本**: 2.0.0`, `两层 AI 分工`, `Aria 2.0 运行时` (use Python `pathlib.Path.read_text().splitlines()` + manual substring search, NOT shell grep — keeps script portable).
  - **State-checks probe presence**: read `.aria/state-checks.yaml` as text; verify 3 probe names appear via substring search.
  - **Optional PyYAML structural check**: `if importlib.util.find_spec('yaml'): import yaml; ...` — do the AC-4-equivalent dict-traversal verification. If PyYAML absent, log `[INFO] G-3: PyYAML unavailable; structural check skipped, grep-only` and proceed with grep result.
  - All grep PASS → PASS; any grep FAIL → RED; file missing (CLAUDE.md or state-checks.yaml absent) → ABORT.

- [ ] 2.5 Implement `gate_4_secret_rotation_buffer()`:
  - `HARD_CAP = date(2026, 8, 2)` literal (per AD-M6-12 + `[[project_secret_rotation_deferred_2026-05-02]]`).
  - Read `os.environ.get('M6_RELEASE_TODAY_OVERRIDE')`; if set, parse via `date.fromisoformat()`; else `datetime.now(timezone.utc).date()`.
  - Compute `buffer_days = (HARD_CAP - today).days`.
  - `>= 21` → PASS; `14..20` → RED; `< 14` → ABORT. Message includes buffer_days + cap date + (if override) override date echoed.
  - Edge case: `buffer_days < 0` (cap already past) → ABORT with explicit `cap exceeded by N days` message.

- [ ] 2.6 Implement `gate_5_submodule_pointer()`:
  - Enumerate submodules via `git config --file .gitmodules --get-regexp 'submodule\..*\.path'`. Parse module-name + path pairs.
  - For each submodule:
    - Main-repo pointer: `git ls-tree HEAD <path>` → parse SHA (3rd column of single output line).
    - Submodule's remote HEAD: `git -C <path> ls-remote origin HEAD` → parse SHA (1st column).
    - Detached HEAD check: `git -C <path> symbolic-ref HEAD 2>/dev/null` → if nonzero, ABORT for this submodule.
    - Pointer match → PASS; mismatch → ABORT with both SHAs printed.
  - `aria-orchestrator/` not in `.gitmodules`? Skip with `[PASS] G-5: aria-orchestrator skipped (in-tree, not submodule)`.
  - Aggregate: any submodule ABORT → gate ABORT; all PASS → gate PASS.
  - Offline fallback: if `ls-remote` fails (network), emit `[RED] G-5: <submodule> remote unreachable; manual verify required`. RED not ABORT to allow offline ship paths (rare but possible).

- [ ] 2.7 Implement `gate_6_forgejo_discussion_url()`:
  - Read `docs/release-notes-v2.0.0.md` (per Spec #3 §A.3).
  - Locate "Forgejo Discussion FAQ" section heading via regex `^##\s+Forgejo Discussion FAQ`. If section missing → RED with `Forgejo Discussion FAQ section absent`.
  - Within FAQ section, extract first URL matching `https://forgejo\.10cg\.pub/\S+` regex.
  - If no URL → RED with `Forgejo Discussion URL not yet posted in release notes; owner action`.
  - If URL found: derive Forgejo path (strip `https://forgejo.10cg.pub`) → subprocess `forgejo GET <path>` capture exit code.
  - Exit 0 → PASS; nonzero → RED with stderr captured (do NOT log stdout — Forgejo wrapper output may contain auth headers per `[[feedback_secrets_never_in_conversation]]`).
  - If `forgejo` CLI absent (`FileNotFoundError`): RED with `forgejo CLI unavailable; manual URL check required, paste exit code into summary`.

- [ ] 2.8 Implement `gate_7_five_files_version_sync()`:
  - SoT read: `aria/.claude-plugin/plugin.json` → `json.load(...)['version']` → save as `sot_version`. On parse failure → ABORT.
  - Derived reads (each returns extracted version string OR `None` on parse failure):
    1. `aria/.claude-plugin/marketplace.json`: top-level `version` + `plugins[0]['version']` (BOTH must match SoT).
    2. `aria/VERSION`: regex `^version:\s*(\S+)` last match (file uses YAML-ish `version: X.Y.Z` per current format).
    3. `aria/CHANGELOG.md`: regex `^##\s+\[(\d+\.\d+\.\d+)\]` first match.
    4. `aria/README.md`: regex `^\*\*Version\*\*:\s*v?(\S+)` first match.
    5. `VERSION` (main project root): regex `aria \(子模块\)\s*\|\s*v?(\S+)` first match (per current `/home/dev/Aria/VERSION` format observed).
  - All 5 derived strings == `sot_version` → PASS. Any mismatch → ABORT with explicit per-file diff (file_path + expected_sot + actual_value).
  - Any parse failure → ABORT (cannot ship with unparseable version file).

- [ ] 2.9 Implement `gate_8_archive_trigger_eligibility()`:
  - For each of 3 sibling Specs (`aria-2.0-m6-cost-acceptance`, `aria-2.0-m6-e2e-resilience`, `aria-2.0-m6-docs`):
    - Check `openspec/changes/<sibling>/` is directory → expected (still active).
    - If absent: probe `openspec/archive/*-<sibling>/` glob → if pre-archive found, ABORT with `<sibling> already archived (<path>); Spec #4 out-of-order`. If absent both places, ABORT with `<sibling> missing from openspec/changes/ AND openspec/archive/`.
  - All 3 present in `changes/` AND none in `archive/` → PASS.

- [ ] 2.10 Implement aggregator + exit code logic + owner-override:
  - Collect 8 `(verdict, message)` tuples.
  - Count ABORT / RED / PASS.
  - If any ABORT: verdict = "ABORT", exit_code = 2. If `--owner-override` set, reject: stderr `[ERROR] --owner-override rejected: ABORT verdict has no override path`, exit_code = 2.
  - Else if any RED: verdict = "RED", exit_code = 1. If `--owner-override "<rationale>"` set (non-empty), exit_code becomes 0 (ship with override); log `[VERDICT] RED → SHIP (owner-override)` + verbatim rationale in summary.
  - Else: verdict = "ALL_PASS", exit_code = 0.
  - Print final `[VERDICT] <verdict>` line to stdout AFTER all 8 per-gate lines.
  - Empty rationale (`--owner-override ""`): exit_code = 2 with `[ERROR] --owner-override rationale must be non-empty`.

- [ ] 2.11 Implement summary report writer:
  - Filename: `.aria/m6-release-readiness/{datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")}-report.md`.
  - Idempotent: each invocation writes NEW file (NEVER overwrites). Directory accumulates trail.
  - Content sections: `# M6 Release Readiness Report — {ts}`, `## Invocation`, `## Per-Gate Verdicts` (G-1..G-8 each with full stdout/stderr), `## Aggregate Verdict`, `## Owner Override` (if used; includes verbatim rationale + timestamp).
  - Report write is always done (PASS / RED / ABORT alike) UNLESS `--dry-run` (in dry-run, print intended filename to stdout, do not write).

---

## T-A3 — Pytest suite (~3h)

<!-- AC-1 through AC-10 per proposal §Acceptance criteria. Each AC gets at least one test, boundary ACs get parametrized scenarios. -->

- [ ] 3.1 Setup `aria-orchestrator/tests/acceptance/test_m6_release_readiness.py` with pytest fixtures:
  - `tmp_repo_fixture`: `tempfile.TemporaryDirectory()` + `subprocess.run(['git', 'init'])` + minimal `aria/.claude-plugin/plugin.json` + minimal `.aria/state-checks.yaml` + minimal `CLAUDE.md`. Used by all tests needing repo context.
  - `mock_sibling_scripts_fixture`: monkey-patch `subprocess.run` for `validate-m6-handoff.py` / `check-m6-e2e-acceptance.py` invocations to return configurable exit codes. Per `[[feedback_test_mock_pattern_hides_prod_bug]]`: mock at subprocess transport layer ONLY.

- [ ] 3.2 AC-1 — `test_orchestrator_exists_and_help_works`: assert script exists; `--help` exits 0; help text contains all CLI surface keywords (ALL_PASS / RED / ABORT / --owner-override / --dry-run).

- [ ] 3.3 AC-2 — G-1..G-3 sibling consumption (9 fixtures):
  - `test_G1_PASS` / `test_G1_RED` / `test_G1_ABORT`: mock validate-m6-handoff.py returns 0/1/2.
  - `test_G2_PASS` / `test_G2_RED` / `test_G2_ABORT`: same for check-m6-e2e-acceptance.py.
  - `test_G3_PASS` / `test_G3_RED` / `test_G3_ABORT`: combinations of CLAUDE.md content + state-checks.yaml content (PASS = all 3 grep + 3 probe names present; RED = 1 grep miss; ABORT = file missing).
  - Use `pytest.mark.parametrize` for the 3 verdict cases per gate.

- [ ] 3.4 AC-3 — G-4 secret rotation buffer (3 boundary + 2 edge):
  - `test_G4_PASS_at_21d`: `M6_RELEASE_TODAY_OVERRIDE=2026-07-12` → exit 0 with `[PASS] G-4: secret rotation buffer 21d`.
  - `test_G4_PASS_above_21d`: `M6_RELEASE_TODAY_OVERRIDE=2026-07-01` → exit 0.
  - `test_G4_RED_at_20d`: `M6_RELEASE_TODAY_OVERRIDE=2026-07-13` → exit 1.
  - `test_G4_RED_at_14d`: `M6_RELEASE_TODAY_OVERRIDE=2026-07-19` → exit 1.
  - `test_G4_ABORT_at_13d`: `M6_RELEASE_TODAY_OVERRIDE=2026-07-20` → exit 2.
  - `test_G4_ABORT_past_cap`: `M6_RELEASE_TODAY_OVERRIDE=2026-08-10` → exit 2 with `cap exceeded by 8 days`.

- [ ] 3.5 AC-4 — G-5 submodule pointer (3 scenarios):
  - `test_G5_PASS_aligned`: tmp_repo with submodule pointer = remote HEAD → exit 0.
  - `test_G5_ABORT_misaligned`: tmp_repo with stale pointer (1 commit behind) → exit 2 with explicit SHA diff.
  - `test_G5_ABORT_detached`: tmp_repo with submodule in detached HEAD → exit 2 with `detached HEAD state` message.
  - Optional: `test_G5_RED_offline`: mock `ls-remote` to raise → exit 1 RED with `remote unreachable`.

- [ ] 3.6 AC-5 — G-6 Forgejo Discussion URL (3 scenarios):
  - `test_G6_PASS_url_200`: tmp_repo with release-notes containing valid URL + mock `forgejo` returns exit 0 → PASS.
  - `test_G6_RED_url_404`: same URL + mock `forgejo` returns nonzero → RED.
  - `test_G6_RED_no_url`: release-notes missing FAQ URL → RED `not yet posted`.
  - **Secret-hygiene assertion** per `[[feedback_secrets_never_in_conversation]]`: assert mock fixtures contain ZERO occurrences of strings matching PAT patterns (`r'forgejo_pat_\w+'`, `r'ghp_\w+'`, etc) — meta-test that prevents future fixture writers from leaking credentials.

- [ ] 3.7 AC-6 — G-7 5-files SemVer (2 scenarios):
  - `test_G7_PASS_all_match`: tmp_repo fixture with all 6 files showing `2.0.0` → PASS.
  - `test_G7_ABORT_changelog_stale`: plugin.json=`2.0.0`, CHANGELOG.md top entry=`1.27.0` → ABORT with `drift detected (CHANGELOG.md=1.27.0 != SoT=2.0.0)`.
  - Optional: `test_G7_ABORT_marketplace_plugins0_stale`: top-level marketplace.json version=`2.0.0` but `plugins[0]['version']`=`1.27.0` → ABORT (verify nested-path correctness).

- [ ] 3.8 AC-7 — G-8 archive trigger ordering (2 scenarios):
  - `test_G8_PASS_all_active`: tmp_repo with all 3 sibling dirs in `openspec/changes/`, none in `openspec/archive/` → PASS.
  - `test_G8_ABORT_prearchived`: tmp_repo with `cost-acceptance` only in `openspec/archive/2026-05-30-aria-2.0-m6-cost-acceptance/` → ABORT.

- [ ] 3.9 AC-8 — Summary report write idempotency:
  - `test_report_written_on_first_run`: invoke orchestrator → assert 1 `.md` file appears in `.aria/m6-release-readiness/`.
  - `test_report_repeat_run_appends`: invoke twice (with `time.sleep(1)` between) → assert 2 distinct `.md` files (no overwrite).
  - `test_report_dry_run_no_write`: invoke with `--dry-run` → assert 0 files written + stdout shows intended filename.

- [ ] 3.10 AC-9 — Owner override:
  - `test_override_accepted_on_RED`: fixture forces G-N to RED → invoke with `--owner-override "ack: known"` → exit 0; assert summary contains rationale.
  - `test_override_rejected_on_ABORT`: fixture forces G-N to ABORT → invoke with `--owner-override "..."` → exit 2; stderr contains `--owner-override rejected`.
  - `test_override_empty_rationale_rejected`: invoke with `--owner-override ""` → exit 2 with `rationale must be non-empty`.

  AC-10 archive runner tests are in T-A4.4 below (with archive runner implementation).

---

## T-A4 — Phase D archive runner (~1.5h)

- [ ] 4.1 Create `aria-orchestrator/acceptance/m6-archive-runner.py`:
  - Argparse: `--dry-run` (default True; explicit `--execute` required to mutate fs — safer default), `--owner-override "<rationale>"` (forwarded to readiness check).
  - Step 1: subprocess invoke `check-m6-release-readiness.py` with same `--owner-override` (if any). Exit 2 → archive runner refuses with `[ERROR] readiness verdict ABORT; archive refused`, exit 2.
  - Step 2: compute `today = datetime.now(timezone.utc).strftime('%Y-%m-%d')`.
  - Step 3: plan 4 moves: `openspec/changes/aria-2.0-m6-{cost-acceptance,e2e-resilience,docs,release-closeout}` → `openspec/archive/{today}-aria-2.0-m6-{...}/`.
  - Step 4: dry-run prints planned moves + exits 0 without mutation; execute proceeds.
  - Step 5: per-move execution with rollback tracking (per AD-M6-11):
    ```python
    completed_moves = []  # list of (orig_src, orig_dst) tuples
    try:
        for src, dst in planned_moves:
            src.rename(dst)
            completed_moves.append((src, dst))
    except OSError as e:
        # rollback completed moves
        for orig_src, orig_dst in reversed(completed_moves):
            try:
                orig_dst.rename(orig_src)
            except OSError:
                pass  # log to summary; cannot fix further
        raise SystemExit(f"[ERROR] archive mid-failure on move N; rollback attempted")
    ```
  - Step 6: append archive record to most-recent summary report (read last file in `.aria/m6-release-readiness/` by name sort).
  - Step 7: emit US-026 status diff recommendation (text only — per OOS-5 do NOT execute mutation; print recommended `requirements/us/US-026.md` edit for owner copy-paste).

- [ ] 4.2 US-026 status update helper (recommendation-only per OOS-5):
  - Function `recommend_us026_update()` returns markdown snippet:
    ```
    ## Owner Action: US-026 status update
    Recommended edit to docs/requirements/user-stories/US-026.md (frontmatter):
    - status: in_progress → done
    - completed_at: <today>
    Use /aria:progress-updater to apply.
    ```

- [ ] 4.3 Dry-run mode verification: by default `--dry-run` is true (must explicitly pass `--execute`); helps prevent accidental destructive run. Add prominent stderr banner on `--execute` invocation: `[WARN] --execute mode: 4 directories will be moved. Proceeding in 3 seconds (Ctrl-C to abort)...` + 3s sleep (escape hatch per `[[feedback_t15_owner_blocking_pattern]]`).

- [ ] 4.4 AC-10 pytest (atomicity):
  - `test_archive_PASS`: tmp_repo with 4 sibling+self dirs in `openspec/changes/`; mock readiness exit 0; invoke `--execute` → assert all 4 in `openspec/archive/{today}-*` AND `openspec/changes/aria-2.0-m6-*` empty.
  - `test_archive_ABORT_no_partial`: monkey-patch `pathlib.Path.rename` to raise `OSError` on 3rd call → assert first 2 moves rolled back to `changes/`, last 2 never attempted, exit code 2.
  - `test_archive_dry_run`: invoke without `--execute` → assert stdout shows 4 planned moves; filesystem unchanged.
  - `test_archive_refuses_on_ABORT_verdict`: mock readiness exit 2 → archive runner refuses, exit 2.
  - `test_archive_refuses_on_RED_without_override`: mock readiness exit 1 + no `--owner-override` → archive runner refuses (RED without override is hold).
  - `test_archive_proceeds_on_RED_with_override`: mock readiness exit 1 + `--owner-override "ack"` → archive runner proceeds.

---

## T-A5 — Docs (~1h)

- [ ] 5.1 Create `.aria/m6-release-readiness/README.md` explaining the artifact directory:
  - Purpose: stores timestamped readiness reports.
  - Naming: `{YYYY-MM-DDTHHMMSSZ}-report.md` UTC, no colons.
  - Retention: keep all (audit trail per `[[feedback_audit_driven_fix_conventions]]`). No auto-cleanup at Phase A.1 (revisit if directory grows >100 reports).
  - Cross-link: orchestrator script + Spec #4 proposal.
  - Header: this file is the only tracked file pre-execute besides `.gitkeep`.

- [ ] 5.2 Sibling Spec cross-ref enrichment: NO modifications to sibling Spec proposals (Approved + sealed). Instead, document the "Spec #4 is canonical pre-release gate orchestrator" relationship inline in CLAUDE.md (T-A5.3).
  - Verify Spec #1 `Successor` frontmatter already cites Spec #4 (line 682 confirmed in Phase A.1 read).
  - Verify Spec #2 `Successor` frontmatter cites Spec #4.
  - Verify Spec #3 `Successor` frontmatter cites Spec #4 (line 22 confirmed).
  - If any sibling frontmatter is missing Spec #4 backlink, raise as Phase A.2 audit finding (NOT fixed by Spec #4 — sibling-side concern).

- [ ] 5.3 Augment CLAUDE.md "版本发布检查清单" section:
  - Locate section header `### 版本发布检查清单` (currently lines ~315-345 per Phase A.1 read).
  - Add new sub-section after the existing checklist:
    ```markdown
    ### M6 v2.0.0 自动化预发版闸 (Spec #4)

    M6 ship 前必跑 `python3 aria-orchestrator/acceptance/check-m6-release-readiness.py` →
    exit 0 = ALL_PASS (可 ship) / exit 1 = RED (需 --owner-override) / exit 2 = ABORT (硬阻).
    自动化覆盖 8 个 gate (G-1..G-8): cost-acceptance / e2e-resilience / docs / secret-rotation-buffer /
    submodule-pointer-pre-release / Forgejo-Discussion-URL-liveness / 5-files-version-sync /
    archive-trigger-eligibility。详情见
    [openspec/changes/aria-2.0-m6-release-closeout/proposal.md](openspec/changes/aria-2.0-m6-release-closeout/proposal.md)。
    ```
  - Post-check: `grep -q "check-m6-release-readiness.py" CLAUDE.md` exits 0 after T-A5.3 ships.
  - Constraint per Spec #3 §Constraints (Rule #1-#9 FROZEN): this edit adds a NEW sub-section (additive); does NOT modify Rule #1-#9 text.

- [ ] 5.4 Orchestrator script header docstring:
  - First 30 lines of `check-m6-release-readiness.py` are docstring covering: purpose, 8 gates summary, exit code contract, CLI surface, summary report location, sibling Spec references. Self-documenting per `[[feedback_paper_fix_antipattern]]` (code + test + doc 三位一体).

---

## T-A6 — Memory candidate (deferred to Phase D, ~0.5h)

- [ ] 6.1 At Phase D close (post-merge, post-archive), evaluate whether pre-release orchestrator gate pattern proved useful enough to write as a reusable memory entry. Candidate filename: `feedback_pre_release_orchestrator_gate_pattern.md`. Per `[[project_meta_repo_pattern]]` memory conventions:
  - Title: ≤80 chars
  - Body: ≤24KB cumulative budget across all entries (check via `wc -c memory/*.md`)
  - Triggers: when a future Spec needs cross-cutting release gates aggregated from sibling Specs.
  - Source: this Spec #4 design + Phase B implementation evidence.
  - Decision (write OR skip): owner-confirmed at Phase D close. Phase A.1 default: WRITE (pattern is novel for Aria and likely reusable for M7+ release closeouts).
  - Write target: `/home/dev/.claude/projects/-home-dev-Aria/memory/feedback_pre_release_orchestrator_gate_pattern.md` + index entry in MEMORY.md.

- [ ] 6.2 Phase D Spec archive triggered via T-A4 archive runner with `--execute`. After archive, this Spec moves to `openspec/archive/{YYYY-MM-DD}-aria-2.0-m6-release-closeout/`. M6 closes. US-026 status update is owner-action per OOS-5.

---

## Sequencing summary

```
Phase A.1 (Spec drafting)               2026-05-25  ← THIS COMMIT
    │
Phase A.2 (multi-agent audit)           2026-05-26..27  (parallel with sibling Phase B)
    │
Phase A.3 (agent allocation: backend-architect primary)
    │
─── HARD GATE: Sibling Spec #1+#2+#3 all complete Phase C.2 merge ───
    │
Phase B.1 (branch creation)
    │
Phase B.2 (T-A1..T-A5 implementation)   ~10h impl
    │
Phase C.1+C.2 (commit + PR merge with C.2.4 pre-merge gate per Rule #8)
    │
Phase D.1 (progress update — partial; full UPM mutation is OOS-5 owner action)
    │
Phase D.2 (archive runner --execute) ← uses Spec #4's own m6-archive-runner.py
    │
Phase D.3 (session handoff per Rule #9 if conditions met)
    │
M6 CLOSED
```

---

## Risk-mitigation checklist (Phase B kick)

Before T-A2.1 implementation begins, owner verifies (per `[[feedback_per_spec_assumption_recheck]]`):
- [ ] A-1: Spec #1 `validate-m6-handoff.py` exists + `--all` flag accepted (or fallback path documented)
- [ ] A-2: Spec #2 `check-m6-e2e-acceptance.py` exists + `--all` flag accepted
- [ ] A-3: Spec #3 TG-DOCS-A shipped to master (CLAUDE.md v2.0 + 3 state-checks probes)
- [ ] A-4: `aria/.claude-plugin/plugin.json` `version` parseable
- [ ] A-5: `forgejo` CLI wrapper on PATH

Any FAIL → Phase B kick HELD; owner escalation per `[[feedback_owner_invoked_convergence_loop]]`.

---

> **Phase A.1 task breakdown complete 2026-05-25.** ~25 tasks targeting ~10h impl. Ready for Phase A.2 audit. Audit may catch missed deps (e.g., `aria-orchestrator/tests/acceptance/` directory existence, pytest invocation pattern conformity to Spec #1/#2 test layout) — these are expected Phase A.2 R1 findings.
