---
verdict: REVISE
agent: qa-engineer
round: R1
critical_count: 1
major_count: 2
minor_count: 3
---

# post_spec R1 审计 — session-closer-autofill-yaml-datasource (qa-engineer 视角)

审计对象: `/home/dev/Aria/openspec/changes/session-closer-autofill-yaml-datasource/proposal.md`
逐行核对: `handoff_autofill.py` (L160-175, L223-238) / `test_handoff_autofill.py` / `state-scanner/scripts/lib/detailed_tasks.py` (L225-273, `parse_detailed_tasks`) / `skill-benchmark-exemption.md` / `.aria/triage-report.json`。

---

## Critical

### C-1 — SC 集合遗漏 `parse_ok=False`(含结构自洽性失败/空 tasks 块)分支, 会以「格式损坏的 yaml」这条新触发路径复刻本 issue 要修的同一病根 (静默 0)

**位置**: proposal §What 第 2 点(yaml 分支) + Success Criteria SC-1~SC-5。

**主张**: `parse_detailed_tasks(text)` 在**文件级**有 4 种 `parse_ok=False` 归零场景(`detailed_tasks.py` L233-260): 无 `tasks:` 顶层块、`tasks:` 块下零 `- id:` 条目、重复顶层 `tasks:` 键、`base_indent` 直接子项数与 `- id:` 匹配数不一致(结构自洽性失败)。这四种情况下 `result["tasks"] == []`。

proposal §What 第 2 点只写「`parse_detailed_tasks(text)` 逐 task 取 `{id, raw_status, title}`」, **未提及要先检查 `parse_ok`**。若实现照字面对 `result["tasks"]` 直接遍历, 那么一份**存在但畸形**的 `detailed-tasks.yaml`(如 owner 手改产生重复 `tasks:` 键, 或 A.3 期文件被截断)会静默产出 **0 条**未完成项 —— 与触发本 issue 的「`tasks.md` 缺席 ⇒ 静默 0」是**同一形态的假绿**, 只是换了触发条件。

decision 4(「降级方向: 宁噪音勿假绿」)明确把这条哲学用在**跨 skill 导入失败**上(sentinel item), 但没有对称地覆盖**同一解析器返回的文件级失败**(`parse_ok=False`)。两者在「消费方看到 0 条时无法分辨『真的 0』还是『机制失效』」这一点上是同类风险, 但只有一个被 decision 4 + SC-5 处理。

SC-1~SC-5 没有任何一条构造过「detailed-tasks.yaml 存在但 `parse_ok=False`」的 fixture(如重复 `tasks:` 键、`- id:` 缺失、缩进错位导致自洽性检查失败)。这意味着即便实现真的漏判 `parse_ok`, 现有 SC 集合也**抓不到**。

**建议**: 补一条 SC(如 SC-5b): yaml 存在但 `parse_detailed_tasks(text)["parse_ok"] is False` → 产 sentinel item(与 decision 4 同款「解析不可用, 需人工核对」措辞, 而非静默 0), 并要求实现显式检查 `parse_ok` 而非只信任 `tasks` 列表的真值。

---

## Major

### M-1 — yaml 文件本身的 `open()`/`read()` I/O 失败(如权限错误、TOCTOU 竞态)路径未在 proposal 中定义, 现有 `tasks.md` 分支的「静默 continue」先例若被复用会与 decision 4 的哲学自相矛盾

**位置**: `handoff_autofill.py` L167-172(现行 `tasks.md` 分支的 `try/except OSError: continue`); proposal §What 第 2/4 点。

**主张**: 现行 `tasks.md` 分支对 `open()` 失败是**静默 continue**(不产任何 item, 也不产 warning)。proposal 只讲了 yaml 分支的「解析」步骤和「跨 skill 导入失败」的降级, 没有说 yaml 文件读取本身失败(如 `os.path.isfile` 通过之后, `open()` 因权限 / 竞态删除而抛 `OSError`)该走哪条路径。

若实现直接照抄 `tasks.md` 分支的 `try/except OSError: continue` 惯例, 会产生「yaml-only spec 因读取失败静默报 0」—— 这与 decision 4 明确写的「跨 skill 导入失败时**不**静默回 0」的降级方向不一致: 两种失败(导入失败 vs 文件读取失败)对使用者而言都是「本该有数据但拿不到」, 只有一种被设计为可见降级。

**建议**: proposal 应显式裁定 yaml 读取 `OSError` 的降级方向(建议与 decision 4 同款: 产 sentinel 而非静默 continue), 并补一条 SC 覆盖它, 否则实现者大概率会复用旁边最近的 `tasks.md` 惯例(继续静默), 制造第三条静默假绿路径。

### M-2 — SC-5「模拟跨 skill 导入失败」面临 Python `sys.modules` 缓存, 若不显式处理会使该测试退化为「看似跑了失败路径, 实际仍走了成功路径」的假绿测试

**位置**: proposal §What 第 3/5 点(lazy import, sys.path 插入 `state-scanner/scripts/lib`); Success Criteria SC-5; `test_handoff_autofill.py` 的既有测试类布局(同文件已有多个 TestCase, 均在同一进程 `python3 test_handoff_autofill.py` 内顺序执行)。

**主张**: decision 5 明确这是 **lazy import**(仅 yaml-only spec 命中时触发), 且 decision 3 明确用**裸模块名** `from detailed_tasks import parse_detailed_tasks, is_done_status`。Python 的 import machinery 会把裸模块名以 `detailed_tasks` 为 key 缓存进 `sys.modules`。

如果 SC-1(yaml-only 正常 fixture)先于 SC-5(模拟导入失败)执行 —— 而 unittest 默认按方法名字母序在同一进程内跑, 无法保证 SC-5 排在 SC-1 之前 —— 那么当 SC-1 触发一次成功的 `from detailed_tasks import ...` 之后, `sys.modules['detailed_tasks']` 已被填充。SC-5 若只是通过临时改 `sys.path`(移除 `state-scanner/scripts/lib` 或指向一个不存在的路径)来「模拟导入失败」, 这个手法对**已缓存的模块名**无效 —— Python 优先命中 `sys.modules` 缓存, 根本不会重新触发路径解析, 导入依然成功, SC-5 测的「导入失败降级」分支实际上从未被执行, 而断言(若只断言「产出了 sentinel」)可能因为函数实现里另有一条基于 `changes_dir` 内容构造的分支而侥幸通过, 也可能直接不通过——但无论哪种, 测试没有真正覆盖它声称覆盖的失败路径, 这正是 baseline-failing 可证伪性设计要防的「看似测了实际没测到」。

proposal 的「fixture 用独立 tempdir」(SC 末尾一条)只处理了**文件系统**隔离, 没有处理**import 缓存**隔离 —— 这是两个不同维度的隔离要求, 后者未被点名。

**建议**: SC-5 的实现指引应显式要求 `del sys.modules['detailed_tasks']`(以及可能的 `is_done_status`/`parse_detailed_tasks` 绑定名)或改用 `unittest.mock.patch` 在**函数调用点**打断导入(如 patch 掉触发 lazy import 的内部 helper, 而非只操纵 `sys.path`), 并在 spec 里对「为什么单纯改 `sys.path` 不足以模拟导入失败」留一句 rule6_note 级别的落地说明, 否则这条 SC 很可能被写成一条「形式上存在、实际上是空判定」的测试。

---

## Minor

### m-1 — 「两文件都缺席」状态未被 SC 显式覆盖(低风险, 但 SC-2~SC-5 未构成对状态空间的完整划分证明)

**位置**: proposal §What 第 1 点(仅描述 tasks.md 存在 / tasks.md 缺席+yaml 存在两种); Success Criteria SC-2~SC-5。

**主张**: 状态空间是 `{tasks.md 存在/缺席} × {yaml 存在/缺席/畸形}`。proposal 只显式定义了「tasks.md 存在」(现行为不变)和「tasks.md 缺席 + yaml 存在」(新分支)两支, 「两者都缺席」这一格没有对应的 SC(虽由现有 `if os.path.isfile(tasks): ... elif os.path.isfile(yaml_path): ...` 结构可以推出是安全的 0 结果, 但没有测试钉死这个推断)。按 memory `feedback_predicate_tiers_need_total_partition_proof` 的谓词分档要求(拆 N 档必须证全分割), 这属于遗留的未证空隙, 优先级低于 C-1/M-1(那两个是真实误报风险), 但仍值得补一条零成本的负控测试。

### m-2 — decision 2 的 `item` 输出契约 `"<id> <title>"` 在 `title` 缺失/空值时的具体形态未测试

**位置**: proposal §What 第 2 点; `detailed_tasks.py::_extract_block_title` (L191-195, 字段缺失返回 `""`)。

**主张**: 若某 yaml task 条目没有 `title:` 字段, `_extract_block_title` 返回 `""`, 那么按字面拼接 `"<id> <title>"` 会产出带尾随空格的 `"TASK-001 "`(或视实现是否 `.strip()` 而定)。这只是显示层面的瑕疵(item 是自由展示串, 不影响下游逻辑), 不影响正确性判断, 但 decision 2 既然明确写了输出格式契约, 就应该有一条 fixture 覆盖「title 缺失」这个边界, 否则该契约的这个角落没有可证伪保障。

### m-3 — 同一 yaml 内 done/pending 混合的组合态未被任何 SC 单独覆盖

**位置**: Success Criteria SC-1(全 pending)/ SC-3(全 done)。

**主张**: SC-1 与 SC-3 各自用「全 pending」「全 done」的单一状态 fixture, 没有一条混合(如 3 个 task 中 1 个 done、2 个 pending)的 fixture。由于 `grep_unchecked_tasks` 对每个 task 是逐条独立判定(`not is_done_status(raw_status)`), 混合态在实现层面风险很低(不存在会因为「混合」而改变行为的聚合逻辑), 因此只标 Minor —— 但既然 SC-4 已经在谈「fail-CLOSED」这个精确性主张, 一条混合态回归测试能以近零成本把「精确到每条」这件事钉死, 而不是靠「全 pending」和「全 done」两个极端态旁证。

---

## 已核对、未发现问题的部分(供收敛判断参考)

- **SC-1 baseline-failing 设计本体**: Tasks 1.2 明确「先写 SC-1 验证 baseline FAIL, 再实现」, 与 rule6_note 声明的 substitute 要求(SOT `skill-benchmark-exemption.md` §2 第一行「deterministic substitute: SC 级 baseline-failing 结构化测试, 必须在场」)吻合。此为 spec 阶段设计意图审查, 实现是否真做到需留到 pre_merge 用 git 历史核验(worked example 精神: 回退改动应使 SC-1 转红)。
- **rule6_note 判据本身**: `handoff_autofill.py` 是纯 Python 函数变更, 不碰 `SKILL.md`/`description`, 对照 SOT §5 worked examples 表「纯代码层」→ substitute 的既有裁定先例(`state-scanner-stale-refs-false-parity` v1.59.0/v1.60.0), 归类一致, 无异议。
- **`lib` 顶层名绑定毒化规避设计(decision 3)**: 逐行核对 `owner_container()`(L305-326)确实把 `state-scanner`(skill 根)插入 `sys.path` 以解析 `from lib.identity import ...`, 这会把顶层名 `lib` 绑定到 `state-scanner/lib`(Layer L 包, 非 `state-scanner/scripts/lib`)。decision 3 采用插入 `state-scanner/scripts/lib` + 裸模块名 `from detailed_tasks import ...` 的方案确实避开了这个绑定冲突(不经过 `lib.` 前缀), 设计正确, 与 memory `feedback_state_scanner_dual_lib_package_shadow.md` 描述的坑位吻合。
- **SC-2 并存优先级(防双报)**: `grep_unchecked_tasks` 现行结构是 `if os.path.isfile(tasks): ...` 单分支, 按 decision 1「tasks.md 存在 ⇒ yaml 不看」若实现为 `if/elif` 结构即可天然满足, SC-2 断言到位。
- **下游 `assemble_unfinished` 零改动兼容(decision 2 「新前缀零改动兼容」)**: 逐行核对 L223-238, `unchecked_tasks` 是被 `out.extend(unchecked_tasks or [])` 直接拼接的, 对 `source` 字符串内容零依赖, 新前缀 `detailed-tasks.yaml:{name}` 不需要下游改动, 断言成立。
- **SC-6 双侧回归**: 与 memory `feedback_test_runner_scope_blind_to_cross_skill_consumers` 的坑位吻合(single-skill runner 结构上看不见跨 skill 消费方), SC-6 显式要求两边都跑, 设计正确; 但其充分性受 M-2(sys.modules 缓存)影响 —— 「两边测试绿」不能保证 SC-5 真正测到了它声称测的场景, 这是 SC-6 本身覆盖不到的更深一层问题。
- **fixture 隔离(tempdir)**: Success Criteria 末条显式要求独立 tempdir, 与 memory `feedback_test_worktree_fixture_isolated_tmpdir` 吻合, 但如 M-2 所述, 这只覆盖了文件系统维度, 未覆盖 import 缓存维度。
- **`_UNCHECKED_RE` 对 `- [x]` 的处理对称性**: 该正则本身不在本次改动范围内(proposal 未触碰 `tasks.md` 分支代码), 现有测试 `test_grep_unchecked_tasks` 已验证 `- [x]` 被正确排除, 非本次变更引入的风险, 不构成新 finding。

---

## Verdict 依据

存在 1 条 Critical(C-1: `parse_ok=False` 分支缺失会以新触发条件复刻本 issue 的病根形态, 且现有 SC 集合结构上抓不到)+ 2 条 Major(M-1 yaml 读取 I/O 失败降级方向未定义; M-2 SC-5 的「模拟导入失败」手法存在 `sys.modules` 缓存导致假绿的具体风险), 判定 **REVISE**。
