# State Scanner — Phase 1.13 Issue Scan Report

**Generated**: 2026-04-15T10:40:26Z
**Branch**: feature/aria-2.0-m0-prerequisite
**Skill Version**: state-scanner v2.10 (aria-plugin v1.16.0)
**Scan Mode**: scan_submodules=true (meta-repo mode)
**Platform**: Forgejo (forgejo.10cg.pub)
**Data Source**: live (freshly fetched from API)

---

## Phase 1.13 Execution Summary

```yaml
issue_status:
  fetched_at: "2026-04-15T10:40:26Z"
  source: live
  fetch_error: null
  warning: null
  platform: forgejo
  open_count: 5        # total across all repos
  repos:
    "10CG/Aria":
      platform: forgejo
      source: live
      fetch_error: null
      open_count: 2
    "10CG/aria-plugin":
      platform: forgejo
      source: live
      fetch_error: null
      open_count: 2
    "10CG/aria-standards":
      platform: forgejo
      source: live
      fetch_error: null
      open_count: 0
    "10CG/aria-orchestrator":
      platform: forgejo
      source: live
      fetch_error: null
      open_count: 1
  label_summary: {}    # no labels assigned to any issue
```

---

## All Open Issues (5 total across 4 repos)

### Repo: 10CG/Aria (main repo) — 2 open issues

| # | Title | Labels | URL | Linked OpenSpec | Linked US |
|---|-------|--------|-----|-----------------|-----------|
| #16 | [US-020] Aria 2.0 M0 — 前置验证与架构定稿 | (none) | https://forgejo.10cg.pub/10CG/Aria/issues/16 | `aria-2.0-m0-prerequisite` (heuristic) | US-020 |
| #5 | [Feature] Pulse 项目集成 — AI-native 通讯层 (Matrix + Conduit + Element) | (none) | https://forgejo.10cg.pub/10CG/Aria/issues/5 | null | null |

---

### Repo: 10CG/aria-plugin (submodule: aria/) — 2 open issues

| # | Title | Labels | URL | Linked OpenSpec | Linked US |
|---|-------|--------|-----|-----------------|-----------|
| #18 | feat(estimator): 引入 Token × Attention 双主轴工作量估算 — 替代 4-8h 人工时假设，适配单人 + Claude Code 工作流 | (none) | https://forgejo.10cg.pub/10CG/aria-plugin/issues/18 | null | null |
| #17 | feat(audit-engine): 多轮挑战循环加固 — 新增"原始目的锚定"(Drift Guard) 防偏移检查 | (none) | https://forgejo.10cg.pub/10CG/aria-plugin/issues/17 | null | null |

---

### Repo: 10CG/aria-standards (submodule: standards/) — 0 open issues

No open issues found.

---

### Repo: 10CG/aria-orchestrator (submodule: aria-orchestrator/) — 1 open issue

| # | Title | Labels | URL | Linked OpenSpec | Linked US |
|---|-------|--------|-----|-----------------|-----------|
| #1 | [Idea] 轻量化 Hermes — 自研精简版替代完整 Hermes Agent | (none) | https://forgejo.10cg.pub/10CG/aria-orchestrator/issues/1 | null | null |

---

## Flat Aggregated View (all 5 items)

```yaml
items:
  - number: 16
    title: "[US-020] Aria 2.0 M0 — 前置验证与架构定稿"
    labels: []
    url: "https://forgejo.10cg.pub/10CG/Aria/issues/16"
    repo: "10CG/Aria"
    linked_openspec: "aria-2.0-m0-prerequisite"
    linked_us: "US-020"
    heuristic: true

  - number: 5
    title: "[Feature] Pulse 项目集成 — AI-native 通讯层 (Matrix + Conduit + Element)"
    labels: []
    url: "https://forgejo.10cg.pub/10CG/Aria/issues/5"
    repo: "10CG/Aria"
    linked_openspec: null
    linked_us: null
    heuristic: true

  - number: 18
    title: "feat(estimator): 引入 Token x Attention 双主轴工作量估算"
    labels: []
    url: "https://forgejo.10cg.pub/10CG/aria-plugin/issues/18"
    repo: "10CG/aria-plugin"
    linked_openspec: null
    linked_us: null
    heuristic: true

  - number: 17
    title: "feat(audit-engine): 多轮挑战循环加固 — 新增原始目的锚定(Drift Guard)"
    labels: []
    url: "https://forgejo.10cg.pub/10CG/aria-plugin/issues/17"
    repo: "10CG/aria-plugin"
    linked_openspec: null
    linked_us: null
    heuristic: true

  - number: 1
    title: "[Idea] 轻量化 Hermes — 自研精简版替代完整 Hermes Agent"
    labels: []
    url: "https://forgejo.10cg.pub/10CG/aria-orchestrator/issues/1"
    repo: "10CG/aria-orchestrator"
    linked_openspec: null
    linked_us: null
    heuristic: true
```

---

## Phase 1.11 Custom Check Result

The issue-cache-freshness check in .aria/state-checks.yaml now passes:

```
custom_checks:
  configured: true
  total: 1
  passed: 1
  failed: 0
  results:
    - name: "issue-cache-freshness"
      status: pass
      severity: warning
      output: "OK"
```

Cache written to .aria/cache/issues.json at 2026-04-15T10:40:26Z.

---

## Triage Summary

Total open issues: 5 across 4 repos.
No blocker/critical labels detected — open_blocker_issues rule does NOT trigger.

| Priority | Repo | Issue # | Title | Action |
|----------|------|---------|-------|--------|
| Active | 10CG/Aria | #16 | [US-020] Aria 2.0 M0 | In-progress — linked to current branch and OpenSpec |
| Backlog | 10CG/Aria | #5 | Pulse 集成 | Feature idea, no active Spec |
| Backlog | 10CG/aria-plugin | #18 | Token x Attention Estimator | New feature idea, no active Spec |
| Backlog | 10CG/aria-plugin | #17 | Drift Guard for audit-engine | Enhancement proposal, no active Spec |
| Deferred | 10CG/aria-orchestrator | #1 | 轻量化 Hermes | Decision record, "暂不行动" per issue body |
