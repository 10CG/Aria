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

- [ ] 1.3 Phase B kick verify probe (per `[[feedback_per_spec_assumption_recheck]]` + §Assumptions A-1..A-5): create a one-off script `aria-orchestrator/acceptance/m6-release-closeout-verify-assumptions.sh` (NOT committed; runs once at B-kick) that exercises all 5 assumptions: <!-- R1-fix C3 (owner Q3 lock): per-flag canonical verify, not aspirational `--all` -->
  - A-1: `python3 aria-orchestrator/docs/validate-m6-handoff.py --help 2>&1 | grep -qE -- '--check-abi-compat|--check-3-day-history|--check-cost-method-enum|--check-pricing-freshness'` (all 4 flags documented in sibling Spec #1 §AC-6/7/8)
  - A-2: `python3 aria-orchestrator/acceptance/check-m6-e2e-acceptance.py --help 2>&1 | grep -qE -- '--tg-a|--tg-b|--tg-c'` (3 TG flags per Spec #2)
  - A-3: `grep -q '\*\*版本\*\*: 2.0.0' CLAUDE.md && grep -qF 'm6-version-badge-match' .aria/state-checks.yaml && grep -qF 'm6-claude-md-version' .aria/state-checks.yaml && grep -qF 'm6-arch-doc-stale' .aria/state-checks.yaml`
  - A-4: `python3 -c "import json; print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])"`
  - A-5: `forgejo --help`

  Any failure → STOP, escalate to owner. Per `[[feedback_probe_first_scope_reframe]]`. Script is throwaway (delete after green run); evidence captured in Phase B opening commit message.

- [ ] 1.4 **NEW R1-fix C7 + owner Q1 lock 2026-05-25**: pytest scaffolding + main /VERSION reconcile (~0.3h):
  - **Pytest dir setup** (per C-qa-4 fix): create `aria-orchestrator/tests/__init__.py` + `aria-orchestrator/tests/acceptance/__init__.py` (both empty). Verify pytest discovery: `pytest --collect-only aria-orchestrator/tests/acceptance/ 2>&1 | head -5` returns "no tests collected" (not "ERROR collecting"). NO `pytest.ini` change required (existing `aria-orchestrator/` test configuration covers this path; if not, propose at audit).
  - **Main /VERSION reconcile** (per C-cr-3 + owner Q1 lock): main repo `/VERSION` plugin row is currently STALE — `aria (子模块) | v1.23.1` (verified 2026-05-25) while plugin.json SoT is v1.27.0. Update the row to current SoT BEFORE Phase B G-7 testing:
    ```bash
    SOT_VERSION=$(python3 -c "import json; print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])")
    # Edit /VERSION: replace "aria (子模块) | v1.23.1 | ..." with "aria (子模块) | v${SOT_VERSION} | ..."
    # Verify post-edit: grep -E "aria \(子模块\)\s*\|\s*v${SOT_VERSION}" /VERSION
    ```
  - Commit message: `chore(m6-release-closeout): scaffold pytest dirs + reconcile main /VERSION plugin row to v1.27.0 (T-A1.4)`. Per `[[feedback_plugin_version_drift_multiple_sources]]` — pre-empts G-7 ABORT day-1 of Phase B.

---

## T-A2 — Orchestrator script (~3h)

<!-- Per §What A + §How diagram: G-1..G-8 sequential, three-state verdict, summary report -->

- [ ] 2.1 Create skeleton `aria-orchestrator/acceptance/check-m6-release-readiness.py`:
  - Python 3.9+ stdlib only (no PyYAML / requests / etc).
  - Argparse: `--owner-override "<rationale>"` (str, default None), `--dry-run` (bool, default False, propagated to summary-report write path), `--gates G-N[,G-M,...]` (optional gate selector for tests; default = run all 8; comma-separated string parsed at runtime; unrecognized gate name → argparse error exit per N-qa-8 fix).
  - **REPO_ROOT 2-variable contract** (R1-fix C1 + owner Q-ba-1 lock; previously off-by-one): <!-- DO NOT use the old `REPO_ROOT = HERE.parent` pattern — script lives at aria-orchestrator/acceptance/ which is TWO levels deep from main repo root (aria-orchestrator/ is itself a submodule per .gitmodules verified 2026-05-25) -->
    ```python
    import subprocess, sys
    from pathlib import Path
    HERE = Path(__file__).resolve().parent  # aria-orchestrator/acceptance/
    ORCH_ROOT = HERE.parent                 # aria-orchestrator/ (submodule root; for G-1/G-2 subprocess cwd)
    # MAIN_REPO_ROOT = main Aria repo (for G-3/G-5/G-7/G-8 cross-repo file reads):
    try:
        result = subprocess.run(['git', 'rev-parse', '--show-toplevel'],
                                capture_output=True, text=True, check=True, cwd=str(HERE))
        MAIN_REPO_ROOT = Path(result.stdout.strip())
        if not (MAIN_REPO_ROOT / 'CLAUDE.md').is_file():
            MAIN_REPO_ROOT = HERE.parent.parent  # fallback: assume submodule layout
        if not (MAIN_REPO_ROOT / 'CLAUDE.md').is_file():
            print(f'[ERROR] MAIN_REPO_ROOT resolution failed: {MAIN_REPO_ROOT} missing CLAUDE.md', file=sys.stderr)
            sys.exit(20)
    except subprocess.CalledProcessError:
        print('[ERROR] git unavailable; M6 release readiness cannot run', file=sys.stderr)
        sys.exit(20)
    ```
  - Top-level `main()` runs G-1..G-8 in sequence (or filtered subset per `--gates`), accumulates per-gate verdict list, aggregates, writes summary, exits 0/1/2 (or 3 on inconsistent-state per T-A4.5).
  - Stub each G-N as a function `gate_N(...)` returning `(verdict_str, message_str, stdout, stderr)` tuple where verdict ∈ {"PASS", "RED", "ABORT"}; stdout may be None for G-6 (suppressed per secret-hygiene policy).

- [ ] 2.2 Implement `gate_1_cost_acceptance()` (per-flag canonical per R1-fix C3 owner Q3 lock):
  - **Primary path** (sibling Spec #1 contract — 4 individual flags ship; `--all` NOT contracted):
    - Subprocess invoke 4 separate calls via `subprocess.run(..., capture_output=True, text=True, timeout=60, cwd=str(MAIN_REPO_ROOT))`:
      1. `python3 aria-orchestrator/docs/validate-m6-handoff.py --check-abi-compat`
      2. `python3 ... --check-3-day-history`
      3. `python3 ... --check-cost-method-enum`
      4. `python3 ... --check-pricing-freshness`
    - Aggregate: any returncode 2 → ABORT; any returncode 1 (no 2) → RED; all 0 → PASS.
    - Each unexpected exit (≥3) → ABORT with `unexpected exit code N from <flag>`.
  - **Optional fast-path** (if sibling later ships `--all`): probe `validate-m6-handoff.py --help 2>&1 | grep -qE -- '--all'`; if yes, may invoke single `--all` instead. NO behavioral difference. NOT required for Phase B kick.
  - Capture stdout/stderr verbatim → summary report (all 4 outputs concatenated with `--- flag separator ---` headers).

- [ ] 2.3 Implement `gate_2_e2e_resilience()` (per-flag canonical per R1-fix C3 owner Q3 lock):
  - **Primary path** (sibling Spec #2 contract — 3 TG flags ship; `--all` NOT contracted):
    - Subprocess invoke 3 separate calls:
      1. `python3 aria-orchestrator/acceptance/check-m6-e2e-acceptance.py --tg-a`
      2. `python3 ... --tg-b`
      3. `python3 ... --tg-c`
    - **Explicit aggregation per I-ba-2/I-qa-6**: any returncode 2 → ABORT; any returncode 1 (no 2) → RED; all 0 → PASS.
    - Each unexpected exit (≥3) → ABORT with `unexpected exit code N from <flag>`.
  - **Optional fast-path** (if sibling later ships `--all`): same probe pattern as G-1. NO behavioral difference.
  - Capture stdout/stderr verbatim → summary report (3 outputs concatenated with `--- tg- separator ---` headers).

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

- [ ] 2.6 Implement `gate_5_submodule_pointer()` (R1-fix C5: enumerate ALL submodules unconditionally):
  - Enumerate submodules via `git config --file .gitmodules --get-regexp 'submodule\..*\.path'` (invoked with `cwd=str(MAIN_REPO_ROOT)`). Parse module-name + path pairs.
  - **Verified 2026-05-25**: `.gitmodules` declares exactly 3 submodules: `standards`, `aria`, `aria-orchestrator`. ALL 3 are processed unconditionally; NO in-tree special case (C5 fix — previous draft misread aria-orchestrator as in-tree, which silently skipped the most-likely-to-drift submodule).
  - For each submodule:
    - Main-repo pointer: `git ls-tree HEAD <path>` (cwd=MAIN_REPO_ROOT) → parse SHA (3rd column of single output line).
    - Detached HEAD check: `git -C <MAIN_REPO_ROOT>/<path> symbolic-ref HEAD 2>/dev/null` → if nonzero (returncode != 0), ABORT for this submodule with `[ABORT] G-5: <submodule> in detached HEAD state; checkout master before release`.
    - Submodule's remote HEAD: `git -C <MAIN_REPO_ROOT>/<path> ls-remote origin HEAD` → parse SHA (1st column).
    - Pointer match remote HEAD → PASS; mismatch → ABORT with both SHAs printed in `[ABORT] G-5: <submodule> pointer <stale-sha> != remote master <fresh-sha>`.
  - Aggregate: any submodule ABORT → gate ABORT; all PASS → gate PASS.
  - **Offline fallback (single mechanism per R1-fix I-ba-4/I3)**: if `ls-remote` raises subprocess error (network failure), emit `[RED] G-5: <submodule> remote unreachable; manual verify required`. RED not ABORT — allows offline ship paths with owner-override. (Removed earlier `--use-local-master` CLI flag idea — automatic detection is simpler and sufficient.)

- [ ] 2.7 Implement `gate_6_forgejo_discussion_url()`:
  - Read `<MAIN_REPO_ROOT>/docs/release-notes-v2.0.0.md` (per Spec #3 §A.3).
  - Locate "Forgejo Discussion FAQ" section heading via regex `^#+\s+.*Forgejo Discussion FAQ` (R1-fix I-cr-3: loose heading-level — Spec #3 §A.3 does not pin to `##`; could be `###` or `####` depending on parent doc structure). If section missing → RED with `Forgejo Discussion FAQ section absent`.
  - Within FAQ section, extract first URL matching `https://forgejo\.10cg\.pub/\S+` regex.
  - If no URL → RED with `Forgejo Discussion URL not yet posted in release notes; owner action` (R1-fix I-cr-3: this is the EXPECTED v2.0.0 verdict; canonical ship path uses `--owner-override "FAQ URL pending owner post"` for exit 0).
  - If URL found: derive Forgejo path (strip `https://forgejo.10cg.pub`) → subprocess `forgejo GET <path>` capture exit code via `subprocess.run(..., capture_output=True, text=True)`.
  - **Stdout suppression** (R1-fix C6/I-ba-6/C-qa-5): `forgejo` wrapper stdout may contain auth headers (Authorization / Cookie / cf-access-jwt-assertion); the gate function returns `stdout=None` (suppressed) and ONLY captures stderr for summary report. Per `[[feedback_secrets_never_in_conversation]]` + `[[feedback_nomad_inspect_secret_leak]]`. NEVER log stdout to `.aria/m6-release-readiness/*.md` (which is git-tracked).
  - Exit 0 → PASS; nonzero → RED with stderr captured.
  - If `forgejo` CLI absent (`FileNotFoundError`): RED with `forgejo CLI unavailable; manual URL check required, paste exit code into summary`.

- [ ] 2.8 Implement `gate_7_six_surfaces_version_sync()` (R1-fix C2/I-cr-4: regexes corrected for actual Chinese Markdown blockquote formats verified 2026-05-25; clarified as 6 surfaces):
  - SoT read: `MAIN_REPO_ROOT / 'aria/.claude-plugin/plugin.json'` → `json.load(...)['version']` → save as `sot_version`. On parse failure (FileNotFoundError / json.JSONDecodeError) → ABORT with `SoT plugin.json missing OR unparseable; cannot derive expected version`.
  - Derived reads (each returns extracted version string OR `None` on parse failure):
    1. `aria/.claude-plugin/marketplace.json`: top-level `version` + `plugins[0]['version']` (BOTH must match SoT — verify each independently).
    2. `aria/VERSION`: regex `^>\s*\*\*版本\*\*:\s*(\d+\.\d+\.\d+)` first match. (Verified 2026-05-25: actual format is `> **版本**: 1.27.0` — Chinese Markdown blockquote, NOT YAML.)
    3. `aria/CHANGELOG.md`: regex `^##\s+\[(\d+\.\d+\.\d+)\]` first match. (Verified format: `## [1.27.0] - 2026-05-24`.)
    4. `aria/README.md`: regex `^>\s*\*\*Version\*\*:\s*v?(\d+\.\d+\.\d+)` first match. (Verified 2026-05-25: actual format is `> **Version**: 1.27.0 | **Released**: ...` — English in Markdown blockquote.)
    5. `MAIN_REPO_ROOT / 'VERSION'` (main project root, "6th surface"): regex `aria \(子模块\)\s*\|\s*v?(\d+\.\d+\.\d+)` first match. (T-A1.4 pre-reconciles this row to current SoT before Phase B G-7 testing — see C-cr-3 fix.)
  - All 5 derived strings (#1-5) == `sot_version` → PASS. Any mismatch → ABORT with EXPLICIT per-file diff listing ALL drifting files (NOT just the first):
    ```
    [ABORT] G-7: drift detected (SoT plugin.json=2.0.0):
      aria/CHANGELOG.md=1.27.0 (drift)
      aria/README.md=1.27.0 (drift)
      VERSION=v1.27.0 (drift)
    ```
  - Any parse failure (None return) → ABORT (cannot ship with unparseable version file).

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

- [ ] 2.11 Implement summary report writer (R1-fix C6/I-ba-6: explicit per-gate capture rules — G-6 stderr-only):
  - Filename: `MAIN_REPO_ROOT / '.aria/m6-release-readiness' / f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')}-report.md"`.
  - Idempotent: each invocation writes NEW file (NEVER overwrites). Directory accumulates trail.
  - **Per-gate capture rule** (CRITICAL — security):
    - G-1, G-2, G-3, G-4, G-5, G-7, G-8: capture BOTH stdout AND stderr.
    - G-6: capture **stderr ONLY** (stdout suppressed at gate-function level — `forgejo` wrapper stdout may contain auth headers per `[[feedback_nomad_inspect_secret_leak]]`). Report writer MUST handle `stdout=None` gracefully and emit `<!-- G-6 stdout: omitted (auth-header leak risk per Rule #7) -->` comment placeholder in the rendered Markdown.
  - Content sections: `# M6 Release Readiness Report — {ts}`, `## Invocation`, `## Per-Gate Verdicts` (G-1..G-8 each with captured stream(s) per rule above), `## Aggregate Verdict`, `## Owner Override` (if used; includes verbatim rationale + timestamp).
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

- [ ] 3.4 AC-3 — G-4 secret rotation buffer (6 boundary + edge tests; R1-fix I1 unified on `--gates G-4` selector):
  - All tests use `--gates G-4` selector to isolate G-4 from other gates (orchestrator skips G-1..G-3/G-5..G-8). Test fixture uses `mock_sibling_scripts_fixture` for completeness even though G-4 doesn't invoke siblings.
  - `test_G4_PASS_at_21d`: `M6_RELEASE_TODAY_OVERRIDE=2026-07-12` + `--gates G-4` → exit 0 with `[PASS] G-4: secret rotation buffer 21d`.
  - `test_G4_PASS_above_21d`: `M6_RELEASE_TODAY_OVERRIDE=2026-07-01` + `--gates G-4` → exit 0.
  - `test_G4_RED_at_20d`: `M6_RELEASE_TODAY_OVERRIDE=2026-07-13` + `--gates G-4` → exit 1.
  - `test_G4_RED_at_14d`: `M6_RELEASE_TODAY_OVERRIDE=2026-07-19` + `--gates G-4` → exit 1.
  - `test_G4_ABORT_at_13d`: `M6_RELEASE_TODAY_OVERRIDE=2026-07-20` + `--gates G-4` → exit 2.
  - `test_G4_ABORT_cap_day_itself`: `M6_RELEASE_TODAY_OVERRIDE=2026-08-02` + `--gates G-4` → exit 2 with `[ABORT] G-4: secret rotation buffer 0d` (NOT "cap exceeded by 0 days" — buffer==0 message format per R1-fix N-qa-2).
  - `test_G4_ABORT_past_cap`: `M6_RELEASE_TODAY_OVERRIDE=2026-08-10` + `--gates G-4` → exit 2 with `cap exceeded by 8 days`.

- [ ] 3.5 AC-4 — G-5 submodule pointer (4 scenarios; R1-fix I-qa-4 explicit fixture construction):
  - **Fixture construction** (per `[[feedback_test_mock_pattern_hides_prod_bug]]`): construct synthetic submodule via `tempfile.TemporaryDirectory()` + sequence:
    ```bash
    git init --bare /tmp/T/origin-sub.git              # bare repo as "origin"
    git clone /tmp/T/origin-sub.git /tmp/T/sub-clone   # working clone for commits
    cd /tmp/T/sub-clone && git commit --allow-empty -m "M1" && git push origin master
    cd /tmp/T/main-repo && git init && git submodule add file:///tmp/T/origin-sub.git sub
    ```
    This avoids the mock-return-shape pitfall (`ls-remote` returning real 40-char hex SHA vs empty string).
  - `test_G5_PASS_aligned`: tmp_repo with submodule pointer = remote HEAD → exit 0 with `[PASS] G-5: <submodule>`.
  - `test_G5_ABORT_misaligned`: tmp_repo with stale pointer (commit M2 pushed to bare origin AFTER main repo pointed at M1) → exit 2 with explicit SHA diff `<stale-sha-M1> != remote master <fresh-sha-M2>`.
  - `test_G5_ABORT_detached`: submodule checked out at SHA directly (not on branch) → `symbolic-ref HEAD` returns non-zero → exit 2 with `detached HEAD state` message.
  - `test_G5_RED_offline`: mock `subprocess.run` for `ls-remote` to raise `CalledProcessError` (simulates network failure) → exit 1 RED with `remote unreachable`. (Previously Optional per draft; promoted to required per R1-fix I-ba-4.)

- [ ] 3.6 AC-5 — G-6 Forgejo Discussion URL (3 scenarios + reframed meta-test):
  - `test_G6_PASS_url_200`: tmp_repo with release-notes containing valid placeholder URL `https://forgejo.10cg.pub/10CG/Aria/issues/999` + mock `subprocess.run` returns `CompletedProcess(returncode=0, stdout='{"id":999,...}', stderr='')` → PASS. Assert summary report contains the empty stderr but NOT stdout (per G-6 stderr-only capture rule).
  - `test_G6_RED_url_404`: same URL + mock returns `CompletedProcess(returncode=22, stdout='', stderr='HTTP/1.1 404')` → RED.
  - `test_G6_RED_no_url`: release-notes missing FAQ URL → RED `not yet posted`.
  - **Secret-hygiene meta-tests** per `[[feedback_secrets_never_in_conversation]]` (R1-fix I-qa-2 reframed — Forgejo PATs have no unique prefix, so old regex was tautological):
    - `test_G6_no_pat_env_var_refs`: scan all fixture test files; assert NONE reference env var names known to carry credentials: `for env_name in ['FORGEJO_TOKEN', 'FORGEJO_PAT', 'ARIA_PAT', 'GH_TOKEN', 'GITHUB_TOKEN']: assert env_name not in open(fixture_file).read()`.
    - `test_G6_forgejo_subprocess_always_mocked`: assert `subprocess.run` is `unittest.mock.MagicMock` instance during ALL G-6 test executions (never live call to `forgejo` wrapper).
    - `test_G6_report_excludes_stdout`: invoke `test_G6_PASS_url_200` then assert generated summary report does NOT contain the mocked stdout string (e.g., `'{"id":999,...}'`); MUST contain stderr-redacted placeholder comment.

- [ ] 3.7 AC-6 — G-7 6-surfaces SemVer (5 scenarios; R1-fix I-qa-1 promoted optional + added 2 more):
  - `test_G7_PASS_all_match`: tmp_repo fixture with all 6 surfaces showing `2.0.0` → PASS.
  - `test_G7_ABORT_changelog_stale`: plugin.json=`2.0.0`, CHANGELOG.md top entry=`1.27.0` → ABORT with `drift detected (CHANGELOG.md=1.27.0 != SoT=2.0.0)`.
  - `test_G7_ABORT_marketplace_plugins0_stale` (promoted from Optional per R1-fix I-qa-1): top-level marketplace.json version=`2.0.0` but `plugins[0]['version']`=`1.27.0` → ABORT (verifies nested-path correctness — independent dict-key reads).
  - `test_G7_ABORT_plugin_json_missing`: fixture without `aria/.claude-plugin/plugin.json` (or with corrupt JSON) → ABORT with `SoT plugin.json missing OR unparseable`.
  - `test_G7_ABORT_multi_stale`: fixture where CHANGELOG.md + README.md + main `/VERSION` are ALL stale (3 surfaces drifted) → ABORT message must list ALL 3 stale files (NOT just the first found).

- [ ] 3.8 AC-7 — G-8 archive trigger ordering (2 scenarios):
  - `test_G8_PASS_all_active`: tmp_repo with all 3 sibling dirs in `openspec/changes/`, none in `openspec/archive/` → PASS.
  - `test_G8_ABORT_prearchived`: tmp_repo with `cost-acceptance` only in `openspec/archive/2026-05-30-aria-2.0-m6-cost-acceptance/` → ABORT.

- [ ] 3.9 AC-8 — Summary report write idempotency:
  - `test_report_written_on_first_run`: invoke orchestrator → assert 1 `.md` file appears in `.aria/m6-release-readiness/`.
  - `test_report_repeat_run_appends`: invoke twice (with `time.sleep(1)` between) → assert 2 distinct `.md` files (no overwrite).
  - `test_report_dry_run_no_write`: invoke with `--dry-run` → assert 0 files written + stdout shows intended filename.

- [ ] 3.10 AC-9 — Owner override (4 scenarios; R1-fix N-qa-4 added whitespace):
  - `test_override_accepted_on_RED`: fixture forces G-N to RED → invoke with `--owner-override "ack: known"` → exit 0; assert summary contains rationale verbatim.
  - `test_override_rejected_on_ABORT`: fixture forces G-N to ABORT → invoke with `--owner-override "..."` → exit 2; stderr contains `--owner-override rejected: ABORT verdict has no override path`.
  - `test_override_empty_rationale_rejected`: invoke with `--owner-override ""` → exit 2 with `rationale must be non-empty`.
  - `test_override_whitespace_only_rejected` (R1-fix N-qa-4): invoke with `--owner-override "   "` (3 spaces) → exit 2 with `rationale must be non-empty (whitespace-only is treated as empty)`. Implementation MUST use `rationale.strip()` in the non-empty check.

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
  - **Test escape hatch** (R1-fix N-qa-7 / N-ba-3): `if not os.environ.get('M6_ARCHIVE_NO_COUNTDOWN'): time.sleep(3)` — pytest fixtures set `M6_ARCHIVE_NO_COUNTDOWN=1` to skip the 3s sleep (saves ~18s across 6 test cases). Document the env var in the help text (`--help` output).

- [ ] 4.4 AC-10 pytest (atomicity + idempotency + double-rollback per R1-fix I-qa-3):
  - `test_archive_PASS`: tmp_repo with 4 sibling+self dirs in `openspec/changes/`; mock readiness exit 0; invoke `--execute` → assert all 4 in `openspec/archive/{today}-*` AND `openspec/changes/aria-2.0-m6-*` empty.
  - `test_archive_ABORT_no_partial`: monkey-patch `pathlib.Path.rename` to raise `OSError` on 3rd call → assert first 2 moves rolled back to `changes/`, last 2 never attempted, exit code 2.
  - `test_archive_IDEMPOTENT` (NEW R1-fix I-qa-3): invoke `--execute` once (succeeds), then invoke `--execute` again on the already-archived state → second invocation detects ALL 4 destinations already exist; exits non-zero (exit code 3 or distinct) with `[ERROR] N of 4 destinations already exist; archive runner refuses to overwrite (already archived?)`. NO mutation; NO silent rename; NO unhandled exception.
  - `test_archive_ROLLBACK_also_fails` (NEW R1-fix I-qa-3): monkey-patch `pathlib.Path.rename` to raise `OSError` on forward 3rd call AND also on rollback rename (double-mock pattern) → script exits with exit code 3 (`[ERROR] inconsistent state — N moves committed, K rollbacks failed; manual intervention required`) instead of unhandled exception crash. Inconsistent-state final state documented in summary report (post-mortem aid).
  - `test_archive_dry_run`: invoke without `--execute` (default = dry-run per R1-fix I-cr-6) → assert stdout shows 4 planned moves; filesystem unchanged; NO summary report file written.
  - `test_archive_refuses_on_ABORT_verdict`: mock readiness exit 2 → archive runner refuses, exit 2.
  - `test_archive_refuses_on_RED_without_override`: mock readiness exit 1 + no `--owner-override` → archive runner refuses (RED without override is hold).
  - `test_archive_proceeds_on_RED_with_override`: mock readiness exit 1 + `--owner-override "ack"` → archive runner forwards override + proceeds.

- [ ] 4.5 Exit code contract documentation in archive runner:
  - Add module docstring section `EXIT CODES`:
    - 0: ALL_PASS (archive succeeded) OR dry-run (no mutation)
    - 1: (reserved — not used by archive runner; readiness is the RED authority)
    - 2: archive refused (readiness ABORT, RED-without-override, or already-archived destinations)
    - 3: **inconsistent state** (mid-move OSError + rollback ALSO failed); manual intervention required — see most-recent summary report for partial-state details.
    - 20: hard pre-condition failure (git unavailable / MAIN_REPO_ROOT resolution failure — same contract as orchestrator).

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
