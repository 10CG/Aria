# 状态扫描: 当前分支 vs upstream + 子模块偏离

> 依据 state-scanner v1.61.0 快照 (SKILL.md v3.1.1 + references/sync-detection.md + state-snapshot-schema.md + RECOMMENDATION_RULES.md)。
> 本次为**说明性输出**: 描述会怎么扫、会给出哪些字段、结论怎么读。未真实执行 scan.py / fetch / push (并发测试期只读)。

---

## 1. 扫描方式

### Step 0 — 机械采集 (不可协商)

state-scanner v3.0.0+ 的硬约束: Phase 1 全部字段由 `scan.py` 机械产出, AI 不得用 `git status` / `git rev-list` 之类命令逐字段手工替代, 也不得在 scan.py 失败时"降级"手工采集。

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/scan.py" \
  --output .aria/state-snapshot.json
```

退出码契约:

| 退出码 | 含义 | 动作 |
|--------|------|------|
| 0 | 全部采集成功 | 读 snapshot, 进入阶段 2 推荐 |
| 10 | 部分软错误 (snapshot 仍可用, 见 `errors[]`) | 读 snapshot, 受影响子阶段展示 warning, 继续 |
| 20 | 硬前置失败 (非 git repo / 输出路径不可写) | abort, 不读 snapshot |
| 30 | 未捕获异常 (scan.py 内部 bug) | abort, 提 issue; 临时可 `mechanical_mode=false` |

### 与本问题相关的采集子阶段

- **Phase 0.5 `remote_refresh`** (F3′) — 跑在最前面, **新鲜度信号的唯一生产者**。每 host 一个线程池并行 `fetch --prune`, 顺序准入闸门 + `refresh_deadline_seconds` (默认 15s) / `per_host_fetch_limit` (默认 4) / `fetch_timeout_seconds` (默认 30)。派发顺序按 `fetched_at` 升序, never-fetched 优先, 防饥饿。
  这一步就是回答"我怀疑落后了"的关键: **新鲜度靠获取, 不靠测量** —— 不是去看 FETCH_HEAD 多久没动, 而是本轮真去 fetch 一次。
- **Phase 1.12 `sync_status`** — 恒开启、不可关闭 (它承载 US-008 方向性数据丢失护栏)。算当前分支 ahead/behind、遍历子模块三方偏差、并做多远程 parity。
- 注意: 文档里历史上那个 `state_scanner.sync_check.{enabled,check_submodules,warn_after_hours}` 配置块是**虚构的, 从未被代码消费** (F9′ 9.2 勘误), 别往 `.aria/config.json` 里写。真实可调的是 `state_scanner.sync_freshness.*` (`evidence_window_seconds` / `hard_cap_days` / `k_min`) 和 `state_scanner.multi_remote.*`。

全程只读, fail-soft: 任一命令失败只把对应字段置 `null` + 标 `reason`, 绝不 exit ≠ 0, 绝不阻塞后续阶段。

---

## 2. 会输出什么字段

### 2.1 当前分支相对 upstream (`sync_status.current_branch`)

```yaml
current_branch:
  name: "feature/xxx"        # null = detached HEAD
  upstream: "origin/feature/xxx"   # null = 未配置 upstream
  upstream_configured: true
  ahead: 2                   # 本地领先 upstream 的 commit 数
  behind: 7                  # 本地落后 upstream 的 commit 数
  diverged: true             # ahead>0 且 behind>0
  reason: null               # null | no_upstream | shallow_clone | detached_head | not_a_git_repo
```

null 语义 (你在 feature 分支上, 这几条很可能命中):

| 情况 | ahead/behind | reason |
|------|--------------|--------|
| 正常 | 数字 | `null` |
| 分支从没 `--set-upstream-to` | `null` | `"no_upstream"` |
| detached HEAD | `null` | `"detached_head"` |
| 浅克隆 | `null` | `"shallow_clone"` |

另外 `sync_status.remote_refs_age` ("15m"/"2h"/"3d"/"never") 仍在 schema 里, 但已 **DEPRECATED**: Phase 0.5 自己的 fetch 会改写 `.git/FETCH_HEAD`, 使它每次扫描后恒近似 `"1m"` —— 它测的是"本次扫描自己刚 fetch 完多久", 不再是任何有意义的陈旧度信号。判新鲜度请改读下面的 `evidence_grade`。

### 2.2 多远程 parity + 证据等级 (`sync_status.multi_remote`)

每个 `RemoteEntry`:

```yaml
name: "github"
remote_head: "e476a2b"
parity: "behind"        # equal | ahead | behind | diverged | unknown
behind_count: 1
ahead_count: 0
reachable: true
reason: null            # auth_failed | not_found | network_timeout | no_local_tracking_ref
                        # | remote_branch_missing | parse_error | shallow_clone
                        # | detached_head | not_refreshed
method: "local_refs"    # local_refs | ls_remote
evidence_grade: "fresh" # fresh | stale_unverified | expired
fetch_ok: "true"        # "true" | "false" | "not_attempted"
```

`evidence_grade` 三档 (全分割, 互斥且全覆盖):

- **fresh** — `fetched_at ≠ null ∧ (now − fetched_at) ≤ evidence_window` (默认 1h)。**唯一能当正证据**的一档。
- **stale_unverified** — 不够新, 但代际/墙钟/连续未验证次数还在容忍范围内。诊断性中间态: 可见、**不作证、不阻断**。`parity` 仍显示 `equal`, 但不满足 `overall_parity` 的存在性子句。
- **expired** — 双重陈旧, **阻断态 (fail-CLOSED)**。原本的 `parity: "equal"` 会被 `_apply_freshness_downgrade` 改写成 `parity: "unknown"` + `reason: "not_refreshed"` —— 绝不允许一个陈旧的 equal 冒充"已同步"。

`fetch_ok` 三态要点: `"not_attempted"` (被 deadline 砍掉) **不等于** `"false"` —— "我们没去问" ≠ "对方不可达"; `has_unreachable_remote` 只看 `fetch_ok == "false"`。

`overall_parity` 四子句, **全满足才为 true**:

1. `enforced_set ≠ ∅` (守 `all([])` 的 vacuous-true 陷阱)
2. `∃ r: parity == equal ∧ evidence_grade == "fresh"` (两者都要)
3. `∀ R ∈ gitlink_integrity: ¬gitlink_blocking(R, k_eff)`
4. `∀ r: parity ∉ {behind, diverged} ∧ ¬blocking_unknown(r)`

### 2.3 子模块偏离主仓库记录 (`sync_status.submodules[]`)

这是你问题的第二半。三方比较: 主仓 HEAD 记录的 gitlink (`tree_commit`) / 子模块本地 checkout (`head_commit`) / 子模块远程 (`remote_commit`)。

```yaml
- path: "aria"
  tree_commit: "abc1234"     # 主仓库 HEAD 记录的 commit
  head_commit: "abc1234"     # 本地 checkout 的 commit
  remote_commit: "def5678"
  remote_commit_source: "local_ref"   # local_ref | unavailable
  drift:
    workdir_vs_tree: false   # 工作目录偏离主仓库记录 ← 你问的"子模块有没有偏离主仓库记录"
    tree_vs_remote: true     # 主仓库记录与远程不一致
    behind_count: 4          # tree..remote, 本地落后远程
    ahead_count: 0           # remote..tree, 本地领先远程
    hint: "git submodule update --remote aria"
    hint_type: "update"      # update | push | manual_check | null
```

未初始化的子模块 (`git submodule status` 输出 sha 以 `-` 开头) 直接跳过, 不报错、不出现在列表里。

### 2.4 gitlink 完整性 (`sync_status.multi_remote.gitlink_integrity[]`, Phase 2A)

与上面的 parity **完全正交**: 它查的不是"本仓 vs remote 是否同步", 而是"主仓已发布的 gitlink, 在子模块自己的 remote 上可不可达"。每个 (远程 R, 子模块 S) 一条, 9 种状态:

| status | 含义 | 阻断 `overall_parity`? |
|---|---|---|
| `ok` | gitlink 在 S 的 `R/*` 上 branch-reachable | 否 |
| `orphaned` | 确认不可达且非陈旧误报 | **是, 恒阻断** |
| `orphan_unverified` | 不可达但时间序模糊, 可能只是没重新 fetch | 仅当 `consecutive_unverified ≥ k_eff` |
| `no_published_ref` | 主仓在 R 上无可解析的主分支 ref (含主仓 detached HEAD) | 否 |
| `not_a_gitlink` | 该路径在该 commit 不存在或 mode ≠ 160000 | 否 |
| `uninitialized` | S 磁盘上没有 `.git` | 否 |
| `no_matching_remote` | S 没有叫 R 的远程 | 否 |
| `shallow_unverifiable` | S 是浅克隆, 可达性不可判定 | 否 |
| `soft_error` | 检查命令本身跑不起来 | 否 |

零子模块的仓库该字段恒 `[]`, 不额外付 git 调用。可达性定义窄化为 **branch-reachable** (Fetch 1 `--no-tags`): 只靠 tag 可达的 gitlink 会被报 `orphaned`, 这是刻意收窄不是 bug, 逃生口是 `read_only_remotes`。

---

## 3. 输出长什么样

标准输出的 **🔄 同步状态** 区块 (10 个 canonical 区块的第 8 个):

```
🔄 同步状态
───────────────────────────────────────────────────────────────
  当前分支: feature/xxx (⚠️ 落后 origin/feature/xxx 7 commits, 领先 2)
  远程引用: 刚刚同步 (Phase 0.5 fetch)
  建议操作: git pull --rebase
  子模块:
    ✅ standards: 同步
    ⚠️  aria: 落后远程 4 commits
        修复建议: git submodule update --remote aria
```

多远程时另有 **🌐 多远程一致性** 区块:

```
🌐 多远程一致性
───────────────────────────────────────────────────────────────
  ⚠️ 主仓库: github 落后 1 commit
     修复: git push github master
     当前: origin=5b7a5f7 | github=e476a2b (behind 1)
  ✅ aria 子模块: 所有远程一致 (origin, github)
  ❓ upstream 子模块: github 不可达 (auth_failed)
     提示: 检查 CF_ACCESS_CLIENT_ID 环境变量
```

联动的推荐规则 (都是**非阻塞降级提示**, 不改变主推荐能否执行):

| 规则 | 优先级 | 触发 | 置信度 |
|---|---|---|---|
| `multi_remote_drift` | 1.35 | `overall_parity == false`, 按 (parity, reason, evidence_grade) 六路分派 | 75% |
| `submodule_drift` | 1.97 | 任一子模块 `tree_vs_remote == true` (实际只在 `behind_count > 0` 时发 update 建议) | 70% |
| `branch_behind_upstream` | 1.98 | 当前分支落后 upstream **≥ 5** commits | 65% |

---

## 4. 给你的建议 (方向性是重点)

你在 feature 分支开发了几天, 下面按扫描结果的方向分情况说。**方向搞反的代价不对称**: 落后时执行 update/pull 是安全的; 领先时误执行 `git submodule update --remote` 会**直接丢弃本地未推送的 commit**。所以先看方向, 再动手。

### 4.1 主分支方向

| 扫描结果 | 含义 | 建议 |
|---|---|---|
| `behind > 0, ahead == 0` | 纯落后 | `git pull --rebase` 或 `git merge origin/<branch>`。落后 ≥ 5 会触发 `branch_behind_upstream` 降级提示 |
| `ahead > 0, behind == 0` | 纯领先, 本地几天的活儿没推 | `git push`。**不要**做任何 "update to remote" 类操作 |
| `diverged == true` (两者都 > 0) | 真分叉 | 人工决策: rebase 还是 merge。别自动化 |
| `reason == "no_upstream"` | 分支根本没设 upstream, ahead/behind 全 `null` | 先 `git branch --set-upstream-to=origin/<branch>`, 再重扫。**此时"没报落后"不代表没落后, 是根本没测** |
| `reason == "detached_head"` | 不在分支上 | 先 checkout 回分支 |
| `reason == "shallow_clone"` | 浅克隆, 落后数不可算 | `git fetch --unshallow` 后重扫 |

### 4.2 子模块方向 (`hint_type` 就是方向裁决)

- `hint_type == "update"` (`behind_count > 0`) — 主仓记录落后子模块远程 → `git submodule update --remote <path>` 安全。
- `hint_type == "push"` (`ahead_count > 0`) — 本地领先远程, 有未推送的子模块 commit → `cd <path> && git push origin HEAD`。**此时执行 update --remote 会丢 commit**, 这条守卫就是为防这个而存在的。
- `hint_type == "manual_check"` — `tree_vs_remote == true` 但两个计数都是 0/null (典型是浅克隆导致计数失效) → 手动查, 别自动操作。
- `workdir_vs_tree == true` — 子模块工作目录 checkout 的 commit 和主仓记录的 gitlink 不一致。这正是你问的"偏离主仓库记录": 要么你在子模块里另开了分支/提交没在主仓 `git add <submodule>`, 要么主仓被别人更新了 gitlink 而你没 `git submodule update`。**先判清是哪一边动的**, 再决定是"提交 gitlink" 还是 "同步 checkout"。

### 4.3 别被"看起来同步"骗了 (这次扫描最重要的一条)

`parity == "equal"` **单独不足以**证明已同步。必须配 `evidence_grade == "fresh"`:

- `equal + fresh` → 真同步。
- `equal + stale_unverified` → 显示 equal, 但那是旧的 remote-tracking ref 说的, 不作证。你"怀疑落后"的直觉在这一档下往往是对的。
- `expired` → 已被降级成 `parity: "unknown"` + `reason: "not_refreshed"`, 别当成同步。

同理, `fetch_ok == "not_attempted"` (被 15s deadline 砍掉) 意味着这条 remote 这轮压根没查, 不是"查过没问题"。这种情况下建议放宽 `state_scanner.multi_remote.refresh_deadline_seconds` 再扫一次。

### 4.4 gitlink orphaned 单独处理

若 `gitlink_integrity[]` 出现 `orphaned`: 主仓已经发布了一个 gitlink, 但这个 commit 在子模块自己的远程上够不着 —— 典型是**子模块 commit 忘了推**, 或推到了 origin 没推 github (镜像漏推)。这会恒阻断 `overall_parity`。修法是把子模块那个 commit 推到对应远程: `git -C <submodule> push <remote> <branch>`。注意 `multi_remote_drift` 规则的 dispatch 表目前**还没接这第七路成因**, 所以推荐区可能给的是 remotes 层的通用措辞, 需要你自己对着 `gitlink_integrity[]` 字段读。

`orphan_unverified` 先别慌 —— 那是"可能只是没重新 fetch"的模糊态, 连续 `k_eff` 次才升级为阻断。

### 4.5 顺序建议

1. 跑 `/state-scanner` (Step 0 会自动先 fetch --prune, 不必手动 fetch)。
2. 读 `current_branch.reason` —— 是 `null` 才看 ahead/behind, 否则先修前置 (upstream / detached / shallow)。
3. 读每个 remote 的 `evidence_grade`, 只信 `fresh`。
4. 按 `hint_type` 决定子模块动作方向, 绝不跳过这一步直接 `update --remote`。
5. 处理完再扫一次确认 `overall_parity == true`。

---

**依据**: state-scanner 快照 v1.61.0 (SKILL.md v3.1.1) — `references/sync-detection.md` §2/§4/§5/§10, `references/state-snapshot-schema.md` §`remote_refresh`/§`sync_status`/§`evidence_grade`/§`overall_parity`/§`gitlink_integrity[]`, `references/output-formats.md` §同步状态/§多远程一致性, `RECOMMENDATION_RULES.md` 1.35/1.97/1.98。
