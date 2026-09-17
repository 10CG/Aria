---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-15T18:25:52.787Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — backend-architect 审计报告

## 审计结论

### 实读文件 / 实跑命令清单

- 审计对象三份全文实读: `tasks.md`(146 行)、`detailed-tasks.yaml`(784 行, 34 TASK)、`sc11-predicate-validation.py`(123 行)。
- 依据实读: R1 聚合报告 `post_planning-R1-2026-09-15T151749-638Z-...-aggregated.md`(全文)、本席 R1 报告(全文, 复用其中未变化的结论)、`git diff 07e0a6e 0f50239 -- openspec/changes/handoff-multibranch-subdir-path-fidelity/`(1133 行, 分 4 次 offset/limit 读全, 首次因 token 上限漏读 373-744 行后已补读确认无缺口)。
- `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` — 未见改动, 本轮不复核(post_planning 不重审设计取舍)。
- 代码/文档实读全文或按需 `grep -n`/`sed -n` 核对:
  - `aria/skills/state-scanner/scripts/collectors/handoff_multibranch.py`(755 行, 全文)
  - `aria/skills/state-scanner/scripts/writers/latest_md_writer.py`(320 行, 全文)
  - `aria/skills/state-scanner/references/state-snapshot-schema.md`(1171 行, `sed -n '1057,1171p'` 精读 `tracks_multibranch` 全段)
  - `aria/skills/state-scanner/references/phase-1-collectors.md`(`sed -n '95,108p'`)
  - `aria/skills/state-scanner/references/layer-l-integration.md`(`grep -n -B2 -A2 '单 track'`)
  - `standards/conventions/session-handoff.md`(`sed -n '90,100p;168,186p'`)
  - `aria/CHANGELOG.md`(`grep -n '^## \[1.70.0\]'` + `sed -n '198,220p'`)
- 子模块 SHA 核验: `git submodule status` → aria `1cb387218935433312fde4067c276754b77686a8`(= 1cb3872, 与 metadata 声称一致), standards `8b4956242d74b24400aa8e62bca020f0233eb0f2`(= 8b49562, 一致)。
- **实跑** `python3 -B openspec/changes/handoff-multibranch-subdir-path-fidelity/sc11-predicate-validation.py`(只读, 仓库根目录, 未加参数即用默认 `aria/skills/state-scanner`) → exit code 0, 输出 19×5 矩阵与 `detailed-tasks.yaml` 的 `metadata.sc11_predicate_validation.measured_2026_09_15_at_1cb3872` 逐格核对, **完全一致**(base 全 FAIL / target 全 PASS / bad_codeonly 全 FAIL / bad_changelog_only 除 g 外全 FAIL / bad_partial 的 FAIL 集合恰为 {a2,i2,j4,j5,k,l1})。
- `grep -c 'legacy:<branch>:<filename>'` / `grep -ni 'four-level\|four levels'` / `grep -n 'dictionary-max'` 对 `handoff_multibranch.py` 全文扫描, 逐一核对 TASK-010/019/020 声称的行号是否覆盖全部出现处(见下文 finding 与核验表)。
- `est_hours` 逐任务手工求和(34 项) = 100, 与 `est_hours_total: 100` 一致; `agents` 计数(qa-engineer 14 / backend-architect 10 / knowledge-manager 10, 逐任务 `agent` 字段清点)与声明一致; `total_tasks: 34` 与任务清单计数一致。
- `grep -n $'\xef\xbf\xbd'` 确认 tasks.md / yaml 内无字面 U+FFFD 字符(exit 1, 未命中), 且 `chr(0xFFFD)` 转义写法已在三处使用。

### R1 处置落地核验

| 处置编号 | 落地与否 | 证据 |
|---|---|---|
| PP1-M1(键层级描述整类改写) | **落地, 且精确** | `handoff_multibranch.py` 内 `legacy:<branch>:<filename>` 恰 3 处(:36/:332/:494, 全部由 TASK-010 覆盖); `four-level`/`four levels` 恰 3 处(:355/:368/:429, 全部落在 TASK-020 声称的 :355/:368-399/`_dedupe_sort_key` docstring 范围内); `dictionary-max` 恰 6 处行命中(:59,:60,:95,:491,:492,:716, 全部落在 TASK-020 声称的 :58-61/:93-96/:490-492/:716-717 范围内); schema 侧 `four-level` 恰 2 处(:1124/:1134, 均由 TASK-019 覆盖, :1134 "Renderer parity" 句是 R1 新增覆盖点, 实读确认该句原文确含 "four-level sort key" 字面, 此前会被漏掉)。sc11-predicate-validation.py 的 (j4)(j5) 谓词与三态实跑证实这套覆盖对"漏改一处"有鉴别力(bad_partial 的 j5 = FAIL, 因脚本故意跳过 :491-492 一处未改)。 |
| PP1-M10(writer 契约面统一归 TASK-013) | **落地, 且精确** | TASK-020 deliverables 已不含 `latest_md_writer.py`, verification 显式写 "latest_md_writer.py 归 TASK-013, 本任务不碰"; TASK-013 deliverables 新增 "模块 docstring :30-35 / write_latest_md docstring :277-290"。实读 `latest_md_writer.py` 确认: :30-35 恰为 "Return dict schema: { ... }" 代码块(现无 `degraded_reason` 键), :277-281 恰为 docstring "Returns:" 小节, :287-290 恰为 "Scenarios:" 小节(现僅 3 支, 待补第 4 支), :124 恰为 `_render_pointer` 内唯一 `_render_pointer_unavailable` 调用行, :303 恰为 `write_latest_md` 内唯一 `_render_pointer` 调用行。行号锚点 100% 命中, 无重叠、无遗漏。 |
| PP1-M4(TASK-021/026/029 依赖补全 + 合并树回归) | **落地, 且一致** | `TASK-021.dependencies` 现含 `TASK-023, TASK-024`(v1 缺); `TASK-026.dependencies` 现含 `TASK-023`(v1 缺); `TASK-029`(现拆分为 029+034)新增 verification "合并后、推送前对合并树重跑: run_tests.py 全量 + pytest 两腿 + `metadata.sc11_baseline_predicates` 全部谓词"。 |
| PP1-M9(组 5 执行序消歧) | **落地, 且与依赖图一致** | tasks.md 组 5 标题改为 "5.3 与 5.5 互不依赖、均先于 5.1"; 核验 `TASK-025`(5.3)、`TASK-026`(5.5) 互相 dependencies 均不含对方, `TASK-027`(5.1) 的 dependencies 含两者。未加人为串行边, 符合处置声明。 |
| PP1-M13(CHANGELOG 偏移表补 v1.70.0 先例行号) | **落地, 且精确** | 实测 `grep -n '^## \[1.70.0\]'` = `:200`; `sed -n` 核对 `### Fixed`=:202、`### Added`=:209、`### Changed`=:215, 与 `metadata.baseline_rebase.shifts.changelog_md` 声称的四个行号**逐一精确命中**。 |
| Minor m1(TASK-009 前缀剥离切片支须先判前缀) | **落地, 且正确** | TASK-009 verification 现为: "…或先判 `path.startswith(_HANDOFF_TREE_PATH + "/")` 不成立即走 reporter、成立才切片 `rel = path[len(_HANDOFF_TREE_PATH) + 1:]`; 不得只切不判"。逻辑核验: `_HANDOFF_TREE_PATH="docs/handoff"`(无尾斜杠, 实读 :178 确认), 拼接后判据字符串含 "/" 可正确排除 "docs/handoffs/..." 这类共享字符串前缀但非真子目录的路径, 两支(`relative_to` 抛异常 / `startswith`+切片)均安全。 |
| Minor m2(TASK-009 行号 :240-288→:240-290) | **落地, 且精确** | 实读确认 `_list_handoff_files` 函数体恰为 :240-290(:290 = `return filenames, None`), yaml 现文本为 ":240-290", 与函数真实边界完全吻合。 |
| Minor m14(TASK-010 补 :686 调用点) | **落地, 且精确** | 实读确认 :686 恰为无 frontmatter 分支内 `fallback_date = _get_file_commit_date(...)` 调用行; TASK-010 deliverables 现文本 "…与 :683-698(含 :686 的 `_get_file_commit_date` 调用)…" 精确覆盖。 |
| m6(字面 U+FFFD → 转义) | **落地** | 全仓 grep 未命中字面 U+FFFD 字符; 三处均已改为 `chr(0xFFFD)`。 |
| m9(TASK-005 平铺基线 JSON 防重生成守卫) | **落地, 且是机制而非纸面** | `hard_constraints` 新增该文件入禁重生成清单; `TASK-021` verification 新增机械检查: "`git -C aria log --format=%H -- <平铺基线JSON>` 只有 RED 批次那一次提交, 且该提交的 diff 为空" — 是可执行的 git 断言, 不是纯措辞声明(不构成 memory `feedback_paper_fix_antipattern` 意义上的纸面修复)。 |

以上 8 项 R1 处置(本席侧重相关 + 抽样核实的 backend-architect 关切项)全部**正确落地**, 未发现"声称已改但实际未改"或"改法与处置表不符"的情况。

### Finding 1 — [Major] [risk] [implementation] [scope: TASK-033 / TASK-019 / TASK-020 (`detailed-tasks.yaml`)] — 由 v2 返工引入: **是**

TASK-033(v2 新增, `parent: "2.7"`, "组 2 收口提交")的核心断言是: 提交前 `git -C aria status` 的改动面"恰为组 2 交付物"(`handoff_multibranch.py` / `scan.py` / `latest_md_writer.py` / `test_scan_integration.py`), 这份"干净的组 2 checkpoint SHA"是 TASK-015..018(组 3, 全部 `dependencies: [TASK-033]`)做三步法反事实的唯一检出源。

证据(逐条读依赖字段, 非转述):
- `TASK-033.dependencies = [TASK-013, TASK-014]`(:401); `TASK-033.deliverables` 只列 "aria feature 分支上的实现提交" 与 `verification-ledger.md`, **不列 `handoff_multibranch.py` 等任何具体文件**(:402-404)。
- `TASK-019.dependencies = [TASK-012, TASK-013, TASK-014]`(:491); deliverables 含 `handoff_multibranch.py` 的键序描述改写点。
- `TASK-020.dependencies = [TASK-012, TASK-013, TASK-014]`(:511); deliverables 含 `handoff_multibranch.py` 的 `:58-61 / :93-96 / :355 / :368-399 / _dedupe_sort_key docstring / :490-492 / :716-717` 等多处编辑(与 TASK-033 隐含要求"干净"的**同一份文件**)。
- 全 yaml 搜索: `TASK-019`、`TASK-020` 的 `dependencies` 均不含 `TASK-033`; `TASK-033` 的 `dependencies` 也不含 `TASK-019`/`TASK-020`。两者之间**无任何依赖边、也无互斥声明**。
- yaml 文件头 :9 自述"执行序以 dependencies 为准"——即该文件把 `dependencies` 字段而非 tasks.md 的散文分组奉为执行序的唯一权威。

推演(dimension C, 实施者视角): 一旦 `TASK-012/013/014` 全部完成, `TASK-019`、`TASK-020`、`TASK-033` **同时**进入可执行集合, 彼此不互斥。若执行序按 TASK-ID 升序派发(019/020 的编号小于 033, 这是新任务追加在文件末尾的直接后果), 或按 agent 空闲情况并行派发(TASK-019/020 归 knowledge-manager、TASK-033 归 backend-architect, 而多数并行安全判断依据各任务自己声明的 `deliverables` 文件域——TASK-033 的 `deliverables` 里根本不出现 `handoff_multibranch.py`, 不会被文件域冲突检测捕捉到它与 TASK-020 共享该文件), `TASK-020` 对 `handoff_multibranch.py` 的文档编辑就会在 `TASK-033` 提交前落入同一份 aria 工作树。

照计划执行会出的错:
1. 若执行者认真核验 TASK-033 第一条 verification("改动面恰为组 2 交付物"), 会在"组 2 收口提交"卡住——计划未写明卡住后怎么处理(是把 TASK-020 的改动 `git stash`? 一并提交打破"组 2 only"的承诺? 等 TASK-020 完成后重新核验?), 造成非计划内的即兴决策。
2. 若执行者不严格核验(只顺手 `git add -A && git commit`), 会静默产出一个混入组 4 文档改动的"组 2 收口"SHA。该 SHA 之后在 `verification-ledger.md` §组 2 收口 被记成"纯代码实现提交", 与实际内容不符, 污染台账可信度; 且组 3(TASK-015..018)基于该"不纯"SHA 做的"未打补丁副本绿"基线快照, 已经不是这份计划自己定义的"组 2 only"状态。

这不是结构性不可满足(功能上不影响 SC 验收本身可满足, 因为组 3 的反事实补丁全部针对**代码逻辑**而非文档/注释, 混入的文档改动大概率不会让任何断言变义), 但属于典型的"会让执行者做错、漏做、或需要临场自行裁决"的 Major 缺陷——TASK-033 是 v2 在本轮才新增的任务, 其与既有 TASK-019/020 的交互缺口是这次返工新造出来的, 不属于 R1 已处置范围。

建议改法: 给 `TASK-019`、`TASK-020` 的 `dependencies` 追加 `TASK-033`(在现有 `[TASK-012, TASK-013, TASK-014]` 基础上), 把"组 4 文档任务须在组 2 收口提交之后开始"从 tasks.md 的散文分组变成 yaml 里机械强制的依赖边; 或者在 `TASK-033` 自身 verification 里显式加一条前置判断("TASK-019/TASK-020 尚未 claim/未落笔")并给出违反时的处理指令(例如: `git stash` 组 4 侧改动, 提交纯组 2 SHA 后再 `stash pop`)。

### Finding 2 — [Minor] [issue] [implementation] [scope: TASK-020 deliverables 行号引用] — 由 v2 返工引入: 是

`TASK-020` deliverables 新增了 v1 没有的具体行号 "`_dedupe_sort_key` docstring `:429-452`"(:513)。实读确认该函数 `def _dedupe_sort_key` 始于 :428, 其三引号 docstring 实际收尾于 :453(`"""` 闭合行), 而非 :452(:452 是 docstring 正文最后一行 "the order `tracks[]` happens to be built/passed in.")。范围少标了闭合引号所在的 1 行。

照计划执行会出的错: 几乎不会——需要编辑的目标文本("four levels"字样)在 :429, 落在给定范围内; 闭合引号行本身无需编辑。纯属引用区间精度问题, 不影响实施。

建议改法: 改为 `:429-453`。

## Verdict

**PASS_WITH_WARNINGS** — 0 Critical / 1 Major(v2 引入) / 1 Minor。

## Vote

**REVISE**(存在 1 Major)。

## 轮次记录

Round 2(backend-architect, convergence): REVISE — 0C/1M/1m; R1 处置(PP1-M1/M4/M9/M10/M13 + Minor m1/m2/m6/m9/m14)逐条实读代码与行号核验, 全部正确落地, 无"声称已改实际未改"情形; `sc11-predicate-validation.py` 实跑 exit 0, 五态输出与 yaml 声称矩阵逐格一致, 全部锚点字符串与真实 1cb3872 代码/文档逐字核对通过, 未发现假红/假绿风险; 新发现 1 处 v2 返工引入的 Major: `TASK-033`("组 2 收口提交")与 `TASK-019`/`TASK-020`(同样编辑 `handoff_multibranch.py` 的组 4 文档任务)之间缺依赖边, 依赖图允许两者乱序或并发执行, 会让 TASK-033 自身"改动面恰为组 2 交付物"的断言在非顺序执行下失效; 另有 1 处 Minor(docstring 行号范围少 1 行, 无实施影响)。
