---
checkpoint: post_planning
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-20T05:12:40.118Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_planning R4 — tech-lead 席 (10CG/Aria#199, A.2/A.3 v2.3, 主仓 `a182ba2` / yaml `a71c94e`)

> frontmatter 的 `drift_check_skipped` 我写 `true`, 不是模板里的 `false`: 派单背景与 `.aria/config.json` 都说 `drift_guard` 未配置, convergence 下该检查 opt-in 且未开启。R1/R2/R3 三轮五席一律写 `false`、三轮都被聚合改判 —— 我按事实写, 理由记在此处备聚合核对。

## 已实读文件

被审对象 (全文):

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md` (227 行)
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml` (1734 行: metadata 全键 + 31 个 TASK 全文)

差异面 (确认返修边界):

- `git diff 12c870d a71c94e` 的 yaml 与 tasks.md 两份 patch 全文

规范与决策:

- `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md` §1.0 求值总序全段 (`:103-151`)、§4 表的 `version.yaml` 行 (`:368`)、SC-14 (`:470`)、rule6_note 照跑面 (`:484`)、待复议 4 (`:530`/`:536`)
- `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` (全文 §1–§5)
- `CLAUDE.md` 多远程推送两条硬约束 + 不可协商规则 3 / 5 / 6 / 8 / 9 / 10 (session 自动加载)
- `standards/conventions/session-handoff.md` `:101-120` (§2.3 五字段 schema)、`:212-220` (§2.3.7 E1 / E2 两层 content enforcement)
- `.aria/state-checks.yaml` `:29-47` (`no-unresolved-version-placeholder`)、`:124` / `:177` / `:302` / `:325` / `:408` (TASK-029 点名的其余五个 check)

源码 (实读, 行号以我实读为准):

- `aria/skills/state-scanner/scripts/phase1_gate.py` `:1125-1204` (`_heartbeat_only` 与返回 JSON)、`_gate_result_to_dict` (认领路径投影, `push_success` / `push_skipped` / `push_skipped_reason` 三键)、`:1425-1500` (argparse 全表: `--heartbeat-only` / `--repo-path` / `--remote` 缺省 `origin`)
- `aria/skills/state-scanner/scripts/release_gate.py` `:111-117` (结果 dict 键)、`:148-155` (`released` 子 dict 的 `success`)、`:190-210` (no_push 与 push 失败两支)
- `aria/skills/state-scanner/lib/coordination_ref.py` `:65` (`REF_NAME`)、`:1285-1287` (push refspec)
- `aria/skills/phase-c-integrator/SKILL.md` `:603`-`:638` (C.2.5 全段)
- `aria/skills/git-remote-helper/scripts/push_all_remotes.sh` `:49` (`PRE_LOCAL_HEAD`)、`:95-125` (成功判据)
- `aria/skills/config-loader/DEFAULTS.json` `:6-15`
- `aria/skills/phase-d-closer/references/execution-steps.md` `:95-115` (D.3 action 全表)
- `aria/skills/phase-d-closer/references/handoff-mechanics.md` `:84-135` (写后自校验 + latest.md 两子步)
- `aria/skills/state-scanner/SKILL.md` Layer L A.1 heartbeat 集成段

我自己实跑的 (全部在 `/tmp/claude-1000/.../audit-R4/tech-lead/` 与只读命令, 真仓零写入、零 git 写操作):

- 用 yaml `metadata.baseline_rebase.standards_files_basis` 逐字描述的机械求法, 对 standards 全仓 102 份 `.md` 的 basename 在三份语料里重算一遍计数
- 用 yaml `metadata.commit_attribution` 的 v2.3 判据代码, 对 31 个 TASK 的 `deliverables` 全量重算路径分类
- `python3` 解析 yaml 重算 DAG、工时合计、agent 分配

## Findings

本轮 0 critical / 1 major / 3 minor。

---

### M1 · `8d2e93ff` · major · issue · documentation · scope: `detailed-tasks.yaml TASK-031`

**一句话**: 5.9 手写 Phase D 绕过 phase-d-closer, 连带丢掉 D.3 的两个正典机械子步 —— Rule #9 五字段写后自校验 (E1) 与 `docs/handoff/latest.md` 两子步维护; 而 TASK-031 只断言五个字段里的 `track-id` 一个, 全计划对另四个字段与 latest.md 零要求、零检查。

**证据 (实读)**:

SOT 侧, D.3 的 action 逐字 (`aria/skills/phase-d-closer/references/execution-steps.md:104-110`):

```
    2b. 写后 frontmatter 自校验 (#137 v1.43.0+, warn-then-fix 非硬 abort):
        head -8 <handoff> | grep -cE '^(track-id|owner-container|phase|status|updated-at):'
        须 ==5; 不足 → 按模板派生规则补齐后重验。不得带缺字段 handoff 进子步 3。
        (口径注: 勿在 frontmatter 内插注释行, 可能把字段推出 head -8 窗口致误报)
    3. 更新 docs/handoff/latest.md pointer (mechanical, 子步骤 1+2 详见 handoff-mechanics.md)
```

同族 SOT `handoff-mechanics.md:135` 对 latest.md 子步骤 1 逐字写「**任何 cycle 都不可跳过**, 否则 cycle 在 latest.md 隐形」并附实证事故。`standards/conventions/session-handoff.md:218` 的 §2.3.7 表把 E1 登记为两层 content enforcement 之一, 覆盖路径逐字是「经 phase-d-closer 的 handoff」; 另一层 E2 只对 **resolved latest doc** 发 soft warning, 不覆盖新写的周期 handoff, 也不阻断。

计划侧, TASK-031 的 handoff 条逐字 (`detailed-tasks.yaml:1733`), 全条只出现一个字段名:

```
周期 handoff 写 docs/handoff/ (Rule #9), frontmatter 的 track-id 逐字写
pre-merge-completeness-gate-change-scope —— 它同时是 metadata.commit_attribution 判该提交为
exclusive 的唯一依据 (写成别的或漏写 ⇒ 判 foreign, 停在 owner_gates 第 16 项); 照录 tasks.md 的
AI 流程判断清单并追加 Phase B–D 新增项, 摘录 TASK-022 的活体输出与各 issue 号
```

我对两份被审文件全文检索: `owner-container` 零命中, `updated-at` 零命中 (yaml 与 tasks.md 都是 0)。`latest` 在 tasks.md 只命中判断清单第 28 条 (讲提交归属), 在 yaml 只命中 `commit_attribution.cannot_catch`「`docs/handoff/latest.md` 这类共享指针一律判 foreign」与 N9 fixture 两处造数据 (`:924` / `:934`) —— **没有任何一个 TASK 要求更新 latest.md**。

易被误读的一处, 我特地核过: TASK-031 确有一条「断言五字段齐备」(`:1727`), 但那五个字段逐字是 `decision_table_row / description_changed / scenario1 / scenario4b / negctrl`, 是 `rule6_note` 的五字段, 与 Rule #9 的 handoff 五字段毫无关系。

判断清单第 25 条逐字 (`tasks.md:79`) 只列了三项偏离:

```
25. 5.9 手写 Phase D, 不调 phase-d-closer: D.1 跳过留痕, D.2b 不带 `--sweep-stale` / `--gc`, D.4 照跑。
```

D.3 的两个机械子步被放弃这件事, 既不在这条里, 也不在别处 —— owner 照这条复议时看不见自己正在批准放弃什么。

机械兜底面我也查了: `.aria/state-checks.yaml` 全文对 handoff frontmatter 与 latest.md 零检查 (唯一含 `frontmatter` 的 `:93` 是 waiver 的 `superseded_by`)。本仓 207 份 handoff 里 178 份带 `track-id`, 说明缺字段不是理论风险。

**失败场景 (照计划字面执行)**: 执行者到 5.9, 按 TASK-031 手写周期 handoff, 唯一被点名的 `track-id` 写对了 —— 它有强动机写对, 因为写错会让提交判 foreign 而停。其余四个字段 (`owner-container` / `phase` / `status` / `updated-at`) 没有任何一条验收提到, 漏写不会红; latest.md 没人要求碰, 不碰也不会红。TASK-031 全部验收通过, 归档、回帖、关单、双推照走完。结果: (1) 这份 handoff 在 state-scanner 的多 track 看板上落成 `legacy` 行, owner 显示 `unknown` (session-handoff.md §2.3.4 的既定行为), Rule #9 的机读 schema 被破坏而无人知道; (2) 本 cycle 在 `latest.md` 里完全隐形 —— 下个 session 的 collector 以 latest.md pointer 为语义权威, 一个刚 ship 完的 cycle 查不到; SOT 对这一形态有逐字禁令与实证事故。Rule #9 是不可协商规则, 「必须写 `docs/handoff/`」只是它的落点要求, §2.3 的五字段是同一条规则的内容要求。

**它怎么会红 (三态)**: 基线 = 今天的判据下, 一份只有 `track-id`、且 latest.md 原封不动的交付**通过 TASK-031 全部验收** (恒绿, 计划里没有任何断言能看它一眼); 目标 = TASK-031 补上 E1 那条逐字命令 (`head -8 <doc> | grep -cE '...' == 5`) 与 latest.md 两子步断言 ⇒ 缺字段或漏 prepend 时该条红, 执行者按 warn-then-fix 补齐重验; 坏实现 = 只 grep `track-id` 一个键 (现状), 或对整份文件 grep 而不限 `head -8` 窗口 ⇒ 正文里出现同名串照样计数 ⇒ 仍是假绿 —— SOT 的口径注正是防这个, 所以补的时候必须连 `head -8` 一起照抄, 不能自己改写成全文件检索。

**建议修法**: (1) TASK-031 的 handoff 条把 E1 命令逐字写进验收 (含 `head -8` 窗口与「不得带缺字段 handoff 进下一步」); (2) 同条补 latest.md 两个子步骤 (子步骤 1 History prepend 无条件做, 子步骤 2 pointer 按 multi-track 判定), 并把 `docs/handoff/latest.md` 的归属后果一次说清 —— 它按 `commit_attribution` 判 foreign, 会停在 owner_gates 第 16 项请裁, 这是计划已有的 fail-closed 路径, 但要写明「该停点是预期的、由 latest.md 维护引起」, 否则执行者会以为自己做错了; (3) 判断清单第 25 条把「不调 phase-d-closer 所放弃的机械子步」逐条列全 (D.3 的 2b 与 3), 使 Rule #10 §5 的复议面完整。

---

### m1 · `d4319379` · minor · issue · documentation · scope: `detailed-tasks.yaml metadata.baseline_rebase.standards_files`

v2.3 新增的七文件清单把「指令有、落点无」补成了可执行落点 (这是 R3-M1 的正解, 见对账), 但集合本身漏了一个**计划确实依赖其内容**的 standards 文件: `conventions/session-handoff.md`。

证据: 该文件定义 Rule #9 的机读 frontmatter schema, `:115` 逐字把 `track-id` 列为五个必填字段之一并规定归一化函数。计划有两处承重地依赖这个字段名 —— `commit_attribution` 的 `exclusive()` 分支 (`:625-627`) 用 `^track-id:\s*<SID>\s*$` 判周期 handoff 是否本轨, TASK-031 (`:1733`) 逐字说它是「判该提交为 exclusive 的唯一依据」。而我按 `standards_files_basis` 的机械求法实跑: `session-handoff` 在 `proposal.md` / `tasks.md` / `gen_yaml.py` 三份语料里的 basename 命中数**全为 0** (`Rule #9` 这个词在 yaml 与生成器里各 2 次, 但不带文件名)。求法只能找到「计划点名过的文件」, 而写下的集合判据是「计划实际依赖其内容的文件」—— 两者不等价, 这个文件就是差集里的实例。

为什么只判 minor 不判 major: 失败方向是 fail-closed。若 Rule #9 的字段名在 B.1 之后漂移 (该 SOT 现为 1.3.0, 有 1.1.0 / 1.2.0 / 1.3.0 三次记录在案的 schema 变更, 且 standards 正是本 cycle 已经动过一次的共享子模块), 后果是周期 handoff 被判 foreign 而停在 owner_gates 第 16 项请裁 —— 多一次请裁, 不是放行错的东西。fail-open 的那一半 (五字段合规本身无人验) 已计在 M1, 不在此处重复计数。

建议: 把 `conventions/session-handoff.md` 补进 `standards_files` (依赖点写「§2.3 五字段 schema, `commit_attribution` 的 track-id 判据与 TASK-031 的 handoff 要求都建立在它上面」), 并把集合判据的措辞与求法对齐 —— 要么承认求法只覆盖「被点名的文件」, 要么补一轮「按依赖点人工过一遍」。

---

### m2 · `f5b3afad` · minor · issue · documentation · scope: `detailed-tasks.yaml metadata.baseline_rebase.standards_files_basis`

`standards_files_basis` (`:86`) 给的机械求法, 我逐字复跑了一遍, **复现不出它自己写的结果**: 按该求法, 命中的 basename 是 10 个家族, 它点名剔除的同名误命中只有两族 (`standards/README.md` 与 `core/*/README.md` 撞主仓 `README.md`; `standards/openspec/templates/tasks.md` 撞本目录 `tasks.md`), 剔完余 **8** 份, 而上表是 **7** 份。差的那一份是 `standards/README.zh.md` (实存, 9172 字节; 在三份语料里命中 3 次, 全部是主仓的 i18n README —— TASK-029 的九个版本同步面文件之一)。

我的实跑输出 (截断):

```
standards .md total: 102
README.md: [('README.md', 11), ('core/ten-step-cycle/README.md', 11), ...]
README.zh.md: [('README.zh.md', 3)]
configured-gate-authority.md: [...]  content-integrity.md: [...]  git-commit.md: [...]
project.md: [...]  proposal-minimal.md: [...]  skill-benchmark-exemption.md: [...]
tasks.md: [('openspec/templates/tasks.md', 79)]  version-management.md: [...]
```

结论本身是对的 (`README.zh.md` 确属同名误命中, 该剔), 错的是**排除清单少列了一族**。不影响执行: TASK-001 是对清单逐个重测, 不是重新求这个集合。但它是「删除/排除建议必须枚举完排除项」这条老账的同形复发, 下一轮若有人拿这段求法复核, 会得出与清单不符的结果并以为清单错了。

建议: 排除清单补 `standards/README.zh.md` 撞主仓 `README.zh.md` 这一族 (与已列两族同一句式)。

---

### m3 · `ea958583` · minor · issue · documentation · scope: `tasks.md AI 流程判断清单`

判断清单停在第 34 条, 三条新增项 (第 32 / 33 / 34) 全部标 `(v2.2)`; **v2.3 一条新增项都没有**。而 v2.3 至少作出两个新的流程判断: (1) `standards_files` 这个七文件集合本身是阅读判断 —— 执笔实例在自报薄弱点 (c) 里逐字承认「求法机械, 但『计划是否依赖其内容』这一步仍是判断」, 且明说 `git-commit.md` 是它加的、边界可争; (2) `coord_push_verify` 的容忍规则 —— `ls-remote` 与本地不等时「先 fetch, 本地值是 FETCH_HEAD 的祖先就算正常」(`:554`), 这是一条新的「什么样的不一致不算失败」判断。第 27 条虽被改写引了 `coord_push_verify`, 但只说「推后再核验」, 没说这条容忍规则。

TASK-031 的交付物之一是「照录 tasks.md 的 AI 流程判断清单」, 照录出来的 Rule #10 §5 复议面就会缺这两项。

**与 R3 的关系 (按四元组算 id 撞车, 是有意的)**: 本条四元组与 R3 的 `ea958583` 完全相同, 算出同一个键。那条 (rule6_note 五字段的取值决定未进清单) 至今未处置; 本条是**同一缺陷类别在 v2.3 的新对象上复发**, 证据是新的 (v2.3 的两个新判断), 不是复述前轮。我按四元组如实登记同键, 请聚合按「同类第二次」处理, 不要当成前轮未闭合。

建议: 补两条 `(v2.3)` 判断; 并考虑把「每轮返修新作的流程判断必须同步进判断清单」写成返修的固定收尾动作 —— 这是它第二次被漏。

## R3 对账

| 题 | 判定 | 证据 |
|---|---|---|
| **R3-M1** (`699adf2f`, TASK-001 基线复核缺 standards 落点) | **closed** | 新增 `metadata.baseline_rebase.standards_files` (`:78-85`, 七条, 每条「文件: 依赖的节与用途 —— 实测 diff」) 与 `standards_files_basis` (`:86`)。TASK-001 的基线复核条 (`:1112`) 现含第四组命令, 与 aria / 主仓两组同构: `git -C standards diff --shortstat 21748d4 <B.1 当时的 standards gitlink, 由 git ls-tree HEAD standards 取> -- <文件>`, 并逐字写「standards 组必须对 B.1 当时的 gitlink 重测, 不得沿用 940cb5b 数值」; tasks.md 的 1.1 checkbox (`:131`) 同步为「**aria / 主仓 / standards 三组**」。我复跑了它的求法 (见 m2), 七份里六份的依赖点我逐条核过属实 (含 `git-commit.md` 的 §6.2 trailer 形制 —— 它确实被 `TRAILER` 正则依赖, 该进集合)。**反事实成立**: 若 B.1 前 `skill-benchmark-exemption.md` 再被并发轨改一次 (它 2026-09-17 刚被改过), 新增那组会给出非空 shortstat ⇒ TASK-001 红; 改前 31 个任务无一会看该文件一眼。残余问题 (集合漏 `session-handoff.md` / 排除清单漏一族) 我按**新发现**计为 m1 / m2, 不算旧洞未闭。 |
| **R3-M2** (`9122f4a9`, 收紧后误伤本轨自己的两个形态) | **closed** | 形态 2: `TOOLING = ".aria/notes/2026-09-17-199-a2-a3-tooling/"` 落在模块常量 (`:607`) 并进 `exclusive()` 的前缀集 (`:618`)。形态 1: TASK-023 新增 trailer 义务与回读确认 (`:1545`), 理由逐字点明「两个交付物都在 shared 集, 结构上不可能含 exclusive 路径 ⇒ 不带 trailer 恒判 shared-only」; owner_gates 第 16 项 (`:142`) 补进 TASK-023。**我用 v2.3 的判据代码对 31 个 TASK 的 deliverables 独立重算了一遍路径分类**, 结果与计划的代价陈述逐项吻合: 主仓侧结构上不含 exclusive 路径的**恰好两组** —— TASK-023 (`ab-suite/audit-engine.json` + `ab-suite/version.yaml`, 两条都在 SHARED 集) 与 TASK-029 (九个版本同步面文件); TASK-024 的 `ab-results` 判 foreign 且 foreign 短路优先, 只能靠调用时传 `extra` (TASK-030 `:1699` 已这样传); TASK-031 的 handoff 靠 `track-id`。**没有第三组**。一个给复算者的提醒 (我第一遍就踩了): 组 1–3 与 TASK-025 的交付物是 aria 子模块内的路径, 它们永远不会作为主仓提交路径出现在 `origin/master..feature` 里, 天真地把 deliverables 当主仓路径分类会误报一批 foreign —— 这不是计划的问题。 |
| **R3-M3** (`e06fea62`, frontmatter 比对面只覆盖四份中的三份) | **closed** | TASK-018 的复核条 (`:1439`) 改为四份并逐字列名 (audit-engine / phase-c-integrator / phase-b-developer / phase-a-planner), 写明 CRLF 两份先去 CR、LF 两份直接切, 并加了「这四份是本 cycle 被改 SKILL.md 的全集, 缺一即 `description_changed` 取 no 失去证据」; TASK-017 (`:1423`) 新增与 TASK-015 同款的 frontmatter sha256 断言, 覆盖 phase-a-planner (LF, 实测 `i/lf w/lf`) 与 phase-b-developer (CRLF, 先去 CR); `rule6_note.fields_basis` (`:149`) 的「三份」已改「四份」并逐字列名。我复核了组 3 的交付物集: TASK-014~017 共七个文件, 其中 SKILL.md 恰为四份, 与「全集」的说法一致, 全计划没有第五份被改的 SKILL.md。这正是我 R3 报的 M2, 修法与我建议的 (1)(2)(3) 逐条对上。 |
| **R3-M4** (`6dddf9f4`, 协调 ref 推送无推后核验) | **closed** (残余见风险段) | 新增 `metadata.coord_push_verify` (`:552-557`) 四段; 三处落点全部接上: TASK-001 的心跳条 (`:1108`) 与同条的重认领分支, TASK-031 的 release 条 (`:1731`)。断言形态与我 R3 建议的一致: `push_success == true` 且 `push_skipped == false`, 再独立 `ls-remote` 与本地 `rev-parse` 比对。hard_constraints 第 2 条 (`:114`) 把协调 ref 纳入硬约束 2 的口径并补上「免授权只覆盖发起这次推送, 不覆盖推成了没有」; owner_gates 第 15 项 (`:141`) 增加「推后核验不过」这一触发条件。**我对源码逐项核了这条新检查是否真能跑**, 这是我判 closed 的依据而不是采信自报: `_heartbeat_only` 返回 JSON 确含 `push_success` / `push_skipped` / `push_skipped_reason` (`phase1_gate.py:1194-1204`); 认领路径的 `_gate_result_to_dict` 同样投影这三键 (且逐字注释「a deliberate skip must be distinguishable from a push FAILURE」); `release_gate.py` 的结果 dict 含 `push_success` / `push_skipped` (`:111-117`) 与 `released.success` (`:148-155`), 计划断言的 `released.success` 名字正确; push refspec 是 `REF_NAME:REF_NAME` (`coordination_ref.py:1285-1287`, `REF_NAME = "refs/aria/coordination"` @ `:65`) ⇒ 计划写的 `git ls-remote origin refs/aria/coordination` 取的是同名远端 ref, 比对可执行。`--heartbeat-only` / `--repo-path` / `--remote` (缺省 `origin`) 三个参数在 argparse 里都存在。`no_push_branch` 那段把带 `ARIA_COORDINATION_NO_PUSH` 的会话的**相反期望值**单列且不算失败, 与 TASK-024 的 AB 会话前提自洽 —— 这一层我上一轮没要求, 是它自己补的, 补得对。 |

## 对执笔人自报薄弱点的表态

- **(a) 往计划里写过一条未实跑的事实断言 (「ab-results 与台账同提交即判 own」), 靠对照实验才发现**: **可接受**, 但要记账。它自己把改正结果写成了 TASK-024 里一句逐字警告「归属口径 (2026-09-19 实测, 不要按直觉推)……foreign 短路优先于 exclusive」(`:1573`), 我按 v2.3 代码复算确认这句是对的 —— 错误已闭环且留了防复发的措辞; 可接受的前提是「未实跑的事实断言」这条教训进 handoff, 不是它这次改对了就算了。
- **(b) 用 `ast.parse` 当编辑闸太弱, 语法合法但跑不通的片段能通过**: **可接受**。这个闸守的是「生成器产出的 yaml 里嵌的判据代码语法没被改坏」, 不是「代码语义对」; 语义正确性本轮由我与主控各自实跑判据代码来兜 (我跑了 `commit_attribution` 与 `standards_files_basis` 两段), 这是规划阶段能有的最强兜法。
- **(c) standards 七文件集是它的阅读判断, `git-commit.md` 是它加的、边界可争**: **部分不可接受** —— 不是因为 `git-commit.md` 加错了 (我复跑求法确认它命中, 且 `TRAILER` 正则确实依赖 §6.2, 该加), 而是因为这个自报点名了风险却没落进任何可复议面: 集合漏了 `session-handoff.md` (m1), 排除清单漏了一族 (m2), 判断清单里一条都没记 (m3)。自己说「这里是判断」之后, 正确动作是把它写进判断清单交 owner 复议, 而不是只在 handoff 里自陈。
- **(d) M1 / M3 / M4 三题的修法都是计划文字, 可证伪性依赖它手跑的反事实, 这些实测没进 yaml 的三态证据**: **可接受**。规划阶段的交付物本来就是文字; 关键是反事实能不能被第三方独立重跑 —— 本轮 R3-M2 / M3 / M4 我都独立跑了 (代码复算 + 源码键名核对), 三条都复现, 说明它的反事实不是自说自话。`coord_push_verify.measured` 那段四态实测其实已经进了 yaml, 比它自陈的要好。
- **(e) 执笔容器与前几轮同, 它既是返修者又是自检者**: **可接受, 但已到边界**。R1 定的换人判据是「Major 过半由本轮返修自身引入」, 本轮我实测四题全部闭合、零新 Major 由 v2.3 引入, 判据不触发。不过本轮我提的 M1 与三条 minor 全是**同一类**: 计划自己声明的规则 (手写 Phase D 要逐步对应 phase-d-closer / 集合判据是「实际依赖」/ 判断清单要收全流程判断) 与它自己的落点不一致 —— 这正是自检者与执笔者同体最难看见的盲区。若开 R5, 建议换人执笔, 不是因为判据触发, 是因为剩下的问题类型已经换了。

### 对执笔人三条请裁项的表态 (不作为新发现)

- **(1) R3-M2 的计数口径 (形态 1 本就通过, 真正由 v2.2 引入的只有形态 2)**: **同意它的技术事实, 但不同意据此改计数**。我按 v2.2 代码推演确认: TASK-023 的形态若带 trailer, 在 v2.2 下走 `own-release-sync` 分支确实能过 —— 但 v2.2 的 TASK-023 **没有 trailer 要求**, 所以「照 v2.2 字面执行」得到的就是恒红。缺陷的计量单位是「照计划字面执行会不会出错」, 不是「代码有没有 bug」; 按这个单位, 形态 1 是 v2.2 收紧引入的真缺陷。结论不影响本轮判定 (两个形态都已修), 只影响 R3 的归因表述。
- **(2) ab-results 不进静态 exclusive 集, 靠 `extra` 放行**: **可接受, 是正解**。写死会把他轨 ab-results 一并放行 (样本 `9de3074` 正是他轨的), 取舍方向 fail-closed; 代价 (TASK-030 漏传 `extra` 就停) 已在 TASK-024 与 TASK-030 两处写明, 且 TASK-001 / owner_gates 第 2 项两个调用点发生在 ab-results 产生之前, 结构上不受影响 —— 这一点我按任务序核过, 成立。
- **(3) `git-commit.md` 进了 `standards_files` 但被引措辞仍是未处置的 minor `31b4c0f1`**: **可接受**。进集合是对的 (依赖真实存在); 措辞失准是另一条账, 它在 `standards_files` 那条里明写「本轮未处置」, 没有掩盖。我 R3 报的那条 minor 状态不变, 仍待 owner 一次性处置, 本轮不重复计入。

## 风险 / 疑问 (不计入 finding)

1. **`/state-scanner` 入口心跳是第四类协调 ref 推送, 但没有逐任务落点**。`state-scanner/SKILL.md` 的 Layer L 段逐字说「持 active claim 的**每次 `/state-scanner` 入口**都调用一次」心跳且不带 `--no-push`, 而它的 fail-soft 契约是「心跳失败只记遥测, 绝不阻断扫描」。计划对这条路径只写了**推前** precheck (hard_constraints 第 4 条 + owner_gates 第 15 项), 推后核验的三个落点是 TASK-001 / TASK-024 / TASK-031。我判**不构成 finding**: 该心跳是 AI 在终端里自己跑的 bash 命令, JSON 就在眼前, 而 hard_constraints 第 2 条与 owner_gates 第 15 项的措辞是按「心跳」这一类写的, 覆盖得到。留作风险是因为它依赖执行者把通用规则套到具体动作上, 而这正是 R3-M4 那一类漏洞的温床。
2. **发布段与 C.2.5 五问: 我逐条对源码核过, 五问全部属实**, 本轮无 finding。具体: 子模块先推、仅主仓调 `verify_parity_post_push` (`SKILL.md:613-623`, verify 在 `:620`) ⇒ 计划据此把 aria 的硬约束 2 交给 TASK-028 自己做, 成立; `push_all_remotes.sh` 的成功判据确为「退出码 0 且 `refs/remotes/<remote>/<branch>` 等于 `PRE_LOCAL_HEAD`」, 而 `PRE_LOCAL_HEAD` 逐字就是 `git rev-parse HEAD` (`:49`) ⇒ 计划写「等于 HEAD」准确; `DEFAULTS.json:6-15` 确为 `fail_on_partial_push: true` + `read_only_remotes: []` ⇒ 失败会阻断; 触发条件与 `expected_sha` 取合并后本地 HEAD (`:603` / `:613`) ⇒ 计划让 TASK-030 先快进是必须的; 枚举面 `git submodule status --recursive` (`:614`) 与 detached 比 HEAD (`:638`) ⇒ 计划事前断言三个子模块无待推内容, 对得上。TASK-029 点名的六个 custom check 我在 `.aria/state-checks.yaml` 里逐个找到了 (`:29` / `:124` / `:177` / `:302` / `:325` / `:408`), TASK-027 第 7 步引的 `:29-46` 与 `no-unresolved-version-placeholder` 的实际块范围一致。
3. **粒度与 DAG 我机械核过, 干净**: 31 个 TASK 的 `dependencies` 全部指向更小编号, 无环、无缺失节点; 工时合计 97–143 与 `metadata.estimated_hours` 逐字相等; 单任务工时上界无一超过 8h (最大 6-8); agent 分配 (qa 15 / backend-architect 8 / knowledge-manager 7 / tech-lead 1) 与 `metadata.agents` 相等。组 2 的六个任务切分与 proposal §1.0 的求值总序边界一一对应 (P0+P1 / P2a+P2 / P3+P4 / P5 / P6 / 收口), 没有跨 P 阶段的切口, 也没有哪个 P 阶段无人认领。
4. **「回归测的是最终树」这条我特地追了一遍, 成立**: TASK-023 末条先把 aria `origin/master` 并入 feature 再开 AB; TASK-025 取号前再并一次并重跑 TASK-018 / TASK-021; TASK-027 第 4 步 (b) 用 `git diff --stat <AB 基线 A> S3 -- skills/audit-engine skills/phase-c-integrator` 判 AB 之后上游有没有动这两个 skill 目录, 非空就回去重跑 AB; 第 7 步在合并树原位重跑三套回归 + 文档机检 + L2。这条链没有缺口。
5. **与 10CG/Aria#195 的顺序**: owner_gates 第 1 项的判据 (该轨台账或 handoff 记下的主仓 PR 合并提交 M, 与 `ls-remote` 的 R 满足 `merge-base --is-ancestor M R`) 可执行; `version.yaml` 与 10CG/Aria#211 的撞号处置 (读 `origin/master` 上的文件取下一个 MINOR, 在飞轨未合并前看不到, 以 TASK-030 合并时的冲突或合并后复读为准) 也可执行 —— 我核了 `version.yaml` 现值确为 `1.5.0`、`audit-engine.json` 文件内 `version` 确为 `1.0.0` 且 2 个 eval, 与计划记录一致。
6. **本轮工作区纪律**: 我只写了本报告一个文件; 真仓零 git 写操作 (无 commit / push / fetch / checkout / stash / tag / update-ref); 所有实跑都是只读命令或在我自己的 scratch 目录里; 未派任何子代理。

## Verdict

**PASS_WITH_WARNINGS · 0C/1M/3m · Vote: REVISE**

R3 的四题 Major 我逐条独立复核, **全部 closed**, 且没有一条是靠计划自述判定的 —— 四题的关键修法我都用源码或自己重跑的判据代码验过。本轮唯一的 Major (M1) 不是前轮遗留, 也不是 v2.3 返修引入的, 而是 v1 起就在、前三轮没人从「手写 Phase D 丢了什么」这个角度看过的面: Rule #9 的五字段与 latest.md 两子步, 计划只覆盖了五个字段里的一个。三条 minor 里两条 (m1 / m2) 挂在 v2.3 新增的 `standards_files` 上, 属新面新问题; m3 是同类缺陷第二次复发。

## 是否足以开始 Phase B

**不足以**, 但差得不远, 且卡点不在计划质量上。两个理由, 强弱不同: (1) 强制性的 —— owner_gates 第 1 项要求 10CG/Aria#195 已完成 C.2 合并或 owner 明示改序, 而该轨现为 `yielded`、B.1 未起, 这道门与本轮审计结论无关, 不清掉就没有合法的下一步; (2) 本轮 M1 是 5.9 才兑现的缺口, 结构上不挡 B.1 起步, 但它恒绿、到 Phase D 才会以「Rule #9 被破坏且无人知道」的形式显形, 而那时已经没有下一道闸了 —— 修它只要在 TASK-031 补两条断言与判断清单一条, 成本远低于事后补救, 应在进 B.1 前随手补掉。
