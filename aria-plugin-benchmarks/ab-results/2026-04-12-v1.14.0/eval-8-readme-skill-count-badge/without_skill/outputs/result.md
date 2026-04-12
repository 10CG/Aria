# Eval 8: README Skill Count & Badge Consistency Audit

**Date**: 2026-04-12
**Target Version**: v1.14.0 (claimed by user)
**Mode**: without_skill (built-in knowledge only)

---

## 1. Ground Truth: Actual Directory Contents

### Skills (from `aria/skills/`)

**Total directories: 35**

1. agent-creator
2. agent-gap-analyzer
3. agent-router
4. agent-team-audit
5. api-doc-generator
6. arch-common
7. arch-scaffolder
8. arch-search
9. arch-update
10. aria-dashboard
11. aria-report
12. audit-engine
13. brainstorm
14. branch-finisher
15. branch-manager
16. commit-msg-generator
17. config-loader
18. forgejo-sync
19. openspec-archive
20. phase-a-planner
21. phase-b-developer
22. phase-c-integrator
23. phase-d-closer
24. progress-updater
25. project-analyzer
26. requesting-code-review
27. requirements-sync
28. requirements-validator
29. spec-drafter
30. state-scanner
31. strategic-commit-orchestrator
32. subagent-driver
33. task-planner
34. tdd-enforcer
35. workflow-runner

**Classification** (based on README descriptions):
- Internal (non-user-invocable): arch-common, config-loader, audit-engine = 3
- User-facing: 35 - 3 = 32
- Note: agent-team-audit is described as "disabled by default" but listed as internal in some places and user-facing in others

### Agents (from `aria/agents/`)

**Total: 11 files**

1. ai-engineer.md
2. api-documenter.md
3. backend-architect.md
4. code-reviewer.md
5. context-manager.md
6. knowledge-manager.md
7. legal-advisor.md
8. mobile-developer.md
9. qa-engineer.md
10. tech-lead.md
11. ui-ux-designer.md

---

## 2. plugin.json (Source of Truth)

**File**: `aria/.claude-plugin/plugin.json`
- **version**: `1.13.0`
- **description**: "33个 Skills + 11个 Agents + Hooks系统"

### ISSUE: Version not updated to v1.14.0

The user claims v1.14.0 was released, but plugin.json still shows `1.13.0`.

### ISSUE: Skill count in description is wrong

Description says "33个 Skills" but actual directory count is 35 total (32 user-facing + 3 internal). If counting agent-team-audit as user-facing (since it's not marked internal in English README), then 33 user-facing + 2 internal = 35, but that still doesn't add up cleanly. The description omits the total vs user-facing distinction.

---

## 3. File-by-File Audit

### 3.1 `aria/README.md` (English Plugin README)

| Item | README Value | Actual | Status |
|------|-------------|--------|--------|
| Version | 1.13.0 | plugin.json says 1.13.0 (should be 1.14.0) | STALE (not updated to 1.14.0) |
| Release date | 2026-04-11 | — | STALE if 1.14.0 released |
| Skill count (header) | "33 Skills + 11 Agents" | 35 dirs, 11 agents | MISMATCH |
| Skills detail | "33 user-facing + 3 internal" | 32 user-facing + 3 internal = 35 dirs | MISMATCH (claims 33+3=36 but only 35 dirs) |
| Skills listed | 36 skills listed in detail | 35 skill directories | MISMATCH |

**Skills listed in README but NOT in directory:**
- README claims 36 total (33 user-facing + 3 internal)
- Directory has 35 directories
- The README counts "agent-team-audit" separately (noted as "disabled by default, enable via .aria/config.json") outside the 3 internal, making it effectively a 4th special-status skill, pushing the README count to 36. But only 35 directories exist.

**Detailed skill list check in README:**
The README lists these skills:
- Ten-Step Cycle Core (9): state-scanner, workflow-runner, phase-a-planner, phase-b-developer, phase-c-integrator, phase-d-closer, spec-drafter, task-planner, progress-updater
- Collaborative Thinking (1): brainstorm
- Git Workflow (4): commit-msg-generator, strategic-commit-orchestrator, branch-manager, branch-finisher
- Dev Tools (4): subagent-driver, agent-router, tdd-enforcer, requesting-code-review
- Architecture Docs (5): arch-common, arch-search, arch-update, arch-scaffolder, api-doc-generator
- Requirements (4): requirements-validator, requirements-sync, forgejo-sync, openspec-archive
- Infrastructure (1): config-loader
- Visualization (1): aria-dashboard
- Project Adaptation (3): project-analyzer, agent-gap-analyzer, agent-creator
- Feedback (1): aria-report
- Audit System (2): audit-engine, agent-team-audit

**Total listed: 9+1+4+4+5+4+1+1+3+1+2 = 35**

So the README lists 35 skills in the detailed section, which matches the directory count. But the header says "33 user-facing + 3 internal" = 36 total, which is WRONG. It should say "32 user-facing + 3 internal" = 35 total, or if counting agent-team-audit as a separate category (disabled by default), then "31 user-facing + 3 internal + 1 disabled = 35".

**Missing skills from README (if any new skills were added for v1.14.0):**
The user claims 3 new skills were added for v1.14.0, but these do NOT appear in the skill directories yet. The directories still show 35 skills matching v1.13.0 content. Either:
- The new skills haven't been added to the `aria/` submodule yet, OR
- The submodule pointer hasn't been updated

### 3.2 `aria/README.zh.md` (Chinese Plugin README)

| Item | README Value | Actual | Status |
|------|-------------|--------|--------|
| Version | 1.11.1 | plugin.json: 1.13.0 | SEVERELY STALE |
| Release date | 2026-04-10 | — | STALE |
| Skill count (header) | "30 个 Skills + 11 个 Agents" | 35 dirs | SEVERELY STALE |
| Skills detail | "30 个面向用户 + 3 个内部" = 33 | 35 dirs | SEVERELY STALE |

**Missing from Chinese README (skills present in directory but not listed):**
1. aria-dashboard (added in v1.10.0)
2. project-analyzer (added in v1.13.0)
3. agent-gap-analyzer (added in v1.13.0)
4. agent-creator (added in v1.13.0)
5. audit-engine (internal, missing from list)

The Chinese README is stuck at v1.11.1 level and is missing at least 5 skills.

### 3.3 `README.md` (Main Project English README)

| Item | README Value | Actual | Status |
|------|-------------|--------|--------|
| Plugin badge | v1.13.0 | Should be v1.14.0 | STALE |
| Plugin version in text | "1.13.0" | Should be 1.14.0 | STALE |
| Skill count in text | "36 Skills (33 user-facing + 3 internal)" | 35 dirs | MISMATCH |
| Submodule version in tree | "v1.13.0" | Should be v1.14.0 | STALE |
| Project Version in status | "1.5.0" | — | May need update |
| Plugin Version in status | "1.13.0 (aria-plugin, 36 Skills + 11 Agents)" | 35 dirs; should be 1.14.0 | STALE + MISMATCH |

**Skills table check:**
The main README's Skills table lists skills in categories. Let me count:
- Cycle Core: 9
- Collaborative Thinking: 1
- Git Workflow: 4
- Dev Tools: 4
- Architecture Docs: 5
- Requirements: 4
- Project Adaptation: 3
- Feedback: 1
- Dashboard: 1
- Infrastructure: 3 (config-loader, audit-engine, agent-team-audit)

**Total: 9+1+4+4+5+4+3+1+1+3 = 35** (matches directory)

But the header says "33 user-facing + 3 internal" = 36, while the table only lists 35. Off by one.

### 3.4 `README.zh.md` (Main Project Chinese README)

| Item | README Value | Actual | Status |
|------|-------------|--------|--------|
| Plugin badge | v1.10.0 | Should be v1.14.0 | SEVERELY STALE |
| Plugin version in text | "1.10.0" | Should be 1.14.0 | SEVERELY STALE |
| Skill count | "27 个面向用户 + 2 个内部" = 29 | 35 dirs | SEVERELY STALE |
| Submodule version in tree | "v1.10.0" | Should be v1.14.0 | SEVERELY STALE |
| Project Version in status | "1.3.0" | Should be 1.5.0 | SEVERELY STALE |

**Missing from Chinese main README:** At least 6+ skills not listed (everything added since v1.10.0).

### 3.5 `README.ja.md` (Japanese README)

| Item | README Value | Actual | Status |
|------|-------------|--------|--------|
| Plugin badge | v1.7.2 | Should be v1.14.0 | SEVERELY STALE |

Minimal stub document, but badge version is far behind.

### 3.6 `README.ko.md` (Korean README)

| Item | README Value | Actual | Status |
|------|-------------|--------|--------|
| Plugin badge | v1.7.2 | Should be v1.14.0 | SEVERELY STALE |

Minimal stub document, but badge version is far behind.

### 3.7 `aria/.claude-plugin/marketplace.json`

| Item | Value | Actual | Status |
|------|-------|--------|--------|
| version | 1.13.0 | Should be 1.14.0 | STALE |
| plugins[0].version | 1.13.0 | Should be 1.14.0 | STALE |
| description | "33个 Skills" | 35 dirs (or 32 user-facing) | MISMATCH |

### 3.8 `aria/VERSION`

| Item | Value | Actual | Status |
|------|-------|--------|--------|
| 版本 | 1.13.0 | Should be 1.14.0 | STALE |
| Skills count | "36个, 33 面向用户 + 3 内部" | 35 dirs | MISMATCH |

### 3.9 `VERSION` (Main Project)

| Item | Value | Actual | Status |
|------|-------|--------|--------|
| Plugin version | v1.13.0 | Should be 1.14.0 | STALE |
| Skills total | "36 (33 面向用户 + 3 内部)" then contradicts with "33 (30 面向用户 + 3 内部)" | 35 dirs | CONTRADICTORY + MISMATCH |

Note: Main VERSION has two contradictory lines:
- Line 38: "Skills 总数: 36 (33 面向用户 + 3 内部)"
- Line 39: "Skills 总数: 33 (30 面向用户 + 3 内部)"
This is a clear internal contradiction.

### 3.10 `CLAUDE.md`

| Item | Value | Actual | Status |
|------|-------|--------|--------|
| 插件版本 | v1.10.0 | Should be v1.14.0 | SEVERELY STALE |
| 主项目版本 | v1.3.0 | Should be v1.5.0 | STALE |

---

## 4. Summary of All Issues Found

### Critical Issues

| # | File | Issue | Severity |
|---|------|-------|----------|
| 1 | `aria/.claude-plugin/plugin.json` | Version 1.13.0, not updated to 1.14.0 | CRITICAL |
| 2 | `aria/.claude-plugin/plugin.json` | Description says "33个 Skills" but 35 skill dirs exist | HIGH |
| 3 | `aria/.claude-plugin/marketplace.json` | Version 1.13.0, not 1.14.0; skill count wrong | CRITICAL |
| 4 | `aria/VERSION` | Version 1.13.0, not 1.14.0; claims 36 skills (33+3) but 35 dirs | CRITICAL |
| 5 | `aria/CHANGELOG.md` | No entry for v1.14.0 | CRITICAL |
| 6 | `VERSION` (main) | Plugin version 1.13.0; contradictory skill counts (36 vs 33) | HIGH |
| 7 | No new skill directories | User claims 3 new skills for v1.14.0 but only 35 dirs (same as v1.13.0) | CRITICAL |

### README Version Badge Issues

| # | File | Badge/Version | Expected | Gap |
|---|------|--------------|----------|-----|
| 1 | `aria/README.md` | 1.13.0 | 1.14.0 | 1 minor behind |
| 2 | `aria/README.zh.md` | 1.11.1 | 1.14.0 | 3 minors behind |
| 3 | `README.md` (main EN) | v1.13.0 badge | v1.14.0 | 1 minor behind |
| 4 | `README.zh.md` (main CN) | v1.10.0 badge | v1.14.0 | 4 minors behind |
| 5 | `README.ja.md` (main JA) | v1.7.2 badge | v1.14.0 | 7 minors behind |
| 6 | `README.ko.md` (main KO) | v1.7.2 badge | v1.14.0 | 7 minors behind |

### README Skill Count Issues

| # | File | Claimed Count | Actual Dirs | Delta |
|---|------|--------------|-------------|-------|
| 1 | `aria/README.md` | 33 user + 3 internal = 36 | 35 | +1 overcounted |
| 2 | `aria/README.zh.md` | 30 user + 3 internal = 33 | 35 | -2 undercounted |
| 3 | `README.md` (main EN) | 33 user + 3 internal = 36 | 35 | +1 overcounted |
| 4 | `README.zh.md` (main CN) | 27 user + 2 internal = 29 | 35 | -6 undercounted |

### Skill List Completeness

| # | File | Missing Skills |
|---|------|---------------|
| 1 | `aria/README.md` (EN) | Detailed list has 35 (matches dirs). Header count (36) is wrong. |
| 2 | `aria/README.zh.md` (CN) | Missing: aria-dashboard, project-analyzer, agent-gap-analyzer, agent-creator, audit-engine |
| 3 | `README.md` (main EN) | Table lists 35 (matches dirs). Header count (36) is wrong. |
| 4 | `README.zh.md` (main CN) | Missing: aria-dashboard, aria-report, project-analyzer, agent-gap-analyzer, agent-creator, audit-engine, agent-team-audit |

### Internal Contradictions

| # | Location | Contradiction |
|---|----------|--------------|
| 1 | `VERSION` (main) lines 38-39 | "Skills 总数: 36" immediately followed by "Skills 总数: 33" |
| 2 | `CLAUDE.md` | Plugin version v1.10.0 vs plugin.json 1.13.0 |
| 3 | `aria/README.md` header vs detail | Header: "33+3=36", Detail list: 35 items |

---

## 5. Recommendations

1. **Update plugin.json to v1.14.0** and add the 3 new skill directories (or verify they exist if submodule needs updating)
2. **Synchronize all version files** (plugin.json, marketplace.json, VERSION, CHANGELOG.md, all READMEs) to v1.14.0
3. **Fix skill count** across all files to match actual directory count (currently 35; will be 38 if 3 new skills added)
4. **Update Chinese plugin README** (`aria/README.zh.md`) -- it's 3 versions behind and missing 5 skills
5. **Update Chinese main README** (`README.zh.md`) -- it's 4 versions behind, badge at v1.10.0, skill count at 29
6. **Update Japanese and Korean READMEs** -- badges stuck at v1.7.2
7. **Fix contradictory skill counts** in main `VERSION` file (lines 38-39)
8. **Update CLAUDE.md** plugin version from v1.10.0 to current
9. **Add CHANGELOG entry** for v1.14.0

---

## 6. Verdict

**Consistency Score: 2/10 (Poor)**

The version information across the project is significantly fragmented. The English files are 1 version behind (at v1.13.0), the Chinese files are 3-4 versions behind, and the Japanese/Korean files are 7 versions behind. The skill count is inconsistent across every file, with overcounts and undercounts depending on the document. The main VERSION file contains a self-contradiction on consecutive lines. The CLAUDE.md project context (which AI agents read as their primary orientation) is 4+ minor versions behind.

The user's suspicion is confirmed: README skill counts, skill lists, and badge versions are NOT consistent with the actual state of the project.
