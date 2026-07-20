# 多远程 parity 扫描 (origin=Forgejo / github=镜像, 漏推 github)

> 依据: state-scanner v3.1.1 快照 (aria-plugin v1.61.0)。本文是"我会怎么扫 + 会输出什么 + 建议什么"的说明, 未真正执行 scan.py / fetch / push。

---

## 1. 我会怎么扫

### Step 0 (硬约束, 不可协商)

Phase 1 全部字段由 `scripts/scan.py` 机械采集, 我**不允许**用 `git status` / `git remote -v` / `git rev-list` 逐字段手工替代, 也不允许在 scan.py 失败时手工 Bash 补齐:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/scan.py" \
  --output .aria/state-snapshot.json
```

退出码契约:

| 退出码 | 含义 | 我的动作 |
|--------|------|----------|
| 0 | 全部采集成功 | 读 snapshot, 进阶段 2 |
| 10 | 部分软错误 (`errors[]` 有条目) | 读 snapshot, 对受影响子阶段挂 warning, 继续 |
| 20 | 硬前置失败 (非 git repo / 输出路径不可写) | abort, 展示 stderr, 不读 snapshot |
| 30 | scan.py 内部未捕获异常 | abort, 提示 report bug |

Schema 契约: `snapshot_schema_version == "1.0"`, additive-only 演进。

### 本题真正吃到的两个采集阶段

- **Phase 0.5 `remote_refresh`** (F3′, 新鲜度信号的唯一生产者) —— 跑在最前面, 按 host 分桶并行 `fetch --prune`, 每条 leg 记 `fetched_at` / `fetch_ok` 三态 / `error_kind` (Rule #7 类型化标签, 绝不回传原始 stderr, 因为 fetch 的 stderr 可能回显带凭据的 URL) / `generation_fetched` / `consecutive_unverified`。这是我判断"origin 与 github 的证据到底新不新"的唯一来源 —— **新鲜度靠获取, 不靠测量**。
- **Phase 1.12 `sync_status`** (恒开启, 不可关闭 —— 它承载 US-008 方向性数据丢失护栏), 其中 `sync_status.multi_remote` 就是多远程 parity 主体, 对主仓 + 每个子模块 × 每个 enforced remote 逐条判 parity。

⚠️ 我**不会**用 `sync_status.remote_refs_age` 来判断"上次同步多久了" —— 该字段已 DEPRECATED (F9′ 8.4): Phase 0.5 自己的 fetch 会改写 `.git/FETCH_HEAD`, 使它每次 scan 后恒近似 `"1m"`, 测的是"本次 scan 自己刚 fetch 多久前", 不是任何有意义的陈旧度。新鲜度判据一律读 `multi_remote.*.remotes[].evidence_grade`。同理 `multi_remote.local_refs_stale` 已 RETIRED (F2′), 不读。

---

## 2. 我会看哪些字段 / 按什么判据

### 2.1 逐 remote 条目 (`RemoteEntry`)

路径: `sync_status.multi_remote.main_repo.remotes[*]` 与 `sync_status.multi_remote.submodules[*].remotes[*]`。

关键字段: `name` / `remote_head` / `parity` / `behind_count` / `ahead_count` / `reachable` / `reason` / `method` / `evidence_grade` / `fetch_ok`。

`parity` 五值枚举, **以本地 HEAD 为基准**:

| parity | 判据 | 本题含义 |
|--------|------|----------|
| `equal` | `local_head == remote_head` | 该 remote 已同步 |
| `ahead` | `remote..HEAD > 0` 且 `HEAD..remote == 0` | 本地有该 remote 没有的 commit = **漏推** |
| `behind` | `HEAD..remote > 0` 且反向为 0 | 本地落后 |
| `diverged` | 两向计数均 > 0 | 需人工 merge/rebase |
| `unknown` | 见 `reason` 枚举 (`no_local_tracking_ref` / `not_refreshed` / `network_timeout` / `auth_failed` / `shallow_clone` / `detached_head` / `remote_branch_missing` / `parse_error` / `not_found`) | 不可判定 |

### 2.2 新鲜度 (`evidence_grade`, D20 三值, 独立字段, 从不折进 `reason`)

- `fresh` —— 证据资格 E 成立: `fetched_at != null 且 (now - fetched_at) <= evidence_window` (默认 1h)。**只有它能当 `overall_parity` 存在子句的正证据**。
- `stale_unverified` —— `¬E` 但豁免资格 X 成立 (代际差 ≤ `k_eff` 且墙钟 ≤ `hard_cap` 默认 7d 且 `consecutive_unverified < k_eff`)。诊断态: 可见, **不作证, 不阻断**。
- `expired` —— `¬E ∧ ¬X`, 阻断态 (fail-CLOSED)。若原 `parity == "equal"`, 会被 `_apply_freshness_downgrade` 改写成 `parity: "unknown" + reason: "not_refreshed"` —— 绝不允许双重陈旧的 `equal` 冒充"已同步"。

三档全分割 (互斥 + 全覆盖 E×X 定义域)。

### 2.3 汇总三 flag

- `overall_parity: bool` —— 四子句**全部满足才为 true** (`_overall_parity`):
  1. `enforced_set != ∅` (守 `all([])` 的 vacuous-true 陷阱);
  2. `∃ r: parity == equal 且 evidence_grade == "fresh"` (两者都要);
  3. `∀ R ∈ gitlink_integrity: ¬gitlink_blocking(R, k_eff)`;
  4. `∀ r: parity ∉ {behind, diverged} 且 ¬blocking_unknown(r)`。
- `has_pending_push: bool` —— 存在 `parity == "ahead"` 的 remote。
- `has_unreachable_remote: bool` —— **只**看 `fetch_ok == "false"` 三态 (真去问了且失败), 与 `error_kind` 取值无关, 零枚举 fail-CLOSED。`not_attempted` (被 `refresh_deadline_seconds` 砍) **不算** 不可达 —— "我们没去问" ≠ "对方不可达"。

### 2.4 子模块 gitlink 跨仓可达性 (`gitlink_integrity[]`, Phase 2A / F10″)

per-(R, S) 一条 —— R 遍历主仓 enforced remote, S 遍历全部已声明子模块 (含未 init)。检测: **主仓在 R 上已发布的那个 commit 所引用的子模块 gitlink, 在该子模块自己的 R 上是否 branch-reachable**。9 分支状态: `ok` / `orphaned` / `orphan_unverified` / `no_published_ref` / `not_a_gitlink` / `uninitialized` / `no_matching_remote` / `shallow_unverifiable` / `soft_error`。只有 `orphaned` 恒阻断, `orphan_unverified` 需连续 `k_eff` 次才升级阻断。

这一项与本题最相关的两种走向, 见下文第 4 节。

---

## 3. 我预期会输出什么

### 区块 8 · 🔄 同步状态 (含多远程子块)

按 output-formats 的多远程变体渲染 (仅当 `multi_remote.enabled` 且 remote 数 > 1 才出块, 单远程静默跳过避免噪音):

```
🔄 同步状态
───────────────────────────────────────────────────────────────
  当前分支: master (超前 origin/master 0 / 落后 0)

🌐 多远程一致性
───────────────────────────────────────────────────────────────
  ⚠️ 主仓库: github 落后 1 commit
     修复: git push github master
     当前: origin=<sha7> | github=<sha7> (ahead 1)
  ⚠️ aria 子模块: github 落后 N commits
     修复: git -C aria push github master
     当前: origin=<sha7> | github=<sha7> (ahead N)
  ✅ standards 子模块: 所有远程一致 (origin, github)
```

说明措辞: 输出面板用"github 落后 N commits"是从**远程视角**说的; 对应 snapshot 字段是 `remotes[name=github].parity == "ahead"` + `ahead_count == N` (以本地为基准)。两者是同一件事的两种表述, 不要混淆。

### 汇总 flag 的预期取值 (这是本题最容易看错的地方)

漏推 github = 本地领先 github ⇒ github 条目 `parity: "ahead"`。按 F4′ 定义:

- `has_pending_push: **true**`
- `overall_parity: **true**` —— 因为 `parity: ahead` **不计入** `overall_parity` (它只进 `has_pending_push`); 子句 2 由 `origin=equal/fresh` 满足, 子句 4 只排除 `behind/diverged/blocking_unknown`。schema 的 worked example 逐字写明: `origin=equal, github=ahead` ⇒ `overall_parity: true, has_pending_push: true`。
- `has_unreachable_remote: false` (github 可 fetch, 只是没收到新 commit)。

因此 **推荐规则 `multi_remote_drift` (priority 1.35) 不会触发** —— 它的触发条件是 `overall_parity == false`; 且即便触发, 六路 dispatch 里 `parity == ahead` 那一路显式 `triggers_rule: false` ("不重复 —— 已由 has_pending_push 覆盖")。§10.7 也把 `has_pending_push: true (仅 ahead)` 列为**不触发条件**: 正常待推送, 不报警。

我会诚实地把这一点讲给你: 漏推镜像在当前判据下是 **info 级"待推送"提示**, 不是告警, `overall_parity` 仍为 true。这不是我在弱化问题, 而是当前 `overall_parity` 的语义边界 —— 它回答的是"有没有正证据说某个 remote 同步了 + 有没有落后/分歧/阻断态", 不回答"每个 enforced remote 是不是都推齐了"。要靠 `has_pending_push` 这条来接住漏推。

---

## 4. 一个必须分清的岔路: 主仓推没推到 github

你说的"忘记推 github", 有两种落法, 判据完全不同:

**情形 A —— 主仓和子模块都只推了 origin (你描述的典型情况)**
github 上主仓的 ref 还停在旧 commit, 它引用的还是**旧 gitlink**, 那个旧 gitlink 在 aria 的 github 上是可达的 ⇒ `gitlink_integrity[(github, aria)].status == "ok"`, 不阻断。表现就是上面那套: 两处 `ahead` + `has_pending_push: true`, `overall_parity: true`。

**情形 B —— 主仓 gitlink bump 推到了 github, 但 aria 子模块没推 github**
github 上主仓已发布的 commit 引用了一个 aria 的**新** commit, 而该 commit 在 aria 的 github 上不存在 ⇒ `gitlink_integrity[(github, aria)].status == "orphaned"` ⇒ 子句 3 被打破 ⇒ **`overall_parity: false`**, 镜像上的 clone 会拉不到子模块。这才是真正会伤人的形态 (对应主仓 Aria #165 的镜像漏推)。

已知缺口 (我如实标注): `multi_remote_drift` 的六路 dispatch 表**只覆盖 `remotes[]` 层, 尚未新增 gitlink 专属的第七路**。AC-16 设想的建议 `git -C S push R <branch>` 目前只是 proposal 里的设计意图, 未接入机械 dispatch。所以情形 B 下我会看到 `overall_parity: false`, 但规则给不出针对性的 gitlink 修复语句 —— 需要我在输出层额外检查 `gitlink_integrity[]` 是否有 blocking 条目并手动点出来。

**正确的推送顺序** (子模块先, 主仓后): 先把子模块推齐所有 remote, 再推主仓 gitlink, 才不会在任何时刻在镜像上留下 orphaned gitlink。

---

## 5. 给你的修复建议

按 remote 逐条给, 不发笼统的"git push" (v9 改写的初衷: 旧版对所有 `overall_parity: false` 一律建议 push, 在 behind 场景下 push 无意义甚至诱导强推)。

```bash
# 1) 先推子模块 (顺序要紧: 子模块先, 主仓后)
git -C aria push github master
# 若 standards 子模块本轮也有新 commit:
git -C standards push github master

# 2) 再推主仓 (gitlink bump)
git push github master

# 3) 复核: 重跑扫描, 期望 github 全部 parity=equal 且 evidence_grade=fresh
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/scan.py" \
  --output .aria/state-snapshot.json
```

复核的验收判据 (别只看命令 exit 0):

- `main_repo.remotes[name=github].parity == "equal"` 且 `evidence_grade == "fresh"`;
- 每个有变更的子模块, `remotes[name=github].parity == "equal"`;
- `has_pending_push == false`;
- `gitlink_integrity[]` 中 `remote == "github"` 的条目全部 `status == "ok"`;
- `overall_parity == true` **且**至少一条 `equal/fresh` 撑起子句 2 —— 如果这轮 fetch 因 deadline 被砍 (`fetch_ok == "not_attempted"`) 或 `evidence_grade` 落到 `expired`, `equal` 会被降级成 `unknown/not_refreshed`, 那时的 "true" 不成立、"false" 也不代表真的没推齐, 应重跑而不是当成结论。

配套的流程侧建议 (与 Aria 项目自身约定一致):

- 多远程推送在 Phase C.2.5 已自动化 (`phase-c-integrator`), 手动推是灾备路径 —— 这次漏推说明走了手动路径, 下次让 C.2.5 兜。
- 想让扫描把 github 当"必须推齐"的对象而不是可选发现项, 在 `.aria/config.json` 显式写 `state_scanner.multi_remote.enforced_remotes: ["origin", "github"]`。注意 F5′ 陷阱: `[]` 或 `null` **不是**空集, 而是"自动发现全部远程 (减去 `read_only_remotes`)"。配了白名单后, 名字不存在的 remote 会以 `no_matching_remote` 出现, 不会造出幽灵 fetch leg。
- 若某个 remote 只读 (纯上游镜像, 本来就不该推), 放进 `read_only_remotes` 而不是靠忽略告警。

---

## 6. 我不会做的事

- 不代你执行 `git push` / `git fetch` / 任何写操作 —— 扫描全程只读, 修复命令交你确认后执行。
- 不用手工 Bash 逐字段替代 scan.py (v3.0.0 机械化契约禁区)。
- 不把 git 命令的原始 stderr 贴进输出或 snapshot —— fetch 的 stderr 可能回显带凭据的 remote URL (Rule #7); 只用类型化标签 `error_kind ∈ {network, auth_403, non_ff, git_missing, other}`。
- 不依赖 `remote_refs_age` / `local_refs_stale` 做陈旧度判断 (前者 DEPRECATED, 后者 RETIRED)。
