# Atomicity Guard — `check_secret_guard_install` schema evolution contract

> **Date**: 2026-05-23
> **Skill**: `aria-doctor` v1.0.0 (ships with aria-plugin v1.24.0)
> **Memory ref**: `feedback_deterministic_structural_skill_rule6_substitute`

---

## Why an atomicity guard

`check_secret_guard_install()` JSON output is **consumed by**:

- AI assistants reading `aria-doctor` skill output to advise the user
- Human operators reading the advisory text + state value
- (Future) automated `aria-doctor` aggregate dashboards / metrics
- (Future) `aria-doctor self-test` sub-command (deferred to v1.25.x)

Breaking the schema (rename / delete a state, change a sub-flag name)
silently invalidates every downstream consumer. Since the schema is a
**boundary contract**, evolution must be **append-only**.

---

## Allowed evolutions (additive)

✅ **Append new sub-flag** to an existing primary state. Example future
addition: `signature_mismatch` (could indicate tampered local copy).

✅ **Append new primary state** (rare). Must have a clear, mutually
exclusive trigger condition documented.

✅ **Extend `details` object** with new fields. Existing fields retain
their type and meaning.

✅ **Improve advisory text** for existing state without changing its
semantic.

✅ **Add new optional CLI arg** to the check script (back-compat defaults).

---

## Forbidden evolutions (breaking)

❌ **Rename primary state**. e.g. `single_plugin` → `plugin_only`. Locks
downstream consumers to old name.

❌ **Rename sub-flag**. e.g. `stale_local_version` → `outdated_local`.

❌ **Delete primary state or sub-flag**. Even if "logically unreachable".

❌ **Change `state` field type** (currently string enum). e.g. moving to
nested object.

❌ **Re-purpose existing field** (semantic change of `details.plugin_version`
from semver to commit SHA, etc.).

❌ **Change banner regex in either direction** (v1.24.2 audit followup —
backend-architect M3 closure):
- **Tightening**: previously-matching version banners now fail to detect
  (silent `local_version: null` regression, loses `stale_local_version`
  sub-flag accuracy)
- **Loosening**: previously-non-matching strings now register as version
  banners (false-positive version match on unrelated comments, may
  trigger spurious `stale_local_version`)
Either direction silently changes detection semantics without bumping
the schema contract. Regex changes that demonstrably preserve all
existing test fixtures' classification + add new positive cases via
new fixtures are the only safe path.

❌ **Change exit code semantics**. (Currently: 0 = check succeeded; 2 = usage
error.)

---

## Migration discipline

When a breaking change becomes unavoidable (Aria v2.0 MAJOR):

1. **Document the breaking change** in `aria/CHANGELOG.md` under MAJOR header
2. **Provide deprecation period** of ≥1 MINOR cycle where both old and new
   schema co-exist (e.g. emit `state` in old form + `state_v2` in new form)
3. **Notify downstream** via Forgejo Issues / release notes
4. **Final removal** only in next MAJOR after deprecation period

---

## Why this is "Rule #6 substitute" not LLM benchmark

Per memory `feedback_rule6_framing_differs_by_skill_type`, structural
deterministic skills do not benefit from `/skill-creator` with/without LLM
AB comparison because:

1. **No LLM reasoning** — output is computed mechanically (filesystem +
   regex + sha256)
2. **No prompt sensitivity** — same input always produces same output
3. **No description tuning value** — skill metadata triggers human/AI
   invocation, but the *output* is the contract

The relevant quality signal is **schema stability over releases**. This
file IS the Rule #6 substitute deliverable for the structural-skill class.

---

## Audit checkpoint

Pre-MAJOR-release manual audit checklist:

```yaml
audit_questions:
  - Has any primary state been renamed?       # MUST be "no"
  - Has any sub-flag been renamed?            # MUST be "no"
  - Has any primary state or sub-flag been    # MUST be "no" without
    deleted?                                  #   deprecation period
  - Has the JSON `state` field type changed?  # MUST be "no"
  - Has a `details` field semantic changed?   # MUST be "no"
  - Are all 8 unit tests still passing?       # MUST be "yes"
  - Has CHANGELOG.md documented any           # If applicable, MUST be "yes"
    additions?
```

If any "yes" appears under "MUST be no" — **block release** until either
revert the change, or follow Migration discipline above.

---

## Refs

- Schema source: `aria/skills/aria-doctor/scripts/check_secret_guard_install.sh`
- Test suite: `aria/skills/aria-doctor/tests/check_secret_guard_install.test.sh`
- Skill doc: `aria/skills/aria-doctor/SKILL.md` §State Schema
- Sibling artifact: [`README.md`](./README.md)
- Sibling artifact: [`dogfood-evidence.md`](./dogfood-evidence.md)
