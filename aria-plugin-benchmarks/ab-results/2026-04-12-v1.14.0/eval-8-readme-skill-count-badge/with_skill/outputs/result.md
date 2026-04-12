# State Scanner — Phase 1.8 README Sync Check

> **Scan Date**: 2026-04-12
> **Scanner**: state-scanner v2.9 (Phase 1.8 focused)
> **Context**: Post v1.14.0 release — verify README sync

---

## Summary

| Check | Status | Severity |
|-------|--------|----------|
| aria/README.md version vs plugin.json | MISMATCH | **error** |
| aria/README.md skill count vs actual | MISMATCH | **error** |
| aria/README.md skill list completeness | PASS | info |
| aria/README.zh.md version vs plugin.json | MISMATCH | **error** |
| aria/README.zh.md skill count vs actual | MISMATCH | **error** |
| aria/README.zh.md skill list completeness | MISSING SKILLS | **warning** |
| Main README.md badge version vs plugin.json | MISMATCH | **warning** |
| Main README.md project structure version | MISMATCH | **warning** |
| Main README.md skill count vs actual | MISMATCH | **warning** |
| Main README.md "Project Status" section | MISMATCH | **warning** |
| aria/VERSION version vs plugin.json | MISMATCH | **error** |
| aria/marketplace.json version vs plugin.json | MISMATCH | **error** |
| aria/CHANGELOG.md latest entry | MISSING v1.14.0 | **error** |

**Verdict**: Multiple version and count mismatches detected. README files are out of sync with actual project state.

---

## Detailed Findings

### 1. Version Source of Truth (plugin.json)

```yaml
plugin.json version: "1.13.0"
```

**Note**: The user states v1.14.0 was just released, but `plugin.json` still reads `1.13.0`. Either the submodule pointer has not been updated, or the release has not been committed yet to this working copy.

### 2. Actual Skill Inventory

**Total skill directories**: 35

**Internal skills** (user-invocable: false): 5
- agent-router
- agent-team-audit
- arch-common
- audit-engine
- config-loader

**User-facing skills**: 30 (= 35 total - 5 internal)

Complete list of 30 user-facing skills:
1. agent-creator
2. agent-gap-analyzer
3. api-doc-generator
4. arch-scaffolder
5. arch-search
6. arch-update
7. aria-dashboard
8. aria-report
9. brainstorm
10. branch-finisher
11. branch-manager
12. commit-msg-generator
13. forgejo-sync
14. openspec-archive
15. phase-a-planner
16. phase-b-developer
17. phase-c-integrator
18. phase-d-closer
19. progress-updater
20. project-analyzer
21. requesting-code-review
22. requirements-sync
23. requirements-validator
24. spec-drafter
25. state-scanner
26. strategic-commit-orchestrator
27. subagent-driver
28. task-planner
29. tdd-enforcer
30. workflow-runner

### 3. aria/README.md (English)

```yaml
readme_version: "1.13.0"
plugin_version: "1.13.0"  # from plugin.json
version_match: true        # Both say 1.13.0, but if v1.14.0 was released, BOTH are stale

readme_skill_count: "33 user-facing + 3 internal"
actual_skill_count: "30 user-facing + 5 internal"
skill_count_match: false

skill_list_completeness: PASS  # All 35 directories listed in README
skill_list_missing: []
```

**Issues**:
- README claims 33 user-facing + 3 internal = 36 total
- Actual is 30 user-facing + 5 internal = 35 total
- The discrepancy: README counts agent-router and agent-team-audit as user-facing, but both have `user-invocable: false` in their SKILL.md
- README header says "33 Skills + 11 Agents" but `## Skills` section also says "(33 user-facing + 3 internal)"
- plugin.json description also says "33个 Skills + 11个 Agents + Hooks系统"

### 4. aria/README.zh.md (Chinese)

```yaml
readme_version: "1.11.1"
plugin_version: "1.13.0"  # from plugin.json
version_match: false

readme_date: "2026-04-10"
changelog_latest_date: "2026-04-11"
date_match: false

readme_skill_count: "30 个 Skills + 11 个 Agents"
actual_skill_count: "30 user-facing + 5 internal = 35 total"
skill_count_match: true (user-facing count matches)
total_count_match: false (README doesn't mention internal count)
```

**Issues**:
- Version severely outdated: shows 1.11.1 vs plugin.json 1.13.0 (2 minor versions behind)
- Missing skills from listing (not updated since v1.11.1):
  - aria-dashboard (added v1.10.0, present in listing)
  - project-analyzer (added v1.13.0, MISSING from listing)
  - agent-gap-analyzer (added v1.13.0, MISSING from listing)
  - agent-creator (added v1.13.0, MISSING from listing)
  - audit-engine (added later, MISSING from listing)
- "Project Adaptation" category entirely missing from zh README

### 5. Main README.md (Root)

```yaml
badge_version: "v1.13.0"
plugin_version: "1.13.0"  # from plugin.json
badge_match: true (both 1.13.0, but stale if v1.14.0 released)

project_structure_aria_version: "v1.13.0"
skill_count_in_structure: "36 Skills (33 user-facing + 3 internal)"
actual_total: 35
skill_count_match: false

project_status_plugin_version: "1.13.0"
project_status_skill_count: "36 Skills + 11 Agents"
actual: "35 Skills + 11 Agents"
match: false

skills_section_header: "Skills (33 user-facing + 3 internal)"
actual: "30 user-facing + 5 internal"
match: false
```

**Issues**:
- Line 8: Badge says `Plugin-v1.13.0` -- needs update to v1.14.0
- Line 129: "Skills (33 user-facing + 3 internal)" -- should be "30 user-facing + 5 internal"
- Line 217: `aria/  # Aria Plugin (submodule, v1.13.0)` -- needs v1.14.0
- Line 218: `skills/  # 36 Skills (33 user-facing + 3 internal)` -- should be 35 (30+5)
- Line 238: `Plugin Version: 1.13.0 (aria-plugin, 36 Skills + 11 Agents)` -- needs v1.14.0 + 35 Skills

### 6. aria/VERSION

```yaml
version_file: "1.13.0"
plugin_json: "1.13.0"
match: true (but both stale if v1.14.0 released)
```

**Additional issue in VERSION file**:
- Line 38: "Skills 总数: 36 (33 面向用户 + 3 内部)" -- incorrect, should be 35 (30+5)
- Line 39: "Skills 总数: 33 (30 面向用户 + 3 内部)" -- contradicts line 38; the 30+5 split is also wrong (30 user + 3 internal = 33, not matching 5 internal)
- Lines 38-39 have duplicate conflicting entries

### 7. aria/marketplace.json

```yaml
marketplace_version: "1.13.0"
marketplace_plugins_version: "1.13.0"
marketplace_description: "33个 Skills + 11个 Agents + Hooks系统"
plugin_json: "1.13.0"
version_match: true (but stale if v1.14.0 released)
skill_count_match: false (says 33, actual user-facing is 30)
```

### 8. aria/CHANGELOG.md

```yaml
latest_entry: "[1.13.0] - 2026-04-11"
expected: "[1.14.0] - 2026-04-12"  # if v1.14.0 was released
match: false (no v1.14.0 entry)
```

### 9. Agent Count

```yaml
agent_directories: 11
readme_agent_count: 11
match: true
```

Agent list: ai-engineer, api-documenter, backend-architect, code-reviewer, context-manager, knowledge-manager, legal-advisor, mobile-developer, qa-engineer, tech-lead, ui-ux-designer

---

## Root Cause Analysis

There are **two distinct issues**:

### Issue A: Skill Count Miscalculation (Pre-existing)

The "33 user-facing + 3 internal" count has been wrong since at least v1.13.0. The actual breakdown:

| Category | README Claims | Actual |
|----------|--------------|--------|
| User-facing | 33 | 30 |
| Internal | 3 | 5 |
| Total | 36 | 35 |

The 3 internal skills counted by README are: config-loader, audit-engine, arch-common.
The 2 additional internal skills not counted: agent-router (user-invocable: false), agent-team-audit (user-invocable: false).

This discrepancy predates v1.14.0 and affects all version files.

### Issue B: v1.14.0 Version Not Propagated

If v1.14.0 has been released with 3 new Skills, none of the version files reflect this:

| File | Current | Expected |
|------|---------|----------|
| plugin.json | 1.13.0 | 1.14.0 |
| marketplace.json | 1.13.0 | 1.14.0 |
| aria/VERSION | 1.13.0 | 1.14.0 |
| aria/README.md | 1.13.0 | 1.14.0 |
| aria/README.zh.md | 1.11.1 | 1.14.0 |
| aria/CHANGELOG.md | no 1.14.0 entry | needs new entry |
| Main README.md badge | v1.13.0 | v1.14.0 |
| Main VERSION | v1.13.0 (plugin) | v1.14.0 |

If 3 new skills were added in v1.14.0, the corrected counts would be:
- Total directories: 35 + 3 = 38 (assuming new skills are user-facing)
- User-facing: 30 + 3 = 33
- Internal: 5
- Corrected label: "33 user-facing + 5 internal"

**Note**: The 3 new v1.14.0 skills are NOT present in the current skill directories (only 35 exist). This suggests the aria submodule pointer has not been updated to the v1.14.0 release commit yet.

---

## Recommendations

### Priority 1 (Error — must fix before release)

1. **Update aria submodule pointer** to v1.14.0 release commit (if published in aria-plugin repo)
2. **Fix all version numbers** across version files to 1.14.0 (per version release checklist in CLAUDE.md)
3. **Fix internal skill count** from 3 to 5 everywhere (agent-router + agent-team-audit are user-invocable: false)
4. **Add CHANGELOG.md entry** for v1.14.0
5. **Update aria/README.zh.md** — severely outdated (v1.11.1), missing 3 categories of skills

### Priority 2 (Warning — should fix)

6. **Update main README.md badge** to v1.14.0
7. **Update main README.md** project structure section and Project Status section
8. **Fix VERSION file** duplicate/conflicting skill count lines (lines 38-39)
9. **Update marketplace.json description** skill count

### Priority 3 (Info)

10. **Skill list in aria/README.md (EN)** is complete for current 35 skills — will need 3 new entries for v1.14.0

---

## Output (Phase 1.8 Structured)

```yaml
readme_status:
  root:
    exists: true
    version_match: true  # badge=1.13.0, plugin.json=1.13.0 (but both stale)
    badge:
      version_match: true  # 1.13.0 = 1.13.0
      plugin_version: "1.13.0"
      badge_version: "v1.13.0"
      stale: true  # user reports v1.14.0 released
    date_match: N/A  # no date in main README header
    skill_count_match: false
    skill_count_actual: 30  # user-facing (excluding 5 internal)
    skill_count_readme: 33  # README claims 33 user-facing
    suggestion: "Update badge to v1.14.0, fix skill count to 30 user-facing + 5 internal (35 total)"
  submodules:
    aria:
      exists: true
      readme_en:
        version_match: true  # 1.13.0 = 1.13.0 (both stale)
        plugin_version: "1.13.0"
        readme_version: "1.13.0"
        skill_count_match: false
        skill_count_actual: 30
        skill_count_readme: 33
        internal_count_actual: 5
        internal_count_readme: 3
        skill_list_missing: []  # all 35 current skills listed
        suggestion: "Fix to 30 user-facing + 5 internal, update version to 1.14.0"
      readme_zh:
        version_match: false
        plugin_version: "1.13.0"
        readme_version: "1.11.1"
        skill_count_match: true  # says 30, actual user-facing is 30
        skill_list_missing:
          - project-analyzer
          - agent-gap-analyzer
          - agent-creator
          - audit-engine
        suggestion: "Update version to 1.14.0, add missing v1.13.0+ skills and Project Adaptation category"
  badge:
    version_match: true  # both 1.13.0, but stale
    stale: true
  version_files:
    plugin_json: "1.13.0"
    marketplace_json: "1.13.0"
    version_file: "1.13.0"
    changelog_latest: "1.13.0"
    all_consistent: true  # among themselves, but all stale
    expected: "1.14.0"  # per user report
```
