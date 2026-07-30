---
checkpoint: post_spec
round: 6
converged: false
overridden_by_user: false
incomplete: false
---

# post_spec R6 (新鲜眼睛) — silent-failure-hunter

**verdict**: REVISE
**scope_ok**: true
**counts**: critical=2 major=8 minor=7

**审计对象**: `openspec/changes/phase-c-gate-path-coverage-not-applicable/proposal.md` (A2 版, 379 行)
**席位**: 1 (silent-failure-hunter, 未参与 R1-R5)
**timestamp**: 1785380000000

**completeness**:

- ✅ **已审完**: (1) 值位互斥 D12-(2) 全部三问 (块边界计算 / 三层嵌套 / 反方向过度排除 / 判定表覆盖度); (2) A2 六个 fix (C1-C6) 逐个复发筛查 + M3/M5/M6 附带核验; (3) D13 四个边界逐条; (4) SC-29(a)(b)(c)(d) / SC-30(i)-(ix) / SC-31(a)-(e) / SC-32 逐条「它怎么会红」; (5) 专长视角四问 (兜底吞信息 / `uncertain_workflows` 有无消费方 / 6a 路径 / covered 可辨性 / 永不 raise 的捕获后可观测性)。
- ✅ **实跑证据**: PyYAML 6.0 验 4 种 YAML 形态 (下 C-1/C-2 证据); 实跑 state-scanner `_extract_status`+`_normalize_status` 验 M5; 实读 4 份真实语料; 实测 `aria` 为 gitlink 且 `aria-plugin-benchmarks/` 属主仓 tracked; 实读 pinned `benchmark.json` 全 8 metric 与 `primary_pass_gate` 形状; 实读 `run_all_tests.sh:29,48`; 实读 `aria/skills/phase-c-integrator/SKILL.md:236-262`; 实读 A2 新引的代码先例 `test_handoff_worktrees.py:9,36` + `test_git_operation_detection.py:92`。
- ⚠️ **未审 (缺口, 下轮或 owner 自行决定是否补)**:
  1. **SC-1~28 本身未逐条复核** (按 owner 定的范围排除; 但 SC-6 / SC-25 因被 A2 的 6a/6b 二分改变了期望输出而**破例纳入**, 见 M-3)。
  2. **§6 SKILL.md 同步清单的 8 处行号锚点只抽验了 `:236-262` 一处** (verdict/路由段, 锚点对齐属实), 其余 7 处未逐一实读比对。
  3. **§7 主仓 `.aria/config.json` 三字段退役 / DEC 存档时序**未审 (R1-R4 既有, 且 A2 未动)。
  4. **未审 `phase-c-integrator-pre-merge-gate.json` 6 个 fixture 的实际内容**与 SC-2/9/10 的形态相关性 (CR-4 声称)。
  5. **未跑任何 AB / 未执行 benchmark** (只读约束)。
- 本轮为单席轮, 上述缺口无其他席位可补。

---

## A2 六个 fix 的复发筛查

「复发」判据 = 该 fix 新写的条款/兜底/落点上, 是否重犯它自己要治的病 (memory `feedback_fix_recurs_in_its_own_fallback_path`)。

| fix | 是否在自身复发 | 依据 |
|---|---|---|
| **C1** 值位互斥 (D12-2) 治「leading-`*` glob 被判 alias ⇒ 恒 wait」 | **是, 两处 (双 CRITICAL)** | (a) 排除条件写死「缩进 **>** 该键行缩进」, 而 YAML 合法的**同缩进块序列** (`    paths:` + `    - '**.js'`, PyYAML 实测 OK) 不满足 ⇒ 不被排除 ⇒ 走 (4) 剥 `- `+剥引号 ⇒ 首字符 `*` ⇒ 判 alias ⇒ **恒 wait 逐字复发** (C-1); (b) 排除是无条件的, 于是 `paths: *alias` / `- *alias` 这类**真 YAML 构造**被当 pattern ⇒ 假 not_applicable, 把 C1 的 fail-CLOSED 病换成了 **fail-OPEN** 病 (C-2) |
| **C2** 键值拆分 (D12-3) 治「`push: &push_cfg` 漏判」 | **否 (判定面); 定义顺序自指 (m-1)** | 8 行判定表逐行走查, `push: &push_cfg` / `<<: *base` / `tags: !!str foo` 均确定命中, 未发现新漏判。但 (2) 需要「该行的**键**」才能排除, 而「键」的提取规则定义在 (3), (3) 又只对「未被 (2) 排除的行」适用 —— 定义顺序不闭合 (未构造出结果分叉例) |
| **C3** 区间就地定义 (D12-1) 治「区间悬空」 | **否** | (1) 起止定义完整 (起点 = 顶层 `on:` 物理行; 终点 = 首个缩进 ≤ 的非空非注释行; 无则文件末尾), 且**显式**声明空行/纯注释「既不参与判定, 也不终止区间」。D13 的全文件区间与之并存也已在 `:92` 分别声明。唯一残缺: 未定义「找不到顶层 `on:` 键」分支 (见 OUT_OF_SCOPE) |
| **C4** reason 二分 + `uncertain_workflows` 治「构造级 covered 被折叠成事实错误的 matched」 | **是, 三处 (M-1 / M-2 / M-3)** | (i) 同一个病在**兜底捕获**分支未治: 「永不 raise ⇒ 内部全捕获 ⇒ unknown + reason」而封闭集 8 个 reason 无 internal-error 槽 ⇒ 内部异常只能冒用 `git-diff-failed`/`workflow-parse-failed` = 事实错误的 reason (M-1); (ii) A2 自己点名的 **6a 分支** (`:118`「否则…在 6a 路径上再次隐形」) 既无 SC 也无正确文案 (M-2); (iii) 二分未回填**既有 SC-6 / SC-25** —— `paths-ignore` 与 `pull_request_target` 是最常见的两个 6b 成因, 实现把它们路由进 6a 仍能全绿 (M-3) |
| **C5** SC-32 收窄 + 落点移回 skills 域 治「恒真 + 落点永不执行」 | **是, 两处 (M-4 / M-5)** | (a) 新落点 `aria/skills/phase-c-integrator/tests/` 与被断言文件 `aria-plugin-benchmarks/...` **分属两个 git repo** (`aria` 是 gitlink, benchmarks 属主仓) ⇒ aria-plugin 独立 clone 下文件不存在 ⇒ 失败或静默 skip (M-4); (b) 保留下来的第 3 条断言的是**冻结归档**的类型, 不是本 change 产出的新 benchmark.json ⇒ 换了个形状的近似恒绿 (M-5) |
| **C6** 勘正 1 方向订正「两个套件都跑」 | **是, 一处 (M-6)** | 加了执行臂却没加对照臂: 勘正 2 只钉死 `-pre-merge-gate` 套件的基线; `ab-results/` 27 个归档中按目录名与 `skill_name` 两种线索检索, **零个 parent 套件 (LLM eval) 归档基线** ⇒ 被 C6 救回来的那条臂无历史对照 |

**附带核验的 M 级 fix**: M3 (引用换真实代码先例) — 实读 `test_handoff_worktrees.py:9` 「inside ONE isolated tempdir (NOT repo.parent) per the #135 $TMPDIR-leak lesson」+ `:36`「#135: never repo.parent」+ `test_git_operation_detection.py:92`「NOT repo.parent」⇒ **修对, 引用属实**。M5 (Status 行) — 实跑 `_extract_status` → raw 首段 `📝 **Draft (A2, post_spec R5-fix)**` → `_status_lifecycle_head` 在破折号处截断 → `_normalize_status` = **`pending`** ⇒ **修对, 机读层已看不到 approved**。M6 (`!` 所有权) — 两条路径 (glob matcher 判匹配 / D12 判构造) 终点都是 covered, 划分无行为差异, **无害**; 但同一句话对 `*` 不成立 (`*` 是**已建模** glob 字符, 不落「未建模 → 判匹配」兜底), 这正是 C-2 的入口。

---

## Findings

### [CRITICAL] C-1 值位互斥的块归属计算未成文 —— 同缩进块序列 / 空行 / 列 0 注释三种输入下 C1 原病 (恒 wait) 逐字复发

- **位置**: `openspec/changes/phase-c-gate-path-coverage-not-applicable/proposal.md:71` (D12 第 (2) 段 (b)); 对照 `:69` (第 (1) 段) 与 `:81`/`:87` (判定表第 1、7 行)
- **问题**: (2)(b) 的排除条件是「缩进 **>** 该键行缩进, 且在该键块结束前」, 两个承重量都没定义完整:
  1. **同缩进块序列**: YAML 允许块序列项与其父键**同缩进**。`    paths:` 后跟 `    - '**.js'` 时, 序列项缩进 = 4, **不满足 `> 4`** ⇒ 不被排除 ⇒ 落 (4): 剥 `- ` → `'**.js'` → 剥成对引号 → `**.js` → 首字符 `*` ⇒ **判为 alias ⇒ 该 workflow covered ⇒ 恒 wait**。这与 R5 C1 的失败链**逐字相同**, 只是入口从「剥引号顺序」换成了「缩进比较符」。
  2. **「该键块结束」无定义**: (1) 为 `on:` 区间**显式**写了「空行与纯注释行跳过: 既不参与判定, 也不终止区间」, (2)(b) **没有同款子句**。于是 `paths:` 列表中间的空行、或列 0 的注释行 (缩进 0 ≤ 4) 按字面终止 paths 块, 其后的 `- '**.js'` 不再被排除 ⇒ 同上恒 wait。
  3. **两个实现者会分叉**: 一个实现者补 YAML 常识 (序列项可同缩进 / 空行注释不终止块), 另一个照字面写 `indent > key_indent`。前者 not_applicable, 后者 covered——**结果相反**, 正是 memory `feedback_spec_underdetermination_two_implementer_test` 的形态。更糟的是, 若实现者的 **paths 列表解析器**也用「缩进 >」找列表项, 同缩进形态下 paths 会被解析成**空列表** ⇒ 零贡献 ⇒ **假 not_applicable (放行)**。同一个输入, 两个实现方向的错误**指向相反**: 一个恒 wait, 一个误放行。
- **证据**:
  - PyYAML 6.0 实跑: `on:\n  push:\n    paths:\n    - '**.js'\n` → **解析成功**, `{'push': {'paths': ['**.js']}}` ⇒ 同缩进形态是完全合法的真实输入, 不是病态构造。
  - 判定表 8 行全部假定缩进 6 的序列项 (`:81` `      - '**.js'`、`:87` `      - 'a/**'`) 配缩进 4 的 `paths:` (`:86`) ⇒ **表结构上覆盖不到同缩进形态**, 这与 R5 指出的「A1 负控 `'a/**'` 首字符是 `a` 所以抓不到 C1」是同一类盲区 (示例集与判据的失效域不重合)。
  - 本仓 4 份语料实读: 全部使用缩进 6 序列项 ⇒ 今天零代价。但这与 D13 自己在 `:99` 用的论证标准一致 —— 「本仓语料 4/4 首行为注释, 今天零代价, **但对采用者非零**」。同一标准必须对称适用。
- **建议修法** (方向 = 收紧块边界计算, 与危害「排除域算小了 ⇒ 误判构造 ⇒ 恒 wait」一致): 在 (2)(b) 就地写死三条, 不留给实现者补常识 ——
  1. 序列项归属: 「以 `- ` 开头且缩进 **≥** 该键行缩进的行, 与缩进 > 该键行缩进的行, 同属该键的值域」;
  2. 块终点: 「首个缩进 ≤ 该键行缩进**且不以 `- ` 开头**的非空非注释行 (无则区间终点)」;
  3. 空行与纯注释行**不终止** paths 块 (与 (1) 对齐, 一字不差地重述, 不靠「参见 (1)」);
  并在 SC-30 增负控 (x) 「`    paths:` + 同缩进 `    - '**.js'`」、(xi)「paths 列表中夹一个列 0 注释行后再跟 `- '**.js'`」, 期望**均不触发构造判定**。

### [CRITICAL] C-2 值位互斥无条件排除 ⇒ `paths:` 值域内的真 alias 被当 pattern ⇒ 假 not_applicable (fail-OPEN), 与 D2 承重原则直接冲突

- **位置**: `:71` (D12 (2) 排除规则)、`:73` (排除的理据)、`:101` (glob matcher 的 fail 方向)、对照 `:42` (D2 fail-toward-covered) 与 `:67` (anchors → covered)
- **问题**: (2) 说「一行被排除出构造扫描**当且仅当**… (a) 键是 `paths`/`paths-ignore`; (b) 处于其子块内」, 且「**被排除的行不做任何构造级判定**」。于是两种**真 YAML 构造**失去了唯一的检出通道:
  - `    paths: *common_paths` —— 键是 `paths` ⇒ (a) 排除。手写 parser 拿到的值既不是 block list 也不是 flow list (`:62` 只建模这两形), 落到未定义行为: 要么 paths 空列表, 要么把字面量 `*common_paths` 当 pattern。两条路都得不到真实 pattern (真实值可能是 `['**']`) ⇒ **零贡献 ⇒ not_applicable ⇒ 闸门在 CI 本该拦它时放行**。
  - `      - *p` (paths 列表项是 alias) —— (b) 排除 ⇒ 字面 `*p` 当 glob。**`*` 是本 Spec 已建模的 glob 字符** (`:101` 把未建模语法限定为「字符类 `[abc]` / 否定 `!` / 其他」), 所以它**不会**落进「未建模 → 判匹配 → covered」那个安全兜底, 而是走真实匹配 ⇒ 几乎必然不命中 ⇒ 同上假 not_applicable。
  - 对照: 落在同一位置的 `!` 有救 (`:73` 明确划给 glob matcher, 而 matcher 对 `!` 判匹配 → covered)。**唯独 `*` 两头落空** —— D12 不判它 (被排除), matcher 不兜它 (已建模)。
  - **与 D2 冲突**: `:42` 的核心原则是「任何不确定, gate 行为一律退回…现状」「绝不把『解析不了』当『无覆盖』」。`:73` 自己承认这里**确实不可靠区分** (「glob 的 `*`/`!` 与 YAML 的 `*`/`&`/`!` 在同一位置的字符上不可靠区分」) —— 承认了不确定, 却把它解到 not_applicable 一侧。A1 版本在这一点上是 fail-CLOSED (恒 wait, 难受但安全), A2 把它翻成了 **fail-OPEN**。对一个闸门放行判定, 这是方向性回归。
- **证据**:
  - PyYAML 6.0 实跑: `x: &common\n  - "a/**"\non:\n  push:\n    paths: *common\n` → 解析成功, `paths` 实际展开为 `['a/**']`; `x: &p "a/**"\n…\n      - *p` → 同样展开为 `['a/**']`。**两种 alias 形态都是合法且会真实扩展成 pattern 的**。
  - PyYAML 6.0 实跑: `- **.js` (裸的 leading-`*`) → **ScannerError while scanning an alias**。⇒ **YAML 层面, 值位上裸的 `*` 开头 token 必定是 alias, 而 glob pattern 必定带引号**。这条铁律说明:「按位置排除」不是唯一稳健解, 存在既治 C1 又不过度排除的判据 (见修法), `:73` 的「唯一稳健的区分是…按位置」是**过强断言**。
  - 现有 SC 无一覆盖: SC-30 的 9 个子用例里没有「alias 出现在 paths 值域」这一形态; SC-6 只测 `paths-ignore`。⇒ 该 fail-OPEN 路径**零红窗**。
- **建议修法** (方向 = 缩小排除面, 让被排除的只剩「确定是 pattern」的 token, 与危害「排除过头 ⇒ 漏检真构造 ⇒ 误放行」一致):
  1. 把 (2) 的排除条件从「位置」改成「**位置 ∧ 形态**」: 值域内的 token, **带成对引号者**判 pattern (排除); **裸 token 且首字符为 `*`/`&`/`!` 者仍判构造级** (不排除)。这直接消灭 C1 (`'**.js'` 带引号 ⇒ 排除) 而不放过 alias (`*common_paths` 裸 ⇒ 命中 ⇒ covered)。判据可证伪、可对字符级实现。
  2. 追加一条独立兜底 (即使不采纳 1 也必须有): 「`paths:` / `paths-ignore:` 的值**不是** block list / flow list 两形之一 (含同行标量、alias、空值) ⇒ 该 workflow 记**构造级不确定 → covered**」, 并入 6b 的成因列表 (`:111`)。
  3. SC-30 增正控 (xii) `paths: *common_paths` 与 (xiii) `- *p` (在 paths 子块), 期望 `decision==covered` ∧ `reason==workflow-construct-uncertain` ∧ `uncertain_workflows` 含该文件。

### [MAJOR] M-1 「永不 raise + 全捕获」没有对应的 reason 槽位 —— 内部异常只能冒用 `git-diff-failed`/`workflow-parse-failed`, C4 治的「事实错误 reason」在兜底分支原样复发

- **位置**: `:117` (返回契约「永不 raise (内部全捕获 → unknown + reason)」) vs `:116` (reason **封闭集 8 个** + 与测试矩阵**满射**) vs `:144` (D9 surface 的 reason 枚举)
- **问题**: 封闭集里能产出 `unknown` 的 reason 只有两个: `git-diff-failed` (规则 1) 与 `workflow-parse-failed` (规则 7)。可是全捕获兜底要接住的是**任意位置的内部异常** —— 最可能的来源恰恰是 A2 新引入的缩进块归属计算、键值拆分、`---` 扫描 (`:353` 自己承认这是「本轮最大的新机制」)。这类异常发生时:
  - 若按封闭集上报 ⇒ 只能说「git diff 失败」或「workflow 解析失败」, **两者都不是事实** ⇒ 这正是 C4 判定为 CRITICAL 的那个病 (「上报的 reason 是事实错误」), 只是换到了兜底分支;
  - 若上报第 9 个字面值 ⇒ **违反 `:116` 的封闭集与满射声明**, 且 `:144` 的 surface 文案 (只枚举了那两个 reason) 无处安放它。
  - 后果具体化: 值位互斥的实现里一个 `IndexError`, 会以「C.2.4: 评估失败 (git-diff-failed), gate 已按 covered 现状行为处理」的面貌出现。运维/AI 会去查 git 与 main ref, 而真正的 bug 在 parser 里, 且它每次都稳定复现却永远指向错误的方向。这是本项目 memory `reporter-miscite` 的机制化版本。
  - 为何评 MAJOR 而非 CRITICAL: gate 行为落 unknown ⇒ 退回现状 ⇒ **不产生误放行**。危害限于可观测性与误诊, 但它恰恰打在「评估器自身失效必须可见」(D9) 这条义务的正中间。
- **证据**: `:116` 逐字「产生终态判定的规则的 reason 字面值构成**封闭集**, **A2 后共 8 个**(…), 全部可断言且与测试矩阵**满射**」; 8 个字面值中无任何一个表示「评估器内部错误」。`:117` 逐字「永不 raise (内部全捕获 → unknown + reason)」——「reason」在此无所指。`:144` D9 warning 的 reason 括号里只有 `git-diff-failed` / `workflow-parse-failed`。
- **建议修法** (方向 = 给兜底一个诚实的出口, 与危害「冒用他人 reason ⇒ 误诊」一致):
  1. 封闭集增第 9 槽 `internal-error: <exception 类型 + 摘要>`, 明确它**只**由全捕获兜底产生, 且 `decision` 恒为 `unknown`;
  2. `:144` D9 surface 的 reason 枚举同步加它, 并要求文案点明「评估器自身异常 (非 git / 非 workflow 解析), 请报 issue」;
  3. 加 SC: 用 `mock.patch` 让内部某函数抛 `RuntimeError` ⇒ 断言 `decision=="unknown"` ∧ `reason.startswith("internal-error")` ∧ 不抛出。**这条 SC 同时是「永不 raise」承诺唯一的红窗** (现在没有任何 SC 验证它)。

### [MAJOR] M-2 6a 路径上的 `uncertain_workflows` 义务: 有条款、无红窗、且强制的文案在该路径上是事实错误

- **位置**: `:118` (「6a 优先, 但两个列表**各自照实填** —— 否则…在 6a 路径上再次隐形 (C4 的同一病在另一分支)」)、`:146` (D15 义务「覆盖规则 6a … 与 6b **两条路径**」)、`:145` (warning 文案)、`:253` (SC-30 正控前置条件)
- **问题**: A2 亲手指认了「6a 是同一个病的另一分支」, 然后:
  1. **没给红窗**。SC-30 的 9 个正控**显式要求**「该 workflow **无任何真实 paths 匹配**以免被 6a 掩盖」, SC-31(a) 断言 `uncertain_workflows == []` —— 全部 SC 都活在 6b 或空集。**一个只在 6b 分支填 `uncertain_workflows`、6a 分支恒填 `[]` 的实现, 能通过全部 SC**。「有记录 ≠ 有路由」在这里退化成「有条款 ≠ 有验收」。
  2. **强制的文案在 6a 上说错话**。`:145` 的 warning 逐字要求输出「已保守按 covered 处理 — 若本应 not_applicable 则表现为多余等待」。在 6a, covered 是**真实路径匹配**得出的, 不是保守兜底; 那个 workflow 读不懂与否不改变结论, 更没有「多余等待」。⇒ 强制 AI 在 6a 上报一句事实错误的解释 —— 与 C4 要治的「上报事实错误」同形。
- **证据**: `:253` SC-30 正控括号内逐字「(均须 `uncertain_workflows` 含该文件 ∧ reason==`workflow-construct-uncertain`, 且该 workflow **无任何真实 paths 匹配**以免被 6a 掩盖)」; `:254` SC-31(a) 逐字「`uncertain_workflows == []`」。SC 表 32 条中无一条构造「≥1 真实匹配 ∧ ≥1 构造不确定」的混合语料。
- **建议修法**: (1) 增 SC-33: 双 workflow 语料, W1 真实 paths 命中、W2 含 `&anchor` ⇒ 断言 `reason=="workflow-trigger-matched"` ∧ `matched_workflows==[W1]` ∧ **`uncertain_workflows==[W2]`** (缺一即红); (2) `:145` 文案拆两版 —— 6b 用现文案, 6a 用「本次 covered 由真实路径匹配得出; 另有 N 个 workflow 的触发定义含不建模构造 (`<…>`), 其覆盖贡献未参与判定」。

### [MAJOR] M-3 6a/6b 二分未回填既有 SC-6 / SC-25 —— 最常见的两个 6b 成因仍无 reason 断言, 实现把它们路由进 6a 也全绿

- **位置**: `:229` (SC-6 `paths-ignore` 在场)、`:248` (SC-25 `pull_request_target`) vs `:111` (6b 的成因列表明确含「`paths-ignore` 在场 / 其他不建模构造」)
- **问题**: A2 新建了 `workflow-construct-uncertain` 终态, 并把 `paths-ignore` 在场**明文**列为 6b 成因, 却只重写了自己新写的 SC-30/31, 没回填这两条既有 SC:
  - SC-6 期望列只有「`covered` (per-workflow 档)」—— 无 reason、无 `uncertain_workflows`;
  - SC-25 期望列只有「该 workflow `covered`」—— 同样两缺。
  - 后果: 一个把这两种成因照旧折叠进 `workflow-trigger-matched` 的实现**通过全部 SC**。而 `paths-ignore` 与未建模触发键是现实中**最高频**的构造级兜底成因 (远高于 anchor / 多文档分隔) ⇒ C4 的病在覆盖面最大的那条路径上存活。
  - 附带: 这也戳破了满射声明的成色 —— `:116` 说封闭集与测试矩阵满射, 满射只保证「每个 reason 至少被某条 SC 断言过」, 不保证「每条产生该 reason 的**路径**都断言了 reason」。
- **证据**: `:111` 逐字「**6b** 无任何真实匹配 ∧ 存在 workflow 因**构造级不确定** (D12 节点标记 / D13 多文档分隔 / **`paths-ignore` 在场** / 其他不建模构造) 判 covered → reason=**`workflow-construct-uncertain`**」; `:229`/`:248` 期望列实读如上, 无 reason。
- **建议修法**: SC-6 期望改为「`covered` ∧ reason==`workflow-construct-uncertain` ∧ `uncertain_workflows` 含该 workflow」; SC-25 同款追加 (`pull_request_target` fixture 须保证无真实匹配, 否则落 6a)。并在 `:116` 的满射措辞后补一句「满射按**规则分支**计, 非按 reason 字面值计」。

### [MAJOR] M-4 SC-32 的新落点跨 git repo 边界 —— 测试在 `aria` 子模块内, 被断言文件在主仓, 独立 clone 下必失败或静默 skip

- **位置**: `:255` (SC-32 落点与被读文件)、`:214` (可机械化分层表第 3 行)、`:276` (Impact 表)
- **问题**: C5 把 SC-32 从「`aria-plugin-benchmarks/` 结构上永不被执行」移到「`aria/skills/phase-c-integrator/tests/`, 在 `run_all_tests.sh` 扫描域内」, 但被断言的文件仍是 `aria-plugin-benchmarks/ab-results/2026-05-10-…/benchmark.json`。这两者分属**两个独立 git 仓库**: `aria` 是 gitlink (`160000`, 指向 `10CG/aria-plugin`), 而 `aria-plugin-benchmarks/` 由**主仓 Aria** tracked。于是:
  - 在 `10CG/aria-plugin` 的独立 clone (插件的正常分发形态) 中, 该路径**不存在** ⇒ 测试 error;
  - 若实现者为了让它绿而写 `skipIf(not path.exists())` ⇒ 得到一条**在 CI 与他机上恒 skip** 的测试 = 假绿, 正是 memory `feedback_false_green_dual_is_permanent_red` 与 C5 原本要消灭的「结构上永不执行」的**同一后果, 换了机制**;
  - 路径如何解析也没成文 (相对 cwd? 相对 `__file__` 上溯几层?) —— `run_all_tests.sh` 用 `find "$SKILLS_DIR" …` 且 `SKILLS_DIR="skills"` 是**相对 cwd** 的, 意味着套件必须在 `aria/` 下运行, 此时 benchmark 文件在 `../aria-plugin-benchmarks/…`, 一个 repo 外的相对路径。
- **证据**: `git ls-files -s aria` → `160000 6ffd8cd… 0 aria`; `.gitmodules` 中 `aria` → `10CG/aria-plugin.git`; `git ls-files aria-plugin-benchmarks` → 主仓 tracked (`AB_TEST_OPERATIONS.md` 等); `aria/skills/run_all_tests.sh:29` `SKILLS_DIR="skills"`, `:48` `for tests_dir in $(find "$SKILLS_DIR" -type d -name tests | sort)`。
- **建议修法** (方向 = 让断言与被断言物同仓, 与危害「跨仓 ⇒ 恒 skip 假绿」一致): 二选一并写进 Spec ——
  1. 把这条降级为**执行手册约束** (与已降级的第 1/2 条同处), 承认它无法在 aria 仓内机械化;
  2. 或改为断言**本 change 自己产出**的 benchmark.json (落 `aria-plugin-benchmarks/`, 由主仓侧的检查执行), 并**显式禁止** `skipIf(not exists)` —— 文件缺失必须红。
  无论选哪个, 都必须成文「路径解析基点」与「文件缺失 = 红, 不是 skip」。

### [MAJOR] M-5 SC-32 保留的第 3 条近似恒绿 —— 它守的是冻结归档的类型, 不是本 change 会写错的那个文件

- **位置**: `:255` (SC-32)、对照 `:204` (勘正 3 的真实意图) 与 `:206` (新增指标 / 新存档目录)
- **问题**: 勘正 3 要防的错是「**本次 AB 把 `measured` 写成 `\"100%\"` ⇒ 与既有 int 指标比较恒假 ⇒ 无红→绿窗口**」。SC-32 却去断言 **2026-05-10 那个已归档、本 change 一个字节都不会碰的 baseline 文件**的类型。它唯一可能变红的方式是有人去改历史归档 —— 与本 change 无关。⇒ 对「这次会不会写错」这个问题输出零信息, C5 判定的「恒真」换了个成因 (从「测 AI judgment」变成「测一个冻结常量」) 保留下来。
- **证据**: 实读该文件: 8 个 `structural_metrics.*.measured` 全部为 `int 100` (`unit: "percent"` 另存), `primary_pass_gate` 为 dict 且 `measured == "100%"` (str) —— **断言在今天就已成立**, 且该目录 `mtime` 为 2026-05-10。`:206` 明确本次要新建的是 `ab-results/<date>-v1.65.0-phase-c-gate-path-coverage-not-applicable/`, SC-32 完全不看它。
- **建议修法**: 把断言目标改成 (或至少扩展到)**本次新产出的** `ab-results/<date>-v1.65.0-…/benchmark.json`: 断言其全部 `structural_metrics.*.measured` 为 `int`、`primary_pass_gate.measured` 为 `str`、且新增的 `not_applicable` 指标 `measured == 100` (int)。这样「写成 `\"100%\"`」这个错在 Phase C 之前就会红。若嫌时序太晚 (AB 在发版前跑), 则退为执行手册 checklist, 并在 Spec 里说明「本条无 SC」而不是挂一条守错对象的 SC。

### [MAJOR] M-6 C6 的「两个套件都跑」缺配套基线 —— 被救回来的 LLM eval 臂没有历史对照

- **位置**: `:202` (勘正 1 的 A2 方向订正「两个执行面并列, 缺一不可」) vs `:203` (勘正 2 把基线**写死**为 `-pre-merge-gate` 套件的归档) 与 `:206` (「新增 `not_applicable` 指标无历史对照, 只需 `measured == 100`」)
- **问题**: C6 的修正是对的 (parent 套件是唯一含 LLM eval 的, 排除它会让处方性变更失去 AB 双臂对象), 但只补了执行面没补对照面: 勘正 2 钉死的那个基线是 **structural fixture 套件**的。parent 套件 (`ab-suite/phase-c-integrator.json`, 3 个 LLM eval) 要跑出「双臂」就需要它自己的 A 臂基线, 而 Spec 全文没有指定, `:206` 的免责句只覆盖「新增指标」, 不覆盖「新增套件臂」。⇒ Phase B/C 执行时会遇到一个 Spec 没答的问题, 大概率就地即兴 (跑完当场记一个 measured, 无对照 = 无回归检出力), 于是 Rule #6 的双臂在这条臂上退化成单臂。
- **证据**: `aria-plugin-benchmarks/ab-results/` 27 个归档中, 目录名含 `phase-c` 的**仅** `2026-05-10-phase-c-integrator-pre-merge-gate` 一个; 按 `benchmark.json.skill_name` 内容检索, phase-c 相关命中 **0** 个 (该 pinned 文件本身无 `skill_name` 键, 故此项检索为弱证据, 目录名检索为主证据)。`ab-suite/phase-c-integrator.json` 存在。
- **建议修法**: 在勘正 2 内分列两行 —— 「structural 臂基线 = (已写死的路径)」「**LLM eval 臂基线 = 需在 Phase B 前确认; 若确认不存在历史归档, 则本次为首建基线, 须在 rule6_note 显式声明『parent 套件本次无 A 臂, 结论只覆盖 structural 臂』**」。方向与危害 (无声地把双臂当成跑过了) 一致: 要么补对照, 要么把缺口写在脸上。

### [MAJOR] M-7 §6 SKILL.md 同步清单只点名 D8/D9, 未点名 A2 新增的 D15 —— 而 `:351` 仍宣称「§6 不需为 A1/A2 扩项」

- **位置**: `:156` (§6「`:246-249` 路由决策 + D8/D9 surface 义务」)、`:147` (「三义务写入 SKILL.md §C.2.4 指令面」)、`:351` (「§6 SKILL.md 同步清单不需为 A1/A2 扩项」)
- **问题**: A2 自己新增了第三条 surface 义务 (D15), 并在 `:147` 说「三义务」都要写进 SKILL.md。但 §6 的**逐处点名清单** —— 也就是 Phase B 真正照着改的那张表 —— 仍写「D8/D9 surface 义务」。同时 `:351` 把 R5 对 A1 的结论「§6 不需扩项」**原样延伸到了 A2**, 而 A2 恰恰新增了一条义务。⇒ 一条「有记录无路由」的典型: `uncertain_workflows` 的消费方只存在于 §5 的散文里, 没进入实现清单。§6 的座右铭是「逐处点名不数数」, 这里正是漏了一处点名。
- **证据**: `:156` 实读逐字「`:246-249` 路由决策 + D8/D9 surface 义务」; `:351` 实读逐字「§6 SKILL.md 同步清单不需为 A1/A2 扩项」。实读 `aria/skills/phase-c-integrator/SKILL.md:236-262`: 第 5 项「Verdict 计算」与第 6 项「路由决策」确在该锚点区间内 (锚点本身准确), 且现文只在 `fail` 分支输出 raw_message —— covered 路径**当前没有任何 surface 通道**, 因此 D15 若不点名就等于不存在。
- **建议修法**: `:156` 改为「`:246-249` 路由决策 + **D8/D9/D15** 三条 surface 义务 (含 covered 路径的 `uncertain_workflows` 上报 —— 现文 covered 路径无 surface 通道, 需新增)」; `:351` 删去或改为「§6 需为 **D15** 扩一处 (R5 结论只对 A1 成立)」。

### [MAJOR] M-8 SC-29(d) 恒绿 —— 「不抛异常, decision 有效」正好被「永不 raise 的全捕获」满足, 与它自己的期望列矛盾

- **位置**: `:252` (SC-29(d) 场景与期望列「(d) `text=True` 实现必红」)、`:56` (D14 第 3 条解码契约)、`:117` (永不 raise)
- **问题**: (d) 的断言写成「路径含非 UTF-8 字节序列 → **不抛异常, `decision` 有效**」。一个用 `text=True` 的实现会在 `subprocess.run` 里抛 `UnicodeDecodeError` —— 然后被评估器的**全捕获**接住, 返回 `decision="unknown"` + 某个 reason。此时:「不抛异常」✅ 成立 (被内部吃了);「`decision` 有效」✅ 也成立 (`unknown` 是契约里的合法值)。⇒ **要抓的实现全绿, 期望列「`text=True` 实现必红」不成立。** 这是全捕获的经典副作用: 它把崩溃翻译成了一个**长得很正常的合法返回值**, 于是任何「没炸就算过」形态的断言全部失效。
- **证据**: `:117` 逐字「永不 raise (内部全捕获 → unknown + reason)」; `:252` (d) 的断言文本与期望文本实读如上, 两者互斥。对比同表的 (a)(b)(c) 都钉死了具体终态 (`covered` / `count==3` / `empty-diff`), 唯独 (d) 只要求「有效」。
- **建议修法**: (d) 改为钉死终态: 「fixture 中该非 UTF-8 路径是**唯一命中** workflow paths 的文件 ⇒ 断言 `decision == "covered"` ∧ `reason == "workflow-trigger-matched"` ∧ `reason` **不以** `git-diff-failed`/`internal-error` 开头」。并把这条推广成一条 SC 编写规则写进 Spec: **「永不 raise」使得任何『不抛异常 / 值有效』形态的断言恒绿; 涉及异常路径的 SC 必须断言精确的 `decision` + `reason`**。

### [MINOR] m-1 D12 的 (2) 与 (3) 定义顺序自指 —— (2) 用「该行的键」, 而「键」的提取规则定义在 (3), (3) 又只作用于「未被 (2) 排除的行」

- **位置**: `:71` (2)(a)「该行的**键**是 `paths` 或 `paths-ignore`」; `:74` (3)「**对未被 (2) 排除的行**, 按首个未被引号包裹的 `:` 拆为键与值」
- **问题**: 判定顺序被声明为 (2)→(3)→(4), 但 (2) 需要一个只在 (3) 才定义的概念。实现者只能自己补: 有人写 `line.strip().startswith("paths:")`, 有人把 (3) 的拆分规则前置。我**未能构造出结果分叉的输入** (试了引号键 `"paths":`、键后带空格 `paths :`、`paths-ignore`, 三种下两派实现终点一致), 因此只报为定义闭合性缺陷, 不主张行为风险。
- **建议修法**: 把「键的提取」从 (3) 提为 (2) 之前的独立第 (0) 步 (「先按首个未被引号包裹的 `:` 拆键值, 键再 strip 并剥成对引号」), (2)/(3)/(4) 都引用它。顺带消除 (2)(a) 里「含 flow list 同行形态」这句冗余说明。

### [MINOR] m-2 D13「精确匹配形态」的首句与它自己的排除项相矛盾 (`  ---` 缩进形)

- **位置**: `:98` (D13 边界 4)
- **问题**: 首句「只有**整行 strip 后恰等于 `---`** 才参与判定」按字面**包含** `  ---` (strip 后正是 `---`), 紧接着的排除项却说「缩进 > 0 的 `---` 均不参与」。同一句话里的必要条件与排除清单冲突。照首句实现的人会把块标量里的缩进 `---` (例: `run: |` 内 heredoc 输出 YAML frontmatter) 判成多文档分隔 ⇒ covered ⇒ 恒 wait —— 就是 L 侧 R3 那个 `echo "--- image size ---"` 坑的近亲。
- **证据**: `:98` 实读全句; 唯一的救命绳是 SC-31(e) (`:254` 实读「形态负控 `--- foo` / `----` / 缩进 `  ---` → **均不参与**判定」) —— 测试面是对的, 所以定为 MINOR 而非 MAJOR。
- **建议修法**: 首句改为「只有**列 0 起始且整行 (去行尾空白后) 恰为 `---`** 才参与判定」, 让「列 0」进入必要条件本身, 排除清单退化为示例。

### [MINOR] m-3 D13 的 `%`-指令豁免没定义「紧随」是否容许中间夹注释/空行

- **位置**: `:97` (D13 边界 3「**显式豁免**: 紧随 `%`-指令块之后的**第一个**列 0 `---` 仍是文档起始标记 ⇒ 忽略」)
- **问题**: YAML 允许指令行与 `---` 之间出现注释/空行。「紧随」= 物理下一行, 还是「跳过空行与注释后的下一行」? 前者实现下 `%YAML 1.2` + 空行 + `---` 的 `---` 前已有内容行 (`%YAML`) ⇒ **命中 ⇒ covered ⇒ 恒 wait**; 后者正确忽略。两个实现者分叉, 且一侧就是本 change 要治的病。现实度低 (GHA workflow 极少写 `%YAML`), 故 MINOR。
- **建议修法**: 「紧随」改为「跳过空行与纯注释行后的第一个列 0 `---`」, 与 (1) 对空行/注释的处理保持同一约定。

### [MINOR] m-4 `rstrip("\0")` 与「滤空串」并非「各治一病」—— 滤空串完全覆盖 rstrip, SC-29(b) 对「缺 rstrip」恒绿

- **位置**: `:55` (A2 新增的「两步不重复, 各治一病」说明 + 由此推出的 SC-29(b) 断言设计)、`:252` SC-29(b)
- **问题**: A2 说「rstrip 治尾随 NUL 产生的末位空元素; 滤空串治空 diff 的 `[""]` 与任何中间空元素」, 并据此要求 SC-29(b) 同时断言计数。但**滤空串已经把尾随 NUL 产生的末位空元素也滤掉了** —— 它就是「任何空元素」的一种。⇒ 一个**省略 rstrip、保留滤空串**的实现: 3 文件 diff → `split("\0")` → `[a,b,c,""]` → 滤空 → 3 个 ⇒ `changed_files_count == 3` ✅、无空串 ✅、SC-29(b) **全绿**。所以 A2 为这条 minor 设计的红窗并不存在; SC-29(b) 实际只能抓「两步都缺」的实现。
- **建议修法**: 二选一 —— (a) 承认 rstrip 是冗余步骤, 从 D14 义务 2 中删除, 只留「split 后滤空串」并相应简化 `:55` 的说明; 或 (b) 保留 rstrip 但**如实说明它无独立红窗** (措辞从「各治一病」改为「rstrip 为可读性冗余, 其缺失被滤空串掩盖, SC-29(b) 只对两步皆缺可红」)。当前措辞属于「声称有红窗而实际没有」, 比缺步骤本身更有害。

### [MINOR] m-5 A2 吸收表声称「`:62` anchors 与 D12 建立引用关系」, 但目标行实际无任何 D12 引用

- **位置**: `:347` (Minor ×7 吸收表末项「`:62` anchors 与 D12 建立引用关系」) vs `:67` (该条款在 A2 版中的实际行)
- **问题**: 交叉核对失败。`:67` 实读全文为「`paths-ignore` 在场 / anchors / 其他无法辨识的**构造级**内容 → 该 workflow 记 `covered` (per-workflow 级不确定, **D2**);」—— 引的是 D2, 全行**无 D12**。全文 `grep -n "D12"` 的命中行为 68/92/93/111/189/190/313/335/336/337/346/353/361, **不含 67**。⇒ 吸收表记了一条未实际落地的 fix (本项目 memory `feedback_cross_doc_claim_verify_at_target` 的形态)。这条 minor 本身影响不大, 但吸收表是下一轮判断「哪些已闭环」的依据, 失实条目会让下轮误以为该处已收敛。
- **建议修法**: 要么在 `:67` 补上「(判据见 D12)」, 要么把 `:347` 该项改为「未落地」。附带建议: 既然 `:67` 的三类成因 (`paths-ignore` / anchors / 其他) 现在全部归 6b, 该行应同时补「→ 计入 `uncertain_workflows`, reason=`workflow-construct-uncertain` (规则 6b)」, 与 M-3 一并处理。

### [MINOR] m-6 `uncertain_workflows == []` 在短路规则 1/2/3/4 下等价于「未扫描」, 与「已扫描且无不确定」不可辨

- **位置**: `:117` (「`uncertain_workflows`… **恒存在, 无则 `[]`**」)、`:104-107` (规则 1/2/3/4 均在 workflow 枚举/解析之前产出终态)
- **问题**: 规则 1 (git-diff-failed)、2 (empty-diff)、3 (workflow-files-changed)、4 (no-workflow-files) 都在「逐 workflow 解析」之前返回, 此时 `uncertain_workflows` 只能是 `[]`, 但其含义是「**没扫**」而非「**扫了没有**」。唯一可用于区分的线索是 `workflows_scanned`, 而 Spec 未规定它在这四条短路路径上的取值 (尤其规则 3: 文件枚举是否已发生?)。⇒ 一个「按 `uncertain_workflows == []` 判定评估干净」的下游 (含 D15 的 AI 判断) 会把「没评估」读成「评估通过」。这是 covered 系列里最容易被当正常结果吞掉的一种。
- **建议修法**: 在返回契约里为这四条短路路径明确 `workflows_scanned == 0` (规则 4 亦为 0), 并在 D15 的判断条件里写「`uncertain_workflows` 非空**或** `workflows_scanned == 0` 时…」的正确读法; 或更彻底: 给 `uncertain_workflows` 加 `null` 语义 (未扫描) 与 `[]` 语义 (扫了没有) 的区分。

### [MINOR] m-7 D13 只建模 `---`, 未建模 `...` (document-end marker)

- **位置**: `:91-98` (D13 全段)
- **问题**: 「四个边界」问的是 `---` 的封闭性, 但多文档 YAML 的另一个文档级 token 是 `...`。`on: push` … `...` … 之后再起内容, 构成第二个文档而**不出现 `---`** ⇒ D13 检测不到 ⇒ 手写 parser 会把两个文档的键混读成一份。现实度很低 (workflow 极少用 `...`), 且后果方向不定, 故 MINOR / 可 WONTFIX, 但「封闭了吗」的诚实回答是: **对 `---` 封闭度已高, 对文档级 token 整体未封闭**。
- **建议修法**: 一句话即可: 「列 0 且 strip 后恰等于 `...` 的行, 与列 0 `---` 同等对待 (记构造级不确定)」; 或在非目标里显式声明不建模 `...`。

---

## OUT_OF_SCOPE (越界, 单独列, 不计入 counts)

- **`on:` 的 flow mapping 形与引号键形不被识别 ⇒ 假 not_applicable (fail-OPEN)**: `:62` 的触发子集解析 (R1-R4 既有) 只建模标量 / 列表 / 块映射三形。`on: {push: {paths: ['a/**']}}` 走 D12 也不命中 (值首字符 `{`), 而 `"on":` (YAML 1.1 把裸 `on` 当布尔真, 不少仓因此加引号 —— 本 Spec `:99` 自己引用的 `on:  # yamllint disable-line` 就是同一批用户的另一种应对) 则连 `on:` 键都识别不到。两者都导致「零自动触发 ⇒ not_applicable ⇒ 放行」。**这是既有条款的缺口, 不是 A1/A2 引入**, 但它与 C-2 同属 fail-OPEN 家族, 建议 owner 决定是否并入本 Spec 或单开。
- **D12(1) 未定义「文件中找不到顶层 `on:` 键」时的区间**: 与上一条同源 (A2 新写的 (1) 是本可以顺手关闭它的位置), 归为同一条处置。
- **L-1 `compute_verdict` catch-all `else → GREEN`**: `:323` 已列入 Follow-up, 本轮不重复。

---

## 经本轮核验属实 / A2 确实修对的部分 (下轮免重复)

1. **C4 的 reason 二分确实救活了两个红窗**: SC-30 正控现可断言 `reason=="workflow-construct-uncertain"`、SC-31(a) 现可断言 `=="workflow-trigger-matched"` ∧ `uncertain_workflows==[]` —— 两种实现输出不再逐字节相同。这是 A2 最有价值的一处修复 (缺口只在覆盖面, 见 M-2/M-3)。
2. **C2 的键值拆分 + 8 行判定表**: 逐行走查未发现新的漏判/误判; `push: &push_cfg` / `<<: *base` / `tags: !!str foo` 判定确定。
3. **C3 的区间就地定义**: (1) 起止完整, 且比 (2) 多写了「空行/注释不终止区间」这条关键子句 (讽刺的是 (2) 缺的正是它, 见 C-1)。D12/D13 两个区间并存在 `:92` 已分别声明, 不再悬空。
4. **M3 引用订正属实**: 新引的代码先例经实读确认存在且语义匹配 —— `test_handoff_worktrees.py:9` 「inside ONE isolated tempdir (NOT repo.parent) per the #135 $TMPDIR-leak lesson」、`:36`「#135: never repo.parent」、`test_git_operation_detection.py:92` 「NOT repo.parent, which resolves to a fixed $TMPDIR…」。
5. **M5 Status 行修对 (实跑验证)**: `_extract_status` → `_status_lifecycle_head` 在破折号处截断为 `📝 **Draft (A2, post_spec R5-fix)**` → `_normalize_status` = **`pending`**。机读层已不再返回 approved, 下游不会据此起 Phase B。
6. **勘正 3 的事实内核属实 (独立复核)**: pinned baseline 的 8 个 `structural_metrics.*.measured` 全为 `int 100` (`unit:"percent"` 另存), `primary_pass_gate` 为 dict 且其 `measured == "100%"` (str) ⇒ SC-32 的两条断言在语法上可实现 (问题在守错对象与跨仓落点, 见 M-4/M-5, 不在事实)。
7. **M6 的 `!` 所有权划分无行为差异**: 值位内归 glob matcher (未建模 → 判匹配 → covered) 与值位外归 D12 (构造级 → covered), 两条路终点相同, 划分安全。**但同一论证对 `*` 不成立** —— `*` 是已建模 glob 字符, 落不进 matcher 的兜底, 这是 C-2 的入口, 请勿把 M6 的结论外推到 `*`。
8. **§6 的行号锚点抽验准确**: `aria/skills/phase-c-integrator/SKILL.md` 第 5 项「Verdict 计算」与第 6 项「路由决策」确落在 `:241-249` 区间内 (缺的是 D15 的点名, 不是锚点漂移)。

---

## 给 owner 的一句话判断

**REVISE。** 两条 critical 都落在 A2 唯一的新承重逻辑 (值位互斥) 上, 且方向相反 —— 一条让它**恒 wait 复发** (块归属算小了), 一条让它**误放行** (排除面无条件, 把真 alias 当 glob, 与 D2 直接冲突)。后者是本 Spec 迄今出现的第一个 fail-OPEN 缺陷: 之前所有缺陷的坏结果都是「多等 1800 秒」, 这一条的坏结果是「CI 本该拦它时闸门放行」。八条 major 里有五条 (M-1/M-2/M-3/M-6/M-8) 是同一形状: **义务写了、槽位留了、红窗没有** —— A2 在「把事实记下来」这件事上做得很好, 在「让记错时会红」这件事上系统性欠一步。建议下一轮 (若跑) 只审两处: 值位互斥的字符级判据 + 每条新义务的红窗存在性。
