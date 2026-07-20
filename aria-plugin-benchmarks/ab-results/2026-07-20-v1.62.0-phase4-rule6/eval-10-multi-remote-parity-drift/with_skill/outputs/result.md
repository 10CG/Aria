# eval-10 多远程 parity drift — with_skill 产出

> 臂: with_skill (`/home/dev/Aria/aria/skills/state-scanner/` v1.62.2)
> 场景: 主仓 + 子模块双 remote (origin=Forgejo / github=镜像), aria-plugin v1.15.0 子模块更新只推了 origin
> 说明: 本文件是**描述性产出** —— 描述"我会怎么扫、会输出什么字段、给什么建议", 未执行 scan.py, 未执行任何 fetch/push/写操作。

---

## 一、我会怎么扫 (执行路径)

### Step 0 (硬约束): 机械跑 scan.py, 不手工逐字段采集

state-scanner v3.x 的不可协商契约: Phase 1 全部字段由 `scripts/scan.py` 机械产出, AI 不得用 `git remote -v` / `git rev-list` 逐字段替代, 也不得在 scan.py 失败时"降级"手工补齐。

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/scan.py" \
  --output .aria/state-snapshot.json
```

退出码契约: `0` 全成功 → 读 snapshot 进阶段 2; `10` 部分软错误 (snapshot 仍可用, 见 `errors[]`) → 展示 warning 后继续; `20` 硬前置失败 (非 git repo / 输出路径不可写) → abort; `30` 内部异常 → abort + 报 bug。

### 关键子阶段 (回答本问题真正吃的两块数据)

| 子阶段 | snapshot 顶层字段 | 在本场景的作用 |
|---|---|---|
| Phase 0.5 `remote_refresh` (F3′) | `remote_refresh` | **新鲜度信号的唯一生产者**。per-(repo, remote) 一条 leg, 每 host 一个线程池并行 `fetch --prune --no-tags`, 顺序准入闸门 + `refresh_deadline_seconds` (默认 15s) 兜底。跑在所有 Phase 1 collector **之前**, 保证同一份 snapshot 内的 parity 结论不是拿几天前的陈旧 ref 算出来的 |
| Phase 1.12 `sync_check` (恒开启, 无开关) | `sync_status` (含 `sync_status.multi_remote`) | per-remote parity 计算 + `gitlink_integrity[]` + 三个汇总 flag |

两点必须说清楚, 否则结论会撒谎:

1. **新鲜度靠"获取", 不靠"测量"**。`sync_status.remote_refs_age` (FETCH_HEAD mtime) 已 **DEPRECATED** —— 它是仓库全局量, 结构上做不了 per-(repo, remote) 判据, 而且 Phase 0.5 自己的 fetch 会把它改写成恒约 `"1m"`。现行陈旧度判据是 `sync_status.multi_remote.*.remotes[].evidence_grade`。
2. **`sync_check` 不是 opt-in, 也没有开关**。历史文档里的 `state_scanner.sync_check.{enabled,check_submodules,warn_after_hours}` 是虚构键, 代码从不读 (F9′ 9.2 勘误), 写进 `.aria/config.json` 也不生效。真正可配的是 `state_scanner.sync_freshness.*` 与 `state_scanner.multi_remote.*`。

### 枚举范围: 主仓 + **每一个**子模块 × **每一个** remote

`multi_remote.main_repo.remotes[]` 与 `multi_remote.submodules[].remotes[]` 各自遍历。remote 集合默认自动发现 (`git remote`), 配了 `state_scanner.multi_remote.enforced_remotes` 则用白名单; **配了但仓库里不存在的 remote 名不产出条目**, 而是记入 `remote_refresh.no_matching_remotes[]` (RM-3/F5′: 绝不伪造成一条 ghost fail 腿)。

remote HEAD 只走**单一路径** `method: "local_refs"` (读 `refs/remotes/<remote>/<branch>`)。`ls_remote` / `verify_mode` 已于 v1.62.0 退役 —— Phase 0.5 已经 fetch 过每条 enforced 腿, 本地 ref 即服务器真相, 再打一次 ls-remote 只会造出第三个独立可达性计算点。

---

## 二、我会输出什么 (字段级)

### 快照字段形态 (本场景预期值)

只推了 origin、github 落后一次 gitlink bump 时, 从**本地 HEAD 视角**算出的 parity 是 `ahead` (local 领先 mirror), 不是 `behind`:

```yaml
sync_status:
  multi_remote:
    enabled: true
    enforced_remotes_resolved: ["origin", "github"]   # 裁决实际覆盖的 remote 名集合
    excluded_read_only: []
    main_repo:
      path: "."
      branch: "master"
      local_head: "<sha>"
      remotes:
        - name: "origin"
          parity: "equal"
          behind_count: 0
          ahead_count: 0
          evidence_grade: "fresh"        # 本轮 Phase 0.5 刚 fetch 成功
          fetch_ok: "true"
          method: "local_refs"
          reason: null
        - name: "github"
          parity: "ahead"                # ← 本地领先镜像 = 漏推的形态
          ahead_count: 1                 # gitlink bump 那一个 commit
          behind_count: 0
          evidence_grade: "fresh"
          fetch_ok: "true"
          reason: null
    submodules:
      - path: "aria"
        branch: "master"
        remotes:
          - {name: "origin", parity: "equal", ahead_count: 0, behind_count: 0, evidence_grade: "fresh"}
          - {name: "github", parity: "ahead", ahead_count: <N>, behind_count: 0, evidence_grade: "fresh"}
      - path: "standards"
        remotes: [...]                   # 无变更时两条均 equal/fresh
    gitlink_integrity:
      - {remote: "origin", submodule: "aria", status: "ok", consecutive_unverified: 0}
      - {remote: "github", submodule: "aria", status: "ok", consecutive_unverified: 0}
      - ...                              # R × S 全对, 含未 init 的子模块
    overall_parity: true                 # ← 见下方判据推演, 不是 false
    has_pending_push: true               # ← 本场景的**真正信号**
    has_unreachable_remote: false
```

### 判据推演 (为什么是这几个值)

**`overall_parity` 四子句** (`multi_remote.py::_overall_parity`, 全满足才 `true`):

1. `enforced_set ≠ ∅` — 满足 (origin, github)。
2. `∃ r: parity == "equal" ∧ evidence_grade == "fresh"` — origin 满足。注意**两个条件都要**: 一个 `stale_unverified` 的 `equal` 不算正证据 (这是 14h 假绿事故的根)。
3. `∀ R ∈ gitlink_integrity: ¬gitlink_blocking(R, k_eff)` — 本场景全 `ok`, 满足。
4. `∀ r: parity ∉ {behind, diverged} ∧ ¬blocking_unknown(r)` — github 是 `ahead`, **不在** 集合内, 满足。

⇒ `overall_parity: true`, 因此 **`multi_remote_drift` (priority 1.35) 在本场景不触发**。

这不是漏报, 是刻意的语义分工:

| 信号 | 含义 | 谁来报 |
|---|---|---|
| `parity: ahead` → `has_pending_push: true` | 本地有 mirror 还没有的 commit = **待推送**, 正常状态, 不是"数据不一致告警" | 输出层 info 级 + `🌐 多远程一致性` 区块逐 remote 点名 |
| `parity: behind/diverged` → `overall_parity: false` | 本地落后/分歧 = 需要 pull 或人工决策 | 规则 1.35 dispatch 第一路 |

规则 1.35 的 dispatch 表对 `ahead` 明写 `triggers_rule: false` / "不重复 — 已由 `has_pending_push` 覆盖, 本规则不再对 ahead 发建议"。v9 之所以这么改, 正是因为旧版把 `overall_parity: false` 的所有成因一律建议 `git push` —— 那本身是方向性 bug (behind 场景下 push 无意义甚至诱导强推)。

**如果本场景真触发了 1.35**, 那说明快照里还有别的成因 (例如某条腿 `evidence_grade: expired` 被 `_apply_freshness_downgrade` 改写成 `parity: unknown` + `reason: not_refreshed`), 那时按六路 dispatch 逐条分派, 而**不是**对整块发一条 push 建议。

**`parity: unknown` 的现行处理** (不建议方向性操作):

| reason | 归档 | 动作 |
|---|---|---|
| `detached_head` / `shallow_clone` / `remote_branch_missing` | benign unknown | 不触发, 零证据不当负证据 |
| `no_local_tracking_ref` ∧ `evidence_grade == "fresh"` | benign unknown | 不触发 (1.35 内消化) |
| `no_local_tracking_ref` ∧ `evidence_grade != "fresh"` | 改路由 | 走规则 **1.36 `has_unpublished_branch`**: "该分支可能从未推过", 建议 `git -C <path> push -u <remote> <branch>` (先确认分支名) |
| `not_refreshed` / `network_timeout` / `auth_failed` | 不可验证 | "无法验证, 请检查网络或凭据" —— **不建议 pull/push** |
| 其他 / 未来新增枚举 | fail-CLOSED 补集 | 同上档处理 |

另: `has_unreachable_remote == true` (或全部 enforced 腿的 `evidence_grade ∈ {stale_unverified, expired}`) 时, 1.35 不走 dispatch, 改出一条「离线 / 远端不可达, 同步状态不可知」降级横幅 (OQ-C 裁定 2026-07-19)。降级**只在建议层**, 裁决层照常 fail-CLOSED。

### 渲染 (输出格式区块 8 + 多远程一致性区块)

```
🔄 同步状态
───────────────────────────────────────────────────────────────
  当前分支: master (超前 origin/master 0 / 落后 0)
  证据: 主仓 origin=fresh · github=fresh; aria origin=fresh · github=fresh

🌐 多远程一致性
───────────────────────────────────────────────────────────────
  ⚠️ 主仓库: github 待推送 (本地领先 1 commit)
     当前: origin=<sha7> | github=<sha7>  (ahead 1, evidence_grade=fresh)
     修复: git push github master
  ⚠️ aria 子模块: github 待推送 (本地领先 N commits)
     当前: origin=<sha7> | github=<sha7>  (ahead N, evidence_grade=fresh)
     修复: git -C aria push github master
  ✅ standards 子模块: 所有远程一致 (origin, github)
  ✅ gitlink 完整性: 6/6 对 ok (origin·github × aria·standards·aria-orchestrator)

  汇总: overall_parity=true · has_pending_push=true · has_unreachable_remote=false
```

要点 (评分方向对应):

- **per-remote 而非单一状态**: 每个 (repo, remote) 一行, 带 `parity` / `ahead_count` / `behind_count` / `evidence_grade` / `fetch_ok`。
- **枚举全部 remote 含子模块**: 主仓 + 每个已声明子模块 (含未 init 的, gitlink 层照样出条目)。
- **给数字**: `ahead_count` / `behind_count` 直接落到行内, 不写"有差异"这种糊话。
- **不出现 "Everything up-to-date" 式歧义**: `git push` 对 origin 会回 "Everything up-to-date", 但那只是**对这一个 remote** 的结论。本区块的 ✅ 一定绑定具体 remote 名 + 具体证据等级, 绝不出现无主语的"已同步"。
- **陈旧证据必须逐条点名**: 若某条腿是 `stale_unverified`, 输出「⚠️ 证据陈旧 (parity 结论未经本轮验证): - 主仓库 github」, 不允许把它折进一个汇总 ✅。

---

## 三、给用户的修复建议

### 直接结论

你的 origin (Forgejo) 是最新的, **github 镜像落后一次 aria-plugin v1.15.0 的 gitlink bump**。快照上的形态是 `parity: ahead` + `has_pending_push: true`, 不是 `behind` —— 这是"本地有、镜像没有", 属于待推送, 不是数据不一致告警, 所以规则 1.35 不会响; 别因为没看到红字就以为推全了。

### 修复命令 (顺序有讲究)

**必须先推子模块, 再推主仓。** 反过来会让 github 上的主仓引用一个 github 上不存在的子模块 commit —— 那时 `gitlink_integrity[(github, aria)]` 会翻成 `orphaned`, 这是 `overall_parity` 第三子句的**恒阻断**状态, 而且任何人从 github `clone --recursive` 都会当场断裂。

```bash
# 1. 先推子模块到 github (aria 有变更; standards 若也动过同样处理)
git -C aria push github master

# 2. 再推主仓 (含 gitlink bump)
git push github master

# 3. 复扫确认 (只读, 会重新 fetch 一遍拿 fresh 证据)
/state-scanner
```

复扫后期望: 主仓与 aria 的 github 腿变成 `parity: "equal"` + `evidence_grade: "fresh"`, `has_pending_push: false`, `gitlink_integrity` 全 `ok`。

### 两个别踩的坑

1. **别用 `git push` 的输出当同步判据**。`git push origin` 回 "Everything up-to-date" 只说明 origin 一个 remote, 对 github 零信息量。判据请看 `enforced_remotes_resolved` 覆盖下的 per-remote `parity` + `evidence_grade`。
2. **别只看主仓**。多 repo ship 的漏推 90% 漏在子模块那一侧, 而且主仓推成功 + 子模块没推 = `gitlink_orphaned`, 比"两边都没推"更糟 (对外表现为镜像仓库直接不可用)。

### 想让这类漏推以后自己红出来

在 `.aria/config.json` 写死白名单, 别依赖自动发现:

```json
{
  "state_scanner": {
    "multi_remote": { "enforced_remotes": ["origin", "github"] },
    "sync_freshness": { "evidence_window_seconds": 3600, "hard_cap_days": 7 }
  }
}
```

`enforced_remotes` 决定裁决覆盖面 (体现在 `enforced_remotes_resolved`); 留空 = 自动发现全部远程, 新加一个临时 remote 就会连带进裁决。配了但仓库里没有的名字进 `remote_refresh.no_matching_remotes[]`, 不会伪造成一条失败腿。

另外, 十步循环 Phase C.2.5 (phase-c-integrator) 自 v1.15.0 起会自动推送所有 enforced remote 并做 post-push SHA 验证 —— 走完整 Phase C 流程发版, 这次的漏推本来就不会发生。手工 `git push origin` 绕过了那道闸。
