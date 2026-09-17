---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-17T10:30:00.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# 组 2 (`scripts/completeness_gate.py` 实现) 对 proposal 忠实度审计

## 已实读文件

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md` 全文 (207 行)
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml` 全文 (1056 行, 含 `metadata` 与全部 31 个 TASK, 组 2 = TASK-008~TASK-013)
- `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md`: `:103-152` (§1.0 求值总序), `:153-171` (§1.1 S1-S4), `:172-186` (§1.1b 判定表), `:187-220` (§1.2/§1.2b 归属规则与枚举边界), `:221-269` (§1.3 三态), `:271-323` (§1.4 路由与 stdout 契约), `:325-354` (§2/§3 接线), `:453-478` (Success Criteria SC-1~SC-22 全文)
- `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` 全文 (117 行, 含 §1/§2/§3/§5)
- `aria/skills/config-loader/DEFAULTS.json` (`audit` 子集全字段)
- `aria/skills/config-loader/SKILL.md:270-352` (旧配置兼容层, 触发条件与映射规则)
- CLAUDE.md 的「多远程推送两条硬约束」与不可协商规则 #3/#6/#8/#10 (随 system prompt 提供)

## Findings

无 critical, 无 major。以下两条 minor:

| id | severity | type | category | scope | summary |
|---|---|---|---|---|---|
| `75603be0` | minor | issue | documentation | `detailed-tasks.yaml` TASK-009 (`:605`) | SC-7(e) 归入 TASK-009 但其核心断言依赖 TASK-011 的格 D 逻辑 |
| `79577c25` | minor | issue | documentation | `detailed-tasks.yaml` TASK-012 (`:661`) | S3 态 `results[].change_id` 应为 `null` 的 JSON 字段要求未在 TASK-012 校验条目里显式复述 |

### m1 — `75603be0`: SC-7(e) 的任务归属与其断言的实际承重逻辑不在同一任务

**证据**: `tasks.md` SC↔任务映射表第 5 行 `| SC-7 | 1.5 | 2.2 ((c)(d) 由 2.3) | 4.1 |` 与 `detailed-tasks.yaml:605` `'转绿: SC-5(8) / SC-7 (除 (c)(d)) / SC-17 (除 (5)) / SC-22(1)(3)'` (TASK-009/2.2) 均把 SC-7 除 (c)(d) 外的全部子项 (含 (e)) 记为由 2.2 转绿。而 SC-7(e) (proposal `:463`) 的断言是「adaptive 档 Level 1 → **不是** exit 2, 而是 `verdict=pass` exit 0 + `no_prior_checkpoints=true` (落 §1.4 **格 D**)」——`no_prior_checkpoints` 字段与格 D 路由逻辑只在 `detailed-tasks.yaml:639` (TASK-011/2.4, P5) 才实现: `'格 D (存在 adaptive:level_N) ⇒ pass, 逐 change 一行 [INFO]'`。TASK-009 (2.2) 的校验条目只覆盖 P2/S1-S4 作用域解析, 不产出 `no_prior_checkpoints` 或格路由结果。

**失败场景**: 若执行者严格按「2.2 完成即应让 SC-7(除 c,d) 转绿」的字面记录去核验 (例如在 TASK-009 收口时单独跑 `test_scope_resolution_matrix` 期望全绿), SC-7(e) 的那一分支在 TASK-011 完成前仍会是 RED, 会被误判为「TASK-009 实现有缺陷」而不是「等待 TASK-011」。

**为什么不到 major**: 整个组 2 是单一 backend-architect 在 TASK-008→013 的严格依赖链上顺序执笔 (同一 agent、同一文件), TASK-012 (2.5) 收口条件明写「至此 `python3 -B -m unittest test_completeness_gate` **全绿**」, TASK-021 (4.3) 又整套回归重跑一次；只要执行到组 2 收口, SC-7(e) 必然被两次全量测试网住, 不会被静默漏做或误判为「已完成」。真正的风险只是「归因表述不精确」, 不改变执行者最终会不会把代码写对。

**建议修法**: `detailed-tasks.yaml:605` 的 `SC-7 (除 (c)(d))` 改为 `SC-7 (除 (c)(d)(e))`, 并在 `:639` (TASK-011) 的「转绿」列表 (目前该任务无独立「转绿」小结, 只在 P5 判据条目里隐含) 追加 `SC-7(e)`, 使表述与实际承重逻辑对齐。

### m2 — `79577c25`: `results[].change_id` 在 S3 态应为 `null` 的 JSON 字段要求, TASK-012 校验条目未显式复述

**证据**: proposal `:158` (§1.1 S3): 「**`results` 里的 `change_id` 取 `null`** (R2 rework 补定义 —— 原稿只定义了 S4-bypassed 的 `results=[]`, 这一格漏了), trail 行相应渲染为 `{cp} (无 change_id)` 而非 `{cp}@{change_id}`」。proposal `:463` (SC-7 主体): 「`--no-spec` 合法 → 全部 `not_applicable/level1-no-spec` + `scope_source=no_spec` + **`change_ids == []` 且 `results` 每条 `change_id is None`**」。`detailed-tasks.yaml:661` (TASK-012/2.5) 的 trail 行校验条目只写「not_applicable 的 `[INFO]` (S3 渲染为 `(无 change_id)`)」——只复述了 **stderr 渲染** 的文本形态, 未复述 **stdout JSON `results[].change_id` 字段本身须为 `null`** 这条独立契约。

**失败场景**: 若实现者只读 TASK-012 的校验条目 (未回头核对 proposal `:158`/`:463` 原文), 有一定概率只在 stderr 渲染层做条件判断 (`if change_id is None: render "(无 change_id)"`) 而在构造 `results` 字典时仍把 `change_id` 填成某个占位字符串 (如空串 `""` 而非 Python `None`)——这会让 `json.loads(stdout)["results"][i]["change_id"] is None` 断言 (SC-7 的一部分) 判红。

**为什么不到 major**: 该字段值已由 SC-7 主体的显式断言 (`results` 每条 `change_id is None`) 锁定, 且该断言在 TASK-005 (1.5, RED 第二批) 即已写入测试 (`test_scope_resolution_matrix`), TASK-012 收口的「全绿」门槛与 TASK-021 的整体回归都会把这条 RED 网住。不是「漏做」而是「任务级校验条目复述不全, 但底层测试网未破」。

**建议修法**: `detailed-tasks.yaml:661` 补一句「S3 态 `results` 条目的 `change_id` 字段须为 `None` (非占位字符串), 与 stderr 渲染分别核验」。

## 对执笔人自报薄弱点的表态

**(a) 读前必看第 7、8 条的取值是执笔人钉定的, proposal 未定义**：可接受。逐条核对: 第 7 条 (裁定 11 把 `no_spec_unverifiable` 纳入 `allow_incomplete_checkpoints` 豁免范围) 与第 8 条 (短路运行的非判定键取值, 含 `checked_checkpoints` 的 explicit-only 规则、`[WARN] bypassed: <error_kind>` 追加行) 两条内部一致 —— 第 8 条明确把「S4 与 no_spec_unverifiable 被豁免时」并列处理, 与第 7 条的裁定同向; 与 §1.4 的 `error_kind` 9 值封闭集、`enabled_by` 6 值封闭集、R-1/R-2 归约规则均无冲突 (`no_spec_unverifiable` 的豁免发生在 P2a, 在 §1.0 求值总序上严格早于 P5 的 R-1/R-2 归约, 两者是不相交的代码路径, 不存在交互, 更谈不上矛盾)。TASK-011 (`detailed-tasks.yaml:640-643`) 对两条的落地表述与之逐字一致。判据表这类「proposal 明确留给 Phase B 钉定的取值」按 tasks.md 的一般约束「发现某格期望值确须变化 ⇒ 停下走 spec 修订」已有兜底, 不构成风险。

**(b) 组 5 发布前提偏重 (5.8 要求 aria-orchestrator 与两端完全一致; 5.2 结束后强制对齐协调 ref 会回退 `--no-push` 心跳)**：可接受, 但不在本视角深入核验范围 (组 5 属发布/收尾, 非组 2 `completeness_gate.py` 实现)。就其对组 2 的影响而言, 组 2 全程在 `--repo-path`/`--diff-repo-path` 指向 scratch/worktree 副本上开发与测试 (TASK-019/020/021 的做法段均明写 `git worktree add`), 不依赖 5.8/5.2 的发布前提, 两者无耦合。

**(c) N1/N2 仍是按行切片的文本谓词; SC-11 的 post_planning 期望收紧为 `present`; SC-6 快照自证放在活体运行 (4.4), 不进单测**：可接受。N1/N2 的 `cannot_catch` 声明 (`detailed-tasks.yaml:170`) 已明确点出「只看文本落点, 拦不住条款语义写错」并指名由 SC-16/SC-18/SC-17(5) 的运行时断言兜底 —— 这三条 SC 均落在组 2 的 TASK-010/TASK-011 职责范围内 (`Step 3 枚举源过优先级链` / `排除分支` / `SC-17(5)` 均是运行时行为断言, 非文本匹配), 兜底链条真实存在, 非自我安慰式的声明。SC-11/SC-6 与组 2 无直接耦合 (前者是组 4 的活体命令, 后者的快照分支也在组 4)。

## 风险 / 疑问

- **TASK-008 (`:584`) 的「同仓判定」在求值总序上未被 proposal `:105-116` 的 P0-P6 表格明确命名**: proposal 的总序表未列出一个独立的「两面 toplevel 相等性早期核验」阶段; `git rev-parse --show-toplevel` 归一化比较的需求来自 SC-17(2) (跨仓/同仓判定须用归一化路径而非字符串比较), 但 SC-17(2) 描述的是 `not_applicable (b)` 通道 (P6 阶段) 消费的同仓判定, 不是一个独立的早期错误分支。`detailed-tasks.yaml:584` 把它放进 2.1 (P0/P1 阶段) 并赋予「任一失败 ⇒ `git_failed` exit 2」的语义, 是任务规划者补的实现细节, 不在 proposal 字面授权范围内。核对了具体顺序 (P1 早于此步, 此步早于 P2a) 后未发现会产生错误的最终分类结果 (无论何时核验, 两个路径若不是合法 git 仓库, 最终都应归为 `git_failed`), 故未计入 finding, 仅记录供组 2 执笔人在实现时确认「同仓判定失败」与「`--repo-path`/`--diff-repo-path` 本身就不是合法路径」是否应共用同一个 `git_failed` 分支, 还是应该延后到真正需要该判定的地方 (P6 的 (b) 通道与 S2/S3 的 diff 求值) 再各自处理。
- **SC-15(5) 按裁定 1 重算的复核**: 已独立重新推导 —— 8 键 checkpoint 去掉裁定 1 追加后的 5 项排除 (`pre_merge`/`post_closure`/`mid_post_spec`/`mid_implementation`/`post_brainstorm`) 剩 `post_implementation`/`post_planning`/`post_spec` 三键 (字典序恰为 `['post_implementation', 'post_planning', 'post_spec']`); fixture 里 diff 为 0 行 (`--base`/`--anchor-base` 指向含 HEAD 的 ref) 使 `post_implementation` 的 not_applicable(b) 通道因「diff 非空」前提不成立而不触发, 落 `missing`；锚点含内联 `## Tasks` 使 `post_planning` 的 not_applicable(c) 通道因「不存在任何 A.2 产物」前提不成立而不触发, 亦落 `missing`；`post_spec` 本身无 not_applicable 通道, 目录零报告直接落 `missing`。三对全 `missing` ⇒ `verdict=fail` exit 1, `len(results) == 3`。与 `detailed-tasks.yaml:544` (TASK-006) 记录的期望值逐字一致, **裁定 1 重算正确**。

## Verdict

**0C / 0M / 2m** — Vote: **PASS**

组 2 (TASK-008~TASK-013, 对应 tasks.md 2.1-2.6) 对 proposal §1.0-§1.4 的求值总序、S1-S4 作用域解析、判定表、归属规则、枚举边界、三态与路由/stdout 契约的转译忠实度高: 22 条 Success Criteria 全部有明确的任务归属 (SC↔任务映射表与各任务「转绿」条目相互印证, 无遗漏), 裁定 1/11 的执行口径 (读前必看第 6/7/8 条) 内部一致且与 §1.1 末段、§1.4 键集、`enabled_by` 封闭集、R-1/R-2 归约规则无冲突, SC-15(5) 按裁定 1 的重算值经独立复核确认正确, 组 2 六个任务经由严格依赖链在同一 agent 内顺序执笔、对同一对文件 (`completeness_gate.py`/`test_completeness_gate.py`) 无并行写入风险, config 直读/内联缺省/旧配置兼容映射的字面引用 (`config-loader/DEFAULTS.json` 与 `SKILL.md:311-331`) 与实际源码逐字核对无误。两条 minor 发现均属「任务校验条目对承重逻辑的归因/复述不够精确」, 但已有测试套件 (TDD RED 先行 + 组 2 收口全绿 + 组 4 整体回归) 兜底, 不构成执行者会做错/做漏/卡住的风险。

## 是否足以开始 Phase B

**足以**。组 2 视角下未发现会导致 Phase B 执行者卡死、得出不可证伪结论、漏做必做项或与 SOT 矛盾的问题; 两条 minor 建议可在 B.1/B.2 执行中顺手补一句话修正, 不构成阻塞。
