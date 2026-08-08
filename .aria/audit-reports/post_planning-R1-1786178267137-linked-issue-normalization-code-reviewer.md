---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T08:37:47.000Z
context: openspec/changes/linked-issue-normalization/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 — code-reviewer 席

**审计对象**: `openspec/changes/linked-issue-normalization/tasks.md` (A.2) + `detailed-tasks.yaml` (A.3)
**source_sha**: `a52ab81` (主仓) · `af87cae` (aria 子模块, 与 `metadata.scope_repo_head` 一致 — 实测核验通过)
**镜头**: 重算全部派生数字 / 每条 verification 的双向可证伪性 / 引用实读 / 三方交叉一致性

---

## 审计结论

计划的**算术层与引用层质量很高** —— 45 下界的逐 SC 分摊、复杂度汇总、工时锚、agent 分摊、任务 1:1 映射、测试基线全部独立重算无误，被引用的 file:line 除一处外全部实读命中。缺陷集中在**验收层**: 7 条 verification 中出现「功能全对却判红」或「功能有错却判绿」，其中**发版同步面那条是结构性假绿** —— 两条 enabled custom check 对计划遗漏的 7 处版本引用天然失明，照本计划执行会在残留陈旧版本号的情况下 100% 判绿。

---

## 第一部分: 我自己的重算过程 (不采信文件自述值)

### 1. 子用例下界 = 45 ✅ 与自述一致

按 tasks.md 分组独立加总:

| 组 | 构成 | 我的加总 | 文件自述 |
|---|---|---|---|
| 1.1 | SC-1(6)+SC-1b(3)+SC-2(1)+SC-3(1)+SC-4(2) | **13** | 13 ✅ |
| 1.2 | SC-5(1)+SC-5b(3)+SC-5c(1) | **5** | 5 ✅ |
| 1.3 | SC-6(5)+SC-6b(9)+SC-10(1) | **15** | 15 ✅ |
| 1.4 | SC-11(2)+SC-13(2)+SC-15(2)+SC-14(2) | **8** | 8 ✅ |
| 1.5 | SC-9(1) | **1** | 1 ✅ |
| 1.6 | SC-12(3) | **3** | 3 ✅ |
| — | 13+5+15+8+1+3 | **45** | ≥45 ✅ |

覆盖性: 17 条 SC (1/1b/2/3/4/5/5b/5c/6/6b/9/10/11/12/13/14/15) 在六组里**恰好各出现一次**，无重复无遗漏，与 proposal §Impact 逐条推导 (`proposal.md:276`) 逐格吻合。

**独立第三方核验**: 实跑 `.aria/repro/sc-baseline-linked-issue-normalization.py aria/skills/state-scanner` → exit 0，其「子用例」列输出 `6,3,1,1,2,1,3,1,5,9,1,1,2,2,2,2` = 42，加 SC-12 的 3 (无 baseline 行) = **45**。红集合实测 = `SC-1/1b/3/4/5b/11/13/15` 八条，与 `co_dependency_note` 声称的 8 条**逐条相同**。

### 2. 复杂度 / 工时 / agent 分摊 ✅ 全部与自述一致

- S = {002,005,006,008,010,011,012,014,015,016,017} = **11**; M = {001,004,007,009,013} = **5**; L = {003} = **1**; XL = **0** → 自述 `S×11 · M×5 · L×1 · XL×0` ✅
- 锚公式 11×3 + 5×6 + 1×10 = 33+30+10 = **73h**; 逐条 `est_hours` 直接相加亦 = **73h** (两法互证) ✅
- qa-engineer = {001,002,003,004,005,006,013,014} = **8**; knowledge-manager = {010,011,012,015,017} = **5**; backend-architect = {007,008,009,016} = **4**; 8+5+4 = **17** = `total_tasks` ✅
- 关键路径按 est_hours: 003(10)→007(6)→008(3)→012(3)→013(6)→014(3)→015(3)→016(3) = **37h**，与自述关键路径同链 ✅

### 3. 任务 1:1 映射 ✅

tasks.md checkbox: 1.1–1.6(6) + 2.1–2.3(3) + 3.1–3.3(3) + 4.1(1) + 5.1–5.4(4) = **17**; TASK-001..017 的 `parent` 逐个对上且互不重复 ✅

### 4. 测试基线 ✅ 实跑复现

- `cd aria/skills/state-scanner/tests && python3 run_tests.py` → **`Ran 1322 tests` / `OK` / exit 0** ✅ 与 `test_baseline_note` 一致
- `bash aria/skills/run_all_tests.sh` → **`9 OK / 0 FAIL / 0 SKIP (累计 1698)`** ✅ 逐字一致
- `python3 run_tests.py collision` → **ImportError** (`cannot import name 'collision' from 'lib' (…/scripts/lib/__init__.py)`)，`known_env_trap` (aria-plugin #134) 描述属实，且成因就是 `tests/test_collision.py:29-30` 两个 insert 使 `scripts/` 占据 `sys.path[0]` 遮蔽了 `lib` ✅
- 既有 6 条实读核验: `test_release_by_track.py:206` = `class TestLinkedIssueOverlaps`，含 4 个 test 方法 (`:224/:232/:236/:245`)；`:527` = `class TestPhase1GateLinkedIssueCli`，含 2 个 (`:533/:563`) ✅

### 5. 发版落点数 ❌ **算错** — 应为 11，非 9

逐个实读枚举 (全部确认存在):

| # | 落点 | 实读证据 |
|---|---|---|
| 1-5 | `aria/.claude-plugin/plugin.json` · `marketplace.json` · `aria/VERSION` · `aria/CHANGELOG.md` · `aria/README.md` | 均存在 |
| 6 | 主仓 gitlink | `.gitmodules` 有 `aria` |
| 7 | 主仓 `VERSION` 子模块表行 | `VERSION:24` `\| aria (插件) \| v1.65.5 \|` |
| 8 | root `README.md` Plugin badge | `README.md:8` |
| 9-11 | `README.{zh,ja,ko}.md` 的 `translated-from` | 各 `:3` |

5 + 3 + 3 = **11**。tasks.md:65 与 detailed-tasks.yaml:408 均写「**9 处**」。CLAUDE.md §版本管理 的 canonical 列举 (「aria 子模块 5 文件 + 主仓 gitlink + 主仓 VERSION + root README badge + i18n README」) 同样是 11。「9」= 早期叙事「5 文件 + gitlink (6) 漏 3 处 (i18n)」的残留，它把 5.3 里的 VERSION 行与 badge 两项吞掉了——而同一份文件的 5.3 明写「**3 项**」。

### 6. 发版同步面的**真实**面 ❌ 计划列举不全 (见 F1)

上次 bump `fb5ed36` 的 stat 是 ground truth:

```
CLAUDE.md      | 4 ++--     (2 行: :139 版本史 + :141 版本行)
README.ja.md   | 6 +++---   (3 行: translated-from + badge + "Plugin Version:")
README.ko.md   | 6 +++---   (3 行)
README.zh.md   | 6 +++---   (3 行)
README.md      | 4 ++--     (2 行: badge + "Plugin Version:")
VERSION        | 2 +-       (1 行)
aria           | 2 +-       (gitlink)
```
commit message 自陈: 「版本引用同步: **CLAUDE.md** / root README / i18n ×3 / VERSION 表」。

---

## 第二部分: 结构化发现

```yaml
- type: issue
  severity: critical
  category: documentation
  scope: detailed-tasks.yaml TASK-016/TASK-017 · tasks.md 5.3/5.4 · README.{md,zh,ja,ko}.md
  summary: >
    发版同步面漏 7 处版本引用 (root README "Plugin Version:" 行 + i18n ×3 的 badge 与
    "Plugin Version:" 行); 两条 enabled check 对这 7 处结构性失明 ⇒ 计划照做后
    TASK-016/017 的 verification 会在残留 v1.65.5 的情况下全绿 = 验收假绿。
  evidence: >
    实读: README.zh.md:10 badge v1.65.5 / :244 "Plugin Version: 1.65.5"; ja/ko 同构;
    README.md:8 badge / :242 "Plugin Version: 1.65.5"。TASK-016 只覆盖 badge (:382-384),
    TASK-017 只覆盖 translated-from 标记 (:403-405)。
    实跑 m6-version-badge-match 的 command: grep -m1 只扫 README.md 首个含版本的 badge
    → BADGE=1.65.5 PLUGIN=1.65.5 → OK; 该 check 结构上看不到 i18n 文件, 也看不到
    "Plugin Version:" 行。实读 i18n-readme-translation-currency 实现
    (.aria/state-checks.yaml:161-166): 只 re.search("translated-from") 比对版本, 正文一概不看。
    ⇒ 只更标记 ⇒ 两 check 皆 OK ⇒ 7 处陈旧版本号无人发现。
    历史 ground truth: fb5ed36 上次 bump 在每个 i18n 文件改 3 行、README.md 改 2 行,
    证明这 7 处一直属于同步面。该 check 自己的 fix 文案也写「以当前 README.md 为源重新
    同步滞后语种, **并**把标记更新」—— 计划只执行了「并」的后半。
    这正是 #140 的原教训 (「badge 称最新但正文旧, 比旧 badge 更误导」) 的镜像复发。

- type: issue
  severity: major
  category: documentation
  scope: detailed-tasks.yaml TG-5 (TASK-015..017) · tasks.md §5 · CLAUDE.md:139,141
  summary: >
    CLAUDE.md 的两处版本引用未列入任何任务; ship v1.66.0 后 CLAUDE.md 项目状态段仍写
    "插件 aria-plugin v1.65.5" ⇒ 违 Rule #3 (文档与代码同步), 且无任何 check 兜。
  evidence: >
    CLAUDE.md:139 "v1.52.0–v1.65.5 已 ship" · :141 "版本: 插件 aria-plugin v1.65.5"。
    fb5ed36 stat 显示 CLAUDE.md 改 2 行, commit message 把 CLAUDE.md 列在版本引用同步
    第一位。TG-5 三个任务的 deliverables 合计 10 个路径, 无 CLAUDE.md。
    注: CLAUDE.md §版本管理 自己的「发布同步面」列举也漏了自身 —— 计划忠实继承了这个洞,
    但落点在本 Spec 就会实际发生。CLAUDE.md 的编辑权属 owner, 建议 Phase B 只提示不自行改。

- type: issue
  severity: major
  category: documentation
  scope: tasks.md:65 · detailed-tasks.yaml:408
  summary: >
    「合计 9 处落点」与它自己的分解 5.2(5 文件)+5.3(3 项)+5.4(3 项)=11 直接矛盾;
    该数字在 A.2 与 A.3 两份文件同值传播, 且被当作收尾清点的总数用。
  evidence: >
    tasks.md:61-63 列 5+3+3; tasks.md:65 写「5.2–5.4 合计 9 处落点」;
    detailed-tasks.yaml:408 写「TASK-015~017 合计 9 处落点」。逐个实读枚举 = 11 (见上表)。
    CLAUDE.md canonical 列举同为 11。用于防「scoped git add 声称 global」的清点总数写错,
    等于把清点本身的 backstop 弄钝 (该形状 memory 记为本项目一天两次实证)。

- type: issue
  severity: major
  category: testing
  scope: detailed-tasks.yaml TASK-014 verification[0]
  summary: >
    "Ran ≥1367 / OK (1322 + ≥45)" 把「子用例」当成 unittest 方法计数。45 是配对/断言级
    下界, 不是 test 方法数 ⇒ 功能全对 (45 子用例齐备) 仍可能 Ran < 1367 而判红。
  evidence: >
    实测: 单个 test 方法内 6 个 subTest → unittest 报 "Ran 1 test"。宿主文件既有风格正是
    单方法多子用例 (test_terminal_and_no_issue_ignored :236-243 一个方法覆盖 4 条 claim;
    test_same_issue_different_track_flagged 一方法覆盖 1 对)。若 17 条 SC 写成 17 个方法
    覆盖 45 子用例, 全量套件 = Ran 1339 ⇒ 该 verification 判红而功能无错。
    反向副作用同样坏: 为凑 Ran 数把 45 个子用例硬拆成 45 个方法, 是让度量驱动写法。
    修法: 拆成两条独立断言 —— (a) 全量 run_tests.py exit 0 且 Ran ≥ 1322 + N_methods;
    (b) 子用例 ≥45 由各 TG-1 任务的 verification 按断言/参数化条目数自证 (已有)。

- type: issue
  severity: major
  category: testing
  scope: detailed-tasks.yaml TASK-007 verification[0] ↔ TASK-006 dependencies
  summary: >
    TASK-007 的第一条验收是「SC-12 全绿」, 但落 SC-12 的 TASK-006 依赖 TASK-007
    ⇒ 007 完成时该测试尚不存在, 这条只能被口头声称 (假绿) 或逼实施者违反已声明 DAG。
  evidence: >
    detailed-tasks.yaml:168 TASK-006 dependencies: [TASK-007]; :175 notes 明写「唯一依赖
    实现的 TG-1 任务 (normalize_linked_issue Phase B 才存在)」。而 :193 TASK-007
    verification[0] = "SC-12 全绿 (返回契约)"。两者构成环。
    修法二选一: 把 TASK-007 的这条改为「SC-1/1b/3/4/5b/11/13/15 由 TASK-008 观测转绿」
    或直接删除, SC-12 的绿归 TASK-006 自身验收; 或把 TASK-006 改成先落红 (对不存在的
    符号 import 失败即红), 让 007 的这条成立。

- type: issue
  severity: major
  category: testing
  scope: detailed-tasks.yaml TASK-008 verification[0]
  summary: >
    SC-11 无任何 per-task 的「修后转绿」断言。TASK-008 的绿名单列了 11 条 (1/1b/2/3/4/5/
    5b/5c/13/14/15) 独漏 SC-11, 而 SC-11 是 8 条 substitute 证据面之一 (baseline 红)。
  evidence: >
    detailed-tasks.yaml:213 逐字为 "SC-1/1b/2/3/4/5/5b/5c/13/14/15 全绿"。SC-6/6b/10 归
    TASK-009 (:234)、SC-12 归 TASK-007 (:193)、SC-9 由 :215 的「:228 回显不动」间接守,
    唯 SC-11 无归属。SC-11 的姊妹条 SC-15 (同为 Q7-1 新增切分方向) 却在列 ⇒ 是遗漏非有意。
    后果: TASK-008 可在 SC-11 仍红时判绿, 缺陷推迟到 TASK-014 全量套件才暴露 (返工),
    且 substitute 证据面「八条 baseline-failing 全部翻绿」的论证少一条 per-task 锚。

- type: issue
  severity: major
  category: testing
  scope: detailed-tasks.yaml TASK-013 verification (Rule #6 AB)
  summary: >
    AB 任务的验收只要求「跑了 + 结果落盘 + 时点在 5.x 前」, 没有任何结果判据
    ⇒ AB 判出退化 (WITHOUT_BETTER) 时该任务照样判绿, Rule #6 闸门退化为「执行留痕」。
  evidence: >
    detailed-tasks.yaml:317-319 三条 verification 全是过程性的; :320-325 notes 讨论的也
    只是「若属套件覆盖外怎么办」, 未涉及「若结果为退化怎么办」。
    而成文判据是存在的: aria-plugin-benchmarks/AB_TEST_OPERATIONS.md:547
    「[ ] 无 WITHOUT_BETTER verdict 的 Skill (否则必须修复)」, 计划未引用。
    建议补第 4 条: "本轮 grading-summary.md 无 WITHOUT_BETTER verdict; 若有则回到 TASK-012
    改措辞重跑, 不得以『纯括注』结案"。

- type: issue
  severity: minor
  category: implementation
  scope: detailed-tasks.yaml:218-219 (TASK-008 notes)
  summary: >
    「collision.py:155 与 :307 两处 _TERMINAL = {done, abandoned}」—— :155 处无 _TERMINAL
    绑定, 是列表推导内联元组; 且 :210/:307 都是 tuple 不是 set。metadata 自称「全部路径与
    行号已对该 HEAD 实测核验」。
  evidence: >
    实读 collision.py:155 = `active = [c for c in claims if c.status not in ("done", "abandoned")]`;
    :307 = `_TERMINAL = ("done", "abandoned")`; :210 = `_TERMINAL = ("done", "abandoned", "unknown")`。
    影响有限 (该分歧已开 aria-plugin #133 且本 Spec 只披露不改), 但 Phase B 若按「找 _TERMINAL
    赋值」grep 会在 :155 扑空。改为「:155 的内联终态元组 与 :307 的 _TERMINAL」即可。

- type: issue
  severity: minor
  category: testing
  scope: detailed-tasks.yaml TASK-014 verification[2] · tasks.md:32
  summary: >
    「既有 6 条 (:206-247 与 :527-575) 逐字未改」用行号锚, 而本 change 正是往同一文件插
    新用例 ⇒ 验收时点这两个区间必然位移 (:527-575 尤甚), 锚点被任务自身作废。
  evidence: >
    实读 test_release_by_track.py 共 579 行, TestLinkedIssueOverlaps 在 :206、
    TestPhase1GateLinkedIssueCli 在 :527。新增 ≥45 子用例落同一文件后行号全部下移。
    改为内容锚 (类名 + 6 个方法名) 或 `git diff -- tests/test_release_by_track.py` 断言
    这 6 个方法体零 hunk。

- type: risk
  severity: minor
  category: architecture
  scope: detailed-tasks.yaml TASK-009 ∥ TASK-010 (同为 lib/collision.py)
  summary: >
    DAG 允许 TASK-009 (backend-architect, collision.py) 与 TASK-010 (knowledge-manager,
    collision.py docstring) 并发 —— 两个 agent 同时改同一文件, 与 TG-1 同情形的处置不一致。
  evidence: >
    TASK-009 deps [TASK-007]; TASK-010 deps [TASK-008]; TASK-008 deps [TASK-007]
    ⇒ 009 与 010 的前驱集不互斥, 拓扑上可同时就绪。:427 的并行组注释给 TG-1 加了
    「建议串行落盘避免冲突」的告示, 对这一对却没有。memory feedback_workflow_partition_by_file_domain
    的判据是「同文件串行」。建议给 TASK-010 加 dependencies: [TASK-008, TASK-009] 或同款告示。

- type: issue
  severity: minor
  category: documentation
  scope: detailed-tasks.yaml:417-419 (DAG 注释) vs TASK-013 dependencies
  summary: DAG ASCII 图把 TASK-010/011/012 三条都汇入 TASK-013, YAML 里 TASK-013 只依赖 [TASK-012]。
  evidence: >
    :417-419 画作 "TASK-010 ┐ / TASK-011 ├─┐ / TASK-012 ─┴─▶ TASK-013"; :291 TASK-013
    dependencies: [TASK-012]。机器读的是 YAML, 人读的是图, 二者不同 ⇒ 图应改为只从 012 引出。

- type: issue
  severity: minor
  category: documentation
  scope: detailed-tasks.yaml TASK-016 deliverables
  summary: >
    gitlink (主仓 aria 子模块指针) 在 verification 里承重 ("gitlink 指向合并后的 master SHA"),
    却不在 deliverables 里; deliverables 只有 VERSION 与 README.md。
  evidence: >
    detailed-tasks.yaml:379-384。gitlink 是 TG-5 里最容易 orphan 的一项 (CLAUDE.md 硬约束 1
    列了 2026-07-14 事故), 建议显式写入 deliverables 为 `aria  # submodule gitlink`。
```

---

## 第三部分: 优点 (确认做对的)

1. **派生数字的可证伪性做到位**: 45 的逐 SC 分摊在 tasks.md、detailed-tasks.yaml、proposal 三处独立成立, 且与仓内可执行 artifact (`sc-baseline-*.py`) 的实测子用例列**逐格吻合** —— 这是本项目多次出问题的老形状 (`≥12→≥35(算错)→≥43→≥38→≥44→≥45`), 本次是干净的。
2. **复杂度/工时/agent 三行自带「派生值须重算」告示且明说首版算错过一次** (:435-437), 实测本版三行全对。
3. **引用精度高**: `collision.py:217` 裸 `!=`、`:228` 回显、`:182-206` docstring、`claim_schema.py:107-114` (原文逐字 "Two active claims with the SAME linked_issue")、`SKILL.md:176`、`phase1_gate.py:1235` 的 `except Exception`、`test_collision.py:29-30` 的 insert 倒置 —— **七处逐条实读命中**, 只有 `:155` 的 `_TERMINAL` 措辞不准。
4. **`known_env_trap` 是真的**: 实跑 `run_tests.py collision` 复现 ImportError, 且「验收一律以全量 run_tests.py 为准」的处置正确 —— 这条会实打实省掉 Phase B 一次误判。
5. **RED/GREEN 极性逐条正确**: 六个 TG-1 任务声称的 baseline 状态 (RED: SC-1/1b/3/4/5b/11/13/15; GREEN: SC-2/5/5c/6/6b/9/10/14) 与我实跑 repro 脚本的 16 行输出**逐格一致**, 且负控/护栏的「baseline 就红 = 用例写错」反向判据也写了。
6. **TASK-009 的 `limit > 0` 告示是本计划最高价值的一条**: 点名「照抄成裸 `len > limit` 会让本 Spec 要修的缺陷原样复活且看起来完全照抄了 Spec」, 精确对上 memory `feedback_fix_recurs_in_its_own_fallback_path`。
7. **已知限成文而不修** (tasks.md §Phase B 开工前必读) 处理得当: 三件辅助工具的「空真洞 / 枚举不全 / fail-OPEN 豁免」被明确降级为「便宜的辅助, 不是机械闸门」, 避免了「工具打绿 = 已清零」的假绿继承。

---

## Verdict

**verdict: FAIL** (1 Critical + 6 Major)
**vote: REVISE**

### 阻塞项 (必须在 Phase B 开工前修)

| # | 项 | 落点 |
|---|---|---|
| C1 | 发版同步面漏 7 处版本引用 + 两条 check 对其失明 ⇒ TASK-016/017 假绿 | TASK-016/017, tasks.md 5.3/5.4 |
| M1 | CLAUDE.md 两处版本引用无任务归属 (Rule #3) | TG-5 |
| M2 | 「9 处落点」与自身分解 (5+3+3=11) 矛盾, 两文件同值 | tasks.md:65, yaml:408 |
| M3 | 「Ran ≥1367」把子用例当 unittest 方法计数 ⇒ 功能全对判红 | TASK-014 |
| M4 | TASK-007 验收「SC-12 全绿」与 TASK-006 依赖成环 ⇒ 只能声称 | TASK-007/006 |
| M5 | SC-11 无 per-task 转绿断言 (八条证据面之一) | TASK-008 |
| M6 | AB 任务无结果判据 ⇒ 退化也判绿, Rule #6 闸门退化为留痕 | TASK-013 |

### 复议建议 (给 R2)

C1/M1/M2 是同一根: **发版同步面的「面」在三份文档里都是按文件数而非按版本引用点数枚举的**。建议 fix 时不要逐条打补丁, 而是把 TG-5 的验收换成**一条机械断言**:

```
grep -rn "1\.65\.5" CLAUDE.md README.md README.zh.md README.ja.md README.ko.md VERSION → 零命中
```

(bump 后旧版本号在主仓应彻底消失; CLAUDE.md 那两处若属 owner territory 则单列为「提示 owner」而非 AI 自改)。这条同时覆盖 C1 的 7 处、M1 的 2 处, 且与 M2 的计数无关 —— 它是**维度匹配**的检查 (memory `feedback_invariant_dimension_must_match_error_dimension`: 无向的「文件是否被 touch」对「哪一行没改」天然免疫)。

---

## 轮次记录

| 轮 | 席位 | 结论 | Critical | Major | Minor |
|---|---|---|---|---|---|
| R1 | code-reviewer | REVISE | 1 | 6 | 5 |

**本轮方法**: 全部数字独立重算 (未采信任何自述值); 实跑 4 个命令取 ground truth (`run_tests.py` 全量 / 单模块 / `run_all_tests.sh` / `sc-baseline-*.py`) + 实跑两条 enabled custom check 的 command 本体 + 用 `git show --stat fb5ed36` 取上次 bump 的落点 ground truth + 一个 subTest 计数微实验; 12 处 file:line 逐条实读。
