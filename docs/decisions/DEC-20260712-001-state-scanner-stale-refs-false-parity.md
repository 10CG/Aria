# DEC-20260712-001 — state-scanner 陈旧 ref 假同步 (parity false-green)

> **状态**: **✅ Approved — owner 终审通过 2026-07-15 (D15′-D20 五条代裁全部签字生效)**。v10 (2026-07-14) — v10 新增 **D20** (§3e: 8C-1 三档全分割, E 优先)。v9 新增 **D15′/D18/D19** (§3d: R7 三 C 合并解 + RC-8 + Spec C 基底; D15 由 D15′ 取代)。v8 新增 **D15/D16/D17** (§3c: R6 的 3 条 owner 待裁, 代裁 [owner /goal 授权] 待 R7 复核 + owner 终审)。前史: post_spec **R1→R6 全 FAIL** (6 轮; R5 5-agent + R6 3-agent)。**D10 (F10′) 已被 R6 证伪并由 D14 取代**。post_spec **R1→R5 全 FAIL** (收敛单调, 5 轮 × 5 agent)。v1 药方被推翻 (R1); 公式两端皆错 (R3); fail-open 枚举 (R4); **公式的上游数据不存在 (R5)**。owner 裁定**扩本 Spec 加 F10′**。v1 决策 D1/D2/D3 已作废 (见 §3); **v6 新增 D7-D13 (见 §3b)**。
> **创建**: 2026-07-12 | **v2 修订**: 2026-07-12 (折入 R1 的 3C + 12M/m) | **v6 修订**: 2026-07-12 (折入 R2-R5; **R5 的 5 Critical + F10′ 裁定**)
> **审计轨迹**: [R1+R2](../../.aria/audit-reports/post_spec-R1-R2-2026-07-12T1850Z-state-scanner-stale-refs-false-parity-aggregated.md) → [R3+R4](../../.aria/audit-reports/post_spec-R3-R4-2026-07-12T2000Z-state-scanner-stale-refs-false-parity-aggregated.md) → [**R5**](../../.aria/audit-reports/post_spec-R5-2026-07-12T2230Z-state-scanner-stale-refs-false-parity-aggregated.md)
> **触发**: 本 session 亲历 — `/state-scanner` 开局报 `parity=equal / overall_parity=true`, 实际本地落后 `origin/master` **4 个 commit** (双子星并发 session 已 ship v1.56.0 + v1.56.1)。
> **决策人**: 10CG Lab owner (v1: 范围/阈值; v2: 重设计方向 F3′)
> **前置 grounding**: probe-first 代码探查 (v1) + **post_spec R1 三方独立实证** (v2, 含真 git fixture 跑真 collector)
> **Spec Level**: 3 (Full)
> **关联**: aria-plugin #109 (协调层维度, 经 R1 核实真 disjoint)
> **Track**: `state-scanner-stale-refs-false-parity`

---

## 1. Context — 缺陷 (诊断层, R1 三方实测确认成立)

`state-scanner` 是十步循环的**统一入口**。它的 `sync_status` 会在本地 remote-tracking ref 陈旧时报 `parity: equal` / `overall_parity: true`, 而工作树实际落后远程 → **AI 基于落后工作树开工 → 重复劳动** (memory `feedback_concurrent_duplicate_audit_fetch_before_start` 的**工具层成因**)。

**本 session 活体证据** + **R1 实测复现** (qa-engineer 在未修改代码 `fc7c372` 上造 fixture 跑真 collector):

```
fixture: local refs/remotes/{origin,github}/master=367e66e, 真实远程=12f730a (前进 4 commit), FETCH_HEAD age=14h
=== UNMODIFIED code, warn_after_hours=24 ===
overall_parity   : True        ← 假绿
local_refs_stale : <absent>    ← 14h < 24h, 没置位
  remote=origin  parity=equal  behind=0
  remote=github  parity=equal  behind=0
```

**核心洞察 (R1 确认成立)**: 这是 **QA-C1 不变量的孪生缺口**。`_aggregate_flags` docstring 记载 QA-C1 修的是「**零证据**不得当正证据」(all-unknown 短路成 true)。本缺陷是「**陈旧证据**不得当新鲜证据」。R1 进一步发现**第三次**违反: 「**从未获取过的证据**」(submodule FETCH_HEAD 不存在 → `age is None` → 判为不陈旧) 也在当正证据。

---

## 2. v1 药方为何失败 (post_spec R1, 3 Critical, 全部有实证)

### C1 — 新鲜度信号没有 per-remote 分辨率, 且 F3 会把它清零

`_fetch_head_age_hours()` (`multi_remote.py:130-142`) 读 `<gitdir>/FETCH_HEAD` 的 **mtime** —— **每仓一个文件**, 任何 remote 的任何 fetch 都整体覆写它。代码中**不存在任何 per-remote 新鲜度数据**。

`coordination_fetch` 只 fetch 单个 remote (origin)。v1 的 F3 把它前移 → FETCH_HEAD mtime ≈ now → age ≈ 0 → **`local_refs_stale` 对包括 github 在内的所有 remote 结构性恒 False** → **F1 变死代码, F2 变 no-op**。

backend-architect 实测 (真 fetch + 真 collector):
```
BEFORE fetch: FETCH_HEAD age = 14.00 h
>>> git fetch origin --no-tags +refs/heads/*:refs/remotes/origin/*    ← coordination_fetch Fetch 1 原文
AFTER  fetch: FETCH_HEAD age = 0.0000 h
   refs/remotes/origin/master   68284bf   ← 刷新
   refs/remotes/github/master   326074e   ← 依然陈旧

阈值扫描 (github ref 人为 aged 30 天):
  warn_after_hours=24     local_refs_stale=False  github.parity=equal  ==> overall_parity=True
  warn_after_hours=1      local_refs_stale=False  github.parity=equal  ==> overall_parity=True
  warn_after_hours=0.001  local_refs_stale=False  github.parity=equal  ==> overall_parity=True   ← 3.6 秒阈值都救不回来
```

⇒ v1 的 DEC D3 推理「F3 落地后 origin 恒新鲜, 故 1h 阈值只对非-origin 触发」**是事实错误**: age 是 repo 级单值, age≈0 意味着**对所有 remote 都不触发**。**F1 与 F3 互相拆台。**

### C2 — 子模块零新鲜度覆盖 (而事故第二条硬证据正是子模块)

- `_scan_repo()` 恒返回 `stale=False` (L364-365, 死返回值, 两个调用点都丢弃)。
- 陈旧度只对 `project_root` 算一次 (L495-498)。
- `_fetch_head_age_hours` 在 FETCH_HEAD 不存在时返回 `None`; L497 的 `if age is not None and age > warn` ⇒ **`None` 判定为「不陈旧」**。实测三个子模块 `.git/modules/*/FETCH_HEAD` **全部不存在** —— **「从未 fetch」(最陈旧) 被当成最新鲜**。
- `coordination_fetch` 只在 project_root 跑 ⇒ F3 对子模块**零效果**。
- 而 `_aggregate_flags` 主仓+子模块**混合聚合** ⇒ 这些从未刷新的 ref 照样提供 `equal` 正证据。

**HEAD 上的活体现状** (qa-engineer 真跑本仓):
```
overall_parity: True | local_refs_stale: <absent>
main:                  [(github, equal),   (origin, equal)]
 sub aria:             [(github, unknown), (origin, unknown)]   ← 两个 remote 全 unknown
 sub aria-orchestrator:[(github, unknown), (origin, equal)]
```
`aria` 子模块两个 remote **全 unknown**, 仍被主仓的 equal 证据吞掉 → `overall_parity: True`。

⇒ Spec 引的第二条硬证据 (aria-orchestrator github 镜像落后 32 commit) **恰恰是子模块**, 在 v1 设计下**原封不动**。

### C3 — v1 的 F1 字面语义会制造**新的**假绿, 并杀死 push 提醒

v1 写「陈旧时把该 remote 的 `parity` 降级为 `unknown`」—— **无限定**。但 `unknown` **不阻断** `overall_parity`。backend-architect 实测:

```
origin 新鲜+equal; github 陈旧且读作 behind (真落后)
  TODAY              : overall_parity=False        ← 现状反而是对的
  AFTER F1 (v1 字面) : overall_parity=True         ← 假绿翻转: 修 bug 的部件造出新 bug

单 remote 陈旧且读作 ahead (有未推送工作)
  TODAY              : has_pending_push=True
  AFTER F1 (v1 字面) : has_pending_push=False      ← session-closer 未推送告警死掉
```

`multi_remote.py:270-277` 的 **QA-I1 注释明写警告过这个失败模式** ("Marking reachable=False would suppress push reminders incorrectly"), v1 正在重蹈。

⇒ 降级**只能针对 `equal`** (正证据)。`behind`/`diverged`/`ahead` 是**下界**, 陈旧 ref 报出来的依然是真信号, **不得动**。

### C4 (qa) — AC-3 把唯一正解排除在解空间外

本地既然不存在 per-remote 新鲜度信号, 正确修复**必然**对每个非-origin remote 增加网络调用。而 v1 的 AC-3 断言「单次 scan 的 `git fetch` 调用次数**不增加**」—— **AC-3 与 primary_goal 二者只能活一个**。

---

## 3. v2 锁定决策 (owner 2026-07-12, 折入 R1)

> **v1 的 D1/D2/D3 作废**。核心教训: **新鲜度不能「测量」, 只能「获取」。**

R1 逐一实测排除了所有本地新鲜度候选信号:

| 候选 | 实测结论 |
|------|----------|
| `FETCH_HEAD` mtime | repo 全局单值, 任一 remote 的 fetch 都重置 |
| `.git/refs/remotes/<r>/<b>` 文件 mtime | **只在 ref 值变化时更新** → 「刚 fetch 但没变」与「3 天没 fetch」不可区分 |
| 同上, packed 之后 | `git pack-refs` (gc 自动跑) 后 loose 文件**直接消失** → 信号归零 |

⇒ per-remote 新鲜度**只能**由 Aria **亲自获取**并记录。

### 承重实测 (spike-first, 本 session 实机)

```
串行全量 fetch (8 个 repo×remote 对)  = 42.7s     ← 不可接受
并行全量 fetch (8 个对)               =  7.6s     ← 等于最慢单腿 (origin 走 CF Access ~7s)
当前 scan 已经在付的                  ≈  7.0s     ← 它本来就 fetch 了 origin 一次
当前 scan 全程                        = 16.9s
──────────────────────────────────────────────
边际成本                              ≈ +0.6s  (17s → 17.6s, +4%)

单次 ls-remote 耗时 ≈ 单次 fetch 耗时 (均被 SSH 握手主导, 非传输量)
```

⇒ **fetch 严格优于 ls-remote**: 同价, 但 fetch **顺便真的刷新了 ref** (这本就是你要的)。**OQ-2 (ls_remote) 因此被删除, 不是「倾向不做」而是「无存在理由」。**

| ID | 决策 | 内容 |
|----|------|------|
| **D1 (F3′)** | **新鲜度靠获取** | `coordination_fetch` 泛化为 **fetch 所有 enforced remote**, 覆盖**主仓 + 全部子模块**; **跨 repo 并行、同 repo 内串行** (避免同仓两 remote 并发写 `.git/FETCH_HEAD` 竞态)。snapshot 记录 per-remote `{fetched_at, fetch_ok, error}`。 |
| **D2 (F1′)** | **裁决挂在获取结果上** | parity 的可信度由「**本次 scan 是否成功刷新了该 remote**」决定, **不再**由 FETCH_HEAD mtime 决定。未成功刷新 ⇒ 该 remote **仅把 `equal` 降级**为 `unknown` + `reason: "not_refreshed"`; **`behind`/`ahead`/`diverged` 原样保留** (下界仍为真信号, 修 C3)。 |
| **D3 (F2′)** | **退役 mtime 启发式** | `local_refs_stale` / `warn_after_hours` 的 FETCH_HEAD-mtime 路径**整体退役** (而非 24→1)。理由: 新鲜度已构造性可知; 且该信号是 repo 全局, **当 fallback 都不合格**。⚠️ 这**推翻了 owner v1 的「24→1」决策** —— 其前提 (F3 后 origin 恒新鲜 ⇒ 1h 只对非-origin 触发) 已被 C1 证伪。**交 R2 挑战。** |
| **D4 (C2 修)** | **子模块全覆盖** | fetch + parity + 裁决覆盖子模块; `age is None` / 从未 fetch ⇒ **视作新鲜度未知** (fail-toward-warn), **不得**视作新鲜。 |
| **D5 (OQ-1)** | **裁 (a)** | `overall_parity: true` 要求**每个** enforced remote 都确认 `equal`。R1 grep 实证: **phase-c-integrator 不消费 `overall_parity` (全 skill 树 0 命中)**, 唯一消费者是**非阻塞**的 `multi_remote_drift` 推荐规则 (75% 置信) ⇒ (a) 的成本被 v1 高估。**但 (a) 不是解药** —— 陈旧 ref 算出的 `equal` 在 (a) 下依然是 `equal`; 解药是 D1/D2。 |
| **D6 (F4′)** | **重定义断言, 而非挪位置** | `issue-cache-freshness` 若只是把 `custom_checks` 挪到 `issue_scan` 之后 → cache 刚写完 → **恒绿真空** (从假红变假绿, 同一枚硬币反面)。断言必须改为**断言本次 snapshot 的 `issue_status.fetched_at`**, 而非 cache 文件 mtime。 |

---

## 4. R1 揭出的连带修复 (v1 完全没看到)

| ID | 内容 |
|----|------|
| **R-1** | **F3′ 落点必须在 `collect_git_state` 之前** (Phase 0.5)。`collectors/git.py:147` 的 `_collect_upstream` 也用 `refs/remotes/origin/*` 算 ahead/behind 且跑在 1.12 之前 ⇒ 若 F3′ 落在 1.11.5, `git.upstream.behind`(陈旧) 与 `sync_status.current_branch.behind`(新鲜) **在同一 snapshot 里打架** —— 制造新的自相矛盾, 而 AC-6 抓不到。 |
| **R-2** | **Impact 表遗漏 `git` block 行为变更**: ahead/behind 由陈旧变新鲜 ⇒ 影响 `branch_behind_upstream` 规则 (阈值 `behind >= 5`) + golden fixture。 |
| **R-3** | **`handoff_autofill.py:52` 显式把 `parity == "unknown"` 排除出 warnings** ⇒ F1′ 产出的 `unknown` 会被 session-closer **静默吞掉** → handoff 既不说「已同步」也不说「不知道」= **新假绿通道**。必须让 `reason ∈ {not_refreshed}` 升级为 warning。 |
| **R-4** | **`RECOMMENDATION_RULES` 的 `multi_remote_drift` 给的是 push 建议**, 但陈旧 ref 导致的 false 意味着用户需要 **fetch/pull**, 不是 push ⇒ 建议内容本身会误导。 |
| **R-5** | **`git-remote-helper` 姊妹实现: QA-C1 那个「已修复」的缺陷在它里面还活着**。`check_parity.sh:383` 的 `jq 'all(...)'` 对空数组/全 unknown 返回 `true` = pre-QA-C1 假绿; `local_refs_stale` 硬编码 86400s 不读 config。而 `multi_remote.py` docstring L4-7 声称它是 "canonical schema SOT" ⇒ **被声明为 SOT 的文档/实现早已 drift**。必须同步或显式迁移 SOT。 |
| **R-6** | **F2 的 SOT 清扫 v1 只覆盖 2/6 处**, 遗漏: `config-loader/DEFAULTS.json:38` (**默认值 SOT**) / `.aria/config.template.json:21` (**采用者 copy 的模板** ⇒ 不改则新采用者仍拿旧值) / `sync-detection.md` ×4 / `git-remote-helper/schema.md:58`。 |
| **R-7** | **baseline 不是全绿**: `tests/test_normalize_snapshot.py::TestStabilityIntegration::test_two_consecutive_runs_diff_zero` 在 `fc7c372` **现在就是红的**, 且红因**正是 F4** (run1 的 1.11 看到 >30min cache → failed:1; 该 scan 的 1.13 刷新 cache; run2 → failed:0 ⇒ 两次 snapshot 不一致)。⇒ **F4 的红测试已经存在**; AC-5「现有测试全绿」前提为假。该测试还**环境相关** (30min 内跑过 scan 就转绿) —— 正是 `feedback_falsifiable_evidence_for_binary_acceptance` 说的 AI 可代填 true 的场景。 |
| **R-8** | **现有测试的 mock 是共犯**: `test_multi_remote_mocked.py` 的 `_make_run` 伪造 `refs/remotes/origin/master` 的值和 rev-list 计数 = 把 tracking ref **钉死为 ground truth**, 而陈旧性恰恰是「ref 不是 ground truth」⇒ 该文件**结构上不可能**抓到本缺陷 (memory `feedback_test_mock_pattern_hides_prod_bug` 精确命中)。**更尖锐**: `test_local_refs_stale_flag` (L685) **已经构造了事故 fixture**, 却只断言 `local_refs_stale is True`, **从未断言 `overall_parity`** —— 跑出来是 `local_refs_stale=True` 而 `overall_parity=True`, **自相矛盾早就在屏幕上**。最便宜的红测试 = 往这个既有测试加 2 行断言。 |
| **R-9** | **golden fixture 把假绿腌进去了**: `tests/fixtures/reference-snapshot-aria.json` 记录 `overall_parity: true` + 全部子模块 remote `equal` (采自本仓 = 事故现场), 且**无自动测试消费** (只被人工 diff 参考) ⇒ 会继续充当「正确输出」参照。必须重新生成。 |
| **R-10** | **`_load_config` 只读 `state_scanner.multi_remote`**, 而 `enforced_remotes` 概念住在顶层 `multi_remote.*` (phase-c-integrator 命名空间) —— 本仓 config.json 里**两个 block 都不存在**。D5/D1 的「enforced remote」需要未列入 v1 范围的 config 打通。 |
| **R-11** | 死代码/文档 drift 顺手清: `_scan_repo` 的 `stale` 返回值 (恒 False + 两处丢弃); `reason` enum 已 drift (代码还发 `rev_list_failed` / `rev_list_parse_failed`, schema 未记); `sync.py` **从不读** `sync_check` config (而 `phase-1-collectors.md:21` 声称可用 `sync_check.enabled=false` 关闭); `remote_refs_age` 在 F3′ 后恒为 "1m" ⇒ 字段实质死亡。 |

---

## 5. AC 重写要求 (可证伪性, R1 M5/m1/m2/m3/m6)

| AC | v1 问题 | v2 要求 |
|----|---------|---------|
| AC-1 | **可被 F3 单独满足** (fetch 后 ref 变新鲜 → behind → 断言过, 全程不经 F1) ⇒ F1 可作为死代码 ship 而 AC-1 全绿 | 必须**显式断言走过 F1′ 代码路径** (`reason == "not_refreshed"`), 或钉死被测单元为 collector 级 (无 fetch) |
| AC-2 | **在 v1 设计下不可构造** (单个 repo-global FETCH_HEAD 无法表达「origin 新鲜 + github 陈旧」) | 在 D1/D2 下可构造 (per-remote fetch 结果) —— 必须真跑通 |
| AC-3 | **禁止了唯一正解** | 改为**预算断言**: 并行 fetch-all wall-clock ≤ 单次最慢 remote fetch × 2 (实测基线: 7.6s vs 7.0s); 且 scan 总耗时增幅 ≤ 10% |
| AC-5 | 「现有测试全绿」**前提为假** | 写明真实 baseline: `fc7c372` = **1 failed / 1021 passed**, 红的是 `test_normalize_snapshot::test_two_consecutive_runs_diff_zero` (F4 所致) |
| AC-6 | prose 谓词, AI 可代填 true | 机械化: 当 `tracks_multibranch` 出现 HEAD 不可达的 commit 时, 断言 `overall_parity == false` 或该 remote `reason` 非空 |
| — | tasks 2.4 只防一半 | 补: 「fix 后红测试**仍无法转绿** ⇒ 设计缺陷, 回 Phase A」(C1 就是这种情况: v1 的 AC-2 永远转不绿) |

---

## 6. Dogfood — 本 track 在 Phase A.1 提前认领

按 aria-plugin **#109** 主张 (claim 触点应前移到「决定要做某事的那一刻」, 因为最烧钱的是 issue-pick → Phase A 窗口), 本 track 在起草前即 advisory 认领:

```
phase1_gate.py --raw-track-id state-scanner-stale-refs-false-parity --phase A.1 --mode advisory
→ {"outcome":"passed","proceed":true,"push_success":true,"competing_winner":null}
```

`--phase` 是自由字段, 无需改代码即可前移认领。**本 session 的 R1 回炉恰好印证了 #109 的成本论证**: Phase A (含 5-agent 审计) 是最贵的窗口, 若两个 session 并发做同一 Spec, 浪费的正是这一段。

> ✅ **(v6 结案 —— 该警示已交叉核对完毕, 结论: 「#109 首次活体验证」这个说法是错的, 已删除该断言。)**
> **实测**: `coordination-gate-invocation` 探针分区显示 **2 条生产 run_gate 记录**, 且 2026-07-09 的 handoff 记有更早的真实生产调用 (`carry-followup-99`)。⇒ **本 track 不是首次活体验证**, 该机制在本 track 之前就已被真实调用过。
> ⇒ memory `feedback_spec_precedent_verify_execution_history` 的又一次实证: **写下「首次 / 从未」这类时间断言前, 必须先查执行史。**

---

## 3b. v6 新增决策 (owner 2026-07-12, 折入 R2-R5)

| ID | 决策 | 依据 |
|----|------|------|
| **D7** | **`ahead` 不算正证据** —— `overall_parity` 语义 = 「本地与远端一致」。修的是「**落后时假绿**」(危险: 会在旧代码上开工重复劳动), **不是「领先时假红」** (领先不导致重复劳动)。 | R4-C7 (tech-lead ↔ code-reviewer 正面冲突, owner 采纳 code-reviewer)。与现有代码 `has_equal_evidence` / golden fixture / AB rubric **三者一致 ⇒ blast radius 最小**。tech-lead 反方论据存档, 若 Phase B dogfood 实测告警疲劳可重开 |
| **D8** | **拆 3 个 Spec** (主 / Spec B Rule #7 / Spec C issue-cache) | 5/5 agent 一致建议。落地顺序: **Spec C (独立) → Spec B (Rule #7, 须先于主 Spec) → 主 Spec** |
| **D9** | **一切「不变量」必须写成 fail-CLOSED 兜底 (补集定义), 不得写成正向枚举** | 同一不变量在本 Spec 起草期**复发 7 次** (QA-C1 零证据 / 陈旧证据 / 从未获取 / v3 只豁免 ahead / v4 枚举 fail-open / **R5: `has_unreachable_remote` 正向枚举** / **R5: `可信` 的 null**)。⇒ **谓词定义域横扫表 (proposal §横扫) + tasks 5.1d 机械闸** |
| ~~**D10**~~ 🔴 **SUPERSEDED by D14** | ~~扩本 Spec 加 F10′~~ (detached-HEAD 仓库改用 commit-based parity), **不拆 Spec D** | **R5-C-A**: `multi_remote.py:169` 在 `branch is None` 时**在触碰任何 remote-tracking ref 之前就返回** ⇒ 子模块 (detached HEAD 是其规范常态) 的**非-origin 远端 drift 结构性不可见** ⇒ **本 Spec 要杀的 bug 在 v5 公式下原样存活**。**今日活体复现**: `standards`/`aria-orchestrator` 的 github 镜像各落后 2 commit + gitlink 从 GitHub 不可达, 而 `/state-scanner` 报 `overall_parity: true`。**不补这一块, 本 Spec 声称修好的那个 bug 在它自己 §Why 引的场景下原样存活。** 修法**不是发明新机制** —— `sync.py:200-330` 已有验证可工作的 commit-based 算法 (只是硬编码只查 origin), 参数化搬过来即可 |
| **D11** | **deadline 砍掉的 leg ⇒ `fetch_ok="not_attempted"` (三态), 裁决权交回 `可信(r)`; 并按 `fetched_at` 升序排队防饥饿。🔴 __不__ 归 benign 桶, 也 __不__ 无条件标 `not_refreshed`** | **R5-C-C** + **owner 自查推翻 v6 初稿**。v5 无条件标 `not_refreshed` (∈blocking) ⇒ 大仓恒红; 但 backend-architect 建议的「归 benign ①」**会制造假绿** —— benign 判据是「fetch **不能**改变它」, 而「我们没去问」fetch **完全能**改变 ⇒ 大仓 origin 快腿提供 ∃ 证据 + github 被砍判 benign ⇒ `overall_parity: true`, 而 github 可能真领先 100 commit ⇒ **本 Spec 要杀的 bug 经由新机制复活 (第八次复发)**。**正解 (code-reviewer M-2)**: 两端都不做 —— 只把 `fetched_at` 留在原地, 让 `可信(r)` 说话 (窗内 ⇒ 证据仍有效; 窗外 ⇒ 诚实 blocking)。**恒红的真正根因是饥饿, 不是分桶** ⇒ 优先级排队解决。*(v10 读法注: 本条的 可信(r) 按 D15′/D20 读作三档全分割 — 历史决策原文留痕)* |
| **D12** | **Spec B 词表 = (b) 保留 `coordination_fetch` 旧词表**, 不发明第三套; `issue_scan` 的第二个分类器**有意不合并** | **R5-M-4** (三方独立收敛): v1 只披露矛盾、无任务承载裁定。母 Spec 的 fail-CLOSED 兜底使**正确性不依赖词表长相**; 但词表必须单一 |
| **D13** | **三份 Spec 的「0 failed」判据豁免 `test_two_consecutive_runs_diff_zero`**, 由**母 Spec 认领消除** (4 条漂移通道) | **R5-C-E**: owner 连跑两次实测 —— baseline **本来就是 1 红** (`Ran 1006 tests, failures=1`)。**Spec B 被指定「应先落地」, 却按自己的 AC-3 结构性无法 ship** |

| 🔴 **D14** | **F10′ → F10″ 换原语: orphaned-gitlink 可达性** (取代 D10) | **R6 三方独立证伪 F10′**: 「镜像落后」在 git 眼里是 **`ahead`** 不是 `behind` (`rev-list --left-right 79b7cd6...9df1722` → `2 0`; `multi_remote.py:205` 映射 `ahead=parts[0]`) ⇒ 而 `ahead` 的非阻断性被 **AC-8/D7 + golden fixture (`main github->ahead ⇒ overall_parity: true`) + AB rubric (`:143` "Should exclude parity: ahead")** 三重锁死 ⇒ **F10′ 上线后事故场景仍是 `true`, AC-16 与 AC-8 字面互斥**。<br>**根因**: `parity` 天生无法区分「我有未推的 commit」(开发常态) 与「**已发布的 gitlink** 在 remote 上不可达」(完整性破损)。**今天断掉的不变量是跨仓可达性, 不是 parity。**<br>**F10″**: `gitlink_orphaned(R) := 主仓在 R 上【已发布】commit 引用的 gitlink G, 在子模块的 R 上不可达` (判定: `git -C S branch -r --contains G --list "R/*"` 为空)。<br>**实测已验** (真仓真命令): 事故态**正确报警** / 开发期**零误报** (只看已发布的, 不看本地 HEAD) / **零分支名假设**。<br>**一次性免疫 R6 全部 3 Critical + M-4**: 不碰 parity ⇒ 与 AC-8 零冲突, **D7 不必重开**; 不猜分支名 ⇒ 免疫 C-2 (实测三个子模块的 `refs/remotes/github/HEAD` **全不存在**); shallow 守卫语义清晰; **pin 住旧 commit 的子模块天然免疫** (只要可达就不报警, 与"新不新"无关) |

> 🔴 **D7 的盲区 (R6 揭出, 但 D14 使其不必重开)**: D7 的理据「本 Spec 修的是**落后时假绿**, 不是**领先时假红** (领先不会导致重复劳动)」—— **这句话对 mirror remote 是错的**。领先 github 恰恰就是危害本身 (镜像陈旧 / `clone --recursive` 断裂 / 市场版本滞后)。**今天的事故 + CLAUDE.md 记的 2026-04-10 事故, 都是「领先」形态。**
> **但 D14 换原语后, D7 不必重开** —— F10″ 用可达性而非 parity 表达该不变量, 两者正交。
> **元教训**: v6 修 R5-m-1 时, owner 让**理据**去迁就**公式** (`ahead ⇒ true`)。而 v5 原本的理据 (「有未推送 commit 确实不是已同步的」) 对 mirror 才是对的。⇒ **当理据与公式矛盾时, 不要默认公式是对的; 先问「这个矛盾在保护什么」。**

### §3e v9 裁决 (2026-07-14, R8 8C-1 — **代裁**: owner「按你的建议裁决」授权; R9 复核)

| ID | 裁决 | 理由 |
|----|------|------|
| 🔍 **D20** | **8C-1 (equal 三档守卫重叠格) 裁 E 优先 — 三档改全分割**: `E ⇒ 供 ∃ 作证` / `¬E ∧ X ⇒ stale_unverified` / `¬E ∧ ¬X ⇒ not_refreshed (blocking)` (E=证据资格, X=豁免资格) — 守卫两两互斥、并集全覆盖, 无重叠格。**附带三条款** (两审计共同要求): (1) D18 计数器**清零在豁免判定之前** (本 scan fetch 成功 ⇒ 先清零再评 X — 消灭「恢复 scan 落 E∧¬X」路径); (2) AC-15(a)/(b) 措辞同步 (b 的 blocking 前提 = ¬E∧¬X); (3) 5.1d 闸加**守卫全分割断言**维度 (N 档谓词组: 两两互斥 + 并集=全域, 机械可判)。**DEC 公式一律指针引用 proposal F4′ (8M-2)**, 本条不复制公式细节。 | **E 无法被 artifact 伪造**是裁决基石: 写入侧三条 fail-CLOSED (tasks 3.7/3.16 — fetched_at/generation_fetched 只在真成功时推进) ⇒ `fetched_at ≈ now` ⟹ 1h 内必有一次真实成功 fetch ⟹ 证据世界时间新鲜。反方 (¬X 优先偏红) 担心的钳位/lost-update 场景**恰好只能把 fetched_at 覆盖成更旧** (E→false, 方向安全), 造不出假 E=true; D18 恢复路径由清零先序条款消灭; 退避腿 56min 场景 (E 真成立) 按 D15′「作证要世界时间新鲜」立意应作证 — 数据 56min 新鲜却因代际簿记 blocking 是自相矛盾。E ⇒ 墙钟 ≤1h ≤7d ⟹ hard_cap 臂对 E 腿自然蕴含, 无冲突 |

### §3d v8 裁决第二批 (2026-07-14, R7 三 C 的合并解 — **代裁**: owner /goal「按你的建议裁决并完成 v8→R8」授权; R8 重点复核)

| ID | 裁决 | 理由 |
|----|------|------|
| 🔍 **D15′** | **取代 D15: `可信(r)` 拆双角色谓词** — `证据资格` (∃ 侧) + `豁免资格` (降级侧), equal 按三档全分割处置 (v10 D20)。**公式/conjunct/k_eff 细节一律以 proposal F4′ v9+ 公式块为 SOT, 本条不复制** (8M-2 指针化; v9 前本条曾内联公式并漂移 — R9-M3 修正)。 | R7 backend C-1/C-2/C-3 的合并解: 作证要世界时间新鲜, 豁免要注意力节律新鲜, 量纲不同必须分键。与 AC-15(b)「origin 不能替 github 作证」同构 |
| **D18** | **RC-8: `orphan_unverified` / `stale_unverified` 持续 ≥ k_eff 代 ⇒ 升级 blocking** (per-leg cache 记录连续 unverified 代数); 且两状态必须渲染进输出区块 (进 AC, 不许只活在 reason 枚举) | 「没去问 ⇒ 放行」与第八次复发同构 (R7 狩猎 M-1); advisory 可见通道有被吞史 ⇒ 单靠可见不够, 需时限升级 — 与「过期即诚实」同一逻辑。k_eff 代 = 防饥饿保证内必然轮到, 正常运行永不触发; 触发即真异常 (fetch 连败/退避死锁) |
| **D19** | **Spec C 求值基底 = (a) lag-1** (check 读上一份 snapshot, 不挪 collector 位置); AC-2 改**两跑断言** (「故障后的下一次 scan 该 check FAIL」) + lag-1 语义公示 | R7 qa C-1 二选一: (b) 挪位/内存接线破坏 Spec C 与母 Spec 的解耦叙事 (拆分理由), 且 §1 已论证挪位后检查变同义反复; lag-1 对「外部反向证据」型检查是诚实语义 (审计的是上一次 scan 的产物), 滞后一拍换独立性, 值 |

### §3c v8 裁决 (2026-07-14, R6 的 3 条 owner 待裁 — **代裁**: owner /goal「1+2 都做」授权, spec approval 时 owner 终审; R7 重点复核)

| ID | 裁决 | 理由 |
|----|------|------|
| 🔍 **D15** | **M-1 大仓恒红 → `可信(r)` 的窗从「wall-clock 300s」改为「scan 代际 + wall-clock 硬上限」双条件**: `可信(r) := fetched_at ≠ null ∧ generation_age(r) ≤ k (默认 3 次 scan) ∧ (now − fetched_at) ≤ hard_cap (默认 7d)` | 三个原选项皆有硬伤: (a) 窗随 leg 数自适应 — staleness 容忍度与仓库大小无原理关联; (b) 放弃 deadline — 60 腿仓 scan 墙钟无上界; (c) 裸接受 — 恒红照旧。**根因**: wall-clock 窗预设了 daemon 式连续运行, 而 scanner 是**事件驱动**的 — 它只在 scan 时刻获得新知, 「新鲜度」的自然单位是 **scan 代际**而非秒。防饥饿队列 (D11) 保证 ≤⌈legs/预算⌉ 代内全腿必刷 ⇒ 稳态下全腿代际 ≤3 ⇒ 不恒红; hard_cap 7d 防「两次 scan 相隔数月 ⇒ 代际新鲜但墙钟古老」的陈旧证据假绿回流 (违反形态 #2 的回流口)。**实现**: cache 持久化 scan generation 计数器 + per-leg `generation_fetched`。⚠️ **本条改 `可信(r)` 核心定义 — R7 必须重点对抗审查** (第十次复发候选位) |
| **D16** | **M-5 谓词横扫表 → 搬 aria-plugin** (`skills/state-scanner/references/predicate-domain-table.md`) **+ 机械 lock 测试** (unit test 断言 multi_remote/sync 引入的每个布尔谓词在表中登记); 主仓 proposal 保留副本仅作审计快照, 表头注明 SOT=插件侧 | 二选一里「review checklist」被否: 本轨 9 次复发史证明纪律性检查不守恒, 机制才守恒 (D9 同理)。表在主仓则插件 unit test 结构性读不到 (R6-M-5 的原始发现) ⇒ 唯一能机械化的位置是插件内 |
| **D17** | **OQ-F 转正: `verify_mode: ls_remote` 退役** (删除 scanner 内 ls-remote 平行校验路径, 单一计算路径 = F3′ fetch + local_refs) ; ship 前强验需求由 **C.2.5 gate 的独立一次性 ls-remote 校验脚本**承载 (在 phase-c-integrator, 不在 scanner) | 平行计算点是本 Spec 病灶家族 (F9′ sync.py 平行点同因); scanner 内双路径 = 语义漂移温床。「ship 前要直接问远端」是真需求, 但属 gate 场景 (一次性、可慢、可失败即阻断), 与 scanner 的常态扫描 (预算内、fail-soft) 是两种契约, 分开各自最优 |

> ⚠️ **v1 的两条决策已被实证推翻, 此处留痕**: 「F1+F2+F3+F4 全包」与「`warn_after_hours` 24→1」—— **前提不成立** (R1: age 是 repo 级, `age≈0` 对**所有** remote 都不触发; 阈值降到 **3.6 秒**都救不回 github)。

---

## 7. 元教训 (值得进 memory)

1. **新鲜度不能测量, 只能获取。** 想用文件 mtime 之类的本地痕迹推断「数据有多新」, 在 git 里全部行不通 (FETCH_HEAD 全局 / ref mtime 仅值变时更新 / packed 后消失)。要知道远端状态, 只能去问远端。
2. **「修 bug 的部件」自己会造 bug。** C3: 把 parity 一律降级为 unknown, 反而让 `behind` 停止阻断 → 假绿翻转 + push 提醒死亡。降级必须**只作用于正证据**, 不能碰负证据 —— 负证据即使来自陈旧数据也是**下界**, 依然为真。
3. **同一份 snapshot 内部自相矛盾, 是 collector 编排缺陷的可靠指纹。** (sync 说已同步 / tracks 说对方已 ship)
4. **测试的 mock 姿势可以让缺陷结构上不可见。** 把 tracking ref 钉成 ground truth 的 mock, 永远测不出「ref 不是 ground truth」这个 bug。而且事故 fixture 早就在测试里了, 只是没人断言那个会暴露矛盾的字段。

---

## 8. 关联

- Spec: `openspec/changes/state-scanner-stale-refs-false-parity/`
- post_spec R1 报告: `.aria/audit-reports/post_spec-R1-*-state-scanner-stale-refs-false-parity-*.md` (3/5 agent; code-reviewer + knowledge-manager 经 owner 决策跳过, R2 跑满 5 人)
- aria-plugin #109 (协调层维度; R1 核实真 disjoint — 代码面零重叠, `coordination_probe` 读本地 telemetry 分区非 git ref)
- memory: `feedback_concurrent_duplicate_audit_fetch_before_start` (本缺陷是其工具层成因) / `feedback_probe_first_scope_reframe` / `feedback_test_mock_pattern_hides_prod_bug` (R-8 精确命中) / `feedback_completion_signals_vs_runtime_invocation` (v1 的 F1 死代码风险)
- CLAUDE.md 多远程推送段 (2026-04-10 市场滞后事故 —— 即本缺陷盲区所在)
