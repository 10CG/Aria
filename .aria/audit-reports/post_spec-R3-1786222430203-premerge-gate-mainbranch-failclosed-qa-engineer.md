---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T21:06:37.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec Round 3 — qa-engineer 席位报告

## 审计结论

本轮性质是「砍掉的能不能砍」而非「新增的对不对」，因此本报告**不复核 R1/R2 旧清单**，只针对 R2-fix 后残留的 186 行版本本体做独立事实核验。核验方法：全部对当前代码 (HEAD 98ad1f5) 实读 + 实跑 + 对 SC-M4/M5 两条 grep 断言做**真实字符串模拟**（不是纸面推断），并用 `git`/`pytest`/`python3` 现场验证每一条数字性声明。

**主要结论**：Spec 在事实性数字上极其扎实——24 处调用、DEFAULT_CONFIG 9 键、SC-M1/M2 的 argparse/TypeError 行为、111 基线测试数、R1/R2 审计报告存在性，**全部逐条复核通过，无一处数字造假或引用漂移**。但 SC-M4（`pre_merge_gate.py` 全文 grep 断言）本身携带一个我用实际字符串模拟验证过的**结构性缺陷**：Spec 自己的措辞（"无 `\"main\"` 字面量"，"机械 grep，零裁量"）在两个最自然的实现方向上都会失效——窄模式（带引号 `"main"`）对 baseline 的 3 处命中只捕获 2 处（漏 :21 docstring 裸词），若 Phase B 漏改该行，测试仍会**假绿**；宽模式（裸词边界 `\bmain\b`）在完整应用三处修复后仍残留 **14 处**命中（含 `def main()` / `sys.exit(main())` 本体），**永远无法收敛为绿**。这正是被要求核查的"一条会漏的 grep 断言是假绿"的实例，且是双向失效（假绿 + 恒红两个可复现的具体实现都踩坑）。SC-M5（SKILL.md 侧）用窄模式 (`--branch main` / `"branch": "main"`) 复核则精确收敛，无此问题——两条 grep 断言不能一概而论。

另需指出：D4（存在性核验移出）留下的"显式传一个错的分支名"路径，当前测试套件**零覆盖**（已用 grep 逐一核实），但 Spec 在 §移出面表格中已诚实、显式地区分了这是"另一个缺陷"，并非隐瞒——这一点应被记入判断。

## Verdict

**FAIL**（1 Critical）。verdict 判据：0C+0M=PASS；0C+≥1M=PASS_WITH_WARNINGS；≥1C=FAIL。本轮发现 1 项 Critical（SC-M4 grep 机制本身不可靠，且该发现有可复现的字符串级证据，非推测）、1 项 Major（D4 遗留的显式错值路径零测试覆盖）、2 项 Minor。

## 轮次记录

### 已逐条核验并确认准确的 Spec 声称（正面记录，非 finding，避免报告只讲负面）

| Spec 声称 | 核验方法 | 结果 |
|---|---|---|
| `gate_check(` 调用点 24 处，显式传 `main_branch=` 0 处 | `grep -n "gate_check("` / `grep -n "main_branch="` 全文 | **24 / 0，精确匹配** |
| `test_pre_merge_gate.py` 46 + `test_ci_backends.py` 25 + `test_path_coverage.py` 40 = 111 | 三个文件分别 `pytest -q` | **46 / 25 / 40，合计 111，全绿，精确匹配** |
| `DEFAULT_CONFIG` 9 键，不含 `main_branch` | 实读 `pre_merge_gate.py:53-65` | **9 键（enabled/ci_backends/no_ci_fallback/wait_timeout_seconds/wait_check_intervals/primitive_call_timeout_seconds/poll_chunk_seconds/user_escape_hatch/path_coverage_enabled），无 `main_branch`** |
| `_normalize_config` 的 alias 表不会把旧键翻译成 `main_branch` | 实读 `_OLD_TO_NEW` 映射表 (`:69-72`) | **只含 `primitive_preference→ci_backends`、`no_aether_fallback→no_ci_fallback` 两项，与 `main_branch` 无关** |
| SC-M1：CLI 缺 `--main-branch` → RC≠0，stderr 含 `--main-branch` | 用等价 argparse 配置直接模拟 | **RC=2，stderr 含 `--main-branch`，精确匹配** |
| SC-M2：函数缺 `main_branch` → `TypeError` | 用等价签名直接模拟 | **`TypeError: gate_check() missing 1 required positional argument: 'main_branch'`，精确匹配** |
| `test_sc12_default_true_lock` 是唯一断言 `main_branch=` 值的既有测试 | 全文 `grep "main_branch="` + `grep "pc_eval"` | **确认唯一，位于 :668-670，其余 23 处 `gate_check(` 调用对 main_branch 字符串值无差别断言（均走 mock backend）** |
| SC-M5：SKILL.md 今日命中 `--branch main` / `"branch": "main"` 各 3 处 (167/243/270) | 窄模式 grep + 应用 Impact 表描述的修法后重跑模拟 | **改前 3 处精确命中；应用三处修法后模拟残留 0，无新增误报（171/242/253/589/590/765 等含"main"的行均正确排除）** |
| SKILL.md:765 `skip_if: in [develop, main]` 与本 Spec 无关 | 实读上下文 | **确认属 C.1/C.2 的 skip_evaluation 机制，与 C.2.4 gate 无关，非遗漏** |
| `state-scanner/phase1_gate.py` 的 `run_gate` 与本 skill `gate_check` 无引用关系 | 全文 grep | **确认零引用，Spec 区分准确** |
| R1/R2 十份席位报告 + 两份 aggregate 均存在 | `ls .aria/audit-reports/` | **12 个文件全部存在，时间戳连续合理** |

### Finding 1（Critical）：SC-M4 的 grep 机制在两个自然实现方向上都失效——非推测，已用真实字符串模拟复现

**"怎么会红"不是本条问题所在——问题是"怎么会假绿"和"永远不会绿"，各有一个可复现实例。**

现状（`pre_merge_gate.py`）三处 "main" 相关命中的**字面形态并不统一**：

```
:21   [--main-branch main]                                   ← 裸词，无引号（docstring 内文本）
:300  main_branch: str = "main",                              ← 带引号
:427  parser.add_argument("--main-branch", default="main", help="Main branch to check (default: main)")  ← 带引号 + 该行另含裸词 "main"（help 文本内）
```

**模拟 A（窄模式，带引号 `"main"`，与 Spec 自己 SC-M4 单元格的措辞"无 `\"main\"` 字面量"逐字一致）**：

```
候选A (带引号 "main") 改后残留命中: 0
```

看似收敛，但——用 Python 脚本模拟"只改 :300 与 :427，故意漏改 :21"这个场景（真实存在的实现失误，:21 是文档性 docstring，最容易被 Phase B 实现者当作"不影响功能"而顺手漏掉）：

```
场景: line21 遗漏未改, 带引号模式 '"main"' 残留命中: 0   ← 假阳性：判绿，但 :21 其实没改
```

**这就是任务书要求核查的"一条会漏的 grep 断言是假绿"，且不是理论推演，是我在当前代码上跑出来的真实结果。**

**模拟 B（宽模式，裸词边界 `\bmain\b`，为了不漏 :21 而做的"更完整"版本）**：

```
候选B (裸词边界 \bmain\b) 改后残留命中: 14   ← 应用全部三处修复后依然为 14，永不收敛
上下文示例: 'r-branch <branch> --main-branch <name> [--co'   （--main-branch 本身，标志名，必须保留）
           'ser.add_argument("--main-branch", required=T'  （同上）
           'PR CI passing + (b) main branch no in-flight'  （模块 docstring 首段散文，Rule #8 说明）
           '"waiting on main in-flight runs only'          （raw_message 动态字符串内容）
```

且未在上述截断列表中出现、但同样命中的还有 `def main(argv: ...)` 与 `sys.exit(main())`——**Python 入口函数名本身**，与分支名字面量毫无关系。这意味着宽模式**结构性地不可能归零**，即便三处目标全部正确修复。

**结论**：SC-M4 描述的"机械 grep，零裁量"这一自我定性不成立——真实存在的两条自然实现路径，一条产生假绿（漏检真实缺陷），一条永久报红（不可能收敛，因为命中了 `main()` 函数名与合法散文）。这不是"实现细节留给 Phase B 裁量即可"的量级问题：本 Spec 存在的全部理由就是"一个信号猜错时会不会被发现"（§Why 判据原文），而 SC-M4 如果照最直觉的方式实现（窄模式），恰好复刻了这个判据要根治的那种"猜错但发现不了"的失效模式——只是猜错的对象从"分支名默认值"变成了"这个测试到底测没测到 :21"。

**建议修法**（供 Phase B 参考，不代表本审计要求采纳此具体方案）：SC-M4 不应是单一全文正则，应改为**逐行定点断言**——分别读取 `:21`/`:300`/`:427` 三行的确切内容并断言其不再包含目标子串（如 `assert "[--main-branch main]" not in line21_text` 而非全文 regex）。这样规避了"全文单一模式"在精确率与召回率之间的结构性两难。

**anchor**: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md:105`（SC-M4 表格行）+ `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py:21,300,424,427,444`

---

### Finding 2（Major）：D4 移出"存在性核验"后，"显式传一个错的分支名"路径当前零测试覆盖——与本 Spec 治的缺陷同构，但 Spec 已诚实披露

**核验**：全文 grep `main_branch="[^m]` 与 `main_branch=` 于 `tests/*.py`，唯一命中是 `test_sc12` 里对 `evaluate_path_coverage` 调用参数的断言（值为 `"main"`，即 baseline 值，不是"错误值"）。**当前 111 个基线测试中，没有任何一个测试显式传入一个语法合法但实际不存在/错误的分支名给 `gate_check` 或 `evaluate_path_coverage` 并断言其行为。**

这个残留缺口的严重性在于：Spec §Why 自己论证的核心机制——"main 猜错时恰好落进后端无法区分的空集，永远不会被发现"（`aether ci status --branch <任意值> --in-flight` 对不存在分支与"存在但无 in-flight"返回同形）——**在"必填"修复后依然原样成立，只是触发条件从"忘记传参"变成"传了但传错"**。§移出的面 表格第 2 行也明确写了"它治的是显式传了错值，与本 Spec 治的缺省是错值是两个缺陷"——这个区分是对的，但区分之后，Spec 没有为这第二个（暂不修的）缺陷留一个"证明它确实还在"的回归钉子测试。目前只能靠读文档知道这个洞还在，代码层面无法自证。

不算隐瞒（`D4` 行 + `§移出的面` 表格 + `proposal.md:182-186` 的"待 R3 重点审"段落都清楚写了这是两个缺陷、有意不修），因此不评 Critical。但 follow-up issue 目前只承诺"移出的四个设计面 + 两套件覆盖不到 C.2.4"（`§Impact` 表 "follow-up issue" 行），**没有承诺携带"当前零测试覆盖"这个具体事实**——建议 follow-up issue 显式带上这一条，否则这个"暂不修"的状态可能在后续迭代中被无声地当成"已经够安全了"。

**anchor**: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md:73`（§移出的面 表格第 2 行）+ `proposal.md:152`（follow-up issue 行）+ 全仓 `tests/*.py` grep 结果（零命中）

---

### Finding 3（Minor）：SC-M3"负控"检验力接近重言式（tautological），建议改用参数流转断言

`gate_check` 内部对 `main_branch` 的唯一用法是原样透传给 `evaluate_path_coverage(main_branch=...)` 与 `backend.query_branch_in_flight(main_branch)`——在当前 111 个测试全部 mock 掉 backend 的前提下，**mock 对象不关心传入的字符串值是什么**（除非像 `test_sc12` 那样专门断言调用参数）。这意味着"显式传 `--main-branch master`，行为与现状逐字一致"这条负控，只要 `gate_check` 的内部分支逻辑本身没被动到（本 Spec 明确没有动），**在 mock 化测试下天然为真，与是否真的做对了三处字面量替换几乎无关**——它更像是"这次编辑没有语法错误/没有意外破坏其他代码路径"的冒烟测试，而不是针对本 Spec 变更风险面的定向回归。

不是缺陷（作为廉价冒烟保险有其价值，本 Spec diff 极小，这个测试的低区分力后果也小），但 Spec 声称的"红则说明改坏既有路径"这个因果关系在当前设计下**没有一个具体机制能让它真的红**（除非实现者手滑引入语法错误）。建议：若要让 SC-M3 有实质检验力，应比照 `test_sc12` 的模式，断言 `main_branch="master"` 确实被原样传递到 `evaluate_path_coverage`/`query_branch_in_flight` 的调用参数，而不仅仅断言输出 verdict 字典相等。

**anchor**: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md:104`（SC-M3 表格行）

---

### Finding 4（Minor）：`pre_merge_gate.py:427` 的 `help=` 文案未被 Spec 表格显式钉住，存在"必填但 help 仍写默认值"的文档失真风险

`§What Changes` 表格第 1 行只写"`add_argument("--main-branch", default="main", ...)` → `add_argument("--main-branch", required=True, ...)` (无 default)"，其中的 `...` 省略了 `help="Main branch to check (default: main)"` 这部分。若 Phase B 实现者只替换 `default="main"` → `required=True` 而不动 `help=` 字符串，`--help` 输出会继续显示"(default: main)"，与"必填、无默认值"的真实语义矛盾——对照 §Why 的核心判据（"信号猜错会不会被发现"），一个自相矛盾的 `--help` 文案本身就是一种新的、小号的"猜错但不易发现"来源（人类操作者会读 help 文本判断该不该传参）。

顺带verify：该 help 文案中的裸词 "main" (`(default: main)`) 恰好**不会**被 Finding 1 讨论的窄模式 `"main"`（带引号）grep 捕获（因为它前后没有紧邻的引号），这进一步印证 Finding 1 里"这个字段的字面形态本来就不统一，单一正则天然力不从心"的判断。

**anchor**: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md:45`（表格第 1 行）+ `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py:427`

---

## 附：验证命令留痕（节选）

```bash
# 24 处调用 + 0 处显式 main_branch
grep -n "gate_check(" aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py | wc -l   # 24
grep -n "main_branch=" aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py           # 仅 :669 (assertion, 非 call)

# 111 基线
python3 -m pytest tests/test_pre_merge_gate.py tests/test_ci_backends.py tests/test_path_coverage.py -q
# 111 passed in 5.06s (46 + 25 + 40 分别验证)

# SC-M4 双模拟（完整脚本见本轮工具调用记录）
# 候选A（带引号 "main"）: 漏改 :21 时残留命中 = 0  → 假绿
# 候选B（裸词边界 \bmain\b）: 完整修复后残留命中 = 14 → 永不收敛（含 def main() / sys.exit(main())）

# SC-M5 模拟（窄模式 --branch main / "branch":"main"）: 完整修复后残留命中 = 0，无新增误报
```

无文件被修改，无 commit/push。
