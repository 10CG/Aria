# aria-ci-backend-abstraction — CI backend 抽象 + Aether 搬迁 + GHA stub (Sprint 2 boundary audit P0 C5+C6)

> **Level**: 3 (Full — `proposal.md` + `tasks.md`, cross-file impact: new `ci_backends/` package + `pre_merge_gate.py` refactor + `tests/` rewrite + CLAUDE.md + 2 SKILL.md files)
> **Status**: ✅ **Approved** (Rev1.1, 2026-05-28) — post_spec R1 REVISE × 2 + PASS_WITH_WARNINGS × 1 → Rev1 → **R2 PASS_WITH_WARNINGS × 3 unanimous CONVERGED** (per [[feedback_audit_convergence_patterns]] L3 effective convergence — agent withdrawal + verdict 改善 + 无振荡) + Rev1.1 polish for substance-converged R2 ba N-1 (query order paper-fix → corrected to ground truth main-first)
> **Rev1.1 polish** (R2 close-out, 2026-05-28):
>   - **R2 ba N-1 paper-fix correction**: §B.4 query order corrected from incorrect "PR-first then in-flight" (Rev1 paper-fix) to ground-truth-verified "main in-flight FIRST then PR CI SECOND" (matches `gate_check` L309-329). Hard Constraint #1 强制此顺序
>   - **R2 trivials acknowledged but deferred to Phase B implementation** (per ba "does not block Phase B" + qa "do not require a revision round"):tech N-1 SKILL.md ref count body drift / tech N-2 task 2.7 import re-coupling / qa partial AC-7.2 body distribution / qa minor `priority?` mention in §D.2 / qa minor 5.6 cd prefix — implementer will fix during T-docs + T-tests with no Spec rewrite needed
> **Rev1 changelog** (R1 post_spec audit fixes):
>   - **C-1 fix**: AC-2.4 add message body assertion (tech F-01) — `assertIn("GHA backend probe succeeded but", str(exc.value)) and assertIn("PR welcome", str(exc.value))`
>   - **3-agent CONVERGED `_compute_verdict`**: §B.4 重命名 `_compute_verdict` → `compute_verdict` (匹配现 ground truth L217 公共名) + extend signature to `(main_in_flight_runs: list[dict], pr_ci_status: str, backend_name: str) -> str` (加 backend_name 替代旧 hardcoded `"aether-ci-cli"` in `primitive_used` output field) — new Hard Constraint #10 locks
>   - **§A.2 responsibility table** added (ba c1d6a8e3): 9 rows mapping 8 functions + 4 constants in pre_merge_gate.py → aether.py vs stay
>   - **§A.4 `ci_backends: []` semantic lock** (ba b7e19f4a): `[]` = **explicit disable** (return None immediately, route to `no_ci_fallback`); missing/null = auto-detect via BACKENDS order — new AC-4.5
>   - **§B.2 `_translate_value` complete table** (tech F-02): 2 keys with value-shape mapping
>   - **AC-5.1 count fix** (ba F-05 + qa F-05 CONVERGED): "5 members: 2 ClassVar (`name`, `priority`) + 3 abstract (`probe`, `query_pr_ci`, `query_branch_in_flight`)";AND drop unused `priority` field (ba F-06 + qa F-06 CONVERGED) — BACKENDS list order is the explicit precedence
>   - **Hard Constraint #11**: probe cache strategy locked = **Option B** (module-level `_probe_cache: dict[type[CIBackend], bool]` + `reset_probe_cache()` helper); drop lru_cache (tech F-04 + ba minor)
>   - **§B.5 _no_aether_output rename verification**: Task 4.6 added — `grep -rn "_no_aether_output\|no_aether" aria/skills/phase-c-integrator/` returns 0 in code (md ok) post-rename (tech F-05)
>   - **§B.4 query order annotation** (Rev1.1 corrected per R2 ba N-1): main in-flight FIRST then PR CI SECOND — matches ground truth `gate_check` L309-329 verified;Hard Constraint #1 (Aether behavior zero change) 强制此顺序;originally R1 ba minor finding implied reversal but ground truth IS main-first;Rev1 wrote paper-fix wrongly, Rev1.1 corrects
>   - **Task 3.1-3.2 class split fix** (qa F-01): use ground truth 5 classes (ComputeVerdictTests 4 + TranslateInFlightRunTests 3 + GateCheckTests 7 + FallbackTests 3 + NormalizePrCiStatusTests 4 = 21);drop nonexistent "TestDetectAether"
>   - **AC-7.2 vs Task count reconciliation** (qa F-02): new Task 1.7 — create `tests/test_ci_backends.py` with ≥11 module-tests (base.py contract 4 + aether.py migrated 3 + github_actions.py stub 2 + registry 2) → 21 rewritten + 16 in test_pre_merge_gate.py new + 11 in test_ci_backends.py new = 48 total (well above AC-7.2 "≥27")
>   - **Task 5.5 dogfood command fix** (qa F-03): use `python3 aria/skills/phase-c-integrator/scripts/pre_merge_gate.py --pr-branch <branch>` (current CLI entry verified L368-380) + `cwd=<repo root>` annotation
>   - **Task 8.7 v1.29.0 race guard added** (tech F-06): `git fetch --all && grep "## \[1.29.0\]" aria/CHANGELOG.md` — abort if v1.29.0 entry written by sister (block-flip ship 应早于本 Spec ship)
>   - **Minor batch (10 items)**: SKILL.md ref count corrected 14 (was ~10);gate_check docstring updated to declare NIE-propagation contract;Out-of-Scope adds verdict-semantics fence;Rule #9 trigger explicit at session >4h OR cycle full;Phase D handoff template path locked;AC-7.3 dogfood NIE manual-verify command made concrete;test isolation Option B `reset_probe_cache()` signature locked
> **Change ID**: `aria-ci-backend-abstraction`
> **Decisions source**: [DEC 2026-05-28](../../../.aria/decisions/2026-05-28-ci-backend-abstraction-brainstorm.md) (Q1-Q5 owner-approved + R1 post_brainstorm audit PASS_WITH_WARNINGS × 3 unanimous, see §Audit findings in DEC)
> **Boundary audit source**: `.aria/notes/2026-05-27-boundary-audit-10cg-hardcode.md` §修复 2 (P0 items C5+C6)
> **Predecessor**: Sprint 1 `aria-forgejo-hosts-parameterization` (v1.30.0) shipped 2026-05-27 — same boundary-audit Sprint, different P0 items
> **Target version**: aria-plugin **v1.31.0** (v1.29.0 reserved for block-flip ship D+14 hard date 2026-06-07;v1.30.0 already shipped forgejo-hosts)
> **Ship target**: single cycle ~10-10.5h Phase B (revised from initial 8.5h per R1 audit M-1 substance-converged finding)
> **Risk class**: **Backward-compatible** (Aether behavior 100% preserved + soft alias for old config keys + new GHA backend is stub-only)

---

## Why

### Direct trigger

2026-05-27 boundary audit (Sprint 1 forgejo-hosts ship 同 session) 发现通用层 `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py:47-62` 硬编码假设唯一 CI primitive 是 **aether-ci-cli** (10CG 自研 CI 平台):

```python
DEFAULT_CONFIG = {
    "enabled": True,
    "primitive_preference": ["aether-ci-cli"],          # ← C5 hardcode
    "no_aether_fallback": "skip_with_warning",          # ← C5 + C6
    ...
}

def detect_aether() -> tuple[bool, str | None]:
    binary = shutil.which("aether")                     # ← Aether-only probe
    if binary:
        return True, binary
    config_yaml = os.path.expanduser("~/.aether/config.yaml")  # ← C6 hardcoded path
    ...
```

这违反 aria-fleet DEC D2 硬约束 "通用层禁止新增 10CG-specific hardcode" (per [[feedback_three_layer_universal_workspace_instance]]):
- 任意 aria-plugin 用户无 Aether (GHA / GitLab CI / Forgejo Actions / 自建 Jenkins) → Rule #8 pre-merge gate 必降级 `skip_with_warning` → 整个不可协商规则 #8 在非-Aether 环境下永久 vacuously satisfied
- 别人无法 fork aria-plugin 替换 Aether — 需在 `pre_merge_gate.py` 内部多处改 Aether-specific 假设

### Why now (Sprint 2 P0 第二项)

Per 2026-05-27 handoff §6 carry-forward S1 "C5+C6 CI backend abstraction (~8-12h L3 Spec)":
- **Sprint 1** (v1.30.0 forgejo-hosts) 已 ship — 顺势做 Sprint 2
- **不阻塞 M6** (sister terminal 在 M6 sub-Specs;本 Spec 触 phase-c-integrator,与 M6 文件零碰撞)
- **D+14 v1.29.0 block-flip ship (2026-06-07, today D-10) window** — 严守 D+14 期间正好做独立 scope 的 hygiene cycle
- **GHA stub 占位** = 后续 (v1.32.0+) GHA 真实现的最小投资:contract 设计是一次性决定,值得单独 ship 单独审计

### 当前 pre_merge_gate.py state (R1 audit 复核验证)

| 项 | 当前状态 | R1 audit verified |
|----|---------|------------------|
| LOC | 387 lines | tech-lead R1 |
| Test file LOC | 23 `mock.patch.object(gate, "detect_aether", ...)` 实测 (DEC 原写 "~10") | tech-lead M1 + backend-architect F-02 + qa F3 (3-agent substance convergence) |
| Mock targets per test | 3 stacked (`detect_aether` + `verify_aether_in_flight_flag` + `_query_aether`) | backend-architect F-02 |
| SKILL.md references | ~10 处含 `aether-ci-cli` / `aether ci status` / `no_aether_fallback` | tech-lead R1 |
| CLAUDE.md Rule #8 references | 4 处 (L432-444) | tech-lead R1 |
| `aria/skills/config-loader/SKILL.md` references | L183/L189 documents legacy keys | tech-lead M2 (audit memo missed) |
| `standards/` Rule #8 references | 3 conventions引用,**无** aether-specific 字面 (verified grep) | tech-lead R1 (DEC §Hard constraint #5 verified) |

### Why NOT bigger scope (explicit deferrals)

- **GHA real implementation** → next cycle (~4-6h L2, ship v1.32.0+):本 cycle 仅 stub + contract,GHA 实际 `gh run list --json` schema mapping + auth 集成是 mechanical fill-in,值得独立审计
- **GitLab CI / Forgejo Actions backends** → aria-fleet M7+ (per DEC D5 deferred timing)
- **GitProvider ABC** (类似抽象但 git-host-side) → aria-fleet M7+ 主线 (boundary audit memo S5)
- **DEFAULTS.json `forgejo.10cg.pub` legacy fallback deprecation** → M7+ (per Sprint 1 DEC D2 compliance discussion)
- **CHANGELOG v1.29.0 placeholder replacement** → block-flip ship day (2026-06-07) 时统一替换,本 cycle 不动

---

## What

### 5 Decisions (from [DEC 2026-05-28](../../../.aria/decisions/2026-05-28-ci-backend-abstraction-brainstorm.md))

| # | Decision | Selected | DEC anchor |
|---|----------|----------|-----------|
| Q1 | Ship shape | **(b) Contract + Aether full + GHA stub** | DEC §5 Q1 |
| Q2 | Backward compat | **(b) Soft alias + deprecation warning** | DEC §5 Q2 |
| Q3 | Auto-detect strategy | **(b) Config-first + probe fallback** | DEC §5 Q3 |
| Q4 | Contract surface | **(b) 双方法 + dataclass (`CIStatus` / `InFlightStatus`)** | DEC §5 Q4 |
| Q5 | Rule #8 wording | **(b) 通用化 + Aether 作默认示例** | DEC §5 Q5 |

### Deliverables (6 deliverables, A→F)

| # | Deliverable | Estimate | Key files |
|---|-------------|----------|-----------|
| **A** | New `ci_backends/` package | 3h | `aria/skills/phase-c-integrator/scripts/ci_backends/{__init__.py, base.py, aether.py, github_actions.py}` |
| **B** | `pre_merge_gate.py` refactor | 1h | `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py` (L30-70 config + L57-70 `detect_aether` + L240-260 `_no_aether_output` + L180-220 query 主流程) |
| **C** | Test rewrite (R1-revised) | **3-3.5h** | `aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py` + new test classes |
| **D** | Doc updates (R1-revised + config-loader added) | **1.25h** | `CLAUDE.md` Rule #8 L432-444 + `aria/skills/phase-c-integrator/SKILL.md` ~10 处 + `aria/skills/config-loader/SKILL.md` L183/L189 |
| **E** | Rule #6 substitute (R1-revised) | **1.5-2h** | `aria-plugin-benchmarks/aria-ci-backend-abstraction/` (structural fixture + 27+ unit tests + dual-path dogfood smoke) |
| **F** | 5+1 SOT v1.31.0 bump | 0.5h | `aria/.claude-plugin/{plugin.json, marketplace.json}` + `aria/VERSION` + `aria/CHANGELOG.md` + `aria/README.md` + `CLAUDE.md` plugin 版本字段 |

**Total Phase B**: **~10-10.5h** (revised from initial 8.5h per R1 audit M-1 + M-2 + m-8;still within boundary audit memo "~8-12h L3" range)

---

## Out of Scope

- ❌ GHA backend real implementation (deferred to v1.32.0+ next cycle)
- ❌ GitLab CI / Forgejo Actions backends (deferred to aria-fleet M7+)
- ❌ GitProvider ABC (aria-fleet M7+ 主线 scope)
- ❌ DEFAULTS.json `forgejo.10cg.pub` legacy deprecation (M7+)
- ❌ Feishu / notification backend abstraction (Sprint 3, separate cycle)
- ❌ `~/.aether/config.yaml` schema 修改 (本 Spec 仅参数化路径不动 schema)
- ❌ standards/ submodule 任何改动 (verified zero touch)
- ❌ aria-orchestrator submodule 任何改动 (Spec scope = aria-plugin only)

---

## Hard Constraints (9 total)

> **6 original from DEC §Hard constraints + 3 new from R1 audit**

### Original (from brainstorm Q1-Q5 sign-off)

1. **Aether 行为零变化** — 所有现 `test_pre_merge_gate.py` cases 必须 PASS (内部 mock target 改但 assertion 行为不变)
2. **Rule #8 mechanism 不可降级** — 文字通用化但 (a)+(b) 两个检查行为 + `no_*_fallback` 降级行为完全保留;只通用化"哪个工具检查",不通用化"检查什么"
3. **Alias 旧 key 完整工作** — `no_aether_fallback` + `primitive_preference` 仍读取并 emit deprecation warning;unit test 显式 cover
4. **GHA stub `raise NotImplementedError` 含可操作 message** — e.g. `"GHA backend probe succeeded but query not implemented; PR welcome (see SKILL.md §C.2.4.X)"`;不允许裸 `pass` 或空 stub
5. **Standards 子模块零触碰** — Rule #8 引用文件 (`issue-triage.md` / `submodule-pointer-hygiene.md` / `session-handoff.md`) 经 grep verified 无 aether-specific 字面,不改
6. **不允许把 GHA 真实现塞进本 Spec** — GHA 实现独立为 next cycle (~4-6h L2 Spec)

### New from R1 audit (DEC §Audit findings)

7. **GHA stub `NotImplementedError` routing = abort, not skip** (qa F1, Critical) — `gate_check()` 遇 NIE **必须 raise to caller** (abort),**不允许** catch-and-route-to-`no_ci_fallback` 路径吞掉。Rule #8 mechanism 安全性硬约束:防止 `gh` 装但实际用 Aether 的项目 GHA stub probe success → query NIE → 静默吞掉 → Rule #8 (a)+(b) 检查 BOTH 不执行
8. **Backend registry pattern = static import list** (backend-architect F-01) — `ci_backends/__init__.py` 用 static `from .aether import AetherBackend; from .github_actions import GitHubActionsBackend; BACKENDS = [AetherBackend, GitHubActionsBackend]` 模式;**禁止** decorator-based registration / `setuptools.entry_points` / 任何 dynamic discovery。理由:零 plugin discovery complexity + 顺序锁定 (Aether-first precedence per Q3 现网保护承诺)
9. **Old + new config key 同时存在时 → new key wins** (tech-lead M3 + backend-architect F-04) — alias translation 在 `{**DEFAULT_CONFIG, **config}` merge **之前** 执行 (dedicated `_normalize_config(config)` step);冲突时 new key (`no_ci_fallback`) override old key (`no_aether_fallback`) + emit `both_keys_present` warning

### New from R1 post_spec audit (Rev1, 2026-05-28)

10. **`compute_verdict()` signature locked** (Rev1, R1 3-agent CONVERGED tech F-03 + ba a3f8c2d1 + qa F-04) — public function (no underscore), signature 扩展为 `compute_verdict(main_in_flight_runs: list[dict], pr_ci_status: str, backend_name: str, cfg: dict | None = None) -> dict`。`backend_name` 替代旧 hardcoded `"aether-ci-cli"` in `primitive_used` output field。Backward compat: 老 test 可通过 kwargs 调用 (`backend_name="aether-ci-cli"`) 保持 assertion 兼容
11. **Probe cache strategy = Option B** (Rev1, R1 tech F-04 + ba minor) — 用 module-level `_probe_cache: dict[type[CIBackend], bool]` + `reset_probe_cache() -> None` helper export from `ci_backends/__init__.py`;**禁止** `@functools.lru_cache` (test isolation hazard)。`reset_probe_cache()` 调 `_probe_cache.clear()` (idempotent),tearDown 显式调用

---

## Acceptance Criteria

### AC-1: Aether backward behavior (Hard constraint #1)
- AC-1.1: 全部 21 现有 `test_pre_merge_gate.py` test methods PASS after refactor (mock target 改但 assertion 不变)
- AC-1.2: 现网零配置项目 (`.aria/config.json` `phase_c_integrator: {}`) gate_check() 行为完全等价 v1.30.0
- AC-1.3: dogfood smoke 在 Aria 自仓 (Aether 装) 上 gate_check() returns same verdict as pre-refactor

### AC-2: GHA stub safety (Hard constraint #7, R1 Critical fix)
- AC-2.1: `GitHubActionsBackend.probe()` 真实现 — `shutil.which("gh") and _gh_authed()`
- AC-2.2: `GitHubActionsBackend.query_pr_ci()` + `.query_branch_in_flight()` 各 `raise NotImplementedError("GHA backend probe succeeded but query not implemented; PR welcome (see aria/skills/phase-c-integrator/SKILL.md §C.2.4.X)")`
- AC-2.3: 伪代码约束 `gate_check()`:
  ```python
  try:
      pr_status = backend.query_pr_ci(pr_ref)
      in_flight = backend.query_branch_in_flight(branch)
  except NotImplementedError as e:
      # Backend probe succeeded but query not implemented (e.g. GHA stub)
      # → MUST abort (raise to caller), NOT route to no_ci_fallback
      # Rationale: silently skipping when gate mechanism is implementable
      # but unfinished defeats Rule #8. Force user to either:
      #   (1) explicitly disable backend in config, or
      #   (2) complete the backend implementation.
      raise  # propagate up
  ```
- AC-2.4: Test `test_gha_probe_true_query_nie_aborts_not_skips` — 装 mock gh + mock auth → 调 gate_check → assertRaises NotImplementedError (不调 _no_ci_output)
- AC-2.5 (Rev1, R1 tech F-01 Critical): NIE message body assertion — test MUST also `assertIn("GHA backend probe succeeded but", str(exc.value))` AND `assertIn("PR welcome", str(exc.value))` to prevent Hard Constraint #4 (操作可 message) 字面 silent rot

### AC-3: Soft alias precedence (Hard constraint #3 + #9)
- AC-3.1: 旧 key `no_aether_fallback` 单独存在 → 等价行为 + emit DeprecationWarning("`no_aether_fallback` is deprecated; use `no_ci_fallback`; will be removed in v2.0")
- AC-3.2: 旧 key `primitive_preference` 单独存在 → 等价行为 + emit DeprecationWarning("`primitive_preference` is deprecated; use `ci_backends`; will be removed in v2.0")
- AC-3.3: 新+旧 key 同时存在 → new key wins + emit warning("both_keys_present: ignoring `no_aether_fallback`, using `no_ci_fallback`")
- AC-3.4: Test `test_old_key_emits_deprecation_warning_with_expected_message` assertion 包含完整 message 字面 (避免 silent rot per qa F5)
- AC-3.5: Test `test_both_keys_present_new_wins` (per R1 tech-lead M3)

### AC-4: Backend registry + probe precedence (Hard constraint #8)
- AC-4.1: `ci_backends/__init__.py` 包含 static import:
  ```python
  from .aether import AetherBackend
  from .github_actions import GitHubActionsBackend
  BACKENDS: list[type[CIBackend]] = [AetherBackend, GitHubActionsBackend]
  ```
- AC-4.2: `resolve_ci_backend(config) -> CIBackend | None` 按 `BACKENDS` 顺序 probe (Aether 先 GHA 后);config 显式 `ci_backends: [{name: "..."}]` 时按 config 顺序
- AC-4.3: Test `test_aether_takes_precedence_when_both_probe_true` — mock 装 aether + gh → resolve returns AetherBackend instance (per R1 qa F2)
- AC-4.4: 无 decorator / 无 entry-point 验证 — `grep -rn "@register\|entry_points" aria/skills/phase-c-integrator/scripts/ci_backends/` returns 0
- AC-4.5 (Rev1, R1 ba b7e19f4a): `ci_backends: []` (empty list) **explicit disable** semantic — Test `test_explicit_empty_ci_backends_disables` → `resolve_ci_backend({"ci_backends": []})` returns None;Test `test_missing_ci_backends_auto_detects` → `resolve_ci_backend({})` returns AetherBackend (assuming probe true);两者行为必须 distinguishable (区别于 missing vs empty)

### AC-5: Contract surface (Q4)
- AC-5.1 (Rev1, ba F-05 + qa F-05 CONVERGED count fix + F-06+F-06 priority drop): `CIBackend` ABC 含 **4 个 member 共 1 ClassVar + 3 abstract**:`name: ClassVar[str]` + `@classmethod probe(cls) -> bool` + `query_pr_ci(pr_ref) -> CIStatus` + `query_branch_in_flight(branch) -> InFlightStatus`。**`priority` field 已 drop** (Rev1) — BACKENDS list order in `__init__.py` 是 explicit precedence (Hard Constraint #8 + AC-4.1)
- AC-5.2: `CIStatus` dataclass fields: `state: Literal["passing", "failing", "pending", "not_found"]` + `run_id: str | None` + `url: str | None` + `checked_at: str` (ISO 8601)
- AC-5.3: `InFlightStatus` dataclass fields: `runs: list[dict]` + `checked_at: str` (runs 字段 list-of-dict 因 backend schema 不同)
- AC-5.4: `pre_merge_gate.py` 调用使用 attribute access (`pr_status.state == "passing"`),不允许 dict-key access

### AC-6: Doc consistency (Hard constraint #5 + Q5)
- AC-6.1: `CLAUDE.md` L432-444 Rule #8 重写为 backend-agnostic 表述:"通过 CI backend 抽象层调用配置的 CI primitive"
- AC-6.2: `aria/skills/phase-c-integrator/SKILL.md` 新增 §C.2.4.X "CI Backends" 段 (Aether real + GHA stub 表格 + 配置示例 + alias deprecation 注释)
- AC-6.3: `aria/skills/config-loader/SKILL.md` L183/L189 加 alias deprecation 注释 (R1 M-2 fix)
- AC-6.4: `standards/` 任何文件 unmodified — `git diff --stat standards/` returns empty

### AC-7: Rule #6 substitute (Hard constraint per Rule #6 + memory [[feedback_deterministic_structural_skill_rule6_substitute]])
- AC-7.1: `aria-plugin-benchmarks/aria-ci-backend-abstraction/` 目录创建,含 `README.md` 列 12+ AC 行为表
- AC-7.2: ≥27 new unit tests 分布: ci_backends/base.py (5+) + aether.py (8+) + github_actions.py stub (3+) + registry (5+) + alias normalize (3+) + pre_merge_gate integration (3+)
- AC-7.3: Dual-path dogfood smoke evidence 在 README:
  - Default: `AetherBackend.probe()` real-machine return + gate_check() actual verdict
  - GHA detection: `GitHubActionsBackend.probe()` real-machine return + manual NIE abort verification
- AC-7.4: 全 test suite 631+ tests PASS (zero regression)

### AC-8: 5+1 SOT v1.31.0 ship
- AC-8.1: 6 SOT files 全部 `1.31.0` consistent
- AC-8.2: CHANGELOG entry 写在 v1.30.0 entry 上方,v1.29.0 placeholder block 不动 (per R1 m-1)
- AC-8.3: 主仓 CLAUDE.md `插件版本: v1.31.0` 同步
- AC-8.4: aria submodule pointer bump,3-way SHA parity (local = origin = github) verified post-push

---

## Implementation outline

### A. `ci_backends/` package (3h, 4 files)

#### A.1 `aria/skills/phase-c-integrator/scripts/ci_backends/base.py`

```python
"""CI backend abstraction (ABC + data contracts).

Per [DEC 2026-05-28] §Q4 (b) 双方法 + dataclass.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, Literal


@dataclass
class CIStatus:
    """PR CI status check result (per Rule #8 (a) check)."""
    state: Literal["passing", "failing", "pending", "not_found"]
    run_id: str | None = None
    url: str | None = None
    checked_at: str = ""  # ISO 8601


@dataclass
class InFlightStatus:
    """Main branch in-flight run check result (per Rule #8 (b) check)."""
    runs: list[dict] = field(default_factory=list)  # list-of-dict because backend schemas vary
    checked_at: str = ""  # ISO 8601

    @property
    def has_runs(self) -> bool:
        return len(self.runs) > 0


class CIBackend(ABC):
    """Abstract base for CI backend integrations.

    Per [DEC 2026-05-28] §Q4 (b) contract + Hard Constraint #8 (static registry).
    Implementations live in sibling files (aether.py, github_actions.py)
    and are registered in __init__.py via static import (no decorator).
    Precedence is BACKENDS list order (see __init__.py) — no priority field
    (Rev1, R1 ba F-06 + qa F-06: dropped unused priority).
    """
    name: ClassVar[str]

    @classmethod
    @abstractmethod
    def probe(cls) -> bool:
        """Detect whether this backend is available on current machine."""
        ...

    @abstractmethod
    def query_pr_ci(self, pr_ref: str) -> CIStatus:
        """Query PR CI status. MUST raise NotImplementedError if probe() success
        but query unimplemented (e.g. stub backend). gate_check() will abort
        (NOT route through no_ci_fallback) per Hard Constraint #7."""
        ...

    @abstractmethod
    def query_branch_in_flight(self, branch: str) -> InFlightStatus:
        """Query branch in-flight runs. Same NIE contract as query_pr_ci."""
        ...
```

#### A.2 `aria/skills/phase-c-integrator/scripts/ci_backends/aether.py`

**Migration responsibility table** (Rev1, ba c1d6a8e3) — current `pre_merge_gate.py` symbols → new location:

| Current symbol | Current line | New location | Migration note |
|----------------|--------------|--------------|----------------|
| `AETHER_CLI_MIN_SHA = "f29abee"` | L33 | `aether.py` module-level | Aether-specific constant |
| `AETHER_CLI_MIN_DATE = "2026-05-06"` | L34 | `aether.py` module-level | Aether-specific constant |
| `RETRY_BACKOFF = (5, 15, 45)` | L37 | `aether.py` module-level | Aether subprocess retry config |
| `MAX_RETRY_ATTEMPTS` | L38 | `aether.py` module-level | derived from RETRY_BACKOFF |
| `detect_aether()` body | L57-70 | `AetherBackend.probe()` (classmethod) | Aether-specific detection |
| `verify_aether_in_flight_flag()` | L71-101 | `AetherBackend._verify_in_flight_flag()` (private instance method, called by `query_branch_in_flight()`) | Aether-specific |
| `_run_aether_with_retry()` | L103-131 | `AetherBackend._run_with_retry()` (private instance method) | Aether-specific subprocess retry |
| `_query_aether()` | L133-158 | `AetherBackend.query_pr_ci()` + `AetherBackend.query_branch_in_flight()` | Split: 当前函数同时返回 PR+main flat dict;new contract 拆 2 query method,return dataclass |
| `_normalize_pr_ci_status()` | L160-186 | `AetherBackend._normalize_pr_ci_status()` (private) | Aether JSON schema parser, returns `CIStatus.state` enum |
| `_translate_in_flight_run()` | L188-215 | `AetherBackend._translate_in_flight_run()` (private) | Aether JSON schema parser, populates `InFlightStatus.runs` list-of-dict |
| `compute_verdict()` | L217-246 | **stays** `pre_merge_gate.py` (backend-agnostic verdict logic) — signature extended see §B.4 | Verdict computation works on `CIStatus.state` + `InFlightStatus.runs`, not backend-specific |
| `_no_aether_output()` | L248-272 | rename to `_no_ci_output()` (stays `pre_merge_gate.py`) | Generalize message wording from "aether" to "CI backend" |
| `gate_check()` | L274-385 | **stays** `pre_merge_gate.py` (orchestration logic) | Refactored body per §B.4 |

**Behavior preservation**: 所有 migrated functions 保留 byte-for-byte subprocess command + JSON parsing + retry timing — only **call site** changes (in `gate_check`, via `backend.query_*()` instead of `_query_aether()` direct).

#### A.3 `aria/skills/phase-c-integrator/scripts/ci_backends/github_actions.py`

```python
"""GitHub Actions CI backend stub (v1.31.0).

Real implementation deferred to v1.32.0+ next cycle.
probe() is real (detects gh CLI + auth); query methods raise NIE per Hard Constraint #4.
"""
import shutil
import subprocess
from typing import ClassVar

from .base import CIBackend, CIStatus, InFlightStatus


class GitHubActionsBackend(CIBackend):
    name: ClassVar[str] = "github-actions"

    @classmethod
    def probe(cls) -> bool:
        if not shutil.which("gh"):
            return False
        # Check gh authed (not in pre-merge gate's critical path so subprocess OK)
        try:
            result = subprocess.run(
                ["gh", "auth", "status"], capture_output=True, timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, OSError):
            return False

    def query_pr_ci(self, pr_ref: str) -> CIStatus:
        raise NotImplementedError(
            "GHA backend probe succeeded but query_pr_ci not implemented; "
            "PR welcome (see aria/skills/phase-c-integrator/SKILL.md §C.2.4.X). "
            "Per Hard Constraint #7, gate_check() will abort here, NOT skip — "
            "set ci_backends: [] in .aria/config.json to explicitly disable."
        )

    def query_branch_in_flight(self, branch: str) -> InFlightStatus:
        raise NotImplementedError(
            "GHA backend probe succeeded but query_branch_in_flight not implemented; "
            "PR welcome (see aria/skills/phase-c-integrator/SKILL.md §C.2.4.X). "
            "Per Hard Constraint #7, gate_check() will abort here, NOT skip — "
            "set ci_backends: [] in .aria/config.json to explicitly disable."
        )
```

#### A.4 `aria/skills/phase-c-integrator/scripts/ci_backends/__init__.py`

```python
"""CI backend registry (static import list per Hard Constraint #8).

Order is precedence: AetherBackend probed first, GitHubActionsBackend second.
"""
from .base import CIBackend, CIStatus, InFlightStatus
from .aether import AetherBackend
from .github_actions import GitHubActionsBackend

BACKENDS: list[type[CIBackend]] = [AetherBackend, GitHubActionsBackend]

__all__ = ["CIBackend", "CIStatus", "InFlightStatus",
           "AetherBackend", "GitHubActionsBackend", "BACKENDS"]
```

### B. `pre_merge_gate.py` refactor (1h)

#### B.1 Replace `DEFAULT_CONFIG` (L46-55)

```python
DEFAULT_CONFIG = {
    "enabled": True,
    "ci_backends": [],  # empty = auto-detect via probe (Hard Constraint #8 default)
    "no_ci_fallback": "skip_with_warning",
    "wait_timeout_seconds": 1800,
    "wait_check_intervals": [30, 60, 120, 300, 300],
    "primitive_call_timeout_seconds": 30,
    "poll_chunk_seconds": 5,
    "user_escape_hatch": True,
}
```

#### B.2 Add `_normalize_config()` (NEW) — alias translation **before** merge

```python
_OLD_TO_NEW = {
    "primitive_preference": "ci_backends",  # value shape changes too — see _translate_value
    "no_aether_fallback": "no_ci_fallback",
}


def _normalize_config(config: dict) -> dict:
    """Translate legacy config keys to v1.31.0 schema with deprecation warnings.

    Per Hard Constraint #3 (alias support) + #9 (new key wins on conflict).
    Operates at the `phase_c_integrator.pre_merge_gate` config sub-dict level
    (caller responsibility to pass the right sub-dict, not the top-level
    .aria/config.json dict).
    """
    out = dict(config)  # shallow copy
    for old, new in _OLD_TO_NEW.items():
        if old in out:
            if new in out:
                # Conflict: new wins, old discarded (Hard Constraint #9)
                warnings.warn(
                    f"both_keys_present: ignoring `{old}`, using `{new}`",
                    DeprecationWarning, stacklevel=2,
                )
                del out[old]
            else:
                # Soft alias: translate old → new + warn
                warnings.warn(
                    f"`{old}` is deprecated; use `{new}`; "
                    f"will be removed in v2.0",
                    DeprecationWarning, stacklevel=2,
                )
                out[new] = _translate_value(old, out.pop(old))
    return out


def _translate_value(old_key: str, old_value):
    """Per-key value-shape translation (Rev1 complete table, tech F-02).

    Translation map (2 keys total):
      primitive_preference: ["aether-ci-cli"]  → ci_backends: [{"name": "aether-ci-cli"}]
                            ["foo", "bar"]    → ci_backends: [{"name": "foo"}, {"name": "bar"}]
                            []                → ci_backends: []  (preserves Rev1 [] disable semantic)
      no_aether_fallback:   "skip_with_warning" → no_ci_fallback: "skip_with_warning"  (no shape change)
                            "abort"             → no_ci_fallback: "abort"              (no shape change)
    """
    if old_key == "primitive_preference":
        # Old value is list[str], new value is list[{"name": str}]
        return [{"name": n} for n in old_value]
    if old_key == "no_aether_fallback":
        # String enum literal, no shape change
        return old_value
    # Defensive: unknown old key → return as-is (shouldn't reach since _OLD_TO_NEW filter upstream)
    return old_value
```

#### B.3 Replace `detect_aether()` (L57-70) → `resolve_ci_backend()`

```python
def resolve_ci_backend(config: dict) -> CIBackend | None:
    """Per [DEC 2026-05-28] §Q3 (b) config-first + probe fallback.

    Semantics (Rev1, R1 ba b7e19f4a lock):
      - config["ci_backends"] absent OR None  → auto-detect via BACKENDS list order
      - config["ci_backends"] is empty list [] → **explicit disable** (return None
        immediately, caller routes per no_ci_fallback). This is the canonical way
        for user to bypass CI backend integration in v1.31.0+.
      - config["ci_backends"] non-empty list  → try in user-specified order,
        return first that probes True;exhausted (all probe False) → None

    Returns None signals caller to route through no_ci_fallback path.
    """
    explicit = config.get("ci_backends")
    if explicit is not None:
        # Explicit user config (including [] = disable)
        if not explicit:
            return None  # [] = explicit disable per Rev1 ci_backends:[] semantic lock
        name_map = {b.name: b for b in BACKENDS}
        for entry in explicit:
            backend_cls = name_map.get(entry.get("name") if isinstance(entry, dict) else entry)
            if backend_cls and backend_cls.probe():
                return backend_cls()
        return None
    # Auto-detect (config missing or None)
    for backend_cls in BACKENDS:
        if backend_cls.probe():
            return backend_cls()
    return None
```

#### B.4 Replace `gate_check()` body — backend dispatch

```python
def gate_check(pr_ref: str, branch: str, config: dict | None = None) -> dict:
    """Pre-merge gate orchestration (Rule #8).

    Returns dict with `verdict` field (green/wait/fail) and `primitive_used`
    (backend name) for downstream workflow-runner consumption.

    Exception semantics (Rev1, Hard Constraint #7):
      - NotImplementedError from backend.query_*() propagates (abort, NOT
        caught and routed to no_ci_fallback). This breaks the prior contract
        that "gate_check returns a structured verdict, never raises";callers
        MUST be updated to expect NotImplementedError when backend is a stub.
    """
    cfg = _normalize_config({**DEFAULT_CONFIG, **(config or {})})  # alias translation BEFORE merge
    if not cfg["enabled"]:
        return {"verdict": VERDICT_GREEN, "skipped": True, "reason": "disabled"}

    backend = resolve_ci_backend(cfg)
    if backend is None:
        return _no_ci_output(cfg["no_ci_fallback"])  # renamed from _no_aether_output

    # Query order: main in-flight FIRST then PR CI SECOND (Rev1.1 corrected
    # per R2 ba N-1 — matches ground truth gate_check L309-329:main in-flight
    # queried L309-318 before PR CI queried L320-329). Hard Constraint #1
    # (Aether behavior zero change) requires this exact order — early-fail on
    # main in-flight short-circuits PR query (matches current Aether subprocess
    # invocation count + log emission order).
    # Hard Constraint #7: NIE from query MUST propagate (abort, not skip)
    in_flight = backend.query_branch_in_flight(branch)  # raises NIE → propagate
    pr_status = backend.query_pr_ci(pr_ref)             # raises NIE → propagate

    # Verdict computation — existing public function compute_verdict() L217,
    # signature extended in Rev1 to accept backend.name for primitive_used field.
    # Rev1 Hard Constraint #10 locks signature.
    return compute_verdict(
        main_in_flight_runs=in_flight.runs,    # backward compat: list[dict] field
        pr_ci_status=pr_status.state,          # backward compat: enum string
        backend_name=backend.name,              # NEW Rev1 param: replaces hardcoded "aether-ci-cli"
        cfg=cfg,                                # for wait_timeout / fallback config
    )
```

**`compute_verdict()` signature (Rev1, Hard Constraint #10)** — extended from ground truth L217:

```python
def compute_verdict(
    main_in_flight_runs: list[dict],   # was: list[dict] (no change)
    pr_ci_status: str,                  # was: str (no change, accepts CIStatus.state enum value)
    backend_name: str,                  # NEW Rev1 — replaces hardcoded "aether-ci-cli" in output
    cfg: dict | None = None,            # NEW Rev1 — for wait_timeout / fallback access (was implicit)
) -> dict:
    """Compute pre-merge verdict from PR CI + main in-flight signals.

    Output dict (unchanged keys except primitive_used uses backend_name):
      verdict: "green" | "wait" | "fail"
      primitive_used: backend_name  # was: hardcoded "aether-ci-cli"
      primitive_version_sha: backend-specific (Aether: AETHER_CLI_MIN_SHA; GHA: "<stub>")
      pr_ci_status: pr_ci_status   # echo for caller
      main_in_flight: bool         # has_runs derived
      ...
    """
```

#### B.5 Rename `_no_aether_output()` → `_no_ci_output()` (preserve all behavior)

### C. Test rewrite (3-3.5h, ~30+ test cases)

Per R1 audit M-1 substance convergence: actual `test_pre_merge_gate.py` has 23 `detect_aether` mocks + 3 mock targets per test (`detect_aether`, `verify_aether_in_flight_flag`, `_query_aether`). All 3 collapse:

| Old mock target | New mock target |
|----------------|----------------|
| `gate.detect_aether` | `AetherBackend.probe` (classmethod patch) |
| `gate.verify_aether_in_flight_flag` | absorbed into `AetherBackend.query_branch_in_flight` |
| `gate._query_aether` | `AetherBackend.query_pr_ci` + `AetherBackend.query_branch_in_flight` |

New test classes (estimated +1-1.5h beyond rewrite):
- `TestGHAStubAbortNotSkip` (~3 cases per AC-2)
- `TestAliasKeyPath` (~3 cases per AC-3.1/3.2/3.4)
- `TestBothKeysPresentNewWins` (~1 case per AC-3.5)
- `TestBackendRegistry` (~5 cases: empty config auto-detect / explicit order / unknown name / Aether-first precedence / no decorator verification)
- `TestNormalizeConfigSequencing` (~2 cases: alias runs before merge)
- `TestProbeCacheIsolation` (~2 cases: lru_cache tearDown OR module-level dict reset)

**Test isolation fix** (R1 backend-architect F-05): `tearDown(self): AetherBackend.probe.cache_clear(); GitHubActionsBackend.probe.cache_clear()` OR drop `@lru_cache` and use module-level `_probe_cache: dict[type[CIBackend], bool]` reset per test.

### D. Doc updates (1.25h)

#### D.1 `CLAUDE.md` Rule #8 L432-444 — full rewrite to backend-agnostic

#### D.2 `aria/skills/phase-c-integrator/SKILL.md` — ~10 edits + new §C.2.4.X

New section sketch (§C.2.4.X CI Backends, ~40 lines):
- Backend selection algorithm (config → static registry → probe order)
- Backend table (Aether real + GHA stub + future GitLab/Forgejo)
- Config schema (`ci_backends: [{name, priority?}, ...]`)
- Alias deprecation notes
- NIE abort behavior per Hard Constraint #7

#### D.3 `aria/skills/config-loader/SKILL.md` L183/L189 (R1 M-2 fix)

Add alias deprecation note: "v1.31.0+: `no_aether_fallback` → `no_ci_fallback`; old key still readable until v2.0"

### E. Rule #6 substitute (1.5-2h, per memory [[feedback_deterministic_structural_skill_rule6_substitute]])

`aria-plugin-benchmarks/aria-ci-backend-abstraction/README.md` (mirror Sprint 1 forgejo-hosts pattern):
- §AC behavior table (12+ rows mapping AC-1~AC-8 to test name + expected behavior)
- §Structural fixture: example `MockCIBackend` 实现 + how to add new backend (decorator-free, static registry path)
- §Unit test count: 27+ tests breakdown by file
- §Dual-path dogfood smoke evidence:
  - Aether-installed run: `AetherBackend.probe() = True` + gate_check() verdict ≡ pre-refactor
  - GHA-installed run: `GitHubActionsBackend.probe() = True` (if `gh` authed) + gate_check() raises NIE (manual verify via `python -c` invocation)
- §How this substitutes Rule #6 benchmark: deterministic Skill (no AI capability AB testable;structural correctness + behavior preservation are the substance)

### F. 5+1 SOT v1.31.0 bump (0.5h)

| File | Change |
|------|--------|
| `aria/.claude-plugin/plugin.json` | `"version": "1.31.0"` |
| `aria/.claude-plugin/marketplace.json` | top-level + `plugins[].version` = `1.31.0` |
| `aria/VERSION` | `1.31.0` |
| `aria/CHANGELOG.md` | new entry above v1.30.0 (per R1 m-1 ordering) |
| `aria/README.md` | version field |
| `CLAUDE.md` (main repo) | `插件版本: v1.31.0` |

---

## Risk + Mitigation

| Risk | Likelihood | Severity | Mitigation |
|------|-----------|----------|-----------|
| **Alias path 无 production traffic → dead code rot** (qa F5) | Medium | Low | AC-3.4 强制 test 验 deprecation warning 字面 message;`_normalize_config()` unit test ≥3 cases covering single old, single new, both present |
| **Test rewrite blast radius underestimated** (R1 substance-converged M-1) | Mitigated | Mitigated | Estimate revised 2h → 3-3.5h;Phase B 总 estimate 8.5h → 10-10.5h;实施时若超 4h 触发 owner check |
| **lru_cache test isolation** (ba F-05) | Medium | Medium | AC-7 + tasks.md 强制 tearDown cache_clear,OR 重构为 module-level dict with explicit reset helper |
| **CHANGELOG v1.31.0 vs v1.29.0 ordering during 9-day overlap** (tech m-1) | Low | Medium | v1.31.0 entry 写在 v1.30.0 上方,v1.29.0 placeholder block 不动 (留作 block-flip ship day 替换点) |
| **Sister terminal CLAUDE.md contention** (per [[feedback_claude_md_project_status_high_contention]]) | High | Low-Medium | session 开始 `git fetch` 验无 inflight Spec 触 CLAUDE.md;改动只触 Rule #8 段 (L432-444) 不撞 sister 的 项目状态 section / footer (L600+) |
| **GHA stub probe success → silent skip when run in pure-GHA repo** (R1 qa F1 Critical) | RESOLVED by Hard #7 | RESOLVED | AC-2.3 伪代码 + AC-2.4 test 强制 NIE → abort 路径;非降级 |
| **Old + new key precedence ambiguity** (tech M3) | RESOLVED by Hard #9 | RESOLVED | AC-3.3 + AC-3.5 强制 new wins + both-present warning + test |
| **registry discovery pattern drift** (ba F-01) | RESOLVED by Hard #8 | RESOLVED | AC-4.4 grep verification 无 @register/entry_points |

---

## Rule #6 substitute plan

本 Spec 是 **deterministic / structural Skill 范畴** (per memory [[feedback_deterministic_structural_skill_rule6_substitute]]) — collector/parser/detector 类代码,无 AI capability AB testable behavior。Rule #6 substitute = **structural fixture + unit tests + dogfood smoke**,不跑 `/skill-creator benchmark` AB 对比 (因 with/without_skill delta 没有 substance:Skill 行为是 deterministic Python 函数 + Python 函数,无 AI prompt 变量)。

详见 Deliverable E §README + AC-7。

---

## References

### Source
- DEC: [`.aria/decisions/2026-05-28-ci-backend-abstraction-brainstorm.md`](../../../.aria/decisions/2026-05-28-ci-backend-abstraction-brainstorm.md) (273 lines, 5 decisions + 9 Hard Constraints + §Audit findings)
- Boundary audit memo: `.aria/notes/2026-05-27-boundary-audit-10cg-hardcode.md` §修复 2
- aria-fleet strategic memo: `.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md` §4 边界切割规则
- Predecessor handoff: `docs/handoff/2026-05-27-forgejo-hosts-parameterization-v1.30.0-shipped.md` §6 carry-forward S1
- R1 audit reports:
  - `.aria/audit-reports/post_brainstorm-R1-2026-05-28T080358-929Z-aria-ci-backend-abstraction-backend-architect.md`
  - `.aria/audit-reports/post_brainstorm-R1-2026-05-28T080401-452Z-aria-ci-backend-abstraction-tech-lead.md`
  - `.aria/audit-reports/post_brainstorm-R1-2026-05-28T080514-474Z-aria-ci-backend-abstraction-qa-engineer.md`

### Forward
- Next Spec: GHA backend real implementation (~4-6h L2, ship v1.32.0+)
- M7+ aria-fleet: GitProvider ABC + workspace layer extraction + Feishu notification abstraction

### Memory
- [[feedback_three_layer_universal_workspace_instance]] — aria-fleet 三层架构边界硬约束
- [[feedback_cross_cutting_capability_as_agent_tool_pack]] — 跨项目能力的 tool pack 模式
- [[feedback_deterministic_structural_skill_rule6_substitute]] — Rule #6 substitute pattern
- [[feedback_brainstorm_substance_convergence_pattern]] — R1 M-1 三 agent 独立 surface 同根因
- [[feedback_audit_convergence_patterns]] — L3 baseline 4-round + Critical-but-addressable-downstream pattern (R2 skip rationale)
- [[feedback_sub_pr_scope_splitting_pattern]] — Q1 stub-vs-full split 正当性
- [[feedback_sequenced_multirepo_gitlink_bump]] — Phase C aria submodule → main repo gitlink bump 顺序
- [[feedback_claude_md_project_status_high_contention]] — Phase C CLAUDE.md contention 防御
- [[feedback_release_phase_d_5_files_synchronization]] — 5+1 SOT bump checklist
