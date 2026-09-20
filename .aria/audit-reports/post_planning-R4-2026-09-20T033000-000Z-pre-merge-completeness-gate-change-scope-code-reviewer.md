---
checkpoint: post_planning
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-20T05:02:30.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

> **`drift_check_skipped` 取值说明 (不改口径, 只说明为何与提示词骨架的 `false` 不同)**: 我实读 `.aria/config.json` 的 `audit` 段, 键集为 `{_comment, enabled, mode, max_rounds, checkpoints, teams}`, **无 `drift_guard`** ⇒ convergence 下 drift 检查为 opt-in 且未开启 ⇒ 本字段应为 `true`。R3 聚合「流程记录 1」已指出该字段连续三轮被五席写错并建议在提示词里写死; 本轮提示词骨架仍是通用值, 故按事实填 `true` 并在此留痕, 省掉聚合重算。

# post_planning R4 — code-reviewer 席 (证据与命令可执行性视角 + 本轮指派的独立复算)

## 已实读文件

**被审对象** (主仓 `a182ba2`, yaml 落在 `a71c94e`):

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md` 全文 (227 行)
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml` 全文 (1735 行; `metadata` 35 个键 + 31 个 TASK)
- **`git diff a71c94e^ a71c94e` 三文件全部 hunk (582 行) —— 按本轮额外要求先逐 hunk 独立复算, 期间未读 `scratchpad/rework-r3/rework-report.md`**

**对照读**:

- `proposal.md` 按视角取节: `:4` `:9` `:10` `:16` `:77-80` `:103` `:117` `:118` `:122` `:162` `:181` `:267` `:285` `:338` `:340` `:360` `:366` `:368` `:378` `:386` `:407` `:409` `:451` `:462` `:467` `:468` `:469` `:473` `:510`
- 决策单 `.aria/decisions/2026-09-12-…-owner-gates-and-technical-rulings.md` 全文 (§1–§5)
- `CLAUDE.md` 多远程两条硬约束 + 不可协商规则 3 / 6 / 8 / 9 / 10; `.aria/config.json` 的 `audit` 段全文
- `.aria/audit-reports/post_planning-R3-…-aggregated.md` 全文; 我自己的 R3 席位报告全文
- standards `940cb5b`: `conventions/git-commit.md:193-196` (§6.2)、`conventions/content-integrity.md:161` / `:189` (§4.4 / §4.5)、`conventions/skill-benchmark-exemption.md:57-62` (§4.1)、**`conventions/session-handoff.md` 全文要点 (`:32` `:97` `:108` `:115` `:171-173` `:212-219` `:357`)**、`openspec/project.md:117`、`openspec/templates/proposal-minimal.md:28-32`
- aria `1cb3872` 实读 (逐行清单见「引用精度抽查」): `phase-c-integrator/SKILL.md`、`audit-engine/SKILL.md`、`execution-modes.md`、`report-storage.md`、`report-format.md`、`pre-write-validation.md`、`phase-a-planner/SKILL.md`、`phase-b-developer/SKILL.md`、`task-planner/SKILL.md`、`brainstorm/SKILL.md`、`state-scanner/SKILL.md`、`lib/spec_complete.py`、`phase1_gate.py`、`release_gate.py`、`config-loader/DEFAULTS.json`、`run_all_tests.sh`、`test_pre_merge_gate.py`、`push_all_remotes.sh`、**`openspec-archive/SKILL.md`**、**`phase-d-closer/SKILL.md` 与 `references/handoff-mechanics.md`**
- `docs/handoff/latest.md` 头部; 主仓 `CLAUDE.md` / `VERSION` / 四份 README / 两份 architecture 文档的版本点

**实跑** (全部在 `/tmp/claude-1000/…/scratchpad/audit-R4/code-reviewer/` 下; 真仓只做 `log` / `show` / `diff` / `diff-tree` / `ls-tree` / `cat-file` / `ls-remote` 等读操作, **零 git 写操作、零仓内文件改动**, 共享审计副本未被改动 —— 我 `cp -a` 到自己的 `work/` 再用):

| 实跑 | 结果 |
|---|---|
| `metadata.a2_state_runs.script` 全文按其 `command` 在 `a563192` + aria `1cb3872` 副本复跑 | **逐字节一致** (`cmp` 通过, 2396 bytes) |
| `metadata.v2_state_runs.script` 全文按其 `command` 在同一副本复跑 (含 v2.3 新增 5 个 N9 子态) | **逐字节一致** (`cmp` 通过, 4829 bytes) |
| `gen_yaml.py` 用 yaml 自带的四个嵌入块重生成 | **REGEN_IDENTICAL** (`cmp` 通过) |
| `metadata.commit_attribution.code` 对真提交 `12c870d` / `a71c94e` / 自造 ab-results 形态 | 见 R3 对账 M2 行 |
| 协调 ref 推送四态 (我自建临时仓, **不复用执笔人的脚本, 从零重做**) | 见 R3 对账 M4 行 |
| standards `21748d4..940cb5b` 七文件逐个 `--shortstat` + bad-object 失败形态 | 见 M1 |
| 31 个 TASK 的 `deliverables` 全量路径分类 (我自写分类器, 不用执笔人的) | 见 R3 对账 M2 行 |
| standards 全仓 102 份 `.md` 的 basename 在三份计划文件里的计数 (独立重做「机械求法」) | 见 m1 |
| 引用精度抽查 **57 处** | 见下 |

### 引用精度抽查 (57 处; aria 对 `1cb3872` 实读, proposal 与主仓对当前文件实读)

逐条「引用 / 实读 / 是否一致」已机械输出。**结论: 55 处一致, 2 处不一致**, 两处均为**旧账**, 本轮未新增错引:

- 一致 (节选): `phase-c-integrator/SKILL.md:42/:57/:131/:132/:157/:754/:612/:623`、`audit-engine/SKILL.md:381/:385/:410/:423`、`execution-modes.md:9/:10/:15/:34/:43/:44/:66/:82`、`report-storage.md:8/:37/:43`、`report-format.md:5`、`pre-write-validation.md:3`、`phase-a-planner:246/:267`、`phase-b-developer:204/:214/:255/:277`、`task-planner:123`、`brainstorm:141`、`state-scanner/SKILL.md:182`、`spec_complete.py:273/:733/:744/:924/:1642`、`DEFAULTS.json:130`、`run_all_tests.sh:41-46`、`test_pre_merge_gate.py:266`、`push_all_remotes.sh:103-119`、`standards/openspec/project.md:117`、`proposal-minimal.md:28-32`、主仓 `README.md:8/:242`、`VERSION:24`、`system-architecture.md:189`、`version-scheme.md:23`、`.aria/state-checks.yaml:29-46`、proposal `:77-80`(与 `canonical_call` 逐行相同)/`:407`/`:409`/`:451`/`:462`/`:467`/`:468`/`:469`/`:473`/`:510`
- **不一致 1**: TASK-029 写 `CLAUDE.md 两处 (:139 / :141)`, 实读 `:139` = 「残余 deferred 挂 Aria #168…」、`:141` = 「standards 940cb5b / SOT 1.1.0…」; 真正的版本点在 **`:138`** 与 **`:142`**。这是 R2 起就挂着、owner 未裁的 8 条 minor 之一, **本轮不重复计入** (TASK-029 有「行号以执行时 grep 为准」兜底)。
- **不一致 2**: `git-commit.md §6.2` 的引用措辞 —— 实读 `:193` 是 `### 6.2 Spec 关联`, `:196` 的示例值是 `Spec: standards/openspec/changes/{feature}/spec.md` (带 `standards/` 前缀 + 指向文件)。计划的 trailer 形态与 `TRAILER` 正则都不接受 SOT 的字面值。这是 R3 minor `31b4c0f1`, 未处置, **本轮不重复计入**, 但 v2.3 把该文件正式写进了 `standards_files` 并声明「TRAILER 正则…都引它」, 依赖度加深 —— 见「对三条待裁项的表态」第 3 条。

---

## Findings

### Critical

无。

### Major

#### M1 `d7f5b04c` · major · issue · implementation · scope: `detailed-tasks.yaml TASK-001 基线复核条 standards 组`

**一句话**: v2.3 为 R3-M1 新加的 standards 重测组, 在「standards 真的动过」这一**唯一**需要它的场景下会**静默判过** —— 目标 gitlink 的对象不在本机 standards clone 里时, `git diff --shortstat` 的 stdout 是**空串**, 与计划自己定义的「零 diff = 输出为空」签名**逐字节相同**, 而 TASK-001 全程没有任何一步 fetch standards。

**证据**:

1. 新命令原文 (yaml `metadata` → TASK-001 第 9 条 verification, 即 v2.3 唯一改动的那条):
   `对 metadata.baseline_rebase.standards_files 各条冒号前的文件跑 git -C standards diff --shortstat 21748d4 <B.1 当时的 standards gitlink, 由 git ls-tree HEAD standards 取> -- <文件>`
2. **TASK-001 十条 verification 里没有 standards 的 fetch**。我机械扫描: 含 `fetch` 的是第 1 / 5 / 7 条, 其中第 7 条 (分支起点) 逐字为 `git fetch origin 与 git -C aria fetch origin 后…`; 含 `standards` 的**只有第 9 条**。全 yaml 搜 `submodule update` → **零命中**。全计划唯一 fetch standards 的地方是 TASK-030 (`调用前对 aria / aria-orchestrator / standards 各自 fetch origin 与 github`), 那已是 5.8。
3. **失败形态实测** (我在真仓只读跑):
   ```
   $ git -C standards diff --shortstat deadbeefdeadbeefdeadbeefdeadbeefdeadbeef 940cb5b -- conventions/git-commit.md
   stdout=||  rc=128
   stderr=fatal: bad object deadbeefdeadbeefdeadbeefdeadbeefdeadbeef
   ```
4. **零 diff 签名实测** (同命令, 合法 SHA): 七个文件里五个的 stdout 就是**空串**, 另两个是 `1 file changed, 56 insertions(+), 2 deletions(-)` 与 `…21 insertions(+), 3 deletions(-)` —— 与 `standards_files` 写的数字逐字相符。也就是说「命令失败」与「零 diff」在 stdout 上**不可区分**, 而计划记的判据正是 `各自 shortstat 输出为空`。

**失败场景 (执行者照字面做什么 → 得到什么错误结果)**: 并发轨 (如 `10CG/Aria#211` 那种) 推进 standards 并 bump 主仓 gitlink → 本轨执行 owner_gates 第 2 项的 `git fetch origin` + `git merge origin/master` (主仓) → 本地主仓 HEAD 现在记着一个新的 standards gitlink, 但**主仓 fetch/merge 不会拉子模块对象**, 本机 standards clone 里没有它 → `git ls-tree HEAD standards` 照样吐得出那个 SHA → 七条命令各自打印空串、退出 128 → 执行者按「与 A.2 记录比对」看到七个空串, 记台账「standards 组零 diff, 与 A.2 一致」→ **基线复核通过**。而这恰恰是 standards 真的动了的那一次: gitlink 与本机 clone 顶点不同, 本身就蕴含 standards 动过。**检查的失效条件与它要检测的条件是同一个条件。**

**「它怎么会红」三态**: 基线态 = 七个空串 (真零 diff, 过); 目标态 = 动过的文件给出非空 shortstat (红, 触发逐处实读); **坏态 (本条) = 七个空串但 rc=128 (假绿)** —— 三态里有两态输出完全相同, 只有退出码能分开, 而计划没有任何一处要求看退出码。

**为什么是 major 不是 critical**: 方向 fail-open (漏检而非误放外向动作), 不写错代码、不推错东西; 但它让 R3-M1 的修复在其目标场景下不可证伪, 且 R3 聚合里 knowledge-manager 点名的后果 (`rule6_note` 五字段格式与写法自检都建立在 standards 当前内容上, 31 个任务无一会侧向发现漂移) 原样保留。

**建议修法 (三处, 都在同一条 verification 里)**: (a) 该组命令之前加 `git -C standards fetch origin` (与 aria 组同构); (b) 跑之前先 `git -C standards cat-file -e <gitlink>^{commit}`, 不成立 ⇒ 停下上报 (不得当作零 diff); (c) 把判据从「输出为空」改成「**退出码为 0 且输出为空**」, 非 0 一律停。顺带: `git ls-tree HEAD standards` 返回的是整行 `160000 commit <sha><TAB>standards`, 条文应点明取第三字段, 否则直接把整行喂给 `diff` 也会得到同一个假绿形态。

---

#### M2 `8d2e93ff` · major · issue · documentation · scope: `detailed-tasks.yaml TASK-031`

**一句话**: 计划明示 5.9 **手写 Phase D、不调 `phase-d-closer`**, 却没有把 D.3 里两个 mechanical 子步骤接过来 —— `docs/handoff/latest.md` 的 **History prepend (SOT 逐字「任何 cycle 都不可跳过」)** 与 **pointer 子步骤的多 track 决策**, 以及写后的 frontmatter 五字段自校验, 在 TASK-031 里零出现; 计划全文提到 `latest.md` 只有两处, 都是「归属判 foreign / 一律请裁」, 没有一处是「本 cycle 要改它」。

**证据**:

1. `tasks.md:79` 判断清单第 25 条逐字: 「5.9 手写 Phase D, 不调 phase-d-closer: D.1 跳过留痕, D.2b 不带 `--sweep-stale` / `--gc`, D.4 照跑」; TASK-031 第 2 条 verification 逐字把 D.1 / D.2 / D.2b / D.3 / D.4 一一对应, 其中 **`D.3 = 周期 handoff`** —— 只有这五个字。
2. TASK-031 的 `deliverables` 四项: `tasks.md` / `detailed-tasks.yaml` / `openspec/archive/<日期>-…/verification-ledger.md` / `docs/handoff/<周期 handoff>.md`。**无 `docs/handoff/latest.md`**。
3. TASK-031 的 handoff 条 (v2.3 刚改过的那条) 只要求 `frontmatter 的 track-id 逐字写 …` —— 而且理由是给 `commit_attribution` 用的, **不是** Rule #9 的五字段义务。
4. SOT 逐字 (aria `1cb3872`, `phase-d-closer/references/handoff-mechanics.md`): `:102` 「## latest.md 维护 (mechanical, 2 个独立子步骤)」; `:106` 「### 子步骤 1 (always, **不可跳过**): History 表格 prepend 新条目」; `:114-123` 子步骤 2 pointer 行更新 + 三行决策表 (按 `snapshot.tracks_multibranch` 判 single-track / multi-track leader / follower); `:135` Forbidden patterns 第一条逐字「❌ 跳过 latest.md 子步骤 1 (History prepend) —— **任何 cycle 都不可跳过**, 否则 cycle 在 latest.md 隐形 (实证: nexus PR #107)」; `:84-100` 写后 frontmatter 自校验 (#137) `grep -cE '^(track-id|owner-container|phase|status|updated-at):' == 5`, 且明写它是「**latest.md 维护的前置**」。
5. 另一份 SOT `standards/conventions/session-handoff.md`: `:32` 把「跳过 `docs/handoff/latest.md` pointer 更新」列为反模式; `:97` 「写入后**自动**更新 `docs/handoff/latest.md` pointer (单 track 场景) 或 deprecation banner (多 track 场景)」; `:115` `track-id` 只是五个必填字段之一; `:357` 记着这一类事故的历史实证 (pointer 陈旧)。
6. **本仓当前就是多 track**: 我实读 `docs/handoff/latest.md`, 顶部有 `⚠️ 当前是多 track 场景, 单指针无法准确表达` 与三条在飞 track 的表 ⇒ 子步骤 2 必须走决策表判 leader / follower, 这是个需要判断的动作, 不是照抄。

**失败场景 (两条路都不对)**: (i) 执行者严格照 TASK-031 字面做完 Phase D —— 写了周期 handoff, **没碰 latest.md** ⇒ 本 cycle 在 latest.md 隐形、pointer 停在 `2026-09-18-…` (SOT 明令不可跳过的那一条), 下个 session 的 A.0 与 L2 collector 读到的「最新」不是本 cycle; (ii) 执行者按 SOT 补做 —— 这次编辑落在计划自己判为「共享指针, 一律请裁」的 `latest.md` 上, 而 TASK-031 的外向动作/等待点里没有这一项 (`owner_gates` 第 13 项只写「Phase D 提交双推与 release_gate 的协调 ref 推送」), 于是变成一个**未登记的请裁点**, 与 Rule #10「AI 的流程判断必须登记」相抵。

**为什么是 major**: 漏掉的是 Rule #9 SOT 逐字标注「不可跳过」的必做项 + 一个未登记的共享指针改动 (外向动作登记面), 且正是「手写 Phase D」这个 AI 流程判断把原本由 Skill 兜住的两个 mechanical 子步骤连带丢掉的 —— 计划对 D.1 / D.2b / D.4 都逐项交代了怎么手做, 唯独 D.3 只有五个字。不是 critical: 后果可事后补救 (改 pointer 是一次提交), 不产生不可撤销的外向动作。

**建议修法**: TASK-031 的 D.3 条展开为三小步 —— (1) 写 handoff doc 后跑 #137 五字段自校验 (`grep -cE … == 5`); (2) `latest.md` 子步骤 1 History prepend (无条件); (3) 子步骤 2 按 `handoff-mechanics.md` 三行决策表判本 cycle 是 leader 还是 follower (当前多 track ⇒ 需显式判并把结论记台账); 同时把 `latest.md` 的这次改动写进 `owner_gates` (并入第 16 项或新增一项), 与判断清单第 28 条的「一律请裁」自洽。

### Minor

#### m1 `0f027861` · minor · risk · documentation · scope: `detailed-tasks.yaml metadata.baseline_rebase.standards_files_basis`

**一句话**: `standards_files` 的集合判据自述是**语义的**(「本计划实际依赖其内容的 standards 文件」), 求法却是**字面的**(basename 在三份计划文件里出现过) —— 两者的差集里躺着 `conventions/session-handoff.md`, 而计划的 `cannot_catch` 逐字引用了它的内容。

**证据**: 我独立重做了那段机械求法 (standards 全仓 `.md` 实测 **102** 份, 与 `standards_files_basis` 写的数字一致; basename 在 `proposal.md` / `tasks.md` / `gen_yaml.py` 三份里计数, 剔同名误命中 `README.md` / `tasks.md` / `README.zh.md`), **得到的正是那七份, 与计划逐字相同** —— 求法本身复现无误。但 `metadata.commit_attribution.cannot_catch` 逐字写着「frontmatter 的 track-id 逐字为本 spec id (**Rule #9 五字段之一**)」, 该「五字段」的 SOT 就是 `conventions/session-handoff.md:115` 与 `:212-219`, 计划从未写出这个 basename ⇒ 机械求法看不见它, 它也就不在 TASK-001 的重测面上。

**为什么只算 minor**: 真漂移时方向 fail-closed (字段改名 ⇒ handoff 提交判 `foreign` ⇒ 停在第 16 项请裁), 执行者不会做错也不会静默通过。**建议**: 在 `standards_files_basis` 里加一句「机械求法只覆盖被点名的文件; 以 Rule #N 间接引用的 SOT (当前已知: `session-handoff.md`) 手工补入」, 并把该文件补进清单。

---

#### m2 `cb1529a3` · minor · issue · documentation · scope: `detailed-tasks.yaml metadata.baseline_rebase.standards`

**一句话**: v2.3 把零 diff 断言的范围从四个文件扩到五个, 但**同一段里那句粗体范围限定句仍写「四个文件」**, 与它前一句自相矛盾, 也与 `tasks.md` 已改对的措辞不一致。

**证据** (同一个字符串值内, 前后相隔约 120 字):
- 前句: `零 diff 的断言限定在其余五个被引文件 {openspec/project.md, openspec/templates/proposal-minimal.md, conventions/configured-gate-authority.md, conventions/version-management.md, conventions/git-commit.md}…`
- 后句 (粗体): `**这是对上述四个文件、在 21748d4..940cb5b 之间的断言, 不是对 standards 全仓、也不是对任意时点的全称句**`
- 对照 `tasks.md:21` 已改对: 「其余**五个**被引文件 … **这是对这五个文件、这两个 SHA 的断言**」

**为什么只算 minor**: TASK-001 照 `standards_files` 逐个重测七份, 不读这句数字, 执行面无影响。**但**这句粗体句正是 R2 的 `PP2-M4` 逼着加上的「范围限定句」—— 限定句自己数错了数, 值得一改。**建议**: 四 → 五。

---

#### m3 `f0e78a1e` · minor · issue · documentation · scope: `detailed-tasks.yaml metadata.revision_log`

**一句话**: `revision_log` 的 v2.3 minor 条声称「`638d2a0f` 随 R3-M2 一并理顺 (**TASK-029 的 deliverables 与 verification 表述**)」, 实际 deliverables **一个字没动**, 只有两条 verification 改了。

**证据**: `git diff a71c94e^ a71c94e` 里 TASK-029 只有两个 hunk, 都落在 verification (trailer 条与提交条); TASK-029 的 `deliverables` 十项今天仍以 `openspec/changes/…/verification-ledger.md` 收尾 —— 即 R3 minor `638d2a0f` 指出的那一项。矛盾是靠新写的执行口径 (「本提交只含九个版本同步面文件」「台账随 TASK-030 一并提交」) 消解的, 不是靠改 deliverables。

**为什么只算 minor**: 执行口径写清楚了, 执行者照做不会错 (我的 31 TASK 全量分类在「按口径只 add 九个文件」下与计划的两组结论一致)。**建议**: 要么把 deliverables 里的台账移到 TASK-030, 要么把 `revision_log` 这句改成「verification 表述」(删掉 deliverables)。**写什么改了, 就得真改了** —— 这条本身是个可被 diff 证伪的声称。

---

#### m4 `9c0dcb27` · minor · risk · testing · scope: `detailed-tasks.yaml metadata.coord_push_verify`

**一句话**: R3-M4 的修复是全计划**唯一**一处「新增判据但不附 `script` + `output` 可复跑对」 —— `coord_push_verify.measured` 是一段散文, 与 `a2_state_runs` / `v2_state_runs` 的做法不同, 复核方无法按其 `command` 重跑比对, 只能从零重建实验。

**证据**: `metadata` 里带 `script` + `output` 的证据块有两个 (`a2_state_runs` / `v2_state_runs`), 两个都给了 `command` 且我逐字节复现; `coord_push_verify` 只有 `why` / `assert` / `no_push_branch` / `measured` / `cannot_catch` 五段散文, `measured` 以「2026-09-19 在 scratch 临时仓实测…」开头, 没有可复跑入口。我因此自建临时仓从零重做了四态 (见 R3 对账 M4 行), **结论与 `measured` 逐项吻合**, 所以这是证据可复现性问题, 不是内容问题。

**为什么只算 minor**: 内容我已独立证实为真, 执行者拿到的 `assert` 可直接执行。**建议**: 下次把这类新增判据的取证脚本也按 `script` + `output` 嵌进来 (`v2_state_runs` 已有现成位置, 加一个 `n11_block` 即可), 否则每轮复核都要重建一次实验。

---

## R3 对账

| 题 | 判定 | 证据 (全部我亲自跑/读) |
|---|---|---|
| **R3-M1** `699adf2f` (基线复核条 standards 零出现) | **closed** (原洞闭合), 但修复**引入 M1** | TASK-001 第 9 条现含第四组命令, 与 aria / 主仓两组同构, 点名 `metadata.baseline_rebase.standards_files`; 新增 `standards_files` (七条, 各带依赖点) 与 `standards_files_basis`; `scope_repos` 的 standards 行、`tasks.md` 读前必看第 5 条、1.1 checkbox (「**aria / 主仓 / standards 三组**」) 同步。**我独立复算**: 七份文件在 `21748d4..940cb5b` 的 shortstat 与清单逐字相符 (五个空串 + `+56/-2` + `+21/-3`), `git diff --name-only` 全仓恰好只有那两个文件; 我重做的 basename 机械求法**独立得到同一个七份集合**。「指令有、落点无」这一条确实闭了。**但**新命令在 gitlink 未 fetch 时假绿 ⇒ 单列为 **M1** (不重复计入本题)。 |
| **R3-M2** `9122f4a9` (收紧后误伤本轨) | **closed** | 形态 2: `TOOLING = .aria/notes/2026-09-17-199-a2-a3-tooling/` 进了 `exclusive()` 前缀集; **我对真提交跑判据代码**: `12c870d` 由 R3 的 `foreign` 翻为 `{"verdict":"ok","commits":1,"kinds":["own"]}`, 本轮的 `a71c94e` 同样 `own`。形态 1: TASK-023 补了与 TASK-029 同款 trailer 义务 + 回读确认, `owner_gates` 第 16 项补了 TASK-023。**我独立重写分类器对 31 个 TASK 的 deliverables 全量分类**: 唯一结构上纯 shared 的是 TASK-023 的两个 ab-suite 文件; TASK-029 十项里含台账 (exclusive), 所以「两组」这个结论**只在 v2.3 新加的执行口径 (只 add 那九个文件、台账随 TASK-030) 下成立** —— 口径写在 verification 里, 自洽 (deliverables 未同步是 m3)。ab-results: 我自造「结果目录 + 台账同一提交」实测 `{"verdict":"stop","kinds":["foreign"]}`, 传 `extra` 后 `own` ⇒ TASK-024 新写的那段「foreign 短路优先于 exclusive, 同提交捎台账救不了」**经我实测为真** (这正是执笔人自报被对照实验推翻的那条, 见最后一节)。 |
| **R3-M3** `e06fea62` (frontmatter 比对面三份漏第四份) | **closed** | TASK-018 与 `rule6_note.fields_basis` 均改为**四份**并逐字列名; TASK-017 新增一条与 TASK-015 同款的 sha256 frontmatter 比对 (phase-a-planner 直接切、phase-b-developer 先 `tr -d '\r'`); `tasks.md` 3.5 行同步。**我独立核**: (a) 本 cycle 被改 SKILL.md 确为四份 (TASK-015 / 016 / 017 的 deliverables 汇总, TASK-025 只动版本 5 文件, 无第五份); (b) 四份**全部**带 `description:` frontmatter (逐份实读); (c) 行尾实测 `i/lf w/lf` = audit-engine + phase-a-planner, `i/crlf w/crlf` = phase-b-developer + phase-c-integrator, 与新条文逐字相符 (v2.3 新写的「phase-a-planner 是 LF (2026-09-19 实测 i/lf w/lf)」属实)。 |
| **R3-M4** `6dddf9f4` (协调 ref 推送无推后核验) | **closed** | 新增 `metadata.coord_push_verify` 并接进三处 (TASK-001 心跳 + 重认领、TASK-031 release), `hard_constraints` 第 2 / 3 条与 `owner_gates` 第 15 项、`tasks.md` 判断清单 27 / 外向动作引言 / 等待点 15 / 1.1 / 5.9 同步。**我不用执笔人的脚本, 自建临时仓从零复现四态**: 正常 `outcome=refreshed / push_success=True / push_skipped=False`, exit 0, `ls-remote` 与 `rev-parse` 相等; `ARIA_COORDINATION_NO_PUSH=1` ⇒ `False / True / env_var`; `--no-push` ⇒ `False / True / cli_flag`; **origin 指向不存在路径 ⇒ `refreshed / False / False`, exit 仍 0** (stderr 三行 `push failed (rc=128…)`) —— v2.2 那条「期望 outcome refreshed」在这一态确实假绿。**另核 `assert` 的键名在真代码里可执行**: 心跳路径 `phase1_gate.py:1194-1204` 输出 `push_success` / `push_skipped` / `push_skipped_reason`; 认领路径 `:1391-1409` 有 `proceed` 与同三键 (我实跑 `proceed=True`); release 路径 `release_gate.py:148-155` 的 `released` 是**含 `success` 的 dict** (我实跑 `released={'success': True, …}`) ⇒ 计划写的 `released.success 为 true` 可执行, 不是想当然。残余只有证据不可复跑 (m4)。 |

**本轮两条 Major 的引入来源** (给聚合方做 R1 换人判据用): **M1 由 v2.3 返修自身引入** (v2.2 没有这条命令, 也就没有这个假绿面); **M2 自 v1 起就有** (判断清单第 25 条「手写 Phase D」是 v1 决定)。⇒ 1/2, **未过半**。

---

## 独立复算 vs 执笔自报的差异

**顺序声明**: 上文全部结论在**读返修报告之前**形成并落盘 —— 我先读 `git diff a71c94e^ a71c94e` 的三文件全部 hunk, 再读成品 yaml/tasks.md, 再做全部实跑, 写完报告后才打开 `scratchpad/rework-r3/rework-report.md` (217 行, 已完整读)。

### 一致 (我先独立得出, 它也这么写)

| 项 | 我的独立结果 | 它的自报 |
|---|---|---|
| standards 七文件集 | 我重做机械求法 (102 份 `.md` basename × 三份计划文件, 剔同名误命中) ⇒ **同一个七份** | 同 |
| `21748d4..940cb5b` 实测 | `+56/-2` · `+21/-3` · 五个空串; `--name-only` 全仓恰两文件 | 同 |
| 真提交 `12c870d` | `foreign` → **`own`** | 同 |
| TASK-023 形态带 trailer 在 v2.2 代码下**本就通过** | 我从 diff 独立确认: v2.3 没碰 `TRAILER` / `own-release-sync` 分支, 那是 v2.2 就有的 | 同 (它 §8 第 1 条据此请裁计数口径) |
| **ab-results + 台账同提交仍 `foreign`** | 我自造该提交实跑: `{"verdict":"stop","kinds":["foreign"]}`; 传 `extra` 才 `own` | 同 (它 §9(a) 自报初稿写反, 靠对照实验推翻) |
| 协调 ref 四态 | 我自建临时仓从零重做, 四行**逐格相同** (含 `refreshed / false / false / exit 0` 那一行) | 同 |
| `REGEN_IDENTICAL` · a2 / v2 输出逐字节 | 我各自独立复跑通过 | 同 |
| diffstat · 机械体检 | 实测 `3 files changed, 144 insertions(+), 57 deletions(-)`; 三文件 NUL=0 / CR=0 / 禁用字形=0; yaml 顶层末键仍是 `tasks` | 同 |

**一条值得单独记的印证**: 它自报唯一被推翻的自造错误 (「ab-results 与台账同提交即判 `own`」), 我在**不知情**的情况下独立构造提交实测, 确认改正后的文字为真。更有意思的是: 我第一版静态分类器 (只判「有没有 exclusive 路径」) 也把 TASK-024 归成 `HAS-EXCLUSIVE`, **踩的是同一个坑** —— 只有真造提交跑判据才得 `foreign` (`if not ks or "foreign" in ks` 在 `elif "exclusive" in ks` 之前短路)。这说明该错误不是粗心, 是「读意图 vs 读求值顺序」的结构性陷阱; TASK-024 里那句「不要按直觉推」应当保留。

### 出入 (我有、它没有)

1. **M1 (standards 组假绿) —— 它完全没看到, 且盲点就在它自己的反事实设计里。** 它 §1 的反事实自检逐字是「区分力已实测: 同一命令形对七个文件跑, 2 个非空 / 5 个空 —— 不是恒绿真空」: 这是在**本机已有该 gitlink 对象**的 happy path 上测的, 从没问过「B.1 时 gitlink 的对象不在本机 standards clone 里会怎样」。我实测那一态 stdout 同样是空串 (rc=128), 与「零 diff」不可区分。
2. **M2 (手写 Phase D 漏掉 latest.md 两个子步骤 + 五字段自校验) —— 不在它的返修范围**, 它只动四题 Major + 两条连带 minor, 所以不构成矛盾; 但 R3 五席与本轮返修都没碰到这一面。
3. **m2 (「四个文件」) —— 自报与产物不符。** 它 §1 的落点表逐字写「`standards` 散文: 零 diff 断言**四文件 → 五文件** + 写明可执行落点」; 实际只改了前半句, 同一段里那句粗体范围限定句仍是「这是对上述**四个文件**…的断言」。`tasks.md` 那边改对了, yaml 这边没有。
4. **m3 (`revision_log` 声称改了 deliverables) —— 同类自报与产物不符。** 它 §5 写「`638d2a0f`: 随 R3-M2 理顺 (TASK-029 的 **deliverables 与 verification 表述**, `gen_yaml.py:574` / `:576`)」, 而 `:574` / `:576` 两处都是 verification 条; deliverables 十项一字未动。yaml 里的 `revision_log` 也照抄了这个说法。
5. **m1 (七文件集缺 `session-handoff.md`) —— 它 (c) 承认「是阅读判断」, 我给出具体缺口。** 另有一处枚举不全: 它 §1 只列了两个同名误命中族 (`README.md` 与 `tasks.md`), 我的独立复算撞到**第三族 `README.zh.md`** (standards 确有该文件, 生成器里出现 3 次)。结论不变 (都该剔), 但与本仓 memory「守卫 fixture 按敏感名形态族穷举」同型。
6. **m4 (证据不可复跑) —— 我的判断比它 (d) 更分化。** 它把 M1 / M3 / M4 三题并列为「没有内嵌状态证据」; 实测下来 **M3 说重了** (它的可证伪落点确实写进了计划: TASK-017 的 frontmatter sha256 断言 + TASK-018 的四份复核, 不依赖手跑), **M1 说轻了** —— M1 缺的不只是证据, 是缺陷本身没被发现的原因。

### 其它

- 它 §8 第 1 条 (R3-M2 计数口径) 我独立采纳, 见上一节第 1 条。给聚合方补一个同类数: **本轮我两条 Major 中 M1 由 v2.3 返修自身引入、M2 是 v1 遗留 ⇒ 1/2, 未过半** (R1 换执笔实例判据不触发)。
- 它 §2 写「全仓只有本轨两个提交碰过工具目录 (`12c870d` 与 `1ab72cc`)」—— 写的时候为真, 现在是**三个** (`a71c94e` 自身也碰了)。不影响判据 (静态前缀集不数提交数), 只是该句已过期。
- **总结**: 独立复算**没有推翻它任何一条返修结论**; 出入全部落在两类 —— 它**没看到的面** (两条 Major) 与**自报与产物之间的偏差** (两条 minor)。这恰好支持它 (e) 提的那条建议: 换一席不读结论、直接对 diff 复算, 抓到的正是自检抓不到的那一类。


## 对执笔人自报薄弱点的表态

- **(a) 「ab-results 与台账同提交即判 own」是未实跑的事实断言, 活过两轮编辑, 靠对照实验而非自检发现 —— 可接受 (作为自报), 但请把教训落成机制。** 我独立实测该形态确为 `foreign` (foreign 在聚合里短路优先), 现在 yaml 里写的口径是对的; 问题不在结论而在「计划里可以存在没跑过的事实句」这件事本身 —— 与 m4 同源 (新判据不附可复跑取证)。
- **(b) 用 `ast.parse` 当编辑闸太弱 (语法合法但跑不通的片段能过) —— 可接受, 且本轮不构成风险。** 我从 yaml 取出 `gen_yaml.py` 的四个嵌入块**原样重生成 yaml 并 `cmp`, 得 REGEN_IDENTICAL**; 两个嵌入脚本我都按其 `command` 真跑完并逐字节比对通过 ⇒ 本版的嵌入代码不是「只过得了语法」的那一类。
- **(c) standards 七文件集是阅读判断 (求法机械, 「计划是否依赖其内容」仍是判断); `git-commit.md` 是它加的、边界可争 —— 可接受, 但边界确实漏了一个。** 我独立重做机械求法得到**同一个七份集合**; 分歧不在求法而在判据与求法的类型不匹配 (语义判据 / 字面求法), 差集里有 `session-handoff.md` ⇒ m1。`git-commit.md` 加得对 (计划确实依赖 §6.2 的语义), 争的是措辞 (见下)。
- **(d) M1 / M3 / M4 三题的修法都是计划文字, 可证伪性依赖它手跑的反事实, 这些实测没进 yaml 的三态证据 —— 部分不可接受。** M3 的可证伪落点是**真落在计划里**的 (TASK-017 的 sha256 断言 + TASK-018 的四份复核), 不依赖手跑; M4 的 `measured` 我独立复现为真但不可复跑 (m4); **M1 最糟**: 它不但没有三态证据, 新命令在最需要它的场景下三态里有两态输出相同 (M1)。「没进证据块」在 M1 这一条上不是记录风格问题, 是缺陷本身没被发现的原因。
- **(e) 执笔容器与前几轮同, 既是返修者又是自检者 —— 本轮可接受 (被本轮的流程设计对冲掉了)。** 主控把「不读返修报告、直接对 diff 独立复算」指派给我, 正是对这条的对冲; 我的独立复算与它的自报吻合 (见最后一节), 这比再换一个执笔实例更能说明问题。

## 对执笔实例三条待裁项的表态 (不作为新发现)

1. **R3-M2 的计数口径 (形态 1 不是 v2.2 引入的代码缺陷, 真正由 v2.2 引入的只有形态 2)** —— **事实成立, 采纳该更正**。我在 v2.2 的判据代码下实测: TASK-023 形态**带 trailer** 时本来就判 `own-release-sync` (通过), 所以形态 1 确实是「连带义务没写进 TASK-023」而非代码判错。但请注意这不改变 R3 的定性: 计划在两种写法下都是错的 (要么 TASK-023 缺义务, 要么恒红), 只是归因层次不同。对换执笔实例的判据而言, 这条把 v2.2 自引入数从 1 压到 1 (形态 2), 不影响「未过半」。
2. **ab-results 不进静态 `exclusive` 集 (写死会把他轨 ab-results 一并放行), 代价是 TASK-030 漏传 `extra` 就会停** —— **可接受, 取舍正确**。我实测样本 `9de3074` 确为他轨 ab-results 形态, 写死即放行; 而漏传 `extra` 的方向是 `stop` (fail-closed, 多一次请裁), 不是静默放行。TASK-024 新写的那段把「不要另找同提交捎带 exclusive 路径的替代做法」讲死了, 正确。
3. **`git-commit.md` 进了 `standards_files` 但被引措辞仍是未处置的 minor `31b4c0f1`** —— **进集合是对的, 措辞应随 owner 批次一并处置**。计划确实依赖 §6.2 的语义 (trailer 键名与「单起一行」的写法), 所以它属于「实际依赖其内容」的文件; 但我实读 `:196` 的示例值是 `Spec: standards/openspec/changes/{feature}/spec.md`, 而计划的 `TRAILER` 正则 `^Spec:\s+openspec/changes/<SID>(?:\s|$)` **会拒绝 SOT 的字面值** —— 现在这层依赖被写进了 `standards_files` 的依赖点说明 (「TRAILER 正则…都引它」), 依赖度加深了一层, 所以这条 minor 的处置优先级应升一档 (仍由 owner 批处理, 我不重复计为 finding)。

---

## 风险 / 疑问 (不计入 finding)

1. **`a2_state_runs` 仍是 premise-bound 到 `a563192`** (R3 minor `a5996c58`, 未动, 等 owner 裁): 我在 `a563192` 副本上复跑**逐字节一致**, 证据本身自洽; 但 Phase B 实际执行的树是当前 master, 那上面七条 liveness 状态行不复现 (根因是本轨自己提交进主仓的 `gen_yaml.py` 让符号恒 alive)。验收面 (L2 / L3) 仍有区分力, 故不升级。
2. **归档门预演与 Step 7 的外向动作**: 我在 C 态复现 `gate verdict=warn exit=0`, warn 的唯一来源是 `unverified_claims` 那条「活体 dogfood (SC-11) 与 SC-… → dogfood/benchmark/deploy claim 无可链接产物路径或路径不存在」, 与 TASK-031 的预期逐字一致; `d_payload_is_null=False`, 而 `openspec-archive/SKILL.md:287` 的 Step 7 触发条件逐字是 `gate_result.d_payload != null`, `:294-296` 明写不看 ack、headless 也会自动建 tracker ⇒ **warn 下 Step 7 确会产生外向动作**, 计划已登记为 `owner_gates` 第 11 项并写明「裁不建则只跳过 Step 7」, **登记到位**。
3. **入口门未变**: 我实读 `docs/handoff/latest.md`, `10CG/Aria#195` 仍为 `yielded`、B.1 未起 ⇒ 即使本轮收敛, 下一步仍是 `owner_gates` 第 1 项的 owner 门, 不是 Phase B。
4. **TASK-001 从本地 `refs/aria/coordination` 解析 claim 而 `coord_ref_precheck` 只 fetch 到 `FETCH_HEAD`** (R3 风险 2, 未动): 本地 ref 落后 origin 时解析读的是旧快照 (`10CG/aria-plugin#197` 形态)。本轮未复现, 仍只列为风险。
5. **`cannot_catch` 的两个统计数字经我复核为真**: 仓内 `docs/handoff/*.md` 实测 **207** 份, 带 `^track-id:` 的 **178** 份, 与计划写的「207 / 178」逐字相符。

---

## Verdict

**PASS_WITH_WARNINGS** — counts: **0C / 2M / 4m**

**Vote: REVISE**

## 是否足以开始 Phase B

**不足以** —— R3 四题我逐条实证闭合 (两份嵌入证据逐字节复跑通过、生成器 REGEN_IDENTICAL、真提交 `12c870d` 翻 `own`、四份 SKILL.md 全集与行尾逐份核对、协调 ref 四态我从零重建复现), 证据层是四轮以来最硬的一版; 但 M1 让本轮刚加上的 standards 重测在「standards 真动过」时静默判过 (三态里两态输出相同, 只有退出码能分开), M2 让手写的 Phase D 漏掉 Rule #9 SOT 明令「任何 cycle 都不可跳过」的 latest.md 子步骤。两处都是定点文字修改 (加一条 fetch + 判退出码; TASK-031 的 D.3 展开三小步并登记 latest.md), 不触任务结构与设计取舍; 改完仍须先过 `owner_gates` 第 1 项的 owner 门才进 B.1。
