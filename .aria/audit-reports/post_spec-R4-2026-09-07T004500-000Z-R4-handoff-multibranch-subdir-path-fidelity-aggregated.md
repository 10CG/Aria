---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-09-07T00:45:00.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
---

# post_spec 聚合审计报告 — handoff-multibranch-subdir-path-fidelity (Round 4)

本文件由汇总引擎席产出, 合并本轮 5/5 席位的结构化结论。五份单席报告原文**逐字**落盘于同目录 `…-{role}.md` (role ∈ tech-lead / backend-architect / qa-engineer / code-reviewer / knowledge-manager); 五份 frontmatter 15 字段齐全 (机械核验: 逐文件 awk 抽 frontmatter 后计 `^[a-z_]+:` = 15/15/15/15/15), **0 份需补齐**。缺席 0, `round_incomplete: false`, `skipped_agents: []`。

**合并规则 (本轮实际执行, 与 R1 / R2 / R3 聚合报告同规则, 供 Round 5 复算对齐)**:

1. 按 `{category, scope}` 匹配, 语义同、写法异的合并为一条; `found_by` 列全部提出席位, `severity` 取各席**报告值**的最高者。
2. `category` / `type` 席位间不一致时取多数标注; 平票取席位序在先者 (顺序: tech-lead → backend-architect → qa-engineer → code-reviewer → knowledge-manager)。每处不一致均在条目内注明原始标注。
3. 同 scope 的**矛盾**意见 (不是同一缺陷的不同 severity, 而是结论相反) 保留双方并标 `conflicted: true`, 汇总席**不裁决**。本轮 `conflicted` = **0** —— 逐条比对未发现「一席说成立、另一席说不成立」的对立结论; 唯一的定级差 (`5c28d58f` code-reviewer critical vs backend-architect major) 按规则 1 属 severity 差而非矛盾, 已按 SOT 取最高。
4. `scope` 语义不同则不合并 —— 即使锚在同一节 / 同一 Task。本轮实例三处: (a)「`degraded_reason` 传播路径未定义」与「§2.5 三选一裁定块的机械依据不成立」都锚在 §2.5 / Task 2.5(e), 但主张与修法不同 (前者要求指定传播路径 + 补布局 1/3 断言, 后者要求重写裁定依据), 保留两条; (b)「Task 2.0 前置门未含待复议 7」与「待复议 7 判据面比正文更宽」都锚在待复议 7, 前者是流程门缺口、后者是判据枚举不全, 保留两条; (c) `handoff_multibranch.py` 三行 docstring 与 `latest_md_writer.py` 两处 docstring 是不同文件的不同同步面, 保留两条。
5. 席位**报告正文有、结构化清单未列**的条目**不计入** `found_by`, 但在相应条目内注明, 以免 Round 5 丢失该信号。本轮共 4 处: tech-lead 正文 decisions「SC-11 机检判据的基线可证伪性」与「根因判断成立」; knowledge-manager 正文 decision「sibling probe」; 另 backend-architect 的「本轮机械核验清单」8 项、code-reviewer 的「复核记录」6 项、qa-engineer 的「本轮机械核验清单」11 项均为正文-only 的正向核验, 已归并入 decision `be109744` / `25cffd35` 内注明。
6. `finding id` = `sha256("{category}:{scope}:{severity}:{type}")[:8]`, 用 python3 实算 (34 条全部唯一, **0 碰撞**)。scope 归一为小写写法后入哈希与 keys。
7. 本轮去重前 **57** 条 (tech-lead 12 / backend-architect 12 / qa-engineer 12 / code-reviewer 9 / knowledge-manager 12), 去重后 **34** 条。
8. severity 计数**不含** decision 类 (与 R1 / R2 / R3 同口径)。

---

## 审计结论

### Critical (1)

- `5c28d58f` [critical] testing/`scan.py:186` 缺键早退打红 `test_scan_integration` 三条 (§3 / Task 2.2(a) / SC-10) — **found_by: backend-architect (major/testing), code-reviewer (critical/implementation) (2/5)**
  两席**各自独立**在自己的工作副本上按 §3 处方实改 (`rel_path = t.get("rel_path")` + `if not rel_path: continue`, `proposal.md:125` 明令「**不得**照抄 §2.5 的兜底」), 取到**同一组三条转红**: `TestSnapshotSelfConsistencyAC5::test_contradiction_is_reported` / `::test_unevaluable_track_is_recorded_not_swallowed` / `::test_detection_uses_enforced_set_not_hardcoded_origin`。根因一致: 夹具 `HEALTHY_TRACKS` (`tests/test_scan_integration.py:164-166`) 只有 `track_id` / `filename` / `branch` 三键、无 `rel_path` ⇒ 每一行都被早退跳过 ⇒ `errs` 由 1 变 0 (code-reviewer 记下 `AssertionError: 0 != 1` @ `test_scan_integration.py:270`; backend-architect 记下基线 `Ran 11 … OK` → 改后 `FAILED (failures=3)`)。
  ⇒ 三条 spec 内文本互斥: (1) §3 自述「写 `.get()` 则**照绿**但测不出拼进命令行的是哪个字段」(`proposal.md:125`) 经实跑为假 —— 「照绿」只在「不早退、把 `None` 拼进路径」这一被 Task 2.2(a) 明令禁止的写法下成立; (2) SC-10 (`:304`) 把该模块以「回归面身份 …… 只保证不被打红」纳入点名集; (3) Task 4.3 (`:266`) 要求「既有测试全绿」。夹具补 `rel_path` 这一动作**全文无任务承接**。
  code-reviewer 另指: 不闭合则 Phase B 只剩三条路 —— 改夹具 (未登记、未授权) / 加 §3 明令禁止的 `or filename` 兜底 / 削断言, 第三条正是本文多处引用的失效模式; 并判其与 R2 判 critical 的 `6f8fa9f7`「既有夹具立刻翻红」**同型**。
  *severity 分歧注 (汇总席不裁决, 按规则 1 机械取最高)*: backend-architect 报 major (其 rationale 逐字写「无『方案错误』『破坏生产消费方』『SC 恒绿假绿』三类 critical」), code-reviewer 报 critical (「处方与验收判据互斥」)。按 `report-storage.md §Verdict 计算` 的 SOT 与合并规则 1, 取 critical ⇒ 本轮 verdict = FAIL。**该定级差本身建议交 owner / R5 复议** —— 它是本轮 verdict 从 PASS_WITH_WARNINGS 翻到 FAIL 的唯一支点 (其余四席自报 verdict 均为 PASS_WITH_WARNINGS)。
  *category 分歧注*: backend-architect testing、code-reviewer implementation ⇒ 1:1 平票, 按规则 2 取席位序在先者 = testing。
  *修法 (两席一致, 均属定点 rework)*: Task 2.2 明写「同批给 `HEALTHY_TRACKS` 补 `rel_path`」(与 Task 2.1(ii) 改四处 mock 同型), 并删掉 §3 那句已被证伪的「照绿」断言。

### Major (10)

- `5513534d` [major] architecture/`scan.py` AC-5 上报字段 `filename` 的语义归属 (§3 / Task 2.2(a) / §5) — **found_by: tech-lead (issue/major/architecture), code-reviewer (risk/minor/implementation) (2/5)**
  §3 用整段规定 `:186` 改读 `rel_path` 且不做缺键兜底, 却未说**同一函数**上报的 `"filename"` 该装 basename 还是相对路径 —— `scan.py:180` 的那个局部变量同时喂 `:186` 的命令行与 `:193` (`inconclusive[].filename`) / `:204`(tech-lead 记 `:209`, `offenders[].filename`)。两个 dict 经 `:269` / `:283` 进快照顶层 `errors[].tracks[]`, 是机读输出 (tech-lead 另核: schema `:1141-1147` 的 `errors[]` 形状只列三键, 根本没记 `tracks` 子键)。按 Task 2.2(a)「沿用 `:180-182` 既有早退形态、改成读 `rel_path` 后同形早退」的字面写法, 最自然的实现是重指那个局部变量 ⇒ 一个机读字段的取值语义静默改变, 而 A′ 的立意恰是**不动既有 `filename` 语义**。§5 消费方表、§6 同步清单、CHANGELOG、SC 集四处零登记 (对照: `legacy_count` 语义收窄与 `identity_advisories` 加法面都登记了)。code-reviewer 另指 `test_scan_integration.py:272` 正钉该值, 夹具补键时若取相对路径写法, 该断言需同批更新。
  *severity / type / category 分歧注*: tech-lead issue/major/architecture、code-reviewer risk/minor/implementation ⇒ severity 取最高 major; type 与 category 各 1:1 平票, 按规则 2 取席位序在先者 = issue / architecture。

- `ead9ac24` [major] architecture/`degraded_reason` 传播路径未定义 + 布局 1/3 无断言 (§2.5 / Task 2.5(e) / SC-15) — **found_by: tech-lead, backend-architect (2/5)**
  守卫落在 `_render_pointer` (`latest_md_writer.py:110-148`, 返回 `str`), 而 `degraded_reason` 要出现在 `write_latest_md` (`:298-320`) 的返回 dict; 两者如何连接 (改 `_render_pointer` 的返回形状, 还是在 `write_latest_md` 里**重算**同一谓词) 全文未指定 —— tech-lead 实测全文 10 处提 `degraded_reason` 无一处说明如何回传。最省事实现 = 重算 `rel == filename`, 于是同一判据在两个函数里各写一遍靠巧合一致, **正是本 spec §3 自己点名的根因族**(「两处独立字面量, 今天靠巧合一致」)。两席同指: 本 spec 对同类选择 (Task 2.1 的 (i)/(ii)、Task 2.2 的缺键口径) 都坚持「选型后果不能对实施者不可见」, 唯此处没给。
  第二半 (backend-architect): SC-15 **只在布局 2 断言该键**, 布局 1 (a)(b)(c) 与布局 3 (g) 都不断言 `degraded_reason is None`, 三条反事实也无一针对它 ⇒ 「正文写真指针、机读键报 `target_in_subdir`」这种镜像谎言全绿通过 —— 正是 R3 `92565b30` 要根除的形态; SC-15(h) 只断返回值, 对两种实现同样绿。
  *修法 (两席一致)*: Task 2.5(e) 明写传播路径 (backend-architect 推荐 `_render_pointer` 返回 `(content, reason)`), 并给布局 1 / 3 各加一条 `degraded_reason is None` 断言 + 一条反事实。

- `5105b00e` [major] architecture/§2.5 `action` 三选一裁定块的机械依据不成立 (`test_p1_layer_h:264`) — **found_by: qa-engineer (1/5)**
  §2.5 就地裁定「保留 `action` 三值枚举、改为新增 `degraded_reason`」, 其唯一机械证据是「改枚举会打红 `tests/test_p1_layer_h.py:264` 的 `assertEqual(result["action"], "pointer")`」—— 该断言经实读为假。`:264` 的夹具是 `_active_track("my-spec", "2026-05-20-my-spec.md")` (`:230-240`, 八字段、**无** `rel_path`、filename 是顶层名), 按 §2.5 强制的缺键兜底 `rel = rel_path or filename` 判为平铺 ⇒ 走真指针支 ⇒ `action` 仍是 `"pointer"`, 新增第四个枚举值**根本触不到它**; 全模块 8 处 `_active_track(` 调用与全文件均无子目录 / `rel_path` 夹具 (grep 实证)。另一半理由 (打破 `phase-1-collectors.md:102` 的公开契约) 对「加 `degraded_reason`」同样成立 —— 本文自己已把 `:102` 排进 Task 4.2 的同步面。⇒ 「保留说谎的 `action`」这一支目前缺可核实的机械支撑, 而本文自述其反面 (§2.5「把无声失败原样复制到写侧」) 恰恰指向改枚举。
  *与 `ead9ac24` 的关系 (规则 4 保留两条)*: 两条同锚 §2.5 / Task 2.5(e), 但本条主张「裁定依据须重写」、`ead9ac24` 主张「传播路径与负向断言须补」, 修法互不覆盖; R5 若判为同一缺陷可自行并轨。
  *修法 (qa-engineer)*: 结论可保留, 但须换成真依据 (例: 老消费方只 switch `action` 时的向后兼容代价), 或把该取舍并入 §待 owner 复议。

- `7ae33f13` [major] testing/`rel_path` / `unreadable_count`「恒存在」在 legacy 行与成功路径无 SC 钉住 (SC-13 / SC-16) — **found_by: backend-architect, qa-engineer, code-reviewer (3/5)**
  §7 与 §6.5 CHANGELOG `### Added` 把两个字段声明为**恒存在**, 但 §4 删掉 git-show 失败行之后 TrackEntry 仍有**两个**构造点 —— frontmatter 分支 (`handoff_multibranch.py:663-676`) 与无 frontmatter 的 legacy 分支 (`:683-700`), 三席行号写法略异 (`:665-676`/`:687-698` · `:683-700` · `:663-674`/`:686-697`), 指向同两处。SC 只覆盖前者: SC-1 / SC-8 后半走 frontmatter 分支, SC-13 造了两份无 frontmatter 文件却只断言 `track_id` 与 `updated_at`, SC-16 是「`tracks[]` **每一行**」的**全称谓词而夹具组成未钉死** ⇒ 夹具若只放带 frontmatter 的文件即**真空满足** (memory `feedback_universal_predicate_vacuous_truth_on_empty_set` 同型)。
  code-reviewer 另指本文在 SC-15 处刚立过「夹具组成是判据的一部分, 不得按字面取最小夹具」(`:310`), SC-16 (`:311`) 自己却没执行这条。qa-engineer 另加一层: 成功路径上 `unreadable_count == 0` 也无任何断言 (SC-14 只覆盖 fail-soft 早退)。
  后果三席一致: 叠加 §3 的无兜底早退 (即 `5c28d58f` 的处方), legacy 行漏填 `rel_path` 时 `scan.py:180-186` 的 AC-5 会**静默跳过全部 legacy 行**, 零告警 —— 与 §Why F1 认定的失效形态同型、与 §Impact 声称修掉的 F1 (`proposal.md:239`) 原样复现, 只是换了人群。对照 SC-14 为 `unreadable_count` 的「恒存在」专设错误路径断言, 此处的不对称是缺口。
  *修法 (三席一致)*: SC-16 夹具明写「至少一份带 frontmatter + 一份不带」并断言其 `rel_path` 存在; SC-13 追加 `rel_path` 断言; 任一正常路径 SC 追加 `"unreadable_count" in data and data["unreadable_count"] == 0`。

- `177d72e6` [major] testing/SC-3 baseline-red 资格随 `core.quotePath` 漂移 (§Why F2 / Task 1.2) — **found_by: qa-engineer (1/5)**
  F2 的「引号 + 八进制转义 ⇒ 静默漏扫」不是 `git ls-tree --name-only` 的无条件属性, 而是 `core.quotePath` 的默认值。qa-engineer 在隔离配置的临时仓 (git 2.39.5) 实测: 默认输出 `"docs/handoff/2026-\346\265\213\350\257\225-\344\272\244\346\216\245.md"`, 加 `-c core.quotePath=false` 输出原样 `docs/handoff/2026-测试-交接.md`。而生产侧 `_noninteractive_git_env` (`_common.py:317-346`) 只注入 `LC_ALL` / `GIT_TERMINAL_PROMPT` / `GIT_SSH_COMMAND`, **继承采用方 git 配置** ⇒ (a) 把 `core.quotePath=false` 的采用方 (中文 / 日文环境常见, 本仓工作语言即中文) 今天根本不触发 F2; (b) SC-3 的 baseline-red 资格随宿主配置漂移 —— 在这类机器上 SC-3 在 `301641b` 上就是绿的, Task 1.2 的「五族全红」不可满足, 实施者最可能的反应是削断言。姊妹夹具 `_GIT_ENV` (`test_handoff_multibranch_collision_dedupe.py:174-183`) 已 pin `GIT_CONFIG_GLOBAL=/dev/null` / `GIT_CONFIG_SYSTEM=/dev/null`, 但本文两处 (SC-4 / SC-13) 把它描述成「只 pin 姓名 / 邮箱」, 正好掩盖了这条载重隔离。SC-3 是 rule6_note 十一条 substitute 实体之一, 失去鉴别力即等于 Rule #6 的替代面缺一角。
  *修法 (qa-engineer)*: SC-3 明写「新夹具必须复用 `_GIT_ENV` 式配置隔离」, 并把 §Why F2 与 CHANGELOG `### Fixed` 的 F2 条改成条件式表述 (`-z` 使行为**不再依赖** `core.quotePath` —— 这才是修复的准确措辞)。

- `31bc3c6a` [major] testing/§7 / Task 4.3 禁重生成冻结语料的理由为假 (freeze_corpus 八字段投影) — **found_by: qa-engineer (1/5)**
  「用改后代码重生成冻结语料 ⇒ `test_collision_frozen_corpus.py:51` / `:112` 立刻转红」经实读为假。仓内**受认可的**重采样路径是 `tests/fixtures/freeze_corpus.py` (docstring `:17-21` 逐字写「Re-running the script on a newer dump is how a future spec refreshes the corpus」), 而 `trim()` (`:32-37`) 用 `{k: r.get(k, …) for k in FIELDS}` 把每行投影成**恰好那八个键**, `main()` (`:48-53`) 回写 `"fields": list(FIELDS)` ⇒ 新增 `rel_path` 根本进不了产物, `:51` / `:112` 重生成后**仍然绿**。真正会红的是 `:111` 的 `assertEqual(len(self.rows), 996)` 与依赖该 996 行内容的归因断言。后果: 禁令本身正确、理由却站不住, 实施者一核实就会认定禁令无据而放手重生成, 从而打红 `:111` 一族 —— memory `feedback_never_write_unverified_impossibility_claims` 形态。
  *修法 (qa-engineer)*: 把 §7 / Task 4.3 的证据换成 `:111` 行数钉死 + `freeze_corpus.trim` 的八字段投影事实 (后者恰恰说明「新增字段不构成重采样理由」)。

- `b3e5ea8d` [major] architecture/Task 2.0 前置门未含待复议 7 (Level 裁定无任务承接) — **found_by: tech-lead (1/5)**
  Task 2.0 写「前置门 — 已解除」并逐一枚举「待复议 1 / 3 / 4 / 5 / 6 均取推荐默认推进」, 但 R3 新增的**待复议 7 (Level 2 vs Level 3) 不在枚举内**, 而它恰是全文唯一自述「无推荐默认, 执笔者不自裁」的一条。它的裁定结果决定 Phase B **之前**是否必须先补 A.2 `tasks.md` + A.3 `detailed-tasks.yaml` + post_planning 收敛审计 (tech-lead 实测目录内现仅 `proposal.md` 一个文件)。Task 5.1 为待复议 6 (版本级别) 明装了「裁定后才动手」的前置门, 同等级的待复议 7 却无任何任务挂钩 ⇒ 按现文可直接进 Phase B, 若 owner 裁 Level 3 则整个 A.2 / A.3 要回补。
  *与 `b28c0da7` 的关系 (规则 4 保留两条)*: 本条是「流程门缺一个挂钩」, `b28c0da7` 是「该复议项援引的判据枚举不全」, 主张与修法不同。
  *修法 (tech-lead)*: 给待复议 7 装与待复议 6 同级的前置门 (裁定后才进 Phase B)。**须 owner 裁**, 审计席不代裁 (Rule #10)。

- `ab615189` [major] documentation/rule6_note 首条前提句「无 references 文本变动」被自身任务表证伪 — **found_by: tech-lead (minor), knowledge-manager (major) (2/5)**
  rule6_note 的「变更性质 (不变的部分)」逐字写「**无** `description` 变动, **无** SKILL.md / references 的文本变动」。knowledge-manager 指出它与同句前半「输出 schema 文档」**同句自相矛盾** (「输出 schema 文档」就是 `references/state-snapshot-schema.md`), 并被 R3 rework 新增的任务进一步证伪: Task 4.1 (`:264`) 改 `references/state-snapshot-schema.md`; Task 2.5(e) (`:260`) 改 `references/phase-1-collectors.md:102`; Task 4.4 (`:267`) 改 `references/layer-l-integration.md:103`; Task 4.5 (`:268`) 视复核结果可能改 `references/rules/advanced-rules.md` 与 `RECOMMENDATION_RULES.md`。tech-lead 独立列出前两项同结论。
  knowledge-manager 另把它接到 Rule #6 SOT 的**判据表选行**上: `references/rules/*` 是 SOT 明列的**处方性**类 (`standards/conventions/skill-benchmark-exemption.md:20`「`references/rules/*` 的 dispatch 表、判定规则 …… 与 SKILL.md 正文同性质」), 一旦 Task 4.5 落编辑, 正确落行是判据表**第二行「处方性 · 运行时指令面 ⇒ 照跑 AB, 零裁量」**(`:29`) 而非现写的**第四行「拿不准 ⇒ 照跑」**(`:31`)。**照跑这一处置结论两席一致不变** (两行同去处), 但 SOT §4 强制留痕的 rule6_note 载的是一条假前提, 后续复议 / 重跑 benchmark 会据它误判处方面半径。
  *severity 分歧注*: tech-lead minor、knowledge-manager major ⇒ 按规则 1 取最高 major。
  *修法 (两席一致)*: 订正前提句为「有 references 文本变动 (逐条列出四处)」并把判据表选行改到第二行。

- `5b252465` [major] documentation/`latest_md_writer` 两处函数 docstring 未入同步清单 (`:111-114` / `:152`) — **found_by: knowledge-manager (1/5)**
  §2.5 守卫给 `_render_pointer` 增加第二个降级原因 (`target_in_subdir`), 但两处自述「唯一原因 = 缺 filename」的 docstring 既不在 §6 同步清单也无任何 SC —— `latest_md_writer.py:111-114` 逐字「Falls back to a "(pointer 不可用)" banner when the filename cannot be determined from the track dict (edge case: legacy track missing filename)」, `:152` 逐字「Fallback when single active track has no filename.」(实读 1.71.1 副本)。清单现只列 `:32` / `:279` / `:287-290` (action 契约, R3 `92565b30`) 与 `:159` / `:164` (正文文案与硬编码原因, R3 `3dd75e12` / Task 2.5(c)(f))。落地后这两句在**被改函数头上**直接为假, 与 R3 判 major 的 `ebaad4a5` (`:332` `_make_legacy_track_id` 自身 docstring)、`b5a94a9c` (docstring 块归位) 同型; 本 spec 对同类漏改 (`:20` / `:177` / `:313`) 一律逐条点名, 唯独漏此两处 ⇒ 属缺口而非取舍 (Rule #3)。
  *与 `69e6a1a8` 的关系 (规则 4 保留两条)*: 本条是 `latest_md_writer.py` 的两处, `69e6a1a8` 是 `handoff_multibranch.py` 的三处, 不同文件不同同步面。
  *修法 (knowledge-manager)*: 把 `:111-114` / `:152` 纳入 §6.2 同步清单与 Task 2.5 / 4.2, 并加一条 SC-11 grep。

- `23b414c9` [major] architecture/`n_active` 是第五个被改动却未登记的量 (§5 / Impact / `write_latest_md` 三分派) — **found_by: tech-lead (1/5)**
  §5 与 Impact 登记了 `exists` / `len(tracks)` / `legacy_count` / `collision.kind` / `identity_advisories` 五个量, 唯独漏了 `n_active`。路径修好后子目录件从 legacy 变真 track, 被 `_get_active_tracks` (`latest_md_writer.py:89-94`) 收进 ⇒ `write_latest_md:298-310` 的 **0 / 1 / ≥2 三分派**可从 1 翻到 ≥2 ⇒ 走 `_render_banner` (`:172-223`, 输出**不含** `**Latest**: [` 行) ⇒ `handoff.py:263-266` 的 `_LATEST_POINTER_RE` 不匹配 ⇒ `latest_source` 静默退回 `"mtime"` 且零 soft_error。§2.5 的写侧守卫只活在 `n_active == 1` 这一支, 覆盖不到; SC-15 三个布局最高只到 1 active。
  可达性非假想 (tech-lead 实测): schema `:1118` 逐字记载历史行的 frontmatter「frozen at write time (`status: active`) and never rewritten」, 本仓 `docs/handoff/` 190 份交接里 **22 份 `status: active`** —— 归档进子目录的采用方 (即 #195 报告方形态) 正是这个人群。tech-lead 另点出反讽: Task 4.4 要改的 `standards/conventions/session-handoff.md:172-173` 恰恰就是按「1 active track / ≥2 active tracks」分档的那张表, 而本 spec 只从 `n_active == 1` 这一格里往外看。
  *type 注*: tech-lead 报为 risk/major; 汇总席保留原 type。
  *修法 (tech-lead)*: 把 `n_active` 登记进 §5 / Impact / CHANGELOG, 并给 SC-15 补一个 `n_active ≥ 2` 的布局或明写该情形的处置。

### Minor (14)

- `7b7aed03` [minor] documentation/dedupe 论据句 legacy 公式行号 `:495-496` 实为 `:494` — **found_by: tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager (5/5 — 本轮唯一全席条目)**
  `legacy:<branch>:<filename>` 字面在 `handoff_multibranch.py` 命中 3 次: `:36` / `:332` / **`:494`** (加 `state-snapshot-schema.md:1104` 合计 4 处); 提案五处 (`proposal.md:117` / `:206` / `:257` / `:265` / `:305`) 均写 `:495-496`, 而那两行是后半句「so two legacy rows can never share a dedupe key with each other or with a / real track, and every legacy row's `owner_container` is `"unknown"`」, **不含**该字面。三席另指: R3 rework 记录专门把审计席给的 `:493-496`「勘正」成 `:495-496` —— **勘正动作自身出错**, 方向反了 (memory `feedback_author_and_verifier_must_differ_for_corrections` 形态, 建议由非 R3 执笔者复核)。SC-11(i) 走 grep 计数故不致假绿, 属导航性错误, 但 Task 4.2 会把实施者指到错行。
  *qa-engineer 附加*: SC-11(i) 写的 `grep -c '…' fileA fileB` **合计为 0** —— `grep -c` 多文件时按文件分行输出, 需改成 `! grep -q` 或显式求和。

- `34731677` [minor] architecture/§5 消费方枚举漏 `phase-d-closer/SKILL.md:218` — **found_by: backend-architect (architecture), code-reviewer (documentation) (2/5)**
  两席各自全树 grep: state-scanner 之外读 `tracks_multibranch` 的仅 phase-d-closer 三文件, §5 登记了 `handoff-mechanics.md:116-121` 与 `fetch_gate.py:175-188`, 漏 `SKILL.md:218`「子步骤 2 Pointer 更新 (conditional by `snapshot.tracks_multibranch` multi-track detection)」。它与已登记的 `advanced-rules.md` / `RECOMMENDATION_RULES.md` 同类 (不改文本、输入值变), 按本文自身的「同一判定的两份登记面须一并复核措辞」口径应入表 (Task 4.5 的复核清单亦应含它)。backend-architect 另核: 它**不改变** Rule #6 的 AB 范围结论 (本 spec 不改其文本), rule6_note 说的「SKILL.md 三处」限于 state-scanner 的 SKILL.md, 该限定属实。
  *category 分歧注*: backend-architect architecture、code-reviewer documentation ⇒ 1:1 平票取席位序在先者 = architecture。

- `ce719781` [minor] documentation/Task 1.2 五族 vs 四族计数自相矛盾 + 十一实体红态无承接 — **found_by: backend-architect (testing), qa-engineer (documentation), knowledge-manager (documentation) (3/5)**
  同一 bullet 内: 前半列出五族并写「**这五族**对 `301641b` 全红」, 粗体警示仍写「**⚠️「全红」只限定到上列四族**」, 该警示自己的括注又写「(v4 原写四族也已随 SC-17 更新为五族)」—— R3 落地 `17f270f5` 时的半改。qa-engineer 指出后果: 照后半读会把 **SC-17 排除出红测门**, 而 SC-17 恰是唯一覆盖闸门输入 (`collision.kind`) 的 baseline-failing 实体。
  *backend-architect 另加一层 (规则 5 内注, 勿在 R5 丢失)*: rule6_note 列的十一条 baseline-failing 实体中, **SC-6 / SC-9 / SC-14 / SC-16 与 SC-4 后半 / SC-8 后半**既不在「必须全红的五族」也不在「本就为绿的例外清单」, 其红态验收无人承接 —— 而 R3 `120e1171` 引入例外清单的初衷正是消除这类灰区。
  *category 分歧注*: backend-architect testing、qa-engineer / knowledge-manager documentation ⇒ 取多数 documentation。

- `0328fdb3` [minor] documentation/SC-11 未覆盖 R3 新增 references 与 writer 契约面 — **found_by: backend-architect, knowledge-manager (2/5)**
  SC-11 (a)-(j) 把 schema 字段表、fail-soft 形状、Change history、collector 两个 docstring 块、新 soft_error kind、standards 第三态全上了 grep, 唯独 R3 新增的契约面无机检判据: backend-architect 列 `latest_md_writer.py:32` / `:279` / `:287-290` 与 `references/phase-1-collectors.md:102` 四处 `action` 契约面; knowledge-manager 列 `phase-1-collectors.md:102` (实读逐字 `Return dict: {action: "pointer"|"banner"|"skipped", path: str, content_lines: int}`) 与 `references/layer-l-integration.md:103`, 并指 SC-11(h) 只点名 `standards/conventions/session-handoff.md`。并集为五处, 全部只靠任务勾选兜底 —— 与 R2 `7cba5aa4` / R3 `cc313a28` 判「只靠尾句兜底不算判据」同型缺口。

- `726588e5` [minor] documentation/§6.1 Change history「每次变更加一行」既有口径陈述过强 — **found_by: code-reviewer, knowledge-manager (2/5)**
  两席各自实证: v1.70.0 的同 collector 家族 schema 变更 (code-reviewer 定位 commit `f2e4231`, 加 14 行含 `:1091` `identity_advisories`; knowledge-manager 另记 dedupe 键语义改写 `:1120,:1122,:1128`) **未触碰** `## Change history`, 表末行仍是 **2026-07-19** (`:1156-1168`, 文件共 1168 行)。⇒ 「该表既有口径是**每次** schema 变更加一行」不成立。SC-11(g) 要求本 spec 补一行本身正确且可证伪, 但论据句须改写为「表**应**每次登记, 上周期漏登记」。

- `69e6a1a8` [minor] documentation/`handoff_multibranch.py:243` / `:298` / `:315` 三行同族 docstring 未登记 — **found_by: tech-lead (1/5)**
  `:243`「Uses ``git ls-tree -r --name-only origin/<branch> -- docs/handoff/``」在加 `-z` 后失真 (而 `-z` 正是 F2 的载重机制); `:298`「``git show origin/<branch>:docs/handoff/<filename>``」与 `:315`「``git log -1 --format=%aI origin/<branch> -- docs/handoff/<filename>``」在入参改名 `rel_path` 后同样过时。后两者与**已登记**的 `:332` 是同一理由 (§What.2 原话:「就在 Task 2.2 要改的函数头上, 改代码不改它等于当场留一条自相矛盾的注释」), 本 spec 只对三个姊妹函数中的一个施加了这条标准。

- `dd55dac3` [minor] architecture/`unreadable_count` 外延未定 (前缀守卫丢弃行 / 不可解码 UTF-8) — **found_by: tech-lead (1/5)**
  这个新机读契约字段 (CHANGELOG `### Added`、schema 常驻) 的计数范围只被 SC-5 钉住「git show 失败」一例, SC-14 钉早退为 0。前缀守卫 (`handoff_multibranch_unexpected_path_prefix`) 丢弃的行是否计入无定论; 不可解码 UTF-8 名更被 §7 末条与 Impact.Risk 末条给了两个**互斥**选项 (「计入 unreadable_count」vs「显式跳过, 对齐 `handoff.py:319-322` 先例」) 且未择一 ⇒ 新契约的语义会由实施者随手决定, 再由 Task 4.1 写进 schema SOT。
  *type 注*: tech-lead 报 risk/minor, 汇总席保留原 type。

- `137c99e7` [minor] testing/SC-10 可执行命令仍只列五模块并钉死 102 — **found_by: qa-engineer (1/5)**
  SC-10 断言格开头的可执行命令仍只列原五模块并钉死 `Ran 102 tests … OK`, 同格结论却是「点名集共 9 模块 …… 须由 Phase B 重取总数」。验收判据的可执行半与其点名集不一致, 照命令跑只验 9 分之 5。qa-engineer 实测供参考: 原五模块 102 OK, 新四模块 65 OK, 合 167。建议命令行直接列全 9 模块, 把「总数由 Phase B 抄录」的口径留在括注里。

- `b702d253` [minor] testing/§What.1 空段丢弃无 SC 覆盖 (SC-9) — **found_by: qa-engineer (1/5)**
  `git ls-tree -r --name-only -z` 的输出以 NUL **结尾**, qa-engineer 实测 `stdout.split("\0")` 必产生一个尾随空段 (`['…2026-测试-交接.md', '…a.md', '…archive/b.md', '']`)。§What.1 (`:105,107`) 把「空段丢弃」写成要求, 但 SC 集无一条覆盖: SC-9 只断言坏前缀行产生指定 kind 且同分支其它文件照常入 `tracks[]`, SC-2 / SC-16 走八字段投影, SC-12a 的逐字段 diff 也看不到。若实现把空段送进新前缀守卫, 每个分支多一条 `handoff_multibranch_unexpected_path_prefix`, 恰是本 spec 立意要消除的告警噪声; 目前唯一 (偶然、手工) 的网是 SC-12a 的「exit code 与改前相同」。建议 SC-9 加第三条断言: 平铺临时仓上该 kind 计数为 0。
  *与 backend-architect 核验的关系*: backend-architect 的 hermetic 探针同样测到「末段空串」并另证 pathspec `-- docs/handoff` **不匹配** `docs/handoff-archive/c.md` (⇒ 前缀守卫无兄弟目录误剥面), 但其结构化清单未把空段列为 issue, 按规则 5 不计入 found_by。

- `05fa7d76` [minor] testing/SC-10 基线取样时点与 Layer H 日历失效相容性 — **found_by: qa-engineer (1/5)**
  SC-10 写死「基线口径 = 真仓 checkout **零失败**, 出现任何失败都要逐条归因, 不得预先豁免」, 同格又给出第三类归因路径 (日历失效, 2026-09-09 起 2 条自动转红)。两者相容性取决于**基线在哪天取**: 早于 09-09 取则基线零失败; 晚于 09-09 取则基线自身就带 2 条红, 「零失败」判据不可满足。qa-engineer 复核该日历机制成立 (夹具 `test_handoff_multibranch_collision_dedupe.py:380-382` 三行日期 2026-08-02/08-10/08-15, 调用处 `:386` 未 pin `now`, `lib/collision.py:222-241` 按 `lib/constants.py:88` 的 30 天窗丢行; 08-10 行在 2026-09-09 出窗); code-reviewer 的日历探针独立复现「恰 2 条转红且与 `:304` 所列名字逐字相同」。建议 SC-10 明写「基线须在 2026-09-09 之前取, 否则先按 §待复议 8 的裁定处置再取基线」。
  *type 注*: qa-engineer 报 risk/minor, 保留原 type。

- `c454dbe2` [minor] documentation/`handoff-mechanics.md` D.3 决策表行号漂移 (`:116-121` / Single-track 行) — **found_by: code-reviewer (1/5)**
  实读 `phase-d-closer/references/handoff-mechanics.md`: `:116` 判定逻辑句 / `:118-119` 表头 / **`:120-122` 三行判据**。`proposal.md:184` / `:267` / `:348` 写「`:116-121` 的 3 行决策表」(截掉第 3 行), `:218` 更把 Single-track 行写成 `:116` (实为 `:120`)。`:114-124` 的引用则正确 (证据: `grep -n 'Single-track\|Multi-track'` = 120/121/122)。

- `585e210a` [minor] documentation/决策单勘正的复议入口不完整 (头部 `:19` vs §待复议 2 第 (5) 问) — **found_by: knowledge-manager (1/5)**
  头部 `334e62dc` 块称三处勘正「随本 spec 一并请 owner 追认 (§待复议 2 第 (5) 问)」, 但实读该项只写「字段名 `rel_path` 追认」; 另两条**载重**勘正 —— (a) 守卫判据不得照决策单第 2 条写 `relpath != filename`; (b) SC-15 断言须换成顶层留非-active 件的夹具 —— 未在待复议清单出现。owner 只读复议清单即会漏签这两条 (对照 `.aria/decisions/2026-09-07-…-pointer-guard.md:56-61`)。
  *与 R3 `334e62dc` 的关系*: R3 那条要求对决策单 §落地约束补 neutralize (已落地), 本条指出**复议入口**这一半没跟上 —— 是同一动作的下游而非重开。

- `b28c0da7` [minor] architecture/待复议 7 判据面比正文更宽 (另命中「需要 API 契约变更」) — **found_by: backend-architect (1/5)**
  `spec-drafter/LEVEL_GUIDE.md:156-162` 的跨模块条件是「满足任一」, 本 spec 命中的不止「影响多个子模块」—— 新增 `rel_path` / `unreadable_count` / `degraded_reason` 三个机读契约字段 + `write_latest_md` 返回形状变化同时命中「需要 API 契约变更」。待复议 7 只援引前者, 建议把第二条判据一并列出交 owner, 免得「Task 4.4 判 deferred ⇒ 跨模块不成立 ⇒ 维持 Level 2」这条出路被误当成必然成立。
  *type 注*: backend-architect 报 risk/minor, 保留原 type。

- `a078de50` [minor] documentation/§待 owner 复议 8 条积压与无人值守 — **found_by: knowledge-manager (1/5)**
  8 条待 owner 复议中 R3 已定 4 条「须 owner 或 R4 拍板后才进 Phase B」(`019ff413` Spec Level 2 vs 3 / `f658ae7e` 版本级别 PATCH vs MINOR / `334e62dc` 决策单勘正 / `56845091` 是否顺手补 `now=`)。Level 若升 3 需另补 `tasks.md` (A.2) + `detailed-tasks.yaml` (A.3) + post_planning; 版本级别定错会连坐 Task 5.1 的 16 个版本点、tag 与 CHANGELOG 标题。审计席无权代裁 (Rule #10), **R4 之后仍须 owner 闭合才能进 B.1**。
  *type 注*: knowledge-manager 报 risk/minor, 保留原 type。

### Decisions (9 — 全部 minor; 按 R1 / R2 / R3 同规则**不计入**上表缺陷 severity 计数)

- `a1cede1a` [decision] documentation/R3 19 条 major 正文落地复核 — **found_by: tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager (5/5)**
  五席各自独立把 R3 的 19 个 major id 映回 proposal 正文, 结论一致: **19 条全部落在正文而非批注**, 未见「加批注代替修正」形态, 亦未见系统性回填矛盾。knowledge-manager 给出逐 id 命中计数 (`a7536535` 3 / `92565b30` 9 / `ebaad4a5` 6 / `b5a94a9c` 3 / `120e1171` 7 / `2af687f5` 2 / `3dd75e12` 4 / `b57e3209` 3 / `4608f5b2` 6 / `f658ae7e` 2 / `019ff413` 2 / `56845091` 3 / `17f270f5` 1 / `1ad9b4ed` 3 / `90e3b4b8` 1 / `7d909571` 3 / `db126eff` 5 / `e854a801` 2 / `334e62dc` 1); tech-lead 另实读复核 `b5a94a9c` 的块边界正确 (顶层返回键表确为 `:16-31`, TrackEntry 块确为 `:35-44`)。**唯一例外**: tech-lead 指出 `ebaad4a5` 的行号勘正自身出错 (已单列为 `7b7aed03`)。
  *category 注*: 四席 documentation、code-reviewer testing ⇒ 取多数 documentation。

- `be109744` [decision] documentation/载重事实与基线冻结独立复跑 — **found_by: backend-architect (architecture), qa-engineer (documentation), code-reviewer (testing), knowledge-manager (documentation) (4/5)**
  四席各自机械核验, 结论一致「事实底座成立」: 五份 SOT 副本与 `git -C aria show 301641b:` **md5 逐一相同** 且触点 `diff --stat` 为空 (backend-architect) ⇒ 全文行号可信; 9 模块点名集实跑 `Ran 167 tests … OK` (5 模块 102 + 4 模块 65, qa-engineer / code-reviewer 各自复跑); 日历探针恰 2 条转红且名字与 `:304` 逐字一致 (code-reviewer); AB 套件 17551 B、`tracks_multibranch` 唯一命中 `ab-suite/state-scanner.json:214` 且题面写死 `collision.kind`、另三词 0 (qa / code-reviewer / knowledge-manager); Task 5.1 十六个版本点全为 v1.71.1 (code-reviewer 全数 / knowledge-manager 抽验 12 处 / backend-architect 逐处 `sed -n` 命中); gitlink aria=`301641b` / standards=`21748d4` 与头部冻结一致 (四席); 本仓 `docs/handoff/` 190 份顶层 `.md` / 零子目录 / 零非 ASCII, 两份冻结语料各 996 行 (qa / code-reviewer); 10 个 `feedback_*` memory 文件与决策单、两份 archive 先例全存在, issue-195 `:21` / `:41` 与 triage `:25` / `:53` 逐字相符 (knowledge-manager)。
  *规则 5 内注*: backend-architect「本轮机械核验清单」8 项、code-reviewer「复核记录」6 项、qa-engineer「本轮机械核验清单」11 项均为正文-only 的正向核验, 已归并于此, 供 R5 免重跑。

- `59f15b38` [decision] architecture/ship 顺序 / gitlink 归属 / 版本号占用 — **found_by: tech-lead (1/5)**
  主仓 `HEAD` = `origin/master` = `e58ac22`; `git ls-tree HEAD aria` = `301641b` = aria `origin/master`; `standards` gitlink = `21748d4` = 其 `origin/master`; `git -C aria tag --list 'v1.7*'` 最高 `v1.71.1`。⇒ Task 5.2 的「从 `301641b` 前进, 严禁回退 `0545f86`」与 Task 4.4 的「standards 只许从 `21748d4` 前进」两条写死起点均正确, 两个候选号未被占用。

- `a0cb3407` [decision] architecture/越界面 / 同伴容器在飞轨 — **found_by: tech-lead (1/5)**
  触点集合不含 `phase1_gate.py` / `claim_lifecycle` / `spec-drafter` / `phase-a-planner` / AB 套件本体 (`phase1_gate` 全文仅作认领命令出现一次; `ab-suite/state-scanner.json` 四处出现全为证据引用或 Task 5.5(b) 的缺口 issue, 无编辑动作)。同仓另一在制 spec `pre-merge-completeness-gate-change-scope` (#199) 触点为 audit-engine + `ab-suite/audit-engine.json` + `version.yaml`, 与本 spec 五触点**零文件交集**; 两者只在 aria 版本号面串行, 已由待复议 6 的 `ls-remote --tags` 前置覆盖。`docs/handoff/latest.md` track 表在飞仅本容器 M6 轨 (aria-orchestrator, 零交集)。**无越界**。
  *规则 5 内注*: knowledge-manager 正文 decision「sibling probe」给出同结论的第二份扫描面 (`openspec/changes/` 八个在制 spec 中引用 `Aria#195` 的只有本 spec; #199 只引用 `standards/` 不改它, 无 standards gitlink 撞车), 因未列入其结构化清单故不计入 found_by。
  *与上轮的关系*: 本条是**本轮唯一与 R3 四元组完全相同的 key** (交集 1/34)。

- `8e0b1f6e` [decision] architecture/A′ 骨架与真代码及上游原文对得上 — **found_by: tech-lead (architecture), backend-architect (implementation) (2/5)**
  四个 git 路径消费方确为全部 (`handoff_multibranch.py:301` `_read_file_content` / `:321` `_get_file_commit_date` / `:329-336` `_make_legacy_track_id` / `scan.py:186`), 无第五处; `"rel_path"` 作为**字典键**在插件 1.71.1 全树 **0 命中** (56 处 `rel_path` 全是局部变量名) ⇒ 新键不与既有语义撞名; Task 2.1 推荐默认 (保持 2-tuple + 注入带默认值的 reporter) 与 `test_max_branches_resolver.py:286,300,316,332` 的 mock 形态兼容 (tech-lead)。上游原文支持 A′: issue `:41`「`filename` / `track_id` 等需要 basename 的字段另行派生」与 triage `:53` 逐字相符; 守卫挂点 `_render_pointer:116/121/143` 结构可容 `rel == filename` 判据; hermetic 实跑确认 `ls-tree -z` 输出原样路径且 pathspec `-- docs/handoff` 不匹配 `docs/handoff-archive/` ⇒ 前缀守卫无兄弟目录误剥面 (backend-architect)。
  *category 分歧注*: tech-lead architecture、backend-architect implementation ⇒ 1:1 平票取席位序在先者 = architecture。
  *规则 5 内注*: tech-lead 正文另有 decision「根因判断成立」(契约错配定性与实读一致: `:246-247` docstring 自述 + `:277` `Path(path).name` + 三处 `_HANDOFF_TREE_PATH` 拼串 + `scan.py:186` 第四处独立字面量; B/C/D 三案的取舍理由成立), 未列入结构化清单, 归并于此。

- `6a99cefd` [decision] documentation/头部机械判据 / Rule #10 — **found_by: knowledge-manager (1/5)**
  `linked_issue_field_probe.py` 实跑 `OK (8 份在范围内, 6 条在册)`, 本 spec **不在**白名单 (`.aria/linked-issue-field-grandfathered.txt:17-22` 六条全是 M6/M7 轨); 头部 `> **Linked Issue**: \`10CG/Aria#195\`` 为单 code span、行首无空白、`>` 后恰一空格 (`cat -A` 核), 满足 `spec-drafter/SKILL.md:414-424` 三条写法; 字段序与 `standards/openspec/templates/proposal-minimal.md:3-6` 一致。审计计划行与 `.aria/config.json` `audit.checkpoints` 逐项吻合 (post_spec / post_planning = convergence, 其余 off), 8 条待复议全部上交 owner, **无 AI 自行豁免** (Rule #10 满足)。

- `25cffd35` [decision] testing/SC-11(c) 新判据鉴别力实测 — **found_by: knowledge-manager (1/5)**
  R3 `90e3b4b8` 的替换经基线实跑成立: `handoff_multibranch.py` 上 `grep -c 'Returns only the basename'` = **1** (有鉴别力), `'path relative to'` = **0** (正向断言亦 baseline-failing), 旧判据 `'callers compose the full git-object path'` = **0** (确因跨 `:246`/`:247` 而恒绿)。
  *规则 5 内注*: tech-lead 正文 decision「SC-11 机检判据的基线可证伪性」、backend-architect 核验清单第 5 项、code-reviewer 复核记录同项均给出**逐字相同的三个计数**, 因未列入各自结构化清单故不计入 found_by; 四席独立同值 ⇒ 该事实可视为已闭合。

- `9a445c52` [decision] testing/SC-10 点名集与消费方覆盖面 (9 模块 167 全绿) — **found_by: qa-engineer (1/5)**
  真 checkout `301641b` 实跑: 原五模块 `Ran 102 tests … OK`, 新补四模块 `Ran 65 tests … OK`, 合计 167 全绿。全 aria 树中引用 `tracks_multibranch` / `collect_handoff_multibranch` / `write_latest_md` / `_list_handoff_files` 的**测试**模块恰 7 个, 9 模块点名集全覆盖; 跨 skill 唯一生产消费方 `phase-d-closer/scripts/fetch_gate.py:187` 以入参吃 `collision_kind`, 其测试传字面值 ⇒ 无回归面。另: `references/json-diff-normalizer.md` 的 `reference-snapshot-aria.json` 无任何测试消费 ⇒ §6.3 的 defer 无测试面风险。

- `1d02ae0a` [decision] documentation/头部主仓 HEAD 快照已陈旧 — **found_by: backend-architect (1/5)**
  头部写主仓 `HEAD` / `origin/master` 均为 `ecb6296`, 实测现为 `e58ac22` (R3 席位测得 `f634d837`), **三轮三值**; 但载重量 (gitlink 起点 `301641b`, 严禁回退 `0545f86`) 仍成立。建议把该句改成「起草时快照」措辞, 终止逐轮漂移。
  *type 注*: backend-architect 报为 decision, 汇总席保留原 type (其内容含一条可执行建议, R5 若判为 issue 可自行改判)。

---

## Verdict

**FAIL** — Critical **1** / Major **10** / Minor **14** (另 9 条 decision 不计入)。

按 `references/report-storage.md §Verdict 计算` 的 SOT 规则: `>=1 Critical ⇒ FAIL`。`drift_terminated: false`, 无 override。

**这个 FAIL 的来源须说清楚**: 五席里**只有 code-reviewer 一席自报 FAIL**, 另四席自报 PASS_WITH_WARNINGS。翻盘点是 `5c28d58f` 一条 —— backend-architect 与 code-reviewer 在各自工作副本上**独立实跑同一处方、取到同一组三条转红** (`test_scan_integration` 的 `TestSnapshotSelfConsistencyAC5` 三条), 事实层两席完全一致, 分歧**只在定级**: backend-architect 报 major (其判据是「无方案错误 / 无破坏生产消费方 / 无 SC 恒绿假绿」三类), code-reviewer 报 critical (其判据是「处方与验收判据互斥, 且 spec 对该模块的性质判断经补丁模拟证伪」, 并援引 R2 同型条 `6f8fa9f7` 已被判 critical 的先例)。合并规则 1 与 `report-storage.md` 的 SOT 都要求取最高 severity, 汇总席**不自行下调**, 故本轮 verdict = FAIL。**该定级差建议交 owner / R5 复议** (与 R3 对 `90e3b4b8` 记「定级分歧待复议」同办)。

其余判断: 方案骨架 (A′ = `filename` 保持 basename + additive `rel_path` + 四个 git 路径消费方改读 + git show 失败不再伪造 legacy + 写侧守卫) 被五席从五个透镜独立复核成立, **无一席主张推翻**; R3 的 19 条 major 经 5/5 全席逐条复核**全部落进正文而非批注** (`a1cede1a`), 与 R3 四元组交集仅 1 条 (且是一条 decision) —— 本轮 25 条缺陷类**无一是重开 R1 / R2 / R3 已闭合项**。

10 条 Major 集中在**三族**:

1. **R3 rework 新写段落的下游没走完 (4 条)** — `ead9ac24` (`degraded_reason` 有取值定义、无产生路径, 最省事实现重造本 spec 自己点名的根因模式) · `5513534d` (`scan.py` 改读 `rel_path` 后同函数两个**上报**字段归属未定, 是 R3 `b57e3209` 没走完的那半) · `5b252465` (守卫落点的两处 docstring 漏出 Rule #3 同步清单) · `ab615189` (rule6_note 前提句没随新增 references 触点同步, Rule #6 留痕载假前提)。
2. **载重论证经实跑为假 (3 条)** — `5105b00e` (`action` 枚举不动的唯一机械证据不成立) · `31bc3c6a` (禁重生成冻结语料的理由不成立, 真正会红的是另一行) · `177d72e6` (SC-3 的 baseline-red 资格随宿主 `core.quotePath` 漂移)。三条均属**「勘正引入新错」形态**, 与 `7b7aed03` 的行号勘正反向出错同源, 建议连同 R3 那次一并由**非原作者**执笔复核 (memory `feedback_author_and_verifier_must_differ_for_corrections`)。
3. **契约面与流程门缺口 (3 条)** — `7ae33f13` (两个自称「恒存在」的字段在第二构造点无 SC 承接, 承接它的 SC-16 是可真空满足的全称谓词; 叠加 `5c28d58f` 的无兜底早退即把 F1 原样搬回) · `23b414c9` (`n_active` 是第五个被改动却未登记的量, 直通 writer 三分派与 Task 4.4 要改的那张 SOT 表) · `b3e5ea8d` (待复议 7 无任务承接, 而它决定 Phase B 之前要不要先补 A.2 / A.3)。

全部 11 条 (1 critical + 10 major) 的修法都在 Phase A 内改 spec 即可消解, **零设计骨架改动**; 两席对 `5c28d58f` 的修法完全一致 (Task 2.2 明写夹具补键 + 删掉已证伪的「照绿」句)。

`post_spec` 为 `blocking: false` (见 `report-format.md §阻塞行为` —— FAIL 在 post_spec 是「继续 (仅记录)」), 本 verdict **不阻断**后续流程; 但按 Rule #10, 上述 critical / major 不得由实施者以「代码面小 / Level 低 / session 已长」自行降格、跳过或改序。其中 **5 条须 owner 拍板后才进 Phase B**: R3 已定的 4 条 (`f658ae7e` 版本级别 / `019ff413` Spec Level / `334e62dc` 决策单勘正 / `56845091` 日历依赖) 加本轮 `b3e5ea8d` (Level 裁定的任务承接), 另 `5c28d58f` 的 critical vs major 定级差同属 owner 门。

---

## 轮次记录

### Round 1 (承前)

- Agents: 5/5 (缺席 0) — Conclusions 33 去重后 (Critical 2 / Major 15 / Minor 10 / Decisions 6), 去重前 60
- Vote: REVISE 5 / PASS 0 — verdict **FAIL**
- 来源: `.aria/audit-reports/post_spec-R1-2026-09-06T154800-000Z-R1-handoff-multibranch-subdir-path-fidelity-aggregated.md`

### Round 2 (承前)

- Agents: 5/5 (缺席 0) — Conclusions 31 去重后 (Critical 3 / Major 10 / Minor 9 / Decisions 9), 去重前 55; 与 R1 交集 0
- Vote: REVISE 5 / PASS 0 — verdict **FAIL**; conflicted 1 (`cecc06af`, 已由 rework hermetic 实跑闭合)
- 来源: `.aria/audit-reports/post_spec-R2-2026-09-07T004500-000Z-R2-handoff-multibranch-subdir-path-fidelity-aggregated.md`

### Round 3 (承前)

- Agents: 5/5 (缺席 0) — Conclusions 33 去重后 (Critical 0 / Major 19 / Minor 7 / Decisions 7), 去重前 51; 与 R2 交集 0
- Vote: REVISE 5 / PASS 0 — verdict **PASS_WITH_WARNINGS**; conflicted 1 (`120e1171`, 已由 R3 rework 双前提实跑闭合)
- 来源: `.aria/audit-reports/post_spec-R3-2026-09-07T004500-000Z-R3-handoff-multibranch-subdir-path-fidelity-aggregated.md`

### Round 4

- **Agents**: 5/5 (缺席 0; `round_incomplete: false`, `skipped_agents: []`) — tech-lead / backend-architect / qa-engineer / code-reviewer / knowledge-manager
- **Sibling probe**: 本轮已完整扫描, 未发现同 issue 竞品 (五席逐席自述一致; tech-lead 与 knowledge-manager 另各给一份扫描面 —— `openspec/changes/` 8 个在制 spec 中引用 `Aria#195` 的仅本 spec; 唯一与 aria-plugin 发版面重叠的 `pre-merge-completeness-gate-change-scope` (#199) 触点为 audit-engine + `ab-suite/audit-engine.json` + `version.yaml`, 与本 spec 五触点零文件交集; `docs/handoff/latest.md` track 表在飞仅本容器 M6 轨)
- **Conclusions**: 去重前 **57** (tech-lead 12 / backend-architect 12 / qa-engineer 12 / code-reviewer 9 / knowledge-manager 12) → 去重后 **34** (Critical 1 / Major 10 / Minor 14 / Decisions 9)
- **Delta vs 上轮 (R3, 33 条)**: `+33 / -32` —— 四元组交集 **1** (唯一相同 key = `decision|minor|architecture|越界面 / 同伴容器在飞轨`, 即 `a0cb3407`)。R3 的 19 major + 7 minor 全部闭合 (`a1cede1a`, 5/5 复核), 本轮 25 条缺陷类**全部为新增**: 其中 4 条落在 R3 rework 自身新写段落的下游 (`ead9ac24` / `5513534d` / `5b252465` / `ab615189`), 3 条是 R3 rework 写进去的载重论证经本轮实跑证伪 (`5105b00e` / `31bc3c6a` / `177d72e6`), 1 条 (`7b7aed03`) 是 R3 的行号「勘正」自身反向出错, 其余 17 条是前三轮未测到的机械事实
- **Vote 票型**: REVISE **5** / PASS **0** ⇒ `unanimous_pass = false`
- **自报 verdict 票型**: PASS_WITH_WARNINGS **4** (tech-lead / backend-architect / qa-engineer / knowledge-manager) / FAIL **1** (code-reviewer)
- **conflicted**: **0** 条 (逐条比对未发现结论相反的对立意见; 唯一定级差 `5c28d58f` 按规则 1 属 severity 差, 已取最高并记「待 owner / R5 复议」)
- **收敛判定 (汇总席实算, 最终由编排脚本裁决)**: `conclusions_stable = (R4 keys == R3 keys)` = **false** (34 vs 33, 交集 1); `unanimous_pass` = **false** ⇒ **`converged = false`**
- **振荡检测**: `keys_R4 == keys_R2`? **false** —— R2 为 Critical 3 / Major 10 / Minor 9 / Decisions 9 (31 条), R4 为 Critical 1 / Major 10 / Minor 14 / Decisions 9 (34 条), 条目数与 severity 分布均不相等 ⇒ `oscillation = false`
- **Duration**: N/A (编排脚本未向汇总席传递计时)

---

## 统计

| 指标 | 值 |
|------|-----|
| 总轮次 | 4 |
| 总耗时 | N/A |
| Agent 参与率 | 5/5 (缺席 0) |
| 需补齐 frontmatter 的席位报告 | 0 / 5 (机械核验 15/15/15/15/15 字段) |
| 去重前/后 conclusions | 57 / 34 |
| Critical / Major / Minor | 1 / 10 / 14 |
| Decisions (不计入 severity) | 9 |
| conflicted 条目 | 0 |
| finding id 碰撞 | 0 / 34 (python3 sha256 实算) |
| 与上轮四元组交集 | 1 (R4 34 条 vs R3 33 条) |
| 收敛轮次 | N/A (未收敛) |

### 席位票型与自报计数

| 席位 | Vote | 自报 verdict | 自报 C / M / m | 结构化条目数 |
|------|------|--------------|----------------|--------------|
| tech-lead | REVISE | PASS_WITH_WARNINGS | 0 / 4 / 4 | 12 (含 4 decision; 正文另有 2 条 decision 未入清单) |
| backend-architect | REVISE | PASS_WITH_WARNINGS | 0 / 3 / 5 | 12 (含 4 decision) |
| qa-engineer | REVISE | PASS_WITH_WARNINGS | 0 / 4 / 4 (+1 minor risk) | 12 (含 3 decision) |
| code-reviewer | REVISE | **FAIL** | **1** / 1 / 5 | 9 (含 2 decision) |
| knowledge-manager | REVISE | PASS_WITH_WARNINGS | 0 / 2 / 5 (+1 minor risk) | 12 (含 4 decision; 正文另有 1 条 decision 未入清单) |

---

## Rework 清单

Critical **1** 条 + Major **10** 条, 逐条列出 (id / 提出席位 / 建议动作)。动作取自各席报告原文, 汇总席**不裁决**、不新增修法。

| # | id | 席位 | 建议动作 |
|---|----|------|----------|
| 1 | `5c28d58f` **[critical]** | backend-architect · code-reviewer | Task 2.2 明写「同批给 `test_scan_integration.py:164-166` 的 `HEALTHY_TRACKS` 补 `rel_path`」(与 Task 2.1(ii) 改四处 mock 同型), **并删掉** §3 (`proposal.md:125`) 那句经两席实跑证伪的「写 `.get()` 则照绿」断言; 同时确认 SC-10 (`:304`) 与 Task 4.3 (`:266`) 的「不被打红 / 全绿」在补键后成立。**定级分歧 (critical vs major) 待 owner / R5 复议** —— 它是本轮 verdict 的唯一支点。 |
| 2 | `ead9ac24` | tech-lead · backend-architect | Task 2.5(e) 明写 `degraded_reason` 的传播路径 (backend-architect 推荐 `_render_pointer` 返回 `(content, reason)`, 禁止在 `write_latest_md` 内重算同一谓词); SC-15 布局 1 与布局 3 各加一条 `degraded_reason is None` 断言 + 一条反事实。 |
| 3 | `5513534d` | tech-lead · code-reviewer | 在 §3 / Task 2.2(a) 明写 `scan.py:193` / `:204`(或 `:209`) 上报的 `"filename"` 装 basename 还是 `rel_path`; 若语义有变则登记进 §5 / §6 / CHANGELOG, 并同批核对 `test_scan_integration.py:272` 的断言; 顺带补 schema `errors[].tracks[]` 子键形状 (`:1141-1147` 现只列三键)。 |
| 4 | `5105b00e` | qa-engineer | 重写 §2.5 (`proposal.md:144`) 三选一裁定块的依据 —— 现援引的「改枚举会打红 `test_p1_layer_h.py:264`」经实读为假 (该夹具无 `rel_path`, 走真指针支)。结论可保留, 但须换成可核实的真依据 (例: 老消费方只 switch `action` 的向后兼容代价), 或把该取舍并入 §待 owner 复议。 |
| 5 | `7ae33f13` | backend-architect · qa-engineer · code-reviewer | SC-16 夹具明写「至少一份带 frontmatter + 一份不带」并断言 legacy 行 `rel_path` 存在; SC-13 追加 `rel_path` 断言; 任一正常路径 SC 追加 `data["unreadable_count"] == 0`。(与第 1 条同批做 —— 两者叠加才是 F1 复现的完整链。) |
| 6 | `177d72e6` | qa-engineer | SC-3 明写「新夹具必须复用 `_GIT_ENV` 式配置隔离 (`GIT_CONFIG_GLOBAL` / `GIT_CONFIG_SYSTEM` = /dev/null)」, 并订正 SC-4 / SC-13 里「只 pin 姓名 / 邮箱」的描述; §Why F2 与 CHANGELOG `### Fixed` 改成条件式表述 (`-z` 使行为**不再依赖** `core.quotePath`)。 |
| 7 | `31bc3c6a` | qa-engineer | 把 §7 / Task 4.3「禁重生成冻结语料」的证据从 `test_collision_frozen_corpus.py:51`/`:112` 换成 `:111` 的 `assertEqual(len(rows), 996)` + `freeze_corpus.trim` 的八字段投影事实 (`:29,32-37,48-53`); 禁令保留, 理由更正。 |
| 8 | `b3e5ea8d` | tech-lead | 给 §待复议 7 (Level 2 vs 3) 装与待复议 6 同级的前置门 (「裁定后才进 Phase B」), 并在 Task 2.0 的枚举里补上它; 若 owner 裁 Level 3 则须先补 A.2 `tasks.md` + A.3 `detailed-tasks.yaml` + post_planning。**须 owner 裁** (Rule #10)。 |
| 9 | `ab615189` | tech-lead · knowledge-manager | 订正 rule6_note 第 1 条前提句 (`:334`): 从「无 SKILL.md / references 的文本变动」改为逐条列出四处 references 触点 (`state-snapshot-schema.md` / `phase-1-collectors.md:102` / `layer-l-integration.md:103` / 视 Task 4.5 结果的 `references/rules/*`); 判据表选行由第四行「拿不准」改到第二行「处方性 · 运行时指令面 ⇒ 照跑 AB, 零裁量」(`skill-benchmark-exemption.md:29`)。照跑结论不变。 |
| 10 | `5b252465` | knowledge-manager | 把 `latest_md_writer.py:111-114` 与 `:152` 两处函数 docstring 纳入 §6.2 同步清单与 Task 2.5 / Task 4.2, 并加一条 SC-11 grep (与 `:32`/`:279`/`:287-290` 同批)。 |
| 11 | `23b414c9` | tech-lead | 把 `n_active` 作为第五个受影响的量登记进 §5 / Impact / CHANGELOG; 给 SC-15 补一个 `n_active ≥ 2` 布局 (或明写该情形的处置), 并核对 Task 4.4 要改的 `standards/conventions/session-handoff.md:172-173` 那张按 active 数分档的表在子目录场景下是否仍自洽。 |

> **Minor 与 Decisions 不进 Rework 清单** (14 条 minor 见上文 `### Minor (14)` 各条内附修法; 9 条 decision 为核实通过项, 无动作)。
>
> **跨条提醒 (汇总席不裁决, 仅记)**: 第 1 / 5 条是同一条失效链的两端 (无兜底早退 + legacy 行漏填), 建议同批闭合; 第 4 / 7 / 6 条与 minor `7b7aed03` 同属「R3 勘正动作自身引入新错」形态, 按 memory `feedback_author_and_verifier_must_differ_for_corrections` 建议**由非 R3 执笔者执笔**。
