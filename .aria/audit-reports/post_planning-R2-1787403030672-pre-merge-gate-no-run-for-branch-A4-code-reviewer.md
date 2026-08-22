---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: "2026-08-22T13:53:26.172Z"
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A4-code-reviewer
critical_count: 0
major_count: 2
minor_count: 4
---

# post_planning R2 — A4 code-reviewer (R1 簇 #2/#10/#11 核对 + yaml 自洽 + 新鲜眼睛)

## 摘要

实读 proposal.md v7 全文 + detailed-tasks.yaml v2 全文; 机械核 yaml 自洽 (脚本): total_tasks 18 ✓ / estimated_hours 49 ✓ / parent 8 ✓ / exec_order 0..17 唯一且每条 dependencies 的 exec_order 均小于自身 ✓ / `carries_sc` ↔ `sc_coverage_crosscheck` 16 条双向一致 (含 007a/007b 拆分与 SC-16 三分) ✓ / `agent_summary` 四 agent 与 tasks.agent 逐一相等 ✓ / 条件字段五处 (007a·007b `conditional_on`, 006·011·015 `conditional_parts`) ✓ / `status` 全 pending, 零 `skipped` ✓。活体复核: v1.66.4 tag 在 origin 与 github **仍均缺** (ls-remote 两远端各只有 v1.66.0/.2/.3) ⇒ TASK-015 补打步骤仍必要; 主仓 14 个版本点当前全为 1.66.4 且行号与 TASK-015 title 逐一命中; custom checks 10 条 (`state-checks.yaml` `name:` 计数 = 10) ✓。

归我席的三簇 (#2 A4-M1 / #10 A4-m1 / #11 A4-m2·m4·m5·m6) 在 v2 **6 closed / 1 partial**: 唯一残留是 #2 的 proposal §3.5 false 分支 = 「整组**从本 spec 删除** … Impact/CHANGELOG 相应不提」被 INV-3 转录成「整组**不做**」, 只有 CHANGELOG 半边落 TASK-015, proposal.md 自身的删除动作 (§4 / SC-8 / SC-9 dispatchable / SC-2 子项 / SC-5 (c2) / 3.3 (a) / Impact 两项) 零任务承载 (M2)。新鲜眼睛抓到一条更承重的结构问题: **TASK-003 (§1+§2.2 核心实现) 在 `dependencies` 图上只被 TASK-013/015 传递可达**, TASK-005/006/007a/007b/010/011/012/014 全部不经它 —— 顺序只活在 `execution_order` 散文里; 而 yaml 自己把 `exec_order` 定义为 advisory 且 `readiness_rule` 按依赖 status 判就绪, 于是 TASK-006 GREEN / TASK-010 probe PASS / TASK-014 活体三处 verification 在图上「就绪」时结构上不可能通过 (M1)。两条 Major 修法合计 <10 行。

## R1 处置核对

| 簇 | R1 条目 | v2 处置 (聚合表) | R2 实核 | 状态 |
|---|---|---|---|---|
| #2 | A4-PP-M1 条件 scope 文档面/发版面未标记; INV-3 漏 2.3 渲染句 + CHANGELOG; skipped 依赖语义未定 | INV-3 rule 重写列四落点; TASK-006/011/015 `conditional_parts` + 依赖边 → TASK-001; readiness_rule | INV-3.rule (L35) 现含「2.3 表 dispatch 渲染句·3.3 (a) 行·dispatchable_workflows 字段文档 + TASK-015 CHANGELOG 不提」✓; TASK-011 `conditional_parts` (L291) 三项逐字 ✓, deps 含 TASK-001 ✓; TASK-015 `conditional_parts` (L373) ✓ deps 含 001 ✓; TASK-006 (L179) ✓; `readiness_rule` (L16) 定义 completed(N/A) 视为满足 ✓。**缺**: proposal §3.5 (L198) 「整组从本 spec 删除」+ 「Impact 相应不提」两动作无承载 → 见 M2 | **partial** |
| #10 | A4-PP-m1 v1.66.4 无 tag | TASK-015 补打 | title (L366) 「补打漏掉的 v1.66.4@9e6a17c tag (A4-m1, version-management §4.3) + tag v1.66.5 + 双推 + 逐 remote ls-remote 核验 (失败重试 ≥3 次)」+ deliverables 「tags v1.66.4/v1.66.5 (origin==github)」✓; 实核两远端今日仍无 v1.66.4 | closed |
| #11 | A4-PP-m2 TASK-011 deps 缺 010 / SC-14 脚本无落点 | deps 加 010; 落点 `tests/test_doc_sync_no_run.py` | deps (L288) = [006, 007b, **010**, 001] ✓; verification (L302) 给路径 ✓ (残: 该测试断言主仓文件, 需 parents[4]+skip 先例, 见 m1) | closed |
| #11 | A4-PP-m4 「直调不可达」反义 + TASK-010 悬空引用 | 改措辞 | L284 「直调时无计数, 读者按 message 处置」与 proposal L190 语义同 ✓; TASK-010 verification (L278) 「§C.2.4 处方段被 2.5 引用」仍在 011 之前执行 (锚点悬空一步, 同 agent 顺序落, 风险低, 不再单列) | closed |
| #11 | A4-PP-m5 metadata.dispatch_viable 占位 / TASK-002 test_ci_backends 歧义 | 加占位; 改措辞 | L11 `dispatch_viable: null` + 注释 ✓; TASK-002 deliverables (L106) 「实核 _normalize_pr_ci_status 测试 6 处全在此文件, test_ci_backends.py 不动」— 今日复核 grep 仍 6 处且仅 test_pre_merge_gate.py ✓ | closed |
| #11 | A4-PP-m6 dispatchable 字段文档无承载 | 并入 TASK-011 conditional_parts | L291 「SKILL.md :183 + schema 的 path_coverage.dispatchable_workflows 字段文档 — false ⇒ 不写」✓ | closed |
| #6 (共) | A4-PP-m3 traps 三写者 / :241 | 建节权 001; 011 上方插四行不双写; 014 末尾追加 + 终改 :241 | TASK-001 verification (L89) / TASK-011 title+verification (L284, L300 「TASK-0a 行保持 TASK-001 原文 (不双写)」) / TASK-014 title+notes (L346, L359) 三处互相一致 ✓ (残: 014 deliverables 未列 SKILL.md, 见 m3) | closed |

r1_closed = 6, r1_partial = 1, r1_not_addressed = 0。

## Findings

### [A4-code-reviewer-PP2-M1] TASK-003 (§1+§2.2 核心实现) 在 `dependencies` 图上对下游几乎不可达 — 顺序只编码在 execution_order 散文, 与 readiness_rule / exec_order_note / parallel_tracks 三条自定义规则矛盾 (ordering · fresh)

- **锚点**: TASK-005 `dependencies: [TASK-004]` (L159) · TASK-006 `[TASK-005, TASK-001]` (L176) · TASK-010 `[TASK-009]` (L268) · TASK-014 `[TASK-009, TASK-010, TASK-011]` (L350) · `readiness_rule` (L16) · `exec_order_note` (L14) · `parallel_tracks.note` (L430) · `execution_order` (L434-436)
- **实测** (脚本算传递闭包): TASK-005 / 006 / 007a / 007b / 010 / 011 / 012 / 014 的依赖闭包**均不含 TASK-003 (也不含 TASK-002)**; 只有 TASK-013 与 TASK-015 传递可达。v2 把 TASK-004 deps 从 [TASK-003] 改成 [TASK-000] (A1-M4 修法正确) 之后, TASK-005 仍只挂 004, 于是整条 gate 轨自 005 起与 003 断链; 散文 `execution_order` 「TASK-004 → TASK-002 → TASK-003 → TASK-005 → TASK-006」是唯一写有该序的地方。
- **后果** (三处 verification 在图上「就绪」时结构上不可通过):
  1. TASK-006 verification 「SC-5/SC-10 翻绿」: SC-5 (a)(b)(c1)(d) 全部要求 `gate_error` 从 compute_verdict 流出 + `raw_message == gate_error.message`, 这由 TASK-003 产出; TASK-006 的 `if out.get("gate_error")` 回填段在 003 未落时恒不触发。
  2. TASK-010 verification 「config-template-key-currency 探针 PASS (两 key ⊆ DEFAULT_CONFIG)」: 实读 `.aria/probes/config-template-key-currency.py:60-78` — 它 `sys.path.insert(0, "aria/skills/phase-c-integrator/scripts")` 后 `import pre_merge_gate` 并断言模板键 ⊆ `pmg.DEFAULT_CONFIG`; `no_run_prompt_after_observations` 进 DEFAULT_CONFIG 是 TASK-003 的 deliverable (L116)。helper 轨声称「与 gate 轨并行, 文件域 disjoint」, 但 TASK-010 写主仓模板的**正确性**跨轨依赖 TASK-003 —— yaml 自己在 TASK-003 verification (L130) 已承认这点 (「TASK-010 补模板前先用合成模板验」), 却没把边画出来。
  3. TASK-014 活体 「实测 pr_ci_status=not_found + kind」: 没有 §1 (aether.py `not_found`) 与 §2.2, gate 对零 run 仍返 pending, 活体必然失败; 且 execution_order 写「TASK-012 ∥ TASK-013 → TASK-014」而 TASK-014 deps 不含 012/013 (与散文再矛盾一处)。
- **为什么是 Major**: 本文件把 `exec_order` 明写为 advisory tie-break、`readiness_rule` 明写为按依赖 status 判就绪、两轨明写可并行 —— 三条规则叠加后, 「按 yaml 执行」的合法调度里存在 TASK-006 GREEN 先于 TASK-003 的路径 (同 A3-PP2-M1 指出的 TASK-004 形状: 散文修复掩盖机检字段未改)。这不是 TDD 红绿失效的 fail-open, 而是依赖图欠定致实施者分叉 (Major 判据第二/三项)。
- **建议** (4 行): TASK-005 `dependencies` 加 TASK-003 (传递修复 006/007a/007b/011/012/014/015); TASK-010 `dependencies` 加 TASK-003, 并在 `parallel_tracks.note` 补一句「helper 轨 TASK-010 的模板两 key 跨轨依赖 TASK-003 (DEFAULT_CONFIG 注册), 其余 helper 任务不依赖 gate 轨」; TASK-014 `dependencies` 加 TASK-013 (或把 execution_order 那句改成与 deps 一致)。修后重跑闭包脚本断言 TASK-003 ∈ closure(TASK-006/010/014)。

### [A4-code-reviewer-PP2-M2] INV-3 把 proposal §3.5 的「整组**从本 spec 删除**, Impact/CHANGELOG 相应不提」转录成「整组**不做**」 — false 分支下 proposal.md 自身的删除动作与 Impact 行零任务承载 (transcription · coverage; R1 A4-M1 残留半边)

- **锚点**: proposal §3.5 L198 末句 「**若 false: … 整组从本 spec 删除** (不留零消费方字段/常量, R4 A1-m6), Impact/CHANGELOG 相应不提」· §4 标题 L200 「false 则本节整段删除」· Impact L255-256 (`path_coverage` +`dispatchable_workflows` / `DISPATCH_VIABLE` 常量) · yaml INV-3.rule L35 「整组不做」· TASK-015 `conditional_parts` L373 (仅 CHANGELOG) · TASK-016 title L386 (仅 Status → Complete)
- **实测**: `grep -n "proposal\|Impact\|从本 spec 删除" detailed-tasks.yaml` — INV-3 / 五个条件字段 / TASK-016 均无「false ⇒ 编辑 proposal.md」动作; R1 聚合簇 #2 列的「Impact/CHANGELOG 不提」只落了 CHANGELOG 半边。
- **后果**: dispatch_viable=false 时, 归档进 `openspec/archive/` 的 proposal 仍含 §4 整段 + SC-8「红」+ SC-9 dispatchable 子句 + SC-2 子项 + SC-5 (c2) + 3.3 (a) 行 + Impact 两条 additive 字段 —— 读者看到 SC-8 是一条从未翻绿的验收标准, 与 `sc_coverage_crosscheck.SC-8` 「(条件)」三字对不上; INV-6 「SC-1..16 全部有承载」在 false 分支不成立 (SC-8 唯一承载是两条 N/A 任务)。spec 明文的自我修剪动作 (R4 A1-m6 裁定「不留零消费方字段/常量」, 对文档同样适用) 蒸发 — 正是 §7 想防的形状。
- **建议** (2 行): TASK-001 verification 加一条 「false ⇒ 同批按 §3.5 清单编辑 proposal.md: 删 §4 整段 / SC-8 / SC-9 dispatchable 子句 / SC-2 dispatch 子项 / SC-5 (c2) / 3.3 (a) 行 / Impact 的 dispatchable_workflows 与 DISPATCH_VIABLE 两项, 在 §3.5 末留一句 `dispatch_viable=false (TASK-0a <date>, 证据 traps §六) ⇒ 上列整组已删`; `sc_coverage_crosscheck.SC-8/SC-9` 同步标 N/A」; INV-3.rule 「整组不做」改回「整组从本 spec 删除 + 不做」。(也可落 TASK-016, 但 TASK-001 是裁决点, 同批改最不易漏。)

### [A4-code-reviewer-PP2-m1] SC-14 机检脚本落在 aria 测试目录, 却要断言主仓文件 (config.template 两 key / DEC 前向指针) — 需点名 parents[4] + 仓外 skip 先例; 且测试文件不在 TASK-011 deliverables (executability)

- **锚点**: TASK-011 verification L299 (「config.template 两 key」「DEC 文末」) + L302 (`aria/skills/phase-c-integrator/tests/test_doc_sync_no_run.py`) vs deliverables L293-297 (无该测试文件)
- **实测**: phase-c-integrator/tests 现有三 py 文件均不引用主仓路径; 仓内唯一先例是 `state-scanner/tests/test_spec_complete.py:94-104` (`Path(__file__).resolve().parents[4]` 走到 meta-root, 不存在时 `skip` 非 fail)。aria-plugin 可被 standalone clone (GitHub 镜像), 无 skip 的测试在那里红。
- **建议**: TASK-011 deliverables 加该测试文件; verification 加「主仓文件断言沿 test_spec_complete.py parents[4] + skip-outside-meta-repo 先例」。

### [A4-code-reviewer-PP2-m2] aria 子模块 feature 分支无任务创建/命名; 主仓分支「B.1 起」写在 exec_phase C 的 TASK-015 里 (executability · fresh)

- **锚点**: TASK-015 title L366 「(i) … 本地 --no-ff merge」(被合分支名未出现在全文) · 「(ii) 主仓: B.1 起 feature/152-no-run-for-branch 分支」· TASK-000 deliverables L63-65 (仅 claim + fetch)
- **实测**: `phase-b-developer/SKILL.md:58,108-117` B.1 branch-manager 只建**主仓**功能分支; aria 子模块分支 (在 9e6a17c 起, proposal L30 「Phase B 在 9e6a17c 起分支」) 无任何任务/步骤承载, TASK-003 INV-1 有向检查的「父提交」也依赖它存在。
- **建议**: TASK-000 deliverables 加「aria 子模块 `feature/152-no-run-for-branch` @ 9e6a17c + 主仓同名分支 (B.1)」; TASK-015 (i) 写明被合分支名。

### [A4-code-reviewer-PP2-m3] TASK-014 deliverables 缺 SKILL.md (:241 终计数只在 title/notes); 「N 条坑」计数口径未定 (fresh)

- **锚点**: TASK-014 title L346 「traps :241 终计数」/ notes L359 「改 SKILL.md :241 「N 条坑」终计数」 vs deliverables L353-355 (traps + telemetry 两项)
- **实测**: SKILL.md :241 现文 「半页, 7 条实测踩出来的坑」; traps 五节**无编号**, 「7」是散文计数。§六 终态 = F3/F4/(b)/F6 + TASK-0a 行 + SC-13 证据行 (6 条), SC-13 证据行是否算「坑」无口径 ⇒ 终值 12 或 13 两读。
- **建议**: TASK-014 deliverables 加 `phase-c-integrator/SKILL.md (:241)`; notes 一句「计数 = 各节坑条目 (证据行不计)」或反之。

### [A4-code-reviewer-PP2-m4] 补证 A3-PP2-M1 (不重复计数): exec_order tie-break 实算把 TASK-002 排在 TASK-004 前 (ordering)

- 脚本按 `readiness_rule` 取 TASK-000 完成后的就绪集 = {TASK-001, TASK-002, TASK-004, TASK-008}; 按 `exec_order_note` 的 tie-break 升序 = 001 (1) → 002 (2) → 004 (4), 与 `parallel_tracks.tracks[0]` / `execution_order` 的 004 首位矛盾; `parent: P2` 亦晚于 P1。修法同 A3: TASK-004 exec_order 改 2 并整体重排 (或物理前移 + parent 注记「P 为关注域非时序」)。随 M1 一起修 (同一形状: 散文改了, 机检字段没改)。

## 已核验无误

- **INV-3 条件组 ↔ proposal §3.5 清单逐项**: §4 整段 → 007a/b `conditional_on` ✓ · SC-8 ✓ · SC-9 dispatchable 部分 ✓ (crosscheck 注「false 时基线行为由既有 test_path_coverage 守」合理) · `DISPATCH_VIABLE` 常量 → 007b ✓ · 2.3 表 dispatch 渲染句 → 007b (代码) + 011 (文档) ✓ · SC-2 dispatch 子项 → 007a/b ✓ · SC-5 (c2) → 007a/b ✓ (007a 在 006 之后落但 (c2) 需 dispatch 行才含 `feat/x`, 至 007b 前仍红, TDD 配对成立) · 3.3 (a) 行 → 011 ✓ · §2.1 `.replace` → 006 `conditional_parts` (且明写 (c1) 守卫保留、raw_message 同步无条件) ✓ · CHANGELOG → 015 ✓; 仅「从本 spec 删除 + Impact」缺 (M2)。
- **TASK-015 三项**: 补打 v1.66.4@9e6a17c ✓ (两远端实核仍缺, 非陈旧) · 主仓 feature 分支承载 5 类改动 + 「非 scoped add」+ 不带路径 git status ✓ · 双 remote (origin **与** github) ls-remote + 重试 ≥3 ✓ · 「local master == origin == github」断言 ✓ · Forgejo merge 例外仅主仓 (硬约束 1 原文) ✓ · 14 版本点行号 CLAUDE.md:139/:141 · VERSION:24 · README.md:8/:242 · i18n ×3 :3/:10/:244 今日 grep 全为 1.66.4 且位置同 ✓ · custom checks 10 ✓。
- **TASK-011**: deps 含 010 ✓; 「直调时无计数」✓; SC-14 落点给出 ✓ (m1 残); dispatchable 字段文档 ✓; traps 「不双写」✓; INV-5 grep ✓。
- **metadata**: `dispatch_viable: null` 占位 + 注释 ✓; `readiness_rule` 与 TASK-007a/b `conditional_on` 的 completed/N/A 措辞一致 ✓; `audit_checkpoints_note` 四检查点 off 留痕 ✓ (Rule #10 白名单第一类)。
- **TASK-002**: deliverables 「6 处全在 test_pre_merge_gate.py, test_ci_backends.py 不动」今日 grep 复核属实 ✓。
- **INV-1 有向检查** (L30/L128): 「父提交上 `_normalize_pr_ci_status([]) == 'pending'` 且本 commit 同含两文件」对「先单独落 aether.py」能红 ✓; 验证者 main-loop 与 parallel_tracks.note 「子 agent 不 commit」一致 ✓。
- **TASK-008 ↔ SC-11 (d)** 13 个子断言逐项对照 (含 R1 补的两条 reset 成功路径、缺 --source/--state-file exit 2、record verdict≠wait 缺失文件 exit 2) 全部在 title ✓; TASK-009 CLI 签名与 §3.1 封闭签名逐项同 ✓。
- **yaml 机械自洽**: 见摘要 (18/49/8/exec_order 唯一/carries_sc↔crosscheck/agent_summary↔tasks 全 ✓); `checklist_s7_mapping` 四项落点实存 ✓; 无 1.66.3/1.66.4 陈旧目标引用 (baseline 9e6a17c / target 1.66.5) ✓。

## Verdict

**PASS_WITH_WARNINGS** — vote **REVISE**。R1 归我席 7 条 6 closed 1 partial, v2 方向正确; 但新鲜眼睛抓到一条结构性 Major (M1: TASK-003 在依赖图上对 006/010/014 不可达, 顺序只活在散文 — 与 A3-PP2-M1 同形状, 「散文修复掩盖机检字段未改」在 v2 出现了两次, 按 memory `fix_the_class_not_the_instance` 建议一次把 dependencies 与 execution_order 做机械一致性核对后再提 v3) + 一条 R1 残留半边 (M2: false 分支 proposal 自删无承载)。两条合计 <10 行, 四条 Minor 可同批吸收; 修后可进 B.1。
