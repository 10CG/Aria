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
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 — backend-architect 审计报告

## 审计范围与方法

只审 `tasks.md` + `detailed-tasks.yaml` 的**任务分解与验收可执行性**(不重审归一规则本体)。逐条实读核验:

- `aria/skills/state-scanner/lib/collision.py`(实读 140-345 行)
- `aria/skills/state-scanner/lib/claim_schema.py`(实读 95-124 行)
- `aria/skills/state-scanner/SKILL.md`(实读 160-182 行)
- `aria/skills/state-scanner/scripts/phase1_gate.py`(实读 1215-1244 行)
- `aria/skills/state-scanner/tests/test_release_by_track.py`(`grep -n` 精确定位 class 起止行 + 实跑)
- 实跑 `cd aria/skills/state-scanner/tests && python3 run_tests.py` 核验 1322 基线声明
- 核对 aria 子模块 HEAD (`af87caeeed88af6af76f29a8002badbe1228d927`) 与主仓 HEAD (`a52ab813e9fff2a7059a61f1b7be3491c24dbe0a`) 两个 source_sha 锚点

## 逐条核验结果

### file:line 引用 — 全部精确无误

| 引用 | 声称内容 | 实读结果 |
|---|---|---|
| `collision.py:217` | 裸 `!=` 谓词 | ✅ `if c.linked_issue != own_linked_issue:` 逐字确认 |
| `collision.py:228` | linked_issue 原串回显 | ✅ `"linked_issue": c.linked_issue,` 确认 |
| `collision.py:210` | `_TERMINAL = ("done","abandoned","unknown")` | ✅ 确认 |
| `collision.py:307` | `_TERMINAL = ("done","abandoned")` | ✅ 确认 |
| `collision.py:155` | 同值 `{done,abandoned}` (内联 tuple, 未赋值给变量) | ✅ 值一致; tasks.md 措辞把 155/307 并称「_TERMINAL」略有简化 (155 处并非变量赋值), 不影响判定, 不单列 |
| `collision.py` docstring `:182-206` | `linked_issue_overlaps` 文档块 | ✅ 182 行开引号、206 行闭引号, 精确吻合 |
| `claim_schema.py:107-114` | `linked_issue` 字段文档、"SAME"/"active" 措辞 | ✅ 逐字确认 (107 行 `linked_issue : Optional[str]` 至 114 行 "winner determination.") |
| `SKILL.md:176` | claim 生命周期闭环段, 含「同一件事两个名字」 | ✅ 逐字确认 |
| `phase1_gate.py:1232` / `:1235` | `linked_issue_overlaps(...)` 调用 / `except Exception` | ✅ 逐字确认 (注: 实际路径是 `aria/skills/state-scanner/scripts/phase1_gate.py`, 非 `aria/scripts/phase1_gate.py`; tasks.md/proposal 引用時已省略 skill 前缀但未造成歧义) |
| `test_release_by_track.py :206-247` (4 条既有) / `:527-575` (2 条既有) | 既有测试逐字不改的宿主范围 | ✅ `grep -n "^class Test"` 确认 `TestLinkedIssueOverlaps` 206-249、`TestPhase1GateLinkedIssueCli` 527-579, 方法数吻合 (4 + 2) |
| `metadata.test_baseline_note`: 1322 tests / OK | 基线测试数 | ✅ 实跑确认: `Ran 1322 tests in 34.551s / OK` |
| `scope_repo_head: af87cae` / anchor `source_sha: a52ab81` | 两个不同仓的 HEAD | ✅ 均确认 (af87cae = aria 子模块 HEAD, a52ab81 = 主仓 HEAD, 两者分属不同 repo, 非矛盾) |
| 复杂度/工时/agent 分摊汇总 (S×11·M×5·L×1, 73h, qa×8/km×5/ba×4) | 派生统计行 | ✅ 逐条重新加总核验, 三项汇总数字全部与 17 条任务实际字段一致 (此前 3 次失准的历史此次未复发) |

**结论: deliverables 路径真实性 = 全绿, 无一处 file:line 引用错误。**

---

## 结构化发现

- type: issue
  severity: major
  category: architecture
  scope: detailed-tasks.yaml TASK-008/TASK-009/TASK-010 依赖边; lib/collision.py
  summary: TASK-009 (guard 强化) 只依赖 TASK-007, 未依赖 TASK-008; TASK-010 (docstring 同步, 同文件) 也只依赖 TASK-008 未依赖 TASK-009 ⇒ 验收失效 + 同文件跨 agent 冲突风险
  evidence: >
    SC-6/SC-6b/SC-10 (TASK-009 的验收标准) 按 proposal baseline 表「取证方式」栏均为「实跑生产
    linked_issue_overlaps」——即通过 TASK-008 改造后的比较谓词间接验证, 而非直接单测
    normalize_linked_issue。但 TASK-009 (detailed-tasks.yaml:230 `dependencies: [TASK-007]`)
    未列 TASK-008 为前置。若 DAG 按声明的独立性调度 (TASK-008/TASK-009 均只依赖 TASK-007, 无
    互相依赖, 且不在文件底部「并行组」注释的白名单内但也未被显式禁止), TASK-009 可能先于
    TASK-008 执行——此时 linked_issue_overlaps 仍是裸 `!=` 比较, 从未调用 normalize_linked_issue,
    "SC-6/6b/10 全绿"这一验收结果对 TASK-009 新写的 guard 代码是**假阳性**(这三组 SC 在 baseline
    上本就是绿, 参见 proposal.md baseline 表 SC-6/SC-6b/SC-10 行「性质=护栏, 算进证据面?=❌」——
    即它们在改动前后都应为绿, 因此无法区分"TASK-009 guard 写对了"与"TASK-009 guard 根本没被调用")。
    进一步, TASK-010 (detailed-tasks.yaml:255 `dependencies: [TASK-008]`, deliverable 为
    `lib/collision.py` docstring :182-206) 与 TASK-009 (backend-architect) 同改一个文件, 却分给
    不同 agent (knowledge-manager) 且二者间无依赖边——直接违反本项目 memory
    `feedback_workflow_partition_by_file_domain`(同文件必须串行/需依赖边, 不能只按"不同 deliverable
    小节"简单并行)。co_dependency_note (detailed-tasks.yaml:51-54) 与 tasks.md:26 都写「TG-3 可与
    TG-2 并行 (不同文件)」——该断言对 TASK-010 具体不成立 (deliverable 就是同一个 lib/collision.py)。
  suggested_fix: >
    TASK-009 的 dependencies 加 TASK-007→TASK-008 链式 (即 TASK-009 依赖 TASK-008, 而非仅
    TASK-007), 并让 TG-3 三条 (TASK-010/011/012) 统一依赖 TASK-009 (TG-2 全部完成) 而非仅
    TASK-008, 使 TG-2 内部严格串行 (007→008→009)、TG-3 整体等 TG-2 全绿后再起。

- type: issue
  severity: minor
  category: testing
  scope: detailed-tasks.yaml TASK-008 verification
  summary: TASK-008 的验收清单「SC-1/1b/2/3/4/5/5b/5c/13/14/15 全绿」漏列 SC-11, 而 SC-11 与已列的 SC-13/14/15 同为 baseline-RED 主判据、同走 linked_issue_overlaps 取证路径
  evidence: >
    detailed-tasks.yaml:213 TASK-008 verification 列表未出现 "SC-11"; 而 SC-11 (`#` 取最后一个的切分
    方向) 按 proposal baseline 表性质与 SC-13/SC-15 (`/` 取最后一段) 同级 (均为「主判据」「红」),
    且 SC-15 notes 自陈"是 SC-11 的姊妹条"。grep 全文确认 SC-11 只出现在 TASK-004 (写测试) 中,
    未出现在任何 TG-2/TG-4/TG-5 的 verification 字段里。TASK-014 的全量回归会兜底跑到它, 但
    TASK-008 自身完成节点上没有把它钉进验收 checklist, 与其姊妹条 SC-13/14/15 的处置不对称。
  suggested_fix: TASK-008 verification 第一行补上 SC-11, 与 SC-13/14/15 同批列出。

- type: issue
  severity: minor
  category: implementation
  scope: detailed-tasks.yaml TASK-007/TASK-009 verification vs proposal D7
  summary: D7 四条实现约束里的 `number_str.isascii() and number_str.isdigit()` 谓词从未在 TG-2 任一任务的 verification 字段里被逐字点名, 只靠 "SC-6/6b 全绿" 隐式覆盖
  evidence: >
    grep -n "isascii\|isdigit" 对 tasks.md 与 detailed-tasks.yaml 全文均零命中。D7 其余三条
    (不含 # 先判不可解析且不得无守卫拆分 / int() 必包 try-except ValueError / limit>0 前置) 都在
    TASK-009 verification 里逐字复述 (detailed-tasks.yaml:235-237), 唯独 isascii+isdigit 谓词没有
    对应的逐字验收行——行为上被 SC-6b (全角数字 '１２３'、上标 '²' 等边界值) 间接覆盖, 但审计
    brief 明确要求核对 D7 四条是否"落在任务之间的缝里", 这一条属于"有测试兜底但清单未点名"。
  suggested_fix: TASK-009 verification 加一行显式复述 isascii()+isdigit() 谓词, 与另外三条 D7 约束的处置对称。

- type: issue
  severity: minor
  category: documentation
  scope: detailed-tasks.yaml TASK-008 verification vs proposal §非目标
  summary: TASK-008 验收行「函数签名与返回 schema 逐字不变」照抄 D6 原始措辞, 未带上 proposal §非目标 已加的「限于本 Spec 变更面」限定词; 单独读 TASK-008 容易被理解为对母 Spec 未来追加 include_terminal 形参的否定
  evidence: >
    detailed-tasks.yaml:214 TASK-008 verification: "函数签名与返回 schema 逐字不变 ⇒ Phase B 现有
    调用方零改动 (D6)"——无限定词。proposal.md:257 已把 D6 限定为「本 Spec 不改签名; 母 Spec
    落地时追加 keyword-only 形参不视为对本 Spec 的违反」。该限定词在 tasks.md 的
    「✅ 与母 Spec 的接缝 — 已关闭」章节 (tasks.md:85-93) 有复述, 但未同步进 TASK-008 自己的
    verification 字段——两处表述不在同一处, 读者若只看 detailed-tasks.yaml (Phase B 实际执行时
    最贴近的文档) 会漏掉限定。
  suggested_fix: TASK-008 verification 该行末尾加「(限本 Spec 变更面; 母 Spec 后续加 include_terminal 不视为违反, 见 tasks.md §与母 Spec 的接缝)」。

## Verdict

**vote: REVISE** (0 critical, 1 major, 3 minor ⇒ 不满足 PASS 的 "0 critical 且 0 major")

verdict (frontmatter 口径): **PASS_WITH_WARNINGS** (0 Critical + ≥1 Major)

## 轮次记录

R1 (本轮, backend-architect 单席): 实读全部声称的 file:line 引用 (11 处), 全部精确无误; 实跑测试基线确认 1322/OK; 重新加总复杂度/工时/agent 分摊三项派生统计, 与实际字段一致 (无第 4 次失准)。核心发现集中在依赖图: TG-2 内部 (TASK-007/008/009) 与 TG-2→TG-3 (TASK-008/009 → TASK-010) 的依赖边未能反映"谁真的必须先于谁"这一技术事实, 导致 TASK-009 的验收标准 (SC-6/6b/10) 在特定调度顺序下退化为假阳性, 且 TASK-009/TASK-010 同文件跨 agent 无依赖边违反项目既有 memory 约定。次要发现为 SC-11 验收缺口、D7 第二条约束未被逐字点名、TASK-008 措辞未继承 proposal 已加的限定词——三者均有其他机制兜底 (全量回归 / 行为测试 / 文档其他章节), 严重度定为 minor。
