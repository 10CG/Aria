---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T13:51:06.596Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A1-tech-lead
critical_count: 0
major_count: 3
minor_count: 8
---

# post_planning R2 — A1 席 (tech-lead) · pre-merge-gate-no-run-for-branch (v2)

## 摘要

透镜同 R1 (不变量编码 / 依赖 DAG / 分轨 / 流程契约)。**C1 已实测闭环** —— `readiness_rule` +
`completed`/`N/A —` 取代 `skipped` 的处方经合成 yaml 实跑证实: 归档门 `complete: true`,
`d_payload.deferred_items` 为**空** (v1 的假 carry-forward 消失)。INV-3 四落点、TASK-007a/b 拆分、
traps 三写者序、TASK-015 主仓面、14d 时窗、我的 7 条 minor 中 5 条也已闭。

**但 v2 的两个修复各自造出一个新的排序缺陷** (memory `fix_recurs_in_its_own_fallback_path` /
`fixes_contradict_each_other_across_clusters` 的形状, 且两处的源头都是我 R1 提的处方):

1. `TASK-004.dependencies` 从 `[TASK-003]` 改成 `[TASK-000]` 解了「守卫自证快照」, 但**同时切断了
   TASK-003 唯一的传递入边链**: 实测 TASK-012 / TASK-014 的依赖闭包里**没有 TASK-003** (v1 经
   011→006→005→004→003 可达)。SC-13 活体与 SC-15 AB 真跑现在可以在 `not_found` 根本没实现时被判就绪。
2. 「TASK-004 exec_order 前移到 2 之前」写进了 R1 处置表, 但**数字没改** (仍 4, 排在 002=2 / 003=3
   之后), 而 `execution_order` / `parallel_tracks` 轨内序 / `TASK-004.notes` / `tdd_note` 四处散文
   都说守卫先落 —— 唯一的数字信号与四处散文互斥, 且 `dependencies` 里**零条边**强制这个顺序。

第三条 Major 是 R1-M7 的半闭: 主仓交付面全列上了 ✅, 但「B.1 起 feature 分支」被塞进
`exec_phase: "C"` / `exec_order: 16` 的 TASK-015 (字面自相矛盾), 而 **aria 子模块侧的分支创建仍
零任务承载** —— 全部代码落在那个仓里。

无 Critical。三条 Major 的修法都是一行级 (改一个数字 / 补三条边 / 把建分支挪回 TASK-000)。

---

## R1 处置核对

R1 聚合 12 簇中归本席 (或含本席条目) 的 9 簇 + 我的 7 minor:

| R1 簇 / 条目 | v2 落点 | 核对 (实测) | 判定 |
|---|---|---|---|
| #1 **A1-C1** `skipped` 非 done-family | `readiness_rule` + INV-3 rule (`completed` + `N/A —`) + `dispatch_viable: null` | 合成 yaml 全 completed + 两条 `N/A —` notes 实跑 `spec_complete.py` → `complete: true`, `deferred_items: []`; 负控 (仅 TASK-007a 改 `skipped`) → `complete: false, "1/18 non-done"`。全文 `skipped` 仅剩 `readiness_rule` 里的禁令本身 | **CLOSED** |
| #2 A1-M2 INV-3 四落点 | INV-3 rule 重写 + 006/011/015 `conditional_parts` + 三条 → TASK-001 边 | 逐条比对 proposal §3.5 十项 (§4 整段 / SC-8 / SC-9 dispatchable / DISPATCH_VIABLE / 2.3 渲染句 / SC-2 子项 / SC-5 (c2) / 3.3 (a) 行 / §2.1 `.replace` / CHANGELOG) — **10/10 有承载**; `encoded_as` 的「其余任务无条件」已删; 006/011/015 deps 均含 TASK-001 (实测) | **CLOSED** (负控缺, 见 m2) |
| #2 A1-M1 下游就绪性 | `readiness_rule` | `completed(N/A)` 视为已满足, TASK-011/013 对 007b 的边在 false 分支不再停摆 | **CLOSED** |
| #3 A1-M5 TASK-007 RED+GREEN 同任务 | 拆 007a (qa, 2h) → 007b (be, 2h) | agent 分别为 qa-engineer / backend-architect; `carries_sc` RED 侧全在 007a; 007b deps=[007a]; 全文无悬空 `TASK-007` 引用; 18 任务 / 49.0h / 8 parent 三项算术实测自洽 | **CLOSED** |
| #4 A1-M4 守卫前移 + SC-7 拒绝能力 | deps→[TASK-000]; 钉 9e6a17c 入 docstring; SC-7 加多/少一键 mutation | 前三项 ✅; **`exec_order` 未改 (仍 4)** 且新造闭包断链 | **PARTIAL** → M1 / M2 |
| #5 A1-M3 INV-1 有向检查 | INV-1 `encoded_as` + TASK-003 verification 改「父提交上 `==pending` 且本 commit 同含两文件」 | 维度对了: 拆成两 commit 时, 对任一 commit 跑该检查都红 (父提交已返 `not_found` / 本 commit 不含两文件) — 时序敏感成立 | **CLOSED** (归属残余见 m1) |
| #6 A1-M6 traps 三写者 | TASK-001 建节 + TASK-011「上方插入, 不动 TASK-0a 行」+ TASK-014 末尾追加并终改 `:241`; TASK-011 deps 补 001 | 三处措辞互相点名, 顺序无环; verification 有「TASK-0a 行保持原文 (不双写)」 | **CLOSED** |
| #7 A1-M7 主仓 5 类 + B.1 分支 | TASK-015 (ii) 列全 5 类 + 主仓 feature 分支 + 不带路径 git status | 5 类齐 ✅、双 remote + 重试 ✅、git status ✅; **分支创建放在 exec_phase=C**, aria 侧仍零承载 | **PARTIAL** → M3 |
| #12 A1-m1 schema 偏离 | 处置表写「parent 沿 #179 保留 / estimated_hours 沿先例 / agent_reason 逐任务」 | metadata **无 `schema_note`**; `agent_reason` 实测只 **7/18** 任务有, 且写在 notes/verification 串里非 `reason:` 字段 | **PARTIAL** → m4 |
| A1-m2 粒度 | `estimation_note` | 在 | **CLOSED** |
| A1-m3 exec_order 读法 | `exec_order_note` | 在 (但恰因「advisory」使 M1 的数字矛盾更易被执行者踩) | **CLOSED** |
| A1-m4 TASK-002 歧义 | deliverable 改「6 处全在此文件, test_ci_backends.py 不动」 | 在 | **CLOSED** |
| A1-m5 ls-remote 双 remote + 重试 | TASK-015 verification | 「origin **与** github ls-remote 全一致, 失败重试再判」+ merge 前三者一致 | **CLOSED** |
| A1-m6 Rule #10 留痕 | `audit_checkpoints_note` | 实读 `.aria/config.json`: `mid_implementation/post_implementation/pre_merge/post_closure` 四个确为 `off`, `post_planning: convergence` — note 字面属实 | **CLOSED** |
| A1-m7 14d 时窗 | TASK-016 verification | 「须在 TASK-014 production 记录 14 天内; 超窗 ⇒ 重跑活体, 不得手工补记录」 | **CLOSED** |

**计**: closed 11 / partial 3 / not_addressed 0。

---

## Findings

### [A1-PP2-M1] `TASK-004.exec_order` 未按 R1 处置前移 —— 唯一的数字排序信号与四处散文互斥, 且 `dependencies` 零边兜底

- **锚点**: `TASK-004.exec_order: 4` vs `TASK-002.exec_order: 2` / `TASK-003.exec_order: 3` ·
  `execution_order[1]` · `parallel_tracks.tracks[0].tasks` · `TASK-004.notes` · `metadata.tdd_note`
- **问题**: R1 聚合处置表 #4 明写「exec_order **前移到 2 之前** (gate 轨首位)」。v2 改了 `dependencies`、
  钉了 SHA、补了 SC-7 mutation, 唯独**数字没动**。现在同一份文件里四处说守卫先落、一处数字说守卫第三:

  | 编码面 | 说的顺序 |
  |---|---|
  | `execution_order[1]` | `TASK-004 (守卫@基线) → TASK-002 → TASK-003 → …` |
  | `parallel_tracks` gate 轨 `tasks:` 列表 | `[TASK-004, TASK-002, TASK-003, …]` |
  | `TASK-004.notes` | 「守卫必须先于 TASK-003/006 落 (A1-M4: 守卫落在变更之后会退化成自证快照)」 |
  | `metadata.tdd_note` | 「守卫 (GUARD) 任务钉基线 SHA 9e6a17c 且**在被守护变更之前**落」 |
  | **`exec_order` 字段** | 002 (2) → 003 (3) → **004 (4)** ← 守卫排在被守护的变更之后 |

- **实测** (机械抽 18 任务的 `exec_order`/`dependencies`): `TASK-002.dependencies: [TASK-000]`,
  `TASK-003.dependencies: [TASK-002]`, `TASK-004.dependencies: [TASK-000]` —— **`dependencies` 里没有
  任何一条边强制 004 先于 002/003**。而 `readiness_rule` 定义就绪只看 `dependencies`, `exec_order_note`
  又把 exec_order 降为 advisory tie-break。⇒ 一个只读机读字段的执行者 (含无人值守 Layer 2) 会得到
  002 → 003 → 004, **正是 R1-M4 要根治的「守卫落在被守护变更之后」**。
- **为什么不是 Critical**: `TASK-004.verification` 把基线钉成了 SHA (「在 9e6a17c 绿, 钉 SHA 入 docstring」),
  即使晚落也仍可在 9e6a17c 上验证, 快照恒绿的伤害被这条兜住 —— 但 R1 处置表承诺的那一半没落。
- **建议** (二者都做, 缺一仍留缝):
  (a) `TASK-004.exec_order: 4 → 1.5` (与 `exec_order_note` 的 advisory 语义相容, 且与 helper 轨的
      9/10/11 不冲突); 其余任务编号不动;
  (b) 把顺序落进承重字段: `TASK-002.dependencies: [TASK-000, TASK-004]` (同轨串行, 不损并行度 —— 两者
      同写 `test_pre_merge_gate.py`, 本就必须串)。

---

### [A1-PP2-M2] v2 解掉 `TASK-004 → TASK-003` 那条边后, **TASK-003 从 TASK-012 / TASK-014 的依赖闭包中消失** (TASK-010 同型, 既有)

- **锚点**: `TASK-004.dependencies` (v1 `[TASK-003]` → v2 `[TASK-000]`) · `TASK-012.dependencies:
  [TASK-010, TASK-011]` · `TASK-014.dependencies: [TASK-009, TASK-010, TASK-011]` ·
  `TASK-010.dependencies: [TASK-009]` · `parallel_tracks.note` (两轨 disjoint 可并行)
- **实测** (对 18 任务 16 条边跑传递闭包):

  | 任务 | 闭包是否含 TASK-003 | 它凭什么需要 TASK-003 |
  |---|---|---|
  | TASK-012 (SC-15 AB 真跑) | ❌ **不含** (也不含 TASK-002) | verification 是「回退本 spec 代码后 `test_case_in_unit_tests` 指向的测试**转红**」—— 那条测试是 TASK-002 写、TASK-003 才翻绿的 |
  | TASK-014 (SC-13 活体) | ❌ **不含** | 活体要实测 `pr_ci_status=not_found` + kind, 这两样都由 TASK-003 (§1 backend + §2.2 分支) 产生 |
  | TASK-010 (config.template 两 key) | ❌ **不含** | verification 是「`config-template-key-currency` 探针 PASS (两 key ⊆ DEFAULT_CONFIG)」, 而 `no_run_prompt_after_observations` 进 `DEFAULT_CONFIG` 是 **TASK-003** 的交付物 |
  | TASK-013 / TASK-015 / TASK-016 | ✅ 含 | — |

  v1 的闭包靠 `TASK-011 → TASK-006 → TASK-005 → TASK-004 → TASK-003` 兜住 (R1 报告已记录这条链);
  v2 为治 M4 把 004 的入边换成 000, 链断在这里。**这是修复自身引入的缺陷**, 不是 v1 遗留。
- **TASK-010 那一路是 v1 就有的、我 R1 漏掉的**: 实读 `.aria/probes/config-template-key-currency.py`
  —— `unknown = set(模板段) - set(pmg.DEFAULT_CONFIG) - {"_comment"}`, 非空即 `FAIL` (severity warning,
  `enabled: true`); 探针从 `aria/skills/phase-c-integrator/scripts` **实读子模块工作树**的 DEFAULT_CONFIG。
  实跑当前基线 → `OK (8 keys, 0 deprecated, 0 unknown)`; 实测模板段现缺 `path_coverage_enabled`,
  DEFAULT_CONFIG 现无 `no_run_prompt_after_observations` ⇒ TASK-010 若先于 TASK-003 落, 探针立刻 FAIL。
  这同时说明 `parallel_tracks.note` 的「两轨**文件域** disjoint」在**验证面**不成立: helper 轨末端
  TASK-010 的验收条件由 gate 轨 TASK-003 的产物决定。
  (附: TASK-003 的 verification 写「TASK-010 补模板前先用**合成模板**验」—— 实读探针确有
  `--template PATH` 旗标, 这句**可执行** ✅, 但它只解决 TASK-003 自己那一侧, 不解决 TASK-010 的方向。)
- **后果**: 按 `readiness_rule` 字面 (就绪 = `dependencies` 全 done), TASK-014 可在 `not_found` 尚未实现时
  开跑 —— 活体必失败, 而失败信号长得像「Forgejo 又抽风」, 最坏结果是执行者把 SC-13 判成环境问题跳过。
- **建议**: 补三条边 (纯 additive, 不改任何并行结构, 因为 013/015 已在同一汇合点):
  `TASK-010.dependencies: [TASK-009, TASK-003]` · `TASK-012.dependencies: [TASK-010, TASK-011, TASK-013]`
  (或直接加 TASK-003) · `TASK-014.dependencies: [TASK-009, TASK-010, TASK-011, TASK-013]`。
  并在 `parallel_tracks.note` 补一句「两轨在 TASK-010 处有一条**验证面**耦合 (模板键 ⊆ DEFAULT_CONFIG),
  故 TASK-010 须在 TASK-003 之后」。

---

### [A1-PP2-M3] B.1 分支创建: 主仓那半被放进 `exec_phase: "C"` 的 TASK-015 (字面自相矛盾), **aria 子模块那半仍零任务承载**

- **锚点**: `TASK-015.exec_phase: "C"` / `exec_order: 16` / title 「(ii) 主仓: **B.1 起**
  feature/152-no-run-for-branch 分支承载全部主仓改动」· `TASK-000.exec_phase: "B.1-entry"` (只做 claim) ·
  `TASK-001.exec_phase: "B.1-前置"` (只做探针) · `metadata.baseline_sha: "9e6a17c"`
- **问题 (主仓侧)**: 「B.1 起分支」这句话写在一个 Phase C、`exec_order: 16` 的任务里。按任何一种读法都
  自相矛盾: 若真在 TASK-015 才建分支, 那么 TASK-010 (config.template + .gitignore) / TASK-011 (DEC) /
  TASK-012 (ab-suite + ab-results) / spec 目录 yaml 这四类主仓改动, 在 exec_order 11-13 期间是落在
  **master 工作树**上的; 而 `parallel_tracks.note` 明写「主控统一提交」—— 主控一旦在中途提交, 就直接
  提交到了共享 master (memory `sync_instruction_not_push_authorization`: 推共享 master 需显式授权,
  「低风险 doc」不能自我授权)。
- **问题 (aria 侧, 更硬)**: 本 spec **全部代码**落在 aria 子模块。proposal 明写「Phase B 在 `9e6a17c`
  起分支」, metadata 也记了 `baseline_sha`, 但**没有任何任务的 deliverables 说「创建 aria feature 分支」**。
  TASK-015 (i) 直接写「本地 `--no-ff` merge (禁 Forgejo 服务端合并)」—— merge 一个从未被任何任务创建的分支。
  实测: 18 个任务的 deliverables 全文 grep 无 `feature/` 出现在 TASK-015 之外。
- **十步循环层面**: B.1 = 分支创建 (CLAUDE.md 核心概念)。现在 B.1 只剩 claim (TASK-000) + 探针 (TASK-001),
  分支这一步在两个仓里都没有承载 —— 这是 Phase 级的覆盖缺口, 不是措辞问题。
- **建议**: `TASK-000.deliverables` 补两条 (它已经是 `exec_phase: "B.1-entry"`, 归位天然):
  `"aria 子模块 feature/152-no-run-for-branch @ 9e6a17c (git switch -c; 起点 SHA 写进 commit message)"` +
  `"主仓 feature/152-no-run-for-branch @ 当前 master (承载 config.template/.gitignore/DEC/ab-suite/ab-results/spec yaml)"`,
  估时 0.5 → 1h; TASK-015 title (ii) 的「B.1 起 … 分支」改成「在 TASK-000 建的主仓 feature 分支上收口」。

---

### [A1-PP2-m1] INV-1 的有向检查仍挂在一个不提交的 agent 的任务上, 无 main-loop 侧承载

`TASK-003.verification[1]` = 「INV-1 有向检查 (**main-loop 提交时**): …」, 但 TASK-003 的
`agent: backend-architect`, 而 `parallel_tracks.note` 明写「子 agent 不 commit」。v2 把执行者写进了
括号 (比 v1 好), 但**没有任何 main-loop 拥有的任务 (000/001/012/014/015/016) 的 verification 提到 INV-1**
—— memory `delegate-verify` 的三问里「失败会发红吗」仍无着落。建议: 在 `TASK-015.verification` 或
`TASK-013.verification` 加一条「B.2 commit 序列上 INV-1 有向检查通过 (逐 commit: 触 `aether.py` 的
commit 集 ⊆ 触 `pre_merge_gate.py` 的 commit 集)」, 由主控在 ship 前跑一次。

### [A1-PP2-m2] 三处 `conditional_parts` 无可 grep 负控; §7 checklist 1 在 false 分支静默蒸发

R1-M2 的建议里包含「TASK-011 `verification` 加一条可 grep 的负控 (false 分支: SKILL.md 步骤 6 处方段
不含 `dispatches`)」。v2 落了 `conditional_parts` 字段 (结构性那半 ✅), 但 006/011/015 三处都**没有
任何 verification 检查该字段被遵守** —— false 分支下写文档的 knowledge-manager 若照抄 proposal 3.3,
(a) 行会留下且无人发红 (proposal §3.5 明禁「不留零消费方字段/常量」)。另: `checklist_s7_mapping.1`
指向 `TASK-007b.verification` (DISPATCH_VIABLE 裸全局), false 分支下 007b 整任务 N/A ⇒ 该 checklist
项无承载, 而 INV-6 说 §7 四项「不得蒸发」—— 需要一句「1 随条件组一并 N/A」的声明。
建议: TASK-011 加 `"false 分支负控: grep SKILL.md 步骤 6 处方段与 2.3 表, 零处出现 dispatches"`;
TASK-006 加 `"false 分支: grep pre_merge_gate.py 零处 .replace(\"<pr_branch>\""`; INV-6 补一句。

### [A1-PP2-m3] proposal §3.5 的「整组从**本 spec 删除**」只落了「不做」那半, 文档侧零承载

§3.5 原文是「整组**从本 spec 删除**」+「Impact/CHANGELOG 相应不提」。v2 的 INV-3 把它转写成「整组
**不做**」, 于是 false 分支下归档进 `openspec/archive/` 的 proposal 仍会带着 §4 整段、SC-8/SC-9、
SC-2 dispatch 子项、SC-5 (c2)、2.3 dispatch 行、3.3 (a) 行 —— 描述一个从未实现的能力 (Rule #3
文档与代码同步)。CHANGELOG 那一项有承载 (TASK-015 `conditional_parts`) ✅, proposal 本身没有。
建议: `TASK-016.deliverables` 补一条「false 分支: proposal §4 / SC-8 / SC-9 / SC-2 dispatch 子项 /
SC-5 (c2) / 2.3 dispatch 行 / 3.3 (a) 行 按 §3.5 删除或就地标 `N/A (dispatch_viable=false)`, 再归档」。

### [A1-PP2-m4] `agent_reason` 只覆盖 7/18, 且仍非 schema 字段; metadata 无 `schema_note`

R1 处置表 #12 写的是「agent_reason **逐任务**」。实测有 `agent_reason` 字样的任务 = 003 / 004 / 007a /
007b / 008 / 012 / 014 共 **7 个**, 其余 11 个 (含全部 main-loop 任务与 010/011 两个文档任务) 没有;
且它写在 `notes:` / `verification:` 的字符串里, 不是 `DUAL_LAYER_SPEC.md:170` 规定的 `reason:` 字段。
同时 `parent: "P0".."P7"` (路径 B 不应有) 与 `estimated_hours` 用 int/float (SOT 规定 string 范围)
两处偏离**仍无 `metadata.schema_note` 声明** —— 处置表写的「沿 #179 先例保留」这条理据没进文件, 下一个
读者 (含 R3 席与 Layer 2) 无法区分「有意偏离」与「疏漏」。建议: 补 `schema_note` 一行, 并把缺的 11 条
`agent_reason` 一次补齐 (成本近零, 收益是 A.3 分配可复核)。

### [A1-PP2-m5] TASK-012 钉死的绑定名在生产它的 TASK-002 里没有承诺

`TASK-012.notes`: 「`test_case_in_unit_tests` 绑定名约定 = TASK-002 的
`NotFoundVerdictTests.test_trigger_matched_message`」。实测全文 grep: 该方法名**只出现在 TASK-012 的
notes 里**; TASK-002 的 deliverables 只说「新 `NotFoundVerdictTests` / `ThresholdTests`」, 不含方法名。
⇒ 写测试的 qa-engineer 无从得知这个名字承重 (它是 SC-15 catalog 条目的绑定目标, 改名即 AB 条目悬空)。
建议: TASK-002 deliverables 显式点名该测试方法。

### [A1-PP2-m6] SC-14 机检脚本 `test_doc_sync_no_run.py` 不在任何 deliverables, 且由 knowledge-manager 写测试

该文件只出现在 `TASK-011.verification[3]`, 不在 TASK-011 (或任何任务) 的 `deliverables:` 列表里 ——
按 memory `scoped_git_add_splits_claim_from_landing` 的形状, 不在交付物清单的产物最容易「声称已做但
从未提交」。另两点: (i) TASK-011 的 agent 是 knowledge-manager, 而本 yaml 的 A.3 分工是「qa-engineer
写测试」, 这是唯一一处越界; (ii) TASK-013 (SC-12 全量计数) 的依赖闭包**不含 TASK-011** (实测), 所以
它报的 `119+N` 不会包含这个新测试文件。建议: 把该文件加进 TASK-011 的 deliverables 并在 notes 说明
「grep 型文档测试, 归文档任务是刻意选择」, 或改派 qa-engineer; `TASK-013.dependencies` 补 TASK-011。

### [A1-PP2-m7] 补 tag 只补了 v1.66.4, 同类的 v1.66.1 也无 tag

`TASK-015` 采纳 A4-m1 补打 `v1.66.4@9e6a17c`。实测 (本地 `git tag -l` + `git ls-remote --tags` **两个
remote 各一次**): aria 的 v1.66 系列 tag 只有 `v1.66.0` / `v1.66.2` / `v1.66.3`; **`v1.66.1` 与
`v1.66.4` 都缺**, 而 `CHANGELOG.md:51` 有 `## [1.66.1] - 2026-08-16` 条目。memory `fix-the-class`:
修实例必问「这形状还有几个兄弟位置」—— 这里正好有一个。建议: TASK-015 顺带补 `v1.66.1` (定位到
CHANGELOG 对应的 ship commit), 或在 notes 显式声明「v1.66.1 缺 tag 另案, 不在本 spec 处理」。

### [A1-PP2-m8] 归档时 gate `verdict` 必为 `warn` (与 probe 无关), TASK-016 未预告

实跑合成全 completed 的 spec 目录 `spec_complete.py --gate` → 除 runtime_probe 那条外, 还稳定产出一条
`unverified_claims: archive-safety-net-integration-claims-unverified`, 原因是 **TASK-005 的 title 含
「调用」**(「旧名包装关键字**调用**可用」), 命中 `spec_complete.py:325` 的集成类关键词, 于是整个 gate
`verdict` 被抬成 `warn` 并进 `d_payload` (openspec-archive Step 7 会据此开 archive-tracker issue)。
TASK-016 的 verification 只写「gate JSON 显示 **probe** pass」, 没预告这条与 probe 正交的 warn ——
D.2 执行者会面对一个看起来像失败的 gate 输出。建议: TASK-016 notes 加一句预告 (「预期恰一条
integration-keyword warn, 来源 TASK-005 title 的『调用』, 非缺陷」), 或把 TASK-005 title 里的「调用」
改成「调法」等不触发词 (成本最低, 且让 gate 输出干净)。

---

## 已核验无误 (实测; 按 memory `predict-then-measure` 先写预期后跑)

1. **C1 处方真的让归档门通过** (本轮核心): 合成目录 (v2 yaml 全 `pending`→`completed`, TASK-007a/007b
   notes 首词 `N/A —`) → `python3 lib/spec_complete.py <dir>` = `{"complete": true, "reason":
   "detailed-tasks.yaml 全 done (18 task(s), 无 carry-forward/defer 注释)"}`; `--gate` 的
   `d_payload.deferred_items` = **`[]`** (v1 的假 carry-forward 消失)。负控: 同一目录只把 TASK-007a
   改回 `skipped` → `{"complete": false, "…has 1/18 non-done task(s)"}`。**两态对照成立**。
2. **`N/A —` 不会误触 carry-forward 正则**: `carry_forward.py` 的
   `\[(?:carry-forward|TODO|defer(?:red)?|known[ -]gap|PASS-with-note)\b[\s\S]*?\]` 对 v2 全文
   findall = `[]` —— 注意 TASK-007a/007b title 开头的 `[条件: dispatch_viable=true]` 也**不**命中 (token 组不匹配)。
3. **parser 未被 v2 新增字段/字符串搞坏**: `parse_detailed_tasks` 实跑 → `parse_ok=True, "18 task(s)
   parsed"`, 18 个 id/status 全对。特别核: `conditional_on` 串里字面写着 `status: completed`,
   `INV-3.rule` 里也写着 `status: completed` —— 均未被 status 抽取误读 (前者行首键是 `conditional_on:`,
   后者在 `metadata:` 块内被 `_tasks_block_bounds` 排除)。
4. **算术自洽**: 18 任务 = `total_tasks`; `estimated_hours` 逐项求和 = **49.0** = metadata 值;
   P0-P7 = 8 = `parent_task_count`; `agent_summary` 四个 agent 的任务并集 = 18 且与逐任务 `agent:` 字段
   **逐条一致** (qa 6 / be 4 / km 2 / main-loop 6)。
5. **DAG 无环**; 16 条边; 除 M2 点名的三处外, 其余下游任务的闭包覆盖完整 (TASK-013 / 015 / 016 均含 TASK-003)。
6. **INV-3 四落点对 proposal §3.5 十项逐条覆盖** (见 R1 处置核对 #2 行), `encoded_as` 与 `rule` 不再互斥。
7. **`audit_checkpoints_note` 属实**: 实读 `.aria/config.json` → 四个 B/C/D 检查点确为 `off`,
   `post_planning: convergence` ⇒ 不排 B/C/D 审计任务是 Rule #10 白名单第一类, 非漏排。
8. **TASK-003 的「合成模板先验」可执行**: 实读 `.aria/probes/config-template-key-currency.py:36-40`
   —— 支持 `--template PATH`; 当前基线实跑 `OK (8 keys, 0 deprecated, 0 unknown)`。
9. **SC-16 (b) 红窗真红**: 合成目录 `--gate` 的 `runtime_probe` = `{"outcome": "warn", "count": 0,
   "reason": "production telemetry partition missing: .aria/gate-state-telemetry.jsonl"}` + `unverified_claims`
   含 `runtime_probe:record` ⇒ TASK-014 的 (b) 机读断言可执行。
10. **v1.66.4 tag 确实仍缺** (本地 `git describe` = `v1.66.3-15-g9e6a17c`; origin/github 两个 remote
    的 `ls-remote --tags` 都无) ⇒ TASK-015 的补打条款仍必要且正确。
11. **无悬空 `TASK-007` 引用**: 全文 grep `TASK-007\b` 零命中, 拆分后 `sc_coverage_crosscheck` /
    `checklist_s7_mapping` / `parallel_tracks` / `execution_order` 四处引用全部改成 007a/007b。
12. **`checklist_s7_mapping` 四项在目标任务实文可查** (逐条打开): 1→TASK-007b.verification ✅ /
    2→TASK-012.title ✅ / 3→TASK-014.notes ✅ / 4→TASK-008.notes ✅。
13. **INV-1 有向检查的判别力成立** (逐场景推演): 「先单独落 aether.py」拆成两 commit 时, 对后一个 commit
    跑「父提交 `_normalize_pr_ci_status([]) == 'pending'`」为**假** (父提交已改 aether.py), 对前一个
    commit 跑「同含两文件」为**假** —— 两种选法都红, 时序维度匹配 (memory `invariant-dimension` 已闭)。
14. **`skipped` 在全文只剩禁令本身** (`readiness_rule` 第 16 行), 无残留使用。

---

## Verdict

**PASS_WITH_WARNINGS** (0 Critical / 3 Major / 8 Minor) — **vote: REVISE**

R1 的 1C/7M/7m → R2 的 0C/3M/8m: Critical 归零、Major 7→3, 曲线仍在降 (memory
`stop_adding_rounds_when_major_count_flattens` 的加轮判据成立)。但**三条 Major 里有两条是 v2 修复
自身造成的** (M1 = 处置表承诺的数字没改; M2 = 为解 M4 而换掉的那条边同时切断了 TASK-003 的闭包),
第三条 (M3) 是 R1-M7 只落了一半 —— 都属于 memory `fix_recurs_in_its_own_fallback_path` /
`fixes_contradict_each_other_across_clusters` 点名的形状: **逐条吸收后没做条款间交叉一致性检查**。
建议 v3 落完这三条后, 由主控**机械复跑**两项判别式再交 R3, 不要靠阅读判断:
(i) 18 任务依赖闭包中 TASK-003 对 010/012/014 可达; (ii) `exec_order` 排序 == `execution_order` 段
+ `parallel_tracks` 轨内序 (三处一致)。

八条 minor 全部可在同一轮吸收, 单条成本都在分钟级; 其中 m1 (INV-1 无 main-loop 承载) 与 m2
(conditional_parts 无负控) 属于「不修就没有任何东西会发红」的类别, 优先级高于其余六条。
