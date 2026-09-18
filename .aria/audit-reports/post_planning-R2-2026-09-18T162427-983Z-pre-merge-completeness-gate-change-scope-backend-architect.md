---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-18T16:49:25.346Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md` 全文 (225 行)。
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml`: `metadata` 全段 (1–976 行, 含 `baseline_rebase`/`rulings_applied`/`test_runner`/`hard_constraints`/`owner_gates`/`rule6_note`/`new_checks`/`sc13_baseline`/`sc12_liveness`/`a2_state_runs`/`c25_five_questions`/`canonical_call`/`stage_cells`/`coord_ref_precheck`/`crlf_guard`/`commit_attribution`/`revision_log`/`v2_state_runs` 全部子键与内嵌脚本、输出); `tasks:` 段的 TASK-001~TASK-019 全文 (977–1323 行, 覆盖组 1 全部 + 组 2 全部 [TASK-008~013] + 组 3 全部)。TASK-020~031 未逐条精读 (超出本视角, 组 5/发布段)。
- `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md`: `## Why`(:23起)/`## What`§1.0(:103–119)/§1.0 硬约束段(:120–151)/§1.1(:153–170)/§1.1b(:172–186)/§1.2(:187–208)/§1.2b(:210–219)/§1.3(:221–269)/§1.4(:271–323)/§2(:325–341)/§3(:343–354)/§4(:356–369)/§5(:370–391)/Success Criteria 全部 SC-1~SC-22(:453–478)/待owner复议条目 4、5、6、7、8、9、10、11、12(:530–554)。
- 决策单 `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` 未独立通读全文 (proposal.md 内已逐条引其裁定原话并标注决策单行号, 本轮以此为准交叉核对, 未发现转述失真)。
- 源码: `aria/skills/config-loader/DEFAULTS.json` 全文; `aria/skills/config-loader/SKILL.md:305-344`(旧配置兼容层); `aria/skills/config-loader/config-example.md:380-461`(场景 A/B/C/D)。
- R1 聚合报告 `post_planning-R1-2026-09-17T100518-186Z-pre-merge-completeness-gate-change-scope-aggregated.md` 全文; R1 backend-architect 席报告同名 `-backend-architect.md`(核对第 61 行, 确认本轮 M1 不是 R1 重复项)。
- `git diff caa40c8 5d435e9 -- detailed-tasks.yaml` (v2→v2.1 逐字 diff, 独立复核证据层返修范围)。

## Findings

| id | severity | type | category | scope | 摘要 |
|---|---|---|---|---|---|
| M1 | major | issue | testing | detailed-tasks.yaml TASK-011 / 读前必看第8条 | `spec_level_undetermined` 早退 (含被 `allow_incomplete_checkpoints` 豁免降级为 `bypassed` 的分支) 时 `checked_checkpoints` 的取值靠"取已产出值"这一通用规则决定, 但该规则对这一具体错误未像 S4/`no_spec_unverifiable` 那样收窄成"仅级1 explicit 档"的确定性规则, 而是依赖未被钉死的按 pair 遍历顺序; 无任何 SC 对此字段在此状态下的取值下断言, 两个同样"字面遵守"计划的实现可给出不同值且都全绿。 |

### M1 详情

**证据**:

1. `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md:24` (读前必看第 8 条): "……`scope_source`/`change_ids`/`checked_checkpoints` 取已产出值否则 `null`/`[]`/`[]` (**S4 与 `no_spec_unverifiable` 被豁免时 `checked_checkpoints` 用 explicit-only 规则**)。" —— 括注把"explicit-only"这条确定性规则**明确限定**为 S4 与 `no_spec_unverifiable` 两种早退, `spec_level_undetermined` 被排除在外, 落回前半句的通用"取已产出值"。
2. `detailed-tasks.yaml:1189` (TASK-011 verification): "S4 与 `no_spec_unverifiable` 被豁免时, `checked_checkpoints` 只收原始 config 的 `audit.checkpoints` 自身含该键且非 off 的非排除键, 其余非判定键照 tasks.md 读前必看第 8 条" —— 与第 1 条证据完全一致地把 `spec_level_undetermined` 排除在这条确定性规则之外。
3. `proposal.md:170` (S4-bypassed 字段取值原文) 与 `proposal.md:473`(TASK-006 承接的 SC-17(5)(c) 改写) 都**只**给 S4 / `no_spec_unverifiable` 两种早退钉了具体的 `checked_checkpoints` 取值公式 (级 1 explicit 且非 off 才收, 不看 Level/adaptive)。`proposal.md:251` (`spec_level_undetermined` 本体) 与 `proposal.md:465`(SC-9(4)) 都只断言 `verdict=bypassed`/`exit 0`/stderr 文案, **未对 `checked_checkpoints` 的取值下任何断言**——本轮对 SC-9 全文逐字复核确认: SC-9 (1)(2)(3) 各自有具体字段断言, 唯独"另补第(4)路"(即 `spec_level_undetermined` 分支) 只写了 `verdict=bypassed, exit 0`。
4. 构造反例: config `{enabled:true, mode:'adaptive', checkpoints:{post_spec:'convergence'}, allow_incomplete_checkpoints:true}`, `--change-id x`, 锚点 `proposal.md` 无可解析 Level 行。裁定 1 之后非排除 checkpoint 为 `post_spec`/`post_planning`/`post_implementation` 三个。`post_spec` 走级 1 explicit (`convergence`, 非 off), 不需要 Level; `post_planning`/`post_implementation` 未显式写, 走级 2a, 需要 `Level(x)`, 解析失败 → `spec_level_undetermined`, 按 §1.0 短路语义立即终止求值 (proposal.md:118 第 1 类早退)。此刻 `checked_checkpoints` 该是什么, 完全取决于实现按什么顺序遍历三个 checkpoint: 若先处理 `post_spec` 再处理 `post_planning`/`post_implementation`, "取已产出值"给出 `['post_spec']`; 若先处理 `post_planning` (或任何未显式写的键) 就立即报错, 给出 `[]`。两个实现都完全按"读前必看第 8 条"字面行事, 都不违反计划里任何一句话, 也不会被 SC-9(4) 或 stage_cells 里任何一格判红 (TASK-011 的 `stage_cells.cells` 列表里 `SC-9.4-level-undetermined-bypassed` 只在 metadata.stage_cells 里出现一次, 其对应 subTest 按 SC-9(4) 原文只需断言 `verdict`/`exit`/stderr 文案, 不含 `checked_checkpoints`)。

**它怎么会红**: 不会红。基线 (未实现前): 无对应代码, 无从判断。目标 (两种"同样合规"的实现): 一个给 `['post_spec']`, 一个给 `[]`, 均通过现有全部 SC/stage_cells。坏实现 (例如遍历顺序随 `dict` 迭代或多线程调度而"随运行"漂移, 导致同一输入两次运行给不同值): 同样不会被任何断言拦下——这恰是本 proposal 通篇在猎杀的"两个合法实现对同一输入判决不同"模式 (`proposal.md:105` 起对求值总序的整段论证、`proposal.md:170`/`proposal.md:251` 分别给 S4/`spec_level_undetermined` 补洞的动机), 这里残留了一个同类缺口, 只是发生在一个诊断性字段 (`checked_checkpoints` 的设计目的正是"使这对为什么被查/没被查可核对", `proposal.md:251` 原句) 而非 exit code/verdict 上, 后果不致命但确是"验收判据对该字段不可证伪"。

**失败场景**: TASK-011 的实现者拿到"其余非判定键照读前必看第 8 条"这一句, 会按自己对"取已产出值"最自然的理解写代码 (多数人会写成"遍历到哪算哪"的增量式, 顺序通常取字典/集合的默认迭代序而非显式 `sorted()`)。测试套件 (`test_completeness_gate.py` 里 SC-9(4) 对应的用例) 全绿, 不会有人发现问题。日后若因重构 (例如把 checkpoint 遍历改成先处理 explicit 档再处理 adaptive 档, 或反过来) 导致该字段的值悄悄改变, 也没有任何断言会变红——这是一次静默、不可检测的行为漂移。

**建议修法**: 二选一, 成本都很低: (a) 把读前必看第 8 条括注的"explicit-only 规则"适用范围从"S4 与 `no_spec_unverifiable`"扩到"S4、`no_spec_unverifiable` 与 `spec_level_undetermined`"三者 (即：不管在哪个早退点被观测到, `checked_checkpoints` 统一只收"级 1 explicit 且非 off"的键, 不依赖遍历到哪一步), 这与 `spec_level_undetermined` 本身"解析不到就不猜"的 fail-closed 精神一致, 且不需要新增字段语义; (b) 若坚持"取已产出值"是有意为之 (例如想让用户看到"报错前已经确认了哪些"), 则必须补一条钉死遍历顺序的规则 (如"按非排除 checkpoint 名字典序逐一 resolve, 遇错即停"), 并在 SC-9(4) 或新增子格里补一条断言锁定这一具体取值。两者选一, 写进 TASK-011 verification 与对应测试用例即可, 不影响任务分解结构或工时估算。

## 对执笔人自报薄弱点的表态

**(a) `stage_cells` 的 39 格在实现前无法验证**: 可接受。抽样复核了 TASK-008~011 四个任务的全部 `stage_cells.cells` 条目, 逐条验证其判据是否真的在 P6 之前 (含五格 A–E) 终局, 或只依赖参数/常量 (尤其对 `SC-15.4-legacy-pre-merge-only` 与 SC-15(4) 的第一个子断言做了区分: 后者 `checked_checkpoints==['post_spec']` 非空, 需要走到 P6, 正确地未被列入任何早期 stage_cells, 只会在 TASK-012 的"SC 方法级全绿"里兜底)。这条自报的"实现前无法验证"是准确的自我认知, 而 TASK-007 提供的 `cell_status.py` (即 `metadata.stage_cells.code`) 本身有五态自测 (target / 格失败 / 格前置报错 / 格重复执行 / 格改名) 作为兜底, 误判会立刻显式暴露为 `not-run`/`fail`, 不会假绿。

**(b) `coord_ref_precheck`/`commit_attribution` 偏严**: 可接受。这两个机制管的是协调 ref 推送安全与提交归属, 与本视角 (组 2 脚本对 proposal 的忠实度) 不相交; 方向是 fail-closed (过严的代价是多一次停下请裁, 不是误推/误合并), 与 CLAUDE.md 多远程推送硬约束的整体基调一致。

**(c) 三态脚本第 99 行仍 `git fetch /home/dev/Aria`**: 可接受。核对 TASK-018 (`detailed-tasks.yaml:1320`) 的实际验证动作, 是直接调用 `metadata.new_checks.code` 里的 `n1`/`n2`/`n3`/`n4`/`n8` 函数对真实文件求值, 并非重跑整份 `a2_v2_checks.py`; `metadata.v2_state_runs` 只在 TASK-018 verification 里以"三态见……"的方式作为既有证据引用, 不是要求 Phase B 重新执行的步骤。故该硬编码路径不会在 Phase B 的真实执行路径上被触发, 只影响"未来审计席想独立复现这份证据"时的可移植性——这属于可以留到 Phase D 缺口 issue 里顺手记一句的低成本改进, 不构成 Phase B 阻塞项。

**(d) `own_claim_files` 描述生产用法与 fixture 自造 claim 并列可能读成矛盾**: 可接受, 但建议顺手改一句。核对 `metadata.v2_state_runs.script` 的 `n6_block`(`detailed-tasks.yaml:736-737` 注释): "本轨 claim 由 fixture 在临时仓自造, 等价于 TASK-001 在真仓读到的那一条……容器身份由 phase1_gate 自解析后回填 own_claim"——这条注释已经就地解释了两者的等价关系, 实际读代码不会误读成矛盾。但 `metadata.coord_ref_precheck.own_claim_files` 字段本身 (`detailed-tasks.yaml:559`) 只描述生产取值, 没有反向指向这条说明, 单独摘出该字段读确实会有一瞬的"这和 fixture 做的不一样"的疑惑。建议在 `own_claim_files` 字段末尾补一句"v2_state_runs 的 n6_block 用等价的自造 claim 模拟本字段, 见该处注释", 零结构改动、零风险。这一条不影响执行者的实际操作 (`own_claim_files` 只在 TASK-001 的生产调用链上被读取, fixture 走的是完全独立、不依赖它的代码路径), 故未单独计入 Findings。

## 风险 / 疑问

- `metadata.new_checks` 系列的编号 (N1/N2/N3/N4/N7/N8/N10) 跳过了 N5、N6, 而 N6/N9 又被 `v2_state_runs` 重新用于指代 `coord_ref_precheck`/`commit_attribution` 两个完全不同性质 (协调 ref 安全/提交归属, 非 completeness_gate.py 文档一致性) 的检查。核对全文未发现任何地方把 N5/N6 当成"应存在的文档检查"引用, 故不构成断言矛盾, 只是编号序列不连续、跨用途复用同一前缀, 读起来略绕。不计入 finding, 供归档前顺手清一下编号注释。
- 主控背景事实里给出的"脚本 diff 54 行/9 处"与本席独立 `git diff caa40c8 5d435e9 --numstat` 实测的 30+10=40 行/8 hunks 不完全一致 (`--unified=0` 下 39 行改动/12 hunks, 仍不是 54/9)。已确认这不影响结论本身 (改动范围确实完全落在 `metadata.v2_state_runs.script` 与 `.output` 两块, 判据代码零改动, 与背景事实的核心断言一致), 只是这个具体计数口径 (可能是主控按某种别的 diff 参数或人工数的) 未能复现, 记此存疑, 不影响本轮 verdict。

## Verdict

**PASS_WITH_WARNINGS** — 0C / 1M / 0m。**Vote: REVISE**。

## 是否足以开始 Phase B

**不足以** (按本席单独判据: 有 1 条 Major 未消)。但该 Major (`checked_checkpoints` 在 `spec_level_undetermined` 早退下的取值未钉死) 影响面窄 (仅诊断性字段的确定性, 不影响 exit code/verdict/其余 15 个键), 修法成本低 (二选一, 一句话改读前必看第 8 条括注 + TASK-011 verification 同步一句 + 可选补一条 SC-9(4) 断言), 不需要重新设计任务分解或改变组 2 的任务边界。若本轮聚合判定该项可与其他席位的 Major 一并批量吸收进下一版, 组 2 (`scripts/completeness_gate.py` 实现) 本身在其余四项视角 (承重规则覆盖、裁定 1/11 与非判定键内部一致性、写入串行化、SC-15(5) 重算、config-loader 对齐) 上均未发现缺陷, 属于全通过。
