# post_spec R5 (定向) — qa-engineer

**verdict**: REVISE
**scope_ok**: true
**counts**: critical=2 major=2 minor=1

**审计对象**: `openspec/changes/phase-c-gate-path-coverage-not-applicable/proposal.md` A1 修订新增 SC-29~32 (`:201-204`) 及其对应决策 D12/D13/D14 (`:63`/`:65`/`:51`)。视角: 「它怎么会红」——对每条 SC 构造具体错误实现, 论证该 SC 在其上是否真的失败。

**实测基座** (本轮独立复现, 非推断; 与其它席位报告的实测互证):
- scratchpad 建临时 git 仓, 用 `git diff --name-only --no-renames [-z] main...pr` 复现 D14 前提: 无 `-z` 时非 ASCII 路径确被 `core.quotePath` 八进制转义并加双引号 (`"skills/\346\265\213\350\257\225/x.py"`); `-z` 输出确含尾随 NUL, 朴素 `split("\0")` 多出一个空元素。
- 已读 `ab-suite/phase-c-integrator.json` (3 个 LLM eval: commit-generation/merge-conflict-handling/multi-remote-merge-push) / `ab-suite/phase-c-integrator-pre-merge-gate.json` (6 fixtures, 无 `evals` 键) / 基线 `ab-results/2026-05-10-phase-c-integrator-pre-merge-gate/benchmark.json` (8 个 `structural_metrics.*.measured` 为 `int 100`, `primary_pass_gate.measured` 为 `str "100%"`) / `ab-results/latest` (指向 `2026-05-13-state-scanner-issue-101-fix`)。
- `aria-plugin-benchmarks/` 全目录 grep 未发现任何实现"skill 名 → 套件/基线路径"解析的代码; `AB_TEST_OPERATIONS.md:206` 确认该解析是人/AI 读文档后自行判断的过程。

## 必审复核 (与既有 SC-1~28 的关系; 逐项检查, 未发现新增缺陷)

- **reason 封闭集满射未被破坏**: D12/D13/D14 均只在既有判定规则 5 (`:75`, per-workflow 解析) 内部产出效果, 复用既有 `covered`/`workflow-trigger-matched` 出口, A1 未新增、未删除任何一个封闭集内的 7 个 reason 字面值; R4 已确认的满射关系不受影响。
- **Impact 表分派仍是 {1..32} 的无交并**: `test_path_coverage.py` (SC-1~8,14,16~20,23~31 = 23 条) + `test_pre_merge_gate.py` (SC-9~13,15,21~22 = 8 条) + AB 执行面 (SC-32 = 1 条), 合计 32, 逐条核对无遗漏无重复。
- **既有语料型 SC 不受 D12/D13 影响**: 本仓 4 份真实 workflow 语料均不含 YAML anchor/alias/`---`, 故 SC-2/SC-19/SC-23 等既定期望值不因 A1 变化。
- **`-z`/`--no-renames` 组合无冲突**: 已实测三参数同时使用 (`--name-only --no-renames -z`) 输出正常, SC-8/SC-18/SC-26/SC-27 判定路径与 `-z` 正交, 不受影响。

以上均为核对通过、不构成 finding 的部分。

## Findings

### [CRITICAL] SC-31(a) 断言的 `reason` 值在其自证的错误实现下与正确实现完全相同 —— 不可能红
- **位置**: `openspec/changes/phase-c-gate-path-coverage-not-applicable/proposal.md:203` (SC-31); 根因交叉引用 `:76` (判定规则 6) / `:65` (D13 正文)
- **问题**: SC-31(a) 要求 fixture "首行 `---` 的 workflow + **paths 命中变更**", 期望 `covered, reason=workflow-trigger-matched`, 并明确自称"若实现把首行 `---` 当多文档分隔则必红"。但 `:76` 判定规则 6 写明: **任一** per-workflow 判定为 covered 的 workflow —— 无论其成因是路径真实匹配, 还是 `:62` "无法辨识的构造级内容 → 该 workflow 记 covered" 的保守兜底 —— 在**聚合层**都产出同一个 `reason=workflow-trigger-matched`。当 fixture 按 SC-31(a) 字面要求"paths 命中变更"时, 无论 `---` 被正确忽略(走真实匹配)还是被误判为构造不确定(走 D2 保守兜底), 两条路径在聚合输出层都是 `{decision:"covered", reason:"workflow-trigger-matched"}`, 位级相同。
- **证据**: 构造错误实现 E = "任何列 0 的 `---` (不论是否为首行) 一律按 `:62` 处理为『无法辨识的构造级内容』, 该 workflow 记 covered"。在 SC-31(a) 指定的 fixture (paths 确实命中变更) 上运行 E: 该 workflow 因 `---` 判 construct-uncertain-covered → 进规则 6 → 整体 `covered, reason="workflow-trigger-matched"`。同一 fixture 上运行正确实现 (忽略首行 `---`, 走真实 paths 匹配) → 该 workflow 因路径真实匹配而 covered → 同样进规则 6 → 整体 `covered, reason="workflow-trigger-matched"`。两次输出逐字节相同, SC-31(a) 的断言在错误实现 E 上同样 PASS, 不会红, 与其自身"必红"声明矛盾。(注: 同一根因也稀释了 (b) 的区分力 —— 若 changed_files 不特意选择"不命中显式 paths", "把 `---` 之后内容当无害跳过"式的错误实现也可能巧合走到与正确实现相同的输出; (b) 本身未显式自称"必红", 危害较轻, 一并在修法中处理。)
- **建议修法**: 把 (a) 的 `changed_files` 改为**不匹配**该 workflow 显式 `paths` 的文件 (即让"真实匹配"这条路径在正确实现下走不通), 期望值相应改为 `not_applicable, reason="no-triggering-paths"`; 错误实现 E 在同一输入上仍会产出 `covered, reason="workflow-trigger-matched"` —— 这时两者才会在 `decision` 上分道, 断言真正可证伪。(b) 同理需要一份不匹配该 workflow paths 的语料。
  > **与 code-reviewer 本轮报告的交叉关联**: 该报告的 MAJOR 发现 (`:76`/`:79`/`:106`, "reason 封闭集里没有『构造级退回 covered』的槽位") 与本 finding 同根同源——如果采纳其修法选项 (a) (新增 additive 字段 `degraded_workflows` 标记哪些 workflow 是因构造不确定而非真实匹配被记为 covered), 则 SC-31(a)/(b) 可以直接断言 `degraded_workflows` 是否包含该 workflow 而不必改动 fixture 极性, 一次修复同时解决两边发现的问题。若 owner 采纳该统一方案, 本 finding 的"建议修法"可替换为"断言 `degraded_workflows` 而非仅 `reason`"。

### [CRITICAL] SC-32 前两条断言的是执行期人工/AI 判断过程, 不是可调用代码, "结构化测试"测不到它声称要测的东西
- **位置**: `:204` (SC-32); 交叉引用 `:153-163` (rule6_note + 三处勘正表), `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md:206`
- **问题**: SC-32 第 1/2 条断言的是"跑 Rule #6 AB 门禁时**实际解析到**的套件路径/基线路径"。但全仓 grep 未发现任何代码实现"skill 名 → 套件文件路径"或"skill 名 → 基线路径"的解析函数 (`aggregate_benchmark.py`/`generate_review.py` 在当前仓内均不存在)。真实机制是: 人/AI 读 `AB_TEST_OPERATIONS.md` §场景1 步骤 1 ("读取 `{skill}/evals/evals.json` (或 `ab-suite/{skill}.json`)") 与本 Spec rule6_note 表的文字指示后, **自行决定**调用哪个套件名、写哪个基线路径——这是执行期的人工/AI 判断, 不是一段可以被单测调用并断言返回值的函数。这恰恰对应 CLAUDE.md Rule #6 判据表"处方性 · 套件覆盖外 (典型: authoring 向导) → **不能**用 AB/结构化测试测到"那一档, 处置应为"点名行为 + 建可证伪定向 fixture + 套件缺口开 issue", 而非"结构化测试替代"(那一档专属"描述性 schema/字段/命令/勘正")。SC-32 把前两条也归为"结构化测试", 混淆了这两档。
- **证据**: 已核实两个候选文件均真实存在且内容确如 rule6_note 所述互不相关。但这只是**静态文件事实**, 与"本 Spec 真正上线跑 Rule #6 门禁时, 会不会又用裸名调 `/skill-creator benchmark phase-c-integrator`"这一**执行时**问题不相交。构造错误场景 F = "AI 在 v1.65.0 发版前跑 Rule #6 门禁时键入 `/skill-creator benchmark phase-c-integrator`" (裸名, 正是 A1 自己点名要防的错误): SC-32 的结构化断言 (无论是"两路径字符串不相等"还是"两文件各自存在且内容不同") 在 F 发生前后跑都恒为 PASS, 因为它断言的是仓库里两个 JSON 文件的静态属性, 不是"这次门禁执行读了哪个文件"; F 真正发生时 SC-32 全绿但 Rule #6 门禁本身已经错跑, 与本 Spec 存在的理由正面冲突。三条款中只有第 3 条 (`structural_metrics.*.measured` 类型为 `int`) 是对已存在文件的纯类型断言, 真正可结构化验证 (已实读确认属实)。
- **建议修法**: 按 CLAUDE.md Rule #6 判据表第三档处置前两条款——要么诚实降级断言范围为"两文件均存在且内容不同"(仅证明"文档所述的两个文件确实是两个不同文件", 不证明"未来执行会选对"), 同时开 issue 补一条真正可证伪的定向验证; 要么把前两条款从"结构化测试"改记为"发版执行时人工/AI 自查 checklist 项", 不再算作可自动化验收的 SC。第 3 条保留为结构化测试即可。
  > **收敛信号**: 本轮 code-reviewer 独立发现"SC-32 两条断言无可计算的主体"(逐字对应"仓内无解析代码, 左值不存在"), tech-lead 独立发现"SC-32 落点在 `run_all_tests.sh` 扫描域外"——三个角度 (无主体 / 未接入 runner / 测的是执行行为非代码) 共同指向 SC-32 的前两条款目前不构成可自动验收的 SC, 建议 owner 按统一方案一次性重写。

### [MAJOR] SC-29(a) fixture 未锁定"非 ASCII 路径是变更集合里唯一匹配项", 存在被同批 ASCII 文件掩盖的风险
- **位置**: `:201` (SC-29)
- **问题**: SC-29(a) 写"变更**含**非 ASCII 路径…且该路径命中某 workflow paths → covered", 用词是"含" (contains), 未排除同一 diff 里还有其它已匹配的 ASCII 路径。若 fixture 同时含一个已匹配的 ASCII 文件, "忘记 `-z`"的错误实现依然会因为那个 ASCII 文件而判 `covered`, 与 `-z` 是否生效无关, 断言仍然通过, 测不出目标缺陷。本文档其它语料型 SC (SC-19 `changed_files=[aria]` / SC-23 精确语料+精确变更文件) 均采用"精确枚举唯一变更集合"的写法排除这类混淆, SC-29(a) 未遵循同一精度。
- **证据**: 已在 scratchpad 临时仓库实测 (`skills/issue-triage/a.py` 建于 main; `skills/测试/x.py` + `skills/issue-triage/b.py` 建于 pr 分支): `git diff --name-only --no-renames main...pr` (无 `-z`) 真实输出为
  ```
  skills/issue-triage/b.py
  "skills/\346\265\213\350\257\225/x.py"
  ```
  若 workflow 的 `paths: ['skills/issue-triage/**']`, 错误实现 (无 `-z`) 在此双文件 fixture 上仍会因 `skills/issue-triage/b.py` 原样匹配而输出整体 `covered` —— 与 SC-29(a) 期望值相同, 断言通过, 但 `-z` 缺失这个真正的 bug 完全没有被验证到 (那个八进制转义串本身从未参与过匹配判断)。
- **建议修法**: 把 (a) 的措辞改为"changed_files **只**含该非 ASCII 路径 (或其余条目均不匹配任何 workflow 的 paths)", 与 SC-19/SC-23 的精确枚举风格对齐。
  > **与 tech-lead 本轮报告互补**: 该报告从另一独立角度 (`core.quotePath` 是用户可配置项, 中文开发者常置为 `false`) 论证 SC-29(a) 同样可能测不出 `-z` 缺失; 两个角度 (fixture 混淆 / 环境配置未钉死) 独立地都指向 SC-29(a) 当前措辞精度不够, 建议一并在修法里钉死 fixture 唯一性**与** `core.quotePath=true` 前提。

### [MAJOR] SC-30 正控同样未排除"同一 event 内存在其它真实匹配 paths"的混淆
- **位置**: `:202` (SC-30)
- **问题**: SC-30 正控写"`&anchor`/`*alias`/`<<`/`!tag` 落在 `on:` 子树内 → 该 workflow covered", 未要求"该 event 除锚点行外没有其它会独立产生真实覆盖的 paths"。根因与第一条 finding 相同 (`:76` 判定规则 6 的 reason 折叠): 若 fixture 里锚点所在 event 同时含一条会真实匹配变更的 `paths`, "锚点检测完全没实现"的错误实现也会因为真实路径匹配而输出 `covered`, 无法证明锚点 fail-closed 逻辑本身生效。与 SC-31(a) 不同的是, SC-30 文本没有显式钉死"paths 命中变更"这个混淆条件, 因此这里是**未排除的风险**而非**保证必然如此的矛盾**——若 Phase B 实现者选用"锚点行 + 不匹配的 paths"组合作 fixture, 测试仍然有效。但语料层面的诱惑很大: 本仓 4 份真实 workflow 里凡带 paths 的都同时含合法 `paths:` 内容, 若图省事直接在真实语料上加一行 anchor, 极易连带真实匹配。
- **证据**: 假设错误实现 E' = "完全跳过 §1 的锚点/别名扫描 (D12 规定的 fail-closed 分支被完全遗漏), 其余构造一律当正常内容继续解析"。若测试 fixture 恰好是"该 event 的 `paths` 本身就命中变更", E' 会照常解析出真实匹配 → `covered` —— 与期望值相同, 测不出 D12 缺失这一事实。
- **建议修法**: 显式补一句"该 event 除锚点/别名内容外, 其显式 `paths` (若存在) 不得命中 changed_files, 以保证 `covered` 只能来自锚点触发的 fail-closed 判定", 与 SC-30 已有三条负控的精细化程度对齐。
  > 三条负控本身逐条核实有效且互不冗余: (i) 测扫描区间排除 `jobs:`/`run:` 段, (ii) 测注释先剥除, (iii) (SC 原文自称"核心") 测首字符位置判据而非子串判据——三者分别针对流水线的不同环节, 不存在"三条测的是同一件事"的重复浪费。本 finding 只针对**正控**缺失同等精度。

### [MINOR] "区间" (构造级扫描的作用域) 在 A1 新增文本中首次出现但全文未定义边界算法
- **位置**: `:63` ("对**区间**内每一行…" —— 全文 grep 唯一命中)
- **问题**: 姊妹 Spec L 用 5 条编号规则明确定义 `on:` 块缩进起止, 本 Spec 通篇未给出等价定义, A1 直接引入"区间"一词却未回填计算方式。SC-30 给出的三条负控恰好都落在"任何合理区间定义下结论都一致"的位置 (① `run:` 块体远在 `jobs:` 段, ② 注释在区间内被跳过, ③ `paths:` 行明确在 `on:` 块内), 不足以倒逼实现者精确定义边界。
- **证据**: 错误实现 = "『区间』取整份文件, 不限定于 `on:` 键到块结束"。此错误在 SC-30 现有三条负控上都不会被抓到 (三者都发生在明显属于/不属于 `on:` 块的位置, 不落在边界附近)。失败方向总体仍偏安全侧 (歧义扩大更容易落 `covered`, 不易静默漏判出 `not_applicable`), 故定为 MINOR。
- **建议修法**: 参照 L 侧 5 条缩进规则, 把"区间"如何计算起止显式写入 §1 正文。
  > **收敛信号**: 本轮 code-reviewer (CRITICAL, 用 `<<: *defaults` 落在 `jobs:` 段构造出两实现者 skip/wait 分裂的反例) 与 tech-lead (MINOR) 独立发现同一处"区间未定义", 且给出的反例比本 finding 更具体、更能体现潜在危害方向不总是安全侧 (见 code-reviewer 报告 CRITICAL-1)。三席独立命中同一空缺, 建议 owner 采纳 code-reviewer 给出的显式区间定义作为统一修法, 优先级按其 CRITICAL 定级处理, 本条视为佐证而非独立于其上的追加要求。

## 范围声明 (OUT_OF_SCOPE)

无越界 finding。本轮全部结论落在 A1 新增的 SC-29~32 及其与既有判定规则/reason 封闭集/Impact 分派的关系之内; 未复审既有 SC-1~28 自身质量, 未评价 L-1 (catch-all fail-OPEN) 等已明确列为正交 Follow-up 的条目。
