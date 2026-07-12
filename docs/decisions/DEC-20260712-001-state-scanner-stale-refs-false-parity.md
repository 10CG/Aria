# DEC-20260712-001 — state-scanner 陈旧 ref 假同步 (parity false-green)

> **状态**: **v2 (2026-07-12)** — post_spec R1 判 FAIL (3/3 agent unanimous, 机制级 Critical 全部实证), v1 药方被推翻; owner 批准重设计方向 (F3′ 并行 fetch-all)。v1 决策 D1/D2/D3 已作废, 见 §3。
> **创建**: 2026-07-12 | **v2 修订**: 2026-07-12 (折入 post_spec R1 的 3C + 12M/m)
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

> ⚠️ (R1 m3) 「#109 首次活体验证」的措辞需与 `coordination-gate-invocation` 探针分区实证交叉核对再落笔 (memory `feedback_spec_precedent_verify_execution_history`: shipped ≠ executed)。

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
