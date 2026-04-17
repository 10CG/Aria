---
skill_version: state-scanner v2.9.0 (pre-change / old_skill)
eval: eval-meta-repo-issue-discovery
generated_at: 2026-04-15T10:40:37Z
---

```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝
```

## 阶段 0: 中断检测

`.aria/workflow-state.json` 不存在 — 跳过，进入阶段 1。

---

## 阶段 1: 状态收集

### Git 状态

```yaml
git:
  current_branch: feature/aria-2.0-m0-prerequisite
  uncommitted_changes: 1  # 仅 untracked: aria-plugin-benchmarks/ab-results/...
  staged_files: []
  unstaged_files: []
  untracked_dirs:
    - aria-plugin-benchmarks/ab-results/2026-04-15-state-scanner-submodule-issue-scan/
  recent_commits:
    - 1409265 feat(openspec): 新立 state-scanner-submodule-issue-scan Level 2 Spec + Aria 项目级开启
    - 95c91be feat(openspec): M0 T1 回填 + T5.1/T5.2/T5.3 完成
    - 32422df feat(state-scanner): L1 探针 + L3 Spec draft — 防止 Phase 1.13 漏跑
    - de10636 chore: aria-orchestrator submodule pointer → 51d7bae (AD3 回填)
    - 1361cf9 feat(openspec): T5.4 AD3 回填完成
```

### 阶段 1.5: 需求状态

```yaml
requirements_status:
  configured: true
  prd_exists: true
  prd_path: docs/requirements/prd-aria-v2.md
  prd_status: "Approved (Draft → Approved 2026-04-11)"
  stories:
    total: 13
    ready: 1       # US-020
    in_progress: 1 # US-007
    done: 10       # US-001,002,004,005,006,008,009,010,011,012
    pending: 1     # US-003
```

### 阶段 1.6: OpenSpec 状态

```yaml
openspec_status:
  configured: true
  changes:
    total: 5
    draft: 5
    reviewed: 0
    approved: 0
    in_progress: 0
    complete: 0
    items:
      - id: "aria-2.0-m0-prerequisite"
        status: "Draft"
        path: "openspec/changes/aria-2.0-m0-prerequisite/proposal.md"
      - id: "aria-2.0-m0-spike-hermes"
        status: "Draft"
        path: "openspec/changes/aria-2.0-m0-spike-hermes/proposal.md"
      - id: "aria-2.0-silknode-integration-contract"
        status: "Draft (预留, 等待 US-022+ 消费)"
        path: "openspec/changes/aria-2.0-silknode-integration-contract/proposal.md"
      - id: "state-scanner-mechanical-enforcement"
        status: "Draft (待 L1 探针数据激活)"
        path: "openspec/changes/state-scanner-mechanical-enforcement/proposal.md"
      - id: "state-scanner-submodule-issue-scan"
        status: "Draft"
        path: "openspec/changes/state-scanner-submodule-issue-scan/proposal.md"
  archive:
    total: 52
    note: "52 已归档 Spec (见 openspec/archive/)"
  pending_archive: []
```

### 阶段 1.7: 架构状态

```yaml
architecture_status:
  exists: true
  path: docs/architecture/system-architecture.md
  status: Active
  version: "1.9.0"
  last_updated: "2026-04-12"
  parent_prd: prd-aria-v1.md
  chain_valid: true
  chain_issues: []
```

### 阶段 1.8: README 同步检查

```yaml
readme_status:
  root:
    exists: true
    version_match: true   # badge Plugin-v1.15.2 ✓
    date_match: true
    note: "README.md line 217 内联注释仍写 'v1.13.0'，但 badge 已正确为 v1.15.2"
  submodules:
    aria:
      exists: true
      version_match: true
      plugin_version: "v1.15.2"
      readme_version: "v1.15.2"
      skill_count_match: true
      skill_count_actual: 30
      skill_count_readme: 30
  badge:
    version_match: true
```

### 阶段 1.9: 插件依赖检测

```yaml
standards_status:
  registered: true
  initialized: true
```

### 阶段 1.10: 审计状态

```yaml
audit_status:
  enabled: false
  note: |
    audit.* 未在 .aria/config.json 中配置。
    最近审计报告: prd-review-2026-04-11T0700Z.md
    checkpoint: prd_review | verdict: PASS | converged: true
```

### 阶段 1.11: 自定义健康检查

```yaml
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

### 阶段 1.12: 本地/远程同步检测

```yaml
sync_status:
  remote_refs_age: "1m"
  has_remote: true
  shallow: false
  current_branch:
    name: "feature/aria-2.0-m0-prerequisite"
    upstream: "origin/feature/aria-2.0-m0-prerequisite"
    upstream_configured: true
    ahead: 0
    behind: 0
    diverged: false
    reason: null
  submodules:
    - path: "aria"
      tree_commit: "488e736"
      head_commit: "488e736"
      remote_commit: "36428b9"
      drift:
        workdir_vs_tree: false
        tree_vs_remote: true
        behind_count: 0
        ahead_count: 1
        hint_type: "push"   # ahead only — does NOT trigger submodule_drift rule
    - path: "aria-orchestrator"
      tree_commit: "825390e"
      head_commit: "825390e"
      remote_commit: "f051a7d"
      drift:
        workdir_vs_tree: false
        tree_vs_remote: true
        behind_count: 0
        ahead_count: 10
        hint_type: "push"   # ahead only — does NOT trigger submodule_drift rule
    - path: "standards"
      tree_commit: "791f05a"
      head_commit: "791f05a"
      remote_commit: "791f05a"
      drift:
        workdir_vs_tree: false
        tree_vs_remote: false
        behind_count: 0
        ahead_count: 0
        hint_type: null
  multi_remote:
    main_repo:
      local_head: "1409265"
      remotes:
        - name: "origin"
          parity: "equal"
        - name: "github"
          parity: "equal"
    submodules:
      - path: "aria"
        remotes:
          - name: "origin"
            parity: "ahead"
            ahead_count: 1
          - name: "github"
            parity: "ahead"
            ahead_count: 1
      - path: "aria-orchestrator"
        remotes:
          - name: "origin"
            parity: "ahead"
            ahead_count: 10
          - name: "github"
            parity: "ahead"
            ahead_count: 10
      - path: "standards"
        remotes:
          - name: "origin"
            parity: "equal"
          - name: "github"
            parity: "equal"
    overall_parity: true
    has_unreachable_remote: false
    has_pending_push: true
```

### 阶段 1.13: Issue 感知扫描

**配置**: `issue_scan.enabled: true`, `platform: "forgejo"`

**执行**:
1. enabled=true → 继续
2. 平台: 显式配置 `forgejo` (优先级 1)
3. CLI: `/home/dev/.npm-global/bin/forgejo` 可用
4. 缓存: `.aria/cache/issues.json` 不存在 → API 调用
5. API: `forgejo GET /repos/10CG/Aria/issues?state=open&type=issues&limit=20`
6. 返回 2 个 open issues
7. 启发式关联: 计算 linked_us 和 linked_openspec
8. 缓存写回: `.aria/cache/issues.json` (2026-04-15T10:40:37Z)

**安全边界 (pre-change 版本)**:
此版本仅扫描主仓库 `10CG/Aria`。
根据 `references/issue-scanning.md`:
> "不递归子模块 issues: 仅扫描主仓库 (git remote get-url origin)；子模块扫描为预留扩展点 (scan_submodule_issues)"

```yaml
issue_status:
  fetched_at: "2026-04-15T10:40:37Z"
  source: live
  fetch_error: null
  warning: null
  platform: forgejo
  open_count: 2
  items:
    - number: 16
      title: "[US-020] Aria 2.0 M0 — 前置验证与架构定稿"
      labels: []
      url: "https://forgejo.10cg.pub/10CG/Aria/issues/16"
      linked_openspec: null
      linked_us: "US-020"
      heuristic: true
      note: |
        body 含 "openspec/changes/aria-2.0-m0-prerequisite/" 但为 URL 路径格式，
        前缀为 "/" 被边界规则排除，linked_openspec 正确为 null
    - number: 5
      title: "[Feature] Pulse 项目集成 — AI-native 通讯层 (Matrix + Conduit + Element)"
      labels: []
      url: "https://forgejo.10cg.pub/10CG/Aria/issues/5"
      linked_openspec: null
      linked_us: null
      heuristic: true
  label_summary: {}
```

### 阶段 1.14: Forgejo 配置检测

```yaml
forgejo_config:
  forgejo_remote_detected: true
  instance: "forgejo.10cg.pub"
  config_status: "configured"
```

---

## 输出展示

```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝

📍 当前状态
───────────────────────────────────────────────────────────────
  分支: feature/aria-2.0-m0-prerequisite
  模块: Aria 方法论主项目
  变更: 仅 untracked benchmark 目录

📄 需求状态
───────────────────────────────────────────────────────────────
  配置状态: ✅ 已配置
  PRD: prd-aria-v2.md (Approved, 2026-04-11)
  User Stories: 13 个 (ready: 1, in_progress: 1, done: 10, pending: 1)

🏗️ 架构状态
───────────────────────────────────────────────────────────────
  System Architecture v1.9.0: ✅ Active | 需求链路: ✅ 完整

📋 OpenSpec 状态
───────────────────────────────────────────────────────────────
  活跃变更: 5 个 (全部 Draft) | 已归档: 52 个 | 待归档: 0 个

🛡️ 审计状态
───────────────────────────────────────────────────────────────
  审计系统: ⚪ 未启用 (config.json 未配置 audit.*)
  参考: 最近审计 prd-review-2026-04-11 — PASS (收敛)

🔧 自定义检查
───────────────────────────────────────────────────────────────
  ✅ issue-cache-freshness: OK

🔄 同步状态
───────────────────────────────────────────────────────────────
  当前分支: feature/aria-2.0-m0-prerequisite ✅ (origin + github 同步)
  远程引用: 1m 前同步
  子模块:
    ✅ standards: 同步 (origin + github)
    ℹ️  aria: 本地领先 1 commit (feature/state-scanner-submodule-issue-scan, 待 merge)
    ℹ️  aria-orchestrator: 本地领先 10 commits (feature/m0-t4-st1-hermes-analysis, 待 merge)
    注: 均为 ahead (has_pending_push)，不触发 submodule_drift 降级规则

🎫 Open Issues (主仓库: 10CG/Aria)
───────────────────────────────────────────────────────────────
  平台: Forgejo (10CG/Aria) — 2 open
  #16  [US-020] Aria 2.0 M0 — 前置验证与架构定稿
       → 关联 US: US-020 (启发式)
  #5   [Feature] Pulse 项目集成 — AI-native 通讯层 (Matrix + Conduit + Element)
  数据来源: live (2026-04-15T10:40:37Z) | ttl: 15m
  ⚠️  此版本 state-scanner 仅扫描主仓库。
       子模块仓库 (aria-plugin / aria-standards / aria-orchestrator)
       的 issue 未包含在此次扫描中。

🎯 推荐工作流
───────────────────────────────────────────────────────────────
  ➤ [1] feature-dev (推荐)
      理由: M0 前置工作进行中，有 5 个活跃 Draft Spec
  ○ [2] quick-fix
  ○ [3] full-cycle
  ○ [4] 自定义组合

🤔 选择 [1-4] 或输入自定义:
```

---

## Issue 汇总 (供 triage)

> **重要**: 此为 pre-change 版本 (state-scanner v2.9.0，无 scan_submodules 支持)。
> 仅扫描主仓库 `10CG/Aria`，子模块仓库 issue 未包含。

| # | 标题 | 仓库 | 关联 US | 关联 OpenSpec |
|---|------|------|---------|--------------|
| #16 | [US-020] Aria 2.0 M0 — 前置验证与架构定稿 | 10CG/Aria | US-020 | null |
| #5 | [Feature] Pulse 项目集成 — AI-native 通讯层 (Matrix + Conduit + Element) | 10CG/Aria | null | null |

**未扫描的子模块仓库** (pre-change 版本限制):
- `10CG/aria-plugin` — 未扫描 (N/A in this version)
- `10CG/aria-standards` — 未扫描 (N/A in this version)
- `10CG/aria-orchestrator` — 未扫描 (N/A in this version)
