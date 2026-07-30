# post_spec R5 (定向) — tech-lead

**verdict**: REVISE
**scope_ok**: true
**counts**: critical=2 major=3 minor=3

审计对象: `openspec/changes/phase-c-gate-path-coverage-not-applicable/proposal.md` 的 A1 修订
(git `f829aee`, 2026-07-30)。只审 A1 新增 4 处 + A1×既有一致性。全部引用行号均已实读;
全部 finding 均带实跑 / 反事实 / 互斥原文引用。

---

## 先记 A1 中经实测**成立**的部分 (不构成 finding, 但支撑下面的比较基准)

| A1 声称 | 实测结果 |
|---|---|
| D14 上半: 无 `-z` 时非 ASCII 路径被 `core.quotePath` 八进制转义 | ✅ 复现: `git diff --name-only --no-renames master...feat` → `"skills/\346\265\213\350\257\225/x.py"` (带双引号 + 八进制) |
| D14 下半: 非空 diff 的 `-z` 输出含尾随 NUL | ✅ 复现: `od -c` 末字节 `\0`; `d.split('\0')` → `['b.txt','skills/测试/x.py','']`, `d.rstrip('\0').split('\0')` → 无空串 |
| D13 语料前提「本仓 4/4 首行为注释」 | ✅ 4 份 workflow 首行全是 `#` |
| 勘正 3 `structural_metrics.*.measured` 是 int | ✅ 基线 8 个指标全为 `measured=100 (int), unit='percent'`; `primary_pass_gate.measured='100%'` (str) |
| 勘正 1 的解析机制 (裸名 → parent 套件) | ✅ `AB_TEST_OPERATIONS.md:206`「读取 {skill}/evals/evals.json (或 ab-suite/{skill}.json)」; parent 套件 3 evals = commit-generation / merge-conflict-handling / multi-remote-merge-push, `source_evals_count:5, selected_count:3` — 与 A1 描述逐字相符 |
| §修订记录 **L-7 已解决** 的声称 | ✅ 属实。`:62`「`paths-ignore` 在场 … → 该 workflow 记 `covered`」+ SC-6 (`:178`)。R 侧**根本不从 `paths-ignore` 推导不覆盖**, 与 L 的 R2-fix 同结论。(补记: GHA/forgejo 明文禁止同一 event 同时用 `paths` 与 `paths-ignore`, 故 L 侧 R3 的「共存优先级写反」在 R 架构上只作用于非法配置, 不另开 finding) |
| §闸门待裁 引用的 config 事实 | ✅ `.aria/config.json` `audit.checkpoints.post_spec="convergence"`; `audit._comment` (`:61`) 逐字含「**AI 不得自行豁免已 enabled 的 checkpoint**」 |
| reason 封闭集 / 8 条规则互斥穷尽 | ✅ **未被 A1 破坏**。D12/D13 只在规则 5 的 per-workflow 解析层产出 `covered`/`parse_failed`, 不新增终态; D14 只改喂给规则 1/2/3 的 diff 命令 (空 diff 下 `"".rstrip('\0').split('\0')` → `['']` → 滤空 → `[]`, 规则 2 `empty-diff` 仍成立)。SC-29/30/31 未引入封闭集外的 reason 字面值 |

---

## Findings

### [CRITICAL] 勘正 1 + SC-32 与 :153 rule6_note 直接互斥 —— Rule #6 的 AB eval 臂被机械排除

- **位置**: `openspec/changes/phase-c-gate-path-coverage-not-applicable/proposal.md:153` ⟷ `:159` / `:204`
- **问题**: A1 在 `:153` 这句话**正下方**挂了一张勘正表, 而表的第 1 行否定了 `:153` 括注里点名的执行对象, `:153` 本体却一字未改。两者无法同时满足。
- **证据** (互斥原文 + 实读文件):
  - `:153` (pre-A1, owner 已签字): 「**照跑 AB** (phase-c-integrator: ab-suite **3 selected evals** [source 5]; `phase-c-integrator-pre-merge-gate.json` 6 fixtures **一并纳入执行面**)」 —— 明确把 parent 套件的 3 个 eval 列为执行对象之一。
  - `:159` (A1 新增): 「裸名会命中**无关的** parent 套件 `ab-suite/phase-c-integrator.json` (内容是 commit-generation / merge-conflict-handling / multi-remote-merge-push 三个 LLM eval, **与本 change 零关系**)。**必须点名全称** `phase-c-integrator-pre-merge-gate`」
  - `:204` SC-32 把它固化成机械断言: 「解析出的套件路径 == `ab-suite/phase-c-integrator-pre-merge-gate.json` (**非** parent `phase-c-integrator.json`)」——单数「**解析出的套件路径**」+ 显式「非 parent」, 实现出来的测试必然断言 parent 未被使用。
  - 实读两个套件文件: `ab-suite/phase-c-integrator.json` 有 `evals` (3 条, 带 prompt/expectations, 可跑 with/without 双臂); `ab-suite/phase-c-integrator-pre-merge-gate.json` **没有 `evals` 键**, 只有 `fixtures`(6) + `type:"workflow_skill_subextension"` —— 它结构上**跑不出 AB delta**。
  - ⇒ 若按 SC-32 执行: 本 change 被 `:153` 自己定性为「**处方性·运行时指令面** → 判据决策表**第二行** → 照跑 AB, **零裁量**」(Rule #6, CLAUDE.md 不可协商规则第 6 条), 却在唯一有 eval 的套件被排除后**没有任何 AB 双臂可跑**, 事实上降级成决策表第一行的 substitute 档 —— 而降档没有任何 `rule6_note` 论证支撑。
- **建议修法** (与危害同向: 保住 AB eval 臂, 只收窄「命名」这一层):
  1. 改写 `:159` 的「正确做法」列, 把它限定为**指代消歧**而非对象排除: 「当意图是那 6 个 fixture 套件时必须点名全称 `phase-c-integrator-pre-merge-gate`; 裸名 `phase-c-integrator` 解析到 parent 套件——**那是 Rule #6 AB 双臂的正当对象, 不是陷阱**, 两者并列执行」; 删掉「与本 change 零关系」这句 (它与 `:153` 及 Rule #6 判据表第二行同时冲突)。
  2. 相应把 SC-32 第 1 条断言改为「以全称名调用时解析到 `…-pre-merge-gate.json`」, 去掉「非 parent」这个排他子句。
  3. 若 owner 的真意确实是**不跑** parent AB, 则必须反向修 `:153` 并在 `rule6_note` 里给出降档到 substitute 的成文理由 —— 但那是对已签字 Rule #6 判据的实质改动, 应单独请裁, 不能靠一张勘正表隐式完成。

---

### [CRITICAL] D12 的「剥成对首尾引号 + 首字符判定」把引号包裹的 leading-`*` / `!` glob 误判为 YAML 构造 ⇒ 恒 wait 复发

- **位置**: `openspec/changes/phase-c-gate-path-coverage-not-applicable/proposal.md:63` (D12 判据本体) / `:149` (D12 决策行) / `:202` (SC-30 三条负控)
- **问题**: D12 的第 4 步「剥**成对**首尾引号」只会**扩大**命中面 (YAML 里带引号的标量在语义上永远是字面量, 不可能是 anchor/alias/tag/merge key)。剥完再判「值的首字符为 `&`/`*`/`!`」, 就把**以 `*` 或 `!` 开头的路径 glob** 判成构造级不确定 → 该 workflow 强制 `covered` → gate 退回现状 → 对这类仓库**恒 wait**。这正是 D12 自己在 `:64` 声称要根治的病 (「把病从假绿搬到恒红, 按本 Spec §Why 自己的判据同样零信息量」), 只是触发条件从「任何带 `*` 的行」收窄到「以 `*` 开头的 pattern」。
- **证据** (按 `:63` 字面实现 D12 后逐行实跑, 12 条用例 / 4 条误判):

  ```
    HIT  WANT    VERDICT  line
  False False         ok  "      - 'skills/issue-triage/**'"          # 本仓语料
  False False         ok  "      - 'aria/skills/issue-triage/**'"     # 本仓语料
  False False         ok  "    paths: ['a/**']"                       # SC-30 负控 (iii)
   True False   MISMATCH  "      - '**/*.md'"                         # 前导 ** glob
   True False   MISMATCH  "      - '*.py'"                            # 前导 * glob
   True False   MISMATCH  '      - "**.js"'                           # GHA 官方文档示例形态
   True False   MISMATCH  "      - '!docs/**'"                        # 否定 glob
   True  True         ok  '    paths: *common_paths'                  # SC-30 正控
   True  True         ok  '  push: &push_cfg'                         # SC-30 正控
   True  True         ok  '    <<: *base'                             # SC-30 正控
  ```
  - **没有任何 SC 能红**: SC-30 (`:202`) 的三条负控是 (i) token 只在 `run: |` 块体 / (ii) token 只在注释里 / (iii) `paths: ['a/**']` —— 三条全部选在 `*` **不在首位**的安全形态上, 结构上碰不到本缺陷。SC-2/SC-3/SC-19/SC-20/SC-23 用的都是本仓语料, 而本仓 4/4 pattern 都以字面目录名开头 (实读: `'skills/issue-triage/**'` / `'aria/skills/issue-triage/**'` / `'aria-orchestrator/docker/aria-runner/**'`) —— **语料是偶然安全的**。
  - **A1 自身的判据不自洽**: `:66` (D13) 用「本仓语料 4/4 首行为注释, **今天零代价, 但对采用者非零**」论证必须处置; `:64` (D12) 却用「位置式读法 4/4 零命中」就收工。同一份 A1 里对「语料零命中」给出两种相反的结论强度。
  - 反事实: 一个 `paths: ['**.js']` 的采用者仓 (GHA 文档首例形态), 其**任何**变更都落 covered → C.2.4 恒 wait → #122 原样复发。
- **建议修法** (与危害同向: 让判据只命中真构造, 不再吃掉 glob):
  1. **删掉第 4 步「剥成对首尾引号」**, 反向立规: 「带成对引号的标量**一律判字面量, 永不构造级命中**」(依据: YAML 中 anchor/alias/tag/merge key 都不能被引号包裹)。
  2. 把 alias/anchor 判据钉到 YAML 语法: 未加引号 **且** 整节点匹配 `^[&*][A-Za-z0-9_][^\s]*$` 才算命中 (`&`/`*` 后必须紧跟名字字符, 排除 `**`、`*.py`)。
  3. SC-30 增第 4 条负控: `- '**/*.md'` / `- "**.js"` / `- '*.py'` 三行落在 `on:` 的 `paths:` 序列内 → **不**触发构造级命中, 并各自可红。

---

### [MAJOR] `:3` Status 行在 A1 后仍是 `Approved — ready for Phase B`; state-scanner 实测机读为 `approved`, 且完全看不见 `:4` 的闸门警告

- **位置**: `:3` (Status 行, 未随 A1 变更) ⟷ `:4` (A1 警告) / `:275` (「本 Spec 在裁决前不进 A.2/A.3」)
- **问题**: A1 把闸门待裁写在**新增的 `:4`**, 但 `:3` 的 `**Status**:` 字段仍宣称 Approved 且 ready for Phase B。机读面只认 `:3`。结果: 机械通道报「已批准、可进 Phase B」, 而文档正文说「连 A.2/A.3 都不能进」。
- **证据** (跑真实生产代码, 非推断):
  ```
  $ python3 -c "…from collectors._status import _extract_status,_status_lifecycle_head,_normalize_status…"
  RAW STATUS  : '✅ **Approved** (owner sign-off 2026-07-27, … R4 qa PASS 0/0/0) — ready for Phase B'
  HEAD        : '✅ **Approved** (owner sign-off 2026-07-27, 签字面两项均批: 机制本体 + `path_coverage_enabled` 默认 true'
  NORMALIZED  : approved
  A1 warning line seen by extractor?  False
  ```
  - `aria/skills/state-scanner/scripts/collectors/_status.py` 的 6 条 pattern 全部要求行内出现 `**Status**`/`**状态**` 键; `:4` 以 `> **⚠️ A1 修订 …**` 开头, **结构上不可能被任一 pattern 命中**。
  - 下游语义: `aria/skills/state-scanner/scripts/collectors/openspec.py:78` 注释「fresh-approved (<30d) is a legal in-flight state」+ `:254` 谓词 `(st == "approved" and staleness >= 30)` —— 本 Spec 创建于 2026-07-27, staleness < 30d ⇒ **不会**被 surface 成 priority item。CLAUDE.md 指定的进展查询入口 `/state-scanner` 会把它报成一个健康的已批准在飞 Spec。
  - 这与 memory `feedback_spec_frontmatter_reflects_reality` 同形; 且本 Spec 尾段整段都在防「闸门被绕过」, 而机读面正好是最可能绕过它的那条路。
- **建议修法**: 闸门状态必须落在 `**Status**:` 那一行本体, 不能只加旁注。例: `> **Status**: ⏸ **Gate-pending (A1 修订待 post_spec 裁决)** — 2026-07-27 owner sign-off 覆盖 A1 之前的版本, A1 后**不 ready for Phase B**; 详见文末「闸门待裁」`。同时在 `:12` 审计轨迹尾部补一句 A1 使轨迹重开 (裁决落地后再补 R5 结论, 勿预写 `<PENDING>` —— memory `feedback_audit_trajectory_placeholder_footgun`)。

---

### [MAJOR] SC-32 落在 `aria-plugin-benchmarks/`, 结构上在 `run_all_tests.sh` 扫描域外 —— 唯一为「Rule #6 别跑错对象」兜底的验收条自己没有 runner

- **位置**: `:226` (Impact 行) / `:204` (SC-32) / `:234` (测试基线)
- **问题**: `:226` 把 SC-32 的三条结构化断言放进 `aria-plugin-benchmarks/`; `:234` 却把验证入口声明为 `run_all_tests.sh`, 并把 SC-29~32 一起算进 phase-c 的「~120+」基线。两者对不上: SC-32 永远不会被那个入口执行。
- **证据**:
  - 实读 `aria/skills/run_all_tests.sh`: `:28` `cd "$(dirname "$0")/.." || exit 2` → 工作目录 = `aria/`; `:29` `SKILLS_DIR="skills"`; `:48` `for tests_dir in $(find "$SKILLS_DIR" -type d -name tests | sort)`。⇒ 扫描域严格限于 `aria/skills/*/tests/`。
  - `aria-plugin-benchmarks/` 不在 `.gitmodules` (实读: 只有 standards / aria / aria-orchestrator), 是**主仓**普通目录, 与 `aria/` 平级 ⇒ 结构上不可能被上述 `find` 命中。
  - 主仓三份 workflow 也不跑它: `issue-triage-tests.yml` paths=`aria/skills/issue-triage/**`, `build-aria-runner.yaml` paths=`aria-orchestrator/docker/aria-runner/**`, `submodule-gate-tripwire.yml` 仅 dispatch。
  - ⇒ SC-32 = 只在文档里存在的验收条 = memory `feedback_paper_fix_antipattern` 的 doc-only advisory 形态, 而它兜底的恰恰是 A1 自称「每条都会让 Rule #6 跑在错误对象上」的那三个陷阱。
  - 附带: `:234` 的「~120+」把 SC-32 的 3 条算进了 phase-c 套件计数, 使「基线数字对得上」无法反证 SC-32 的缺席。
- **建议修法** (与危害同向: 给 SC-32 一个真会被执行的家):
  1. 把三条断言实现在 `aria/skills/phase-c-integrator/tests/test_ab_execution_surface.py` (落进 `run_all_tests.sh` 扫描域), 以只读方式解析 `../../aria-plugin-benchmarks/ab-suite/*.json` 与基线 `benchmark.json`; 目录不存在时按 `run_all_tests.sh` 自身的「缺依赖 ⇒ SKIP 并写明原因」约定 SKIP (aria 独立 clone 场景), 存在时必须断言。
  2. 若 owner 坚持留在主仓, 则 `:226` 必须同时声明它的 runner 与执行时机 (谁调、什么时候调), 并把这 3 条从 `:234` 的 phase-c 基线里剔出单列 —— 否则计数会掩盖它没被跑。

---

### [MAJOR] D12 与既有 `:68` glob 条款对 `!` 前缀的所有权重叠, 使 BA-1 钉死的 matcher 层 fail 方向在生产路径上不可达

- **位置**: `:63` (D12, 命中集含 `!`) ⟷ `:68` (既有 glob 条款) / `:186` (SC-14)
- **问题**: 同一个输入 (`- '!docs/**'`) 被两条条款同时认领, 且 D12 在**更早的层**短路。
- **证据** (互斥原文 + 上一条 finding 的实跑输出):
  - `:68` (既有, R1 BA-1 Critical 的修复产物): 「**对任何未建模 glob 语法片段 (字符类 `[abc]` / 否定 `!` / 其他) 一律判定为「匹配」→ 该 workflow covered** (BA-1, **matcher 层的 fail 方向显式钉死**; SC-14 含字符类/否定用例)」 —— 明确把 `!` 判给 **matcher 层**。
  - `:63` (A1 新增 D12): 命中集含「值或键的首字符为 … `!`」—— 把同一行判给 **parse/构造层**。
  - 实跑证实 D12 会先吃掉它: `- '!docs/**'` → 剥 `- ` → 剥引号 → 首字符 `!` → **HIT**。
  - 后果: 带 `!` pattern 的 workflow 在生产路径上**永远走不到 matcher**, `:68`/BA-1 钉的那条 fail 方向成为死代码; `:186` SC-14 的「`!` 前缀 → 判匹配」用例仍会绿 (它是 matcher 的表驱动单测), 但**不再描述端到端行为** —— memory `feedback_completion_signals_vs_runtime_invocation` 的形状 (单测绿 ≠ 该分支被真调用)。
- **建议修法** (与危害同向: 恢复单一所有者, 别让新层吃掉旧层):
  - 从 D12 的构造命中集中**移除 `!`**, 并在 `:63` 明写「`paths:` / `paths-ignore:` 序列项一律**不参与**构造级判定, 全部交 matcher (依据 `:68` / BA-1)」;
  - SC-30 (`:202`) 正控里的 `!tag` 用例相应移到 `on:` 子树中**非 `paths` 位置** (如 `branches: !!seq [a]`), 使正控仍可红而不与 `:68` 抢所有权。

---

### [MINOR] D12 的「区间」全文无定义, 只靠 SC-30 负控 (i) 间接钉 —— 与 D12 自陈「承重算法须钉到字符级」不自洽

- **位置**: `:63`
- **问题**: `:63` 写「对**区间**内每一行 …」, 但「区间」在全文只出现这一次, 无前指、无定义; Spec 也从未定义 `on:` 块的**边界判定规则** (缩进? 到下一个列 0 键? 遇空行是否终止?)。
- **证据**:
  - `grep -n "区间" proposal.md` → 只有 `:63` 一行 (即它自己的引入句)。
  - `grep -n "子树|缩进|块结束|on: 块"` → 只有 `:202` (SC-30) 出现「`on:` 子树 / `on:` 块内」, 是 SC 反向暗示扫描窗口, 而非条款定义。
  - 边界不是空谈: 实读 `.forgejo/workflows/build-aria-runner.yaml`, `on:` 块内第 21 行是**空行**, 第 22 行才是 `push:` —— 任何「遇空行终止」的朴素读法都会把该 workflow 读成 dispatch-only。(该形态另有 SC-23 兜底, 但 D12 的扫描窗口只有 SC-30 负控 (i)「token 只在 `run: |` 块体 → 不触发」一条间接约束。)
  - D13 (`:65`) 同样未说明列 0 `---` 的检测窗口是整文件还是 `on:` 子树。
- **建议修法**: 在 `:63` 就地定义: 「区间 = 顶层 `on:` 键的**缩进子树** —— 自 `on:` 行起, 至下一个列 0 非空非注释行止, **块内空行不终止**(语料证据: `build-aria-runner.yaml` `on:` 块内含空行)」; 并在 `:65` 明写 D13 的 `---` 检测窗口为**整文件**(文档分隔是文件级语义, 不是 `on:` 子树级)。

---

### [MINOR] 勘正 2 的理据半边失实:「最近一次归档」实测不是 state-scanner 的归档

- **位置**: `:160`
- **问题**: `:160` 写「基线路径不能用 `latest` symlink 或「最近一次归档」…**二者均解析到 state-scanner 的归档**」。后半句与事实不符。
- **证据** (实测 `aria-plugin-benchmarks/ab-results/`):
  - `latest -> 2026-05-13-state-scanner-issue-101-fix` ✅ 属实。
  - 「最近一次归档」按名序与按 mtime 序都是 **`2026-07-20-v1.62.0-phase4-rule6`** (不是 state-scanner; 该目录含 `benchmark.json`, 是合法归档)。该目录建于 2026-07-20, 早于 L 侧 R2 (2026-07-25+), 故当时也不成立。
  - 危害面窄 (结论「写死路径」本身正确), 但这是一条**可机械证伪**的理据; 按 memory `feedback_rationale_formula_contradiction_is_signal`, 错理据会在 tasks/实现里被照抄成错前提 (例如有人据此去「排除 state-scanner 归档」而不是「写死本 skill 归档」)。
- **建议修法**: 把 `:160` 的理据列改为分述: 「`latest` symlink → `2026-05-13-state-scanner-issue-101-fix`;「最近一次归档」→ `2026-07-20-v1.62.0-phase4-rule6`。**两者都不是本 skill 的**, 故基线路径写死 `…/2026-05-10-phase-c-integrator-pre-merge-gate/benchmark.json`」。结论不变, 只修理据。

---

### [MINOR] 拒并 L-6 后, 替代解 (独立 tempdir) 有一条未成文的必要前提, A1 新增的 SC-29/30/31 全部继承它

- **位置**: `:255` (§修订记录「L-6 未并入」) / `:224` (Impact, A1 把 SC-29~31 加进同一行)
- **问题**: `:255` 用「fixture 用独立 tempdir 非 repo.parent」作为 L-6 的替代解, 并明确「**不引入双层结构**」。该替代解要成立, tempdir 必须是一个 **`git init` 过、且有 main + PR 两个分支和真实 commit** 的仓库 —— 否则 `git rev-parse` / `git diff` 失败, 规则 1 短路成 `unknown`/`git-diff-failed`, 所有期望 `covered`/`not_applicable` 的 parser 级 SC **结构上不可达**。这个前提全文未写。
- **证据**:
  - 实读 `:255`: 只说「独立 tempdir 非 repo.parent」, 无 git 初始化要求。
  - 反事实: 一个裸 `tempfile.mkdtemp()` 目录 → `:71` 规则 1「非 repo → 整体 `unknown`, reason=`git-diff-failed`」 ⇒ SC-2/3/4/5/20/23 与 **A1 新增的 SC-30/SC-31** 全部拿到 `unknown`, 断言无一可达期望值。
  - A1 在 `:224` 把 SC-29~31 追加进同一行, 使新增的三条 SC 一并继承这条未成文前提; 其中 SC-29(a) 还额外要求 tempdir 内能创建**非 ASCII 路径**。
  - 失败方向是响亮的 (测试红, 非静默通过), 故只记 MINOR —— 但这是拒并 L-6 时唯一该补的成文条件。
- **建议修法**: `:224` 括注补一句: 「tempdir 须 `git init` + 至少 base/PR 两分支与真实 commit (否则规则 1 短路成 `unknown`, parser 级 SC 结构上不可达); SC-29(a) 另需能在该 tempdir 创建非 ASCII 路径」。

---

## 范围声明

以上 8 条全部落在授权范围内 (A1 新增 4 处, 或 A1 与既有条款/既有 SC/机读面的一致性)。
findings 3 与 5 分别牵动 `:3` 与 `:68` 两处**既有**文本, 但两者都是 A1 引入的矛盾的另一端,
不是对既有内容自身质量的复审。无 OUT_OF_SCOPE 条目。
