# 扫描分支同步状态与子模块偏离 (state-scanner v1.62.2 路径)

> ⚠️ 本次为并发基准测试环境, **未真实执行** `scan.py` / `git fetch` / `git pull` / `git push` /
> 任何写操作。以下是按 `aria/skills/state-scanner/SKILL.md` 及其 references 规定的**扫描方式、
> 会产出的字段、以及基于这些字段的判读与建议规则**。

---

## 1. 扫描方式 (怎么查)

### Step 0: 机械执行 (不可协商)

SKILL.md Step 0 是硬约束: Phase 1 全部字段由 `scripts/scan.py` 机械采集, AI **不得**用
`git status` / `git rev-list` 逐字段手工替代, 也**不得**在 scan.py 失败时"降级"到手工补齐。

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/scan.py" \
  --output .aria/state-snapshot.json
```

退出码契约:

| 退出码 | 含义 | 动作 |
|--------|------|------|
| 0 | 全部采集成功 | 读 snapshot, 进阶段 2 推荐 |
| 10 | 部分软错误 (snapshot 仍可用, 见 `errors[]`) | 读 snapshot, 对受影响子项展 warning, 继续 |
| 20 | 硬前置失败 (非 git repo / 输出路径不可写) | abort, 不读 snapshot |
| 30 | 未捕获异常 (scan.py 内部 bug) | abort, 提示 report bug |

### 与本问题直接相关的三个采集阶段

1. **Phase 0.5 `remote_refresh` (F3′)** —— 跑在所有 Phase 1 collector 之前, 是**新鲜度信号的唯一
   生产者**("新鲜度靠获取, 不靠测量")。它按 host 分桶并行 `fetch --prune`(顺序准入闸门 +
   `refresh_deadline_seconds` 默认 15s), 每条 (repo, remote) 腿记录 `fetched_at` /
   `fetch_ok` 三态 / `error_kind`。**这一步就是"我怀疑落后了"能被诚实回答的前提** —— 没有它,
   本地 remote-tracking ref 可能是几天前的陈旧快照, 那时报 "已同步" 就是撒谎(正是主 Spec
   `state-scanner-stale-refs-false-parity` 修的 14h 事故形态)。
2. **Phase 1.12 `sync_status`** —— 当前分支 vs upstream 的 ahead/behind/diverged, 以及逐子模块的
   三方比对(工作目录 / 主仓记录 / 远程)。
3. **Phase 1.12 内的 `multi_remote`** —— 把 parity 检查扩展到主仓和每个子模块的**所有 enforced
   remote**(典型: origin=Forgejo + github=镜像), 并给出 `evidence_grade` 与
   `gitlink_integrity[]`。

注意: `sync_check` **恒开启、无法关闭**(F9′ 9.2 勘误 —— 历史文档里的
`state_scanner.sync_check.{enabled,check_submodules,warn_after_hours}` 三个键从未被任何代码读取,
写了也不生效)。它承载 US-008 方向性数据丢失护栏。

---

## 2. 会输出什么字段

### A. 当前分支相对 upstream

`sync_status.current_branch`:

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | str \| null | null = detached HEAD |
| `upstream` | str \| null | 如 `origin/feature-x`; null = 未配置 upstream |
| `upstream_configured` | bool | 是否 set-upstream-to |
| `ahead` | int \| null | 本地领先 upstream 的 commit 数 |
| `behind` | int \| null | 本地落后 upstream 的 commit 数 |
| `diverged` | bool \| null | `ahead > 0 且 behind > 0` 时为 true |
| `reason` | str \| null | `no_upstream` / `shallow_clone` / `detached_head` / `not_a_git_repo` |

fail-soft 语义(为什么会是 null):

| 状态 | `shallow` | `behind` | `reason` |
|------|-----------|----------|----------|
| 正常 | false | 数字 | null |
| 浅克隆 | true | null | `shallow_clone` |
| 无 upstream | false | null | `no_upstream` |
| detached HEAD | false | null | `detached_head` |

> `remote_refs_age`("2h 前同步") 字段仍在输出, 但**已 DEPRECATED**(F9′ 8.4): Phase 0.5 自己的
> fetch 会改写 `.git/FETCH_HEAD`, 使它每次 scan 后恒为 "1m", 测的是"本次扫描自己刚做的 fetch",
> 不再是任何有意义的陈旧度信号。**新鲜度判据请读 `evidence_grade`**。

### B. 多远程 parity + 证据新鲜度

`sync_status.multi_remote.main_repo.remotes[]` / `.submodules[].remotes[]`, 每条 `RemoteEntry`:

| 字段 | 值域 |
|------|------|
| `name` | remote 名 |
| `remote_head` | str \| null |
| `parity` | `equal` / `ahead` / `behind` / `diverged` / `unknown` |
| `behind_count` / `ahead_count` | int \| null |
| `reason` | null / `no_local_tracking_ref` / `remote_branch_missing` / `not_refreshed` / `network_timeout` / `auth_failed` / `shallow_clone` / `detached_head` / `parse_error` … |
| `evidence_grade` | `fresh` / `stale_unverified` / `expired` |
| `fetch_ok` | `"true"` / `"false"` / `"not_attempted"` (三态) |
| `method` | `local_refs`(`ls_remote` 自 task 1.10 已退役) |

`evidence_grade` 三值(D20, 全分割):

- `fresh` —— 本轮真 fetch 到且在证据窗内(默认 1h)。**只有它能给 `overall_parity` 当正证据**。
- `stale_unverified` —— 代际/墙钟/连续未验证次数仍在容忍范围。可见, **不作证也不阻断**;
  即使 `parity == equal` 也不满足存在性子句。
- `expired` —— 双重陈旧, **阻断态**。若原 `parity == equal`, 会被 `_apply_freshness_downgrade`
  改写成 `parity: unknown` + `reason: not_refreshed` —— 绝不允许陈旧的 "equal" 冒充"已同步"。

顶层汇总:

- `overall_parity: bool` —— 四子句全满足才 true:
  1. enforced 集合非空(守 `all([])` 的 vacuous-true 陷阱);
  2. **存在**某 remote 同时满足 `parity == equal` 且 `evidence_grade == fresh`;
  3. `gitlink_integrity[]` 中**没有**被 `_gitlink_blocking` 判定的 (R,S) 对;
  4. **所有** remote 都 `parity ∉ {behind, diverged}` 且非 blocking_unknown。
- `has_pending_push: bool` —— 有 `parity == ahead`(正常待推送, **不报警**)。
- `has_unreachable_remote: bool` —— 只看 `fetch_ok == "false"`(真去问了但失败);
  `not_attempted`(被 deadline 砍 / 离线)**不算** unreachable。
- `enforced_remotes_resolved[]` / `excluded_read_only[]` —— 裁决实际覆盖了哪些 remote 名
  (被过滤掉的 remote 条目仍原样出现在 `remotes[]` 里, 过滤只影响裁决, 从不隐藏数据)。

### C. 子模块偏离 (你问的"有没有偏离主仓库记录的 commit")

这是**两个正交的维度**, snapshot 里也分两处:

**C-1. `sync_status.submodules[]` —— 三方比对**

| 字段 | 含义 |
|------|------|
| `tree_commit` | 主仓 HEAD 记录的 gitlink commit(即"主仓库记录的 commit") |
| `head_commit` | 子模块本地 checkout 实际在哪个 commit |
| `remote_commit` | 子模块远程默认分支 commit |
| `remote_commit_source` | `local_ref` / `unavailable` |
| `drift.workdir_vs_tree` | bool —— **工作目录偏离主仓记录**(`head_commit != tree_commit`) |
| `drift.tree_vs_remote` | bool —— **主仓记录与远程不一致** |
| `drift.behind_count` | int \| null —— `tree..remote`, 本地落后远程多少 |
| `drift.ahead_count` | int \| null —— `remote..tree`, 本地领先远程多少 |
| `drift.hint` | 修复命令字符串 |
| `drift.hint_type` | `update` / `push` / `manual_check` / null |

方向性判定(US-008 护栏, 强制):

- `behind_count > 0` → 落后 → `hint_type: update` → `git submodule update --remote <path>`,
  并触发 `submodule_drift` 规则(priority 1.97);
- `ahead_count > 0` → 领先 → `hint_type: push` → `cd <path> && git push origin HEAD`,
  **不触发** `submodule_drift`, 只走 info 级输出。这里绝不能建议 `update --remote` ——
  那会**丢弃本地未推送的 commit**;
- `tree_vs_remote == true` 但两个计数都是 0/null → `hint_type: manual_check`, 报"方向不明,
  请手动检查"(常见于浅克隆计数失效), 不发方向性建议。

**C-2. `sync_status.multi_remote.gitlink_integrity[]` —— 跨仓可达性 (Phase 2A, F10″)**

这一维**与 C-1 完全正交**: 它问的不是"本地跟远程差几个 commit", 而是"**主仓已经推到 R 上的那个
gitlink, 在子模块自己的 R 上到底存不存在**" —— 也就是别人 `clone --recursive` 会不会直接断掉。
每个 (R=主仓 enforced remote, S=子模块路径) 一条, 9 分支状态:

| status | 含义 | 阻断 `overall_parity`? |
|---|---|---|
| `ok` | gitlink 在 S 的 `R/*` 上分支可达 | 否 |
| `orphaned` | 确认不可达且时序无歧义 | **是, 恒阻断** |
| `orphan_unverified` | 不可达但陈旧/代际错位, 尚不能排除"只是没重新 fetch" | 仅当 `consecutive_unverified >= k_eff` |
| `no_published_ref` | 主仓在 R 上没有可解析的分支 ref(含主仓 detached HEAD) | 否 |
| `not_a_gitlink` | 该路径在那个 commit 上不存在或 mode 不是 160000 | 否 |
| `uninitialized` | 子模块没 checkout(无 `.git`) | 否 |
| `no_matching_remote` | 子模块没有叫 R 的 remote | 否 |
| `shallow_unverifiable` | 子模块是浅克隆, 可达性不可判 | 否 |
| `soft_error` | 检查命令本身没跑成 | 否 |

零子模块的仓库该字段恒 `[]`, 不额外付出任何 git 调用。可达性定义是**分支可达**(Fetch 1 用
`--no-tags`), 只靠 tag 能摸到的 commit 会被报 orphaned —— 这是刻意收窄, 不是 bug。

---

## 3. 输出长什么样

按 output-formats.md, 结果落在第 8 区块「🔄 同步状态」:

```
🔄 同步状态
───────────────────────────────────────────────────────────────
  当前分支: feature/xxx (⚠️ 落后 origin/feature/xxx 3 commits)
  证据: origin fetched 2m 前 (evidence_grade: fresh)
  建议操作: git pull
  子模块:
    ✅ standards: 同步
    ⚠️  aria: 落后远程 4 commits
        修复建议: git submodule update --remote aria
```

若本次 scan 没有任何一条腿拿到新鲜证据(离线, 或全部 fetch 失败), `multi_remote_drift`
规则(priority 1.35)**不走六路 dispatch**, 改出一条降级横幅:

```
  ⚠️ 离线 / 远端不可达, 同步状态不可知 —— 本次未取得任何新鲜证据, 不给方向性建议
```

裁决层不受影响, `overall_parity` 照常 fail-CLOSED 报 false(降级只在建议层, 裁决层去抖会
重新引入假绿)。

---

## 4. 给你的建议 (按方向分派, 不是一律同一个动作)

`multi_remote_drift` v9 起**按 (parity, reason, evidence_grade) 分派**。旧版把
`overall_parity: false` 的所有成因一律建议 `git push`, 那本身就是方向性 bug —— 落后时 push
毫无意义, 甚至可能诱导在落后状态下强推。

### 主仓当前分支

| 扫出来的情况 | 该做什么 | 不该做什么 |
|---|---|---|
| `behind > 0, ahead == 0` | `git pull`(或 `git pull --rebase` 保线性)。`behind >= 5` 会触发 `branch_behind_upstream`(priority 1.98)降级提示, 建议**先拉再继续开发**, 越晚合冲突越大 | 别 push —— 非 fast-forward, 要么被拒要么诱发强推 |
| `ahead > 0, behind == 0` | `git push`(feature 分支首推用 `git push -u origin <branch>`)。这是 `has_pending_push`, **正常待推送, 不算报警** | 别 pull/`update --remote` —— 没必要, 且 submodule 侧同样动作会丢本地 commit |
| `diverged == true`(两边都 > 0) | **人工决策**: `git rebase origin/<branch>`(feature 分支, 保干净历史) 或 `git merge`。你开发几天的场景这是最可能的形态 | 别盲目 `pull` 让它自动 merge 出脏历史, 更别 `push -f` 覆盖别人 |
| `reason == no_upstream` | `git push -u origin <branch>` 建立跟踪 —— 落后/领先根本无从谈起 | 别当成"已同步" |
| `reason == detached_head` | 先 `git switch <branch>` 回到分支 | 任何同步动作 |
| `reason == shallow_clone` | `git fetch --unshallow` 后重扫; 计数在浅克隆下不可信 | 别信 `behind: null` 是"没落后" |
| `parity == unknown` 且 `reason ∈ {not_refreshed, network_timeout, auth_failed}` 或其他未识别 reason | 检查网络/凭据后重扫。**不给 pull/push 建议**(方向未知, 盲建议有害, fail-CLOSED) | 别在证据 expired 时按 `equal` 当同步 |

### 子模块

| 情况 | 该做什么 |
|---|---|
| `workdir_vs_tree: true`(工作目录偏离主仓记录) | 先决定哪边是对的。想保留子模块里的新工作 → 在主仓 `git add <path>` 把新 gitlink 提交上去; 想丢弃 → `git submodule update <path>` 回到主仓记录点(**会丢子模块工作区的 commit, 确认后再做**) |
| `tree_vs_remote: true` 且 `behind_count > 0` | `git submodule update --remote <path>`, 然后在主仓 `git add <path>` 提交新 gitlink |
| `tree_vs_remote: true` 且 `ahead_count > 0` | `cd <path> && git push origin HEAD` —— **本地领先, 绝不能 `update --remote`**, 那会丢掉未推送的 commit |
| `hint_type: manual_check` | 方向不明(常见于浅克隆), 手动比对, 不做破坏性操作 |
| `gitlink_integrity` 出 `orphaned` | `git -C <submodule> push <remote> <branch>` —— 方向是**推子模块**, 不是改主仓 gitlink。主仓引用是对的, 缺的是子模块那侧的镜像; 不修的话从该 remote `clone --recursive` 会断 |
| `gitlink_integrity` 出 `orphan_unverified` | 先重扫一次(多半只是没重新 fetch); 连续 `k_eff` 次仍未验证才升级为阻断 |

### 判读顺序建议

1. 先看 `evidence_grade` —— 若没有任何 `fresh` 的腿, 后面的 `parity` 全部不可信, 先解决网络/凭据;
2. 再看 `current_branch.{ahead, behind, diverged, reason}` 定方向;
3. 再看 `submodules[].drift`(本地三方比对)和 `gitlink_integrity[]`(跨仓可达性)——两者正交,
   同一次 scan 可能同时命中, **两条建议都要处理, 不是二选一**;
4. `overall_parity: false` 只是"有事要看"的分诊入口, 具体做什么**必须**按上面分派表, 不能一律
   pull 也不能一律 push。

---

## 5. 需要你确认的下一步

本次未执行任何命令。要真跑, 我可以:

- **[1]** 执行 `scan.py` 产出 `.aria/state-snapshot.json`, 按上述字段给出你这条 feature 分支的
  真实 ahead/behind/diverged + 子模块 drift 判读(只读, 含 Phase 0.5 的 `fetch --prune`);
- **[2]** 只读现有 snapshot(若有), 不发起任何网络请求 —— 但那样 `evidence_grade` 很可能是
  `stale_unverified`/`expired`, 结论只能标注为"不可验证";
- **[3]** 扫描后按分派表逐条给出可复制的修复命令, 由你自己执行(state-scanner 从不代你操作 git)。
