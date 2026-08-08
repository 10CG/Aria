---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-08T08:37:47.000Z
context: openspec/changes/linked-issue-normalization/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 — qa-engineer 审计报告

## 审计对象与方法

实读 `tasks.md` (94 行)、`detailed-tasks.yaml` (438 行)、`proposal.md` (280 行, 参照非重审)。对 17 条 SC → 6 个 TG-1 任务的映射逐条枚举、对 §Impact 的「≥45」下界逐条独立重算 (从 Success Criteria 表原始行, 非从 §Impact 推导句抄), 对 baseline RED/GREEN 逐条比对, 并实跑 `python3 run_tests.py` 核验 1322 基线。审计镜头 = 验收的可证伪性 (「它怎么会红?」) 与测试覆盖完整性。

## 审计结论

### 已验证一致 (无发现, 记为 decision)

1. **17 条 SC 无遗漏无重复**: SC-1/1b/2/3/4 → 1.1, SC-5/5b/5c → 1.2, SC-6/6b/10 → 1.3, SC-11/13/15/14 → 1.4, SC-9 → 1.5, SC-12 → 1.6。逐一核对 proposal §Success Criteria 表的 17 个 SC 标题, 每条恰好出现一次, 无遗漏无重复。
2. **子用例下界 45 独立重算吻合**: 逐条从 SC 表原始场景描述数(非抄 §Impact 推导句): SC-1=6(六对) / SC-1b=3(三对) / SC-2=1 / SC-3=1 / SC-4=2(两组) / SC-5=1 / SC-5b=3(三元两两) / SC-5c=1 / SC-6=5(a-e) / SC-6b=9(四对+五自配对) / SC-9=1 / SC-10=1 / SC-11=2(两配对) / SC-12=3(三类各一) / SC-13=2 / SC-14=2 / SC-15=2 → 加总 = **45**, 与 proposal §Impact 推导句、tasks.md 六项括注 (13/5/15/8/1/3=45)、detailed-tasks.yaml 六个 TASK 的 verification 内嵌算式三方均一致, 未发现偏差。
3. **baseline RED/GREEN 逐条一致**: proposal baseline 表标红 8 条 (SC-1/1b/3/4/5b/11/13/15), detailed-tasks.yaml 的 TASK-001 (RED: SC-1/1b/3/4; GREEN 负控: SC-2)、TASK-002 (RED: SC-5b; GREEN: SC-5/5c)、TASK-003 (三条全 GREEN: SC-6/6b/10)、TASK-004 (RED: SC-11/13/15; GREEN: SC-14)、TASK-005 (GREEN: SC-9) 逐条核对全部吻合, 无矛盾。SC-12 (TASK-006) 正确标注「无 baseline 行」(因 `normalize_linked_issue` Phase B 才存在), 与 proposal 表实际不含 SC-12 行一致。
4. **派生统计自洽**: 独立重数 17 个 TASK 记录的 complexity/agent 字段, S×11/M×5/L×1(≈73h) 与 agent 分摊 qa-engineer×8/knowledge-manager×5/backend-architect×4 均与文件底部汇总注释精确匹配。
5. **实测复核**: 实跑 `cd aria/skills/state-scanner/tests && python3 run_tests.py` → `Ran 1322 tests / OK`, 与 metadata.test_baseline_note 声称一致。

### 发现问题

- type: issue
  severity: major
  category: testing
  scope: detailed-tasks.yaml TASK-014 (parent 5.1); tasks.md 5.1
  summary: "Ran ≥1367" 把「子用例」(语义计数, proposal §Impact 逐条推导) 与「unittest Ran N」(测试方法计数) 当同一单位, 但两者从未被要求 1:1
  evidence: >
    detailed-tasks.yaml:341 "cd aria/skills/state-scanner/tests && python3 run_tests.py → Ran ≥1367 / OK (1322 + ≥45)"。
    run_tests.py:26-29 用 `unittest.TestLoader().discover()` + `TextTestRunner`, "Ran N tests" 统计的是
    **test 方法个数**, 非方法内部的断言/子用例个数。本文件既有测试已实证「多子用例塞进 1 个 test 方法」的写法 ——
    `test_invalid_shapes_and_paths` (test_release_by_track.py:282-290) 用 4 个 assertEqual 覆盖 4 个不同场景
    (bogus edit / 缺 content / 逃逸路径 / 绝对路径), 但只计 1 个 "Ran"。tasks.md / detailed-tasks.yaml 全文
    **没有任何一处要求「每个子用例必须是独立 test 方法」**, 而 TASK-001~004 的 verification 只写「子用例 ≥N」,
    对写法(独立方法 vs 循环/subTest 内断言)零约束。若 Phase B 实施者按本文件既有惯例, 为 SC-1 的 6 对写
    1 个带 for 循环的 test 方法 (而非 6 个独立方法), "Ran" 增量将远小于 45, 使「Ran ≥1367」在功能完全正确、
    45 条子用例逻辑上全部覆盖并通过的情况下仍判红; 反过来也可能诱导实施者为凑数字而机械拆分测试方法
    (纯为满足计数, 非提升覆盖)。两个方向都是「验收标准不可执行 / 会导致返工」。
  recommendation: >
    要么在 TASK-001~006 的 verification 里显式加约束「每个子用例 = 1 个独立 test 方法」(使 Ran 计数与子用例计数
    对齐), 要么把 TASK-014 的判据改为「全部 SC 断言通过 + 既有 6 条不变」而不锚定具体 Ran 数值, 或至少把
    "≥1367" 降级为参考性估计并写明「实际 Ran 数取决于测试方法粒度, 不作为独立判据」。

- type: issue
  severity: major
  category: documentation
  scope: tasks.md:65; detailed-tasks.yaml:328,406-410 (TG-5 / TASK-015~017)
  summary: "5.2–5.4 合计 9 处落点" 与同段落自身的逐项计数 (5 文件 + 3 项 + ×3 = 11) 不自洽, 该数字还直接决定 Phase B 收尾 `git status` 核验的目标基数
  evidence: >
    tasks.md:65 "⚠️ 5.2–5.4 合计 9 处落点" (与 detailed-tasks.yaml:328 注释、:408 TASK-017 notes 逐字重复)。
    但同一批文件里, TASK-015 (5.2) 标题/deliverables 明确 5 个文件 (plugin.json/marketplace.json/VERSION/
    CHANGELOG.md/README.md); TASK-016 (5.3) 标题逐字「主仓同步面 **3 项** — gitlink + VERSION 子模块版本表行 +
    root README badge」; TASK-017 (5.4) 标题逐字「i18n README translated-from 标记 **×3**」。5+3+3=**11**,
    非 9。proposal.md:271 Impact 表同一行本身也列出 11 个不同落点 (5 文件 + gitlink + VERSION 行 + README
    badge + 三个 i18n 文件), 与本文件的「5 文件+3项+×3」逐项计数完全对应, 进一步印证 11 才是与文中自身
    itemization 一致的数字; "9" 无法用「6(原'5文件+gitlink')+3(新发现)」以外的任何一致计数基准还原
    (若把 i18n ×3 当 1 个类别算, 则 5.2 的 5 个文件也应同理按「1 个类别」算, 而文中并未如此)。
    该注释的直接目的是防「scoped git add 漏发布同步面」复发 (引用 memory
    `feedback_scoped_git_add_splits_claim_from_landing`), 若收尾者以「9」为目标基数核对 `git status`,
    恰有 2 个真实落点 (VERSION 子模块版本表行与 README badge, 或反之) 可能被漏点而不自知 ——
    与该注释本身要防的失效模式同形。
  recommendation: >
    重算并统一为 11 (或给出明确、贯穿一致的「处」计数口径使 9 成立), 并同步更正 tasks.md:65 与
    detailed-tasks.yaml 两处引用。

- type: issue
  severity: minor
  category: testing
  scope: detailed-tasks.yaml TASK-007 (parent 2.1), verification 第 2 条
  summary: "归一 = 每段 strip → ./_ → - 译码 → casefold(), 建议按此顺序书写" 是措辞为「建议」的实现指引, 混进 verification 列表里却不构成可证伪判据
  evidence: >
    detailed-tasks.yaml:194 该条字面用「建议按此顺序书写」。proposal.md D1/§归一规则 明确「三者的施加顺序不影响
    结果 (R1′/backend 实证 ... 0 处不一致)」——按此, 任何合法实现无论写作何种顺序都会通过 SC-12/SC-13 等真实
    断言; 这一条本身不可能单独把某实现判红 ("它怎么会红?" 答不出来), 是嵌在判据列表里的零信息量项,
    容易被误当作独立可测的验收条目。
  recommendation: 从 verification 列表移到 notes (已有 TASK-007 notes 段落更合适), 或改写为可证伪形式(如"链式调用顺序不得影响 SC-12/13/6b 的通过结果")。

- type: issue
  severity: minor
  category: documentation
  scope: tasks.md 1.6 (checkbox); Group Overview 排序依据段 (tasks.md:26)
  summary: tasks.md 未标注 1.6 (SC-12) 对「组 1→组 2 RED-first」排序原则的例外, 该例外只写在 detailed-tasks.yaml 的 TASK-006 notes 里
  evidence: >
    tasks.md:26 "排序依据: 组 1 → 组 2 是 RED-first (SC 的 baseline-failing 状态已于 A.1 实跑留证 ... 组 1
    落盘后应立即复现那 8 条红)"; 该句未提示 1.6 例外。detailed-tasks.yaml:174-176 (TASK-006 notes) 才说明
    "唯一依赖实现的 TG-1 任务 (normalize_linked_issue Phase B 才存在) ⇒ 无 baseline 行, 依赖 TASK-007"
    且 dependencies 字段确实为 [TASK-007] (TG-2)。只读 tasks.md 的实施者可能按 checkbox 顺序尝试在组 2
    之前给 1.6 写「纯 RED」测试, 因 `normalize_linked_issue` 尚不存在而遇到 ImportError/NameError, 可能
    误判为自己环境有问题 (类比本 Spec 已知的 test_collision.py sys.path 陷阱, 但此处是新陷阱, 非同一个)。
  recommendation: 在 tasks.md 的 1.6 行或 Group Overview 段加一句「1.6 (SC-12) 依赖组 2 的 TASK-007 实现落地, 不适用 RED-first 顺序」。

## Verdict

**PASS_WITH_WARNINGS** (0 Critical + 2 Major + 2 Minor)。

判据: 两条 Major 均属「会导致返工或验收失效」—— TASK-014 的 `Ran ≥1367` 判据存在单位不匹配, 可能在功能完全正确时误判红或反向诱导凑数; TG-5 的「9 处落点」计数与其自身逐项枚举 (11) 不自洽, 直接威胁其自陈要防止的「发版同步面漏项」失效模式复发。两条 Minor 是措辞/文档层面, 不阻塞但建议顺手清。SC 覆盖完整性、45 下界分摊、baseline RED/GREEN 标注、派生统计自洽性四项均逐条独立核验通过, 未见恒真/恒假断言或结构性遗漏。

## 轮次记录

- Round 1 (qa-engineer, 独立席位): 实读 tasks.md + detailed-tasks.yaml + proposal.md (参照); 逐条重算 SC→task 映射、45 下界、baseline 标注一致性; 实跑 `run_tests.py` 核验 1322 基线; 追加检视既有测试文件的方法粒度惯例 (`test_invalid_shapes_and_paths`) 以实证 TASK-014 的计数假设风险; 追加核对发版同步面「9 处」与其自身 itemization 是否自洽。产出 2 Major + 2 Minor, 无 Critical。
