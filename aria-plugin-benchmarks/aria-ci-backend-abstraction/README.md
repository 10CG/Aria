# aria-ci-backend-abstraction — Rule #6 Substitute Fixture

> **Spec**: [`aria-ci-backend-abstraction`](../../openspec/changes/aria-ci-backend-abstraction/proposal.md)
> **Ship target**: aria-plugin v1.31.0
> **Type**: Deterministic / structural Skill (per [[feedback_deterministic_structural_skill_rule6_substitute]])
> **Rule #6 substitute**: structural fixture + 41 new unit tests + dual-path dogfood smoke (NOT `/skill-creator benchmark` AB test — see §Why not AB)

---

## Why not /skill-creator benchmark AB?

Per memory [[feedback_deterministic_structural_skill_rule6_substitute]] + [[feedback_rule6_framing_differs_by_skill_type]]:

This Spec refactors **deterministic Python code** (pre_merge_gate.py + new ci_backends/ package). The "Skill" being benchmarked would be the CI backend resolution + query logic — pure Python functions with deterministic input/output. There is **no LLM prompt variable** between `with_skill` and `without_skill` to AB-test:

- AetherBackend.probe() is `shutil.which("aether")` — same answer every time
- gate_check() returns deterministic verdict from `(pr_status, in_flight_runs)` mapping
- _normalize_config() is a pure function over config dict

`/skill-creator benchmark` would yield delta = 0 because there's no AI capability variance to measure.

**Substitute = behavior preservation + structural correctness**:
- **Behavior preservation** (Hard Constraint #1): All 21 existing test methods PASS after refactor (Aether backend behavior byte-for-byte identical to v1.30.0)
- **Structural correctness** (Hard Constraints #4 #7 #8 #9 #10 #11): 41 new unit tests verify ABC contract / NIE-propagation / static registry / alias precedence / probe cache isolation
- **Dogfood smoke** (real-machine evidence below): probe + gate_check + NIE abort verified on actual development machine

---

## AC behavior table (12 rows, maps proposal §AC to test)

| AC | Hard Constraint | Test reference | Expected behavior |
|----|----------------|---------------|-------------------|
| **AC-1.1** | #1 (Aether zero change) | test_pre_merge_gate.py — all 21 rewritten methods | 21/21 PASS |
| **AC-1.2** | #1 | dogfood smoke 3 (below) | `primitive_used: "aether-ci-cli"`, schema equivalent to v1.30.0 |
| **AC-1.3** | #1 | dogfood smoke 3 (below) | gate_check returns same verdict as v1.30.0 baseline |
| **AC-2.2** | #4 (operable NIE msg) | test_ci_backends.py::TestGitHubActionsBackendStub::test_query_*_raises_nie_with_locked_message | NIE message contains "GHA backend probe succeeded but" + "PR welcome" |
| **AC-2.3** | #7 (NIE propagation) | test_pre_merge_gate.py::TestGHAStubAbortNotSkip::test_gha_*_nie_propagates | gate_check raises NIE, does NOT route to fallback |
| **AC-2.4 + 2.5** | #7 + #4 | test_pre_merge_gate.py::TestGHAStubAbortNotSkip::test_gha_query_pr_ci_nie_propagates | assertRaises NIE + assertIn message body |
| **AC-3.1/3.2** | #3 (alias works) | test_pre_merge_gate.py::TestAliasKeyPath | Old keys translated + deprecation warning |
| **AC-3.3 + 3.5** | #9 (new wins) | test_pre_merge_gate.py::TestBothKeysPresentNewWins | new wins + both_keys_present warning |
| **AC-3.4** | #3 (no silent rot) | test_pre_merge_gate.py::TestAliasKeyPath | warning message body assertion |
| **AC-4.1 to 4.4** | #8 (static registry) | test_ci_backends.py::TestRegistry + test_pre_merge_gate.py::TestBackendRegistry | BACKENDS list order = Aether-first; no decorator |
| **AC-4.5** | #8 (`[]` disable) | test_pre_merge_gate.py::TestBackendRegistry::test_explicit_empty_ci_backends_disables | resolve_ci_backend({'ci_backends': []}) returns None |
| **AC-5.1 to 5.4** | (contract) | test_ci_backends.py::TestCIStatus + TestInFlightStatus + TestCIBackendABC | dataclass attribute access; ABC enforce |
| **AC-6.4** | #5 (standards zero touch) | `git diff --stat standards/` | empty diff |
| **AC-7.4** | (zero regression) | `python3 -m unittest discover` aria/skills/state-scanner | 631/631 PASS |
| **AC-8.1** | (5+1 SOT consistency) | grep `1.31.0` across SOT files | count = 6 unique appearances |

---

## Structural fixture: adding a new backend

Sample `mock_ci_backend.py` showing the pattern (subclass `CIBackend` + add to `BACKENDS` list — no decorator):

```python
# aria/skills/phase-c-integrator/scripts/ci_backends/my_new_backend.py
from typing import ClassVar
from .base import CIBackend, CIStatus, InFlightStatus


class MyNewBackend(CIBackend):
    name: ClassVar[str] = "my-new-ci"

    @classmethod
    def probe(cls) -> bool:
        # Cheap detection (shutil.which / config file check / auth check)
        return False  # stub default

    def query_pr_ci(self, pr_ref: str) -> CIStatus:
        # Real impl: call CI API, translate JSON → CIStatus dataclass
        # Stub: raise NotImplementedError with operable message per Hard Constraint #4
        raise NotImplementedError(
            "MyNewBackend probe succeeded but query_pr_ci not implemented; "
            "PR welcome (see SKILL.md §C.2.4.X). Per Hard Constraint #7, "
            "gate_check() will abort here, NOT skip — "
            "set ci_backends: [] in .aria/config.json to explicitly disable."
        )

    def query_branch_in_flight(self, branch: str) -> InFlightStatus:
        raise NotImplementedError("...similar message...")
```

Then in `ci_backends/__init__.py`:

```python
from .my_new_backend import MyNewBackend
BACKENDS: list[type[CIBackend]] = [AetherBackend, GitHubActionsBackend, MyNewBackend]
```

That's it. **No `@register` decorator. No setuptools entry_points. No plugin discovery complexity** (Hard Constraint #8).

---

## Unit test breakdown (62 total — 21 rewritten + 41 new)

### test_pre_merge_gate.py (37 tests)

| Class | Methods | Type |
|-------|---------|------|
| ComputeVerdictTests | 4 | Rewritten (extended `compute_verdict` signature per Hard #10) |
| TranslateInFlightRunTests | 3 | Rewritten (target moved to `AetherBackend._translate_in_flight_run`) |
| GateCheckTests | 7 | Rewritten (mock target collapse to `AetherBackend` methods) |
| FallbackTests | 3 | Rewritten (key `no_aether_fallback` → `no_ci_fallback`) |
| NormalizePrCiStatusTests | 4 | Rewritten (target moved to `AetherBackend._normalize_pr_ci_status`) |
| **TestGHAStubAbortNotSkip** | **3** | NEW (Hard Constraint #7 + AC-2.5) |
| **TestAliasKeyPath** | **3** | NEW (Hard Constraint #3 + AC-3.4) |
| **TestBothKeysPresentNewWins** | **1** | NEW (Hard Constraint #9 + AC-3.5) |
| **TestBackendRegistry** | **5** | NEW (Hard Constraint #8 + AC-4) |
| **TestNormalizeConfigSequencing** | **2** | NEW (Hard Constraint #9 sequencing verification) |
| **TestProbeCacheIsolation** | **2** | NEW (Hard Constraint #11 Option B + AC-7) |

**Subtotal**: 21 rewritten + 16 new = **37 tests**

### test_ci_backends.py (25 tests, NEW per Task 1.7)

| Class | Methods | Coverage |
|-------|---------|----------|
| TestCIStatus | 2 | base.py CIStatus dataclass fields + attribute access (AC-5.4) |
| TestInFlightStatus | 2 | base.py InFlightStatus + has_runs property |
| TestCIBackendABC | 3 | ABC abstract enforce + missing-method TypeError + default precheck |
| TestAetherBackendProbe | 3 | aether.py probe() — binary present / absent / config-only |
| TestAetherBackendQuery | 3 | aether.py query_pr_ci + query_branch_in_flight + AetherQueryError |
| TestAetherBackendPrecheck | 2 | aether.py precheck() — --in-flight flag verification |
| TestGitHubActionsBackendStub | 5 | github_actions.py — probe gh auth + query NIE message body |
| TestRegistry | 5 | __init__.py — BACKENDS order + no decorator + cached_probe + reset |

**Subtotal**: 25 tests, all NEW

### Grand total

**62 tests** (well above AC-7.2 `≥27` requirement).

Plus 631 state-scanner tests unchanged (zero regression).

---

## Dual-path dogfood smoke evidence

Run from `/home/dev/Aria` (Aria self-dogfood machine, 2026-05-28T~13:30 UTC).

### Smoke 1: AetherBackend.probe() real-machine

```bash
$ python3 -c "import sys; sys.path.insert(0, 'aria/skills/phase-c-integrator/scripts'); \
              from ci_backends.aether import AetherBackend; print(AetherBackend.probe())"
True
```

**Verifies**: AC-1.2 (Aria self has aether installed, probe returns True, behavior matches v1.30.0).

### Smoke 2: GitHubActionsBackend.probe() real-machine

```bash
$ python3 -c "import sys; sys.path.insert(0, 'aria/skills/phase-c-integrator/scripts'); \
              from ci_backends.github_actions import GitHubActionsBackend; print(GitHubActionsBackend.probe())"
False
```

**Verifies**: `gh` CLI either not installed OR not authed. GHA stub backend correctly returns False (won't be selected unless explicitly configured — proves Aether-first precedence is safe).

### Smoke 3: CLI invocation — v1.30.0 baseline-equivalent

```bash
$ python3 aria/skills/phase-c-integrator/scripts/pre_merge_gate.py \
    --pr-branch feature/ci-backend-abstraction --main-branch master
{"verdict": "wait", "pr_ci_status": "pending", "in_flight_runs": [],
 "primitive_used": "aether-ci-cli", "primitive_version_sha": "f29abee",
 "raw_message": ""}
```

**Verifies**: AC-1.3 + AC-8 — CLI works, returns same JSON schema as v1.30.0, `primitive_used: "aether-ci-cli"` + `primitive_version_sha: "f29abee"` populated correctly. (Verdict is "wait" because PR doesn't have associated aether runs — this is the correct response for a hypothetical PR branch with no CI activity.)

### Smoke 4: Manual NIE abort verification (Hard Constraint #7)

```bash
$ python3 -c "
import sys; sys.path.insert(0, 'aria/skills/phase-c-integrator/scripts')
from pre_merge_gate import gate_check
from unittest.mock import patch
from ci_backends import AetherBackend, GitHubActionsBackend, reset_probe_cache
reset_probe_cache()
with patch.object(AetherBackend, 'probe', classmethod(lambda cls: False)), \
     patch.object(GitHubActionsBackend, 'probe', classmethod(lambda cls: True)):
    try:
        out = gate_check('test-branch')
        print('FAIL — should have raised NIE')
    except NotImplementedError as e:
        msg = str(e)
        print('NIE raised: OK')
        print('Message contains GHA backend probe succeeded but:', 'GHA backend probe succeeded but' in msg)
        print('Message contains PR welcome:', 'PR welcome' in msg)
"
NIE raised: OK
Message contains GHA backend probe succeeded but: True
Message contains PR welcome: True
```

**Verifies**: AC-2.3 + AC-2.5 + Hard Constraint #7 — when only GHA stub is probed True, gate_check raises NIE (does NOT catch and route to no_ci_fallback). Message body contains required strings preventing silent rot.

### Smoke 5: Alias deprecation warning

```bash
$ python3 -c "
import sys, warnings; sys.path.insert(0, 'aria/skills/phase-c-integrator/scripts')
from pre_merge_gate import _normalize_config
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always')
    cfg = _normalize_config({'no_aether_fallback': 'abort'})
    print('Translated:', cfg)
    print('Warning category:', w[0].category.__name__ if w else 'NONE')
    print('Warning message:', str(w[0].message) if w else 'NONE')
"
Translated: {'no_ci_fallback': 'abort'}
Warning category: DeprecationWarning
Warning message: `no_aether_fallback` is deprecated; use `no_ci_fallback`; will be removed in v2.0
```

**Verifies**: AC-3.1 + AC-3.4 — old key translated to new + DeprecationWarning with exact expected message body.

---

## How this substitutes Rule #6

Per CLAUDE.md Rule #6: "Skill 基准测试必须使用 `/skill-creator`" — but with the exception clause per memory [[feedback_deterministic_structural_skill_rule6_substitute]]:

> "collector/parser/detector 类 deterministic Skill Rule #6 substitute = structural fixture + unit tests + dogfood"

This Spec is exactly that:
- **Structural fixture** ← this README + `MyNewBackend` sample above
- **Unit tests** ← 62 tests (37 in test_pre_merge_gate.py + 25 in test_ci_backends.py), all `OK`
- **Dogfood smoke** ← 5 real-machine evidence runs (above)

`/skill-creator benchmark` would yield delta ≈ 0 (no AI capability variance to measure). Owner-acknowledged substitute path is the appropriate Rule #6 compliance for this Spec.

---

## References

- Spec: `openspec/changes/aria-ci-backend-abstraction/proposal.md` (660 lines)
- DEC: `.aria/decisions/2026-05-28-ci-backend-abstraction-brainstorm.md` (Q1-Q5 + 9 Hard Constraints)
- Audit reports: `.aria/audit-reports/post_spec-R1-*` + `post_spec-R2-*` (CONVERGED unanimous PASS_WITH_WARNINGS × 3)
- Sprint 1 predecessor (similar pattern): `aria-plugin-benchmarks/forgejo-hosts-parameterization/README.md` (v1.30.0 ship)
- Memory: [[feedback_deterministic_structural_skill_rule6_substitute]] + [[feedback_rule6_framing_differs_by_skill_type]]

---

**Created**: 2026-05-28
**Ship target**: aria-plugin v1.31.0
**Status**: ✅ All 5 dogfood smoke PASS + 62/62 unit tests PASS + 631/631 state-scanner zero regression
