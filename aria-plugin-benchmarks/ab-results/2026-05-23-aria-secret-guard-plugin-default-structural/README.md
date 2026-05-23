# Rule #6 Structural Substitute — aria-doctor::check_secret_guard_install

> **Date**: 2026-05-23
> **Spec**: `openspec/changes/aria-secret-guard-plugin-default`
> **Skill**: `aria/skills/aria-doctor/` v1.0.0 (ships with aria-plugin v1.24.0)
> **Substitute pattern**: deterministic structural skill (per memory `feedback_deterministic_structural_skill_rule6_substitute`)

---

## Why structural substitute (not `/skill-creator` LLM AB)

`aria-doctor::check_secret_guard_install` is a **deterministic structural skill**:

- **Input**: filesystem state (file presence + content + JSON validity + semver banner)
- **Output**: JSON state object (`state` + `sub_flags` + `advisory` + `details`)
- **Mapping**: pure function — same input → same output, no LLM creativity or context-dependent reasoning

LLM AB testing (`/skill-creator` with/without comparison) measures **quality
of reasoning**, which does not apply here. Per memory
`feedback_rule6_framing_differs_by_skill_type`, deterministic/structural
skills use:

1. **Structural fixture coverage** — README mapping skill states ↔ test cases
2. **Unit tests** — programmatic verification of each state transition
3. **Atomicity guard** — schema evolution contract preventing breaking change
4. **Dogfood evidence** — in-vivo run on Aria itself + cross-project (TASK-007/008)

This directory contains all four artifacts.

---

## 5-state × 2-sub-flag ↔ 8 test case coverage matrix

| State | Sub-flags | Test | Fixture |
|-------|-----------|------|---------|
| `not_installed` | — | T1 | no plugin hook + no local hook |
| `single_plugin` | — | T2 | plugin hook only |
| `single_local` | — | T3 | local hook only |
| `dual_install` | (none) | T4 | identical content, no divergence |
| `dual_install` | `stale_local_version + divergent_content` | T5 | local banner v1.2.0, plugin v1.24.0, different content |
| `dual_install` | `divergent_content` only | T6 | same version banners (v1.24.0), but content differs |
| `corrupted_settings` | — (mutex) | T7 | dual_install fixture + malformed `.claude/settings.json` |
| `dual_install` | `divergent_content` only **+ banner-missing edge** | T8 | local has NO banner; assert `stale_local_version` NOT set despite SHA differ |

**Coverage**: all 5 primary states + both sub-flags as standalone + both sub-flags
combined + corrupted_settings precedence + banner-missing graceful fallback
(R2 QA NF2).

---

## Run

```bash
bash aria/skills/aria-doctor/tests/check_secret_guard_install.test.sh
```

**Latest run** (2026-05-23, initial implementation):

```
──────────────────────────────────────────────────
check_secret_guard_install.sh unit tests
PASS: 8 / 8
FAIL: 0 / 8
```

---

## R2 deferred items absorbed (closure points)

This substitute closure also satisfies the post_spec R2 audit deferred items
documented in `detailed-tasks.yaml` `metadata.rev2_deferred_items`:

| R2 item | Closure |
|---------|---------|
| **BA N1**: `not_installed` runtime contract — assert-never under normal plugin-loaded execution | aria-doctor SKILL.md §State Schema 5-state table + advisory text ("assert-never under normal plugin-loaded execution + verify CLAUDE_PLUGIN_ROOT"). Test T1 exercises the assert-never path via deliberate plugin-root misresolve. |
| **BA N2**: `single_local` advisory dual-cause | aria-doctor SKILL.md §Advisory table + check script line ~120 advisory string includes BOTH "plugin not loaded?" AND "version < v1.24.0". Test T3 asserts both substrings present in advisory output. |
| **QA NF2**: banner regex spec + 8th unit test (banner-missing edge) | aria-doctor SKILL.md §"Banner regex spec" + check script `BANNER_REGEX` constant + Test T8 explicitly asserts banner-missing → `local_version=null` + `stale_local_version` NOT set. |

---

## Related artifacts

- [`atomicity-guard.md`](./atomicity-guard.md) — schema evolution contract
- [`dogfood-evidence.md`](./dogfood-evidence.md) — Aria self in-vivo run (linked from TASK-007)
- [`aria/skills/aria-doctor/SKILL.md`](../../../aria/skills/aria-doctor/SKILL.md) — skill source
- [`aria/skills/aria-doctor/scripts/check_secret_guard_install.sh`](../../../aria/skills/aria-doctor/scripts/check_secret_guard_install.sh) — implementation
- [`aria/skills/aria-doctor/tests/check_secret_guard_install.test.sh`](../../../aria/skills/aria-doctor/tests/check_secret_guard_install.test.sh) — 8 unit tests
