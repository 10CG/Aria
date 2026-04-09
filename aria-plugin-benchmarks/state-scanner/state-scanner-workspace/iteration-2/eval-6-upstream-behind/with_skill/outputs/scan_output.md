# Aria 项目状态扫描 (state-scanner v2.9.0)

**扫描目标**: `/home/dev/Aria`
**当前分支**: `feature/state-scanner-v2.9`
**扫描时间**: 2026-04-09

---

## 同步状态 (Phase 1.12)

```
同步状态
───────────────────────────────────────────────────────────────
  当前分支: feature/state-scanner-v2.9 (无 upstream 配置)
  远程引用: 2 hours ago 同步
  子模块:
    ⚠️  aria: 主仓库记录与远程 origin/HEAD 不一致 (本地领先 2 commits，非落后)
    ✅ standards: 同步
    ⚠️  aria-orchestrator: 主仓库记录与远程 origin/HEAD 不一致 (本地领先 2 commits，非落后)

  注意: 子模块 aria 的工作目录存在未提交修改 (git status 显示 " m aria")
```

### 结构化输出

```yaml
sync_status:
  has_remote: true
  remote_refs_age: "2 hours ago"
  shallow: false
  current_branch:
    name: "feature/state-scanner-v2.9"
    upstream: null
    upstream_configured: false
    ahead: null
    behind: null
    diverged: null
    reason: "no_upstream"
  submodules:
    - path: "aria"
      tree_commit: "5023bed"
      head_commit: "5023bed"
      remote_commit: "80b268a"
      remote_commit_source: "origin_HEAD"
      drift:
        workdir_vs_tree: false       # submodule pointer 一致 (' m' 来自内部未提交修改)
        tree_vs_remote: true         # tree_commit != remote_commit
        behind_count: 0              # 实际: 本地领先 2 commits (rev-list tree..remote == 0)
        hint: "git submodule update --remote aria"
    - path: "standards"
      tree_commit: "5311ecb"
      head_commit: "5311ecb"
      remote_commit: "5311ecb"
      remote_commit_source: "origin_HEAD"
      drift:
        workdir_vs_tree: false
        tree_vs_remote: false
        behind_count: null
        hint: null
    - path: "aria-orchestrator"
      tree_commit: "c31a85c"
      head_commit: "c31a85c"
      remote_commit: "694ee5d"
      remote_commit_source: "origin_HEAD"
      drift:
        workdir_vs_tree: false
        tree_vs_remote: true
        behind_count: 0              # 实际: 本地领先 2 commits
        hint: "git submodule update --remote aria-orchestrator"
```

---

## 用户问题直接回答

> **Q**: 我的 feature 分支已经开发几天了，是否落后 upstream？是否需要 `git pull`？

**直接回答: 无需执行 `git pull`（因为没有 upstream 可以 pull）**

### 原因解释

1. **当前分支没有配置 upstream**
   - `git rev-parse --abbrev-ref --symbolic-full-name @{u}` 返回空
   - 这是 Phase 1.12 fail-soft 四状态之一：`reason: "no_upstream"`
   - 因此 `ahead/behind` 均为 `null`，**无法**直接判断"落后 upstream"

2. **但是——你可以手动与 `origin/master` 对比**
   - `feature/state-scanner-v2.9` 当前 HEAD: `1445da5`
   - `origin/master` 当前 HEAD: `1445da5`
   - **两者相同**，即 feature 分支与远程 master 完全同步（0 ahead / 0 behind）
   - 这说明从分支创建到现在，你的 feature 分支的基线没有落后

3. **最后一次 `git fetch` 距今 2 小时前**
   - `FETCH_HEAD` 时间戳正常，未触发 `warn_after_hours=24` 告警
   - 但既然你"已经开发几天了"，建议主动 fetch 一次以确保远程视图最新

4. **环境检测结果**
   - `shallow: false` → 非浅克隆，ahead/behind 计算路径畅通（如果有 upstream）
   - `git branch --show-current` 返回非空 → 非 detached HEAD
   - `git rev-parse --is-shallow-repository` 返回 `false`（git 2.39.5，走主路径，非 fallback）

### 推荐操作

```bash
# 1. 先 fetch 刷新远程视图 (主动刷新 FETCH_HEAD)
git fetch --all --prune

# 2. 再次对比（不需要 pull，只是验证）
git rev-list --count feature/state-scanner-v2.9..origin/master  # 应返回 0
git rev-list --count origin/master..feature/state-scanner-v2.9  # 应返回 0

# 3. （可选）为 feature 分支配置 upstream，以便后续 state-scanner 自动检测
git branch --set-upstream-to=origin/master feature/state-scanner-v2.9
# 或推送到远程并跟踪:
# git push -u origin feature/state-scanner-v2.9
```

---

## 推荐规则评估

### `branch_behind_upstream` (priority 1.98)

**状态: 未触发 (SKIP)**

触发条件检查:
- `sync_status.current_branch.behind >= 5` → `behind == null` → **skip**
- `sync_status.current_branch.upstream_configured == true` → `false` → **skip**
- `skip_conditions` 命中: `"behind == null"` 与 `"reason != null"` (reason=no_upstream)

**结论**: 本规则跳过。分支未配置 upstream，无法判定是否落后，**不降级推荐**，也**不提示 `git pull`**。
这是 fail-soft 的正确行为 — 宁可不推荐，也不误导用户对一个不存在的 upstream 执行 pull。

### `submodule_drift` (priority 1.97)

**状态: 触发 (降级提示)**

- `aria`: `drift.tree_vs_remote == true` → 命中
- `aria-orchestrator`: `drift.tree_vs_remote == true` → 命中

但需注意 `behind_count == 0`：主仓库记录的子模块 commit **领先**于远程 origin/HEAD，而非落后。
这是因为本地已经在子模块中 commit 了新提交但还未推送到远程 (或远程 origin/HEAD 缓存陈旧)。

```
子模块 aria: 主仓库 HEAD 记录 5023bed, 远程 origin/HEAD 80b268a
  → 本地领先 2 commits: 5023bed "feat(us-006): state-scanner v2.8.0..."
                        e0240cf "fix(version): sync VERSION file..."

子模块 aria-orchestrator: 主仓库 HEAD 记录 c31a85c, 远程 origin/HEAD 694ee5d
  → 本地领先 2 commits (需要先 git push 子模块, 而非 git pull)
```

**实际建议** (与规则默认 hint 不同):
```bash
# 不要执行: git submodule update --remote aria (这会丢弃本地领先的提交!)
# 应该执行: push 子模块
git -C aria push origin HEAD
git -C aria-orchestrator push origin HEAD
# 然后可选: git fetch 让 origin/HEAD 对齐
```

---

## 扫描摘要

| 项目 | 状态 |
|------|------|
| 当前分支 | `feature/state-scanner-v2.9` |
| Upstream 配置 | ❌ 未配置 (`reason: no_upstream`) |
| 是否浅克隆 | ❌ 否 |
| 是否 detached HEAD | ❌ 否 |
| FETCH_HEAD 年龄 | 2 hours ago (正常) |
| 与 origin/master 对比 | 0 ahead / 0 behind (手动对比) |
| 子模块 `aria` | ⚠️ 本地领先 2 commits (非落后) + worktree 有未提交修改 |
| 子模块 `standards` | ✅ 同步 |
| 子模块 `aria-orchestrator` | ⚠️ 本地领先 2 commits (非落后) |
| **是否需要 git pull** | **否** |

---

## 关键发现

1. **不需要 `git pull`** — feature 分支无 upstream，但与 `origin/master` 已完全同步。
2. **`branch_behind_upstream` 规则正确跳过** — fail-soft 设计避免了误推荐。
3. **子模块存在"反向 drift"** — 本地领先远程，应当 push 而非 update --remote。规则默认的 hint 在此场景下不适用，需要人工判断。
4. **建议**: 为 feature 分支显式设置 upstream (`git branch --set-upstream-to=origin/master`) 或推送到远程 (`git push -u`)，以便后续 state-scanner 能自动提供 ahead/behind 数据。
