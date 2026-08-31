---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-30T15:27:15.222Z
context: openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml (+ linked-issue-field-availability + sibling-spec-probe)
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A2-backend-architect
critical_count: 3
major_count: 1
minor_count: 0
---

## 摘要

本席对三份同族 Spec 的 A.2/A.3 产物 (`tasks.md` + `detailed-tasks.yaml`) 做「实现者试派生」核验: 逐条对 file:line 锚点、接口签名、A.2 显式约束 (audit-engine 不建 `lib/`/`collectors/` 顶层目录、探针 helper 前缀、跨 skill import 顺序)、粒度与「不改」约束做实测。

**anchor 精度**: 抽查约 45 处 file:line / 函数签名 / issue 号引用 (跨 `phase1_gate.py` / `release_gate.py` / `identity.py` / `claim_lifecycle.py` / `collision.py` / `claim_schema.py` / 各 SKILL.md / `execution-modes.md` / `report-format.md` / `DEFAULTS.json` / `multi_remote.py` / `fetch_gate.py` / `handoff_autofill.py` / `coordination_probe.py` / 三份 archive proposal / 四个 Forgejo issue), **全部逐字节命中**, 包括母 Spec 自报「7a/7c/7d/Step 9 本轮补钉」的四处漂移锚点、`phase-a-planner/SKILL.md` 围栏数「Spec 写 7 实为 8」的勘正、`test_` 方法基线计数 1425。sys.path 顺序设计 (`_SS_SCRIPTS` 先插、`_SS_ROOT` 后插使其排最前) 用真实 `lib.collision` 模块实跑验证: 正序两符号 (`lib.collision` + `collectors.multi_remote`) 同时可解析, 反序 (SC-21 负控设计) 确定性 `ModuleNotFoundError`, 与三份 Spec 引用的 memory `ss-two-lib-pkgs` 完全吻合。A.2 显式约束「`audit-engine/` 不建 `lib/`/`collectors/`」在基线与派生计划两端均核实成立。

**唯一实质性缺陷类**: 三份 `detailed-tasks.yaml` 系统性缺失「同文件任务须串行」的机器可读 DAG 边——tasks.md 正文与 Group 注释多处明写「同文件串行」(memory `workflow-file-domain`), 但落到 `dependencies` 字段与 `execution_order`/`phase_N` 元数据时, 写同一文件的多个任务之间**没有相互依赖边**, 其中 4 处更被 `execution_order` **显式标注为「可并行」/「[并行, RED]」**。若 subagent-driver / phase-b-developer 按此 DAG 拓扑派发 (dual-layer 格式存在的目的正是供机器消费), 会对同一文件发起并发 Edit/Write, 与本文件族自己援引的纪律直接冲突, 属「按此执行会错」。

另发现 1 条 major: `sibling-spec-probe` 的 `metadata.line_anchor_recheck` 段自称「与 proposal 一致」「实况全部复现」, 但其中两条 git 远端状态的经验性断言 (`refs/remotes/` 含陈旧 `probe` / `refs/aria/` 现存 3 条) 在当前仓状态下**均不可复现** (无 `probe` 远端引用, `refs/aria/` 零引用), 与该段落自我担保的「全部一致」矛盾。

## Findings

| id | severity | category | scope | type | 描述 |
|----|----------|----------|-------|------|------|
| 73809784 | critical | architecture | openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml | issue | 同文件任务缺串行依赖边 (4 处), 与 tasks.md 明写的「同文件串行」矛盾。详见「实测记录 §1」|
| 9b64d749 | critical | architecture | openspec/changes/linked-issue-field-availability/detailed-tasks.yaml | issue | `execution_order` 显式把写同一新文件的任务标「parallelizable」(3 组), 与「同文件串行」纪律矛盾。详见「实测记录 §2」|
| a257ffa4 | critical | architecture | openspec/changes/sibling-spec-probe/detailed-tasks.yaml | issue | `execution_order` 显式把写同一新测试文件的 5 个任务标「[并行, RED]」。详见「实测记录 §3」|
| f3265bfe | major | documentation | openspec/changes/sibling-spec-probe/detailed-tasks.yaml | issue | `metadata.line_anchor_recheck` 的 git 远端「本仓实况」断言 (陈旧 `probe` 远端 / `refs/aria/` 3 条) 当前不可复现, 与该段自我担保的「一致」矛盾。详见「实测记录 §4」|

### 73809784 — a1-entry: 同文件任务缺串行依赖边

**证据 (`git grep` / `awk` 实测, aria @ d69091d, 主仓 detailed-tasks.yaml)**:

- `scripts/phase1_gate.py` 由 TASK-014 (4.1) → TASK-015 (4.2) → TASK-016 (4.3) 三次连续编辑, tasks.md `## Notes` 明写「同文件串行 (phase1_gate.py 4.1→4.2→4.3)」。实读三任务的 `dependencies`:
  - TASK-014: `[TASK-008, TASK-013]`
  - TASK-015: `[TASK-008, TASK-014]` ← 正确含 014
  - TASK-016: `[TASK-010, TASK-012, TASK-014]` ← **不含 TASK-015**
  拓扑调度器只需等到 TASK-014 完成即可同时启动 TASK-015 与 TASK-016, 两者并发编辑同一文件。
- `tests/test_coordination_default_lockin.py` 由 TASK-025~030 (6.1→6.6) 六次连续编辑, Group 6 注释明写「串行 025 → 030」。实读六任务 `dependencies`: TASK-025 `[TASK-017, TASK-018]`; TASK-026 `[TASK-019]`; TASK-027 `[TASK-022]`; TASK-028 `[TASK-021]`; TASK-029 `[TASK-023]`; TASK-030 `[TASK-020, TASK-021]` —— 六者之间**互不引用**, TASK-026~030 一旦各自的单一依赖就绪即可与 TASK-025 及彼此并发。
- `tests/test_heartbeat_by_track.py` 由 TASK-005 与 TASK-006 (TASK-006 deliverable 注释「同文件加 TestRenameTwoStep 类」) 共写, 两者 `dependencies` 均只为 `[TASK-003]`, 互不引用。
- `tests/test_a1_entry_gate_cli.py` 由 TASK-007/008/009 共写 (TASK-008 注释「同文件加四个测试类」, TASK-009 注释「同文件加 TestA1CarryIdRoundTrip」), 三者 `dependencies` 均只为 `[TASK-003]`, 互不引用。

复现命令: `awk '/id: TASK-01[456]$/{print; f=1; next} f && /dependencies:/{print; f=0}' openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml`

**处方**: TASK-015 补 `TASK-014`(冗余但无害)+ TASK-016 补 `TASK-015`; TASK-026~030 依次追加前一任务 id (026←025, 027←026, 028←027, 029←028, 030←029, 或至少全部追加 025 并在 verification 声明本组仍需人工/主控串行); TASK-006 补 `TASK-005`; TASK-008 补 `TASK-007`, TASK-009 补 `TASK-008`。

### 9b64d749 — linked-issue-field-availability: `execution_order` 显式标同文件任务并行

**证据**:

- `tests/test_linked_issue_field.py` 由 TASK-001~006 共写 (TG-1, tasks.md 头注「宿主逐字采用」同一文件)。TASK-001~005 `dependencies` 全为 `[]`, TASK-006 才依赖 `[TASK-001,002,003,004]`。`metadata.execution_order.phase_1_red_and_probe` (:663-666) 逐字: `parallelizable: [TASK-001, TASK-002, TASK-003, TASK-004, TASK-005, TASK-012]` —— **显式**把五个同写一个新文件的任务标可并行。
- `aria/skills/spec-drafter/SKILL.md` 由 TASK-014 (hunk A) 与 TASK-015 (hunk B) 共写, 两者 `dependencies` 均只为 `[TASK-005]`。`phase_3_docs` (:670-672) 逐字: `parallelizable: [TASK-013, TASK-014, TASK-015]` —— TASK-013 编辑的是 `standards/` 内的另一文件, 与 014/015 并行本身无害, 但 **014 与 015 同文件**仍被并入同一「parallelizable」列表。
- `aria/skills/state-scanner/scripts/linked_issue_field_probe.py` 由 TASK-008 (check 模式) 与 TASK-009 (`--emit-arg` 模式) 共写, `phase_2_green` (:667-669) 的 `chain` 字段逐字: `"TASK-007 → {TASK-008, TASK-009} → TASK-010 → TASK-011"` —— 花括号记法在本文件族内是并行组标记 (对照 a1-entry yaml 同款记法 `{TASK-022, TASK-023}`), 即 TASK-008/009 被判定可并行, 而两者写同一新文件。

复现命令: `sed -n '663,673p' openspec/changes/linked-issue-field-availability/detailed-tasks.yaml`

**处方**: `phase_1_red_and_probe.parallelizable` 移除 TASK-002~005 (改为 `then` 链或标注「同文件, 主控内部串行落盘, 允许并行设计/评审」); `phase_2_green.chain` 的 `{TASK-008, TASK-009}` 改为 `TASK-008 → TASK-009` 或显式加旁注「同文件, 两模式落两次 diff, 禁止两 subagent 并发编辑」; `phase_3_docs` 拆开 TASK-013 (真并行) 与 TASK-014/015 (同文件, 需注明落点物理不相邻不等于可并发写)。

### a257ffa4 — sibling-spec-probe: `execution_order` 显式标同文件任务并行

**证据**: `tests/test_sibling_spec_probe.py` 由 TASK-005~009 共写 (TG-2, 五任务 deliverable 注释均指向该同一文件)。五任务 `dependencies` 均只为 `[TASK-004]`, 互不引用。`execution_order` (:564) 逐字: `"[并行, RED] TASK-005 · TASK-006 · TASK-007 · TASK-008 · TASK-009  ← 004"` —— 显式标记为并行, 且这是五个任务共写一个刚由 TASK-004 新建的测试文件骨架。

复现命令: `grep -n '并行, RED' openspec/changes/sibling-spec-probe/detailed-tasks.yaml`

**处方**: 改为链式 (`TASK-004 → TASK-005 → TASK-006 → TASK-007 → TASK-008 → TASK-009`) 或显式改注「设计/夹具内容可并行构思, 落盘须主控串行合并, 不得派发给独立并发 subagent」。

### f3265bfe — sibling-spec-probe: `line_anchor_recheck` 的 git 远端「本仓实况」不可复现

**证据 (aria @ d69091d 实测, 2026-08-30)**:

```
$ git -C aria for-each-ref refs/aria/ | wc -l
0
$ git -C aria for-each-ref refs/remotes/ | grep -i probe
(无输出)
$ git -C aria config --get-regexp 'remote\.probe\.'; echo exit=$?
exit=1
```

`metadata.line_anchor_recheck` 段落自陈 (行内): 「git remote = {github, origin}; refs/remotes/ 含陈旧 probe (remote.probe.url 空, exit 1); refs/aria/ 现存 3 条; ... — proposal 实况全部复现」, TASK-012 notes 重申「本仓实况 (A.2 复核): ... refs/remotes/probe 陈旧」。当前实测: **`refs/remotes/` 下无任何 `probe` 分支引用** (`git for-each-ref` 与 `.git/packed-refs` 均零命中), **`refs/aria/` 下零引用** (非声称的 3 条); `git remote` = `{github, origin}` 这一条是唯一可复现的。`git config --get-regexp` exit=1 可以理解为「无该 remote 配置」这一半与「url 空」的措辞相容, 但「`refs/remotes/` 含陈旧 probe」与「`refs/aria/` 现存 3 条」两条独立经验断言均为假。

该发现不影响 TASK-012/TASK-013 的实现正确性 (P7 关于「不枚举 `refs/remotes/*`」的架构约束本身独立成立, SC-14 测试用注入式 runner 而非依赖真实仓状态), 但损害 `line_anchor_recheck` 段落作为「已核验证据」的可信度——该段自称「一致」/「全部复现」, 供后续任务 (如 TASK-002 的「基线三态记录」) 直接引用而非重新验证。鉴于三份 Spec 在同一共享仓内被并发轨道操作 (CLAUDE.md Rule #10 引用的 memory `feedback_concurrent_duplicate_audit_fetch_before_start`), 这更可能是 A.2 执笔与本次审计之间的仓状态漂移, 而非虚构, 但文档现状仍是「未经当下复核的历史快照被当作『已复现』呈现」。

**处方**: TASK-002 (基线三态记录) 执行时重新实测 git 远端状态并更新描述, 不再引用 `line_anchor_recheck` 中这两条经验断言作为设计依据; `line_anchor_recheck` 段可保留但应加时间戳/加注「仅 A.2 当日观测, B 期开工前需重跑」(该纪律 TASK-002 notes 已部分具备, 但未回溯标注在 metadata 段本身)。

## 实测记录

**anchor 抽查 (节选, 全部命中)**: `phase1_gate.py` :61/:219/:299-311/:351/:537/:554/:573/:693-697/:761-762/:835/:848/:856/:1010/:1049/:1094/:1255/:1269/:1273/:1332/:1335-1340; `release_gate.py` :150/:238-246/:268/:273-276; `lib/identity.py` :191/:222/:242/:244; `lib/collision.py` :46/:178/:230/:265-279; `lib/claim_lifecycle.py` :377/:397/:425; `lib/claim_schema.py` :120-130; `spec-drafter/SKILL.md` :9/:10/:73/:75-119/:109/:125/:127-162/:139/:140/:336/:424/:429 (438 行); `audit-engine/SKILL.md` :83/:85/:121/:237/:412 (421 行); `execution-modes.md` :84/:89/:90/:113/:118/:119 (144 行); `report-format.md` :50/:52/:58/:67; `config-loader/DEFAULTS.json` :123-128; `collectors/multi_remote.py` :255/:1376; `fetch_gate.py` :50/:55/:86/:108; `handoff_autofill.py` :48/:51/:404/:407; `coordination_probe.py` :17-24/:80-85; `run_all_tests.sh` :44-52/:71; `.aria/state-checks.yaml` 12 条 (@ 主仓当前 HEAD); `aria-plugin-benchmarks/ab-suite/` 31 个 `.json` + `version.yaml` (1.1.0/29/58); `test_release_by_track.py` :23-25/:43/:206/:377/:380/:527/:531/:586; `test_` 方法基线计数 = 1425 (`grep -rh '^\s*def test_' tests/*.py | wc -l`)。三份 archive proposal 逐字核对: `2026-06-11-audit-drift-guard/proposal.md:5`、`2026-08-23-linked-issue-normalization/proposal.md:6`、`2026-08-16-premerge-gate-branch-existence/proposal.md:61` 均逐字节命中。Forgejo issue #150 / #157 / #117 / #127 / #135 均实测 open 且标题与引用意图相符。

**sys.path 实跑**:
```
$ python3 -c "
import sys; from pathlib import Path
for p in ('skills/state-scanner/scripts','skills/state-scanner'):
    sys.path.insert(0, str(Path(p).resolve()))
import lib.collision as c; print(c.__file__)
import collectors.multi_remote as m; print(m.__file__)
"
.../state-scanner/lib/collision.py
.../state-scanner/scripts/collectors/multi_remote.py
# 反序 (先插 root 后插 scripts):
$ python3 -c "...反序..."
ModuleNotFoundError: No module named 'lib.collision'
```
与三份 Spec 引用的正/负控设计逐字一致。

**A.2 显式约束核验**: `ls aria/skills/audit-engine/` 当前恰为 `{SKILL.md, references}`, 三份 Spec 计划的新增交付物 (`scripts/sibling_spec_probe.py`、`scripts/__init__.py`、`tests/test_sibling_spec_probe.py`) 均不越界建 `lib/`/`collectors/` 顶层目录, 亦未规划任何需要 `sibling_spec_probe_` 前缀的额外 helper 文件 (唯一脚本即命名本身)。

**「不改」约束核验**: `branch-manager/SKILL.md:146` 现文本为「### 前置: REQUIRE claim (Part A1, MUST — 与 phase-b-developer B.0 同一条约束)」, 与「不改该标题」的约束一致且理由 (Part A1 是已 ship Spec 部件名) 属实; `phase-b-developer/SKILL.md:86/:88/:92/:96-98`、`phase-d-closer/SKILL.md:42/:51-52/:55-56` 逐字匹配 Spec 引用。

**跨 Spec 接口一致性**: `linked-issue-field-availability` 的 `exports_for_siblings.dataclass_FieldVerdict` (verdict 四态 / token_str / token_elements / line_no / 附加 bad_elements) 与母 Spec `external_dependencies` 引用、`sibling-spec-probe` 的 `external_dependencies.interface_expected` 三方逐字段核对一致, 且 `sibling-spec-probe` 对「非 proposal 成文、来自并发轨 A.2 产物」的 `line_no` nullability 语义诚实标注来源 (`linked-issue-field-availability/detailed-tasks.yaml:47`) 而非默认信任, 该行经核实确实逐字为 `line_no: "int | None — 命中行的 1-based 行号; NO_FIELD 时 None"` (第 47 行)。

**粒度**: 抽查未发现「S 复杂度塞 10+ 实现类 deliverable」的低估模式; 唯一体量偏大的 S 任务 (a1-entry TASK-003, 16 个只读锚点文件 / field-availability TASK-002 类似) 均为纯 `sed`/`grep` 机械核对而非实现, 与其 S/1-2h 估时相称。

## Verdict

FAIL (critical_count = 3)。三份 Spec 均需在 A.2 落版前修正同文件任务的依赖边 (或至少撤除/改写 `execution_order` 中的显式「并行」标注并加主控串行落盘的旁注), 否则按此派生直接执行会在四类文件 (`phase1_gate.py`、`test_coordination_default_lockin.py`、`test_heartbeat_by_track.py`、`test_a1_entry_gate_cli.py`、`test_linked_issue_field.py`、`linked_issue_field_probe.py`、`spec-drafter/SKILL.md`、`test_sibling_spec_probe.py`) 上产生并发写冲突。1 条 major (sibling-spec-probe 的 git 远端「实况」断言过期) 不阻塞但应在 B.1 前重跑核验。

## Vote

REVISE
