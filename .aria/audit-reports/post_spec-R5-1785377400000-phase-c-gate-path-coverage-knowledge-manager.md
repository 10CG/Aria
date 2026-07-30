# post_spec R5 (定向) — knowledge-manager

**verdict**: REVISE
**scope_ok**: true
**counts**: critical=0 major=2 minor=1

## 指针核实表

| 声称 | 位置 | 实测命令 | 结果 | 判定 |
|------|------|---------|------|------|
| 裸名 `phase-c-integrator` 命中 parent 套件, 内容=3 个 LLM eval | :159 | `find . -iname "phase-c-integrator.json"`; `python3 -c "json.load(...)"` 读 `evals[].name` | 文件存在, 3 个 eval 名精确为 `commit-generation`/`merge-conflict-handling`/`multi-remote-merge-push`; 子套件 json 自带 `parent_skill: "phase-c-integrator"` 字段自证层级关系 | 匹配 |
| `AB_TEST_OPERATIONS.md` §场景1 的解析流程真会做裸名替换 | :159 | `Read AB_TEST_OPERATIONS.md:198-221` | 步骤1原文 "读取 `{skill}/evals/evals.json` (或 `ab-suite/{skill}.json`)" — `{skill}`=裸名代入即产出 `ab-suite/phase-c-integrator.json`, 机制描述准确 | 匹配 |
| `latest` symlink 解析到 state-scanner 归档 | :160 | `ls -la aria-plugin-benchmarks/ab-results/` | `latest -> 2026-05-13-state-scanner-issue-101-fix` | 匹配 |
| 「最近一次归档」(chronological) 也解析到 state-scanner | :160 | `ls -d ab-results/*/ \| sort \| tail`; 对最新目录 `2026-07-20-v1.62.0-phase4-rule6` 读 `benchmark.json.skill_name` | 目录名含 "phase4-rule6" 具误导性, 但 `benchmark.json` 内 `skill_name` 字段实为 `"state-scanner"` — 两条路径 (symlink / chronological-latest) 均真落 state-scanner | 匹配 (经内容级复核, 非仅目录名) |
| 基线文件 `ab-results/2026-05-10-phase-c-integrator-pre-merge-gate/benchmark.json` 存在 | :160 | `find`; `python3 json.load` | 存在, 6546→实际字段完整可解析 | 匹配 |
| `structural_metrics.*.measured` 是 `int`(8个), `primary_pass_gate.measured` 是 `str "100%"` | :161 | 同上, dump 全字段 | 8 个指标 `measured: 100` (int) + `unit: "percent"` 独立存放; `primary_pass_gate.measured == "100%"` (str) | 精确匹配 |
| `phase-c-integrator-pre-merge-gate.json` 含 6 fixtures | :153 | `python3 json.load` 该文件 | `fixtures`: list len=6, `fixtures_dir` 字段present, 与基线 `benchmark.json.fixtures.total=6` (4 happy+2 negative) 互证 | 匹配 |
| **AB 勘正表整体 "L 侧 R2 5/5 席实地核实"** (:155 header) | :155/159-161 | grep L 侧 `post_spec-R2` 聚合报告 N-δ 簇 + `post_planning-R2` 聚合报告 | N-δ (post_spec-R2, **5/5** critical) 只含 (a)五维得分[R未用此术语,不适用] (b)latest/最近一次归档→state-scanner (c)裸名→parent套件 —— **不含** measured int/str 项; 该项实际首见于 `post_planning-R2` line 46 "R2-E" 由**单席 cr** 提出 (major, 非 5/5) | **不匹配 (见 Finding 1)** |
| D12(位置式判据)/SC-30 引「L 侧 R4 实跑 3/4 语料命中」 | :64 | grep L 侧 `post_spec-R4` 聚合报告 | R4-B: `1/2 (实跑)`, major, 子串读法 4 份语料命中 3 份, 与位置式改法(AC-5b 第三条负控 `paths:['a/**']`)逐字对应 SC-30(iii) | 匹配 (措辞未夸大为多席共识, 如实写"实跑") |
| D13(`---`语义)/SC-31 引「L 侧 R4 实跑」 | :66 | 同上 | R4-C: `1/2 (实跑)`, major, "列0且在on:块之前"永远满足→首行`---`仓恒wait, AC-7b不钉真值→零AC会红 | 匹配 |
| memory `feedback_spec_underdetermination_two_implementer_test` 存在 | :64 | `ls`+`Read` memory 文件 | 存在, 内容="两个独立实现者同段文本得相反结果=欠定实证"(#113 R4, 16/16 vs 11/17) — 本处应用是该通用判据的**类比引用**(非literal两实现分叉案例), 但不构成误用 | 匹配(从宽) |
| `openspec/changes/phase-c-integrator-ci-path-coverage/MERGE-ANALYSIS.md` 存在且内容对得上 | :4 | `Read` 全文 | 存在(11722 bytes); 文件头已自行更新为 "✅ 已裁决(owner, 2026-07-30): 以R为准" 并点名 "L-6/L-7 未并入", 与 A1 文字逐句吻合; §3 L-6/L-7 行原文与 A1 转述一致 | 匹配 |
| Impact 表已声明 "fixture 用独立 tempdir 非 repo.parent" (QA-13) | :224, :255 | `Read` proposal.md:224 | 原文原样存在 | 匹配(文本本身存在) |
| 该处引用 memory `feedback_test_worktree_fixture_isolated_tmpdir` 存在 | :224, :255 | 精确路径 `ls`; 全目录 `ls`; 全量 `grep -rli "tempdir\|isolated\|repo\.parent"` 遍历 `memory/*.md` | **不存在**(0 命中,含文件名与全文内容两种检索)。真实precedent 在代码: `aria/skills/state-scanner/tests/test_handoff_worktrees.py:9,36` + `test_git_operation_detection.py:92`, 引用 "#135 $TMPDIR-leak lesson"(issue,非memory) | **不匹配 (见 Finding 2)** |
| §6 SKILL.md 同步清单是否因 D12/D13/D14 + SC-29~32 需扩项 | :109-123 vs 现状 SKILL.md | `Read` `aria/skills/phase-c-integrator/SKILL.md` 全 8 处既有落点行号(:39-53/:176/:241-245/:246-249/:258-270/:272-281/:283-289)逐一核对现状**行号仍对齐**; `grep "ab-suite\|benchmark\|Rule #6"` SKILL.md → 0 命中 | D12-14 与既有 D5-D7(同为 parser 内部构造级细节)同属"2.5 Path coverage 评估"笼统桶, 无任何既有决策(D5-D11)单独占一条 §6 行, 一致对待即非缺口; L-5/SC-32(AB 套件) SKILL.md 现状**零** AB 相关内容, 该类内容从不同步进 SKILL.md(住在 AB_TEST_OPERATIONS.md+rule6_note) | 无缺口(经论证, 非橡皮图章) |
| Impact 表测试基线 "62→预计~110+(A1后~120+)" 依据 | :234 | grep 全部 13 份 R1-R4 审计报告 `"62\b"` `"110\b"` | "62"=25+37 有据(R1 code-reviewer 报告逐字确认); "**110**" 在全部13份报告中**零命中**,4轮/13席审计均未核算或质疑过 | **依据缺失 (见 Finding 3)** |
| SC-32 (AB 结构化断言) 是否计入 "phase-c" 测试基线 & 受 `run_all_tests.sh` 覆盖 | :226,:234 | `Read` `aria/skills/run_all_tests.sh:1-30` | `SKILLS_DIR="skills"` — 只扫 `aria/skills/*/tests/`; SC-32 落点 `aria-plugin-benchmarks/`(仓根同级目录, 非 `aria/skills/` 子树)**结构性在扫描范围外**, 却被 :234 一句话与 SC-29~31 一起计入 "phase-c...~120+" 并挂 `run_all_tests.sh` 收口 | 范围混淆 (并入 Finding 3) |
| L-7 (`paths-ignore` 极性) "本 Spec §1 原文即...covered" | :256 | `Read` proposal.md:62 | 原文: "`paths-ignore` 在场 / anchors / 其他无法辨识的构造级内容 → 该 workflow 记 `covered`" | 匹配 |

## Findings

### [MAJOR] AB 勘正表第3行的证据强度被表头 "L 侧 R2 5/5 席实地核实" 不当抬高
- **位置**: openspec/changes/phase-c-gate-path-coverage-not-applicable/proposal.md:155 (表头) 与 :161 (第3行)
- **问题**: :155 表头一句话统摄下方三行, 声称三条勘正均来自 "L 侧 R2 5/5 席实地核实"。经查 L 的 `post_spec-R2` 聚合报告, N-δ 簇确为 5/5 critical, 但其三个子项 (a)「五维得分」字段不存在 (b) latest/最近一次归档→state-scanner (c) 裸名→parent 套件, **不包含** "`structural_metrics.*.measured` 是 int 不是 str" 这一项。该项实际首见于**另一个检查点** `post_planning-R2`(任务规划审计, 非 Spec 审计) line 46「R2-E」, 由**单席** code-reviewer 提出, 定性为 major(非 critical), 且该发现原文关注点是"分母不敏感"(verification 对分母被改不变色), 与 A1 表述的"写成字符串产生恒假断言"是相邻但不同的技术点。表头把 post_spec 阶段的 5/5 强共识, 平移套用到一个实际是 post_planning 阶段单席核验的结论上, 抬高了第3行的证据等级。
- **证据**:
  ```
  $ grep -n "structural_metrics\|primary_pass_gate\|measured" .aria/audit-reports/post_spec-R2-1784996000000-phase-c-integrator-ci-path-coverage-aggregated.md
  (无匹配)

  $ grep -n "五维得分\|latest symlink\|裸名" .aria/audit-reports/post_spec-R2-1784996000000-phase-c-integrator-ci-path-coverage-aggregated.md
  61:| **N-δ** AC-9 判据引用不存在的字段 + 验证错对象 | critical | **5/5** | (a)「五维得分」... (b)「最近一次归档」/`latest` symlink 解析到 **state-scanner**; (c) 裸名 `phase-c-integrator` 按手册流程命中无关 parent 套件...

  $ grep -n "structural_metrics\|measured" .aria/audit-reports/post_planning-R2-1785013000000-phase-c-integrator-ci-path-coverage-aggregated.md
  46:| **R2-E** TASK-022 verification[0] 打在自己碰不到的产物上 ⇒ 结构性恒绿 | major | cr | `structural_metrics` 根本不在 suite JSON 里(只在 ab-results 归档的 benchmark.json)。而 TASK-023 的「8 个 measured 保持 100」对分母变化天然不敏感...
  ```
- **建议修法**: 拆分 :155 表头的笼统归因 — 明确写"1/2 项来自 L 侧 post_spec-R2 5/5 席 critical 共识 (N-δ); 第3项(measured 类型)经 L 侧 post_planning-R2 code-reviewer 单席核验, 本轮(R5)对基线文件独立复核确认属实"。第3行的**结论本身**(经本轮 R5 对 `ab-results/2026-05-10-.../benchmark.json` 的独立读取) 是真的, 只需订正来源标注, 不必推翻。

### [MAJOR] 两处引用的 memory `feedback_test_worktree_fixture_isolated_tmpdir` 在 memory 库中不存在
- **位置**: openspec/changes/phase-c-gate-path-coverage-not-applicable/proposal.md:224 (Impact 表) 与 :255 (§修订记录 A1「未并入」段, 用于论证 L-6 不需并入)
- **问题**: 两处均引用 `memory feedback_test_worktree_fixture_isolated_tmpdir` 作为 "fixture 用独立 tempdir 非 repo.parent" 这一设计已有先例的证据。经对 `/home/dev/.claude/projects/-home-dev-Aria/memory/` 做精确文件名核对、全目录列表扫描、以及跨全部 ~150 份 `feedback_*.md`/`reference_*.md`/`project_*.md` 文件内容的 `tempdir`/`tmp_path`/`isolated`/`repo.parent`/`repo_parent` 全文检索, **零命中**——不存在这个 memory, 也不存在任何命名不同但内容匹配的等价 memory。真实的技术先例存在于**代码**而非 memory: `aria/skills/state-scanner/tests/test_handoff_worktrees.py:9,36` 与 `test_git_operation_detection.py:92` 的注释明确写着 "isolated tempdir (NOT repo.parent) per the **#135** $TMPDIR-leak lesson" —— 这是一个 issue 号 (#135), 不是 memory 文件。该情形正是本项目 memory `feedback_cross_doc_claim_verify_at_target.md` 点名警告的模式("文档 A 写「已在 B 做了 X」必去 B 实测")。由于此引用是论证"L-6 (一个有 L 侧 R2 3席支持的真实发现) 不需要并入本 Spec"这一决策的关键依据之一, 引用失真会削弱该决策的可审计性——即便"独立 tempdir"这个工程方案本身大概率是对的(有代码先例佐证), 但"已有 memory 记录此教训"这个具体断言是假的。
- **证据**:
  ```
  $ ls "/home/dev/.claude/projects/-home-dev-Aria/memory/feedback_test_worktree_fixture_isolated_tmpdir.md"
  ls: cannot access ...: No such file or directory

  $ grep -rli "tempdir\|tmp_path\|isolated" /home/dev/.claude/projects/-home-dev-Aria/memory/*.md
  (无匹配)

  $ grep -rn "repo\.parent\|repo_parent" /home/dev/Aria/aria/skills/phase-c-integrator/ /home/dev/.claude/projects/-home-dev-Aria/memory/*.md
  aria/skills/state-scanner/tests/test_handoff_worktrees.py:9:inside ONE isolated tempdir (NOT repo.parent) per the #135 $TMPDIR-leak lesson.
  aria/skills/state-scanner/tests/test_handoff_worktrees.py:36:    isolated tempdir (#135: never repo.parent). add_worktree(name, None) makes
  aria/skills/state-scanner/tests/test_git_operation_detection.py:92:        # Worktree path lives in its OWN tempdir (NOT repo.parent, which resolves
  (memory 目录内 0 命中)
  ```
- **建议修法**: 将 :224 与 :255 的引用从虚构的 `memory feedback_test_worktree_fixture_isolated_tmpdir` 改为指向真实先例——即 `aria/skills/state-scanner/tests/test_handoff_worktrees.py` 的 "#135 $TMPDIR-leak lesson" 注释(issue 号, 非 memory)。若 knowledge-manager 认为这条教训值得沉淀为可复用 memory(该模式确实通用, 值得被未来 Spec 引用), 应在 Phase D 或本轮之后另行创建对应 `feedback_*.md`, 而不是在 Spec 正文里提前引用一个尚不存在的文件名。

### [MINOR] Impact 表测试基线 "~110+ / ~120+" 缺乏可核实依据, 且 SC-32 的口径与 `run_all_tests.sh` 覆盖范围不一致
- **位置**: openspec/changes/phase-c-gate-path-coverage-not-applicable/proposal.md:234
- **问题**: "测试基线: phase-c 62 → 预计 ~110+ (A1 后 **~120+**, 新增 SC-29~32)" 一句中, 起点 "62" 有据可查(R1 code-reviewer 报告确认 = 25+37, 对应既有 GateCheckTests/FallbackTests), 但 "~110+" 这个中间估算数字在 post_spec R1-R4 全部 13 份审计报告中**从未出现**, 说明这个数字自始至终未被任何一轮审计核算或挑战过, 纯属沿用的未注明依据估算。A1 在此基础上再加 "~120+"(为 SC-29~32 四条新增验收标准), 同样未给出加总依据。此外, 该句把 **SC-32** 一并计入 "新增 SC-29~32" 的测试数增量, 但 SC-32 的验收对象在 `aria-plugin-benchmarks/`(仓根同级独立目录), 而句尾引用的收口机制 `run_all_tests.sh` 硬编码 `SKILLS_DIR="skills"`, 只扫描 `aria/skills/*/tests/` 子树, **结构性不会跑到** `aria-plugin-benchmarks/` 下的任何断言。SC-32 需要经由 Rule #6 AB 重跑流程验证(rule6_note 已正确描述), 但被这一句与"phase-c 测试基线"和"run_all_tests.sh 须绿"捆在一起表述, 造成"这个数字包含 SC-32、且 SC-32 会被 run_all_tests.sh 兜底"的误导性暗示。
- **证据**:
  ```
  $ grep -rn "110\b" .aria/audit-reports/post_spec-R{1,2,3,4}-1785112156889-phase-c-gate-path-coverage-*.md
  (13 份文件, 零命中)

  $ grep -n "62\b" .aria/audit-reports/post_spec-R1-1785112156889-phase-c-gate-path-coverage-code-reviewer.md
  13:核实通过(实码/实跑): ... 测试基线 62 (25+37, 无 exact-dict 断言, additive 新键可共存) ...

  $ sed -n '1,30p' aria/skills/run_all_tests.sh | grep SKILLS_DIR
  SKILLS_DIR="skills"
  ```
- **建议修法**: 要么去掉 "~110+/~120+" 的虚假精确性, 改为 "62 + 待 A.2 任务规划阶段按 SC-1~32 逐条排布后精确核算"(与本 Spec 当前"无任务文件"的实际状态一致); 要么保留估算但注明拆解依据(仿照 "62=25+37" 的先例逐 SC 记账)。无论哪种, 应把 SC-32 从 "phase-c 测试基线 / run_all_tests.sh 须绿" 这句中摘出, 单列一句说明其经 Rule #6 AB 重跑流程验证、不进入 `run_all_tests.sh` 扫描范围。

## 附: 已核实无缺口的问题(非 finding, 供 owner 参考)

**§6 SKILL.md 同步清单是否需为 D12/D13/D14 + SC-29~32 扩项**: 核对 `aria/skills/phase-c-integrator/SKILL.md`(现 1055 行)后判定**不需要**。理由: (1) 现状文件在 §6 列出的全部 8 处行号锚点(:39-53/:176/:241-245/:246-249/:258-270/:272-281/:283-289)与当前 SKILL.md 实际内容逐一核对仍精确对齐, 证明该清单本身指针可靠; (2) D12/D13/D14 与既有 D5-D7(同为 path_coverage.py parser 内部构造级判定细节)性质相同, 而 D5-D11 全部**没有**在 §6 单独占一行, 均被收纳进笼统的"执行流程插 2.5 Path coverage 评估"一条——按同一颗粒度对待, D12-14 不构成新缺口; (3) L-5/SC-32 涉及的 AB 套件路径/基线路径/metric 类型三项勘正, 经 `grep "ab-suite\|benchmark\|Rule #6" SKILL.md` 确认现状 SKILL.md **零处**涉及 AB 测试机制性内容(该内容历来只活在 `AB_TEST_OPERATIONS.md` 与 Spec 自身的 rule6_note 里), 故此类内容从不需要同步进 SKILL.md, A1 未同步是正确的, 不是遗漏。
