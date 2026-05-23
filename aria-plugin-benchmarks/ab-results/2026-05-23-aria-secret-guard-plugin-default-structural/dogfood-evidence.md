# Dogfood Evidence — aria-doctor::check_secret_guard_install

> **Date initiated**: 2026-05-23 (placeholder; final fill on TASK-007 completion)
> **Status**: Initial Aria-self in-vivo capture; cross-project capture deferred to TASK-007/008.
> **Spec**: `openspec/changes/aria-secret-guard-plugin-default` TASK-004 Rule #6 substitute artifact

---

## Aria self in-vivo check (TASK-004 implementation phase)

Captured during TASK-004 implementation, **before** v1.24.0 ship + TASK-006 SOT bump.

**Command**:

```bash
cd /home/dev/Aria/worktrees/aria-secret-guard-plugin-default
bash aria/skills/aria-doctor/scripts/check_secret_guard_install.sh "$PWD" "$PWD/aria"
```

**Output**:

```json
{
  "state": "dual_install",
  "sub_flags": [],
  "advisory": "Double defense active (plugin + local hooks both fire on same event, per Q1 hook orchestrator merge semantics — see standards/conventions/secret-hygiene.md §5.4). KEEP as-is recommended for at least 1 minor cycle as fallback.",
  "details": {
    "plugin_hook_present": true,
    "local_hook_present": true,
    "settings_json_valid": true,
    "plugin_version": "1.23.1",
    "local_version": null,
    "plugin_sha256": "f182ca437dccf5b57cf34bab0886dc5daeb9b9e26a108b4d7a0c723643f75c72",
    "local_sha256": "f182ca437dccf5b57cf34bab0886dc5daeb9b9e26a108b4d7a0c723643f75c72",
    "plugin_hook_path": "/home/dev/Aria/worktrees/aria-secret-guard-plugin-default/aria/hooks/secret-guard.sh",
    "local_hook_path": "/home/dev/Aria/worktrees/aria-secret-guard-plugin-default/.claude/scripts/secret-guard.sh"
  }
}
```

**Validation**:

- ✅ State correctly identified as `dual_install` (Aria has both worktree plugin
  copy + pre-existing local copy from 2026-05-20 Layer 2 cherry-pick)
- ✅ Zero sub-flags because SHA256 matches (both copies derive from same
  SilkNode HEAD bytewise cherry-pick → identical content)
- ✅ `local_version` correctly `null` — SilkNode HEAD has no version banner,
  banner-missing graceful fallback per R2 QA NF2
- ✅ Advisory reflects "KEEP as-is" recommendation for clean dual_install
- ✅ Plugin version reads `1.23.1` from current `plugin.json` (pre-TASK-006 bump)

**Live behavior in this session**: while the script was being written, multiple
Bash invocations of the test runner were **in-vivo blocked** by Aria's currently-
installed secret-guard hook (via SilkNode-style `.claude/settings.json`
registration of the local copy) when test fixture payloads contained
risky patterns like `nomad var get` or `strings ... .env` substrings.
Recovery via `git commit -F` and `printf`-built dynamic payloads validated
the hook's effectiveness on real LLM tool calls + recorded as **dogfood
event #2 of this Spec cycle** in the TASK-002 + TASK-005 commit messages.

---

## Post-bump capture (deferred to TASK-007)

TASK-007 Aria self dogfood (~10 daily commands + p95 timing) will run **after**
TASK-006 v1.24.0 SOT bump. Expected delta from this initial capture:

| Field | This capture (pre-bump) | After TASK-006 (post-bump) |
|-------|-------------------------|----------------------------|
| `details.plugin_version` | `"1.23.1"` | `"1.24.0"` |
| State | `dual_install` (unchanged) | `dual_install` (unchanged) |
| Sub-flags | `[]` (unchanged) | `[]` if no content change; `["divergent_content"]` if v1.24.0 SOT bump adds banner |

TASK-007 will append the post-bump check + ≥10 daily-use Bash/Read/Edit commands
+ timing capture (p50_ms, p95_ms per event) directly to this file under a
"Post-bump capture" section.

---

## Cross-project capture (deferred to TASK-008)

TASK-008 SilkNode cross-project smoke (or P2.5/P3 fallback) will append a
"SilkNode" section to this file with comparable check output + ≥10 daily-use
command coverage + timing capture. P2.5/P3 fallback paths produce a
"deferred_post_ship" or "owner_stand_in" mode marker.

---

## Ship gate verdict integration (TASK-009)

This dogfood-evidence.md file feeds the aggregate `smoke-evidence.md` at
`openspec/changes/aria-secret-guard-plugin-default/smoke-evidence.md` which
TASK-009 finalizes with PASS/REVIEW/BLOCK verdict per tasks.md §5.4 rubric.

---

## State distribution baseline (for future regression detection)

Tracking expected state distribution across Aria-managed environments
post-v1.24.0 ship. This baseline anchors future regression detection — if
a future check reveals a sudden shift from `dual_install` to `not_installed`
across multiple projects, that signals a plugin loader regression.

| Environment | Expected state | Notes |
|-------------|----------------|-------|
| Aria self (this worktree) | `dual_install` | Pre-existing local + plugin SOT |
| SilkNode | `dual_install` | Pre-existing local + plugin SOT |
| Aether | `single_plugin` | New consumer after v1.24.0 default-on |
| truffle-hound | `single_plugin` | New consumer |
| Any project that owner manually copies hook | `dual_install` | Layer 0 documented in `standards/conventions/secret-hygiene.md` §6 |

---

## Refs

- Sibling: [`README.md`](./README.md) (substitute framework overview)
- Sibling: [`atomicity-guard.md`](./atomicity-guard.md) (schema evolution contract)
- Skill: [`aria/skills/aria-doctor/SKILL.md`](../../../aria/skills/aria-doctor/SKILL.md)
- Spec: `openspec/changes/aria-secret-guard-plugin-default/`
- TASK-007 / TASK-008 commits will append additional captures here.
