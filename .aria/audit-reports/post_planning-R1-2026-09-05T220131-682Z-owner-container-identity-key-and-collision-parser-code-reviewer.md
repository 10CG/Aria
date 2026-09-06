---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-05T22:01:31.682Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 — code-reviewer 席 (规格合规 + 双层一致性)

审计对象: commit `60808b2` 的 `tasks.md` (6 组 41 项) 与 `detailed-tasks.yaml` (41 TASK)。依据: 同目录 `proposal.md` v7、`aria/skills/task-planner/DUAL_LAYER_SPEC.md`、`standards/core/ten-step-cycle/phase-a-spec-planning.md`。只审不改; 所有行号均实读 (aria @ `7dd0135`, standards @ `cc864ee`, 主仓 @ `60808b2`)。

## 机械核对结果 (全部通过的项)

- parent ↔ tasks.md 编号: 41 ↔ 41, 双向差集空, 无重复 parent。
- 必需字段 (id / parent / title / status / complexity / deliverables) 41 条齐全; dependencies 全部指向存在的 TASK。
- 工时: 逐条相加 = 84.5h; agent 计数 backend-architect 15 / qa-engineer 16 / knowledge-manager 10 = 41, 与 `metadata.agents` 一致; `total_tasks: 41` 一致。
- 带圈数字 / 希腊字母: 两文件 grep 零命中。
- tasks.md 头部 Scope 三个 SHA 与 `git submodule status` (aria `7dd0135` v1.69.1 / standards `cc864ee`) 及起草时主仓 HEAD (`abb4fd3`, 即 `60808b2` 的父提交) 一致; Level / Status / ship target / ship 形态与 proposal v7 头部、D5、§Impact 一致。
- 引用路径逐一存在: `.aria/decisions/2026-09-05-owner-container-identity-key-rulings.md`、`.aria/repro/handoff-tracks-frozen-2026-09-05.json`、`.aria/triage-comment.md`、post_spec R1–R5 aggregated 五份、五处取值文档、`aria/templates/session-handoff.md` (`:43` 含「设 label 使更可读」句)、`phase-d-closer/tests/test_fetch_gate.py`、`docs/architecture/version-scheme.md`、`tests/test_normalize_snapshot.py`、`tests/test_phase1_gate_advisory.py`。
- 抽查行号锚点全部命中: `collision.py:63` split / `:86` track_to_claim_record / `:143` classify_claims / `:347` Layer H 记录 / `:379-383` 捞回; `handoff_multibranch.py:518-523` dedupe 键 / `:709-716`; `track_board.py:412-417` / `:743-747` / `:778-793` (含 `:783` `_track_to_claim_record`); `identity.py:126-140` 模板 / `:222` `label if label else uuid`; `phase1_gate.py:486` get_identity; `claim_lifecycle.py:377-380` `release_claim_by_track(identity=)`; `session-handoff.md:116` / `:178-186`; a1-entry `proposal.md:571` SC-3; `test_collision.py:158-164`; 全仓 `def test_` 计数 1492 与 4.2 一致。
- SC ↔ 任务映射表与 yaml `verification` 的 SC 引用双向一致; SC-2 (1.2 判定臂+advisory 函数级 / 1.5 端到端 / 1.7 族键)、SC-3 (1.8 S1 / 6.x S2)、SC-9 (1.11 代码 / 3.4 文档 / 3.5 模板) 按子句分割清楚, 无「两任务重复承载同一子句而无主次」。

## 审计结论

### Finding M-1 (Major)
- type: spec-compliance / mechanism-does-not-exist
- severity: Major
- category: 归档门契约
- scope: `tasks.md:8`, `tasks.md:40` (0.1), `detailed-tasks.yaml:7`, `detailed-tasks.yaml:59` (TASK-000 verification), `detailed-tasks.yaml:588`
- summary: 计划依赖「归档门按 `status: deferred-s2` 识别, S2 任务在 S1 下不勾选、不算未完成」, 但该机制在当前 aria `7dd0135` 不存在。
- evidence:
  - `aria/skills/state-scanner/scripts/lib/spec_complete.py:259-297`: tasks.md **存在**时 gate 只读 tasks.md checkbox; 有未勾选即 `complete=false` (除非 proposal Status 归一为 done)。detailed-tasks.yaml 的 status 只在 tasks.md **缺失**时才被读 (`:259` 分支 + `:1569-1576` `_fold_yaml_only_datasource` 同样以 `not tasks_path.is_file()` 门控)。
  - 即便走 yaml-only 路径, `lib/detailed_tasks.py:83` `_DONE_FAMILY = {"done", "completed"}` fail-CLOSED, `:28` 明文「pending/deferred/... counts as residual」; `deferred-s2` 一律算残留。
  - 实跑 `spec_complete.py --gate` 对本 spec 目录: `complete=false, complete_reason="tasks.md has 41/41 unchecked task(s); normalized Status = 'approved'"`, `d_payload.deferred_items` 逐条列出全部 `- [ ]` 行 (S1 归档时 6.1–6.4 四行必然进入 deferred 清单)。
  - `DUAL_LAYER_SPEC.md:164` status 枚举 = pending / in_progress / completed / blocked; `:123-126` 明示新增枚举值前须核对 `_DONE_FAMILY`。
- 后果: S1 (proposal 认为的默认形态) 到 D.2 时, 要么 `complete=false` 归档被 skip (phase-d-closer SKILL.md:75), 要么 (Status 归一 done 放行后) openspec-archive Step 7 自动建 tracker issue 把 4 条 S2 任务当「未完成」上报 —— 与 tasks.md:8 承诺的「不算未完成」相反。
- 建议: 在 A.3 层选一个**真实存在**的机制并写明: (a) S1 下 6.x 勾 `[x]` 并在行内注「S1 形态不适用」(措辞避开 `carry_forward.py:14` 正则命中的 `defer`/`TODO`/`known-gap` 词, 否则又落回 Status 分支); 或 (b) 明写「S1 归档接受 tracker issue 列 4 条 S2 项, 由 5.5 回帖引用」; 或 (c) 另开 Level 1 给 `spec_complete` 加「条件任务不适用」语义 (跨 spec 改 SOT, 不建议塞进本 cycle)。同时把 yaml 计划值从 `deferred-s2` 改回枚举内取值或明写它只是人读标注、不被机器消费。

### Finding M-2 (Major)
- type: dependency-order / release-integrity
- severity: Major
- category: 组 5 发布顺序
- scope: `detailed-tasks.yaml:498-533` (TASK-034 → TASK-035), `detailed-tasks.yaml:482-493` (TASK-033), `tasks.md:86-87` (5.1 / 5.2)
- summary: TASK-035 (aria 版本 5 文件 bump + 主仓同步面) `dependencies: [TASK-034]`, 而 TASK-034 = 「本地 merge 进 master + tag」。顺序倒置: tag 与 master merge 先于 `plugin.json` bump。
- evidence:
  - `version-management.md:104`: aria tag 形如 `v{version}`, 应指向含该版本 SOT 的提交; 按现顺序 tag 打在 bump 之前, tag 名与 tag 处 `plugin.json` 版本不一致 (或者 bump 直接落在 master 上, 不经 feature/PR)。
  - TASK-033 (主仓 14 state-check 含版本面 `m6-version-badge-match` / `plugin-version-arch-docs-match`) 依赖 TASK-035, 即版本面 check 只能在子模块已 merge 之后才跑 —— 版本面红时 master 已含 feature, 回退成本高。
  - TASK-026 (CHANGELOG 条目) 依赖 TASK-024 且写「档位与 5.2 一致」, 但 5.2 在 merge 后才定版本号, 二者同在 `aria/CHANGELOG.md`, 会造成两次写入。
- 建议: 顺序改为 TASK-026 → TASK-035 (在 feature 分支 bump 5 文件, 版本号此时按 `plugin.json` 计) → TASK-032 / TASK-033 → TASK-034 (merge + tag) → TASK-036 (双推 + gitlink)。主仓同步面 (CLAUDE.md 版本行 / VERSION / badge / 架构文档) 可拆到 TASK-036 后与 gitlink 同一提交, 与 memory `feedback_sequenced_multirepo_gitlink_bump` 一致。

### Finding M-3 (Major)
- type: rule6-traceability / coverage-gap
- severity: Major
- category: Rule #6 substitute 留痕
- scope: `detailed-tasks.yaml:36` (metadata.rule6_note), `detailed-tasks.yaml:455-467` (TASK-031), `tasks.md:80` (4.1), `tasks.md:118-120` (rule6_note 节)
- summary: 五条 substitute 里 SC-2 由 TASK-002 / 005 / 007 三条承载, 但 rule6_note 点名 `TASK-001~005/008`, 漏 TASK-007 (D-0(a) 族键子句); TASK-031 的 dependencies 也漏了族键实现 TASK-016 (2.5)。
- evidence:
  - `proposal.md:127` SC-2 明列「D-0(a) 时 `<slug>-<uuid1>` / `<slug>-<uuid2>` 两容器 → 可达 🟡/🔴, 且 `x-20260719` 剥后零碰撞、`slug-abcdefg` 不剥」, 现状无剥离 ⇒ 该臂 baseline-failing, 属 substitute 集。
  - `detailed-tasks.yaml:179-181` TASK-007 verification 标 SC-2; `:462` TASK-031 `dependencies: [TASK-012, TASK-013, TASK-014, TASK-015, TASK-018, TASK-019]` 无 TASK-016; 按图执行, 族键臂的 RED→GREEN 记录可在 TASK-016 未落地时就被写成完成。
  - tasks.md 4.1 / rule6_note 节与 yaml `rule6_note` 是两份不同措辞 (tasks.md 版无 TASK 点名, yaml 版有), 4.1 又要求「写入本文件与 yaml」—— 应是同一份文本, 否则 B 期两处更新易分叉。
- 建议: rule6_note 点名改为 `TASK-001/002/003/004/005/007/008`; TASK-031 dependencies 加 TASK-016; tasks.md rule6_note 节与 yaml `rule6_note` 统一为逐字同文 (或一处正文、另一处只留指针)。

### Finding m-1 (Minor)
- type: format-deviation
- severity: Minor
- category: DUAL_LAYER_SPEC 字段格式
- scope: `detailed-tasks.yaml:62` (TASK-00A), `:453` 组 4 注释, `:590-641` (TASK-027..030), 全部 `est_hours`
- summary: 三处偏离规范文本, 此刻 (B 期前) 零成本可纠。
- evidence: `DUAL_LAYER_SPEC.md:161` id 格式 `TASK-{NNN}` — `TASK-00A` 非数字 (`detailed_tasks.py:76` 正则 `(\S+)` 能吞, 但 phase-d-closer `--n-tasks` 等按 NNN 语义的消费方未核); `DUAL_LAYER_SPEC.md:193`「按顺序分配 TASK-{NNN}」— 027..030 给了组 6 而 031..039 给组 4/5, yaml 注释自认是编号残留; `DUAL_LAYER_SPEC.md:166` 必需字段名 `estimated_hours` (字符串范围) — 本 yaml 用 `est_hours` 数值 (仓内 M6 用 `est_hours`, a1-entry 用 `estimated_hours`, 两派并存, 规范文本是后者)。
- 建议: 编号在 post_planning 通过前重排为 000..040 连续 (含 0.2 → TASK-001, 后续顺延), 或在 metadata 明写「编号不可变自本次审计通过起算」; 字段名择一并在 metadata 注明。

### Finding m-2 (Minor)
- type: anchor-drift
- severity: Minor
- category: 行号锚点
- scope: `detailed-tasks.yaml:117` (TASK-003 deliverables 注 `:305-341, :958-971`)
- summary: 1.3 要改的 `test_owner_segment_participates_in_grouping_key` 实际在 `tests/test_handoff_multibranch_collision_dedupe.py:1039`; `:958-971` 落在 `test_old_active_session_folds_under_newer_done_session_same_container` (`:907` 起) 内, 与 1.3 三臂无关。`:305-341` (`test_both_latest_active_still_reports_self_multi_container`) 正确。
- 建议: 锚点改 `:305-341, :1039-`。

### Finding m-3 (Minor)
- type: traceability-gap
- severity: Minor
- category: proposal T12 → tasks.md
- scope: `proposal.md:43` (D2 末句)、`:121` (T12「Lab 内部指针决策单 (`docs/decisions/`)」) vs `tasks.md` 组 5 / 范围边界表
- summary: T12 的「Lab 内部指针决策单」在 tasks.md 无对应项; 实际已由 `.aria/decisions/2026-09-05-owner-container-identity-key-rulings.md:16-18`「与 Aether 两账号模型的关系 (Lab 内部指针, 不进 standards)」承载, 且该文件 `:13` 自称「Lab 内部指针决策单即本文件」—— 路径与 proposal 写的 `docs/decisions/` 不同。
- 建议: tasks.md 范围边界或 5.2 加一句「T12 决策单项已由 `.aria/decisions/...` 满足 (路径勘正)」, 免 D 期按 proposal 字面再造一份。

## Verdict

PASS_WITH_WARNINGS (Critical 0 / Major 3 / Minor 3)

## Vote

REVISE — 三条 Major 都是 B.1 起手前能在 A.3 层闭合的计划缺陷 (归档机制不存在 / 发布顺序倒置 / Rule #6 留痕漏一臂), 不涉及 proposal 重开; 修完可直接进入 B.1。

## 轮次记录

- R1 (本轮): 实读 tasks.md 全文 (120 行) / detailed-tasks.yaml 全文 (641 行) / proposal.md v7 全文 / DUAL_LAYER_SPEC.md 全文 / phase-a-spec-planning.md A.2 段; 脚本核 parent 1:1、字段齐全、工时、agent 计数、SC 引用、带圈数字; 实跑 `spec_complete.py --gate` 取归档门现状; 实读 `spec_complete.py` / `detailed_tasks.py` / `carry_forward.py` 判定路径; 逐一 ls 引用路径, 逐一 sed 行号锚点。未引用任何未实读行号。
