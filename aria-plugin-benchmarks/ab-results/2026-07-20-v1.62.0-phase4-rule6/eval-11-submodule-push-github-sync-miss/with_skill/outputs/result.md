# 复现 2026-04-12 发版事件: 子模块 GitHub 镜像漏推的检测路径

> 本文按 `aria/skills/state-scanner/` (v1.62.2) 的 SKILL.md + `references/sync-detection.md` +
> `references/state-snapshot-schema.md` + `references/rules/basic-rules.md` + `references/predicate-domain-table.md` 作答。
> 说明: 按测试约束**未实际执行** `scan.py` / fetch / push, 下文是扫描方式、会产出的字段与判据、以及修复建议。

---

## 1. 扫描方式 (不是手工 git, 是机械 scan.py)

state-scanner v3.0 起 Phase 1 全部字段由 `scripts/scan.py` 机械采集, SKILL.md 里写死了 AI 禁区:
**不允许**用 `git status` / `git remote` 逐字段手工替代, 也**不允许**在 scan.py 失败时手工 Bash 补齐。

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/scan.py" \
  --output .aria/state-snapshot.json
```

退出码契约: `0` 全成功 → 读 snapshot 进阶段 2; `10` 部分软错误 (snapshot 仍可用, 看 `errors[]`) → 带 warning 继续;
`20` 硬前置失败 (非 git repo / 写不了输出) → abort; `30` 内部异常 → abort 并报 bug。

### 为什么这次不会像 `git push` 那样被 "Everything up-to-date" 骗过

`git push` 的输出只反映**本地 remote-tracking ref** 的认知。2026-04-12 事故的形态正是:
本地 `refs/remotes/github/master` 是陈旧的, 于是本地以为已推, push 报 "Everything up-to-date", 而 GitHub 上其实没有那个 commit。

state-scanner 的解药是 **Phase 0.5 `remote_refresh` (F3′)** —— 它跑在**所有** Phase 1 collector 读本地 git 状态**之前**,
对每一条 enforced (repo, remote) 腿真的做一次 `fetch --prune`, 然后把结果写进 snapshot 顶层 `remote_refresh.legs[]`:

| 字段 | 用途 |
|---|---|
| `repo` / `remote` / `host` | 哪条腿 (host 是解析后的主机名, 遵守 Rule #7 绝不写凭据 URL) |
| `fetched_at` | 这条腿最后一次**真成功** fetch 的 ISO 时间; `null` = 从未 fetch |
| `fetch_ok` | 三态 `"true"` / `"false"` / `"not_attempted"` ("没去问" ≠ "对方不可达") |
| `error_kind` | 类型化标签 `network` / `auth_403` / `non_ff` / `git_missing` / `other`, 绝不透传 stderr |
| `generation_fetched` / `consecutive_unverified` | 代际与连续未验证计数, 供新鲜度判据用 |
| `no_matching_remotes[]` | 配置里写了但仓库里不存在的 remote 名 (不伪造成 ghost fail 腿) |

核心洞察一句话: **新鲜度靠获取, 不靠测量**。旧的 `remote_refs_age` (FETCH_HEAD mtime) 已 DEPRECATED ——
它是仓库全局的, 结构上不能当 per-(repo, remote) 的判据; `warn_after_hours` 这个配置键也已在 v1.62.2 退役 (F2′)。

### 本仓库这次会跑哪些腿

`.aria/config.json` 里**没有**设 `state_scanner.multi_remote.enforced_remotes`, 按 `resolve_enforced_remotes`
(`[]` / `None` ⇒ 自动发现, 不是空集合) 的语义, enforced 集合 = 各仓库实际配置的全部 remote:

| 仓库 | remotes |
|---|---|
| `.` (主仓 Aria) | `origin` (Forgejo), `github` |
| `aria` (aria-plugin) | `origin` (Forgejo), `github` |
| `standards` (aria-standards) | `origin` (Forgejo), `github` |
| `aria-orchestrator` | 按其 `.git` 实配 |

也就是 (repo, remote) 共约 8 条腿, 每条都会被 Phase 0.5 fetch, 且按 host 分桶并行 (每 host 一个线程池,
`per_host_fetch_limit` 默认 4), 顺序准入闸门受 `refresh_deadline_seconds` (默认 15s) 控制, 被砍的腿记 `not_attempted`。

> 提醒: 也正因为要真 fetch, 这一步是**有网络副作用**的读操作 —— 本次按测试约束没有执行。

---

## 2. 会输出什么字段与判据

### 2.1 parity 层 (`sync_status.multi_remote.*.remotes[]`)

每个 (repo, remote) 产出一条 `RemoteEntry`:

```yaml
name: "github"
remote_head: "<refs/remotes/github/master 的 sha>"
parity: "equal" | "ahead" | "behind" | "diverged" | "unknown"
behind_count / ahead_count: int | null
reason: null | no_local_tracking_ref | remote_branch_missing | not_refreshed
        | network_timeout | auth_failed | shallow_clone | detached_head | ...
evidence_grade: "fresh" | "stale_unverified" | "expired"   # 独立字段, 从不折进 reason
fetch_ok: "true" | "false" | "not_attempted"               # F3′ 腿直接透传
method: "local_refs"                                        # ls_remote 已退役 (task 1.10)
```

`evidence_grade` 三值 (D20, 全分割) 是这次事件的核心判据:

- `fresh` — 证据资格成立: `fetched_at ≠ null ∧ now − fetched_at ≤ evidence_window` (默认 1h)。**只有它能当正证据**。
- `stale_unverified` — 不新鲜但在豁免窗内 (代际 / 墙钟 ≤ `hard_cap` 默认 7d / `consecutive_unverified < k_eff`)。可见, 但**不作证也不阻断**。
- `expired` — 双重陈旧, **阻断态**。若原本 `parity == "equal"`, 会被 `_apply_freshness_downgrade` 改写成
  `parity: "unknown"` + `reason: "not_refreshed"` —— 绝不允许一个陈旧的 `equal` 冒充"已同步"。

这就是"陈旧 ref 上的 equal 不再算正证据"的机制, 也正是 14h 事故的根被堵住的地方。

`overall_parity` 四子句, **全部满足才为 true**:

1. `enforced_set ≠ ∅` (守 `all([])` 的 vacuous-true 陷阱)
2. `∃ r: parity == equal ∧ evidence_grade == "fresh"` (两个条件都要)
3. `∀ (R,S) ∈ gitlink_integrity: ¬gitlink_blocking(R, k_eff)`
4. `∀ r: parity ∉ {behind, diverged} ∧ ¬blocking_unknown(r)`

另有两个正交 flag: `has_pending_push` (存在 `parity == ahead`) 与 `has_unreachable_remote` (存在 `fetch_ok == "false"`, 零枚举 fail-CLOSED)。

### 2.2 gitlink 层 (`sync_status.multi_remote.gitlink_integrity[]`, Phase 2A / F10″)

这一层与 parity 层**正交**, 而且它才是本事件"从 GitHub clone --recursive 会断裂"的直接检测者。
它逐 (R, S) 对回答: **主仓在 remote R 上已发布的那个 commit 所引用的子模块 gitlink, 在子模块自己的 R 上是否分支可达?**

```yaml
gitlink_integrity:
  - remote: "github"            # R = 主仓 enforced remote
    submodule: "aria"           # S = 子模块路径 (含未 init 的)
    status: "orphaned"          # 9 分支域
    consecutive_unverified: 0
```

九种 status 与是否阻断:

| status | 含义 | 阻断 `overall_parity`? |
|---|---|---|
| `ok` | gitlink 在 S 的 `R/*` 上分支可达 | 否 |
| `orphaned` | 不可达, 且两条腿都过新鲜度豁免资格门 + 代际不逆序 → 已确认的断裂 | **是, 恒阻断** |
| `orphan_unverified` | 不可达但时序模糊 (可能只是没重新 fetch) | 仅当 `consecutive_unverified ≥ k_eff` (D18 升级) |
| `no_published_ref` | 主仓在 R 上没有可解析的发布 ref (含主仓 detached HEAD) | 否 |
| `not_a_gitlink` | 该路径在该 commit 上不存在或 mode ≠ 160000 | 否 |
| `uninitialized` | 子模块没有落盘 `.git` | 否 |
| `no_matching_remote` | 子模块没有名字叫 R 的 remote | 否 |
| `shallow_unverifiable` | 子模块是浅克隆, 可达性不可判 | 否 |
| `soft_error` | `branch -r --contains` 本身跑不起来 | 否 |

可达性定义 (RM-11) 是**分支可达**, 只认 Fetch 1 (`--prune --no-tags`) 拉到的 `R/*` remote-tracking 分支;
只能靠 tag 到达的 commit 依然报 orphaned, 这是刻意收窄。`--prune` 是先决条件 (RC-1) ——
没有它, 被删/被强推的远程分支会留下陈旧 ref, 让 `contains` 假绿。

### 2.3 这次事件会落在哪 (两种子形态, 必须分清)

事件描述是"aria 子模块在 Forgejo merge 成功, 本地 master 已同步 Forgejo, GitHub mirror 未推"。
按主仓 gitlink bump 有没有推到 GitHub, 判据落点不同 —— 这点必须诚实分开讲, 不能笼统说"报 overall_parity=false":

**形态一: 主仓 gitlink bump 已推到 github, 子模块没推 github (真正危险的一种)**

- `aria` 的 `github` 条目: `parity: "ahead"`, `ahead_count > 0`, `evidence_grade: "fresh"` → 只进 `has_pending_push`, **不**进 `overall_parity`。
- 真正开火的是 gitlink 层: `(R=github, S=aria)` → `status: "orphaned"` → clause 3 不满足 → **`overall_parity: false`**。
- 后果正是它要抓的: 别人从 GitHub `clone --recursive` 会拿到一个 GitHub 上不存在的 aria commit, 直接断裂。

**形态二: 主仓 gitlink bump 也没推 github (两边一起漏推)**

- 主仓 `github`: `parity: "ahead"`; `aria` 的 `github`: `parity: "ahead"` → `has_pending_push: true`。
- gitlink 层看的是主仓**已发布**在 github 上的旧 commit, 它引用的旧 gitlink 仍可达 → `status: "ok"`, 不阻断。
- 此时 `overall_parity` 可能仍为 `true` (只要有一条 `equal ∧ fresh` 的腿), 检测靠的是 `has_pending_push` + ahead 的 info 级提示,
  而非红色阻断。这是设计意图 ("ahead 是正常待推送, 不报警"), 但对镜像仓库场景确实偏弱 ——
  已作为 follow-up 记在 **Aria #165 (镜像漏推)**, 方案 B 是复用 F10″ 谓词把它拉进裁决。

**如果 `refs/remotes/github/master` 本地根本不存在** (从没 fetch 过 github):
`parity: "unknown"` + `reason: "no_local_tracking_ref"` + `evidence_grade != fresh` → 命中规则 **1.36 `has_unpublished_branch`**,
提示"可能从未推送过", 建议 `git -C aria push -u github <branch>`。

### 2.4 输出面 (第 8 区块 "🔄 同步状态" + 第 10 区块推荐)

```
🔄 同步状态
───────────────────────────────────────────────────────────────
  当前分支: master (超前 0 / 落后 0, upstream origin/master)
  多远程 parity:
    主仓 .        origin ✅ equal (fresh)   github ⚠️ ahead N commits (fresh)
    子模块 aria   origin ✅ equal (fresh)   github ⚠️ ahead N commits (fresh)
  🔴 gitlink 完整性: github × aria → orphaned
      主仓在 github 上引用的 aria commit <sha> 在 github 上不存在,
      从 github clone --recursive 会断裂。
  overall_parity: false   has_pending_push: true   has_unreachable_remote: false
```

推荐区由规则 **1.35 `multi_remote_drift`** (priority 1.35, `non_blocking: true`) 按成因分派 ——
v9 起**不再**对整块 `overall_parity: false` 笼统建议 `git push` (那本身是方向性 bug)。
六路在 `remotes[]` 层逐 remote 判 (behind/diverged → 建议 pull; ahead → 不重复, 归 `has_pending_push`;
benign unknown → 不触发; `no_local_tracking_ref` 非 benign → 路由到 1.36; not_refreshed/network/auth → "无法验证, 查网络凭据";
其他 reason → fail-CLOSED 同上档), **第七路**在 `gitlink_integrity[]` 层逐 (R,S) 对判, 与前六路正交, 同一次 scan 两层可同时命中, 两条建议都要出。

降级例外 (OQ-C, owner 2026-07-19): 若 `has_unreachable_remote == true`, 或所有 enforced 腿的 `evidence_grade ∈ {stale_unverified, expired}`
(本次 scan 没拿到任何新鲜证据), 则不走 dispatch, 改出一条"离线 / 远端不可达, 同步状态不可知"降级横幅。
**降级只作用于建议层, 裁决层照常 fail-CLOSED 报 `overall_parity: false`** —— 裁决层去抖会重新引入假绿。

---

## 3. 哪些 remote 需要补推 + 修复建议

按本仓库 enforced 集合 (主仓 + aria + standards 各自 origin/github), 事件形态下需要补推的是 **`github` 这一侧**:

```bash
# 第一步 (方向是推子模块, 不是动主仓 gitlink —— 主仓引用是对的, 缺的是镜像那侧)
git -C aria push github master

# 第二步: 子模块推完再补主仓, 否则 GitHub 上会短暂存在一个指向不可达 commit 的主仓 commit
git push github master

# 如 standards 本轮也有变更, 同样两步
git -C standards push github master
```

顺序不可颠倒: 子模块先于主仓 gitlink (见 memory `feedback_sequenced_multirepo_gitlink_bump`)。

补充要点:

- **验证方式不是看 `git push` 的输出**。push 说 "Everything up-to-date" 恰恰是本事故的伪装。正确验证是重跑
  `/state-scanner`, 看新 snapshot 里 `remote_refresh.legs` 中 `(aria, github)` 的 `fetch_ok == "true"` 且 `fetched_at` 是本次时间,
  `evidence_grade == "fresh"`, 并且 `gitlink_integrity` 中 `(github, aria)` 从 `orphaned` 变回 `ok`, `overall_parity` 变 `true`。
- **不要盲目 `git submodule update --remote aria`**。那是 `hint_type: "update"` (behind) 场景的解药; 本事件是本地领先远程 (ahead),
  执行它会丢弃本地 commits —— 这正是 US-008 方向性数据丢失护栏 (`sync.py` behind→update / ahead→push 强制方向判据) 要挡的事,
  该护栏恒开启、设计上不允许关闭。
- **Phase C.2.5 的自动多远程推送** (`phase-c-integrator`) 才是长期解药: 发版流程里所有 enforced remote 自动推 + post-push SHA 验证。
  手工补推只是这次的止血。
- **CLAUDE.md 发版检查清单**已把"多远程推送"列为硬项 (灾备 fallback 就是上面这几条 `git -C ... push github master`),
  原因写得很直白: 插件市场从 GitHub 拉, Forgejo 是主开发仓, 只推 Forgejo 会让市场版本滞后 —— 这正是 2026-04-12 aria v1.11.1 的事故。

---

## 4. 诚实边界

- 本次按测试约束**没有真跑** scan.py / fetch, 上文所有字段值是按 schema 与判据推演的**预期形态**, 不是实测 snapshot。
- 形态二 (主仓 gitlink 也没推) 下 `overall_parity` 仍可能为 `true`, 只靠 `has_pending_push` 提示。这是当前实现的已知弱点,
  follow-up 见 Aria #165。不把它说成"一定会红"。
- `k_eff` 目前是冷启动 `k_eff = k_min` (observed_rotation DEFERRED, fail-CLOSED), 所以 `orphan_unverified` 的升级阈值偏保守。
