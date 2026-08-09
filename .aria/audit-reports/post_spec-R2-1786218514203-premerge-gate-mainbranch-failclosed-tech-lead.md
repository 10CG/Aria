---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T20:00:21.181Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 — tech-lead (架构与流程镜头)

## 审计结论

被审版本 = R1 后结构性重写版 (387 行)。本席按任务书要求把镜头压在**本轮新写的内容**上,
并对 §R1 审计吸收记录表的每一条「本版处置」去落点核实, 不采信自陈。

### 先说做对的部分 (已实读核验, 不是转述)

Spec 的**事实性引用精度很高**, 抽查全部命中:

- `pre_merge_gate.py` 三处 `main` 字面量 (`:21` / `:300` / `:427`) — 全仓 grep 确认恰好 3 处, 无遗漏;
- `SKILL.md:167` / `:243` 两处 `--branch main` — 确认, 且全仓 `aria/` 再无第三处;
- `SKILL.md:242` / `:252` / `:257-259` / `:267` / `:279` — 逐行核对, 内容与 Spec 描述一致;
- `ci_backends/aether.py:117-135` `query_branch_in_flight` 只在 aether 自身失败时抛 — 确认;
- `ci_backends/base.py:29` `not_found` 在 `CIStatus.state` Literal 内 — 确认;
- `tests/test_pre_merge_gate.py` `gate_check(` 调用点 **24 处, 显式传 `main_branch` 的 0 处** — 实测确认, C3 「逐字不改已证伪」成立;
- `test_sc12` 逐字断言 `main_branch="main"` (`:668-670`) — 确认必红;
- `test_sc22` patch 的是 `pc_module.subprocess` (`:718`) — 确认该卫生守卫看不到 gate 层新 subprocess;
- 本仓 `origin/HEAD` → `refs/remotes/origin/master` (rc=0), `github/HEAD` **不是 symbolic ref** (rc=128) — 实跑确认, §2 的 remote 绑定论证成立;
- `fetch_gate.py:55` `_DEFAULT_BRANCH_FALLBACKS = ("master", "main")`, 用于 `:124-127` — 确认「字面回落」指控属实;
- `run_gate` 确在 `state-scanner/scripts/phase1_gate.py` — SC-2 的更正准确;
- AB 套件 `phase-c-integrator-pre-merge-gate.json` 存在, `version 1.1.0`, 7 fixtures 名称逐字对上。

R1 的五个 Critical 里, **C1 / C3 / C4 / C5 的方向都改对了**。问题不在方向, 在本轮新写的执行细节。

### 但是: 承重条款在本轮定稿的形态下**仍然 fail-OPEN**

§5 自称「本 Spec 的承重条款」, SC-4 自称「本条是承重断言」。我实跑了它规定的命令:

```
# 构造: 仓里只有 feature/master, 没有 master
$ git ls-remote --exit-code --heads origin master
39c458f...  refs/heads/feature/master
rc=0                      ← 判「存在」
```

`git ls-remote` 的 pattern 按 **ref 尾段**匹配 (slash-separated tail)。裸分支名 `master` 会命中
`refs/heads/feature/master`。⇒ 在任何存在 `feature/main` / `release/main` / `backup/master` 这类
分支的仓上, 「主分支不存在」会被判成「存在」, 然后原封不动落回 `InFlightStatus(runs=[])` 的恒绿。
**这正是本 Spec 存在的理由那个形状。**

对照组 (同一临时仓):

```
$ git ls-remote --exit-code --heads origin refs/heads/master   → rc=2   ✅ 正确判「不存在」
$ git ls-remote --exit-code --heads origin refs/heads/main     → rc=0   ✅ 正确判「存在」
```

修法是一个字符串: pattern 用**全 ref** `refs/heads/<name>`。§5 表里的 exit-code 2 语义本身没错,
错在它钉在了一个会 fail-OPEN 的匹配器上 —— 而 R1-fix 新增的正是那张「exit 2 vs 其他非零」判据表
(D-F), 它给了这个匹配器一层权威外观, 反而更难被后续审计怀疑。SC-4 用普通 fixture 仓也测不出它。

### 三条自陈的裁定

任务书点名的三条自陈, 逐条实读代码后:

| 自陈 | 裁定 | 依据 |
|---|---|---|
| (a) §4 解析点同时满足两侧约束 | **基本成立**, 有一处措辞偏差 | 三个早退 `:328` / `:338` / `:344-352` 之前无任何 `main_branch` 消费者, 之后第一个消费者确是 path coverage — 结构上可满足。偏差见 m1 |
| (b) §7 `gate_error` 不撞消费点 | **不成立 (键名不撞, 但消费点建模错了)** | 见 M6 — `write_gate_state(verdict=)` 消费的根本不是 gate 的 verdict 词表 |
| (c) SC-10/SC-11 真能红 | **两条都不能红** | 见 M7 / M8 — SC-10 在唯一合规实现下等于既有绿测试; SC-11 断言的是 AI 散文义务, 无红窗 |

三条自陈里两条半不成立。这与本项目「fix 轮最易在新写内容里复发」的实证吻合: 我的 12 条 finding 里
**10 条 `introduced_by_r1fix: true`**。

---

## Findings

### C1 — 承重存在性核验用裸分支名, 按 ref 尾段匹配 ⇒ 在要治的病同一形状上 fail-OPEN

- **type**: issue | **severity**: critical | **category**: implementation
- **anchor**: `proposal.md §5` (:158 命令行) + `§D-F` (:239) + `SC-4` (:258)
- **introduced_by_r1fix**: false (命令行在 R1 原版 `git show HEAD:...` 第 93 行即已存在), 但 R1-fix 新增的 exit-code 判据表与 D-F 把它升格为权威判据而未复核匹配语义

Spec 声称怎么修的: 「查 in-flight **之前**, 独立核验该分支在 `<remote>` 上**存在**:
`git ls-remote --exit-code --heads <remote> <main_branch>`」, exit 2 = 不存在。

实际落点是什么: `git ls-remote` 的 refspec pattern 是**尾段匹配**, 不是精确匹配。实跑证据见
上文「审计结论」。⇒ 只要远端存在任一以同名尾段结尾的分支, 核验返回 rc=0 = 存在, 闸门继续走
`query_branch_in_flight(<不存在的分支>)`, 拿到空集判 green。

修法: pattern 改全 ref (`refs/heads/<main_branch>`), 已实测两方向都正确。同时 SC-4 需补一条
「远端存在 `feature/<name>` 但不存在 `<name>`」的 fixture, 否则这条 SC 对本缺陷天然失明。

---

### M1 — §8/D-I 的在场范围表漏掉第四个早退分支, 与它自己逐字引的契约冲突

- **type**: issue | **severity**: major | **category**: architecture
- **anchor**: `proposal.md §8` (:212-224) / `D-I` (:242) / `SC-12` (:267); 落点 `pre_merge_gate.py:369-376` 与 `:392-399`
- **introduced_by_r1fix**: true

§8 开头**逐字引用** `SKILL.md:279`: 「各早退分支 (no-backend / precheck 失败 / **backend query 失败** /
enabled:false) 保持六键不变」—— 四条。紧接着的在场范围表第一行只列了**三条**
(`enabled=false` / no-backend / precheck 失败), SC-12 同样只列三条。

`backend query 失败` 分支实存: `pre_merge_gate.py:369-376` (in-flight 查询 `AetherQueryError`) 与
`:392-399` (PR CI 查询), 两处都走 `_build_output(FAIL, ...)` 而**不是** `compute_verdict`。它们位于
解析点**之后**。按 D-I 的原则句「`main_branch_resolved` 只在解析之后的分支在场」, 实施者会给这两个
分支加上该键 ⇒ 直接违反 §8 自己引的六键契约。

而且 #122 对这条分支是**有测试的**: `test_pre_merge_gate.py:691-697` 明确断言
backend-query-failure 分支不带 `path_coverage` 键。同一位置的新键会与该先例语义分叉。

⇒ §8 的表不是全覆盖分区; 两个实现者会得到不同结果。

---

### M2 — §8 把六键契约的执行委派给一个**不执行它**的测试

- **type**: issue | **severity**: major | **category**: testing
- **anchor**: `proposal.md §8` (:214, :224); 落点 `tests/test_pre_merge_gate.py:598-605` / `:658-659` / `:689-690`
- **introduced_by_r1fix**: true

Spec 声称: 「`SKILL.md:279` 成文契约 ... **且有 `_OLD_KEYS` 守护测试**」, 并在 R1 依据里断言
「全分支在场则 `_OLD_KEYS` 守护测试**必红**」。

实际落点: `_OLD_KEYS` (`:598-605`) 只在两处被用到 ——

- `:658-659` `for key in self._OLD_KEYS: assertEqual(covered_out[key], disabled_out[key])` — 两输出**逐键值相等**;
- `:689-690` `for key in self._OLD_KEYS: assertIn(key, out)` — **存在性**。

两处都不是 exhaustive key-set 断言。**给输出加一个新键, 两处都照绿。** 所以「必红」是错的,
六键契约今天没有任何机械守护。Spec 据此推出「只能选一种解读」的论证链因此断裂 —— 更要紧的是,
它让 Phase B 以为契约有兜底, 于是不会去补真正的 exhaustive 断言。

(SC-12 若新写成 exhaustive 断言, 是能红的 —— 但那是新建守卫, 不是「已有守卫」。Spec 必须说清是哪一种。)

---

### M3 — §5 把非 timeout 的确定性失败也路由进 §6 重试, 超出所引规范的确切触发条件

- **type**: issue | **severity**: major | **category**: architecture
- **anchor**: `proposal.md §5 表第三行` (:165) 与 `§6` (:173-179) / `D-G` (:240); 落点 `SKILL.md:259`
- **introduced_by_r1fix**: true

§6 引的规范原文 (`SKILL.md:259`) 逐字是: 「**timeout 触发** → max 3 attempts retry (backoff
5s/15s/45s) → 仍**超时**则 `fail` verdict」—— 触发条件与终止条件**都**是 timeout。

§5 表第三行写「其他非零 / timeout → 按 §6 重试」。把确定性非零退出 (典型: remote 名不对
`fatal: 'xxx' does not appear to be a git repository`, rc=128; 或鉴权失败) 塞进 timeout 专用的
退避链, 后果是每次调用白等 5+15+45 = 65s 后给出与第一次完全相同的结论。这既不是所引规范说的事,
也让 D-G「复用既有规范不新造参数」变成「扩大既有规范的适用面」——那等于新造了一条规则, 只是没写下来。

处方: §5 第三行按**可重试性**再分一层 (timeout / 传输类瞬时失败 → §6 重试; 确定性非零 → 立即
`main-branch-verify-failed`, 不重试), 或显式在 §6 声明本 Spec 扩展了 `SKILL.md:259` 的触发条件并
同步改那一行。

---

### M4 — D-B 与 D-C 相互矛盾: D-C 用来否决方案的「恒红」判据, D-B 自己踩上了

- **type**: risk | **severity**: major | **category**: architecture
- **anchor**: `proposal.md D-B` (:235) / `D-C` (:236) / `§3 m6 注记` (:125) / `§5 表第三行` (:165)
- **introduced_by_r1fix**: true (R1 原版无 `--remote` 参数, 也无 ls-remote --symref 权威路径)

D-C 的论证是: 只用本地 `refs/remotes/<remote>/HEAD` 快路径不行, 因为「Layer 2 容器里脚本化
checkout 的仓可能根本没有这个 ref ⇒ 只用快路径会让 D2 在**健康常态下**恒 abort = 恒红, 与假绿
同样是零信息量」。这条判据本身很对。

D-B 让 `remote` 取字面缺省 `origin`, 判据只用了一条:「猜错会不会被发现」。但同一个 Layer 2
容器场景下, remote 名不是 `origin` 的仓 (脚本化 checkout / 多远程 / mirror-only) 会让
`ls-remote origin ...` **确定性**失败 → 走 §5 第三行 → 每次 `verdict=fail`。**这就是 D-C 刚刚用来
否决另一个方案的恒红**, 而 D-B 从未按这条判据被复核。

不对称还体现在: `main_branch` 被要求「必须解析, 禁止字面缺省」, 而 `remote` 连一次解析尝试都没有
—— 明明有现成信号 (`git remote` 只有一个远程时唯一解, 或 `git config branch.<cur>.remote`)。

至少需要: D-B 补一句按「健康常态下会不会恒红」的复核结论 + `remote` 解析不出时的行为 (是 fail
还是取唯一远程), 并在 SC 里给一条「remote 名不是 origin」的场景。

---

### M5 — §7 的 `gate_error` schema 没有 `message` 键, 但 §5 / SC-4 把 message 当承重断言

- **type**: issue | **severity**: major | **category**: implementation
- **anchor**: `proposal.md §7` (:203-209) vs `§5 表第二行` (:164) 与 `SC-4` (:258)
- **introduced_by_r1fix**: true (`gate_error` 整体是本轮新增, R1 原版是 `verdict=error`)

§7 钉死的 schema 是三键: `kind` / `remote` / `attempted`。

§5 表第二行要求「`verdict=fail` + `gate_error.kind="main-branch-not-found"`, **message 须点明**
「主分支 `<name>` 在 remote `<remote>` 上不存在 —— 这不是『无 in-flight run』」」;
SC-4 (自称承重断言) 要求「**message** 含分支名与 remote 名且明确区别于『无 in-flight run』」。

「message」在本 Spec 里**没有绑定**: 可能是既有的 `raw_message`, 也可能是一个 §7 没声明的
`gate_error.message`。两个实现者会分别落在两处, 而 SC-4 的断言会跟着分叉。§What Changes 开篇自设
的判据是「两个独立实现者读本节应得**同一结果**」—— 这条在本 Spec 唯一的承重断言上没达成。

(附带: 若实施者只写 `gate_error` 而 `raw_message` 留空, 则该诊断在下游 `gate_state` 持久化里
**完全消失** —— 见 M6, `write_gate_state` 只收 `raw_message`, 不收 `gate_error`。)

---

### M6 — §7 对 `gate_state_helper` 这个消费点建模错了, SC-8 因此不成立

- **type**: issue | **severity**: major | **category**: testing
- **anchor**: `proposal.md §7 表第 4/5 行` (:194-195) 与 `SC-8` (:263); 落点
  `workflow-runner/scripts/gate_state_helper.py:32-34` `:115-155`,
  `workflow-runner/references/workflow-state-schema.md:39-40`, `workflow-runner/SKILL.md:341-344`
- **introduced_by_r1fix**: true

§7 表把 `write_gate_state()` 当成「直接吃 gate verdict 的消费点」, 论证「`:147` `"status": verdict`
原样写入无校验 ⇒ 下游 `== GATE_STATUS_*` 全不匹配」。

实读三处落点后, 这个建模不对:

- `gate_state_helper.py:32-34`: `GATE_STATUS_WAITING = "waiting"` —— 是 **`waiting`**, 不是 gate 的 `wait`;
- `workflow-state-schema.md:39-40`: `"status": "string (waiting | green | fail)"`;
- `workflow-runner/SKILL.md:324` 写 gate 返回 `verdict: "wait"`, 而 `:344` 写落盘时 `status: "waiting"`
  —— **翻译发生在 workflow-runner 路由层**, 不在 helper 里;
- `tests/test_gate_state_helper.py` 全程传 `verdict="waiting"`, 从不传 `"wait"`。

⇒ 那个形参叫 `verdict`, 消费的却是 **gate_state status 词表**。两套词表本来就不同。

后果落在 SC-8: 「`write_gate_state()` 接受该 verdict 不产生未知 status」——

- 若逐字实现 (把 gate 的三态 verdict 喂进去断言 status 已知), 会因**既有的** `wait` 而红,
  红的原因与本 Spec 无关, 是一条不能用的验收条件;
- 若只喂 `fail`, 那 `fail` 本来就被接受, 什么也没测。

SC-8 想守的东西 (verdict 三态封闭) 其实只需在 gate 侧断言, 根本不必牵扯 `write_gate_state`。
建议 SC-8 拆成「gate 输出 verdict ∈ 三态」+ 把 workflow-runner 词表差异写进 §Impact 的已知不同步面
(它现在只列了 `main_branch_resolved`, 没列 `gate_error`, 也没列这个既有词表落差)。

---

### M7 — SC-10 在唯一满足本 Spec 自设卫生要求的实现下**不能红**

- **type**: issue | **severity**: major | **category**: testing
- **anchor**: `proposal.md SC-10` (:265) 与 `§Impact 既有测试小节` (:342-344); 落点
  `tests/test_pre_merge_gate.py:59-88` (mixin) / `:634-645` (既有 `test_sc10`) / `:710-724` (`test_sc22`)
- **introduced_by_r1fix**: true

SC-10 的红窗声明是: 「现状 `main` ⇒ `git diff` RC=128 ⇒ 恒 `unknown` ⇒ 必红」。这要求
`evaluate_path_coverage` **真跑 git**。

但 `_ProbeCacheResetMixin.setUp()` (`:68-76`) 对**每一个**用到该 mixin 的测试类都
`mock.patch.object(gate, "evaluate_path_coverage", ...)`, 这是 #122 立下的隔离方法论 (注释 `:62-64`
写明目的就是「不触发真实 git 子进程」)。两条路都走不通:

- **打桩实现**: 桩直接返回 `not_applicable`, 于是断言 `decision == "not_applicable"` +
  `query_pr_ci.assert_not_called()` —— 这**逐字等于**既有的
  `test_sc10_not_applicable_clean_green_with_message` (`:634-645`), 而那条**今天就是绿的**。零信息;
- **不打桩实现**: 需要真 git 子进程 + 真 workflow fixture 仓, 与 §Impact 自己要求「把 `test_sc22`
  的卫生断言扩到 patch `pre_merge_gate` 模块自己的 `subprocess`」直接冲突 —— 同一个 Spec 一边加强
  「零真实 git 子进程」守卫, 一边要求一条依赖真实 git 的 SC。

⇒ SC-10 的「怎么会红」列在任一合规实现下都不成立。若要保留这条 SC, 必须指定第三条路
(例: 用 `tempfile` 建一个真 git fixture 仓并把该测试**移出** mixin 作用域, 同时在 `test_sc22`
的卫生断言里显式豁免它并说明豁免边界)。

---

### M8 — SC-11 无可证伪的红窗 (断言的是 AI 散文义务, 单测测不到, AB 套件自陈覆盖不到)

- **type**: issue | **severity**: major | **category**: testing
- **anchor**: `proposal.md SC-11` (:266) 与 `§Rule #6 已知缺口` (:287); 落点 `SKILL.md:253`
- **introduced_by_r1fix**: true

SC-11 要验「AI surface 义务照常触发 (`SKILL.md:252` (a) 项警告行)」, 红窗写「若实现让它触发不到则红」。

- 这条义务的执行者是**读 SKILL.md 的 AI**, 不是 `pre_merge_gate.py`。代码里没有任何东西产出那行警告,
  单测无从断言;
- Spec 自己在 §Rule #6 里承认「两套件均覆盖不到 C.2.4 的 D9 surface 措辞」—— AB 侧也测不到;
- 若退化成断言 `raw_message` 非空, 那又是既有 `test_sc10` (`:641-643`) 已经在做的事, 今天就绿。

⇒ 恒绿的验收条件与恒红同样是零信息量。要么给出真实测量手段 (定向 AB fixture / dogfood 留证),
要么把它降格为「观察项」并明说本 Spec 不验它 —— 不要让它以 SC 的身份进验收表。

(附: 锚点也偏了一行, 见 m3。)

---

### M9 — Rule #6 改判后的 ship 路径建立在未核验的前提上, 且第三行的配套义务缺两项

- **type**: issue | **severity**: major | **category**: architecture
- **anchor**: `proposal.md §Rule #6` (:273-287) / `D-L` (:245) / `§Impact AB 行` (:330)
- **introduced_by_r1fix**: true (整节是本轮改判新写)

先声明立场: owner 已裁定「照跑 AB」, 本条**不是**建议跳过或降级 (Rule #10)。问题在于这条 ship 路径
**是否可执行**, 以及归入判据表哪一行的证据是否成立。实测三点:

1. **`phase-c-integrator-pre-merge-gate.json` 不是 AB eval 套件。** 它没有 `prompt`, 没有
   with/without 臂; 每个 fixture 的字段是 `expected_verdict` + `test_case_in_unit_tests`
   (指向 `test_pre_merge_gate.py` 的方法名), 顶层 `type = "workflow_skill_subextension"`。
   它唯一的归档结果 `ab-results/2026-05-10-phase-c-integrator-pre-merge-gate/benchmark.json`
   里逐字写着 `"type": "structural_verification"`, `verified_by` 指向单测方法。
   —— 这恰恰是判据表**第一行**说的 substitute 形态, 不是 AB。`AB_TEST_OPERATIONS.md` 全文不含
   `workflow_skill_subextension`, 没有它的执行程序。「ship 前须过」这个套件, Phase B 无法执行。
2. **`phase-c-integrator.json` 的 3 个 eval 与 C.2.4 无关。** 实读: `commit-generation` (C.1) /
   `merge-conflict-handling` (C.2) / `multi-remote-merge-push` (C.2.5)。**没有一个触及 pre-merge gate**。
   本变更改的是 `SKILL.md:243` 的 C.2.4 指令行, AB 三臂的答案不会因此系统性移动。
3. **引为「结论相反」的 #122 先例, 实际只跑了 `phase-c-integrator.json`。**
   `ab-results/2026-07-31-v1.65.0-122-rule6/` 只有 `eval-1/2/3` 三组 with/without/old 臂,
   `grading-summary.md` 标题即「phase-c-integrator AB Benchmark 评分报告 ... suite: 1.1.0」。
   #122 改的正是 pre-merge gate, 也没跑 fixture 套件。

⇒ §Rule #6 证据 #1 把一个 structural_verification fixture 注册表描述成「专属 AB 套件」, 并据此推出
「落判据表**第二行** (能 AB 测得到 → 照跑 AB)」。**「能测得到」这条腿对本变更不成立** —— 按 CLAUDE.md
Rule #6 表, 处方性但**套件覆盖外**落**第三行**, 其义务是三项:「点名行为 + 建可证伪定向 fixture +
套件缺口开 issue (**缺一照跑**)」。本 Spec 只做了第三项的一半 (「记录于此, 不自行扩套件」),
点名行为与定向 fixture 都没有。

处置建议 (不改 owner 裁定): 照跑 AB 保留; 同时补齐第三行的两项义务, 并把「过
`phase-c-integrator-pre-merge-gate.json`」改写成它真实的形态 (structural 留证 / 单测 fixture 对齐),
否则 Phase B 会拿着一条没有执行程序的 ship 条件。

---

### M10 — SC 编号与同文件既有 #122 测试命名空间正面冲突, 同一文档里 SC-12 指两件事

- **type**: issue | **severity**: major | **category**: documentation
- **anchor**: `proposal.md §Success Criteria` (:249-269) 与 `§Impact` (:327, :340); 落点
  `tests/test_pre_merge_gate.py:623/634/647/663/672/683/699/710` + `pre_merge_gate.py:379`
- **introduced_by_r1fix**: true (原版 7 条 SC, 未进 9-12 号段)

`test_pre_merge_gate.py` 里已经有 `test_sc9_ / test_sc10_ / test_sc11_ / test_sc12_ / test_sc13_ /
test_sc15_ / test_sc21_ / test_sc22_` 八条 #122 的测试; 生产代码注释也在引它们
(`pre_merge_gate.py:379` 逐字写着「SC-9/10 assert_not_called」)。

本 Spec 的 SC-10 / SC-11 / SC-12 语义与同名既有测试**完全不同**, 而 §Impact 指示
「`test_pre_merge_gate.py` | 扩展 SC-1..SC-12」——**写进同一个文件**。同一份 §Impact 里,
`:340` 又用「`test_sc12` 逐字断言 ...」指 #122 的那条。⇒ 「SC-12」在本文档内指两件事,
实施者极可能覆盖或误改。

处方: 本 Spec 的 SC 全部加前缀命名空间 (例 `test_mb1_`..`test_mb12_` 或 `SC-137-1`..), 并在
§Impact 里显式区分「本 Spec SC-n」与「#122 test_scn」。

---

### M11 — R1 吸收表 C2 行自陈「§Impact + **SC**」, 但没有任何 SC 覆盖那三处字面量

- **type**: issue | **severity**: major | **category**: documentation
- **anchor**: `proposal.md §R1 审计吸收记录 C2 行` (:367) vs `§Success Criteria` 全表 (:253-267)
- **introduced_by_r1fix**: true

自陈原文: 「C2 `SKILL.md:243`/`:167` 字面量未枚举, 只改 `:242` | **§Impact + SC** (Impact 表已列三处)」。

去落点核实: SC-1..SC-12 **无一条**断言 `SKILL.md:167` / `:243` 的 `--branch main` 已被改掉。SC-6 引
`SKILL.md:257-259` 只是在借用重试规范; SC-11 引 `:252` 是在讲 surface 义务。C2 在 R1 是 **Critical**,
它现在的全部落地就是 §Impact 表里的一行 doc 变更描述, **零验证腿**。

这正是本项目反复标记的形状: 一个 Critical 的闭环只剩文档描述。文档字面量是可以机械验的
(`grep -c -- "--branch main" SKILL.md` 应为 0 / 或断言那两行改述后不含裸 `main`), 成本近似为零。
建议补一条机械 SC, 否则 C2 的闭环无法在 Phase B 被证伪。

---

### m1 — §4 伪代码把条件调用画成无条件, 且行号偏 2 行; `path_coverage_enabled=false` 分支未讨论

- **type**: issue | **severity**: minor | **category**: documentation
- **anchor**: `proposal.md §4` (:145) 与 `§Why` (:68); 落点 `pre_merge_gate.py:356-360`
- **introduced_by_r1fix**: true (§4 是本轮新写)

实际代码是 `:356 pc = None` → `:357 if cfg.get("path_coverage_enabled", True):` → `:358 pc = evaluate_path_coverage(`。
Spec 两处都标 `:356` 且画成无条件调用。对「解析点必须在它之前」的结论无影响, 但 §4 的第二条理由
(「`None` 会流进 path coverage 拼出 `"None...pr-branch"`」) 在 `path_coverage_enabled=false` 时不成立
—— 此时唯一约束只剩 in-flight 查询。§4 应说明该配置下约束退化后解析点是否仍钉在原处 (我认为应该,
但 Spec 没写, 实施者可能据「唯一理由不成立」而移位)。

---

### m2 — §Why 的 fail-CLOSED 判据归属指向一个不存在的 standards 文档

- **type**: issue | **severity**: minor | **category**: documentation
- **anchor**: `proposal.md §Why` (:50) 与 `§引用卫生` (:291-295)
- **introduced_by_r1fix**: true

R1 M7 指出原版用容器本地 memory 名作承重引用。本版改成「判据见 `standards/conventions/` 的
fail-CLOSED 原则」。实测 `standards/conventions/` **没有** fail-CLOSED 原则文档 —— 该词只在
`configured-gate-authority.md:29` / `skill-benchmark-exemption.md:24` / `shell-jq-crlf-hygiene.md`
的其他语境出现, 都不是 Spec 引的那条判据。

⇒ 悬空引用换了个位置。好在 §引用卫生 承诺的「就地写出判据本体」这一半做到了 (判据句确实写在
`:50` 行内), 所以只是**归属**失效, 论证本身仍自足。建议删掉那半句归属, 或指向真实存在的锚点。

---

### m3 — SC-11 锚点 `SKILL.md:252` 指的是段标题行, 义务文在 `:253`

- **type**: issue | **severity**: minor | **category**: documentation
- **anchor**: `proposal.md SC-11` (:266); 落点 `SKILL.md:252` = 「6. **路由决策**:」, `:253` = green 分支含 (a) 项 surface 义务
- **introduced_by_r1fix**: true

同文档其他锚点 (`:242` `:243` `:257-259` `:267` `:279`) 都精确, 唯此处差一行。§7 表里的
`SKILL.md:252-255` 作为「路由决策三分支」的范围引用是对的; SC-11 引单行时应写 `:253`。

---

## Verdict

**FAIL** — 1 Critical + 11 Major + 3 minor。

Critical 单独就足以 FAIL: 本 Spec 的承重条款 (§5 + SC-4) 在其定稿的命令形态下, 于「远端存在同尾段
分支」这一并不罕见的配置上仍然 fail-OPEN, 落回它自己 §Why 描述的那个恒绿。修法只需把 pattern
换成全 ref, 但必须改, 且 SC-4 要补对应 fixture。

11 条 Major 里 **10 条 `introduced_by_r1fix: true`**, 集中在三簇:

- **验收面 (M6/M7/M8/M10/M11)** — 12 条 SC 里有 3 条 (SC-8/10/11) 在任一合规实现下都不能红, 1 个
  Critical (C2) 完全没有 SC 覆盖, 编号还与同文件既有测试撞车。验收表的**表面积**扩大了 (7→12),
  **判别力**没有同步扩大。
- **契约面 (M1/M2/M5)** — 新写的 §7/§8 一边逐字引用既有契约, 一边给出与之不兼容的分区; 并把执行
  委派给一个实测不执行该契约的守卫。
- **决策自洽面 (M3/M4/M9)** — D-B 踩了 D-C 用来否决方案的同一判据; D-G 悄悄扩大了所引规范的触发
  条件; D-L 的 ship 路径建立在对两个套件性质的误判上。

**给 R3 的判据建议**: 本轮 major 主要不是「R1 清单没划掉」, 而是新写内容的**内部一致性与可证伪性**。
下一轮 fix 应优先做**条款间交叉一致性检查** (每条决策单独看都对, 但 A 是否违反 B 的隐含前提), 以及
对每条 SC 逐条回答「它今天怎么会红、明天改坏了怎么会红」—— 这两项恰是本轮 10/11 条 major 的来源。

## 轮次记录

| 轮次 | 席位 | verdict | C / M / m | 说明 |
|---|---|---|---|---|
| R1 | tech-lead / backend-architect / qa-engineer / code-reviewer / knowledge-manager (5 席) | FAIL (5/5 REVISE) | 5C + 10M + 6m = 21 | 汇总见 `.aria/audit-reports/post_spec-R1-1786216818583-...-aggregate.md`; owner 裁定结构性重写四节 |
| R2 | tech-lead (本席) | FAIL | 1C + 11M + 3m = 15 | 审重写后当前版本。R1 五个 Critical 的**方向**均已改对 (C1/C3/C4/C5 实读确认), 但 10/11 条 major 由本轮 fix 新引入; 承重条款的命令形态仍 fail-OPEN (C1, 实跑证据) |

**收敛性判断**: 未收敛。按本项目判据 (major 数是否还在降 / 本轮 fix 引入的 major 占比),
本轮 `introduced_by_r1fix` 占 major 的 **10/11 ≈ 91%** —— 已过「加轮边际产出转负」的拐点信号线。
建议 R3 **换新鲜眼睛**而非单纯加轮, 且把镜头显式定为「条款间交叉一致性」+「每条 SC 的红窗实证」。
