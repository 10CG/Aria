---
checkpoint: post_spec
round: 5
converged: false
overridden_by_user: false
incomplete: false
---

# post_spec R5 (定向轮) — phase-c-gate-path-coverage-not-applicable

> **性质**: owner 2026-07-30 裁定的**定向轮** —— 范围锁 A1 修订新增的 4 处, 不重审 R1-R4 已收敛内容。
> **席位**: 5/5 (config `teams.post_spec` 全员; owner 收的是范围不是席位, Rule #10 不自行降席)
> **verdict 分布**: **5/5 REVISE** · `scope_ok` **5/5 true** (零越界 finding)
> **timestamp**: 1785377400000 · 审计对象 SHA: 主仓 `3b1b7dc`

## 判定

**REVISE, 未收敛。** A1 修订本身引入了 6 个 critical 簇。

**元教训 (本轮最值钱)**: A1 是「把另一份 Spec 里**已实证**的发现搬进本 Spec」的操作。三条最严重的缺陷全部**产生于搬运本身**, 而非原发现有问题:

| 缺陷 | 搬运动作 | 后果 |
|------|---------|------|
| C1 | 搬了 L 的「位置式判据」, 但把剥引号排在首字符判定**之前** | 引号包裹的 leading-`*` glob 被判为 alias ⇒ **恒 wait 原样复发** —— 正是 L-3 要治的病 |
| C3 | 搬了 L 的命中判据 (L:184), **丢了**紧邻的作用域子句 (L:182) | 「区间」成为无定义悬空词, 承重算法缺一个自由变量 |
| M3 | 沿用了 R 原文 `:224` 的 memory 引用, 并**用它论证新决策** | 该 memory 不存在 ⇒ 「L-6 不并入」的关键依据失实 |

⇒ **搬运不是零风险操作**。已实证的发现在原语境里是正确的, 换语境后其前提子句、执行顺序、依赖引用都可能不再成立。这是 memory `feedback_fix_recurs_in_its_own_fallback_path` 的新 locus: **修复类操作在「移植修复」这个动作上重犯要治的病**。

---

## Critical 簇 (去重后 6 条)

### C1 — D12 剥引号在首字符判定之前 ⇒ 恒 wait 原样复发
**3 席独立命中** (tech-lead / backend-architect / code-reviewer) + **主控独立自验**

- **位置**: `proposal.md:63` (D12 判据) + `:202` (SC-30)
- **问题**: 判据写「剥块序列标记 `- ` → 剥**成对**首尾引号 → 然后判**首字符**为 `&`/`*`/`!`」。对 `- '**.js'`: 剥 `- ` → `'**.js'` → 剥引号 → `**.js` → **首字符 `*`** → 判为 alias ⇒ 该 workflow 记 covered ⇒ 恒 wait。
- **证据**: 逐步跟读判据文本即得; GHA 官方 paths 文档首例即 `'**.js'`。三席另各自构造了 `'**.md'` / `'!docs/**'` 等形态。
- **SC-30 抓不到**: 三条负控 (i) `run:` 块体 (ii) 注释 (iii) `paths: ['a/**']` —— **(iii) 的 pattern 首字符是 `a` 不是 `*`**, 结构上覆盖不到本缺陷。该负控例子系从 L 的 AC-5b 逐字照搬, **L 的盲区被连同抄入**。
- **建议修法**: 判定顺序改为「先判该行是否处于 `paths:`/`paths-ignore:` 的值位 → 是则**跳过构造扫描**; 否则再走剥离+首字符判定」。即**构造扫描与 pattern 值位互斥**, 不靠首字符区分。

### C2 — D12 缺「按 `:` 拆键值」⇒ 主流锚点写法检测不到
**backend-architect** (含跨席欠定实锤)

- **位置**: `:63`
- **问题**: 判据说「**值或键的首字符**」, 但未给出如何从一行文本切出「键」与「值」。同行形态 `push: &push_cfg` (最主流锚点写法) 在缺拆分步骤时首字符是 `p`, **不命中**。
- **证据**: backend-architect 与 tech-lead 两席对同一输入 `push: &push_cfg` **独立实现得出相反结果** (True / False) —— memory `feedback_spec_underdetermination_two_implementer_test` 的教科书式实证。
- **建议修法**: 明确「按**首个未被引号包裹的 `:`** 拆分键/值; 无 `:` 则整行视为值」, 并给 3 种形态 (`key: *a` / `- *a` / `*a`) 的逐例判定表。

### C3 — D12「区间」无定义 (搬运丢失作用域子句)
**code-reviewer CRITICAL** + tech-lead/qa-engineer MINOR + **主控独立自验**

- **位置**: `:63` (「对区间内每一行」)
- **问题**: 全文 grep「区间」**仅此一处**, 无先行定义。
- **证据**: L 原文 `:182` 有完整子句 —— 「构造扫描只在 **`on:` 键行到 `on:` 块结束的行区间内**进行 (区间由规则 1/5 已算出), 且跳过纯注释行」。A1 搬了 L:184 的命中判据, 丢了 L:182 的作用域。
- **建议修法**: 补回作用域定义。注意本 Spec 无 L 的「规则 1/5」编号体系, 需就地定义区间起止。

### C4 — reason 封闭集缺「构造级不确定致 covered」槽位 ⇒ SC-31(a) 自证不成立
**qa-engineer CRITICAL** + **code-reviewer MAJOR**

- **位置**: `:76` (规则 6) / `:203` (SC-31)
- **问题**: 既有规则 6 把「真实路径匹配」与「构造级不确定兜底」折叠成同一 reason `workflow-trigger-matched`。⇒ (a) 上报的 reason 是**事实错误** (没匹配上却说匹配了); (b) 对 D9 的 unknown-surface 义务**隐形**; (c) **SC-31(a) 声称「若把首行 `---` 误判为多文档分隔则必红」不成立** —— 两种实现在该 fixture 上输出逐字节相同。
- **连带**: C1 的缺陷也因此**静默** (被误判为构造级的 workflow 上报成"匹配成功")。
- **建议修法**: reason 封闭集增第 8 个终态 `workflow-construct-uncertain` (或 per-workflow 档单独记录并汇入 surface), 并重写 SC-31 的断言目标。

### C5 — SC-32 前两条无可计算主体, 且落点结构上永不执行
**qa-engineer CRITICAL** + **code-reviewer MAJOR** + **tech-lead MAJOR**

- **位置**: `:204` (SC-32) / `:226` (Impact) / `:234` (测试基线)
- **问题**: SC-32 标注「结构化测试 (非 LLM eval)」, 但前两条断言 (「解析出的套件路径 ==」/「基线路径 ==」) 的被测对象是**人/AI 执行期的 judgment**, 仓内不存在可调用的套件路径解析代码 ⇒ 无法证伪 = 恒真。且落点 `aria-plugin-benchmarks/` 被 `run_all_tests.sh` (硬编码 `SKILLS_DIR="skills"`) **结构上扫不到**, 却被计进 phase-c 的「~120+」基线。
- **建议修法**: 三条勘正改为**执行手册约束** (写进 AB_TEST_OPERATIONS.md + TASK 级 checklist), 不冒充 SC; 或只保留第 3 条 (metric 类型) 作为可对 `benchmark.json` 实跑的断言。

### C6 — 勘正 1 与 `:153` rule6_note 互斥: 排除 parent 套件后 AB 失去双臂对象
**tech-lead**

- **位置**: `:153` (rule6_note) / `:155` (勘正表第 1 行) / `:204`
- **问题**: 勘正 1 要求「必须点名全称 `phase-c-integrator-pre-merge-gate`, 不用裸名」, 而 `:153` 原文说要跑「phase-c-integrator: ab-suite **3 selected evals**」—— 那 3 个 eval 恰在被排除的 parent 套件 `phase-c-integrator.json` 里。**唯一有 LLM `evals` 的套件被机械排除** ⇒ 处方性指令面变更 (SKILL.md §C.2.4) 失去 AB 双臂对象。
- **建议修法**: 区分两个执行面 —— parent 套件 (LLM eval, 测指令面) **要跑**; `-pre-merge-gate` 套件 (structural fixtures) **也要跑**。勘正 1 的真实含义应是「不能**只**用裸名解析而漏掉 fixture 套件」, 不是「排除 parent」。

---

## Major 簇 (去重后 6 条)

| # | 簇 | 席位 | 要点 |
|---|---|------|------|
| M1 | D13 (`---`) 扫描区间 +「内容行」边界未定义 | BA / CR | 四个分叉点: `---` 自身算不算内容行 / 连续两个 `---` / `%YAML` 指令 / 精确匹配形态。且 D13 语义要求全文件扫, 与 D12 的 `on:` 块区间**不重合**, 两区间共存未成文 |
| M2 | SC-29(a) 红窗不成立 | QA / CR | (a) 未锁定非 ASCII 路径为变更集唯一匹配项 —— 同批一个 ASCII 匹配文件即可让「忘记 `-z`」的实现照样绿; (b) 红窗依赖未钉死的 `core.quotePath`, 实测 `quotePath=false` 下无 `-z` 同样绿 |
| M3 | **引用了不存在的 memory** | KM + **主控自验** | `feedback_test_worktree_fixture_isolated_tmpdir` 在 memory 目录**零命中** (文件名 + 内容)。出现在 `:224` (R 原文继承) 与 `:255` (A1 新增, **用它论证 L-6 不并入**)。真实先例在代码里 (`test_handoff_worktrees.py:9,36` 引「#135 $TMPDIR-leak lesson」issue) |
| M4 | AB 勘正表来源标注失实 | KM | 表头「L 侧 R2 5/5 席实地核实」把三项一并归因 post_spec-R2 5/5; 实测第 3 项 (metric 是 int) 首见于**另一检查点** post_planning-R2 的**单席** code-reviewer (major)。结论为真, 证据强度被抬高 |
| M5 | `:3` Status 行未随 A1 更新 | TL | 仍是 `Approved — ready for Phase B`; 实跑 state-scanner `_extract_status` 返回 `approved`, 机读层**看不见** `:4` 的闸门警告 ⇒ 下游可能据此起 Phase B |
| M6 | D12 与既有 `:68` glob 条款对 `!` 前缀所有权重叠 | TL | BA-1 钉死的「matcher 层对未建模 glob 语法判匹配」在生产路径不可达 (D12 先把 `!` 开头判成构造级) |

## Minor (7 条, 详见各席报告)

测试基线「~110+」全 13 份 R1-R4 报告零命中无核算依据 (KM) · `:48` gitlink 条款仍写无 `-z` 的命令字面, 全文唯一未同步处 (CR) · `rstrip("\0")` 与「滤空串」互相覆盖致 SC-29(b) 证不了 rstrip (CR) · D14 未规定字节→字符串解码契约而 `-z` 输出是原始字节 (CR) · 独立 tempdir 方案的前提 (须 `git init` + 两分支) 未成文 (TL) · 勘正 2 理据半失实, 「最近一次归档」实测是 `2026-07-20-v1.62.0-phase4-rule6` 非 state-scanner (TL) · 既有 `:62`「anchors」宽泛措辞与 D12 精确判据未建引用关系 (BA)

---

## 经实测确认**无需改动**的部分 (下轮免重复)

- **D14 (`-z`) 的三条技术前提**均实测成立 (BA / CR 各自验证)
- **AB 勘正 1/2/3 的事实内核**全部属实 (KM 内容级复核: parent 套件确含 3 个 LLM eval / `latest` 与最近归档经 `benchmark.json.skill_name` 复核确为 state-scanner / 基线文件 8 个 metric 全 `int 100` 且 `primary_pass_gate` 确为字符串)
- **L-7 拒并判断属实** (TL 实测 `:62` + SC-6 确实根本不从 `paths-ignore` 推导不覆盖)
- **L-6 拒并方向属实**, 但替代解的前提未成文 (见 Minor)
- **reason 封闭集与 8 条规则的互斥穷尽性**未被 A1 破坏 (TL 复核) —— 但缺一个槽位 (见 C4)
- **D13 的「列 0」限定词**已避开 L 侧 R3 踩过的 `echo "--- image size ---"` 坑 (CR)
- **§6 SKILL.md 同步清单不需为 A1 扩项** (KM: 8 处行号锚点仍精确对齐; D12-14 与既有 D5-D7 同属「2.5 Path coverage 评估」笼统桶)

---

## 下轮建议 (供 owner 裁)

本轮 5/5 REVISE 且 6 个 critical 簇**全部落在 A1 新增的 4 处**内 —— 定向范围选得准, 但也说明 A1 的起草质量不达标。

判据参考 memory `feedback_stop_adding_rounds_when_major_count_flattens`: 本轮是 A1 的**第一轮**审计, critical 尚未开始下降, **不属于「加轮收不敛」的形态**。R5-fix 后再评估。

三条 critical (C1/C3/M3) 已由主控独立自验属实, 不需复议。
