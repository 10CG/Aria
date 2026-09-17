---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-15T22:05:00.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

## 审计结论

### 实读范围

- `openspec/changes/handoff-multibranch-subdir-path-fidelity/tasks.md` 全文 (160 行)
- `openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml` 全文 (868 行)
- `openspec/changes/handoff-multibranch-subdir-path-fidelity/sc11-predicate-validation.py` 全文 (341 行)
- `.aria/audit-reports/post_planning-R2-2026-09-15T180659-081Z-handoff-multibranch-subdir-path-fidelity-aggregated.md` 全文 (334 行)
- `git diff 0f50239 2b9cb3e -- openspec/changes/handoff-multibranch-subdir-path-fidelity/` 全量 (sc11-predicate-validation.py 部分逐行核对; tasks.md / yaml 部分用定向 grep 核对关键改动点)
- `proposal.md` 的 SC-1/3/4/5/6/8/11/17 行 (定向提取「反事实」列原文, 用于核对 TASK-035/015 补丁是否忠实转译)
- `aria/skills/state-scanner/references/state-snapshot-schema.md` 相关段落 (`tracks_multibranch` 块, 1076-1140 行) 与 `scripts/collectors/handoff_multibranch.py` 的 `dictionary-max` 命中行 (用于核对谓词是否对齐真实文件)
- `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` 场景 1 与 WITHOUT_BETTER 定义段; `aria-plugin-benchmarks/ab-results/2026-09-05-v1.70.0-a1-entry-rule6/` (RESULT.md §1.2/§4, SCORES.md 的 rep2/rep3 先例) 与 `2026-09-08-v1.73.0-archive-skill-drift/` 目录是否存在
- `aria/skills/state-scanner/lib/failure_handlers.py:95` (`no_push_requested_by_env` 是否真实存在)

未读: 同轮 code-reviewer / tech-lead 的 R3 报告 (约束要求独立); post_planning R1 聚合报告与 R1 五份席位报告 (任务未要求, 且清单第 16 条明确是 R1 遗留裁决, 与本轮改动无关)。

### 实跑命令与关键输出

1. **完整多状态验证脚本实跑** (`TMPDIR` 指向本席 scratchpad):
   ```
   TMPDIR=.../scratchpad/r3-qa-engineer/tmp python3 -B .../sc11-predicate-validation.py
   ```
   输出 `verdict: OK (mismatch cells 0, stderr notes 0; 13 states x 19 predicates)`, exit code 0, 打印矩阵与 yaml `metadata.sc11_predicate_validation.measured_2026_09_15_at_1cb3872_v3_1` 逐字节一致 (13 状态 × 19 谓词全部核对, 未发现任何格不符)。

2. **`-OO` 等价性核验** (核对「不依赖 assert, python3 -O/-OO 下行为不变」的声明): `python3 -OO` 与 `python3 -B` 两次运行的 stdout 与 stderr 逐字节 diff 为空, `check_doc_lists_states()` 改从源文件重新 `ast.parse` 而非读 `__doc__`, 声明成立。

3. **`assert` 残留检查**: `grep -n "assert" sc11-predicate-validation.py` 只命中 docstring 里描述该性质的一句话, 代码体内零 `assert` 语句, 与「验证脚本不依赖 assert」的返修声明一致。

4. **对抗构造: (a1)/(b) 谓词是否抗「字段填错块」** (proposal SC-11(c) 原文自述过一次真实史料 —— R3 major `b5a94a9c` 曾把 `unreadable_count`/`rel_path` 两个字段错误指派进对方的块): 在 `target` 态基础上把 `unreadable_count` 从顶层块移进 `TrackEntry` 块、把 `rel_path` 从 `TrackEntry` 块移进顶层块 (脚本见 scratchpad `test_wrong_block.py`), 实跑结果 `a1: FAIL`, `b: FAIL`。两条谓词的 `sed` 区间提取正确地把这一类换块错误钉死, 不依赖专门的验证态也能拒绝, 核实通过, 非缺口。

5. **依赖图完整性**: 用脚本解析 yaml 全部 35 个 TASK 的 `dependencies`, 结果: 总任务数 35 (与 `metadata.total_tasks` 一致), `est_hours` 求和 105.0 (与 `metadata.est_hours_total` 一致), 无悬空依赖、无环。`parent` 字段去重后 27 个, 与 `tasks.md` 的 27 个 checkbox (`grep -c '^\s*- \[[ x]\]'`) 完全对应。

6. **AB 引用真实性核验**: `no_push_requested_by_env` 函数确认存在于 `aria/skills/state-scanner/lib/failure_handlers.py:95`; `aria-plugin-benchmarks/ab-results/2026-09-05-v1.70.0-a1-entry-rule6/RESULT.md` §1.2/§4 与 `SCORES.md` 的 `-rep2`/`-rep3` 命名先例真实存在; `2026-09-08-v1.73.0-archive-skill-drift/` 目录真实存在。`AB_TEST_OPERATIONS.md:219` 的 `delta.pass_rate > 0` 验收句与 `:222-235` 的协调 ref 三步隔离流程均与 TASK-026 的描述吻合。

7. **`(j4)` 正则的左边界实测**: `grep -inE '4[- ]levels?' scripts/collectors/handoff_multibranch.py tests/test_handoff_multibranch_collision_dedupe.py references/state-snapshot-schema.md` 在 1cb3872 基线上只命中 `test_handoff_multibranch_collision_dedupe.py:885` 与 `:1162` 两处真实待改行, 无任何数字巧合命中; 结合脚本对 `target` 态的实测 (j4 全 PASS), 当前语料下该正则缺左边界(`\b`) 不构成实际误伤, 见下方 Minor m1。

### R2 处置落地核验 (本席侧重: 判据 / 证据链相关簇)

| R2 项 | 处置摘要 | 落地状态 | 证据 (file:line) |
|---|---|---|---|
| PP2-M1 | TASK-019/020/023 补依赖 TASK-033; TASK-033 收窄为四路径 `git add`; TASK-018 改副本生命周期证据 | 落地 | yaml:537 `dependencies: [TASK-012, TASK-013, TASK-014, TASK-033]`; yaml:558 同式; yaml:619 `[TASK-013, TASK-033]`; yaml:428 (TASK-033 四路径 add); yaml:501 (TASK-018 worktree add/remove + `worktree list` 断言) |
| PP2-M2 | 主仓分支起点加 B.1 前置 (规划提交已推送) + 回落支; 三处 origin/master 先 fetch | 落地 | tasks.md:30 (读前必看 13); tasks.md:51 (清单 13); yaml:164-166 (TASK-001 前置核验含 `merge-base --is-ancestor` 判定); yaml:127 (owner_gates 首项) |
| PP2-M3 | 组 4 各任务补 aria 侧提交点; TASK-021 回归前记两仓 HEAD; TASK-029 干净工作树断言 + 原位回归 (不用 worktree 副本, 主控明确调整未采纳 TL 建议); TASK-031 开 PR 前核验 | **部分落地 + 一处 v3.1 未回链披露 (见 Major 1)** | yaml:548/571/630-631/705/822 (五处提交点); yaml:585 (TASK-021 回归前双仓 HEAD); yaml:771/775/777 (TASK-029 第 4/7 步 + notes 明写「主控调整」); yaml:837 (TASK-031 现文本为「有范围的检查」, **非** R2 原文「为空」, 见 R2 报告:118) |
| PP2-M7 | 脚本改全 13 态 × 19 谓词矩阵比对, rc 语义细化, 临时目录清理入 try/finally | 落地 | 脚本 289-336 行 (`main()` 内 `try/finally` + 逐格 diff); 本席实跑 verdict OK, 13×19 |
| PP2-M8 | (a2) 改为定位 Fail-soft 行反引号内形状 dict, 加 `bad_a2_prose_only` 态 | 落地 | yaml:76 谓词原文; 脚本 `PRED["a2"]`; 本席实跑矩阵 `bad_a2_prose_only` 行仅 a2=FAIL 其余 PASS, 与 EXPECTED 一致 |
| PP2-M9 | proposal SC 表反事实 (SC-1/3/4后半/5/8后半/14/17) 全部改三步法, 新增 TASK-035; RED 记录不再充当反事实; TASK-011 中间态兜底删除 | 落地 | yaml:503-524 (TASK-035 全文, 6 个补丁逐条对应 7 个 SC); yaml:151 (hard_constraints); yaml:284 (TASK-007 "RED 记录只作 RED 证据"); yaml:362 (TASK-011 notes 明确移交 TASK-035) |
| m8 | 由 PP2-M9 统一闭合 | 落地 | 同上; TASK-011 无残留反事实兜底条款 |
| m9/m14/m15 | (j4) 同义词扩面 + 历史措辞约束改写; (j2)/(j3) 锚点调整; (l1) 拆 Returns/Scenarios | 落地 | yaml:66-113 (`sc11_predicate_validation` 全块含 authoring_rules); 本席实跑 `bad_stale_synonym`/`bad_stale_header`/`bad_test_docstring_stale`/`alt_j3_anchor` 四态与 EXPECTED 一致 |
| m16 | 冻结语料 diff 拆成两条独立 `git diff` (子模块/主仓分开), 避免超级仓对子模块路径恒 0 行 | 落地 | yaml:590 (TASK-021 两条独立命令, 各自基线 SHA 取自 TASK-001 台账) |
| **未在本清单单独裁决, 但发现的额外偏差** | v3.1 (j3) 谓词 fail-closed 修复 —— 已回链披露 | 落地且披露 | tasks.md:50 (清单第 12 条括注 "v3.1 主控核验返修") |
| **同上, TASK-029/034 回退命令写死、脚本不依赖 assert** | 已在 yaml:19 的 `metadata.updated` 注记, **未**回链进清单 | 技术上落地, 披露渠道不完整 | 见 Major 1 |

### 实施者试派生 (选 4 个与本席侧重相关的 TASK)

**1. TASK-001** (B.1 基线复核, parent 1.3) — 只看本任务文本 + 引用的 `sc11-predicate-validation.py` / `metadata.sc11_baseline_predicates`: 可无歧义执行。「重跑脚本, 退出码 0 且矩阵与 yaml 实测块逐字节一致」这条已被本席直接验证为真实可达 (见上「实跑」1)。唯一需要跨文件才能确认的点: 「touchpoints-aria.txt 由 proposal §触点文件清单表机械导出」未给出具体导出脚本或字段规则, 需要实施者自行读 `proposal.md:30-95` 的表格结构; 但这与 v3/v3.1 改动无关 (A.2 已完整跑过一次, `metadata.baseline_rebase` 已留痕), 不计入本轮 finding。

**2. TASK-035** (proposal SC 表反事实, parent 3.5) — 只看本任务文本 + 引用的 TASK-017/hard_constraints: 六个补丁描述具体、可与 proposal 原句逐条对照 (本席已对 SC-1/3/4/5/8/14/17 七条原文核对, 补丁 1/2/4/6 是原句的直接转译, 补丁 3/5 是清单第 18 条披露过的合理偏离, 理由站得住 —— 见下方"核对无误的部分"第 6 条)。卡点: 「与 TASK-017 的『_get_file_commit_date 仍拼顶层路径』同形, 可复用该副本与 diff」一句, 按 `hard_constraints` 的强制约束 ("副本的创建与移除...任务结束时 `git -C aria worktree list` 不含本任务副本"), TASK-017 结束时其 worktree 副本已被移除, 实施者若照字面理解"复用该副本"会去找一个已不存在的目录; 只能复用"diff 文本"重新打在 TASK-033 SHA 检出的新副本上。此为 Minor (措辞), 见 m3。

**3. TASK-026** (Rule #6 AB, parent 5.5) — 只看本任务文本 + `rule6_note` + `AB_TEST_OPERATIONS.md`: 三步协调 ref 隔离、PREDICTION 时点、两臂 SHA 口径、逐 eval 判回归的复跑规则均可执行, 且本席已逐条核实引用的函数/先例文件真实存在 (见上「实跑」6)。未发现卡点。

**4. TASK-031** (主仓 PR + pre-merge gate, parent 5.2) — 只看本任务文本: 「开 PR 前 (提交面, 有范围的检查...)」一条本身可执行 (逐行归属 + 判定与本 cycle 无关的操作定义清楚), 但**这条标准已经偏离 R2 聚合报告的原文处置** (R2 原文: 「主仓 `git status --porcelain` 为空」), 而 tasks.md 的「AI 流程判断清单」18 条中没有一条披露这次改动。实施者单独执行 TASK-031 不会做错 (文本本身自洽), 但**审阅 / 复议这次改动的 owner 会因为清单缺项而看不到这个从"空"到"有范围"的放宽**, 这是本轮的主要 finding, 见 Major 1。

### Findings

**[Major] type=issue · category=documentation · scope=tasks.md「AI 流程判断清单」/ detailed-tasks.yaml metadata.updated · v3 引入: 部分 (v3.1 阶段引入)**

证据:
- R2 聚合报告 PP2-M3 处置第 6 条原文 (`.aria/audit-reports/post_planning-R2-2026-09-15T180659-081Z-handoff-multibranch-subdir-path-fidelity-aggregated.md:118`): 「**TASK-031 开 PR 前**: 主仓 `git status --porcelain` 为空, 且 `git ls-files` 列出本次 `aria-plugin-benchmarks/ab-results/<目录>/` 与 `verification-ledger.md`。」—— 这是五席收敛、主控核对后写入 R2 聚合报告的处置, 已进入换执笔人的 R3 rework 依据。
- 当前 (v3.1) `detailed-tasks.yaml:837` 的 TASK-031 对应条款已改写为: 「开 PR 前 (**提交面, 有范围的检查**; 健康常态下主仓本就可能有他轨或其它审计的未跟踪文件, 故**不要求整体为空**): ... 其中不得有任何一行触及本 cycle 交付物路径 —— (白名单列举) ...; **其余每一行逐条在台账写明归属并判定与本 cycle 无关**」。
- 本轮任务简报明确告知: 这条改动是「主控核验 v3」时发现「TASK-031 的主仓干净工作树判据不可满足」后, 在 v3.1 返修阶段做出的。yaml:19 的 `metadata.updated` 字段也承认这一点: 「v3.1: 主控核验返修 ((j3) 谓词 fail-closed / **TASK-031 有范围提交面核验** / TASK-029 与 TASK-034 回退命令写死 / 验证脚本不依赖 assert)」。
- 但 `tasks.md:35-56`「AI 流程判断清单」(Rule #10 §5 指定的、经 `TASK-032` 全文照录进周期 handoff 的唯一披露渠道) 18 条逐条核对, **没有任何一条提及 TASK-031 的这次标准变更**; 第 12 条 (tasks.md:50) 只披露了 `(j3)` 谓词的 v3.1 修复, 未提及另外 3 项 v3.1 改动 (TASK-031 有范围检查 / TASK-029·TASK-034 回退命令写死 / 验证脚本不依赖 assert)。

照计划执行会出的错: TASK-032 (parent 5.4) 的核验明写「周期 handoff 含...tasks.md『AI 流程判断清单』全文照录并追加 Phase B/C/D 新增项」——「追加」只覆盖 B/C/D 阶段**新产生**的判断, 不会倒查 A.2/A.3 阶段是否有遗漏项。清单本身缺项 ⇒ 全文照录时缺项原样传导进周期 handoff ⇒ owner 复议时看不到「一个已经五席收敛的验收标准 (干净工作树) 被放宽为『不要求整体为空、只需逐行归属』」这一改动, 失去了 Rule #10 §5 要求的「AI 自作主张的流程判断必须写进 handoff 请复议」的实际效果。三处技术性更强的修复 (TASK-029/034 回退命令写死、脚本不依赖 assert) 本身不放宽任何验收义务 (只是让已有要求更稳固), 披露必要性低于 TASK-031 这一条, 但同样未被清单覆盖, 一并计入本条以求完整。

建议改法: 在「AI 流程判断清单」补一条 (比照现有条目格式, 例如插入为第 19 条或并入第 12 条同级): 「TASK-031 干净工作树判据放宽: v3 原文照 R2 处置写『主仓 `git status --porcelain` 为空』, 主控核验发现健康常态下主仓可能存在他轨/其它审计的未跟踪文件, 该判据不可满足, 改为『不得含本 cycle 交付物路径 + 其余行逐条记台账归属判定』; 理由: 保留了『本 cycle 自身遗留物必须清空』的核心意图, 放弃的只是『全局清空』这个在多轨并发仓库中不可达的更强形式。」并顺带在同条或另一条里提一句 TASK-029/034 回退命令写死与脚本去 assert 两项 (哪怕只是一句带过), 使 v3.1 的 4 处返修在清单里可查全。

---

**[Minor] type=issue · category=testing · scope=detailed-tasks.yaml PRED["j4"] (`sc11-predicate-validation.py:204` 同式) · v3 引入: 否 (v1 起即无左边界, 本轮未修)**

证据: `PRED["j4"]` (yaml:88, 脚本:204) 为 `` ! { ... } | grep -qiE 'four[- ]levels?|4[- ]levels?|四级|四层' ``。`4[- ]levels?` 左侧没有 `\b` 或等价边界, 理论上会把任意「以数字 4 结尾且紧跟连字符/空格 + level(s)」的子串误判为命中 (例如某个巧合的版本号或行号紧邻 "level" 一词)。

照计划执行会出的错: 目前不会 —— 本席对当前基线三个扫描文件 (`grep -inE '4[- ]levels?' ...`) 只命中 `test_handoff_multibranch_collision_dedupe.py:885`/`:1162` 两处真实待改行, 且脚本对 `target` 态实测 (j4) 全 PASS, 未见误伤。风险是潜在的 (若未来扫描面内出现巧合数字), 不是当前已暴露的缺陷。

建议改法: 顺手加 `\b` 或改用 `(?<![0-9])4[- ]levels?` 等左边界写法, 成本极低, 消除潜在假红面; 非阻塞项, 可留到下次触碰该谓词时一并做。

---

**[Minor] type=issue · category=testing · scope=detailed-tasks.yaml TASK-029 第 2/4 步 (yaml:769-771) · v3 引入: 否 (v1 已有此步序, v3.1 只改了回退命令写死, 未动步序)**

证据: TASK-029 第 2 步 (`git -C aria checkout master ...`) 先于第 4 步 (`git -C aria status --porcelain` 为空的断言) 执行 (yaml:769, 771)。

照计划执行会出的错: 正常路径下不会 —— TASK-021 (yaml:585) 已在组 4 收尾前断言两个子模块工作树干净, TASK-029 之前没有任何任务会在 aria/standards feature 分支上产生未提交改动, 所以第 2 步执行时工作树预期本就是干净的; 若确实脏, `git checkout` 在文件冲突时会直接报错拒绝切换 (安全失败), 不会静默把未提交改动带到 master 上。真正的风险场景 (未提交改动恰好不与 master/feature 分支任何被跟踪文件冲突, 被 checkout 静默带过) 概率低且当前设计的上游保证 (TASK-021) 已覆盖。

建议改法: 出于纵深防御, 可在第 2 步之前插入一次显式 `status --porcelain` 断言 (而不是仅在第 4 步), 使"先检查后切分支"的顺序对任何未来读者都直观, 不必依赖"上游任务已经保证过"这一隐含前提。非阻塞。

### 核对无误的部分 (不计 finding)

1. 19 条 `sc11_baseline_predicates` 与脚本 `PRED` 逐字比对一致 (本席用文本比较, 未见字符级差异); 13 态 × 19 谓词矩阵经本席独立实跑, 与 yaml `measured_2026_09_15_at_1cb3872_v3_1` 逐字节一致。
2. `python3 -B` 与 `python3 -OO` 两种解释器优化级别下脚本输出逐字节相同, 验证"不依赖 assert"声明成立。
3. 谓词 (a1)/(b) 经对抗构造 (字段填错块) 实测仍正确拒绝, 不依赖专门验证态也具备鉴别力。
4. (j5) 谓词的"命中行或下一行含 rel_path"窗口设计, 经与真实文件 (`handoff_multibranch.py` 的 6 处 `dictionary-max` 命中行) 逐行核对, 覆盖全部 6 处且与 TASK-020 的编辑点 (j5a-d) 一一对应, 未发现漏检窗口。
5. 依赖图 (35 任务) 无环、无悬空引用; `parent` 去重后 27 个与 tasks.md 27 个 checkbox 一一对应; `total_tasks`/`est_hours_total` 与实际求和一致。
6. SC ↔ 任务映射表 (tasks.md:133-155) 与 yaml `sc11_baseline_predicates` 归属注释 (yaml:72-74) 逐条核对一致, 包括 (j4) 横跨 4.1/4.2 与 (l3) 归 4.4 等边界情形。
7. TASK-035 的六个补丁与 proposal SC-1/3/4/5/8/14/17 原文「反事实」列逐条核对: 补丁 1/2/4/6 是原句直译, 补丁 3/5 是「AI 流程判断清单」第 18 条已披露的合理偏离 (revert 全枚举层会导致 git show 直接失败、首个失败断言落错位置, 只 revert 目标组件才能让失败落在原句所指断言上), 理由站得住, 且与 SC-4/SC-8/proposal 原文的技术因果链吻合。
8. TASK-015 (SC-6) 的两条反事实与 proposal SC-6 原文「反事实」列逐字对应 (退回 basename ⇒ 空 SHA 断言红; `:180` 局部变量重指 `rel_path` ⇒ `inconclusive[0]["filename"]` 带目录段断言红)。
9. AB 相关引用 (`no_push_requested_by_env`、`ab-results/2026-09-05-.../RESULT.md §1.2/§4`、`SCORES.md` 的 `-rep2`/`-rep3` 先例、`AB_TEST_OPERATIONS.md:219/222-235`) 均核实真实存在, 内容与 TASK-026/rule6_note 的转述吻合, 非杜撰引用。
10. PP2-M1/M2/M7/M8/M9 与 m8/m9/m14/m15/m16 的处置在本席侧重范围内逐条核实已落地 (见上表), 未发现"聚合表说已接受、正文未改"的断链。
11. 组 5 标题的执行序描述 (tasks.md:122) 与实际依赖图逐段核对一致 (TASK-025/026 互不依赖且均先于 TASK-027; 027→028→029→034→030→031→032 单链), 清单第 16 条披露的 R1 遗留裁决在当前文本里落地无误。

## Verdict

PASS_WITH_WARNINGS (0 Critical / 1 Major / 2 minor)

## Vote

REVISE

## 轮次记录

本席为 R3 convergence 模式新派席位, 未参与 R1/R2; 聚焦「验证判据与证据链」维度对 v3.1 (`2b9cb3e`) 做独立核验, 逐条核对 R2 聚合报告在本侧重范围内的九个 Major 簇与相关 Minor 是否落地 (均已落地), 并用真实实跑 (完整 13×19 矩阵重跑、`-OO` 等价性、对抗构造 "字段填错块"、依赖图无环性、AB 引用真实性五类) 取代纯阅读式核验; 发现主控在 v3 之上又做的 v3.1 返修 (4 处) 中有 3 处未经「AI 流程判断清单」披露, 其中 TASK-031 一处涉及放宽此前五席收敛的验收标准, 定为本轮 Major; 另发现两处低风险 Minor (谓词正则缺左边界、TASK-029 步序可加纵深防御), 均为既有设计的边际加固建议, 非 v3.1 新引入的缺陷。未发现 Critical。
