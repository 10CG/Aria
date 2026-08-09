---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-09T12:27:57.283Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 — tech-lead 席位报告

**被审对象**: `openspec/changes/premerge-gate-mainbranch-failclosed/tasks.md` (69 行) + `detailed-tasks.yaml` (19 条 / 378 行)
**参照物**: 同目录 `proposal.md` (已 owner override 放行, 不重审)

---

## 审计结论

19 条任务对 proposal §What Changes / §Impact 的**覆盖面基本完整** (逐行映射见 §附录 A, 无遗漏面、无越出 proposal 的新功能), DAG 依赖闭合, 分组 (TDD 前置 / 实现 / SKILL.md / 合规 / follow-up) 的组织意图成立。A.2 在若干处**比 proposal 更准确** (补了 SC-13、把 SC-10 覆盖不到的两条早退单列、点名 `:240` 的 `aether --help` 不被任何 SC pattern 命中)。

但本轮抓到 **1 Critical + 9 Major + 5 Minor**。Critical 的形状与本项目反复复发的那类完全一致 —— **承重断言测的量与错误的量不是同一个维度** (memory `invariant-dimension` / `redfix-change-quantity`)。

### 本席位实做的核验 (全部为只读, 未改任何文件)

| 核验对象 | 结果 |
|---|---|
| `SKILL.md` `:99` `:101/:216` yaml 围栏 / `:167` `:168` / `:189-191` / `:218` / `:240` / `:242` / `:252-255` / `:259` / `:262` / `:267` / `:270` / `:279` / `:559` / `:610` | 全部实读, 行号准确 |
| `pre_merge_gate.py` `:21` `:300` `:328` `:338` `:344-345` `:356-358` `:366` `:427` `:435` | 全部实读, 行号准确 |
| `path_coverage.py:78-94` (`_run_git` + 三合一 except) | 实读 |
| `ci_backends/aether.py:38` `:164-187` `:189-199` / `base.py:29` `:112` | 实读 |
| `tests/test_pre_merge_gate.py` `:663` `:683` `:710-724`; 24 处 `gate_check(` (多行感知计数, 显式传 `main_branch` = 0) | 实测 |
| 三文件全量 pytest | **111 passed** (与 proposal §测试基线一致) |
| SC-1..SC-5 今日实测 | 4 / 1 / 0 / 1·1·1 / 1 — 与 proposal SC 表「今日实测」列**逐条一致** |
| `commit 7661e96` 是否同提交同步 Rule #8 | ✅ 属实 (主仓, `CLAUDE.md 24 +-` + `aria` gitlink + AB fixture) |
| `ab-suite/phase-c-integrator.json` / `-pre-merge-gate.json` | ✅ 两文件均存在 |
| `standards/openspec/project.md:21` vs `:118` | ✅ 确实不一致 (双层 vs 单层) |
| `.aria/config.json` → `audit.checkpoints.post_planning` | ✅ `"convergence"`, teams 5 席 |
| Forgejo Aria #177 | ✅ open, 标题与引用一致 |
| `CLAUDE_PLUGIN_ROOT` 66 处 / `ARIA_PLUGIN_ROOT` 5 处 | ✅ 计数属实 — **但归属被误引, 见 M-2** |

---

## Critical

### C-1 — 承重断言 SC-3 测的是 `--pr-branch`, 而本 Spec 治的病在 `--main-branch`

**锚点**: `detailed-tasks.yaml:234` (TASK-011 verification #2) / `tasks.md:46` / `proposal.md:198` (SC-3)

TASK-011 是 D1 承重任务, 其全部验收是 4 条:
1. SC-1 `grep -c 'aether ci status'` 由 4→0
2. SC-3 `grep -c -- '--pr-branch'` 由 0→2
3. 折叠块补核验步
4. 去掉全部可执行命令字面量 (含 `:240`)

**这组断言对新写入的两条 helper 调用里 `--main-branch` 取什么值、乃至它在不在, 完全失明。** 受控实测 (本席位实跑):

```
一行 `python3 .../pre_merge_gate.py --pr-branch <PR> --main-branch main`
  → SC-1 命中 0 / SC-2 命中 0 / SC-3 命中 1
两条这样的行 → SC-1=0 ✅  SC-2=0 ✅  SC-3=2 ✅  全部通过
```

于是三种都能过闸的写法, 后果各不相同:

| TASK-011 可能写出的调用 | SC 判定 | 真实后果 |
|---|---|---|
| `--pr-branch <PR>` (漏 `--main-branch`) | **全绿** | TASK-006 已把该参数改必填 ⇒ argparse 直接报 `the following arguments are required` ⇒ **本仓与所有采用方恒红** |
| `--pr-branch <PR> --main-branch main` | **全绿** | 本仓 main 分支叫 `master` ⇒ 新增的存在性核验必判 `main-branch-not-found` ⇒ **本仓每次合并被 BLOCK (恒红)** |
| `--pr-branch <PR> --main-branch master` | **全绿** | 第三方采用方 (main 叫 `main`) ⇒ **对方恒红** |

这正是 R5 已经在**路径**那条腿上抓过一次的形状 (`proposal.md:62` 逐字「把假绿换成了对所有第三方采用方的恒红」)。A.2 为路径那条腿建了 spike + SC-12 双向验收, 却**没有对同一条调用里的分支名参数做同样处理** —— 而分支名恰是本 Spec 的病灶本体。

加重项 (三条独立):
- `.aria/config.json` 的 `phase_c_integrator.pre_merge_gate` **没有 `main_branch` 键** (本席位实查), 且 `main()` 只从 CLI 取值 ⇒ 该值**唯一来源就是 SKILL.md 里这条字面量**, 没有兜底。
- `proposal.md:34` 逐字「把字面量换成占位符也是同一个假绿」—— 该判断在旧世界 (helper 有 `default="main"` 且无存在性核验) 成立, 在本 Spec 落地后**已失效** (占位符 + 必填 + 存在性核验 = fail-CLOSED, 是正解)。这句陈旧断言会把实施者从正确答案 (占位符) 推向错误答案 (硬编码)。
- `proposal.md:58` 同时要求「必须给出一条**可直接执行的** helper 调用」, 与占位符方向相悖。

**处方 (给 A.2, 非本席位执行)**: TASK-011 增一条可证伪断言, 钉住「两条调用各含 `--main-branch`, 且其取值形态是 spike 定稿的占位符/解析形态而非 `main`/`master` 任一字面量」—— 例如 `grep -c -- '--main-branch' SKILL.md == 2` **且** `grep -cE -- '--main-branch (main|master)\b' SKILL.md == 0`。两条一起才既防漏写又防硬编码 (单独任一条都留半边)。

---

## Major

### M-1 — SC-12 挂在 spike 上, 真正 ship 的那条调用从未跨四 cwd 复跑

**锚点**: `detailed-tasks.yaml:61` (TASK-002 verification #1) vs `:232-236` (TASK-011 verification 全集)

SC-12「参数化四种 cwd 跑 §1 的调用」被 TASK-002 (spike) 独家认领。但**写进 SKILL.md 的那条调用是 TASK-011 产出的**, 而 TASK-011 的 verification 里没有 SC-12。DAG 上 TASK-011 依赖 TASK-002, 之后**没有任何任务回头对落地文本复跑四-cwd**。⇒ SC-12 验证的是 spike 草稿, 不是交付物。与 C-1 叠加时后果放大 (spike 结论正确, 抄进 SKILL.md 时走样, 无人发现)。

### M-2 — TASK-002 的 spike 输入把 `${ARIA_PLUGIN_ROOT}` 误标成 `${CLAUDE_PLUGIN_ROOT}`

**锚点**: `detailed-tasks.yaml:63` (TASK-002 verification #3); 源头 `proposal.md:64`

任务原文: 「须核 CLAUDE_PLUGIN_ROOT (仓内 66 处引用) 与 SKILL.md:262/:559/:610 的既有约定是否可直接沿用」; proposal 更直白: 「`SKILL.md:262` / `:559` / `:610` **均用它**」。

本席位逐行实读该三行:

```
262: **Helper 实现**: `${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/pre_merge_gate.py`
559: **Helper 实现**: `${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/submodule_gate.sh`
610: **降级策略**: 检测 `test -f "${ARIA_PLUGIN_ROOT:-aria}/skills/git-remote-helper/SKILL.md"`
```

**三处全是 `ARIA_PLUGIN_ROOT`, 零处 `CLAUDE_PLUGIN_ROOT`** (该文件里 `CLAUDE_PLUGIN_ROOT` 仅 `:737` 一处, 属 aria-token-telemetry)。全仓 `ARIA_PLUGIN_ROOT` 只有 5 处, 其中 3 处就是这三行, 另 2 处是 CHANGELOG 与 `state-scanner/references/sync-detection.md:587`。

⇒ 「66 处的仓内约定」与「这三行的既有约定」是**两套不同的东西**, 任务把它们并置成一件事。实施者据此得出「沿用 :262 的写法 = 用 CLAUDE_PLUGIN_ROOT」就会同时踩中 TASK-014 禁止的「互斥两套并存」。属 memory `delegate-verify` 同形: 引一行说「X 本就是这个约定」前须去 X 核字面。

### M-3 — TASK-014 的作用面越出 §Impact, 且 `:610` 是行为承载行

**锚点**: `detailed-tasks.yaml:288` (TASK-014 verification) / `proposal.md:245-253` (§Impact 表)

TASK-014 要求 `:262` / `:559` / `:610` 与 TASK-002 定稿**全文一致**。但:
- `:559` 是 `submodule_gate.sh` 的定位行, `:610` 是 `git-remote-helper` 的定位行 —— 两个**与本 Spec 无关的 helper**;
- `:610` 的 `test -f "${...}/skills/git-remote-helper/SKILL.md"` 是**降级策略的实际探测**, 改变量名 = 改变探哪个路径 = 改变多远程推送的降级行为;
- proposal §Impact 的 SKILL.md 行只列了「两处散文 · 四行裸命令 · `:270` · `:267` · `:279` · 步骤 6」, **不含 `:262/:559/:610`**; §非目标也没排除它们。

⇒ 一条被写成「一致性核对」的任务, 实际授权了两个 Spec 外 helper 的行为面改动, 且无任何测试/AB 覆盖那两条路径。要么把 `:559/:610` 移出本 Spec (开 follow-up), 要么补进 §Impact 并配验收。

### M-4 — TASK-004 的「⛔ 不得再造」与 §非目标 + backend 抽象边界三者互斥

**锚点**: `detailed-tasks.yaml:105` (TASK-004 verification #4) / `proposal.md:126` / `proposal.md:231` (§非目标「不改 path_coverage.py 代码与行为」)

任务点名两个「不得再造」的先例, 本席位读了两处源码:

- `ci_backends/aether.py:164` `def _run_with_retry(self, args)` —— 是 **`AetherBackend` 的私有实例方法**, 第 174 行写死 `[self.binary] + args`, 跑的是 **aether 二进制不是 git**。新核验要跑 `git ls-remote`, 结构上**无法复用**; 即便强行复用, gate 层直接调具体 backend 私有方法会破坏 v1.31.0 建立的 backend 抽象 (gate 必须对 GHA stub 等同样成立, 而分支存在性核验与 CI backend 无关)。
- `path_coverage.py:78` `_run_git(args, cwd)` —— 有 `(TimeoutExpired, FileNotFoundError, OSError)` 三合一, **但没有重试**; 且它把三类异常压成同一个 `err_summary` 字符串 (`:94`), 而 §5 退出码表要求**把 TimeoutExpired 与其余区分开**(前者重试后者不重试) ⇒ 复用它就得靠字符串嗅探 `"TimeoutExpired:"` 前缀来还原类型, 这本身是 fail-OPEN 易发构造。要把它改成可复用又被 §非目标逐字禁止。

⇒ 约束集的唯一可满足解是任务自己留的逃生口「新写一份 + 显式论证」, 那 `⛔ 不得再造` 就是装饰性的。更实质的缺口: **若 spike 结论真是「抽取共享 util」, §Impact 与所有任务的 deliverables 里都没有 `aether.py` / `path_coverage.py` / 新 util 文件的落点**, 实施者无处安放。

### M-5 — TASK-007 的第一条验收是转写漂移, 且结构上不可证伪

**锚点**: `detailed-tasks.yaml:161` vs `proposal.md:132`

- proposal §5「已知残留限制」逐字: 「本 Spec 只保证核验与 in-flight 查询使用**同一个 `main_branch` 值**且**同一个 cwd**」
- TASK-007 verification #1 写成: 「核验与 in-flight 查询使用**同一个 remote 值**与同一个 cwd」

`main_branch` 被换成了 `remote`。而 `ci_backends/base.py:112` / `aether.py:117` 的签名都是 `query_branch_in_flight(self, branch: str)` —— **无 remote 形参、无 cwd 形参**, 全文件 grep `remote|cwd` 零命中 (subprocess 继承进程 cwd)。⇒ 「同一个 remote 值」在 in-flight 侧根本没有对应量, 该断言不存在能让它变红的实现; 「同一个 cwd」则因两边都继承进程 cwd 而恒真。

这条恰是 `.aria/config.json` 里 post_planning 开启理由所记的那类 (「per-artifact transcription drift」)。

### M-6 — TASK-010 的「全量 111 tests 绿」在其执行点不可达, 且 111 是变更前基线

**锚点**: `detailed-tasks.yaml:218` (TASK-010 verification #3)

- TASK-001 (dep 链最前) 已把 SC-1 / SC-3 两条**针对 SKILL.md** 的断言注入同一套件 (deliverable 同为 `tests/test_pre_merge_gate.py`), 它们要到 TG-2 的 TASK-011 才能转绿;
- TASK-010 在 TG-1, 依赖仅 `[TASK-006]`, 位于 TASK-011 之前 ⇒ 执行 TASK-010 时 SC-1/SC-3 必然是红的, 「全量绿」不可达;
- 数字本身也错: 111 是本席位实测的**变更前**基线, proposal §测试基线自述「新增 12」⇒ 终态应 ~123。写死 111 使该断言在正确实现下也对不上。

后果二选一: 实施者自行放宽判据 (审计标签被销毁), 或卡在一条永远达不成的验收上。

### M-7 — TASK-005 的承重验收在自身执行点恒真, 而其真正生效点无人复检

**锚点**: `detailed-tasks.yaml:118` (dependencies) / `:122` (verification #1) / `:176-180` (TASK-008 verification 全集)

TASK-005 依赖只有 `[TASK-003]`, 因此可在 TASK-006/008 之前完成。此时:
- `test_sc22_no_real_git_subprocess_in_suite` (本席位实读 `:710-724`) 还没有任何新 subprocess 会撞上它 ⇒ 「本 change 落地后仍 PASS」在该时点**恒真**;
- 接缝是否真的挡住了 TASK-008 新引入的 `git ls-remote`, 只有 TASK-008 落地后才可判 —— 而 **TASK-008 的 4 条 verification 里没有一条提 test_sc22**。

(顺带确认: TASK-005 对该守卫机理的判断**是对的** —— `mock.patch.object(pc_module.subprocess, "run", ...)` 打的是 `subprocess` 模块对象本身的属性, 跨模块全局生效, 故新 subprocess 会让它转红而非静默恒绿。这一条 A.2 纠正得准确。)

### M-8 — 一个被点名「须单独 spike」的未知量, 嵌在 L 级实现任务里, 无独立验收

**锚点**: `detailed-tasks.yaml:237-239` (TASK-011 notes) / `tasks.md:13` (组 0 定义)

TASK-011 notes 逐字:「`### 步骤执行` (:99 段) 的 C.2.4 条目在 :101 开 :216 闭的 yaml 围栏内, 且该处没有『5 步』结构 ⇒ 该处改法**须单独 spike**, 不得照搬 :218 段的形态。」

本席位实核: 围栏确在 `:101` 开 `:216` 闭, `:161-175` 段确为纯 YAML 描述结构 (`primitive 调用:` 列表), 无 `执行流程` 的 1-6 步 ⇒ 该判断属实。

但这个 spike **没有被抽成任务**: 它没有独立 deliverable、没有 SC 挂靠、没有「先红」窗口, 被塞在一条 complexity=L / 6h 的实现任务的 notes 里。tasks.md:13 自己立的组织原则是「组 0 = TDD 前置 + spike」, 此处破例且未说明理由。这也是 D1 承重面上风险最高的未知量 —— 「怎样在一个 YAML 描述围栏里表达一条强制执行的 helper 调用」本身就可能没有干净答案。

### M-9 — 折叠 1–5 步会把 `SKILL.md:242` 的两条活的 AI 义务降级, 无任务保护

**锚点**: `proposal.md:78-83` (§2) / `detailed-tasks.yaml:241-257` (TASK-012 只保护步骤 6) / `SKILL.md:242` 实读

`:242` (步骤 2.5) 除了描述 path coverage 算法, 还逐字承载两条**对 AI 的运行时义务**:

```
**执行上下文契约**: 在执行 C.2 合并的目标仓根内调用 (子模块合并 → 子模块根);
`main_branch` 显式传真值 (本项目 `master`), 不依赖 CLI default
```

第一条正是 proposal §1 拿来当 spike 输入的那个 cwd 契约; 第二条是**全仓唯一**一处告诉 AI「本项目要传 master」的指令。§2 要求把 1–5 步整体移进 `<details>` 且标题写 `⛔ 不要手工执行 (供理解与排障)`。⇒ 这两条义务会被搬进一个自我声明为「仅供理解」的块里。

TASK-012 用整条任务保护了步骤 6 的同类问题 (D4), 却**没有任何任务保护 2.5**。与 C-1 直接叠加: 恰在「传什么值」变成 fail-CLOSED 阻断条件的这一刻, 唯一说明该传什么的指令被降级。

---

## Minor

### m-1 — SC-2 未进 TASK-001 的红窗空壳

**锚点**: `detailed-tasks.yaml:40-44` (四条断言) / `proposal.md:197` (SC-2)

可机械 grep 的 SC 共 5 条 (SC-1..SC-5), TASK-001 取了 4 条, 独缺 SC-2 (`"branch": "main"`, 今日实测 1 → 期望 0)。SC-2 与其余四条同类同形, 无任何理由说明为何不入红窗。它最终由 TASK-013 认领转绿, 但缺了本文件自己立的「先看到红」前置。

### m-2 — `tasks.md` 未决 #1 已被自身产物解答

**锚点**: `tasks.md:67`

「`detailed-tasks.yaml` 是否补」列为待 owner 裁, 而该文件已存在 (19 条, mtime 晚于 tasks.md 约 27 分钟)。属 memory `feedback_spec_frontmatter_reflects_reality` 同形的陈旧态。附带确认: `project.md:21`(双层) 与 `:118`(单层) 的不一致**确实存在**, 该未决项的**理由**成立, 只是结论已被行动越过。

### m-3 — TASK-015 未点名 Rule #6 强制的工具 `/skill-creator`

**锚点**: `detailed-tasks.yaml:302-304` / CLAUDE.md 规则 #6 / `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md:23-25,203,533`

Rule #6 逐字「Skill 基准测试**必须用 `/skill-creator`** (自研 runner 已废弃)」, AB 手册 `:23-25` 把自研 runner 列为「废弃」并在 `:533` 把 「`/skill-creator benchmark` 已执行」列为 checklist 项。TASK-015 的验收只写「两套件均跑完, 结果存档」, 未点名工具 —— 对一个曾经真的走过废弃 runner 的项目, 这是可避免的开口。

### m-4 — TASK-019 的 verification 是 issue 内容, 不是可证伪断言

**锚点**: `detailed-tasks.yaml:370-375`

五行 verification 逐条列的是「issue 里该写什么」, 没有一条能回答「它怎么会红」。缺一条形如「5 个 issue 号已开且可 `forgejo GET` 到」的断言 ⇒ 该任务可以在零 issue 被创建的情况下自称完成。

### m-5 — [proposal 层] 决策记录 D2 / D6 已被同文件正文推翻, 仍在表内

**锚点**: `proposal.md:177` (D2) / `:181` (D6) vs `:60-62` (§1) / `:107-115` (§5 三轮实验表)

- **D2** 仍逐字规定「路径用两分支解析 + 不可达即 abort」, 而 §1 已把它降级为 spike 并逐字禁止沿用 (「R5 四席独立实测该形态…全不可达」);
- **D6** 仍逐字规定「存在性核验 pattern **锚定 `refs/heads/<name>`**」, 而 §5 的实验表把锚定判为 **❌ 仍 fail-OPEN**、明写「第三次才对 = 精确字符串比对」, SC-13 更是要求锚定实现**必须在此转红**。

tasks 侧转写得**是对的** (TASK-002 禁止沿用两分支解析; TASK-003 用精确比对), 故不阻塞开工。但 Phase B 实施者会读决策记录表, 两条陈旧条目与任务正面矛盾。属 memory `fixes-contradict` 同形 (同文件内既立判据又违反它, proposal 自己在 `:294` 记录已发生 3 次)。

---

## Verdict

**FAIL** (≥1 Critical)

- Critical 1 / Major 9 / Minor 5
- Critical 与 M-1 / M-9 三者同指一处: **D1 承重面 (TASK-011 写进 SKILL.md 的那两条调用) 的验收网眼比它要挡的缺陷粗**。这三条一起修才闭合, 单修 C-1 会留下「spike 对了但落地文本走样」的口子 (M-1)。
- M-2 / M-4 / M-5 是同一形状的三次复发: **引用一处源码/一条既有条款去承载判断前, 没有去那一处核字面** (`:262/:559/:610` 用的不是 CLAUDE_PLUGIN_ROOT; `_run_with_retry` 跑的不是 git; `query_branch_in_flight` 没有 remote 形参)。建议 A.2 修复时对全部 19 条做一次「凡出现 `由 X 保证 / 复用 X / 对照先例 Y`, 逐处回源核字面」的横扫, 而不是逐条改这三处 (memory `fix-the-class`)。
- M-6 / M-7 是同一形状的两次复发: **验收断言的可评估时点晚于/早于它所在任务的执行时点**。建议 A.2 统一补一条规则: 每条 verification 必须能在该任务完成的那一刻求值。
- 未决三项的处置: #2 (post_planning 闸门) **正确** —— config 实为 `convergence`, 按 Rule #10 不自行跳过, 本轮即其执行; #3 (MAJOR 确认) **正当悬置** —— 属 owner 裁定面; #1 **应由 A.2 自己解决且已被行动越过** (m-2)。

**建议**: REVISE。Critical + M-1 + M-9 必修 (同一面, 一起改); M-2 / M-4 / M-5 建议按类横扫; M-6 / M-7 是低成本文本修正; Minor 可与上述同批带走。

---

## 轮次记录

| 轮 | 席位 | Critical | Major | Minor | verdict | 备注 |
|---|---|---|---|---|---|---|
| R1 | tech-lead | 1 | 9 | 5 | FAIL | 首轮。审计对象 = A.2/A.3 产物 (tasks.md + detailed-tasks.yaml 19 条), proposal 仅作参照物不重审 (post_spec R1-R5 已由 owner override 关闭)。全部 finding 均带实读锚点; 无一条基于 proposal 转述。 |

**本轮未做的事** (供后续轮次接力):
- 未对 19 条的 `est_hours` (合计 55h) 与 `complexity` 分档做校准 —— 本席位镜头未覆盖;
- 未评估 spike (TASK-002/003/004) 结论回写 proposal 的**流程本身**是否需要二次闸门 (回写后 proposal 已过的 post_spec 是否需重开) —— 该问题属编排层, 建议交 owner;
- 未核 `aria-orchestrator/` 侧是否有 `gate_check` 消费者 (TASK-018 的 blast radius 口径覆盖它, 但本席位未替它跑)。

---

## 附录 A — proposal §Impact ↔ 任务映射 (忠实性核验)

| §Impact 行 | 承接任务 | 判定 |
|---|---|---|
| SKILL.md 两处散文重整 + 四行裸命令 | TASK-011 | ✅ (验收网眼见 C-1) |
| SKILL.md `:270` 示例 / `:267` schema / `:279` 注记 | TASK-013 | ✅ |
| SKILL.md 步骤 6 `fail` 分支补一句 | TASK-012 | ⚠️ A.2 改成条件式「已覆盖则不加句」。方向合理 (避 no-op), 但与 §Impact 的确定式表述有出入, 且「是否已覆盖」无判据。**实读 `:255` 现已含 raw_message ⇒ 大概率不加句。** 归入 m 级观察, 未单列 |
| `pre_merge_gate.py` `:21/:300/:427` + help | TASK-006 | ✅ |
| `--remote` / `remote` 参数 | TASK-007 | ✅ (验收见 M-5) |
| `_verify_branch_exists()` + 核验点插入 | TASK-008 | ✅ |
| `raw_message` + `gate_error` | TASK-009 | ✅ |
| 测试: SC 系列 / 24 处调用 / `:663` 断言 / 打桩接缝 | TASK-001·005·008·010 | ✅ (§Impact 写「SC-1..SC-12」漏了 SC-13, 任务侧反而**补齐了** —— tasks 比 proposal 更准) |
| `CLAUDE.md` 规则 #8 | TASK-016 | ✅ 先例 `7661e96` 实核属实 |
| AB 两套件 | TASK-015 | ✅ (工具未点名, m-3) |
| 外部 = no-op | (无任务) | ✅ 正确地没有任务 |
| 发版同步面 (整仓引用点差集) | TASK-017 | ✅ |
| follow-up issue (4 项) | TASK-019 (5 项) | ✅ 超集, 第 5 项 (`:189-191` + `submodule_gate.sh`) 经实读确认存在 |
| **(§Impact 未列)** `SKILL.md:262/:559/:610` | TASK-014 | ❌ 越界, 见 M-3 |

**结论**: 无遗漏面; 唯一超出 proposal 范围的是 TASK-014 (M-3)。
