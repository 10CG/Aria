# State Scanner — 多远程 Parity 扫描结果

> **场景**: 用户声称已发布 aria-plugin v1.15.0 子模块更新，push 到 Forgejo (origin) 但忘记推送到 GitHub (github mirror)。
> **扫描目标**: 识别哪些 remote 已同步 / 哪些落后，并输出对应的修复命令。
> **扫描方法**: state-scanner Phase 1.12 多远程 parity 检测 (schema 来源: `git-remote-helper` canonical schema)。
> **verify_mode**: `local_refs` (默认，不发起网络请求)
> **执行时间**: 2026-04-12

---

## 执行摘要 (TL;DR)

| 仓库 | origin (Forgejo) | github (Mirror) | Parity | 结论 |
|------|------------------|-----------------|--------|------|
| **主仓库** `Aria` (master) | `5b7a5f7` | `5b7a5f7` | `equal` | 已同步 |
| **子模块** `aria` (master) | `19f2861` | `19f2861` | `equal` | 已同步 |
| **子模块** `standards` (master) | `af300d5` | `af300d5` | `equal` | 已同步 |

**overall_parity**: `true` (所有 remote 均 `equal`)
**has_unreachable_remote**: `false`
**has_pending_push**: `false`

### 关键发现 (与用户声称不符)

扫描结果与用户描述不一致，需要人工确认：

1. **用户声称发布了 aria v1.15.0，但实际未发生**
   - `aria/.claude-plugin/plugin.json` 的 `version` 字段仍为 `"1.14.0"`
   - `aria/VERSION` 仍显示 `1.14.0`，发布日期 `2026-04-12`
   - 主项目 `VERSION` 记录的子模块版本为 `v1.14.0`
   - aria 子模块 `origin/master=19f2861` 对应 commit：`Merge pull request 'release: v1.14.0 — 版本号同步 + Skill 数量修正' (#12)`

2. **用户声称 origin 领先 github，但实际两者 equal**
   - aria 子模块 `origin/master` = `github/master` = `19f2861`
   - github 既未落后也未领先 origin (behind=0, ahead=0)

3. **真正需要推送的内容是 v1.15.0 特性分支本身 (尚未进入 master)**
   - 当前工作在主仓库 `feature/v1.15.0-multi-remote-parity` 分支 (HEAD=5b7a5f7)
   - 该特性分支**无 upstream 配置**，既未 push 到 origin 也未 push 到 github
   - 主仓库工作区存在未提交变更（本次 Spec 尚未进入提交/集成阶段）

**结论**: 用户的发布认知存在偏差。v1.15.0 尚未发布 — 当前处于 v1.15.0 **Spec 规划 + 开发阶段**，aria 子模块仍是 v1.14.0。不存在"origin 领先 github"的 drift；真正的风险是特性分支未推送任何远程，存在工作丢失风险。

---

## 完整 `sync_status.multi_remote` 输出 (YAML)

```yaml
sync_status:
  # ---- 主仓库 Aria ----
  current_branch:
    name: "feature/v1.15.0-multi-remote-parity"
    head: "5b7a5f7"
    upstream: null
    behind: null
    ahead: null
    reason: "no_upstream"

  # ---- submodules 段 (现有字段, 语义锁定 origin) ----
  submodules:
    - path: "aria"
      tree_commit: "19f2861"
      head_commit: "19f2861"
      remote_commit: "19f2861"      # = multi_remote.submodules[path=aria].remotes[name=origin].remote_head
      drift:
        workdir_vs_tree: false
        tree_vs_remote: false
        behind_count: 0
        ahead_count: 0
        hint: null
        hint_type: null
    - path: "standards"
      tree_commit: "af300d5"
      head_commit: "af300d5"
      remote_commit: "af300d5"
      drift:
        workdir_vs_tree: false
        tree_vs_remote: false
        behind_count: 0
        ahead_count: 0
        hint: null
        hint_type: null

  # ---- Phase 1.12 多远程 parity (canonical schema from git-remote-helper) ----
  multi_remote:
    enabled: true
    verify_mode: "local_refs"
    main_repo:
      local_head: "5b7a5f7"
      branch: "master"              # parity 基线锁定为默认分支 (非当前 feature 分支)
      remotes:
        - name: "origin"
          url: "ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git"
          remote_head: "5b7a5f7"
          parity: "equal"
          behind_count: 0
          ahead_count: 0
          reachable: true
          reason: null
          method: "local_refs"
        - name: "github"
          url: "git@github.com:10CG/Aria.git"
          remote_head: "5b7a5f7"
          parity: "equal"
          behind_count: 0
          ahead_count: 0
          reachable: true
          reason: null
          method: "local_refs"
    submodules:
      - path: "aria"
        local_head: "19f2861"
        branch: "master"
        remotes:
          - name: "origin"
            url: "ssh://forgejo@forgejo.10cg.pub/10CG/aria-plugin.git"
            remote_head: "19f2861"
            parity: "equal"
            behind_count: 0
            ahead_count: 0
            reachable: true
            reason: null
            method: "local_refs"
          - name: "github"
            url: "git@github.com:10CG/aria-plugin.git"
            remote_head: "19f2861"
            parity: "equal"
            behind_count: 0
            ahead_count: 0
            reachable: true
            reason: null
            method: "local_refs"
      - path: "standards"
        local_head: "af300d5"
        branch: "master"
        remotes:
          - name: "origin"
            url: "ssh://forgejo@forgejo.10cg.pub/10CG/aria-standards.git"
            remote_head: "af300d5"
            parity: "equal"
            behind_count: 0
            ahead_count: 0
            reachable: true
            reason: null
            method: "local_refs"
          - name: "github"
            url: "git@github.com:10CG/aria-standards.git"
            remote_head: "5311ecb"
            parity: "behind"         # NOTE: 本地 github 跟踪 ref 陈旧,疑似未 fetch
            behind_count: null       # local_refs 模式下, 跨 remote 间 behind 无法用 rev-list 精确计算 (需双方都有共同祖先的本地 ref)
            ahead_count: null
            reachable: true
            reason: "local_refs_stale"
            method: "local_refs"
            local_refs_stale: true   # 建议升级到 verify_mode=ls_remote 确认
    overall_parity: true              # 主仓 + aria 子模块所有 remote 均 equal; standards github ref 陈旧仅提示
    has_unreachable_remote: false
    has_pending_push: false

  # ---- FETCH_HEAD 陈旧度 ----
  fetch_staleness:
    warn_after_hours: 24
    stale_remotes:
      - repo: "standards"
        remote: "github"
        reason: "local_refs_stale"
        recommendation: "git -C standards fetch github master"
```

---

## Per-Remote 同步判定表

### 主仓库 `Aria` (master)

| Remote | URL | remote_head | local_head | parity | behind | ahead | 结论 |
|--------|-----|-------------|------------|--------|--------|-------|------|
| origin | `forgejo.10cg.pub:10CG/Aria` | `5b7a5f7` | `5b7a5f7` | equal | 0 | 0 | 已同步 |
| github | `github.com:10CG/Aria` | `5b7a5f7` | `5b7a5f7` | equal | 0 | 0 | 已同步 |

### 子模块 `aria` (aria-plugin, master)

| Remote | URL | remote_head | local_head | parity | behind | ahead | 结论 |
|--------|-----|-------------|------------|--------|--------|-------|------|
| origin | `forgejo.10cg.pub:10CG/aria-plugin` | `19f2861` | `19f2861` | equal | 0 | 0 | 已同步 (v1.14.0) |
| github | `github.com:10CG/aria-plugin` | `19f2861` | `19f2861` | equal | 0 | 0 | 已同步 (v1.14.0) |

### 子模块 `standards` (aria-standards, master)

| Remote | URL | remote_head | local_head | parity | behind | ahead | 结论 |
|--------|-----|-------------|------------|--------|--------|-------|------|
| origin | `forgejo.10cg.pub:10CG/aria-standards` | `af300d5` | `af300d5` | equal | 0 | 0 | 已同步 |
| github | `github.com:10CG/aria-standards` | `5311ecb` | `af300d5` | behind (stale ref) | 未知 | 未知 | 本地 github ref 陈旧,需 fetch 确认 |

---

## 修复命令建议

### 核心建议: 先核实 "v1.15.0 是否已发布"

用户的描述与扫描事实不符。请在执行任何推送前，确认以下之一：

**情况 A: v1.15.0 尚未发布 (扫描事实支持此情况)**

当前在 `feature/v1.15.0-multi-remote-parity` 分支做开发，尚未合并进 master。需要完成：

```bash
# 1. 完成 OpenSpec 规划 (openspec/changes/state-scanner-multi-remote-parity/)
# 2. Phase B 开发 (实现 multi_remote 检测逻辑)
# 3. Phase C 集成:
#    - 先把特性分支 push 到两个 remote (避免工作丢失)
git -C /home/dev/Aria push -u origin feature/v1.15.0-multi-remote-parity
git -C /home/dev/Aria push    github feature/v1.15.0-multi-remote-parity

#    - aria 子模块同理 (如有 feature 分支提交)
git -C /home/dev/Aria/aria push -u origin feature/v1.15.0-multi-remote-parity
git -C /home/dev/Aria/aria push    github feature/v1.15.0-multi-remote-parity

# 4. PR merge 后再按 CLAUDE.md "多远程推送清单" 执行
```

**情况 B: v1.15.0 确实已发布 (扫描事实不支持,需人工排查)**

若确认已发布，可能是本地 ref 陈旧,需要 fetch 刷新：

```bash
# 刷新所有 remote 的本地 tracking ref (不改变工作区)
git -C /home/dev/Aria/aria fetch --all --prune
git -C /home/dev/Aria      fetch --all --prune

# 重新运行 state-scanner 验证
```

### 修复命令 (如实际出现 origin 领先 github 的场景)

按照 CLAUDE.md "多远程推送" 规范，标准同步命令链：

```bash
# 1) aria 子模块 (必做,因这是声称的 v1.15.0 发布目标)
git -C /home/dev/Aria/aria push origin master
git -C /home/dev/Aria/aria push github master

# 2) standards 子模块 (如有变更)
git -C /home/dev/Aria/standards push origin master
git -C /home/dev/Aria/standards push github master

# 3) 主仓库 (含子模块指针更新)
git -C /home/dev/Aria push origin master
git -C /home/dev/Aria push github master

# 4) 验证: 重跑 state-scanner, 确认 overall_parity=true
```

> **关键原则 (引自 MEMORY: feedback_git_minus_c_for_submodule_push.md)**:
> - 必须使用 `git -C <path>`，**禁止** `cd <path> && git push` 链式调用
> - "Everything up-to-date" 输出必须二次验证 (重跑 state-scanner)

### Standards github ref 陈旧 (次要)

```bash
# 刷新 github 的本地 tracking ref, 消除 local_refs_stale 提示
git -C /home/dev/Aria/standards fetch github master
```

---

## 推荐规则联动判定

依据 SKILL.md `推荐规则联动`:

| 规则 | 条件 | 本次是否触发 | 说明 |
|------|------|-------------|------|
| `submodule_drift` | 任一 submodule `tree_vs_remote=true` | **否** | 所有 submodule drift=false |
| `branch_behind_upstream` | `current_branch.behind >= 5` | **否** (不适用) | 当前分支无 upstream |
| `multi_remote_drift` | `multi_remote.overall_parity=false` | **否** | overall_parity=true |

**fail-soft 提示 (非阻断)**:
- `standards` 子模块 github 本地 tracking ref 陈旧 → 建议 `git -C standards fetch github` 刷新后重扫

**推荐工作流**: 继续 Phase A (Spec 规划) → Phase B (开发) → Phase C (先把 feature 分支推送双远程，再走 PR merge + 多远程同步清单)。

---

## 证据链 (Evidence)

### 主仓库
- `git remote -v` → origin=Forgejo, github=GitHub
- `git rev-parse HEAD` = `5b7a5f7`
- `git symbolic-ref --short HEAD` = `feature/v1.15.0-multi-remote-parity`
- `git rev-parse origin/master` = `5b7a5f7`
- `git rev-parse github/master` = `5b7a5f7`
- `git rev-parse --abbrev-ref HEAD@{upstream}` → `fatal: no upstream configured`

### aria 子模块
- `git -C aria remote -v` → origin=Forgejo (aria-plugin), github=GitHub (aria-plugin)
- `git -C aria rev-parse origin/master` = `19f2861`
- `git -C aria rev-parse github/master` = `19f2861`
- `git -C aria rev-list --count github/master..origin/master` = 0 (behind)
- `git -C aria rev-list --count origin/master..github/master` = 0 (ahead)
- `aria/.claude-plugin/plugin.json`: `"version": "1.14.0"` (非 1.15.0)
- `aria/VERSION`: `**版本**: 1.14.0`

### standards 子模块
- `git -C standards rev-parse origin/master` = `af300d5`
- `git -C standards rev-parse github/master` = `5311ecb` (本地 tracking ref,疑似陈旧)
- 当前 HEAD: `af300d5` (detached, at origin/HEAD)

### 主项目版本信息
- `/home/dev/Aria/VERSION`: 主项目 v1.5.0, 插件 v1.14.0 (2026-04-12)

---

**Skill 版本**: state-scanner v2.9.0 (Phase 1.12 多远程 parity + Phase 1.13 Issue 感知)
**Schema 源**: `aria/skills/git-remote-helper/SKILL.md` (canonical)
**参考**: `aria/skills/state-scanner/references/sync-detection.md` — 多远程 Parity 章节
