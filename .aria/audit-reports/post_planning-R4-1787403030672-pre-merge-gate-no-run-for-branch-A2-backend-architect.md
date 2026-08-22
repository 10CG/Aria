---
checkpoint: post_planning
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 1787409562200
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A2-backend-architect
critical_count: 0
major_count: 2
minor_count: 1
---

# post_planning R4 (末轮) — A2 (backend-architect) 审计报告

## 摘要

R3 归本席两条 (M1: TASK-013/INV-1 `git show` 缺 `-C aria`; m1: `grep -c 'return "pending"'` 对基线命中 2 处无方向判别力) 在 v4 均已**如约落地**: INV-1.encoded_as 全部命令改为 `git -C aria show`, 且把 grep 计数换成实跑 `_normalize_pr_ci_status([])` 取真值——两条各自陈述的具体问题均已消失。

但 R4 专项复核 (核实这个"跑函数"新机制本身是否真能跑通) 发现一处**新** Major: 四合取的前两项 (`git -C aria show <c>^:...aether.py` / `<c>:...aether.py` 管道进 python exec 后裸调用 `_normalize_pr_ci_status([])`) **在 parent 与 child 两种提交状态下都会因两个独立原因直接崩溃, 而非产出真值**——(a) aether.py 顶层 `from .base import CIBackend, CIStatus, InFlightStatus` 是相对导入, 脱离包上下文管道执行必 `ImportError: attempted relative import with no known parent package` (已用当前基线 9e6a17c 实测复现, TASK-003 不改动 import 结构, child 提交必同样复现); (b) 即便绕过 (a), `_normalize_pr_ci_status` 现实为 `class AetherBackend` 内的 `@staticmethod`（`:217`), exec 后该名字只绑定为 `AetherBackend._normalize_pr_ci_status`, 裸名调用会 `NameError`。v4 把"跑函数消除恒真"作为对 R3 A1-M2/A2-M1 的修复手段, 但字面写法本身不可执行——四合取的核验能力不是从"恒真"变成"能真正判别", 而是变成"恒报错", 若被误判为"检查已失败"是假阳性, 若被绕过跳过则是 A2-M1 当初要消除的"实施者临场发挥"原样复发。已给出实测可跑的替代写法 (见 Findings)。

另一处新 Major 与本席专项任务 (TASK-010a 依赖核查) 相关: v4 新增 TASK-010a 直接依赖 TASK-003, 但 `metadata.exec_order_note` 里"TASK-003 ∈ …的依赖闭包"枚举清单未回填 TASK-010a (仍是 v3 的 11 项旧清单), 该字段是本 spec 逐轮机检并核对数字的"机检不变量"字符串 (R3 A5/A2 报告都逐项核对过这个数字), 本轮若照此字符串核验会与真实计算出的闭包 (12 项, 含 010a) 不一致——注意: **实际依赖图本身没有问题** (逐任务 exec_order > 依赖 exec_order 20 项全表复核通过, 见下方), 缺陷只在这条描述性/机检用文本字段落后于图结构。

TASK-010a→TASK-009 的依赖边本身另有一处 Minor: 其 title/verification 列出的 5 条 RED 断言均未引用 TASK-009 (gate_state_helper.py/CLI) 内容, 与其对 TASK-003 的依赖 (有「DEFAULT_CONFIG 断言绿 (003 已落)」旁注证成) 形成对比, 疑似缺一条断言或依赖边可精简。

## R3 处置核对

| R3 finding (归本席) | 承诺内容 | v4 证据 | 判定 |
|---|---|---|---|
| A2-PP3-M1 (Major): TASK-013/INV-1 `git show <c>^:path` 缺 `-C aria`, 与 TASK-013 内另两条命令 cwd 隐含约定冲突 | 命令前一律加 `git -C aria` | 实读 `metadata.invariants[0].encoded_as`: 四处 `git -C aria show` 全部带 `-C aria`; `TASK-013.verification`: "INV-1 有向语义核验 (四合取, 见 INV-1.encoded_as; **全部 `git -C aria`, 命令在主仓根执行**)" | **closed**（但见下方 PP4-M1: 该重写引入新的、更根本的可执行性缺口） |
| A2-PP3-m1 (Minor): `grep -c 'return "pending"'` 对基线命中 2 处, 计数无法定位"零 run"分支 | 改用能定位到具体分支的判别式 (如锚定 `if not runs:` 或对函数结果取值) | 实读: R3 的 grep 计数已整条撤除, 换成实跑 `_normalize_pr_ci_status([]) == 'pending'` / `== 'not_found'` 语义谓词——不再是无方向的字面量计数, "命中 2 处但答不出方向"的具体问题已消失 | **closed**（新写法自身的可执行性是 PP4-M1 的范畴, 与 m1 原问题不同一件事） |

r3_closed=2, r3_partial=0, r3_not_addressed=0（本表 2 行 = R3 聚合表中归本席贡献进 cluster#2 的两条原始 finding）。

## 已核验无误 (逐条抽样)

- **exec_order 全表拓扑核验 (v4 20 任务, 含新增 TASK-010a)**: 000(0)→000b(1,[000])→001(2,[000b])→004(3,[000b])→002(4,[000b,004])→003(5,[002])→005(6,[004,003])→006(7,[005,003,001])→007a(8,[001,006])→007b(9,[007a])→008(10,[000b])→009(11,[008])→010a(12,[003,009])→010(13,[009,003,010a])→011(14,[006,007b,010,001,010a])→013(15,[003,006,007b,009,011])→012(16,[010,011,013])→014(17,[009,010,011,013])→015(18,[012,013,014,001])→016(19,[015,001])。逐任务 exec_order 严格大于其全部 dependencies 的 exec_order, 20 项全部成立, TASK-010a 插入未引入新的顺序违例——**图结构本身正确**, 问题只在 PP4-M2 指出的描述性文本未同步(见下)。
- **负控 pattern 基线复测**: `grep -rn -E 'DISPATCH_VIABLE|dispatchable_workflows|/dispatches -d'` 限定 6 个目录 (phase-c-integrator/{scripts,tests,SKILL.md} + workflow-runner/{scripts,tests,SKILL.md}) 实跑 0 命中 (exit 1); `pre_merge_gate.py` 中 `<pr_branch>` 计数 0; `_no_run_gate_error` 基线尚不存在 (true 分支对偶断言的目标函数留待 TASK-007b 建) —— 与 metadata declaration 及 R3 aggregated "A4: 新 pattern 基线 0 命中" 结论一致, 无回归。
- **TASK-010a 的 RED 测试基础设施先例真实存在**: `aria/skills/state-scanner/tests/test_spec_complete.py:94` `_ARIA_META_ROOT = Path(__file__).resolve().parents[4]` + `:99-108` `_require_meta_archive()` skip 逻辑均实读确认, 与 TASK-010a notes 所引"parents[4]+skip 先例"逐字吻合；TASK-010a 测试文件路径 `aria/skills/phase-c-integrator/tests/test_doc_sync_no_run.py` 与该先例同深度 (tests→skill→skills→aria→meta-root), 可直接复用。
- **INV-1 rule↔encoded_as 未见方向或语义倒置**: rule 讲"为何必须同 commit" (fail-open 论证), encoded_as 讲"如何核验" (四合取), 四合取自身的**判别逻辑设计** (拆分提交时第 2/3 项应分别落空) 在假设"exec 能正常产出真值"的前提下是自洽的——缺陷是这个前提目前不成立 (PP4-M1), 非设计方向错误。

## Findings

### [A2-backend-architect-PP4-M1] INV-1 四合取前两项的"管道进 python exec 后裸调用 `_normalize_pr_ci_status([])`"字面不可执行 (两个独立原因, parent/child 提交均 100% 复现)

- **Category**: executability
- **Scope**: `metadata.invariants.INV-1.encoded_as` (第 1/2 项) / `TASK-013.verification` (转述同一命令)
- **问题**:
  1. **相对导入**: `aria/skills/phase-c-integrator/scripts/ci_backends/aether.py` 顶层 `from .base import CIBackend, CIStatus, InFlightStatus` 是包内相对导入。`git -C aria show <c>^:....aether.py | python3 -` (或等价 `exec(sys.stdin.read(), globals())`) 脱离包上下文执行, 该行必抛 `ImportError: attempted relative import with no known parent package`——**已用当前基线 9e6a17c 实测复现** (两种自然读法: `python3 -` 直接吃 stdin、以及 `python3 -c "exec(sys.stdin.read())"`, 结果相同)。TASK-003 不改动 aether.py 的 import 结构 (deliverables 只提 `:218 docstring, :225-226`), 故 child 提交 (`<c>:...aether.py`) 会以完全相同方式复现。
  2. **裸名与实际绑定不符**: 即便 (1) 被绕过, `_normalize_pr_ci_status` 现为 `class AetherBackend` 内的 `@staticmethod` (`:217`, 由文件顶部迁移注释 "`_normalize_pr_ci_status() → AetherBackend._normalize_pr_ci_status() (private)`" 确认), exec 该文件后此名字只存在于 `ns['AetherBackend']._normalize_pr_ci_status`, 全局裸名 `_normalize_pr_ci_status` 未绑定, 引用它会 `NameError`。
  四合取采用 AND 语义, 前两项若统一实现为"exec 后取值比较", 在 parent 与 child 两种场景下都会**无条件**先于任何真实判定崩溃——这与"是否真的拆分提交"无关, 即"四合取任一拆分落地时第二/三项必红"这条设计推理 (rule 段的论证) 在假设 exec 能正常返回布尔值的前提下才成立, 目前该前提不成立。v4 把这处从 R3 的"grep -c 恒真"改成"跑函数", 目的是让核验真正具备方向判别力 (消除恒真), 但字面写法把"恒真"换成了"恒报错"——同样是零信息量的一种 (memory `false_green_dual_is_permanent_red` 同形状: 判定机制的"健康常态值"应是能产出 pending/not_found 的布尔真值, 而不是异常)。且 `ImportError` 若被 main-loop 误读为"该检查判定失败/TASK-003 违反 INV-1", 是比"跳过不判"更危险的假阳性; 若被当作"环境问题, 这次先跳过", 就是 A2-PP3-M1 当初想消除的"实施者临场发挥"原样复发。
- **实测 (已验证可跑的替代写法)**:
  ```
  git -C aria show HEAD:skills/phase-c-integrator/scripts/ci_backends/aether.py \
    | sed 's/^from \.base import .*/CIBackend = CIStatus = InFlightStatus = object/' \
    | python3 -c "
  import sys
  ns = {}
  exec(sys.stdin.read(), ns)
  print(ns['AetherBackend']._normalize_pr_ci_status([]))
  "
  # 输出: pending (exit 0)
  ```
  `_normalize_pr_ci_status` 方法体本身 (`:217-237`) 只用标准库 (`sorted`/`.get`/字符串方法), 对 `.base` 三个类型 (`CIBackend`/`CIStatus`/`InFlightStatus`) 零运行时依赖 (`from __future__ import annotations` 使类型注解惰性求值, 不需要真解析)——用 `sed` 把该 import 行替换为三个占位赋值 (足以让 `class AetherBackend(CIBackend):` 的基类引用有效), 即可无副作用地让整个文件 exec 通过, 且不改变被测函数的真实语义。
- **建议**: 在 `INV-1.encoded_as` (以及 `TASK-013.verification` 复述处, 二者应同步改) 的四合取第 1/2 项补两处: (i) exec 前用 `sed`/等价手段中和 `from .base import ...` 这一行 (给出上面已验证的具体命令); (ii) 取值引用改为 `AetherBackend._normalize_pr_ci_status(...)`, 不用裸名。改完后四合取的"拆分提交时第 2/3 项必红"这条设计推理才具备被真正验证的基础。

### [A2-backend-architect-PP4-M2] `metadata.exec_order_note` 的 "TASK-003 依赖闭包" 枚举清单未回填 v4 新增的 TASK-010a (11 项旧清单 vs 实际 12 项)

- **Category**: transcription
- **Scope**: `metadata.exec_order_note` (行 15)
- **问题**: `exec_order_note` 声明的机检不变量原文: `"TASK-003 ∈ 005/006/007a/007b/010/011/012/013/014/015/016 的依赖闭包"` —— 数一下是 **11** 项。但 v4 新增的 `TASK-010a` (`dependencies: [TASK-003, TASK-009]`, 见行 298) **直接依赖 TASK-003**, 理应也在这个闭包集合里, 使真实闭包变为 **12** 项 (`010a` + 原 11 项)。这条 "机检不变量" 文本字段正是本 spec 每轮拿来逐项核对数字的对象 (R3 A2/A5 报告都实核过"TASK-003 ∈ 11 任务下游闭包"这个数字并与本字段比对), 本轮若照此字符串核验会与真实计算出的闭包大小 **不一致**——是 v4 引入 TASK-010a 后遗留的回填缺口 (memory `ad_slot_backfill_checkpoint` 同形状: 新任务插入后, 既有的机检占位文本未跟着回填)。
  需强调: **依赖图本身没有被破坏** —— TASK-010a 的 exec_order (12) 严格大于其依赖 TASK-003 (5) 与 TASK-009 (11) 的 exec_order, 20 任务全表拓扑序复核通过 (见"已核验无误")；缺陷仅限于这条描述性/机检对照用的枚举字符串落后于图结构一步。
- **建议**: 把 `exec_order_note` 改为 `"TASK-003 ∈ 010a/005/006/007a/007b/010/011/012/013/014/015/016 的依赖闭包"` (12 项, 顺序不影响语义), 或按 exec_order 排序写成 `005/006/007a/007b/010a/010/011/012/013/014/015/016`。

### [A2-backend-architect-PP4-m1] TASK-010a→TASK-009 依赖边缺内容证成 (5 条 RED 断言均未涉及 TASK-009/CLI)

- **Category**: coverage
- **Scope**: `TASK-010a.dependencies`
- **问题**: `TASK-010a.dependencies: [TASK-003, TASK-009]`。对 TASK-003 的依赖有明确旁注证成 ("DEFAULT_CONFIG 断言绿 (003 已落)", 对应"主仓 config.template.json 含两 key"断言需要 import 已改的 `DEFAULT_CONFIG` 做交叉核验, 与 TASK-010 的 "config-template-key-currency 探针" 同一手法, 站得住)。但对 TASK-009 (`gate_state_helper.py`/CLI) 的依赖, title 与 verification 列出的 5 条 RED 断言 (SKILL.md `pr_ci_status` 枚举行 / `:172-183` 含 `gate_error` / config.template 两 key / DEC 前向指针 + 📌 / `path_coverage.py:36` 为 8) **没有一条**引用 `gate_state_helper.py` 或其 CLI 内容——都是 phase-c-integrator/DEC/config.template 域的检查, 与 workflow-runner 的 CLI 实现无关。真正需要 TASK-009 内容的是 **TASK-010** (GREEN 端, 要写 "经 CLI 显式 `--state-file` 全旗标"这类依赖真实 CLI 签名的文档), 而非 TASK-010a 这条本该在 TASK-010/011 之前跑的 RED 测试。
- **建议**: 要么在 verification 里补一条真正需要 TASK-009 内容的断言 (例如校验 SKILL.md 提到的 CLI flag 名与 `gate_state_helper.py` 实际 argparse 定义一致), 要么把 `TASK-010a.dependencies` 精简为 `[TASK-003]` (若精简, 记得同步剔除 PP4-M2 建议清单里对应位置的 010a 前置假设不受影响, 因为 010a 对 TASK-003 的依赖不变)。不影响 TDD 红绿正确性, 只是过度约束/未证成的耦合, 不阻塞进 B.1。

## Verdict

PASS_WITH_WARNINGS — vote: REVISE（2 Major 建议在 B.1 起跑前收敛: (1) INV-1 四合取前两项的 exec 写法补 `sed` 中和相对 import + 改引用 `AetherBackend.` 前缀, 否则 main-loop 在 TASK-013 执行时会 100% 撞见 ImportError/NameError 而非拿到真实判定; (2) `exec_order_note` 的 TASK-003 闭包枚举补回 TASK-010a (11→12 项)。两条都是文本/命令层面的小改, 不涉及重新规划依赖图或任务粒度。1 Minor (TASK-010a→009 依赖证成) 可选顺手改, 不阻塞。R3 归本席两条 finding (`-C aria` 缺失 / grep 计数无方向性) 均已如约落地关闭; 负控 pattern 基线复测 0 命中, exec_order 20 任务全表拓扑序复核无违例, 未发现违反 spec 不变量或漏 SC 承载的 Critical 情形）。
