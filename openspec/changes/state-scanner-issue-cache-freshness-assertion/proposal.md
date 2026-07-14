# Proposal: `issue-cache-freshness` 检查重定义 + snapshot `generated_at` 字段

> **Status**: **Draft v4** (2026-07-14: **R7-qa C-1 一票否决题按 D19 裁定 — 求值基底 = (a) lag-1**: 重定义 check 读**上一份** snapshot [Phase 1.11 时本次 issue_status 尚不存在, 本次文件尚未写盘 — 这是结构事实非选择]; collector 不挪位置的承诺保留; **AC-2 改两跑断言** + lag-1 语义公示; AC-4 可验收面按 R7 RM-12 收窄到单 check 子树) ← v3 (§3 撤回条件性反转) ← v2 ← v1
> **Level**: 2 (Minimal — 单一关注点: 一个 custom check 的断言重定义 + 一个 additive schema 字段)
> **Created**: 2026-07-12
> **Source**: `state-scanner-stale-refs-false-parity` 的 R1/R2/R3 发现; 经 owner 决策**拆出独立 Spec** —— 与 parity 机制**零代码路径重叠** (5/5 agent 一致建议)
> **Target**: aria-plugin (子模块 `aria/`)

---

## Why

### 1. `issue-cache-freshness` 检查结构性恒红

`.aria/state-checks.yaml` 的 `issue-cache-freshness` 断言 `.aria/cache/issues.json` 的 **mtime 在 30 分钟内** (`find -mmin -30`), 其自述目的是「**Phase 1.13 是否真的跑了的反向证据**」。

但 `scan.py` 的执行顺序是: `custom_checks` (Phase 1.11, L105) → `issue_scan` (Phase 1.13, L108)。

⇒ **check 永远只能看到上一次 scan 留下的 cache**。只要两次扫描间隔 > 30min (**绝大多数正常 session**), 它就恒红。

**实证** (本 session 亲历): 首次 scan 报 `STALE — cache > 30min`, 而 cache 文件的 mtime 恰恰**就是本次 scan 写的** (11:03:54)。第二次 scan (6 分钟后) 仍报 STALE —— 因为 1.11 跑的那一刻, 看到的还是**上一轮**的 mtime。

**后果**: 一个恒红的检查 = 告警疲劳 = 该检查失去意义。它想当「1.13 跑没跑」的证据, 却结构性地永远滞后一拍。

### 2. 纯挪位置会把「恒红」换成「恒绿真空」

最直觉的修法是把 `custom_checks` 挪到 `issue_scan` 之后。**但那更糟**:

`issue_scan` 与 `custom_checks` 是**同一进程内**的两个 collector。挪位置后, `issue_scan` 刚在毫秒前写完 cache ⇒ `find -mmin -30` **按构造必然 pass** ⇒ 该检查变成**同义反复**, 只在 `issue_scan` 写盘失败时才红。

> **从假红变假绿, 是同一枚硬币的反面。** (母 Spec 的核心对偶不变量: **假绿的反面是恒红, 两者同样零信息量。判据 = 该信号在健康常态下应是什么值。**)

**且根因不是「collector 顺序」**: 母 Spec 的 F3′ 是「消费者早于生产者」的**真顺序 bug**; 本缺陷是「一个设计为**外部**反向证据的检查, 被放进了它要审计的进程内部」的**设计混淆**。两者不同族 —— 这也是本 Spec 从母 Spec 拆出的理由 (母 Spec 的「四者同根」叙事在这一项上是错的)。

### 3. 🔴 正确的修法依赖一个**不存在的字段**

正确断言应是**同一 snapshot 内**的自洽比较: `issue_status.fetched_at` vs **本次 scan 的开始时刻** —— 两个时间戳来自同一次 scan, 天然自洽, 从根上消除 run-to-run 依赖。

**但 snapshot 顶层没有 `generated_at`**:
```
$ python3 -c "import json; print(sorted(json.load(open('.aria/state-snapshot.json')).keys()))"
['architecture','audit','changes','coordination_fetch','custom_checks','errors','forgejo_config',
 'generated_by','git','handoff','handoff_worktrees','interrupt','issue_status','openspec',
 'project_root','readme','requirements','snapshot_schema_version','standards','sync_status',
 'tracks_multibranch','upm']
```
`scan.py` 全文零 `datetime.now` / `utcnow` / `time.time` / `isoformat` —— **从未有任何代码捕获过「本次 scan 的开始时刻」**。

**兄弟 Spec 已经踩过这个耙子**: `openspec/changes/aria-2.0-m7-fleet-aggregation` (Approved) 的 probe-first recon (proposal L82) **已明写**: 「snapshot 顶层**无** `generated_at` 字段, 实测仅 `snapshot_schema_version`/`generated_by`/`project_root`, 故 age 以**文件 mtime** 为权威」—— 它被迫用文件 mtime 兜底。

⇒ 加 `generated_at` **顺手修好 m7-fleet-aggregation 的 CAVEAT-age**, 是一个双赢的 additive 字段。

---

## What Changes

### 1. snapshot 顶层新增 `generated_at` (additive)

`scan.py` 在 `build_snapshot` **入口**捕获 ISO 8601 UTC 时刻, 写入顶层 `generated_at`。

- **additive** ⇒ `snapshot_schema_version` **不 bump**。
- `generated_at` 已在 `normalize_snapshot.py` 的 `TIMESTAMP_KEYS` 白名单里 (L47) ⇒ 会被打码成 `<timestamp>` ⇒ **不会破坏 `test_two_consecutive_runs_diff_zero`**。(实测确认。)

### 2. `issue-cache-freshness` 断言重定义

从「cache 文件 mtime vs 墙钟 now」改为「**本次 snapshot 内** `issue_status.fetched_at` vs `generated_at`」。

- 该检查**不再**依赖 collector 顺序 ⇒ **`custom_checks` 不需要挪位置**。
- 🔴 **v4 (D19) 求值基底写死 = lag-1**: check 在 Phase 1.11 执行时, 本次 scan 的 `issue_status` 尚不存在、本次 snapshot 尚未写盘 (scan.py L237-240 结尾一次性写) ⇒ **唯一自洽读数源 = 上一份 `.aria/state-snapshot.json`** (两操作数 [`generated_at`, `issue_status.fetched_at`] 同源同代, 断言内部一致)。**语义公示: 本 check 是 lag-1 探测器** — 审计的是**上一次** scan 的产物, 故障在**下一次** scan 被看见 (外部反向证据型检查的诚实语义: 滞后一拍换独立性)。上一份 snapshot 不存在 (首跑) ⇒ check SKIP 可见 (非 PASS 非 FAIL)。
- 它从「1.13 跑没跑的外部反向证据」变成「1.13 **在本次 scan 内**是否产出了新鲜结果」—— 语义更准确, 且**可在健康常态下 pass、在真故障时 fail**。
- 更新该 check 的 `description` (它不再是「外部反向证据」)。

### 3. ⚠️ **消除既有 flaky 测试 — v3 修正: v1 归因条件性正确, 但只是 6 条通道之一** (R5-C-E → CE 归因复验 2026-07-14 结案)

> 🔬 **v3 (CE 复验, 干净条件 5 组对照)**: `custom_checks` **确是**漂移通道 — 触发条件 = issues.json **缺失或 mtime>30min** (v1 说的 cache>30min 场景**成立**); 新鲜热缓存下不触发 (R5 的观察在那个条件下也对)。R5 与 R6 的矛盾根源 = **缓存新鲜度这个隐藏变量**。
> ⇒ v1 的归因**条件性正确**, v2 的全称撤回 (「无一是 custom_checks」) **过强, 收回**。
> ⇒ 但 v2 的**结论**保留: 实测共 **6 条**漂移通道, 本 Spec 的修法只能杀 custom_checks 这一条 ⇒ **仍不声称消除该 flaky 测试** — 整体消除归母 Spec tasks 12.10 (offline 旁路为主)。

<details><summary>v2 原撤回文 (保留溯源; 其全称否定已被 CE 复验推翻)</summary>

> 🔴 **v1 声称**: `test_two_consecutive_runs_diff_zero` 的 flaky 源于 `custom_checks` 的 `failed:1 → failed:0` (cache > 30min 时 run1 红 run2 绿), 且**本 Spec 的修法能从根上消除它**。
>
> **实测证伪。** owner 连跑两次全量测试 (未修改代码, aria HEAD `0964496`):
> ```
> Run A: Ran 1006 tests ... FAILED (failures=1)   test_two_consecutive_runs_diff_zero
> Run B: Ran 1006 tests ... FAILED (failures=1)   同一测试, 不同漂移键
> ```
> **跨 4 次观测 (code-reviewer 2 + owner 2) 暴露 4 条互不相同的漂移通道** —— **没有一条是 `custom_checks`**:
>
> | # | 漂移键 | 根因 |
> |---|--------|------|
> | 1 | `remote_refs_age` | `sync.py:396/405` 读 FETCH_HEAD mtime; **scan 自己的 Phase 1.16 会改写 FETCH_HEAD** |
> | 2 | `issue_status.repos[].source` | `issue_scan.py:822` cache 命中返 `"cache"` / live 返 `"live"` (900s TTL 在两跑间翻转) |
> | 3 | `coordination_fetch.degraded` / `degradation_reason` | 真实网络抖动 ⇒ 一跑降级一跑不降级 |
> | 4 | `errors[]` 数组 | 同上 soft error 时有时无 |
>
> **根因同一**: 该「稳定性测试」**跑的是真 scan 打真网络** —— 两跑之间的网络/TTL/缓存状态本来就会变。**4 条都不在 `normalize_snapshot.py` 的 `TIMESTAMP_KEYS`/`DROP_KEYS` 名单里。**

**v2 裁定**:
- ~~本 Spec 的修法一条漂移通道都消不掉~~ (v3 修正: 能消掉 custom_checks 这一条) ⇒ **仍不声称消除该 flaky 测试** (只杀 6 之 1)。

</details>
- **该测试由母 Spec 认领消除** (母 Spec tasks **12.10**, 4 条通道全认领)。
- **本 Spec 的 AC-5 显式豁免它** (否则本 Spec 结构性无法 ship)。

> 📌 **这与 R4 给姊妹 Spec B 的「AC-1 靶点错位」是同一 species**: **一个可以「碰巧通过」而真 flaky 依旧的 AC。**
> 📌 **仓内已有逐字先例**: `DROP_KEYS` 的 `cached`/`age_seconds`/`refs_fetched` 注释 (v1.30.2) **明写**「TTL-based, varies between consecutive runs… Stability test requires drop」—— **同一 class 已解过一次, v1 又原样引入。**

---

## Impact

| 维度 | 影响 |
|------|------|
| schema | 顶层 `generated_at` (additive, 不 bump version) |
| 下游收益 | **m7-fleet-aggregation** 的 CAVEAT-age 可以从「文件 mtime 兜底」升级为「权威字段」 |
| collector 顺序 | **不改** (与母 Spec 解耦的关键) |
| 既有测试 | ⚠️ **v3**: 本 Spec 的修法可消除 custom_checks 这**一条**漂移通道 (CE 复验: 它确是通道, 条件=缓存缺失/mtime>30min), 但整体 flaky 共 **6 条**通道, **仍由母 Spec tasks 12.10 认领消除** (offline 旁路为主) |
| 采用者 | `issue-cache-freshness` 从恒红变为有意义的信号 |

---

## Verification — 可证伪锚点

- **AC-1 (红测试, 恒红)**: 构造「上次 scan 在 > 30min 前」的环境 → 当前代码下 `issue-cache-freshness` **必须 FAIL**; 修复后 **必须 PASS**。
- **AC-2 (真故障仍能捕获; v4 按 D19 改两跑断言)**: 令 `issue_scan` 失败 (fetch error / 配置错) 于第 N 次 scan → **第 N+1 次 scan** 该 check **必须 FAIL** (lag-1 语义; 单跑断言在 lag-1 基底下结构性不可证伪 — R7-qa C-1)。**(防「恒绿真空」—— 本 Spec 的对偶验收。)** fixture = 预置一份含故障态 issue_status 的上一份 snapshot + 跑一次 scan 断言 check FAIL。
- **AC-3 (`generated_at` 存在 + 容忍 cache 命中)** 🔴 **v1 初稿写反了一个代码事实** (R4 code-reviewer X-1):
  v1 断言 `generated_at <= issue_status.fetched_at` (scan 开始早于 issue fetch)。**但 `issue_scan` 有 900s 缓存** —— cache 命中时 (`issue_scan.py:766`) 它把**缓存里的** `fetched_at` (**上一次** scan 的时刻) 原样端出 ⇒ **`fetched_at` 早于 `generated_at`** ⇒ **该断言恒 false**。而 15 分钟内重复 scan **命中缓存是常态路径**。
  ⇒ **我会在一个专门修「恒红」的 Spec 里, 用一条制造「缓存路径恒红」的断言。** (对偶不变量: 假绿的反面是恒红。)
  🔴 **v2 再修正 — v1 的「正确断言」把恒红从 cache 路径搬到了 live 路径** (R5-C-D; tech-lead + code-reviewer **独立收敛**, owner 实测裁决):
  ```
  ❌ v1 的修法:  fetched_at 非空 ∧ 0 ≤ (generated_at − fetched_at) ≤ 2 × cache_ttl_seconds
                                    ^^^^  这个下界是致命的
  ```
  **代码实测**:
  - `generated_at` = `build_snapshot` **入口** (本 Spec §1; `scan.py:91`)
  - `issue_scan` 是 **Phase 1.13**, 跑在入口**之后**
  - `issue_scan.py:650` / `:711` **live 路径**: `"fetched_at": _now_iso()` ⇒ **fetch 当刻**, **必然晚于** `generated_at`

  | 路径 | Δ = `generated_at − fetched_at` | v1 的 AC-3 |
  |------|--------------------------------|-----------|
  | **cache MISS (live fetch)** | **−8s (负)** | 🔴 **FAIL — 恒红** |
  | cache HIT (600s 前) | +600s | PASS |
  | cache HIT (TTL 边缘 900s) | +900s | PASS |
  | 真陈旧 (1.13 被跳过, 3600s) | +3600s | FAIL ✅ (正确) |

  **cache-miss = 每个 session 首次 scan + 任何间隔 >900s 的 scan + 每次 CI = 常态路径。**
  ⇒ 🔴 **在一个专门修「恒红」的 Spec 里, 第二次制造恒红 —— 只是换了个路径。**

  > ⚠️ **跨 agent 裁决留痕**: qa-engineer 判此 AC **PASS**, tech-lead + code-reviewer 判 **FAIL**。**owner 实测裁决: 后两者对** —— qa 只 emulate 了 **cache-HIT** 路径, **从未测 cache-MISS/live**。**这不是反证, 是漏测。**
  > ⇒ memory `feedback_cross_agent_verdict_independent_verify` 的**新形态**: 不是「两个 agent 同时错」, 而是「**一个 agent 只测了一半的定义域就报 PASS**」。

  ✅ **v2 的正确断言 (单边)**:
  ```
  issue_status.fetched_at 非空
  ∧ (generated_at − fetched_at) ≤ 2 × issue_scan.cache_ttl_seconds     # 只要上界
  ```
  **下界毫无必要** —— `fetched_at` 比 `generated_at` **晚**是**好事**, 它恰恰说明「**1.13 在本次 scan 里真的跑了**」(负值 = live fetch = 最健康的信号)。
  (上界与 `state-checks.yaml:14-15` 已有的「2×TTL (默认 30min)」自述对齐, 且**显式允许 cache-hit**。防「恒绿真空」由 **AC-2** 承担。)

- 🆕 **AC-3b (对偶 pin —— live 与 cached 两条路径都必须 PASS)**:
  **cache-MISS (live fetch)** ⇒ AC-3 **必须 PASS** (Δ 为负);  **cache-HIT (窗口内)** ⇒ AC-3 **必须 PASS** (Δ 为正且 ≤ 2×TTL)。
  > **这是母 Spec v6 新增的「对偶验收」机械闸的实例**: **每条 AC 必须同时给出「健康常态必 PASS」+「真故障必 FAIL」两个 fixture。**
  > **AC-2「防恒绿真空」已经是这个形状 —— v1 只是没有对称地把它应用到 AC-3, 于是 AC-3 制造了新恒红。**

- **AC-4 (~~稳定性测试转确定性~~)** ⚠️ **v4 收窄** (R7 RM-12: v3 的「custom_checks.* 全子树 diff=0」会被通道 #6 [其它 check 天数型 output 跨日界] 打破): 可验收面 = 冷缓存双跑后 **`custom_checks.results[name==issue-cache-freshness]` 单条子树 diff=0** (含 status/output) — 本 check 的 output 必须确定性渲染 (不嵌墙钟时刻/随机 Δ, 任务 3.1 钉住)。flaky 整体消除仍归母 Spec tasks 12.10 (offline 旁路)。
  > v1 的两个前置条件 (「cache 陈旧」/「cache 新鲜」) **钉错了轴** —— 真正的决定因子是 **FETCH_HEAD 热度 + issue-cache 热度 + 网络抖动**。

- **AC-5 (无回归)** 🔴 **v2 修正 baseline 假前提 (R5-C-E)**:
  `python3 aria/skills/state-scanner/tests/run_tests.py` → **0 failed, 除 `test_two_consecutive_runs_diff_zero`** ∧ 无既有绿测试转红。
  > ⚠️ **baseline 不是 0 failed** —— owner 连跑两次实测: `Ran 1006 tests ... FAILED (failures=1)`。**若坚持「0 failed」, 本 Spec 结构性无法 ship。**

---

## Tasks

- [ ] 1.1 写 AC-1 红测试 (cache > 30min 前置) + 🆕 **AC-3b 对偶 pin** (live/cache-miss 与 cached/cache-hit **两条路径都必须 PASS**) —— 确认当前代码 RED。
      ⚠️ **v1 的「AC-4 双前置条件测试」已撤回** (§3: 根因归错, 前置条件钉错了轴)
- [ ] 2.1 `scan.py` `build_snapshot` 入口捕获 `generated_at` (ISO 8601 UTC), 写顶层
- [ ] 2.2 确认 `generated_at` 被 `normalize_snapshot.TIMESTAMP_KEYS` 打码 (已在清单, 需 pin 测试)
- [ ] 3.1 `.aria/state-checks.yaml` 的 `issue-cache-freshness` 断言改为同 snapshot 内 `fetched_at` vs `generated_at`
- [ ] 3.2 更新该 check 的 `description` + `fix` 文案
- [ ] 3.3 AC-2 (v4 两跑): 第 N 跑注入 issue_scan 故障 → 断言**第 N+1 跑** check FAIL (lag-1; fixture 可预置故障态上一份 snapshot 单跑等价实现); 另: 首跑无上一份 snapshot ⇒ check SKIP 可见
- [ ] 4.1 文档: `references/state-snapshot-schema.md` 加 `generated_at`; `references/issue-scanning.md` 同步
- [ ] 4.2 **关联收益**: 通知 / 记录 `aria-2.0-m7-fleet-aggregation` 的 CAVEAT-age 可升级 (其 proposal L82 的 probe 结论已过时)
- [ ] 5.1 版本 bump + SOT 同步 + CHANGELOG

---

## 关联

- **母 Spec**: `state-scanner-stale-refs-false-parity` (本 Spec 从中拆出; **零代码路径重叠** —— `issue_scan`/`custom_checks` 与 `multi_remote`/`coordination_fetch` 是完全独立的 collector)
- **下游收益**: `openspec/changes/aria-2.0-m7-fleet-aggregation` (Approved; proposal L82 的 `generated_at` 不存在 CAVEAT 由本 Spec 消除)
- **memory**: `feedback_falsifiable_evidence_for_binary_acceptance` (环境相关的 baseline 不是 baseline)
