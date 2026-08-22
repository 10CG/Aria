---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T08:08:29.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A3-qa-engineer
critical_count: 0
major_count: 2
minor_count: 3
---

## 摘要

R3 复核 v3 (R2-fix + 设计收缩), 基线仍 aria @ `400f0bc`。实读 `pre_merge_gate.py` 全部早退分支 (逐行号核对 SC-7 的 8 个引用)、`aether.py:218-233`、`path_coverage.py:1-45`、`gate_state_helper.py` 全文 (含 `write_gate_state` 整块重建实现)、`test_gate_state_helper.py` 22 测试全文、`test_pre_merge_gate.py`/`test_ci_backends.py` 中所有 "pending" 相关用例、AB catalog `phase-c-integrator-pre-merge-gate.json` + `NEG-3-internal-error-surface.json`/`wait_then_green.json` 全文、`aria-plugin-benchmarks/ab-results/` 目录 (grep NEG-3 实际执行痕迹)、`.aria/state-checks.yaml` 的 `coordination-gate-invocation` 先例、`pre-merge-gate-empirical-traps.md` 现有章节号。

**0 Critical**: verdict 正确性 (AD-2 wait 结论)、`compute_verdict` 分支插入顺序守卫 (SC-4 红窗)、SC-6 not_applicable 结构性短路、reason 封闭集 "9→8" 勘正 (cluster #14) 均实读确认成立, 未见新的 fail-open 路径。

**2 Major (新)**: (1) NEG-4 沿用 NEG-3 形态注册进 catalog, 但 grep `aria-plugin-benchmarks/ab-results/` 全目录确认 **NEG-3 自 v1.65.3 上线以来从未被任何一次 AB run 实际执行过** (v1.66.0/#137 是最近一次 phase-c-integrator Rule#6 benchmark, 它为另一个行为新建了未入 catalog 的一次性 `eval-4`, 完全绕开了 NEG-3), rule6_note 对「序列型 fixture 无消费机制」诚实地做了「明记为缺口」的免责声明, 但没有对 NEG-3/NEG-4 这类结构上可被 `/skill-creator` 消费、实际上从未被消费的 fixture 做同等披露, "两条行为单步可证伪" 的说法因此只在理论上成立。(2) cluster #6 (TASK-0) 的处置声称「dispatch 2xx 但 600s 零 run 无第三分支」已解决, 但实读 v3 §3.5 确认修复只落在 **SC-13** (三分支), TASK-0a 自身仍是 "结果 = 布尔 `dispatch_viable`" 未定义该分支映射到 true/false 哪一侧 —— 这正是 F4 记录的高发瞬态, TASK-0a 是**先于实现执行**的一次性探针, 一旦命中该分支且无章可循, 执行者会现场发明判据写进 traps §6 (仓内 SOT), 污染后续所有实现的处方文案。

**已验证无新回归**: `_normalize_pr_ci_status([])` 的翻转只影响 `test_pre_merge_gate.py:363`; 全仓 grep 确认 `test_pre_merge_gate.py` 内其余 "pending" 用例 (`:128-129`/`:243-249`) 与 `test_ci_backends.py` 的 `query_pr_ci` 测试均走 `MagicMock` 直接返回字面量或非空 runs 列表, 不经过真实 `_normalize_pr_ci_status([])` 分支, 无隐藏回归面; `test_gate_state_helper.py` 22 测试全文确认无一条对 `write_gate_state` 返回 dict 做 exact-keys 断言, 新增 `gate_error_kind`(默认 `None`) 与派生的 `no_run_observations` 键不会使其变红。

## R2 处置核对

| 簇# | 状态 | 证据 |
|---|---|---|
| #6 (TASK-0 前置成环 + dispatch 2xx/600s 零 run 无第三分支, 含 A3 R2 #10) | **partial** | v3 §3.5 TASK-0a 正确拆分为「实现前纯 API 探针」且明确「§4 与全部 SC 不随之变化」—— 逐条 grep SC-1~SC-16 确认全表零处提及 `dispatch_viable`, 该断言**成立**。但 R2 disposition 承诺的「三分支结果」只字面落在 **SC-13**(「not_found→passing / 600s 仍 not_found 记拥堵数据点 / 4xx 记权限」), TASK-0a 自身 (§3.5) 的产出仍写「结果 = 布尔 `dispatch_viable` + 证据 (HTTP 码 / run id **或 600s 零 run** / Δt / 日期)」—— 它自己列出了「600s 零 run」这个证据形态, 却没有说这种情况下 `dispatch_viable` 该记 true 还是 false。TASK-0a 与 SC-13 是同形兄弟 (都是「dispatch → 轮询 → 判定」), 修复落在了后者身上、前者原地不动, 是 memory `fix-the-class` 点名的形状。 |
| #8 (NEG-4 未登记 catalog + rule6_note 猜测式引用, 含 A3 R2-M1) | **closed** (字面要求) / 新问题见 Findings | R2 point (a)(b) 的字面要求已核实落地: SC-15「NEG-4-no-run-for-branch.json 存在 **且登记进** `phase-c-integrator-pre-merge-gate.json` `fixtures[]` (含 `test_case_in_unit_tests` 绑定)」+ 「代码落点」/§5 均补了 AB 套件行; rule6_note 把「若无则新开」改成实名 `aria-plugin#127 (open, 正是 C.2.4 surface 义务零 eval 覆盖的缺口 issue)`, 与我 R2 用 `forgejo GET issues/127` 实查的原文一致。**但**本轮用新方法 (grep `ab-results/` 找 NEG-3 实际执行痕迹) 发现一个 R1/R2 都没测到的角度, 见 [A3-R3-M1]。 |
| #14 (reason 封闭集「9」未真正勘正, 含 A3 R2-M2) | **closed** | 实读 `path_coverage.py:20-33` 与 v3 §4 逐字比对: §4 现写「reason 族 = **8** (7 条规则终态 + internal-error; 模块 docstring `:36`「共 9 个」是既有错, 本 spec 顺手勘正)」; SC-2「8 reason」、SC-9「8 reason」均已同步改字; §5 文档同步表新增 `path_coverage.py :36 「共 9 个」→ 勘正 8` 一行。数字、修复落点、两条 SC 三处逐字一致, 不再互相矛盾。 |

## 新 Findings

### [A3-R3-M1] Major — NEG-4 沿用 NEG-3 的「登记进 catalog」形态, 但同形前例 NEG-3 有实证的零执行记录; rule6_note「两条行为单步可证伪」目前只是理论可行, 缺可执行的证据支持

**锚点**: `aria-plugin-benchmarks/ab-suite/phase-c-integrator-pre-merge-gate-fixtures/NEG-3-internal-error-surface.json` `_consumed_by` 字段; `aria-plugin-benchmarks/ab-results/` 全目录 (2026-08-22 实测 grep); `2026-08-16-v1.66.0-137-rule6/RESULT.md`; proposal `rule6_note` 第一条; SC-15。

**问题**: NEG-3 的 `_consumed_by` 字段自陈「Documentation + eval prompt data」——即它结构上*可以*被人工发起一次 `/skill-creator` with_skill/without_skill 对比来产生判决, 但这不等于*已经*或*会*被执行。实测 `grep -rln "NEG-3\|internal-error-surface" aria-plugin-benchmarks/ab-results/` 全目录**零命中**——NEG-3 自 v1.65.3 (2026-07-31 附近) 上线以来, 经过了至少两次后续的 phase-c-integrator Rule #6 全量 benchmark (`2026-07-31-v1.65.0-122-rule6` 早于它、`2026-08-16-v1.66.0-137-rule6` 晚于它), **从未被任何一次实际的 with_skill/without_skill 对比消费过**。更能说明问题的是 `2026-08-16-v1.66.0-137-rule6/RESULT.md` 原文——那次 benchmark 遇到了同一类「套件覆盖外」问题 (C.2.4 分支存在性核验), 它选择的处置方式不是去执行已经在 catalog 里躺着的 NEG-3, 而是**现场新建了一个 `eval-4-c24-gate-branchname`**, 产生了真实的 4/4 vs 1/4 数值 delta, 且这个 `eval-4` 本身也**没有被写回任何 catalog 文件** (`phase-c-integrator.json` 仍是 3 evals) ——它是一次性证据, 用完即弃。

这构成一个可复现的经验模式: 本仓库里「注册一个 `_target_behavior`/`_arm_expectations` 齐全的定向 fixture 进 catalog」这件事, 目前 100% (1/1 有据可查的先例) 不会带来一次真实执行; 真正被执行、产生判决数据的做法反而是不进 catalog 的一次性 ad-hoc eval。v3 的 rule6_note 对「序列型 (多轮 prompt) fixture 形态无消费机制」做了诚实披露 (`wait_then_green` 自陈 `_consumed_by: no consumer`, "明记为缺口不伪装已测")——但对 NEG-3/NEG-4 这类**结构上可被消费、实际上从未被消费**的单发 fixture, 没有做同等强度的披露, 隐含地把「结构上可行」当成了「已验证可行」。

**这如何回答任务指定的问题「AI 行为靠什么红」**: 两条点名行为里, (i)「surface `gate_error.message` 原文」在*有人真跑一次 /skill-creator 对比*的前提下确实单步可证伪 (fixture 输入 + 两版本输出 + 一个判别问题, 结构与 NEG-3 完全一致, 可信); (ii)「`should_prompt=true` 时出 prompt 而非继续等」同理, 只要 fixture 把「当前观测数已达阈值」的静态快照喂给一次 with/without 对比, 也是单步可证伪的判断题, 不需要真跑 90s 循环。**两条命题本身的可证伪性设计没有缺陷**——缺陷在于「谁来跑、什么时候跑」全无约束, 而本仓库刚刚给出的经验数据说明「登记进 catalog」这个动作本身并不会带来执行, 大概率重演 NEG-3 的命运。

**建议** (窄, 不需要重新设计):
1. NEG-4 的 `_consumed_by` 字段除了套用 NEG-3 的措辞外, 应额外注明它是「同形态第二个实例, 前例 NEG-3 自 v1.65.3 起零执行记录 (2026-08-22 `ab-results/` 核实)」, 避免下一个审计者/实现者误以为「登记 = 已验证」。
2. §6 Phase D 待办第 3 条 (追加评论到 `aria-plugin#127`) 里把这条经验数据一并写入 (NEG-3 从未被跑过 + `eval-4`/#137 的替代做法), 让 #127 讨论「AB fixture 是否是合适验证载体」时有本仓库自己的实证依据, 而不是纯理论讨论。
3. 若 Phase B/D 团队愿意做得更扎实一点 (可选, 不阻塞本 spec): 比照 `eval-4-c24-gate-branchname` 先例, 在 v1.66.4 发版的 Rule #6 benchmark 里**真跑一次** NEG-4 对应的 with/without 对比 (哪怕不写回 catalog, 只落一份 `ab-results/2026-08-xx-v1.66.4-152-rule6/` 记录), 这样「两条行为单步可证伪」就从「设计上成立」变成「已有一次真实判决数据支持」——成本与 #137 的 eval-4 相当 (一次 benchmark 里多一条 eval)。

**影响**: 不影响 merge 安全性; 削弱的是 Rule #6 判据表第三行「可证伪定向 fixture」这一义务的实际含金量, 且是本仓库自己 `ab-results/` 目录就能查出来的、非推测性的证据。

---

### [A3-R3-M2] Major — TASK-0a 自身仍未定义「dispatch 2xx 但 600s 内零 run」的 `dispatch_viable` 归属; cluster #6 disposition 声称的修复落在了 SC-13 而非 TASK-0a 本身

**锚点**: proposal §3.5 (TASK-0a); SC-13; R2 聚合表 cluster #6 disposition 原文「TASK-0 拆为 TASK-0a...结果=布尔 `dispatch_viable`...; §4 无条件实现...; SC-13 在实现后跑, 三分支结果 (...)」; F4 (`aether.py:225-226` 附近的注记 + Aether CLI `internal/ci/status.go:45-47`)。

**问题**: 逐字重读 v3 §3.5:

> 结果 = 布尔 `dispatch_viable` + 证据 (HTTP 码 / run id **或 600s 零 run** / Δt / 日期) 写入 traps §6

这句话本身已经列出了「600s 零 run」是探针可能撞到的一种真实证据形态 (与 F4「run 已建未被领 (瞬态)」逐字呼应——本 spec 全文反复引用的正是这个事实), 但紧接着要求的输出只是一个**布尔值**, 没有说这种「HTTP 2xx 但轮询 600s 全程零 run」的证据应该折算成 `dispatch_viable=true` 还是 `false`。

对照 cluster #6 的 v3 处置原文, 修复实际发生在 **SC-13**——「SC-13 在实现后跑, 三分支结果 (not_found→passing / 600s 仍 not_found 记拥堵数据点 / 4xx 记权限)」。但 SC-13 是**实现之后**跑的活体验收测试, 与 **TASK-0a**(**实现之前**跑的一次性纯 API 探针, 结果写入 `traps §6` 作为 (a) 处方行是否出现的**唯一**依据) 是完全不同的两个执行时点、不同的产出物、不同的消费方——一个给「验收」用, 一个给「traps SOT + prompt 文案取舍」用。R2 disposition 表把「三分支」处置和 TASK-0/SC-13 这两个概念**合并叙述**, 造成「已经解决」的印象, 但实读 v3 正文, TASK-0a 那句「结果 = 布尔 `dispatch_viable`」在拆分之后**逐字未变**, 没有获得 SC-13 那样的第三分支。

**按 spec 实施会怎样错**: TASK-0a 是本 Lab **提前于实现**执行的一次性动作, 执行者 (Phase A 批准后、Phase B 之前) 拿到 HTTP 2xx 但 600s 内 `aether ci status --branch <b> --json` 始终 `runs=[]` 时, spec 没有给出判定规则, 执行者只能**现场发明**——可能选择「记 true (至少 API 调用成功了)」也可能选择「记 false (没等到 run, 显然没用)」, 两种选择都合理但会**永久写入 traps §6 (仓内 SOT)**, 直接决定后续所有实现里 §3.3 处方 (a) 行是否出现在给人看的 prompt 里, 且没有任何后续机制去纠正一次「猜」出来的判定 (traps §6 是"不能靠读代码想出来"的经验沉淀, 不会被代码 review 挑出逻辑错误)。而 F4/CLAUDE.md 项目状态段都自陈 heavy 节点持续拥堵、Luxeno 延迟 45-54s 是当前常态——这不是刁钻边角, 是这个探针大概率真的会撞到的分支。

**建议**: 在 §3.5 补一句与 SC-13 对称的判定规则, 例如: 「HTTP 2xx 且 600s 内零 run → 本次结果记为 `dispatch_viable=inconclusive`(而非强行二值化), traps §6 附注"证据不足, 处方 (a) 行保守按 false 处理, 待下次机会 (如 SC-13 的三分支之一恰好命中同形态) 补充数据"」——与 Risks R-b 的既有措辞("阈值依据薄, 后果=早一次 prompt") 同一保守精神, 成本是一句话。

## 补充 Minor (未构成独立编号, 并入判定)

- **[m] SC-7 「八个行号 / 七个早退落点」的收缩规则只对 no-backend 一对显式声明, 对main-branch-check 一对未同等处理**: 实读 `pre_merge_gate.py` 确认 8 个引用行号 (`:363/:376/:418/:434/:455/:458/:489/:512`) 逐字准确对应各早退分支的判断/返回语句。但「其中 no-backend 两 fallback 值算一落点两变体」这句收缩规则只覆盖了 `:363`/`:376`(`_no_ci_output` 内两个真正独立的 `return` 语句, 键集相同但确实是两处不同代码位置的返回) ——而 `:455`/`:458` 结构上是**同一个** `if mb_status != "ok":` 块内的两条嵌套条件, 只服务于**同一个** `return _build_output(...)`(main-branch 分支存在性核验失败, kind 在 `main-branch-not-found`/`main-branch-verify-failed` 间取值, 但 gate_error 结构键集从不改变)——按「键集」标准这一对比 no-backend 那一对更应该被算作"一落点两变体", 但 spec 没有给它同等的收缩声明。8 → 7 的算术只有在"只收缩 no-backend 这一对、不收缩 main-branch 那一对"的不对称规则下才能凑出"七"。这不影响 Phase B 按行号钉回归测试的可执行性 (逐行断言键集不变依然是良定义的), 纯粹是自我描述的计数口径不一致, 可能让照字面数"七个"的实现者困惑, 建议要么把 main-branch 那一对也标注"同落点两变体"(得六个落点), 要么去掉"七个"这个数字只留行号清单。
- **[m, 信息性] SC-3 的 `True` 测试用例不能区分「显式排除 bool」与「凑巧被 `<2` 挡住」两种实现**: `_effective_prompt_threshold` 的有效阈值下限是 2, 而 Python `bool` 的数值上限是 1 (`True == 1`) ——任何形如 `isinstance(v, int) and v >= 2` 的实现, **不需要**任何针对 `bool` 的显式排除逻辑, 就会自然地把 `True`/`False` 都判为非法值回落默认。这不是行为缺陷 (两种写法在这个特定阈值范围下行为完全一致, 无法构造出一个真实配置值让二者产生分歧), 只是 SC-3 用「True→3」作为验收点无法证明实现者是否真的写了 `isinstance(v, bool)` 这一支——如果日后阈值下限改成 0 或 1, 这个隐藏的耦合就会浮现。记录为观察项, 不要求本 spec 处理。
- **[m] SC-13 「经 workflow-runner 路径跑一次 wait 循环」建议显式排除「人工模拟 CLI 序列」这一读法**: 现有措辞「经 workflow-runner 路径」已经比「经 CLI 序列」更精确地暗示需要走真实 skill 调用而非人工模拟, 但没有把这一点写死。考虑到 AD-7/F7 这条主线索恰恰是「reference 实现被证明零消费」, 而 SC-13+SC-16 组合要证明的正是"这次是真消费"——若执行者图省事直接手敲 CLI 序列伪造 telemetry, SC-13/SC-16 字面判据依然会全绿, 但没有验证到"一个读 SKILL.md 的 AI agent 会不会真的调用 CLI"这件事(与本 spec 反复强调的 F7 教训擦肩而过)。建议在 SC-13 里加一句「须由一次真实 phase-c-integrator/workflow-runner skill 会话完成, 不接受人工模拟 CLI 序列」, 把这层隐含意图显式钉死, 成本是一句话, 不改变测试结构。

## 未发现问题但已核验的点 (R3 新增核验)

- **回归面扫描 (任务项 4 前半)**: 全仓 `grep -rln "_normalize_pr_ci_status\|AetherBackend" --include="*.py"` 只命中 `ci_backends/*.py`/`pre_merge_gate.py`/`test_ci_backends.py`/`test_pre_merge_gate.py` 四个源。`test_pre_merge_gate.py` 内除 `:363` 外所有 "pending" 相关断言 (`:128-129` 直接传字面量给 `compute_verdict`、`:243-249` 经 `_make_aether_backend_mock(pr_state="pending")` 的 `MagicMock` 直接返回 `CIStatus(state="pending")`、`:358-360` 传非空 `runs` 列表) 均不经过真实的空-runs 归一化逻辑, 不受本次改动影响。`test_ci_backends.py` 里唯一调用真实 `_normalize_pr_ci_status` 路径的 `test_query_pr_ci_success_returns_cistatus` 用非空 runs, 同样不受影响。结论: 回归面精确等于 spec 自陈的 `:363` 一处, 无遗漏。
- **`gate_state_helper.py` / `test_gate_state_helper.py` 加参数安全性 (任务项 4 后半)**: 22 个测试方法逐条读取, 均按字段取值断言 (`gate["retry_count"]` 等), 无一处 `assertDictEqual`/`== {...}` 全字典比较; `write_gate_state` 新增的 keyword-only `gate_error_kind: str | None = None` 对 22 个既有调用点 (均未传该参) 只会在返回 dict 里追加 `no_run_observations=0` 一个新键, 不触发任何既有断言路径。SC-12「既有 22 全绿」可信。
- **cluster #6「dispatch_viable 唯一影响面=处方 (a) 行, 全部 SC 不随之变化」claim** (任务项 2): 逐条核对 SC-1 至 SC-16 全表, 无一条提及 `dispatch_viable`; 该标识符只出现在 Why§F6、§3.3 处方模板、Risks R-c 三处, 均是文案/prompt 层面, 不进入任何断言。claim 成立。
- **main-branch 早退分支与 PR-branch 新早退分支的交叉一致性**: 实读 `gate_check` 现有 `_verify_main_branch_exists` 调用点 (`:449-472`) 与 v3 §2.1 新增的 PR 分支核验伪码, 确认后者复用同一 `_verify_branch_exists` 核心逻辑且插入点 (`pr_status.state == "not_found"` 之后) 不会与既有 main-branch 早退冲突 (main-branch 核验发生在 path_coverage 评估之前, PR-branch 核验发生在其后, 两者不会在同一次调用里都触发之外的方式互相踩踏); `compute_verdict` 新 `not_found` 分支的插入位置 (`not_applicable` 之后、`main_in_flight_runs` 之前) 与 SC-4 的红窗设计吻合, 未见新的顺序类缺陷。

## Verdict

PASS_WITH_WARNINGS (0 Critical, 2 Major, 3 Minor) — 两条 Major 均窄、可证伪、修复成本约一句话级别, 不需要重新设计; 建议 v4 补齐后可批准进 A.2, 不建议为此再开一整轮结构性复议。

vote: REVISE
