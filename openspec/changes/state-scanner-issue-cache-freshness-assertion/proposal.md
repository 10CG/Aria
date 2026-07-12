# Proposal: `issue-cache-freshness` 检查重定义 + snapshot `generated_at` 字段

> **Status**: Draft (待 owner sign-off)
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
- 它从「1.13 跑没跑的外部反向证据」变成「1.13 **在本次 scan 内**是否产出了新鲜结果」—— 语义更准确, 且**可在健康常态下 pass、在真故障时 fail**。
- 更新该 check 的 `description` (它不再是「外部反向证据」)。

### 3. 消除既有 flaky 测试

`tests/test_normalize_snapshot.py::TestStabilityIntegration::test_two_consecutive_runs_diff_zero` **当前是环境相关的 flaky 测试**:
- cache > 30min ⇒ run1 `custom_checks` 报 `failed:1`; 该 scan 的 1.13 刷新 cache ⇒ run2 报 `failed:0` ⇒ **两次 snapshot 不一致 ⇒ 红**
- cache < 30min ⇒ 两次都 `failed:0` ⇒ **绿**

⇒ **同一份代码, 红绿取决于跑之前 30 分钟内有没有跑过 scan。** (R2/R3 双方实测各得到过红和绿。)

本 Spec 的修法**从根上消除**这个 run-to-run 依赖 (同 snapshot 内比较 ⇒ 恒定)。

---

## Impact

| 维度 | 影响 |
|------|------|
| schema | 顶层 `generated_at` (additive, 不 bump version) |
| 下游收益 | **m7-fleet-aggregation** 的 CAVEAT-age 可以从「文件 mtime 兜底」升级为「权威字段」 |
| collector 顺序 | **不改** (与母 Spec 解耦的关键) |
| 既有测试 | `test_two_consecutive_runs_diff_zero` 从 flaky 变确定性 |
| 采用者 | `issue-cache-freshness` 从恒红变为有意义的信号 |

---

## Verification — 可证伪锚点

- **AC-1 (红测试, 恒红)**: 构造「上次 scan 在 > 30min 前」的环境 → 当前代码下 `issue-cache-freshness` **必须 FAIL**; 修复后 **必须 PASS**。
- **AC-2 (真故障仍能捕获)**: 令 `issue_scan` 失败 (fetch error / 配置错) → 该 check **必须 FAIL**。**(防「恒绿真空」—— 这是本 Spec 的对偶验收。)**
- **AC-3 (`generated_at` 存在 + 容忍 cache 命中)** 🔴 **v1 初稿写反了一个代码事实** (R4 code-reviewer X-1):
  v1 断言 `generated_at <= issue_status.fetched_at` (scan 开始早于 issue fetch)。**但 `issue_scan` 有 900s 缓存** —— cache 命中时 (`issue_scan.py:766`) 它把**缓存里的** `fetched_at` (**上一次** scan 的时刻) 原样端出 ⇒ **`fetched_at` 早于 `generated_at`** ⇒ **该断言恒 false**。而 15 分钟内重复 scan **命中缓存是常态路径**。
  ⇒ **我会在一个专门修「恒红」的 Spec 里, 用一条制造「缓存路径恒红」的断言。** (对偶不变量: 假绿的反面是恒红。)
  **正确断言**:
  ```
  issue_status.fetched_at 非空
  ∧ 0 ≤ (generated_at − fetched_at) ≤ 2 × issue_scan.cache_ttl_seconds
  ```
  (与 `state-checks.yaml:14-15` 已有的「2×TTL (默认 30min)」自述对齐, 且**显式允许 cache-hit**。)
- **AC-4 (稳定性测试转确定性)**: `test_two_consecutive_runs_diff_zero` 在「cache 陈旧」与「cache 新鲜」两种前置条件下**都必须绿** (当前: 前者红后者绿)。
- **AC-5 (无回归)**: `python3 aria/skills/state-scanner/tests/run_tests.py` → 0 failed ∧ 无既有绿测试转红。

---

## Tasks

- [ ] 1.1 写 AC-1 红测试 (cache > 30min 前置) + AC-4 双前置条件测试 —— 确认当前代码 RED
- [ ] 2.1 `scan.py` `build_snapshot` 入口捕获 `generated_at` (ISO 8601 UTC), 写顶层
- [ ] 2.2 确认 `generated_at` 被 `normalize_snapshot.TIMESTAMP_KEYS` 打码 (已在清单, 需 pin 测试)
- [ ] 3.1 `.aria/state-checks.yaml` 的 `issue-cache-freshness` 断言改为同 snapshot 内 `fetched_at` vs `generated_at`
- [ ] 3.2 更新该 check 的 `description` + `fix` 文案
- [ ] 3.3 AC-2: 令 `issue_scan` 失败时该 check 仍 FAIL (防恒绿真空)
- [ ] 4.1 文档: `references/state-snapshot-schema.md` 加 `generated_at`; `references/issue-scanning.md` 同步
- [ ] 4.2 **关联收益**: 通知 / 记录 `aria-2.0-m7-fleet-aggregation` 的 CAVEAT-age 可升级 (其 proposal L82 的 probe 结论已过时)
- [ ] 5.1 版本 bump + SOT 同步 + CHANGELOG

---

## 关联

- **母 Spec**: `state-scanner-stale-refs-false-parity` (本 Spec 从中拆出; **零代码路径重叠** —— `issue_scan`/`custom_checks` 与 `multi_remote`/`coordination_fetch` 是完全独立的 collector)
- **下游收益**: `openspec/changes/aria-2.0-m7-fleet-aggregation` (Approved; proposal L82 的 `generated_at` 不存在 CAVEAT 由本 Spec 消除)
- **memory**: `feedback_falsifiable_evidence_for_binary_acceptance` (环境相关的 baseline 不是 baseline)
