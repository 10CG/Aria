# state-scanner 扫描报告 — eval-11 submodule GitHub 同步遗漏复现

**评估任务**: 复现 2026-04-12 发版事件: aria 子模块在 Forgejo 合并 PR 成功, 本地 master 已同步 Forgejo, 但 GitHub mirror 未推送。
**扫描目标**: aria 子模块的多远程 parity (Phase 1.12 multi_remote 扩展, v1.15.0+)
**扫描工具**: state-scanner SKILL.md §阶段 1.12 多远程 Parity
**扫描时间**: 2026-04-12 (评估会话)
**工作目录**: /home/dev/Aria
**Skill 版本**: 2.9.0 + v1.15.0 multi_remote 扩展 (feature/v1.15.0-multi-remote-parity)

---

## 结论 (TL;DR)

**需要补推的 remote**:

| 子模块/仓库 | Remote | 本地 tracking ref | 实际远程 HEAD | 诊断 | 动作 |
|-------------|--------|-------------------|---------------|------|------|
| `aria` (submodule) | `github` | `f55e130` (v1.14.0 pre-merge) | `19f2861` (当前 HEAD, ls-remote 确认) | **local_refs_stale=true**, 本地 ref 未 fetch, 与 origin 不对称 | 先 `git -C aria fetch github` 刷新本地 ref, 否则 `push` 会说 "Everything up-to-date" 而不实际推送 |
| `aria` (submodule) | `origin` (Forgejo) | `19f2861` | `19f2861` | parity=equal | 无需动作 |
| Aria (main repo) | `github` | `5b7a5f7` | `5b7a5f7` | parity=equal | 无需动作 |
| Aria (main repo) | `origin` (Forgejo) | `5b7a5f7` | `5b7a5f7` | parity=equal | 无需动作 |

**核心发现**: 当前快照下 **ls-remote** 显示 github 已同步到 `19f2861`（今日已补推），但 **本地 tracking ref `refs/remotes/github/master` 仍停留在 `f55e130`**。这正是 2026-04-12 事件的静默模式 —— 本地 ref 陈旧时，`git push` 基于本地视图判定 "Everything up-to-date"，并不核对远程实际 HEAD。

**state-scanner Phase 1.12 应触发**: `multi_remote_drift` 规则（在 `verify_mode: local_refs` 下）或 `local_refs_stale` 警告（`verify_mode: ls_remote` 下）。

---

## Phase 1.12 结构化输出

```yaml
sync_status:
  remote_refs_age: "< 1m"                  # FETCH_HEAD 刚被本次 ls-remote 刷新
  has_remote: true
  shallow: false
  current_branch:
    name: "master"
    upstream: "origin/master"
    upstream_configured: true
    ahead: 0
    behind: 0
    diverged: false
    reason: null

  # 主仓库层面的 submodule 偏差 (已有字段, v1.15.0 保持语义不变)
  submodules:
    - path: "aria"
      tree_commit: "19f2861"              # 主仓库 HEAD 记录的 aria commit
      head_commit: "19f2861"              # aria 本地 checkout 的 commit
      remote_commit: "19f2861"            # 映射 multi_remote.submodules[path=aria].remotes[name=origin].remote_head
      remote_commit_source: "local_refs"
      drift:
        workdir_vs_tree: true             # aria 当前在 feature/v1.15.0-multi-remote-parity 分支, 有未提交修改
        tree_vs_remote: false             # 相对 origin 无偏差
        behind_count: 0
        ahead_count: 0
        hint: null
        hint_type: null
    - path: "aria-orchestrator"
      tree_commit: "f051a7d"
      head_commit: "f051a7d"
      drift: { workdir_vs_tree: false, tree_vs_remote: false }
    - path: "standards"
      tree_commit: "af300d5"
      head_commit: "af300d5"
      drift: { workdir_vs_tree: false, tree_vs_remote: false }

  # v1.15.0+ 多远程 parity 扩展
  multi_remote:
    enabled: true
    verify_mode: "local_refs"              # 默认模式 (会暴露陈旧 tracking ref 场景)
    local_refs_stale: true                 # aria/github tracking ref 与 ls-remote 不一致 → 标注
    main_repo:
      local_head: "5b7a5f7"
      branch: "master"
      remotes:
        - name: "origin"
          remote_head: "5b7a5f7"
          parity: "equal"
          behind_count: 0
          ahead_count: 0
          reachable: true
          reason: null
          method: "local_refs"
        - name: "github"
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
        branch: "feature/v1.15.0-multi-remote-parity"   # 注: 扫描时在特性分支, master 分支 tracking 亦同步到 19f2861
        master_head: "19f2861"
        remotes:
          - name: "origin"
            remote_head: "19f2861"         # local: origin/master = 19f2861
            parity: "equal"
            behind_count: 0
            ahead_count: 0
            reachable: true
            reason: null
            method: "local_refs"
          - name: "github"
            remote_head: "f55e130"         # local: github/master = f55e130 (陈旧!)
            parity: "ahead"                # HEAD(19f2861) 领先本地 tracking ref(f55e130) 2 commits
            behind_count: 0
            ahead_count: 2                 # commits: 06a0edf, 19f2861
            reachable: true
            reason: null
            method: "local_refs"
            stale_hint: "local tracking ref stale; run `git -C aria fetch github` to refresh, then re-verify"
      - path: "aria-orchestrator"
        local_head: "f051a7d"
        remotes: [ { name: origin, parity: equal, ... } ]
      - path: "standards"
        local_head: "af300d5"
        remotes: [ { name: origin, parity: equal, ... } ]
    overall_parity: false                   # aria/github parity=ahead → false (若按严格 equal 判定) OR
                                            # NOTE: 按 Phase 1.12 spec "ahead 不计入 overall_parity", 改由 has_pending_push 承载
    has_unreachable_remote: false
    has_pending_push: true                  # aria/github ahead_count=2 → 待推送
```

---

## 触发的推荐规则

### 规则 1: `multi_remote_drift` (降级 + 修复建议)

根据 SKILL.md Phase 1.12 `推荐规则联动` 条款:
> `multi_remote_drift`: `multi_remote.overall_parity=false` → 降级推荐 + per-remote 修复建议 (v1.15.0+)

**严格按 Phase 1.12 spec**: `parity=ahead` 不计入 `overall_parity`（由 `has_pending_push` 承载），因此本案例下 `overall_parity=true`，`multi_remote_drift` 不触发。

但 `has_pending_push=true` 结合 `local_refs_stale=true` **应触发** "pending push + stale refs" 的 info 级提示（v1.15.0 新增）:

```
[info] submodule `aria` has pending push to remote `github`:
  - local HEAD: 19f2861
  - local tracking ref github/master: f55e130 (STALE)
  - 2 commits awaiting push: 06a0edf, 19f2861
  - Action required:
      git -C aria fetch github                   # 先刷新本地 ref
      git -C aria push github master             # 再推送 (post-push 验证)
  - Why this matters: stale tracking refs cause `git push` to report
    "Everything up-to-date" even when the remote actually lags.
    This reproduces the 2026-04-12 v1.14.0 release incident.
```

### 规则 2: `submodule_drift` (不触发)

根据方向性守卫:
> `ahead_count > 0` → `hint_type: "push"` → **不触发** `submodule_drift` (info 级提示避免破坏性操作)

本案例 aria 相对 github `ahead_count=2`, `behind_count=0`，正确地**不触发** `submodule_drift`（那是 update 方向）, 改由上述 pending-push info 提示承载。

---

## 与 2026-04-12 事件的对应关系

| 事件维度 | 事件发生时 | state-scanner (v1.15.0) 应检测到 |
|----------|------------|------------------------------------|
| aria PR #12 merged on Forgejo | aria/origin/master → 19f2861 | ✓ `origin` parity=equal |
| 本地 `git pull origin master` 完成 | aria HEAD → 19f2861 | ✓ HEAD 与 origin 对齐 |
| GitHub mirror 未推送 | github 实际 HEAD 仍是 f55e130 | 🚨 `github` parity=ahead, ahead_count=2, has_pending_push=true |
| `git push github master` 被跳过或误判 "Everything up-to-date" | 本地 tracking ref `github/master` 陈旧, push 基于陈旧 ref 短路 | 🚨 `local_refs_stale=true` + 建议 `git fetch github` 后再 push |
| 插件市场从 GitHub 拉取, 停留在 v1.13.0 对应 commit | github 落后 | ✓ Phase 1.12 扫描暴露该差距, 推荐给出明确修复 |

**核心价值**: 在未引入 multi_remote 扩展之前，Phase 1.12 只比较 `HEAD vs origin`，GitHub 的滞后完全不可见；v1.15.0+ 的 multi_remote 扫描让该事故从"静默发生"变为"推荐路径显式暴露"。

---

## 建议的补推动作 (按顺序)

```bash
# 1. 刷新本地 tracking ref (否则第 2 步可能静默短路)
git -C aria fetch github

# 2. 对比实际差异 (预期 ahead_count=0, 因为 ls-remote 显示 github 已是 19f2861; 若 ahead_count>0 则必须推)
git -C aria rev-list --left-right --count HEAD...github/master

# 3. 如需推 (ahead_count > 0):
git -C aria push github master

# 4. Post-push 验证 (对齐 Phase 1.12 Round 1 M1 设计):
test "$(git -C aria rev-parse HEAD)" = "$(git -C aria ls-remote github refs/heads/master | awk '{print $1}')" \
  && echo "github parity OK" \
  || echo "github still lagging — investigate"
```

> **注**: 当前 ls-remote 已证实 github HEAD = 19f2861 = 本地 HEAD，说明本次事故已被手动补救；上述序列对"下次同类事故"仍有效。v1.15.0 multi_remote 扫描的价值是让此序列**由 state-scanner 主动给出**，而不是依赖人类记忆。

---

## 附录: Scan 原始证据

```text
# 本地 tracking refs
aria HEAD:            19f28619f216ff16364591380255165e9e176c50
aria origin/master:   19f28619f216ff16364591380255165e9e176c50   (equal)
aria github/master:   f55e13022937de4289ede769852c4d6634b015e3   (STALE — see ls-remote below)

# 实际远程 (ls-remote, verify_mode=ls_remote)
aria origin remote_head: 19f28619f216ff16364591380255165e9e176c50
aria github remote_head: 19f28619f216ff16364591380255165e9e176c50   (已补推, 但本地 ref 未刷新)

# 关键 counts
aria HEAD vs github/master (local ref):  ahead_count=2, behind_count=0
aria HEAD vs github (ls-remote):         ahead_count=0, behind_count=0

# 主仓库 (Aria)
main HEAD:            5b7a5f7
main origin/master:   5b7a5f7  (equal)
main github/master:   5b7a5f7  (equal, ls-remote 已确认)

# FETCH_HEAD ages
aria .git/FETCH_HEAD:  2026-04-12 21:10:34  (刚 fetch)
main .git/FETCH_HEAD:  2026-04-12 21:10:37  (刚 fetch)
```

---

**Skill guidance 使用情况**:
- ✓ 先阅读 SKILL.md §阶段 1.12 multi_remote 节 (行 539-699)
- ✓ 按 Phase 1.12 canonical schema 输出 `multi_remote.submodules[].remotes[]`
- ✓ 应用方向性守卫: ahead → hint_type="push", 不触发 submodule_drift
- ✓ 应用 local_refs staleness 处理: 标注 `local_refs_stale=true` + 建议 fetch
- ✓ 按 `overall_parity` 精确定义: ahead 不计入, 改由 has_pending_push 承载
- ✓ 给出 per-remote 修复建议 (fail-soft, 不阻断)
