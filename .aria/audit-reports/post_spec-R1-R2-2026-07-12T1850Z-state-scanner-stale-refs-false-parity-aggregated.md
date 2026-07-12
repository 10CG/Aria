---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
verdict: FAIL
timestamp: 2026-07-12T18:50:00.000Z
context: state-scanner-stale-refs-false-parity
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
---

# post_spec 收敛审计 — state-scanner-stale-refs-false-parity (R1 + R2 聚合)

> **Anchor** (Step 0, 审计周期内不可变)
> - `primary_goal`: 修复 state-scanner 的 sync parity 假绿 —— 陈旧 remote-tracking ref 下报 `overall_parity: true` / `parity: equal`, 而工作树实际落后远程, 导致 AI 基于落后状态开工重复劳动。使「陈旧证据 ≠ 新鲜证据」不变量成立 (QA-C1「零证据 ≠ 正证据」的孪生)。
> - `in_scope`: F1 陈旧度参与裁决 / F2 阈值 / F3 collector 顺序 / F4 custom_checks 顺序; `multi_remote.py`, `scan.py`, config 默认值, snapshot schema
> - `out_of_scope`: aria-plugin #109 (协调层 claim 前移); aria-orchestrator 的 github 镜像策略
> - `source_sha`: `fc7c372`

---

## Round 1 — Spec v1

**参与**: 3/5 (tech-lead / backend-architect / qa-engineer)。code-reviewer + knowledge-manager 经 **owner 决策跳过** (R1 已 unanimous FAIL 且 Critical 在机制层, 药方将整体重写 → 边际价值低; R2 跑满 5 人)。`incomplete: true`。

**Verdict: FAIL — 3/3 unanimous**

| agent | verdict | findings |
|-------|---------|----------|
| tech-lead | FAIL | 2C + 4M + 3m |
| backend-architect | FAIL | 3C + 5M + 5m |
| qa-engineer | FAIL | 2C + 7M + 6m |

### R1 Critical (跨 agent 收敛, 全部有实证)

**C1 — 新鲜度信号无 per-remote 分辨率, 且 F3 会把它清零 (3/3 agent 独立复现)**

`_fetch_head_age_hours()` (`multi_remote.py:130-142`) 读 `<gitdir>/FETCH_HEAD` 的 **mtime** —— 每仓一个文件, 任何 remote 的任何 fetch 都整体覆写。**代码中不存在任何 per-remote 新鲜度数据。** `coordination_fetch` 只 fetch 单个 remote (origin)。⇒ v1 的 F3 (前移) 使 FETCH_HEAD age≈0 ⇒ `local_refs_stale` 对所有 remote (含 github) 结构性恒 False ⇒ **F1 变死代码, F2 变 no-op。两个部件互相拆台。**

实测 (backend-architect, `/tmp/fhtest`, 真 fetch + 真 collector):
```
BEFORE fetch: FETCH_HEAD age = 14.00 h
>>> git fetch origin --no-tags +refs/heads/*:refs/remotes/origin/*
AFTER  fetch: FETCH_HEAD age = 0.0000 h
   refs/remotes/origin/master   68284bf   ← 刷新
   refs/remotes/github/master   326074e   ← 依然陈旧

阈值扫描 (github ref 人为 aged 30 天):
  warn_after_hours=24     → local_refs_stale=False, github.parity=equal, overall_parity=True
  warn_after_hours=1      → 同上
  warn_after_hours=0.001  → 同上   ← 3.6 秒阈值都救不回来
```

本地新鲜度候选信号**逐一实测排除** (qa-engineer):

| 候选 | 结论 |
|------|------|
| `FETCH_HEAD` mtime | repo 全局单值, 任一 fetch 都重置 |
| `.git/refs/remotes/<r>/<b>` 文件 mtime | **只在 ref 值变化时更新** → 「刚 fetch 但没变」与「3 天没 fetch」不可区分 |
| 同上, packed 之后 | `git pack-refs` (gc 自动跑) 后 loose 文件**直接消失** → 信号归零 |

⇒ **新鲜度不能「测量」, 只能「获取」。**

**C2 — 子模块零新鲜度覆盖 (tech-lead + backend-architect)**

`_scan_repo()` 恒返回 `stale=False` (L364-365, 死返回值); 陈旧度只对 `project_root` 算一次; `_fetch_head_age_hours` 在 FETCH_HEAD 缺失时返回 `None`, 而 L497 `if age is not None and age > warn` ⇒ **`None` 判为「不陈旧」**。实测三个子模块 `.git/modules/*/FETCH_HEAD` **全不存在** ⇒ **「从未 fetch」(最陈旧) 被当成最新鲜**, 且照样向 `overall_parity` 提供 `equal` 正证据。

**这是 QA-C1 不变量的第三次违反** (零证据 → 陈旧证据 → **从未获取过的证据**)。而 Spec 引的第二条硬证据 (aria-orchestrator github 镜像落后 32 commit) **恰恰是子模块**。

HEAD 上的活体现状 (qa-engineer 真跑本仓):
```
overall_parity: True
main:                   [(github, equal),   (origin, equal)]
 sub aria:              [(github, unknown), (origin, unknown)]   ← 两 remote 全 unknown, 仍被吞
 sub aria-orchestrator: [(github, unknown), (origin, equal)]
```

**C3 — v1 的 F1 字面语义制造新假绿并杀死 push 提醒 (backend-architect)**

v1 写「陈旧时把该 remote 的 `parity` 降级为 `unknown`」—— 无限定。但 `unknown` 不阻断 `overall_parity`。实测:
```
origin 新鲜+equal; github 陈旧且读作 behind (真落后)
  TODAY              : overall_parity=False   ← 现状反而是对的
  AFTER F1 (v1 字面) : overall_parity=True    ← 假绿翻转

单 remote 陈旧且读作 ahead (有未推送工作)
  TODAY              : has_pending_push=True
  AFTER F1 (v1 字面) : has_pending_push=False ← session-closer 未推送告警死掉
```
`multi_remote.py:270-277` 的 **QA-I1 注释明写警告过这个失败模式**。⇒ 降级**只能针对 `equal`** (正证据); `behind`/`diverged`/`ahead` 是**下界**, 依然是真信号, 不得动。

**C4 — AC-3 把唯一正解排除在解空间外 (qa-engineer)**

本地既无 per-remote 新鲜度信号, 正确修复**必然**增加网络调用。而 v1 的 AC-3 断言「fetch 次数不增加」⇒ **AC-3 与 primary_goal 二者只能活一个**。

### R1 Major 摘要

`git` block 与 `sync_status` 会在同一 snapshot 打架 (F3 落点) / `handoff_autofill.py:52` 静默吞 `unknown` / `multi_remote_drift` 给的是 push 建议 / `git-remote-helper` 里 **QA-C1 那个"已修复"的缺陷还活着** (`check_parity.sh:383` `jq all` 对空数组返 true) / F2 SOT 清扫只覆盖 2/6 处 / **baseline 不是全绿** (`test_normalize_snapshot::test_two_consecutive_runs_diff_zero` 现红, 红因正是 F4) / **既有测试 mock 是共犯** (把 tracking ref 钉死为 ground truth ⇒ 结构上测不出「ref 不是 ground truth」; 且 `test_local_refs_stale_flag` **早已构造事故 fixture 却从未断言 `overall_parity`** —— 矛盾早在屏幕上) / golden fixture 腌入假绿。

### R1 → v2 处置

owner 批准重设计方向。v1 的 D1/D2/D3 作废。核心换轴: **新鲜度靠获取, 不靠测量**。

承重性能 spike (主控实机, 本 session):
```
串行全量 fetch (8 个 repo×remote 对) = 42.7s
并行全量 fetch (8 个对)              =  7.6s   ← 等于最慢单腿 (origin 走 CF Access ~7s)
当前 scan 已在付的 origin fetch       ≈  7.0s
当前 scan 全程                       = 16.9s   ⇒ 边际 ≈ +0.6s (+4%)
单次 ls-remote ≈ 单次 fetch (均被 SSH 握手主导) ⇒ OQ-2 (ls_remote) 删除
```
(tech-lead 独立复现: 8 腿并行 7.81s = 最慢单腿, 8/8 rc=0)

---

## Round 2 — Spec v2

**参与**: 5/5 (R1 的 3 位续跑带上下文 + code-reviewer / knowledge-manager fresh eyes)。

**Verdict: FAIL — 未收敛 (R1 finding 集全灭, 但 R2 finding 集非空)**

| agent | verdict | findings | R1 findings 处置 |
|-------|---------|----------|------------------|
| tech-lead | FAIL | 2C + 4M + 2m | 6/6 fixed |
| code-reviewer (fresh) | FAIL | 1C + 9M + 4m | — |
| backend-architect | PASS_WITH_WARNINGS | 0C + 6M | 3C fixed, 2M partial |
| knowledge-manager (fresh) | PASS_WITH_WARNINGS | 0C + 7M + 5m | — |
| qa-engineer | (见下) | — | — |

> **五位一致认同轴正确** —— 「不需要第三次换轴」/「不需要回 brainstorm」。R2 findings 全部是**新轴上的边界条件**。

### R2 Critical

**R2-C1 (tech-lead) — OQ-1 (a) 没给 `ahead` 豁免 ⇒ `overall_parity` 在开发常态下恒 false**

v2 的 D5(a) 规定「`overall_parity: true` 要求**每个** enforced remote 都确认 `equal`」。但 `ahead ≠ equal` ⇒ **任何有未推送 commit 的仓库 ⇒ false**, 而未推送 commit 是 Phase B 的**默认状态**。唯一下游 `multi_remote_drift` (trigger = `overall_parity=false`) **每次 scan 都触发** ⇒ 告警疲劳 ⇒ 信号归零。**这与 v2 自己在 F4′ 立的标准 (「恒红 = 信号失去意义」) 直接自相矛盾** —— 用一个新假警报换掉一个旧假绿。

**三处独立证据一致反对 D5(a)** (owner 独立复核确认):
- 代码: `multi_remote.py:400-402` 明写 `# ahead does NOT flip overall_parity (normal pending-push state)`
- golden fixture (采自真实 scan): `main github -> ahead` 且 `overall_parity: True`, `has_pending_push: True`
- AB benchmark rubric `ab-suite/state-scanner.json:143`: `"Should exclude parity: ahead and parity: unknown from overall_parity computation"`

⇒ **D5(a) 会让 AB rubric 把正确的新行为判为错。**

Fix: `overall_parity = true iff ∀ remote: refreshed(remote) AND parity ∈ {equal, ahead}` (ahead 继续由 `has_pending_push` 单独承载)。

**R2-C2 (tech-lead) — F1′ 的载重谓词与 30s TTL 缓存冲突, 使 AC-5 数学上不可达**

proposal 的 F1′ 规范文本: 「parity 可信度由**本次 scan 是否成功刷新了该 remote** 决定」。但 `coordination_fetch.py:300-320`: **TTL 未过期 ⇒ 直接短路返回, 一次 fetch 都不跑**。⇒ TTL 命中时「本次是否刷新」= 否。

硬冲突 (可证伪): `test_normalize_snapshot::test_two_consecutive_runs_diff_zero` **连续跑两次完整 scan 并断言 diff == 0**。第二次必落在 30s TTL 窗口内 ⇒ run1 `equal` / run2 `not_refreshed`→`unknown` ⇒ **该测试永久 RED**。而 **AC-5 要求它转绿**。⇒ **Spec 内部硬矛盾, Phase B 照做必然撞墙。**

Fix (同时解 F2′ 的 fallback 空缺): 谓词改为
```
freshness(remote) := now - per_remote.fetched_at
可信 := freshness(remote) <= freshness_window   (默认 = TTL)
降级条件 := NOT 可信   (而非「本次是否 fetch」)
```
`fetched_at` 是 F3′ **本就要产出的字段** ⇒ TTL 命中 / 扫描内刷新 / 离线三条路径用**同一定义**统一。

**R2-C3 (code-reviewer) — R-10 的配置事实写反了**

Spec 称 `enforced_remotes` 只住顶层 `multi_remote.*`, 需「跨命名空间打通」。**实测相反**:
```
DEFAULTS.json → state_scanner.multi_remote = {..., "enforced_remotes": null}   ← _load_config 读的正是这个 block
DEFAULTS.json → 顶层 multi_remote = {"enforced_remotes": [], "read_only_remotes": []}
grep enforced_remotes  在 .py 中命中: 0
grep read_only_remotes 在 .py 中命中: 0
sync-detection.md:515 却记载它「已实现」
```
⇒ 真实缺陷是 **declared-but-never-consumed 死配置 + 已发布的假文档** —— **正是本仓 #95 归档门的靶心**。task 1.1 会去发明第 4 个键, 而正解是**消费既有键 + 修假文档**。

附带: `multi_remote.py` **完全绕过 config-loader** (直读 `.aria/config.json`, 默认值来自代码内常量) ⇒ R-6 把 `DEFAULTS.json:38` 称作「默认值 SOT」**对本 collector 不成立** (改它运行时零效果)。

### R2 Major (跨 agent 去重后)

| # | 内容 | 提出者 |
|---|------|--------|
| M-1 | **Rule #7 新 secret 泄露面**: `error` 字段无脱敏约束。代码有**两种对立先例** —— `coordination_fetch._classify_error` 返回脱敏短串 (docstring 明写 "Rule #7 compliance"), 而 `git.py:184/356` / `sync.py:150` 直接把**原始 git stderr** 塞进 `soft_error` → `snapshot["errors"]` → 被 AI 读进对话。F3′ 把网络调用扩到 N×M 个, 失败 stderr 常含 remote URL; Layer-2 aria-runner 容器用 `https://x-access-token:<TOKEN>@host/...` ⇒ **token 进 snapshot 与 chat**。Spec 零提及。 | code-reviewer |
| M-2 | **`coordination_fetch` 有自己的归档 Spec, 而 F3′ 泛化它却没读**: `#141` (v1.46.0, `2026-06-12-state-scanner-coordination-fetch-resilience`) 确立 two-fetch 拆分 (Fetch 1 `+refs/heads/*` = **载重**; Fetch 2 `refs/aria/coordination`) + benign-missing 三重 AND 闸 + `success` **显式锚定 Fetch 1**。github 镜像与子模块远端**几乎必然没有** `refs/aria/coordination` ⇒ 若 `fetch_ok` 不沿用 Fetch-1 锚定, **每个非-origin remote 恒 `fetch_ok=false` → 全数降级 → `overall_parity` 恒 false** = **把假绿换成恒红**。 | knowledge-manager |
| M-3 | **TTL 缓存继承语义留白 = 旧病复发点**: 现存代码 Fetch-1 失败+有旧缓存时返回 `cached: True` + **任意陈旧**的 `last_fetch_at` + `degraded: True`。实现者若从 `cached`/`last_fetch_at` 推导 `fetch_ok`, 就是把「上次成功」当「这次成功」—— **与被修的病同构**。须钉死 `fetch_ok=true ⟺ 本次 scan (或 ≤TTL 内一次 scan) 真正刷新了该 (repo, remote)`; 建议加 `confirmed_this_scan: bool`。 | backend-architect + code-reviewer |
| M-4 | **同仓并发 fetch 竞态 —— 实证不存在**: 10 轮同仓并发 fetch 两 remote, `10/10 rc=0`, FETCH_HEAD 两条记录都在, 零锁错误 (git 隐式串行化)。tasks 3.2 的「同 repo 内串行」是**不必要的保守**。**且承重数字 7.6s 是在全并发下测的, 与「同仓串行」约束不是同一条件** ⇒ 拿 A 条件的数字验收 B 条件的设计。二选一: 放弃同仓串行 (实证安全且更快) 或重测。 | backend-architect |
| M-5 | **并发上限必须 per-host 而非全局**: sshd `MaxStartups` 默认 `10:30:100`。采用者若 6 子模块 × 2 remote = 14 腿集中在一个 host ⇒ 超过 10 个 pre-auth 并发 ⇒ **随机丢连 ⇒ `fetch_ok` 随机 false ⇒ parity 随机 unknown** = 不可复现的间歇性假警报 (比稳定假绿更难查)。AC-3 公式随之破裂: 应为 `ceil(N_legs_per_host / cap) × slowest_leg`, 非硬编码 ×2。 | tech-lead |
| M-6 | **`_run` 无非交互契约**: `_common.py:344-366` 有 `capture_output=True` 但**无 `stdin=DEVNULL`**, env **只有 `LC_ALL`** —— 无 `GIT_TERMINAL_PROMPT=0` / 无 `BatchMode=yes` / 无 `ConnectTimeout`。今天只 fetch 已配好的 origin 故不暴露; F3′ 后采用者的 github remote 若无缓存凭据 ⇒ `git fetch` **阻塞在凭据提示**直到 30s timeout ⇒ 每 scan 白付 30s + 该 remote 恒 `not_refreshed`。 | tech-lead |
| M-7 | **`multi_remote_drift` 建议必须按成因分派**: (a) 语义下 false 有三种互斥成因 —— `behind/diverged`→pull / `ahead`→push / `not_refreshed`→查网络凭据。R-4 的「一律改 fetch/pull 导向」是**把 v1 的对称错误换个方向再犯**。`sync.py:312-328` 的 US-008 directional guard 明写: 方向搞反会导致 `update --remote` **覆盖未推送的本地 commit** (数据丢失)。 | tech-lead |
| M-8 | **`overall_parity` 的下游消费者结论错**: 「唯一消费者是非阻塞的 `multi_remote_drift`」**在 skill 树内为真、全仓为假**。`openspec/changes/aria-2.0-m7-fleet-aggregation` (**Approved, 活的**) 把 `overall_parity == false` 用作 **fleet 健康信号** (proposal L147 + tasks L126/L139, TB-health-3 pin 到 schema doc)。⇒ D5(a) 收紧后, 任何有未 fetch 子模块的项目在 fleet 看板上**集体翻 warn**。 | knowledge-manager |
| M-9 | **真 SOT 认错了**: `state-snapshot-schema.md` 才是在位 SOT (L1 自称 + L5 `AD-SSME-6`: "this document is the source of truth; scan.py references it via SNAPSHOT_SCHEMA_VERSION constant only", 由归档 Spec 确立, `validate_schema_doc.py` 机械强制)。`multi_remote.py:4` 那句 "canonical SOT is git-remote-helper" 是 **v1.15.0 的 stale docstring, 已被 AD-SSME-6 取代**。tasks 1.3 的选项 (b)「把 SOT 迁到 multi_remote.py」会**推翻 AD-SSME-6 并架空 validate_schema_doc.py**。须补选项 (c)。 | knowledge-manager |
| M-10 | **`coordination_fetch` snapshot 块的基数改变, 不是 additive**: 该块现为**扁平单-remote 标量** (`success`/`cached`/`last_fetch_at`/`refs_fetched`/... 共 10 个), 隐含「一个 remote × 一个 repo」。F3′ 变成 N×M ⇒ **基数全变**。且 m7-fleet-aggregation 已把它列入防御式消费清单。「不 bump schema version」的结论**只对 `multi_remote.remotes[]` 验证过**。 | knowledge-manager |
| M-11 | **tasks 5.2 条件写反**: 写作「**若 R2 判定保留** mtime 为 fallback → **则须**清扫 6 处 SOT」。但 D3 是**退役** ⇒ `warn_after_hours` 变**死配置键** ⇒ 清扫**更必须**。按现文, **退役路径下 5.2 永不触发 ⇒ 死键全部留在 `config.template.json` 发给每个新采用者**。且「6 处」不全, 实测 ≥8 处。 | knowledge-manager + code-reviewer |
| M-12 | **tasks 2.1 与 5.1/9.3 自相矛盾**: 2.1 要往 `test_local_refs_stale_flag` 加 `overall_parity` 断言 (今天确实 RED ✅), 但 5.1 要**退役** `local_refs_stale` ⇒ 退役后该测试的 `assertTrue(local_refs_stale)` 永远 None ⇒ **红测试永远转不绿** ⇒ 按 2.7 字面应「判定设计缺陷、回 Phase A」—— **设计闸把自己误杀**。 | code-reviewer |
| M-13 | **AC-5 的数字数学上不可满足**: 「baseline 1 failed/1021 passed ⇒ 修复后须 1022 passed/0 failed」, 但 §2 至少新增 5 个测试 ⇒ 总数必然 ≥1027。**AC-5 永远不可能满足** (或诱导 AI 代填)。另: baseline 本身**环境相关** (backend-architect 实测当下是全绿 1022, 因 `.aria/cache/issues.json` mtime 才 2.6 分钟 —— **恰恰精确验证了「该测试环境相关」的诊断**, 但也证明它不能当固定 baseline)。且 pytest 无法复现 (44 collection errors; 测试实经 `tests/run_tests.py` unittest 跑) ⇒ AC 必须写明**确切调用命令**。 | code-reviewer + backend-architect |
| M-14 | **AC-6 谓词过宽**: 「tracks_multibranch 出现 HEAD 不可达的 commit ⇒ 断言 overall_parity==false」—— 任何有其它活跃分支的仓库, 其它分支的 commit 对 HEAD **本来就不可达** ⇒ 健康仓被判假红, 或让 AC 恒不可满足并**误触 2.7 的设计闸**。真实指纹是「**同一分支** (HEAD 的 upstream) 上的 track commit 不可达」; `tracks_multibranch` 条目带 `branch` 字段 ⇒ 可精确限定。 | code-reviewer |
| M-15 | **把所有 fetch 失败塌缩成 `not_refreshed` 会杀掉不可达信号**: F3′ 的 fetch 失败**大多数就是 network/auth 类**, 而 `_classify_error` 已算出 `network`/`auth_403`。一律塌缩后, 真正离线/鉴权失败的 remote 报 `has_unreachable_remote=false` + `reachable=true` ⇒ `handoff_autofill.py:54` 的「remote 不可达」告警也不会响。应映射: fetch 失败 kind ∈ {network, auth_403} → 沿用既有 network 类 reason; `not_refreshed` 仅用于「未尝试 / TTL 跳过 / opt-out 禁用」。 | code-reviewer |
| M-16 | **默认 enforced = 全部 remote + policy(a) ⇒ fork 工作流恒假红**: 任何配了 `upstream` (fork 源) 或只读镜像的仓库, 其 `upstream` 永远 behind/diverged ⇒ `overall_parity` 恒 false + 推荐恒亮 + 每 scan 多付一条网络腿。`DEFAULTS.json:10` 早有 `multi_remote.read_only_remotes` 概念, Spec 全文未提。 | code-reviewer + backend-architect |
| M-17 | **Rule #6 (不可协商) 未落 tasks**: 改 Skill 逻辑必须 `/skill-creator` benchmark + 存 `ab-results/`。tasks §9 无此项。**更糟**: `ab-suite/state-scanner.json:143` 的 rubric 明写 `"Should exclude parity: ahead and parity: unknown from overall_parity computation"` ⇒ D5(a) 会让 rubric **把正确的新行为判为错** (R-9 golden fixture 假绿的**高一层**同类缺陷)。 | knowledge-manager |
| M-18 | **Impact 漏 `sync_status.submodules[].drift` 行为变更**: F3′ 也 fetch 子模块 remote ⇒ `remote_commit`/`behind_count`/`hint`/`hint_type` 从陈旧变新鲜 ⇒ 直接改变 `git submodule update --remote` 类建议的触发 —— 而 **US-008 数据丢失护栏正在这条路径上** (memory `project_submodule_drift_direction`)。 | code-reviewer |
| M-19 | **性能数字被隐性放大为通用结论**: `+0.6s/+4%` 是**本机 / 10CG 内网 / CF Access** 单点数据, 但 Impact 表写成好像通用。aria-plugin 是**跨项目分发**的 (memory `project_kairos_adopter`), 外部采用者 remote 数量与网络条件可能远差。在 `fetch_all: false` opt-out 锁定前, 不能把 4% 当承诺写进 CHANGELOG。 | backend-architect + knowledge-manager |
| M-20 | **文档 SOT 链漏 ≥5 处**: `references/rules/basic-rules.md:78` (注释写死旧 OQ-1 语义, D5 后**直接错误**) / `RECOMMENDATION_RULES.md` (只改文案未改触发语义) / `config-loader/SKILL.md:79` / **`docs/architecture/system-architecture.md:892-895` (主仓 L1 架构文档, 且已 drift —— 记 `overall_parity` 为枚举, 代码发 bool)** / `state-snapshot-schema.md:490`。 | knowledge-manager + code-reviewer |

### R2 Minor 摘要

DEC §8 引的 R1 报告路径盘上不存在 (**本文件即修复**) / DEC §7.4 元教训与既有 memory `feedback_test_mock_pattern_hides_prod_bug` 重复 (应补强而非新建) / 性能数字缺采集条件 (host / 时刻 / 冷热 / SSH 复用) / tasks 9.8 跨仓落地流程半枚举 (漏 submodule pointer bump + 多远程推送) / 锚点行号 2 处漂移 (`phase-1-collectors.md:21`→`:34`; `_aggregate_flags` 371-415→371-418) / 跨进程同仓并发 fetch (多终端场景) 应写明是已知可接受降级 / `.aria/cache/coordination-fetch.json` 非原子写而 F3′ 后它承载裁决输入 / `validate_schema_doc.py` **会真跑 scan.py** ⇒ F3′ 后每次 schema 校验触发全量网络 fetch / DEC §6 的 #109 叙述可能已被 v1.56.0 (`coordination.enabled` 默认翻 true + B.0 REQUIRE claim) 改写。

---

## 收敛状态

**R1 → R2: 未收敛** (`conclusions_stable = false`)。

- R1 的 comparison_key 集合 **全部消失** (6/6 fixed, 3 位 R1 agent 独立确认) —— 药方换轴是**真实的机制修复**, 不是措辞让步。
- R2 产生**新的** comparison_key 集合 (3C + 20M 去重后), 集中在**新轴上的边界条件**。
- **五位一致认同轴正确, 不需要第三次换轴。** 两位 FAIL 的 agent 均明确表示「R3 可收敛」/「不需要回 brainstorm」。

**下一步**: v3 修订 (R2 的 3C + 20M) → post_spec R3 (5 agent)。

---

## 元教训 (候选入 memory)

1. **新鲜度不能测量, 只能获取。** 想用文件 mtime 之类的本地痕迹推断「数据有多新」, 在 git 里全部行不通 (FETCH_HEAD 全局 / ref mtime 仅值变时更新 / packed 后消失)。要知道远端状态, 只能去问远端。
2. **「修 bug 的部件」自己会造 bug。** 降级必须**只作用于正证据**, 不能碰负证据 —— 负证据即使来自陈旧数据也是**下界**, 依然为真 (v1-C3)。
3. **假绿的反面是恒红, 两者同样是零信息量。** 修复「恒绿真空」时极易过冲成「恒红疲劳」(R2-C1 / M-2)。判据: 该信号在**健康常态**下是什么值?
4. **同一份 snapshot 内部自相矛盾, 是 collector 编排缺陷的可靠指纹。**
5. **泛化一个机制前, 先找它自己的 Spec。** `coordination_fetch` 有归档 Spec #141 定义了 two-fetch 语义, 不读就泛化 ⇒ 恒红 (M-2)。
6. **被声明为 SOT 的实现/文档会 drift —— SOT 声明本身是一个需要定期核验的断言** (M-9: docstring 声称的 canonical SOT 已被后来的 AD 取代)。
7. **测试的 mock 姿势可以让缺陷结构上不可见**, 且事故 fixture 可能早就在测试里了, 只是没人断言那个会暴露矛盾的字段 (补强既有 memory `feedback_test_mock_pattern_hides_prod_bug`)。
