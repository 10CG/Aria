---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-13T02:20:00.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R5 — code-reviewer — Spec A `premerge-gate-branch-existence`

**VOTE: REVISE · VERDICT: PASS_WITH_WARNINGS (0C + 3M + 3m = 6)**
**引入率 (本席): 5/6 = 83%** (仅 m-2 的路径错字非本轮引入)

审视角度 (席位分工): 逐字核对 —— 末尾溯源表回源抽查 / `SC-A*` 号段无冲突 / 所有 `file:line` 属实 /
条款间自相矛盾。基线: `aria` submodule HEAD = `af87cae` (与 Spec 声明的基线一致, 已 `git rev-parse` 核)。

---

## 0. 先说结论 (owner 要的四个答案)

**① R4 的 12M 里它修的 8 类**: 我逐条回源, **7 类真闭合, 1 类闭合了「可执行内容」但留下定义面残余**
(详见 §2)。**没有一类是「只写下来」**。

**② 引入率预测**: 执笔方预测 **总数 14–20 (点估 17) · Critical 0 · Major 5–8 · 引入率 70–85%**。
本席给出 **6 条 (0C + 3M + 3m), 引入率 67%** —— **Critical 预测准 (0)**;
**Major 单席 3 条**与「五席合计 5–8」这个量级**一致偏低**; **引入率 83% 落在预测区间 70–85% 内**。⚠️ 但请注意一个口径事实: 本席 3 条 Major **全部**由 R4-fix 引入 (3/3 = 100%),
**minor 里 2/3 由 R4-fix 引入** —— 即「少改」策略把引入压在了**总量**上, **没有压在严重度上**。

**③ 关于它主动留痕的自证点 (`evaluate_path_coverage=3` 编造 → 实跑推翻为 1)**:
**本席明确判「不计为 finding」**, 理由与证据见 §4。**并且**: 我实跑复核了该留痕块里的全部三个数,
**全部属实** (`evaluate_path_coverage`=1 · `resolve_ci_backend`=2 於 `:241`/`:319` · §C.2.4 内唯一)。
⇒ 「新写文本 = 净增表面」这句话**成立**, 但它的正确形式是「新写文本里**含错值/欠定的那部分**是净增表面」;
本块两者皆无, 计它为 finding 会把「自查并当场推翻自己」这个唯一在降低缺陷密度的行为反向计价。

**④ 全文件重复锚扫描 (不只验局部区间)**: 我对 `SC-A-doc` / `SC-A-step` / `SC-A-note` 的**全部**锚点
做了不限章节的全文件扫描 (命令与输出见 §3)。**结果: R4 为 `SC-A-note` 修好了这个病, 但同一份
commit 把规则的作用域逐字只扩到 `SC-A-step`, 漏了 `SC-A-doc` —— 而 `SC-A-doc` 的操作数正是由
那条被实测证明不唯一的 `**Output schema**` 锚定位的。** 这是本轮 M-2。

---

## 1. Findings

### M-1 (major, 引入=是) 表 1 `SC-M3c` 行仍引 `B :161` 作「5 步移入折叠块」的依据 —— 与同文件 `:244-246` 逐字互斥

**Locator**: `proposal.md:311` (表 1 `SC-M3c` 行) × `proposal.md:244-246` (R4 新写的更正框)。

- `:311` 逐字: 「B 的 D1 把步骤 1-5 整体折叠 (**B `:161`** 逐字), **A 的新步骤届时就在折叠块内**」。
- `:244-246` (R4-fix **本轮新写**) 逐字: 「上一版写 B `:156`/`:161`, **其中 `:161` 逐字是
  「折叠块**之外**必须留下 `<MAIN_BRANCH>` 的取值来源」, 与「折叠」这件事无关**; 承载「5 步移入折叠块」的
  是 **B `:154`** 的节标题, 折叠标记本体在 **B `:156`**」。
- **实跑回源** (`sed -n '161p' openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md`):
  「🔴 **折叠块之外必须留下 `<MAIN_BRANCH>` 的取值来源** (**SC-M16** 钉住)…」⇒ **`:244-246` 是对的, `:311` 是错的。**
- **怎么会红 / 为什么重要**: 任何按 `:311` 复跑的人拿到的那一行**不含**它被援引来支撑的内容;
  而 `SC-M3c` 的这次改判**正是**「类级 `--` flag 禁令」(全 Spec 对 hunk ① 最硬的一条约束) 的唯一起因。
  更要紧的是**同一份文件对同一行给出两个互斥的逐字引述** —— 这不是「陈旧锚」, 是 R4-fix
  **只扫了同形位置的一个实例**造成的自相矛盾 (memory `fix-the-class`; 与 R4 自己在 §非目标 修的第四份拷贝同形)。
- **最小修法**: `:311` 的 `B :161` → `B :154` (节标题) 或 `B :154`/`:156`。**一处字面替换, 零新增断言面。**

### M-2 (major, blocks_phase_b, 引入=是) R4 新加的「章节内首个匹配」规则逐字只扩到 `SC-A-step`, 漏了 `SC-A-doc` —— 而 `SC-A-doc` 的锚正是被它实测证明不唯一的那个

**Locator**: `proposal.md:785` (`SC-A-doc` 行) × `proposal.md:787` (`SC-A-note` 行内 R4 新加的限定)。

- `:787` (R4 新写) 逐字承认病因: 「**这两个锚在全文件都不唯一, 与 `SC-A-step` 旧锚同款病, 而同一 commit
  里只给 `SC-A-step` 加了这条限定**」, 并把规则写成「两个锚一律取 `### C.2.4` 标题行之后、下一个 `###`
  之前的首个匹配, ⛔ 不得对锚点短语做不限章节的全文件搜索」; 作用域句逐字只有一句:
  「⚠️ **`SC-A-step` 的起点/终点锚同受本条约束**」。**`SC-A-doc` 一个字未提。**
- `:785` (`SC-A-doc`) 的操作数逐字 = 「从 `SKILL.md` **§C.2.4 Output schema json 块** (`:265-277`)
  **实际解析**出的顶层键名集合 (**⛔ 不得硬编码 doc 侧**)」——**必须按锚定位**:
  §Impact hunk ① 要在 `:242` 附近插一个编号步骤, `:265-277` 这组行号在落地分支上**必然漂移**,
  「⛔ 不得硬编码」又堵死了钉行号这条路。
- **实跑证据** (全文件扫描, 非局部):
  ```
  grep -n '\*\*Output schema\*\*' SKILL.md  →  264, 501
  ```
  两个候选块各自跑 `SC-A-doc` 自己钉死的正则 `^  "([A-Za-z_]+)":`:
  ```
  anchor :264 -> block 266..276 keys(7) = [verdict, pr_ci_status, in_flight_runs,
                                           primitive_used, primitive_version_sha, raw_message, path_coverage]
  anchor :501 -> block 503..520 keys(3) = [verdict, affected_submodules, telemetry_files]
  ```
  (`:501` 属 `### C.2.4.5 Submodule Pointer Regression Gate`, 实读 `:376`–`:569`。)
- **怎么会红**: 取末次匹配 / 把「§C.2.4」读成含 `C.2.4.5` 的实现, 解析到 3 键集,
  **与 `_build_output` 的 7/8 键永不相等 ⇒ `SC-A-doc` 与被测实现无关地恒红 = 零信息**
  (memory `false_green_dual_is_permanent_red` —— 正是 R4 接受 qa-engineer `Major-1` 时用的同一条判据)。
- **最小修法**: 在 `:787` 那句作用域里加四个字 ——「`SC-A-step` **与 `SC-A-doc`** 的锚同受本条约束」。
  **零新增判据, 一处字面扩写。**

### M-3 (major, 引入=是) `B detailed-tasks.yaml:488` 两处行锚已失效 —— 失效者正是 R4 fix 窗口自己对该文件的编辑

**Locator**: `proposal.md:327` (表 1 末段) + `proposal.md:863` (§交付义务 D.2 handoff 段)。

- 两处均逐字引「`detailed-tasks.yaml:488` 的「显式传 0 处」」。
- **实跑回源**: `sed -n '488p' .../premerge-gate-mainbranch-failclosed/detailed-tasks.yaml` ⇒ **`  verification:`** (裸 YAML 键)。
  被引的那句今日在 **`:308`** (`grep -n '实测 24 处'` ⇒ `308:  - 实测 24 处 gate_check( 调用点、显式传 main_branch 的 0 处 — 补完后应为 24/24`)。
- **它是本轮打断的**, 有硬证据:
  ```
  git show ff847fb:.../detailed-tasks.yaml | grep -n '实测 24 处'   →  488:...   (R3-fix 时正确)
  git log --oneline -1 -- .../detailed-tasks.yaml                  →  f5b845c  (R4 窗口内「补执行 DEC §5.3」那次编辑)
  ```
  且 R4 本席报告 `:54` 逐字把 `:488` 记为**已实读核对通过** —— 即 R4 当时是对的, 是 R4-fix 自己的
  cancelled 留痕编辑把行号推到了 308, 而 A 侧两处引用未随迁。
- **怎么会红 / 为什么重要**: `:863` 把这条锚写进 **D.2 handoff 的必交接项**;
  按它复跑的接收方落在一个空 YAML 键上。形状 = memory `cross-doc-claim-verify-at-target` 的镜像面
  ——「在 B 里动了刀, 没回 A 扫自己引它的地方」。这也是本轮「少改」策略唯一一处**没算清爆炸半径**的动作。
- **最小修法**: 两处 `:488` → `:308`。**两处数字替换。**

### m-1 (minor, 引入=是) BLOCKER 自查留痕里的「实跑得 **4**」今日实跑得 **7**, 且这一轮是被 R4-fix 自己推到 7 的

**Locator**: `proposal.md:88`。

- 逐字: 「初稿写的是不带 `^` 的 `grep -c '### Key Deliverables'`, 而**本段正文自己就含这个串** ⇒ **实跑得 4**」。
- **实跑**: `grep -c '### Key Deliverables' proposal.md` = **7** (行号 84 / 86 / 88 / **101** / **105** / 842 / 843)。
  R4 本席已报过该值当时为 **5** (m-2, 被判定不修); **`:101` 与 `:105` 是 R4-fix 本轮新写的 delegate 更正框**
  ⇒ 5 → 7 是本轮自己造的。
- **怎么会红**: 这是一个**自指量** —— 任何对本文件的编辑都会改它, 所以它作为「实跑值」永远追不上。
  留着它就等于在一份反复强调「任何数必须实跑」的文件里挂一个**结构上不可能保持为真**的数。
- **最小修法 (且这次是能一劳永逸的)**: 不要修数, **删掉那个绝对值**, 改写成「该命令的计数**恒 ≥ 本段自身的出现次数**,
  故恒 > 0 ⇒ 它从写下那一刻起就不可能得 0」。这句在任何未来编辑下都为真。
  ⚠️ 这一条正好反驳了 R4 对「计数类 minor」的统一理由 (「改一处文字→下一轮多一批同形条目」):
  **对自指量而言, 换掉「量」而不是「值」是终止序列的唯一办法** (memory `redfix-change-quantity`)。

### m-2 (minor, 引入=否) `phase-d-closer/fetch_gate.py` 路径少一段, 实际是 `phase-d-closer/scripts/fetch_gate.py`

**Locator**: `proposal.md:950` (§非目标)。

- 逐字: 「`phase-d-closer/fetch_gate.py` 的字面 `("master","main")` 回落」。
- **实跑**: `find aria -name 'fetch_gate*'` ⇒ **`aria/skills/phase-d-closer/scripts/fetch_gate.py`**;
  `grep -n` 该文件 ⇒ `55:_DEFAULT_BRANCH_FALLBACKS = ("master", "main")` ⇒ **内容属实, 只有路径缺 `scripts/`**。
- **对照**: 同一行的兄弟 `state-scanner/lib/worktree_manager.py:170` 我实读 = `    base_branch: str = "master",` ⇒ **完全正确**。
  两者写成同一形状 (skill/相对路径), 一对一错。
- **怎么会红**: §非目标同一行逐字写「⚠️ **Phase B 实施者不得照抄 `fetch_gate.py`**」——
  实施者按给出的路径 `ls` 会得 "No such file"。危害小, 但它落在「不得照抄」这句**禁令的寻址**上。

### m-3 (minor, 引入=是) 「碰撞面**已在源头消除**, 不再依赖 handoff 纪律」过强 —— B 侧 `TASK-001` / `TASK-021` (均 pending) 仍逐条点名已过户的 `SC-M6/M7/M8/M13/M14`

**Locator**: `proposal.md:316` 行末 + `proposal.md:866-872` (R4 新写的「本段不再承载它」框)。

- **R4 做对的部分我已复核属实**: `detailed-tasks.yaml` 21 条 task **一条未删**,
  status 分布 = **pending 15 / cancelled 6**, cancelled 的正是 `TASK-003/004/005/007/008/009`,
  `TASK-006` 正确地仍 pending; 且 cancelled 各条 notes 末尾逐字带「应承接见 A proposal §What Changes」。
  ⇒ **实现级重复 (重复 `_verify_branch_exists` 定义 / merge conflict) 这条腿确实被消除了。**
- **残余**: 我逐 task 解析 SC 归属得 —— `TASK-001` (**pending**, 「TDD 前置 — 全部机械断言的空壳, 先看到全红」)
  的 owning SC 列表含 `SC-M6/M7/M8/M13/M14`; `TASK-021` (**pending**, 终局收口) 按 `B tasks.md:122` 逐字
  要求「**SC-M1 … SC-M18 全部为期望值**」。这两条**都未被 cancelled、也未被加注**。
- **怎么会红**: B 的实施者执行 `TASK-001` 会为已过户号段写红壳; 执行 `TASK-021` 时那批 SC
  在 B 内**无任务可使其转绿** (使其转绿的六条已 cancelled)。
- **为什么记它**: A 在同一处删掉了原有的 handoff 兜底 (`:872` 逐字「本段不再承载它」)。
  ⇒ 形状 = A 自己反复援引的「有记录 ≠ 有路由」。**最小修法**: 把该句由「已在源头消除」收窄为
  「**实现级**碰撞已在源头消除; **SC 级** (`TASK-001` 空壳 / `TASK-021` 终局全绿) 仍在 B 侧, 交 D.2 handoff」。

---

## 2. R4 的 12M —— 逐条回源, 区分「写下来」与「闭合」

| R4 finding | 处置 | 本席复核 (实跑/实读) | 判定 |
|---|---|---|---|
| tech-lead F-1 「移入 SC ⇒ 路径 B **必然**出六条 TASK」不成立 | 已改 | `task-planner/SKILL.md:59-67` 逐字复读 ✅ / `DUAL_LAYER_SPEC.md:90-93` 三项各带用途 ✅ / `grep -rn 'Success Criteria' task-planner/` = **2** ✅ / A 的 `^## What$`=0 · `^### Key Deliverables`=0 ✅ | **真闭合** —— 「必然读到」保留、「必出 TASK」删除, 与 §交付义务表六项「有机械闸门吗: 没有」自洽 |
| tech-lead F-2 = CR M-1 = QA Major-2 §非目标第四份 landmine 拷贝 | 已改 | `:936-943` 实读: 已改为「只标注本步自身的作用域边界并指向 `#137`, ⛔ 不得标注『步骤 3 硬编码 main』」; 与 §残余暴露 R3 框 / `SC-A-step` (c-含) / §Impact hunk ① 四处口径**逐字一致** | **真闭合** |
| tech-lead F-3 DEC §5.3 是 A.1 动作而非 handoff 备忘 | 已执行 | `DEC:122-132` 实读 (§5 第 3 条逐字「须留 cancelled 痕迹, 不得静默删」; 抬头「裁定人: owner」「状态: Approved」) ✅; B 侧 status 分布 **pending 15 / cancelled 6** ✅ | **真闭合** (残余见 m-3, 不推翻闭合) |
| tech-lead F-4 「跨模块」腿是自造判据 | 已改 | `LEVEL_GUIDE.md:156-160` 四条件 OR 列表逐字对上 ✅ · `:162`「跨模块 → 自动提升为 Level 3」✅ · `:29` Q2 三腿 ✅ · `:26` 确为 Q1 的 LEVEL 1 行 ✅ · `project.md:117`/`:116` 两行确如所述 ✅ | **真闭合** —— 四条件逐条对账 + 条件③ 上呈 `D-c`, 不再自造谓词 |
| tech-lead F-5 Level 的 (c) 腿是版本裁定的函数, 却判「不得合并处理」 | 已改 | `:162-166` 实读: 改为「不得混为一题, 但须**按序裁 —— 先版本, 后 Level**; 版本裁 MAJOR 时直接 Level 3」 | **真闭合** |
| tech-lead F-6 `SC-A-step (a)(b)` 过度收口 | **明确不修** (唯一一条) | 见 §5 逐条验 | **判对了、按理由不修** —— 理由成立 |
| CR M-2 `SC-A10c` 与适用集配方相反 | 已改 | `:718-725` 实读: 「适用集全体 `probe()`→True; **`precheck()`→(True,"") 适用于除 `SC-A10c` 外的 10 条**」; 我实读 `ci_backends/base.py:79-85` 逐字「**Default: always (True, "")**」✅, `tests/:272-276` 先例 `mock_backend.precheck.return_value=(False,…)` ✅ | **可执行内容闭合; 定义面残余** —— 适用集的准入句仍是「凡断言**核验确实发生了**的 SC」, 而 `SC-A10c` 断言的恰是核验**没**发生。**两个独立实现者今日不会分歧** (例外条文已逐字点名), 故不另开 finding, 但这是 12 条里唯一没做干净的一条 |
| CR M-3 定档两条 SOT 行锚都不落在被引文本上 | 已改 | 同 F-4 行 ✅ | **真闭合** |
| CR M-4 O-1 的 gitlink 证据命令恒空 | 已改 | **我三跑复核**: `git diff --submodule=short -- aria` 干净树 = **0 行**; 换用的 `git show --submodule=short fb5ed36 -- aria` = **2 行** (`-Subproject commit 183836b…` / `+Subproject commit af87cae…`); 对未 bump 的 `98ad1f5` = **0 行** ⇒ **两向可区分** ✅ | **真闭合** (本席上轮提的那条, 换的是量不是阈值) |
| QA Major-1 `SC-A-note` 锚点在全文件不唯一 | 已改 | `grep -n '\*\*Output schema\*\*\|\*\*配置参数\*\*:' SKILL.md` = **264 / 281 / 501 / 523** ✅ 与 R4 所述一致; `### C.2.4` = `:218`, 下一个 `###` = `:306` ✅; §C.2.4.5 = `:376`–`:569` ✅ | **对 `SC-A-note` 真闭合; 但类没扫干净 → M-2** |

⇒ **8 类里 7 类真闭合, 1 类 (CR M-2) 内容闭合而定义面残余; 0 类是「只写下来」。**
**判据说明**: 我对每条都做了独立回源 (命令见各行), 不采信 Spec 内的自述。

---

## 3. 全文件重复锚扫描 (owner 点名的复查项 —— 不只验局部区间)

对**全部** doc 侧机械 SC 的**每一个**锚点做了不限章节的扫描:

| 锚点 | 全文件命中 | 归属 SC | 有无「章节内首个匹配」保护 | 结论 |
|---|---|---|---|---|
| `**执行流程**:` | `238` / `582` (`:582` 属 §C.2.5) | `SC-A-step` 起点 | ✅ 自带「首个」+ R4 明文扩入 | 安全 |
| `**Subprocess 调用规范**:` | `257` (**唯一**) | `SC-A-step` 终点 | — | 安全 |
| `**Output schema**` | `264` / `501` | **`SC-A-note` 起点 + `SC-A-doc` 操作数** | `SC-A-note` ✅ / **`SC-A-doc` ❌** | **→ M-2** |
| `**配置参数**:` | `281` / `523` | `SC-A-note` 终点 | ✅ | 安全 |
| `_build_output` (docstring, `ast.get_docstring`) | **def 唯一** (`:232`) | `SC-A-note` (d) | 天然唯一 | 安全 |
| `evaluate_path_coverage` (SKILL.md) | **1** (`:242`) | R4 留痕块所引 | — | 安全 (留痕块自述属实) |
| `resolve_ci_backend` (SKILL.md) | `241` / `319` (`:319` 属 §C.2.4.X) | 同上 | §C.2.4 内唯一 | 安全 |

---

## 4. 关于「主动留痕自查」该不该计为 finding —— 明确回答

**不计。** 三条理由, 逐条可证伪:

1. **它没有把错值带进交付面。** 被推翻的 `evaluate_path_coverage=3` **从未成为任何判据的输入**;
   最终落纸的三个数我**逐个实跑复核全部属实** (=1 / =2 於 `:241`+`:319` / §C.2.4 内唯一)。
   审计计价的对象是**留在文件里的错误**, 不是**作者的中间稿**。
2. **反例检验**: 若判「该计」, 则等价于宣布「**推翻自己的中间结论 ⇒ 加一条 finding**」,
   而**不写这段 ⇒ 零 finding**。这条规则唯一稳定的均衡是**不留痕**, 而不留痕正是让
   `critique-repeats-error` 那类错误躲过审计的机制。⇒ 该判定会**反向选择**掉本轮唯一在降低缺陷密度的行为。
3. **「任何新写文本都是净增表面」这句是对的, 但它由本轮**别的**证据支撑, 不需要用这一块来支撑**:
   本席 3 条 Major **全部**落在 R4-fix 新写文本或其未扫的爆炸半径上 (M-1 `:244-246` 新框造成的互斥 /
   M-2 新规则的作用域漏项 / M-3 新执行的 DEC 动作打断的行锚), m-1 也是新写文本把 5 推到 7。
   ⇒ **给 owner 的净增表面证据是 5/6 = 83% (m-3 的过强断言同属 R4 新写), 与那段自查留痕无关。**

**⇒ 对本 Spec 该不该继续加轮, 这条留痕给出的是相反方向的证据**: 它证明执笔方**已经在写下之前自查**,
且这一轮 12 个触点里 **7 个真闭合**。真正没被压住的是**爆炸半径** (M-1/M-3 都是「改了 X 没扫引 X 的地方」)
—— 那是**机械可枚举**的一类, 不需要靠加轮解决 (见 §6 建议)。

---

## 5. 「明确不修的 15 条」—— 逐条判它的理由成立与否

### 那条 Major (`SC-A-step (a)(b)` 不补内容序断言) —— **理由成立, 且「改法欠定」与「不值得改」的区分站得住**

它给的三条依据我逐条验:

1. **「新增断言面 ≠ 修正」** —— 成立。这是一条**事实陈述** (新增 vs 修正), 不是价值评估, 不撞规则 #10。
2. **「新步骤锚 token 今日不存在, 要现编」** —— **成立, 且是三条里唯一承重的那条**。我实读 §Impact hunk ①:
   逐字只要求「写成**参数化的 helper 函数调用**形态」, **通篇未规定函数名须进 `SKILL.md`**;
   而 `SC-A-step` (c-含) 已经占用了 `#137` 这个 token ⇒ 若拿 `#137` 当第三个锚, 两腿耦合成同一个量。
   ⇒ **今日确实写不成「两个独立实现者会得同一结果」的形式** (memory `spec-underdetermination`)。
   ⚠️ 它自己删掉的那半个理由 (另两个锚也不唯一) 我复跑确认**确实不成立**
   (`evaluate_path_coverage`=**1** 唯一; `resolve_ci_backend`=2 但 §C.2.4 内唯一) —— **删对了**。
3. **「残余是『无从求值』不是假绿」** —— 成立。B 若折叠时改用无序列表, `^[0-9]+(\.[0-9]+)?\.` 提取序列为空,
   (a)「存在 N 满足 2<N<2.5」**判 False = 红**, 不是判 PASS。⇒ **失效方向是红/无从求值, 不是绿。**

⇒ **本席同意不修**, 并同意它写下的前置条件:「若 owner 要求本轮补, 须先裁定新步骤锚 token 的写法」。
**这是规则 #10 的正确用法** (把裁量交回 owner), 不是自我豁免。

### 14 条 minor 的三类统一理由 —— **两类成立, 一类不成立**

- **「措辞/定义」类 · 「悬空引用」类**: 统一理由 (「改一处文字→下一轮多一批同形条目」) **成立**,
  本席不再重复登记 (含 R4 f-9 archive `TASK-` 计数 · f-11 DEC §2 「6 条 vs 7 条 (含 `SC-M10`)」 ——
  两条我都独立实跑复核**确实仍在**: archive 四例的 `31/21/19/28` = **含 `TASK-` 的行数**,
  真实 task 条目为 **9/8/8/10**; `DEC:42` 逐字确为 **7 条**含 `SC-M10`。**结论均不承重**:
  四例 4/4 确为 Level 2 且均出 `TASK-{NNN}` ✅; `SC-M10` 的 A 侧同款 `SC-A10` 在场且 B 的
  `TASK-008` 已 cancelled ✅ ⇒ 不推翻任何处置)。
- **「计数/配平」类: 对**自指量**不成立** —— 见 m-1。自指量 (`grep` 本文件自身的串) 的正确修法不是改数,
  是**换量**; 沿用「不修」会让它每轮自动变假一次。这一条**不该与另两类同处理**。

---

## 6. 溯源表回源抽查 (22 行, 抽 20 行实跑/实读, 命令附上)

| 行 | 复核 | 结果 |
|---|---|---|
| 插入点 5 锚位 / 8 行号 | `sed -n` 逐行 | ✅ `:328` `:338` `:344` `:345` `:356` `:357` `:358` `:366` 全部命中 (`:358` 为多行调用首行) |
| `SKILL.md:255` = `fail` 走 `raw_message` | 实读 | ✅ 逐字 |
| `SKILL.md:279` = 四类早退保持六键 | 实读 | ✅ 逐字, 枚举恰 4 项 |
| `SKILL.md:259`/`:260` (含 `127 → no_ci_fallback`) | 实读 | ✅ 逐字 |
| 锚定 pattern 仍 fail-OPEN | **受控裸仓复跑** | ✅ `refs/heads/mast*` / `m[a]ster` / `maste?` **三者全部命中且 rc=0** |
| `ls-remote` 零命中亦返 rc=0 | 受控裸仓 | ✅ 零行 + rc=0 |
| `--exit-code` 无命中返 rc=2 | 受控裸仓 | ✅ rc=2 |
| `test_sc22` patch 全局 + `:723` 未传 `main_branch` | 实读 `:710`/`:718`/`:723` | ✅ |
| `gate_error` 全仓零消费者 / workflow-runner 四条臂 | `grep -rn 'gate_error' aria/` = **0**; `workflow-runner/SKILL.md:332-336` | ✅ 四条 exit condition, 无异常臂 |
| `_run_with_retry` 硬绑 binary / 只捕 `TimeoutExpired` / 无 cwd / `text=True` | 实读 `aether.py:164-187` | ✅ 四点全中 (docstring 逐字 "other exceptions bubble up") |
| `test_ci_backends.py` 25 tests 零命中 `_run_with_retry` | `pytest -q` = **25 passed**; `grep -c` = **0** | ✅ |
| 测试基线 111 | `python3 -m pytest -q tests/` | ✅ **111 passed** (46 + 25 + 40 逐文件复核) |
| `SKILL.md:243` 硬编码 `--branch main` 且是编号步骤本体 | 实读 | ✅ 逐字, 且 `grep -c 'aether ci status'` = **4** (`:167` `:168` `:243` `:244`) |
| 本仓 `ls-remote --heads origin main` = 零行 + rc=0 | 实跑 | ✅ |
| `workflow-runner` 全文零命中 `pre_merge_gate.py` | 实跑 | ✅ 带 `.py` = **0**; 不带 = **3** (`:342` `:373` + `gate_state_helper.py:37`), 与 R2 更正逐字一致 |
| v1.65.0 先例: 照跑 AB + 补步骤 2.5 | `CHANGELOG:181` + `SKILL.md:242` | ✅ 逐字「Rule #6 照跑 AB (3 eval × with/old/without 三臂」 |
| `issubclass(UnicodeDecodeError, OSError)` = False | 实跑 | ✅ |
| `ls-remote` 指向不存在路径 ⇒ rc=128 | 实跑 | ✅ 确定性 128 |
| 24/24 既有调用不传 `main_branch` | `grep -c` = 24 / 带 `main_branch` = **0**; 六处多行调用逐个实读 | ✅ |
| `_ProbeCacheResetMixin:59-80` | 实读 | ✅ docstring 逐字 + `setUp` 内 `mock.patch.object(gate,"evaluate_path_coverage",…)` |
| 真实调用点 25 | `grep -rn 'gate_check(' aria/ --include=*.py` | ✅ 测试 24 + `main():435`; 另 5 行确为 docstring/字符串 |
| §6 的 5 处不触达 (`:282`/`:301`/`:311`/`:321`/`:524`) | 实读三处外层 | ✅ `:311`/`:321`/`:524` 均在 `mock.patch.object(gate,"resolve_ci_backend",return_value=None)` 内; `:301` 为 `enabled:False`; `:276` 为 `precheck=(False,…)` |

**⇒ 溯源表 20/20 抽查属实。本轮我抓到的三条行锚问题全部不在这张表内, 而在正文的交叉引用里。**

---

## 7. SC-A* 号段与自洽性

- `grep -c '^| \*\*SC-A' proposal.md` = **18** ✅ 与抬头计数法逐字一致。
- **18 个 SC id 两两不重**: `SC-A6 A7 A8 A10 A10b A10c A11 A13 A14 A-zero A-order A-cli A-cwd A-doc A-step A-note A-sc22 A-baseline` = 恰 18。
- **号段无冲突**: `grep -rhno 'SC-[A-Za-z0-9]*' tests/*.py` ⇒ 既有仅 `SC-1/2/4/9/11/14/18/19/22/23/27` (无 `SC-A*`); B 侧全为 `SC-M*` ⇒ **零冲突** ✅。
- **可达前提配平**: 11 (适用集) + 2 (例外) + 3 (不适用) + 2 (元断言) = **18** ✅ 逐条点名核对无遗漏无重复。
- **打桩边界表配平** (我另算的一遍): 6 + 1 + 2 + 4 + 3 + 2 = **18** ✅ 且与可达前提**无成员冲突**
  (R2/R3/R4 三轮修的那三处互斥 —— 标签含义 / `SC-A11` / `SC-A10c` —— 今日全部一致)。
- ⚠️ 仍在的一处**非承重**配平瑕疵 (R4 f-7/m-1, 已被判定不修): 方向 2 归纳的
  「3 类 + 1 条 + **其余 14 条**」把 `SC-A-step` 计了两次, 按 18 行去重实为 **13**。
  **不重复登记** —— 它是摘要句, 不进任何判据。

---

## 8. 建议 (给 fix 执笔方; 与「少改」策略兼容)

**本轮建议只做 5 处字面替换, 不新增任何断言面**:

1. `:311` 的 `B :161` → `B :154` (M-1)
2. `:787` 作用域句加「与 `SC-A-doc`」五个字 (M-2)
3. `:327` + `:863` 的 `:488` → `:308` (M-3, 两处)
4. `:88` 的「实跑得 **4**」→ 改为**自指表述**, 不写绝对值 (m-1)
5. `:950` 的 `phase-d-closer/fetch_gate.py` → `phase-d-closer/scripts/fetch_gate.py` (m-2)

**m-3 建议同批做一句收窄** (「实现级已消除 / SC 级仍在 B 侧」), 无需改 B。

**⚠️ 并建议给 R6 加一道机械前置 (这是真正能把引入率打下来的东西)**:
本轮我的 3 条 Major **全部**是「改了 X, 没扫引用 X 的兄弟位置」。这一类**可以枚举**:
fix 提交前跑一遍
`grep -n 'B \`:[0-9]*\`\|\.md:[0-9-]*\|\.py:[0-9-]*\|\.yaml:[0-9]*' proposal.md`,
对**本次改动碰过的每个被引文件**逐个 `sed -n '<N>p'` 回源。
**这不是新增断言面, 是 fix 的自检步骤** —— 若这一步在 R4-fix 时跑过, 我这三条 Major 一条都不会存在。

---

**VOTE: REVISE** —— 3 条 Major 全部是**一处字面替换**级别的修法, 且其中 M-2 若不修, `SC-A-doc`
(hunk ② 的唯一机械锚) 存在**与被测实现无关地恒红**的落地分支。修法成本远低于风险。
**VERDICT: PASS_WITH_WARNINGS** (0C + 3M)。
