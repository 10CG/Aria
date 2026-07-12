---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
verdict: FAIL
timestamp: 2026-07-12T20:00:00.000Z
context: state-scanner-stale-refs-false-parity
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
---

# post_spec 收敛审计 — state-scanner-stale-refs-false-parity (R3 + R4 聚合)

> **接续**: [R1+R2 聚合报告](./post_spec-R1-R2-2026-07-12T1850Z-state-scanner-stale-refs-false-parity-aggregated.md)
> **Anchor** (不变): 修复 sync parity 假绿, 使「陈旧证据 ≠ 新鲜证据」不变量成立。`source_sha`: `fc7c372`
> **Forgejo**: aria-plugin **#110**

---

## Round 3 — Spec v2 → v3 (换轴后的边界条件)

**参与**: 5/5 | **Verdict: FAIL** (2 FAIL / 3 PASS_WITH_WARNINGS; **未收敛**)

| agent | verdict | findings |
|-------|---------|----------|
| tech-lead | **FAIL** | 2C + 4M + 2m |
| code-reviewer (fresh) | **FAIL** | 1C + 9M + 4m |
| backend-architect | PASS_WITH_WARNINGS | 0C + 3M |
| qa-engineer | PASS_WITH_WARNINGS | 0C + 4M |
| knowledge-manager (fresh) | PASS_WITH_WARNINGS | 0C + 2M + 5m |

> **五位一致: 轴正确, 不需第三次换轴。** R2 的 finding 集全灭; R3 findings 全部是**新轴上的边界条件**。

### R3 Critical

**R3-C5 (tech-lead) — ∀ 公式**太严**: 结构性 `unknown` 被阻断 ⇒ 本仓恒 false**

v3 的 `overall_parity = ∀ r: 可信(r) ∧ parity(r) ∈ {equal, ahead}`。但:
- `detached_head` ⇒ `parity: unknown` ⇒ `∉ {equal, ahead}` ⇒ **阻断**
- 而 **detached HEAD 是每个子模块的规范常态** —— `git submodule update --init --recursive` (CLAUDE.md 让每个新采用者跑的第一条命令) 会把**全部**子模块置于 detached HEAD
- 实测本仓: `aria` 子模块正是 detached (`git -C aria rev-parse --abbrev-ref HEAD` → `HEAD`)

⇒ **`overall_parity` 在 Aria 自己的仓库上恒 false**, 即使一切健康、刚刚全量 fetch 完。**每个新采用者第一天就恒红。**
⇒ `no_local_tracking_ref` (未推送的 feature 分支 = **整个 Phase B**, 十步循环里最长的一段) 同理。

**方法论根因**: v3 只**豁免了 `ahead`**, 没问「还有哪些健康常态值落在允许集之外」—— **点修, 不是类修**。而这与本 Spec 自己批评 QA-C1 (「只修 no-data 没修 old-data」) 是**同一种错误**。
> *「从来没有人把 `parity` 的 5 个取值 × `reason` 的 9 个枚举摊开, 逐格问一遍『健康常态下它应该是什么』。」*

**R3-N1 (code-reviewer) — ∀ 公式**太松**: `all([]) == True` ⇒ vacuous true ⇒ 复活 QA-C1 假绿**

v3 的 ∀ 公式**无声废除了 QA-C1 的正证据要求** (代码有两道显式护栏: `_aggregate_flags([])` → `False`, 注释写死 `# QA-C1: no remotes = no evidence = not confirmed`)。

可达场景:
1. `read_only_remotes` 覆盖全部 remote ⇒ 参与集空 ⇒ `all([]) == True` ⇒ **零证据报「已同步」**
2. 零 remote 的仓库 ⇒ 同上 (今天是 False)
3. 单 remote 且 `ahead` ⇒ v3 = true, 现状 = false —— **一次未声明的语义反转** (而 tasks 却宣称「这是保留不是反转」)

⇒ **这正是 Spec 自己点名批评的 `check_parity.sh:383` `jq 'all(...)'` 假绿** —— v3 会把它**从 shell 抄进 Python**。

### R3 Major (跨 agent 去重)

| # | 内容 | 提出者 |
|---|------|--------|
| M-1 | **可达性与新鲜度两轴被挤在一条路径**: github token 刚过期但 200s 前 fetch 成功过 ⇒ `200s < 300s window` ⇒ 判「可信」⇒ 不降级 ⇒ **不记 reason** ⇒ `has_unreachable_remote=false` ⇒ **不可达告警不响**。凭据坏了 5 分钟, snapshot 一声不吭 | tech-lead |
| M-2 | **TTL per-remote replay 前提在 v3 消失**, 而 AC 完全依赖它。现 cache schema 只有 3 个标量键, **无 per-remote 结构** | tech-lead + code-reviewer |
| M-3 | **网络成本无上界**: `ceil(N/cap) × slowest` 中 **N 无界** —— 采用者 20 子模块 × 3 remote = 60 腿 ⇒ **105s/scan**。而 AC-3 的 wall-clock 又被降格为非 gate ⇒ **blast radius 最大的一面既无上界也无 gate** | tech-lead |
| M-4 | **`_run` 无非交互契约** (`_common.py:344-366`: 有 `capture_output` 但**无 `stdin=DEVNULL`**, env 只有 `LC_ALL`) ⇒ F3′ 后采用者的无凭据 remote 会**阻塞在凭据提示**直到 timeout | tech-lead |
| M-5 | **`multi_remote_drift` 建议须按成因分派** (≥6 种), 「一律改 fetch/pull」是**把 v1 的对称错误换方向再犯** (US-008 directional guard: 方向搞反会 `update --remote` **覆盖未推送的本地 commit**) | tech-lead |
| M-6 | 🔴 **`enforced_remotes` 的配置事实 v3 写反了** —— 它**早在 `DEFAULTS.json:60` 的 `state_scanner.multi_remote` block 声明** (值 null), 顶层 `multi_remote` 另有 `{enforced_remotes: [], read_only_remotes: []}`, **两者 `.py` 中命中均为 0**, 而 `sync-detection.md:515` 记它「已实现」⇒ **死配置 + 假文档 = #95 归档门靶心**。且 `multi_remote.py` **完全绕过 config-loader** | code-reviewer |
| M-7 | 🔴 **Rule #7 新 secret 暴露面**: 代码有**两种对立先例** —— `coordination_fetch._classify_error` 返回脱敏短串 (docstring 明写 "Rule #7 compliance"), 而 `git.py:184/356` / `sync.py:150` **直接把原始 stderr** 塞进 `soft_error` → `snapshot["errors"]` → **被 AI 读进对话**。F3′ 把失败路径放大 N×M 倍; Layer-2 aria-runner 容器用 HTTPS-with-embedded-token remote URL | code-reviewer |
| M-8 | **AC-6 谓词过宽**: 「任意 HEAD 不可达的 commit」—— 任何有其它活跃分支的仓库**本来就有** ⇒ 健康仓假红 + 误触设计闸。真实指纹是「**同分支**的 track commit 不可达」 | code-reviewer |
| M-9 | **tasks 2.1 与 5.1 自相矛盾**: 2.1 要往 `test_local_refs_stale_flag` 加断言, 5.1 却要**退役** `local_refs_stale` ⇒ 该测试**永远转不绿** ⇒ 按 2.7 的设计闸「红测试转不绿 = 设计缺陷回 Phase A」⇒ **设计闸把自己误杀** | code-reviewer |
| M-10 | **AC-5 数字数学上不可满足**: baseline 1021 passed + §2 新增 ≥5 测试 ⇒ 总数必 ≥1027, 却要求「1022 passed」。且 pytest 跑不通 (44 collection errors, 测试实经 `run_tests.py` unittest) | code-reviewer |
| M-11 | **收窄 fetch 有 4-5 个旋钮、无统一心智模型** (`fetch_all` / `enforced_remotes` / `read_only_remotes` / 硬关闭契约 / `coordination.enabled` 混淆) ⇒ **会用一次修复换一次同类 drift**。建议**删除 `fetch_all: false`** (`enforced_remotes: ["origin"]` 已够) | backend-architect |
| M-12 | **read-only 排除只盖 `overall_parity`**, 没盖 `has_unreachable_remote` / `multi_remote_drift` 触发 | backend-architect |
| M-13 | **F9′ 的二选一漏出正式 OQ 列表**, 而它直接落在 **US-008 数据丢失护栏**路径上 | backend-architect |
| M-14 | 🔴 **`sync.py:_collect_current_branch` 是第三个平行 ref 读取点** (独立对 `@{u}` 算 ahead/behind, **无 `fetch_ok` 概念**), 而 `scan.py:127` 把它与 `multi_remote` 合并进**同一个** `sync_status` 对象 ⇒ origin fetch 失败时**同一 snapshot 自相矛盾**。**调顺序解决不了「两处独立计算、只有一处降级」的结构性问题** | qa-engineer |
| M-15 | 🔴 **F8′/AC-4 建立在一个不存在的字段上**: snapshot 顶层**无 `generated_at`**, `scan.py` 全文零 `datetime.now`/`utcnow`/`isoformat`。**而兄弟 Spec `aria-2.0-m7-fleet-aggregation` (Approved) 的 probe-first recon (proposal L82) 早已记录该字段不存在**并留了 CAVEAT (被迫用文件 mtime 兜底) ⇒ **别人踩过的耙子又踩一遍** | knowledge-manager |
| M-16 | 🔴 **`enforced_remotes` 漏看第三个消费方**: `phase-c-integrator/SKILL.md:574` **已发布契约**「skill 级为 null 时**继承顶层** `multi_remote.enforced_remotes`」 ⇒ state-scanner 若另立门户 = **split-brain** = 本 Spec 的病在**跨 skill 层**复现 | knowledge-manager |
| M-17 | 🔴 **F3′ 泛化了一个有自己 Spec 的机制却没读那份 Spec**: `coordination_fetch` 有归档 Spec **#141** (two-fetch 拆分: Fetch 1 `+refs/heads/*` **载重** + Fetch 2 `refs/aria/coordination`, `success` **显式锚定 Fetch 1**)。github/子模块远端**几乎必然没有** `refs/aria/coordination` ⇒ 若 `fetch_ok` 不锚定 Fetch 1 ⇒ **每个非-origin remote 恒 false ⇒ 恒红** | knowledge-manager |
| M-18 | **Rule #6 (不可协商) 未落 tasks** + **AB rubric `ab-suite/state-scanner.json:143` 明写** `"Should exclude parity: ahead and parity: unknown from overall_parity computation"` ⇒ v2 的 D5(a) 会**把正确的新行为判为错** (独立佐证了 R3-C5) | knowledge-manager |
| M-19 | **AC-3 的 wall-clock 绝对预算 = Spec 亲手引入自己抨击的病** (环境相关 ⇒ AI 可代填 true) | knowledge-manager |

### R3 跨 agent 矛盾 (owner 独立裁决)

**`fetched_at` 是否在 `normalize_snapshot` 的易变字段白名单?**
- tech-lead + code-reviewer: **不在** ⇒ 会让 `test_two_consecutive_runs_diff_zero` flaky (各据此提了一个 Major)
- qa-engineer: **在** (`TIMESTAMP_KEYS`) ⇒ 会被打码成 `<timestamp>`

**owner grep 裁决**: `normalize_snapshot.py:43` 的 `TIMESTAMP_KEYS` **第一个元素就是 `"fetched_at"`** ⇒ **qa-engineer 对, 另两位错。两位在 R4 均主动认错。**

⇒ **memory `feedback_cross_agent_verdict_independent_verify` 的又一次实证: 两个 agent 给出相同的代码事实, 也可能同时错。**

---

## Round 4 — Spec v3 → v4 (+ 拆 3 Spec)

**参与**: 5/5 | **Verdict: FAIL** (4 FAIL / 1 PASS_WITH_WARNINGS; **未收敛**)

| agent | verdict | 核心发现 |
|-------|---------|---------|
| tech-lead | **FAIL** | C6 (fail-open 默认) + C7 (AC-8 ⊥ AC-12) + 2M |
| code-reviewer | **FAIL** | X-1 (Spec C 的 AC-3 恒红) + 6M。**母 Spec 单独评: PASS_WITH_WARNINGS (0C)** |
| knowledge-manager | **FAIL** | R4-C1 (同 C6) + 三套 `_classify_error` 词表 |
| backend-architect | **FAIL** | 同 C6 (**真实 git 连接失败复现**) + `∀ 可信` 缺口 |
| qa-engineer | PASS_WITH_WARNINGS | 0C; **三个点名场景实测全过**; 独立发现 `∀ 可信` 缺口 |

> **五位一致: 轴、公式、两轴拆分、benign/blocking 二分都对了。** 收敛**单调**: v1 药方自拆台 → v2 边界条件 → v3 公式两端都错 → **v4 只剩「分类表的空格 + 一条 ∃-子句 + 两处文本不同步」**。

### R4 Critical

**R4-C1 (四方独立收敛) — `blocking_unknown` 写成**正向枚举** ⇒ 未列举值 fail-OPEN**

v4 写的是 `blocking_unknown(r) := reason(r) ∈ {6 个显式值}`。**任何不在这六个里的值都 fail-OPEN (不阻断)**。

实测可达的漏网之鱼:
1. **`reason = None` + `parity = unknown`**: `multi_remote.py:308/312/317` **三条 best-effort 返回路径**
2. **`parse_error`** (`:281`) —— owner 自查 grep 时发现 (v4 初稿两个桶都没有它)
3. **姊妹 Spec B 分类器的兜底值** `unknown` / `git_error` / `permission_denied` / `timeout`

**backend-architect 用真实 git 连接失败复现**:
```
真实 stderr: fatal: unable to access '...': Failed to connect to ... Couldn't connect to server
matched signals: []                     ← 一个已知分类 pattern 都没中 ⇒ 落 catch-all

模拟器 (逐字对照 proposal 公式):
  reason='git_error'         -> blocking_unknown()=False   ← 静默放行
  reason='permission_denied' -> blocking_unknown()=False
  reason='unknown'           -> blocking_unknown()=False
```

⇒ **本 Spec 要杀的那个 bug 原样复活, 只是换了入口: 从「陈旧证据当新鲜证据」变成「零信息当无害」。**

**knowledge-manager 补充: 代码里有三套互不相同的 `_classify_error` 词表**:

| 来源 | 枚举 |
|------|------|
| `coordination_fetch.py:236` (Spec B 要提炼的对象) | `network` / `auth_403` / `non_ff` / `git_missing` / `other` |
| **`issue_scan.py:311` 另一个同名函数** (Spec B **完全没提它存在**) | `ERR_CLI_MISSING` / `ERR_TIMEOUT` / `ERR_AUTH_FAILED` / ... |
| Spec B 提议的新共享枚举 | `network_timeout` / `auth_failed` / `permission_denied` / `git_error` / `unknown` ... |

⇒ **Spec B 自相矛盾**: AC-4 要求 `coordination_fetch` 行为「**逐字节不变**」(断言的是第 1 套词表), 而 §1 提议的是第 3 套。**两个要求不可能同时满足。**

**修法 (四方逐字一致)**:
```
benign_unknown  := 显式封闭白名单
blocking_unknown := parity=="unknown" ∧ ¬benign_unknown        ← fail-CLOSED
```

**R4-C7 (tech-lead) / X-5 (code-reviewer) — AC-8 ⊥ AC-12 字面互斥**

- AC-8: 「有未推送 commit 的**健康仓** ⇒ `overall_parity` **仍 true**」
- AC-12: 「无任何 `可信 ∧ equal` 的 remote (**如单 remote 且 ahead**) ⇒ **必须 false**」

**一个「单 repo + 单 remote + 有未推送 commit」的仓库同时满足两条的前件。两条 AC 不可能同时通过。**

⚠️ **两位给出相反的药方** (真实的产品语义分歧):
- **tech-lead**: 公式错了 —— `ahead` **是**正证据 (「远端 head 是我们的祖先」= 对远端位置的**新鲜且确定**的知识)。且单 repo + 单 remote + 未推送 = **中位数采用者**, 按「健康常态该是什么值」判据答案是 true。
- **code-reviewer**: AC-8 错了 —— `overall_parity` 的语义就是「本地与远端相同」; 有未推送 commit **确实不是**已同步, 报 false 是诚实的, 且下游给的 `push` 建议**是对的**。公式与现状代码 (`has_equal_evidence`) / golden fixture / AB rubric **三者一致**。

**owner 裁定 (2026-07-12): 采纳 code-reviewer** —— `overall_parity` 语义 = 「本地与远端一致」。**本 Spec 修的是「落后时假绿」(危险: 会在旧代码上开工重复劳动), 不是「领先时假红」(领先不会导致重复劳动)。** 是 AC-8 的措辞把「健康」与「已同步」偷换了概念。tech-lead 的反方论据存档, 若 Phase B dogfood 实测告警疲劳成立可重开。

**R4-X-1 (code-reviewer, 在 Spec C) — AC-3 会 ship 一个新恒红**

Spec C 的 AC-3 断言 `generated_at <= issue_status.fetched_at`。**但 `issue_scan` 有 900s 缓存** —— cache 命中时 (`issue_scan.py:766`) 它把**缓存里的** `fetched_at` (**上一次** scan 的时刻) 原样端出 ⇒ **`fetched_at` 早于 `generated_at`** ⇒ **该断言恒 false**。而 15 分钟内重复 scan **命中缓存是常态路径**。

⇒ **在一个专门修「恒红」的 Spec 里, 用一条制造「缓存路径恒红」的断言。**

### R4 Major

| # | 内容 | 提出者 |
|---|------|--------|
| **`∀ 可信(r)` 缺口** | ∀ 子句里的独立 `可信(r)` 项**冗余且有害**: 对 `equal` 的 r, F1′ 降级**已经**把不可信的变成 `not_refreshed`(∈blocking) 挡住了; 对 `behind`/`ahead` 的 r, 新鲜度**没有正确语义**; 对 benign 的 r, 会让「该 remote 恰好这次 fetch 失败」把 `overall_parity` **拖成恒红** | qa-engineer + backend-architect (**独立收敛**) |
| **benign 不是同质的** | ⚠️ tech-lead 与 backend-architect **正面冲突**: 前者说 benign 不能整体豁免 `可信` (`no_local_tracking_ref` 是 **fetch-依赖**的 —— fetch 失败时「没这个 ref」可能只是「我们没 fetch 过」); 后者说应整体豁免 (`detached_head` 的 parity 判定**压根不依赖 fetch**)。**owner 代码实测裁决: 两人都对** —— `multi_remote.py:169/173` 的 `detached_head`/`shallow_clone` 在**读任何 ref 之前**就返回 (fetch-无关); `:181` 的 `no_local_tracking_ref` 是**读 ref 失败**才返回 (fetch-依赖) ⇒ **benign 必须再分一层** | tech-lead ↔ backend-architect |
| deadline × 可达性轴冲突 | 被**我们自己的预算**砍掉的 leg: `fetch_ok=false` ⇒ 按 F1′ → 置 `has_unreachable_remote` (**报 remote 不可达, 但它其实好好的, 只是我们没等**); 按 F3′ → `not_refreshed` (不置)。**Spec 没说哪条赢** | code-reviewer |
| deadline 默认值致大仓恒红 | 20 子模块 × 3 remote = 60 腿 ≈ 105s ⇒ 默认 deadline **15s** ⇒ 大部分 leg 被砍 ⇒ `not_refreshed` ⇒ blocking ⇒ **`overall_parity` 恒 false**。**性能护栏偷偷变成了正确性回归** | code-reviewer |
| **AC-5 无任何对应任务** | v3 有 12.5, **v4 拆分时丢了**。而它恰恰是**本 Spec 叙事的起点** (「同一份 snapshot 自相矛盾 = collector 编排缺陷的指纹」) ⇒ 会作为「**AC 勾了但从没实现**」ship = **本仓刚 ship 的 #95 归档门会 block 它** | code-reviewer |
| **Spec B 站点数错了** | Spec B 说「收口**三处**」。实测 **≥8 处** (`sync.py:232/244`, `handoff_multibranch.py:298/334/354`, `handoff_worktrees.py:348`)。而 **Spec B 的 AC-2 是「grep 断言零处直传」的机械闸** ⇒ 只改 3 处 ⇒ **AC-2 必红 ⇒ Spec B 自相矛盾**。(**好消息: 这个机械闸设计对了 —— 它自己把漏洞逼了出来。**) | code-reviewer |
| **Spec B 的 AC-1 靶点错位** | §Why 点名的三处 (`git log` / `git status` / `rev-list`) 是**纯本地命令** —— argv 里**根本没有 remote URL** ⇒ 用「凭据 URL 的失败 fetch」做 fixture **在未修改代码上就会 PASS** ⇒ **违反它自己的自我否证闸** | qa-engineer |

### R4 实测验证 (qa-engineer, 三个点名场景全过)

```
AC-11 (detached-HEAD 子模块 + 全部刷新成功 + 主仓 equal):
  真实构造 (clone + submodule update --init, 真 detached HEAD)
  overall_parity = True  ✅
  且用真实 aria 子模块验证 dogfood 前提: git -C aria symbolic-ref -q HEAD 失败 ⇒ 确认 detached (0964496)

AC-12 (空参与集 / 单 remote 且 ahead):
  空集 → False ✅ (enforced_set≠∅ 护栏)
  单 remote ahead → False ✅ (∃-equal 护栏)

AC-13 (auth 失败但 fetched_at 在窗内):
  parity 保持 equal (不降级) ✅ | has_unreachable_remote=True ✅ | error_kind=auth_failed ✅
  底层验证: 失败的 fetch **不会清空/破坏已存在的 remote-tracking ref 文件**
  ⇒ 「parity 保持 equal 是自然发生的, 不需特殊代码」这条设计假设站得住
```

---

## v5 公式 (R4 五方发现的合成解)

```
# benign 不是同质的 —— 必须按「fetch 能否改变它」再分一层 (代码实测):
benign_unknown(r) := parity(r) == "unknown" ∧ (
      reason(r) ∈ {detached_head, shallow_clone}                     # ① fetch-无关 (:169/:173 在读任何
                                                                     #    ref 之前就返回) ⇒ 恒 benign
   ∨ (reason(r) ∈ {no_local_tracking_ref, remote_branch_missing}     # ② fetch-依赖 (:181 是"读 ref 失败")
        ∧ 可信(r))                                                   #    ⇒ 只有本次刷新成功才 benign
  )

blocking_unknown(r) := parity(r) == "unknown" ∧ ¬benign_unknown(r)   # 🔴 fail-CLOSED 兜底

overall_parity = (enforced_set ≠ ∅)                                  # 防 vacuous true
               ∧ (∃ r: 可信(r) ∧ parity(r) == "equal")               # QA-C1 正证据 (可信只需在此出现)
               ∧ (∀ r: parity(r) ∉ {behind, diverged}                # ⚠️ ∀ 里没有独立的 可信(r) 项
                       ∧ ¬blocking_unknown(r))
```

**这一个公式同时满足五位 agent 的全部发现**:
- code-reviewer 的 vacuous-true 护栏 (非空 + ∃-equal)
- tech-lead 的 benign 不阻断 + `no_local_tracking_ref` 的 fetch-依赖性
- backend-architect 的 `detached_head` 不该被 fetch 失败拖累
- qa-engineer 的「`可信` 从 ∀ 删掉」
- 四方一致的 fail-CLOSED 兜底

---

## 收敛状态

**R3 → R4: 未收敛**, 但**收敛是单调的**:

| 轮 | 剩余缺陷的量级 |
|----|---------------|
| R1 | 药方**机制上自我拆台** (换轴) |
| R2 | 新轴上的**边界条件** |
| R3 | **公式两端都错** |
| R4 | **分类表的空格 + 一条 ∃-子句 + 两处文本不同步** |

**五位一致: 不需第五次换轴。修完 R4 的发现, R5 应当 PASS。**

**下一步**: post_spec **R5** (tech-lead 建议: 只审 F4′ 的最终公式 + R4 的 5 个修正点, 不必跑全量 —— 其余部分已被五方在 R1-R4 反复验过)。

---

## 元教训

1. **「把一个不变量写进文档」≠「把它写进兜底默认值」。** 没有为「集合的补集」定义行为, 就是给了它一个隐式的、通常是错的默认。QA-C1 的不变量在本 Spec 起草过程中**复发五次**。⇒ memory `feedback_invariant_needs_failclosed_default`
2. **修复必须类修, 不能点修。** 必须把取值域 (parity × reason) **摊开逐格填**, 且**必须 grep 出全集** —— 不能凭印象列举 (owner 自查时又漏了 `parse_error`, 这是第四次漏格)。**已把「逐格填」从纪律变成机制** (pin 测试: 构造一个代码里不存在的枚举值 ⇒ 必须落到保守侧)。
3. **假绿的反面是恒红, 两者同样零信息量。** 本 Spec 在修假绿时**三次过冲成恒红** (v2 的 ahead / v3 的 detached_head / Spec C 的 cache-hit)。⇒ memory `feedback_false_green_dual_is_permanent_red`
4. **两个 agent 给出相同的代码事实, 也可能同时错。** (R3 tech-lead + code-reviewer 同错, qa 对, owner grep 裁决。两位在 R4 主动认错。) ⇒ 补强 memory `feedback_cross_agent_verdict_independent_verify`
5. **泛化一个既有机制前, 先找它自己的 Spec / 先 grep 全仓枚举它所有的既有实现。** (漏读 #141 two-fetch 语义; 漏发现 `issue_scan.py` 的第二个 `_classify_error`。)
6. **机械闸会自己把漏洞逼出来。** Spec B 的 AC-2 (grep 断言零处直传) 正是它暴露了「三处 vs 实际 ≥8 处」的错误。**设计一个会自己失败的验收条件, 比设计一个会自己通过的强。**
