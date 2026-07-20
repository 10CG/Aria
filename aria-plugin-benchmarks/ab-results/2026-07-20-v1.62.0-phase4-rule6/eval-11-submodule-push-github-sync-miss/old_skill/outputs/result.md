# 复现 2026-04-12 「Forgejo 已合并 / GitHub 镜像漏推」场景 — state-scanner 检测路径

> 依据: state-scanner Skill 快照 v1.61.0 (SKILL.md + references/sync-detection.md +
> references/state-snapshot-schema.md + references/predicate-domain-table.md +
> references/rules/basic-rules.md §1.35/§1.36 + references/output-formats.md)
> 说明: 按测试要求**未真实执行** scan.py / fetch / push, 下述为按快照契约推导的扫描方式、
> 输出字段与判据。

---

## 1. 事件形态还原

2026-04-12 事故的机制是: `aria` 子模块的变更在 Forgejo (`origin`) 侧合并并推送成功,
本地 `master` 与 `origin` 完全一致, 但 GitHub 镜像 (`github` remote) 从未收到这批 commit。
由于当时只对 `origin` 做单远程检查, `git push origin` 返回 `Everything up-to-date`,
"看起来一切正常", 于是插件市场停留在旧版本。

这个场景要检测出来, 需要两条相互独立的信号:

- **多远程 parity**: 本仓 (主仓 / 每个子模块) 对**每一个**已配置远程分别算 parity, 而不是只看 `origin`。
- **新鲜度**: `github` 的 remote-tracking ref 如果是几天前的陈旧缓存, `parity` 会算出一个假的
  `equal`。必须先 fetch 拿到新证据, 陈旧的 `equal` 不许当作"已同步"的正证据。

v1.61.0 的 state-scanner 两条都覆盖, 另外还有第三条 (gitlink 跨仓可达性), 见 §4.3。

---

## 2. 扫描方式 (怎么跑)

### Step 0: 机械执行 scan.py (硬约束)

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/scan.py" \
  --output .aria/state-snapshot.json
```

这是不可协商的: Phase 1 全部字段由 scan.py 机械采集, AI 不得用 `git status` / `git remote -v`
逐字段手工替代, 也不得在 scan.py 失败时"降级"回手工采集。退出码契约:

| 退出码 | 含义 | 动作 |
|---|---|---|
| 0 | 全部采集成功 | 读 snapshot, 进阶段 2 |
| 10 | 部分软错误 (snapshot 仍可用, 见 `errors[]`) | 读 snapshot, 对受影响子阶段展示 warning |
| 20 | 硬前置失败 (非 git repo / 输出路径不可写) | abort, 展示 stderr |
| 30 | 未捕获异常 | abort, 提示 report bug |

### 与本场景相关的两个采集阶段

**Phase 0.5 `remote_refresh` (新鲜度信号的唯一生产者)** —— 跑在所有 collector 之前。
按 host 分桶并行 `git fetch --prune --no-tags`, 每条 (repo, remote) 是一条 leg
(这里就是 `(".", "origin")` / `(".", "github")` / `("aria", "origin")` / `("aria", "github")` …)。
核心思想是"新鲜度靠获取, 不靠测量" —— 先真去问一次 GitHub, 再判定。

- `enforced_remotes` 为 `[]` 或未配置 ⇒ **自动发现全部远程** (不是空集合), 所以 `github` 默认会被覆盖;
  只有显式白名单里漏写 `github` 才会漏掉它 (漏写的名字会进 `no_matching_remotes`, 不会伪造 leg)。
- `refresh_deadline_seconds` (默认 15) 砍掉来不及跑的 leg, 这类 leg 记 `fetch_ok="not_attempted"`,
  **不等于** `"false"` ——"我们没去问" 不等于 "对方不可达"。
- `ARIA_SCAN_OFFLINE=1` 时全部 leg 记 `not_attempted`, 冻结新鲜度 (离线可重复扫描)。

**Phase 1.12 `sync_status` (恒开启, 不可关闭)** —— 消费 Phase 0.5 的 leg 数据, 产出
`sync_status.multi_remote`: 主仓 + 每个子模块 × 每个 enforced remote 的 `RemoteEntry`,
外加 `gitlink_integrity[]` 与三个汇总 flag。

> 注意: 老文档里的 `state_scanner.sync_check.{enabled,check_submodules,warn_after_hours}`
> 三个键是历史虚构, 从未被代码消费 (F9′ 9.2 勘误), 写进 `.aria/config.json` 也不生效。
> 真正可调的新鲜度阈值是 `state_scanner.sync_freshness.{evidence_window_seconds, hard_cap_days, k_min}`。
> 同理 `sync_status.remote_refs_age` 已 DEPRECATED —— Phase 0.5 自己刚 fetch 过, 它现在恒等于
> "本次 scan 自己 fetch 了多久", 不再是任何有意义的陈旧度信号。

---

## 3. 会输出哪些字段 (机读)

### 3.1 `remote_refresh.legs[]` (Phase 0.5)

每条 leg:

```yaml
{repo: "aria", remote: "github",
 host: "github.com",              # 已解析 hostname, 绝不含凭据 URL (Rule #7)
 fetched_at: "2026-04-12T…Z",     # null = 从未 fetch
 fetch_ok: "true" | "false" | "not_attempted",
 error_kind: null | network | auth_403 | non_ff | git_missing | other,
 scan_generation: N, generation_fetched: M, consecutive_unverified: 0}
```

另有 `skipped_count` / `skipped_remotes[]` / `no_matching_remotes[]`。

### 3.2 `sync_status.multi_remote.submodules[path="aria"].remotes[]`

本场景的核心证据。每个 `RemoteEntry`:

| 字段 | `origin` (Forgejo) | `github` (镜像漏推) |
|---|---|---|
| `name` | `origin` | `github` |
| `remote_head` | 与 `local_head` 相同 | 旧 commit |
| `parity` | `equal` | **`ahead`** (本地领先 github) |
| `ahead_count` / `behind_count` | 0 / 0 | **N / 0** |
| `reachable` | true | true |
| `reason` | null | null |
| `evidence_grade` | `fresh` | `fresh` (前提: Phase 0.5 这轮真 fetch 成功) |
| `fetch_ok` | `"true"` | `"true"` |
| `method` | `local_refs` | `local_refs` |

### 3.3 汇总 flag

- `has_pending_push: true` ← 本场景**必然置位**的字段, 由 `parity == ahead` 驱动。
- `has_unreachable_remote`: 只看 `fetch_ok == "false"` (零枚举 fail-CLOSED), 本场景为 `false`。
- `overall_parity`: 见下节判据。

---

## 4. 判据 (为什么这次不会被 "Everything up-to-date" 静默放过)

### 4.1 `evidence_grade` 三档 (D20, 防陈旧假 equal)

由双谓词 `证据资格(E)` × `豁免资格(X)` 全分割:

| 档 | 条件 | 语义 |
|---|---|---|
| `fresh` | `E`: `fetched_at ≠ null ∧ now − fetched_at ≤ evidence_window` (默认 1h) | 可作 `overall_parity` ∃-子句的**正证据** |
| `stale_unverified` | `¬E ∧ X` (代际/墙钟/连续未验证均在容忍内) | 可见, **不作证, 不阻断** |
| `expired` | `¬E ∧ ¬X` | **阻断态**; 若原 `parity == equal` 会被 `_apply_freshness_downgrade` 改写成 `parity: unknown` + `reason: "not_refreshed"` |

这一条正是针对"陈旧 remote-tracking ref 撒谎报 equal"的 14h 事故: **一个双重陈旧的 `equal`
绝不允许冒充已同步**。

### 4.2 `overall_parity` 四子句 (全部满足才 true)

1. `enforced_set ≠ ∅` (守 `all([])` vacuous-true 陷阱)
2. `∃ r: parity == equal ∧ evidence_grade == "fresh"` (两者都要)
3. `∀ R ∈ gitlink_integrity: ¬gitlink_blocking(R, k_eff)`
4. `∀ r: parity ∉ {behind, diverged} ∧ ¬blocking_unknown(r)`

**对本场景要诚实说明一点**: `parity == ahead` 按设计**不计入** `overall_parity`
(它归 `has_pending_push`)。所以如果只是"子模块本地领先 github, 主仓 gitlink 还没推 github",
`overall_parity` 仍可能是 `true` —— 检出信号来自 `has_pending_push: true` +
per-remote `parity: ahead / ahead_count: N`, 而不是 `overall_parity` 变红。
schema 的 worked example 明确写了这一格: `origin=equal, github=ahead ⇒ overall_parity=true,
has_pending_push=true`。

真正会把 `overall_parity` 打成 `false` 的是下面这条。

### 4.3 `gitlink_integrity[]` (Phase 2A, F10″) —— 镜像漏推的正解

`multi_remote` 对 (R = 主仓 enforced remote) × (S = 每个已声明子模块路径, 含未 init 的)
做双重循环, 检测「**主仓在 R 上已发布的那个 commit 所引用的子模块 gitlink, 在子模块自己的 R 上
是否可达**」。9 分支域, 关键三个:

| status | 含义 | 阻断? |
|---|---|---|
| `ok` | gitlink 在 S 的 `R/*` 上 branch-reachable | 否 |
| `orphaned` | 不可达, 且两条 leg 都够新鲜、代际 `gen(S,R) ≥ gen(主仓,R)` — 已确认的真断裂 | **是, 恒阻断** |
| `orphan_unverified` | 不可达但时间序有歧义 (可能只是没重新 fetch) | 仅当 `consecutive_unverified ≥ k_eff` 时升级阻断 (D18) |

其余 `no_published_ref` / `not_a_gitlink` / `uninitialized` / `no_matching_remote` /
`shallow_unverifiable` / `soft_error` 均 benign-visible, 不阻断, 也绝不折进 `RemoteEntry.reason`
(折进去会被 `blocking_unknown` 的补集定义误判成阻断)。

所以 2026-04-12 事件按推送顺序分两种形态:

- **形态 A (主仓 gitlink 也还没推 github)**: github 上主仓仍是旧 gitlink, 老 gitlink 依然可达 ⇒
  `gitlink_integrity = ok`, `overall_parity` 仍 `true`。
  检出信号 = 子模块 `github` 的 `parity: ahead` + `has_pending_push: true`(§3.2/§3.3)。
- **形态 B (主仓 gitlink 已推 github, 子模块 commit 没推)**: github 上主仓引用了一个
  github 侧根本不存在的 aria commit ⇒ `status: orphaned` ⇒ clause 3 破 ⇒
  **`overall_parity: false`**, 红。这正是 schema 的 AC-16 worked example。

补充两条前置条件:
- Fetch 1 必须带 `--prune` (RC-1), 否则被删除/force-push 的远端分支留下的陈旧 tracking ref
  会让 `contains` 假绿。
- 可达性定义窄化为 **branch-reachable** (只看 `R/*` 分支, `--no-tags`): 只能经 tag 到达的 commit
  一律报 orphaned, 是刻意收窄不是 bug; 逃生口是 `read_only_remotes`。

### 4.4 推荐规则联动

- **§1.35 `multi_remote_drift`** (priority 1.35, `overall_parity == false` 触发): 按 remote
  逐条六路分派。`ahead` 那一路显式 `triggers_rule: false` ——"已由 `has_pending_push` 覆盖,
  本规则不再对 ahead 发建议"。
  ⚠️ 已知缺口 (快照自述): `overall_parity=false` 由 gitlink blocking 触发时, §1.35 的 dispatch 表
  **尚未新增 gitlink 专属第七路建议** (`git -C S push R <branch>`, AC-16 设计意图), 待后续增量接入。
  也就是说形态 B 会红, 但修复文案还得靠人/输出层补。
- **§1.36 `has_unpublished_branch`**: `parity == unknown ∧ reason == no_local_tracking_ref ∧
  evidence_grade != fresh` 时提示可能从未推送过 —— 本场景不走这路 (`github` 有 tracking ref)。
- 老的 Phase 1.12 单远程 `submodule_drift` 规则只在 `behind_count > 0` 触发;
  `ahead_count > 0` 走 info 级 push 提示, **绝不**发 `git submodule update --remote`
  (那会丢弃本地 commit, US-008 方向性数据丢失护栏)。

---

## 5. 人读输出 (区块 8 「🔄 同步状态」下的多远程子块)

```
🌐 多远程一致性
───────────────────────────────────────────────────────────────
  ✅ 主仓库: 所有远程一致 (origin, github)
  ⚠️ aria 子模块: github 落后 2 commits
     修复: git -C aria push github master
     当前: origin=19f2861 | github=f55e130 (behind 2)
  ✅ standards 子模块: 所有远程一致 (origin, github)
```

形态 B 还会额外把 `gitlink_integrity` 的 `orphaned` 条目呈现出来, 并让
`overall_parity: false` 触发 §1.35 的降级置信度 + 非阻断告警。

---

## 6. 结论: 哪些 remote 需要补推

按事件描述 (aria 子模块已合 Forgejo、本地 master 已同步 Forgejo、GitHub 未推), 判定:

| 仓库 | remote | parity | 需要补推? | 命令 |
|---|---|---|---|---|
| `aria` 子模块 | `origin` (Forgejo) | `equal` / `fresh` | 否 | — |
| `aria` 子模块 | `github` | **`ahead` (N commits)** | **是** | `git -C aria push github master` |
| 主仓 `Aria` | `origin` (Forgejo) | 视 gitlink bump 是否已提交推送 | 若 `ahead` 则是 | `git push origin master` |
| 主仓 `Aria` | `github` | 通常同样 `ahead` | **是** | `git push github master` |
| `standards` 子模块 | `origin` / `github` | 本次无变更则 `equal` | 否 | — |

### 修复顺序 (不可颠倒)

多仓 ship 必须 **子模块先、主仓后**, 否则主仓 gitlink 指向一个 GitHub 上不存在的 commit,
正好造出 §4.3 的 `orphaned` 断裂:

```bash
# 1) 子模块补推所有 enforced remote
git -C aria push origin master
git -C aria push github master

# 2) 再推主仓 (gitlink 已被子模块 commit 覆盖)
git push origin master
git push github master

# 3) 重跑验证
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/scan.py" \
  --output .aria/state-snapshot.json
```

### 验证判据 (重扫后必须同时成立)

- `sync_status.multi_remote.has_pending_push == false`
- 所有 `RemoteEntry.parity == "equal"` **且** `evidence_grade == "fresh"`
  (只看 `equal` 不够 —— 陈旧的 `equal` 不是证据)
- `sync_status.multi_remote.gitlink_integrity[*].status` 全为 `ok` (或其它 benign 值), 无 `orphaned`
- `overall_parity == true`
- `remote_refresh.legs[]` 中 `(aria, github)` 与 `(., github)` 两条 `fetch_ok == "true"`,
  且 `no_matching_remotes` 为空 (确认 `github` 确实被 enforced 覆盖, 没有被白名单漏掉)

### 防复发建议 (机制层)

- 检查 `.aria/config.json` 的 `state_scanner.multi_remote.enforced_remotes` —— 显式列出
  `["origin", "github"]`, 或保持 `[]`/未配置 (自动发现全部远程)。**最危险的写法是只写
  `["origin"]`**: `github` 会被整条排除, 事故原样复现。
- 发版走 phase-c-integrator C.2.5 自动多远程推送 + post-push SHA 验证, 别手推。
- `git push origin` 返回 `Everything up-to-date` 只是关于 `origin` 一个远程的陈述,
  它对 `github` 什么都没说 —— 这就是本事故的根本教训。
