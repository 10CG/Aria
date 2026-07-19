---
unverified_claims:
  - claim: "T4.1 SC-10/SC-11: 全量 1232 tests 绿 + dogfood 合成 fixture → scan.py exit=10 / configured=False / archive.total=1 / layout_drift detail 点名 stray"
    reason: "dogfood/benchmark/deploy claim 无可链接产物路径或路径不存在"
    symbols: []
unverified_ack: true
unverified_ack_reason: "归档门 artifact 分类器的产物路径正则 (_ARTIFACT_PATH_TOKEN_RE) 硬编码只认 ab-results|ab-suite (AB benchmark 目录), 故任何非-AB 的 dogfood 声称结构上恒不可 auto-link → 恒 warn, 与本声称真伪无关。真实 dogfood 执行记录已落盘为可读产物 dogfood-evidence.md (与 proposal 同目录), 含缺陷1 端到端 scan.py exit=10 + archive.total=1 实测输出、缺陷2 baseline 反转 (code-reviewer 独立 stash 复核)、缺陷3 _has_token 词边界实测。分类器该局限已记为 follow-up 观察 (非本 change 引入)。"
---
# Proposal: state-scanner-openspec-collector-false-green (#166)

> **Status**: Approved (post_spec convergence R1→R4 CONVERGED, verdict=PASS, 0 Critical/0 Major outstanding; owner sign-off pending)
> **Created**: 2026-07-18
> **Spec Level**: 2 (Minimal — proposal-only; 三缺陷同域同失效模式「沉默假绿」, 修复路径清晰, blast radius 在 collector/gate 语义而非代码量)
> **关联 Issue**: [10CG/Aria #166](https://forgejo.10cg.pub/10CG/Aria/issues/166) (open; triage verdict=`confirmed`/`major`/`next-cycle`, issuecomment-16143)
> **ship target**: aria-plugin v1.60.0 (MINOR — collector/gate 语义变更: 假绿 → 可见; 当前 SOT plugin.json = v1.59.1)
> **代码落点**: `aria/` 子模块 (`skills/state-scanner/scripts/collectors/{openspec,_status}.py` + `skills/state-scanner/scripts/lib/spec_complete.py`); Spec 落主仓 `openspec/changes/` (project meta-repo 惯例, 与 sibling `state-scanner-stale-refs-false-parity` 一致)
> **与主 spec 关系**: `state-scanner-stale-refs-false-parity` 打 **git 远程同步 collector** (#110); 本 change 打 **OpenSpec 维度 (collector + archive gate)** —— 同属「假绿」bug 类别的姊妹, 代码路径/根因**完全不相交**, 独立 change **不并入**。
> **审计轨迹 (post_spec, convergence)**: R1 5-agent [1 PASS / 4 REVISE, 5/5 SCOPE_OK] → 1 Critical (缺陷2 位置钉错, 3 agent 收敛) + 4 Major + 7 Minor → R1-fix (缺陷2 位置修正到 gate_result option A + configured 落定 + 负控 SC + 行号/路径校正) → R2 [3 PASS / 2 REVISE, 5/5 SCOPE_OK; R1 全闭合] → 1 新 Major (缺陷2 surfacing: 仅 warn 不触 Step7 D-tracker [门控 d_payload!=null], 3 agent 收敛) → R2-fix (缺陷2 改走 unverified_claims 通道 → warn_overlay frontmatter + D-tracker 双点亮, 复用 #95 零改 openspec-archive) → R3 [2 agent, R2 Major 全闭合] → **1 新 Major (rationale-only: 先例 `_fold_runtime_probe` 定性弄反 — 主线本就双写, fix 实为遵循非背离) + 1 Minor (symbols 键), fix 逻辑无变** → 本 R3-fix (更正先例 rationale + 补 symbols:[]) → **R4 稳定确认 [2 PASS / 0 REVISE, 0 新 finding] → CONVERGED (verdict=PASS)**。报告 `.aria/audit-reports/post_spec-R4-1784453650612-*-aggregated.md`

---

## Why

state-scanner 的 OpenSpec 维度在消费方 Aether **假绿约 8 周** (2026-05-22 → 2026-07-17): 每次扫描恒报 `configured=false / 0 active / 0 archived`, 而磁盘实有 3 活跃变更 + 60 归档。该假绿已污染下游 —— 2026-07-16 的 Aether handoff §5 把「OpenSpec: 0 active / 0 pending」当作**已核验的四维同步状态**写入交接。

triage (`.aria/triage-report.json`, verdict=confirmed, 3/3 复现于当前 v1.59.1) 实测三个独立缺陷, 共享**同一失效模式 —— 沉默的假绿**: 都不报错、不 WARN, 而是返回一个看起来完全正常的「干净」结果。这正是 memory `feedback_false_green_dual_is_permanent_red` / `feedback_gate_validation_needs_baseline_failing_scenario` 说的:

> **一个在该失败时不会失败的检查, 不是检查。**

**影响面 (非 Aether 独有)**:
- 缺陷 1: 归档完最后一个 spec 之后 (= 每个走完十步循环的项目, 迟早; git 不跟踪空目录 → `changes/` 自动消失)
- 缺陷 2: 用 `detailed-tasks.yaml` 而非 `tasks.md` 的项目 (= aria `task-planner` path B 的**正常合法**产出)
- 缺陷 3: Status 写 `Completed` 而非 `Complete` (极自然的词形)

---

## What Changes

三缺陷, 三处最小修复。**核心原则: 布局/数据源不符预期时应当尖叫 (可见 soft_error / warn), 而不是返回一个漂亮的零。** 每处配 baseline-failing 测试 (该失败时必失败)。

### 缺陷 1 [Major] — `changes/` 缺失 → 静默全零 + 连 `archive/` 也不扫

**根因 (行号已校正, post_spec R1)**: `collectors/openspec.py:166` `if not changes_dir.is_dir():` 提前 `return`(payload 全零, 约 `:179`)。`archive_dir` 定义在 `:164`, **确被使用** —— 在 `:264 if archive_dir.is_dir():` —— 但早退路径于 `:179` return, **到不了 `:264`**, 故 `changes/` 缺失时 `archive/` 连带不扫。`configured=false` 承载两种相反语义 (真没用 OpenSpec vs 重度使用但布局漂移), 消费方无法区分。

**修复**:
1. **正交扫 `archive/`**: 移除早退, 给 changes-loop (`:186 for d in sorted(changes_dir.iterdir())`) 套 `if changes_dir.is_dir():` 守卫 (否则 `changes/` 缺失时 `.iterdir()` 抛 `FileNotFoundError`); `archive/` 块 `:264` **已自带** `if archive_dir.is_dir():` 守卫, 使 `changes/` 缺失时 `archive.total` 仍反映磁盘真实归档数。drift 路径下 `changes.items`/`pending_archive`/`design_deferred`/`carry_forward_inventory` 自然为空/零 (语义正确 — 无活跃变更), 显式写明。
2. **可见 soft_error (高置信 drift 才发)**: `changes/` 缺失但 `openspec/` (spec_root) 存在 **且有既往使用证据** (`archive/` 非空 **或** `openspec/` 下直接躺着 `*proposal*.md` 裸文件 / 含 `proposal.md` 的非-`changes/` 子目录) → 发 `soft_error("layout_drift", detail)` (让「布局漂移」可见, 区别于「没配置」); detail 点名疑似漂移产物 + 建议补救 (在 `changes/` 放 `.gitkeep` 锁目录常驻, 或迁回变更)。
3. **`configured` 取值落定 (M1, post_spec R1)**: drift 路径 `configured` **保持 `False`** —— 保守于 schema 文档化契约 (`state-snapshot-schema.md:311 configured: bool # openspec/changes/ exists`, `changes/` 确不存在); 消歧完全由 `layout_drift` soft_error + `errors[]` 非空 + `archive.total>0` 承载 (不翻 `True` 以免与文档语义矛盾)。核实: 全插件**无任何代码分支消费 `openspec.configured`** (仅文档化), 故保 False 不致下游误跳过; schema 文档同步该 (configured=False ∧ archive.total>0) 消歧语义。

### 缺陷 2 [Major] — 归档安全网 `gate_result` 对 `detailed-tasks.yaml`-only 项目早退失明

**根因 (位置已修正, post_spec R1 Critical — 3 agent 收敛)**: issue 标题里的 `d_payload` 真实生产者是 `lib/spec_complete.py::gate_result()` (:1287 默认 `d_payload=None`), 由 `openspec-archive` Skill Step 1/7 (#95「归档不吞未完成」) 在**归档时** `--gate` 调用, 决定是否建 Forgejo tracker issue。`gate_result` 在 `:1298-1300` 有**它自己独立**的早退:

```python
tasks_path = spec_dir / "tasks.md"
if not tasks_path.is_file():
    return result   # 无 tasks.md → d_payload=None / verdict=pass / 空 unverified_claims
```

亲验 (owner ground-check): `:476 dt_path = spec_dir / "detailed-tasks.yaml"` 的读取在 `:1300` 早退**之后**才可达 (在 integration_claims 循环内, 遍历 tasks.md `[x]` 项), 故 `detailed-tasks.yaml`-only 项目**根本到不了** yaml 读取 → 归档安全网对这类项目完全失明, `verdict=pass`/`d_payload=None`/空 `unverified_claims` 静默放行, Step 7 一个 tracker 都不建。**原 proposal 钉的 `collectors/openspec.py:244` (`tasks_file`) 只喂 state-scanner 快照的 `carry_forward_inventory` 展示字段, 与 `gate_result` 是两条不相交调用链** (`collect_openspec()` 返回值根本无 `d_payload` 键) —— 原 proposal 继承了 issue 自身的 mis-citation。

**修复 (owner 决策 option A: 修真实位置 gate_result, 先可见; post_spec R2 机制修正)**:
`gate_result()` `:1298-1300` yaml-only 分支 (`tasks.md` 缺失 ∧ `detailed-tasks.yaml` 存在):
1. 向 `result["unverified_claims"]` 追加**一条** `{"claim": "<spec> 完成声称", "reason": "归档安全网数据源 detailed-tasks.yaml 未支持 — 完成声称无法核验 (安全网失明); 需人工复核", "symbols": []}` (含 `symbols` 键 — 对齐 `spec_complete.py:40` 类型契约 `{claim,reason,symbols}` 与全部 5 个既有 append 点, post_spec R3);
2. `verdict = "warn"` (单调升级 pass→warn);
3. 经 `_build_d_payload(spec_dir, [], result["unverified_claims"])` 构造**非 None** `d_payload` (无 deferred_items, 仅带该 unverified 条目) 再 return。

- **为何走 `unverified_claims` 通道而非仅 `warnings[]` (R2 code-ground Critical 修正)**: R2 证伪「仅 `verdict=warn` 即经 Step 7 surface」—— `_build_d_payload` (`:1128`) 在无 deferred ∧ 无 unverified 时返 `None`; openspec-archive D auto-issue 门控 `d_payload != null` (**不看** verdict); Step 2 warn_overlay 落盘 frontmatter 的是 `unverified_claims` (**不是** warnings)。故必须经 `unverified_claims`: 令 (a) warn_overlay 写 frontmatter `unverified_claims` (持久, **headless 亦然** — 文件写) **且** (b) D auto-issue 建 Forgejo tracker (**headless 默认**), **两条 surfacing 都点亮**, 兑现 #166 缺陷2「headless 一个 tracker 都不建」的核心诉求。**复用 #95 既有机制, 零改 openspec-archive 代码。**
- **遵循 `_fold_runtime_probe_declaration` 主线先例 (`:1235-1256` + docstring `:1197-1200`, post_spec R3 更正)**: 该先例 warn/invalid 时**本来就双写** `warnings[]` + `unverified_claims[]` (`{claim,reason,symbols}` 形态), docstring 明写「deliberate TASK-007 double-write so the entry reaches both #95 downstream consumers (warn_overlay persistence AND `_build_d_payload`'s D auto-issue)」—— 本 change 缺陷2 修复**与之完全同型同因**, 非背离。(注: `:1429-1440` 是探测管线**崩溃兜底**分支 [check 机制自身故障], 故意不 tracker 刷屏, 属另一类, 不可作缺陷2 的类比基准。)
- **不做**完整 `detailed-tasks.yaml` 解析 (精确枚举 `tasks[].status` + `deferred_out_of_scope` 填 `d_payload`) —— 留 **follow-up** (见非目标); 届时以精确 per-spec verdict 取代本 blanket unverified 条目 (**只在真有残留时**才 tracker)。
- **诚实态披露 (post_spec R1 code-reviewer + `feedback_false_green_dual_is_permanent_red`)**: 因 gate 不解析 yaml, 无法区分「真干净」vs「有残留」, 故对**所有** `detailed-tasks.yaml`-only spec 归档都发该 unverified 条目 —— 这是诚实的「**无法核验**」态 (非「有残留」断言, 非永久假信号): actionable (加 tasks.md / 等 follow-up / 手工核实如 issue 作者对 190-191 所做), 且 follow-up 落地后被精确 per-spec verdict 取代; tracker 幂等 (dedup marker `<!-- archive-tracker:{spec_id} -->`) 不重复刷屏。

### 缺陷 3 [Minor] — `_normalize_status("Completed") → unknown`

**根因**: `collectors/_status.py:199` done 家族 token `("done", "complete")` + `_has_token` 词边界锚定 (`\bcomplete\b`, #101 修 substring-shadow 引入防 `incomplete` 误配)。`Completed` 后置词边界失败 → 落 `unknown` (且 `unknown` 进一步触发 `design_deferred` → 噪音)。#101 对合法**词形变化**过度收紧。

**修复**: done 家族 token 加 `"completed"`。**已实跑验证** (owner + code-reviewer ground-check): `_has_token("uncompleted","completed")=False`、`("incomplete","completed")=False`、`("completed","completed")=True` —— 不重开 #101。

---

## Success Criteria (可证伪; 每条配 baseline-failing 测试)

| SC | 验收 (二值 metric) | Baseline (修复前必 RED, 除负控/护栏) |
|----|---------|--------|
| **SC-1** (缺陷1a) | `openspec/` 存在 + `changes/` 缺失 + `archive/` 有 N 归档 → snapshot `errors[]` 含 `layout_drift` **且** `archive.total == N` | 当前: `errors=[]` + `archive.total=0` (静默连带归零) |
| **SC-2** (缺陷1 负控) | `openspec/` 存在 + `changes/` 缺失 + `archive/` 空/缺 + 无裸 proposal → **不发** `layout_drift`, `configured=False` (冷启动合法, 非漂移) | 保护性: 当前静默 `configured=False`, 须保持不误触 |
| **SC-3** (缺陷1c) | `layout_drift` detail 点名疑似漂移产物 —— 覆盖**两种真实形状**: `openspec/` 下裸 `*.md` 文件 (triage repro 实测形状) **及** 含 `proposal.md` 的非-`changes/` 子目录 | 当前: 无 detail |
| **SC-4** (缺陷1 configured, M1) | drift 路径 `configured == False` (不翻 True); 消歧靠 `layout_drift` soft_error 存在; schema 文档同步该组合 | 当前: `configured=False` 但无 soft_error 消歧 |
| **SC-5** (缺陷2) | spec_dir 有 `detailed-tasks.yaml` 无 `tasks.md` → `gate_result` `verdict=="warn"` **且** `unverified_claims[]` 含数据源未支持条目 **且** `d_payload != None` (两条 surfacing 都点亮: warn_overlay frontmatter + D-tracker, headless 亦然) | 当前: `verdict="pass"` / `unverified_claims=[]` / `d_payload=None` (静默) |
| **SC-6** (缺陷2 负控) | spec_dir **同时**有 `tasks.md` + `detailed-tasks.yaml` → `gate_result` 走 tasks.md 路径, **不**误发数据源未支持 warn | 保护性: 本 repo `aria-2.0-m6-dispatch-input-delivery` 即此形态, 须不误报 |
| **SC-7** (缺陷3) | `_normalize_status` 对 `Completed`/`COMPLETED`/`Status: Completed` → `done` | 当前: → `unknown` |
| **SC-8** (缺陷3 护栏) | `_normalize_status` 对 `uncompleted`/`incomplete` **不** → `done` (不重开 #101) | 保护性: 当前已 → `unknown`, 须保持 |
| **SC-9** (缺陷3 联动副作用) | Status=`Completed` 的 spec 从 `design_deferred[]` 迁出、入 `pending_archive[]` (跨字段联动, 显式断言) | 当前: 因 `unknown` 落 `design_deferred[]` |
| **SC-10** (无回归) | 全量既有 state-scanner + spec_complete 测试仍绿 | — |
| **SC-11** (dogfood) | 三缺陷各以合成 fixture 端到端: 缺陷1 drift fixture → scan.py exit=10; 缺陷2 yaml-only spec_dir → gate_result warn (**须合成 fixture** — 本 repo 无 yaml-only change dir, `dispatch-input-delivery` 两者都有) | — |

> **SC 设计原则** (memory `feedback_falsifiable_evidence_for_binary_acceptance` + post_spec R1 qa): 每条 SC 均可机验二值 + 明确 baseline; 含**对称负控** (SC-2 冷启动 / SC-6 双源并存 / SC-8 #101 护栏) 防「在健康常态下也触发」的恒红陷阱。

---

## Impact

**Files (aria 子模块)**:
- `skills/state-scanner/scripts/collectors/openspec.py` — 缺陷 1 (移早退 + loop 守卫 + 扫 archive + `layout_drift` soft_error + 冷启动负控)
- `skills/state-scanner/scripts/lib/spec_complete.py` — 缺陷 2 (`gate_result` `:1298-1300` yaml-only 分支: 追 `unverified_claims` 条目 + `verdict=warn` + 构造非 None `d_payload`)
- `skills/state-scanner/scripts/collectors/_status.py` — 缺陷 3 (done 家族加 `completed`)
- `skills/state-scanner/tests/` (**既有测试目录**, 非 `scripts/tests/`; 已有 `test_openspec.py` / `test_openspec_design_deferred.py`) — 各缺陷 baseline-failing 测试 + spec_complete gate 测试
- `skills/state-scanner/references/state-snapshot-schema.md` — 新 `layout_drift` soft_error kind + `configured=False ∧ archive.total>0` 组合语义 (Rule #3)
- `skills/state-scanner/references/status-field-guide.md` — done token set 表加 `completed` (人类可读 SOT, post_spec R1 knowledge-manager)
- `skills/state-scanner/references/output-formats.md` — 补 `layout_drift` 场景 worked-example (防 AI 仍套「未配置」模板渲染, post_spec R1 knowledge-manager)
- `skills/openspec-archive/SKILL.md` — **无需改** (post_spec R2 确认): 缺陷2 复用 #95 既有 `unverified_claims` → warn_overlay frontmatter (`:137-138,:180-182`) + `d_payload != null` → D auto-issue (`:272`) 两条既有路径; gate 侧填 `unverified_claims`+非 None `d_payload` 即自动点亮, openspec-archive 零改动

**Files (主仓, 发版时)**: `aria/CHANGELOG.md` + 版本文件 + gitlink bump + README badge (v1.60.0)

**Downstream 行为变化 (backward-compat: additive)**:
- 新增 soft_error kind: `layout_drift` (无 collector 前缀, 对齐既有 `spec_read_failed`/`status_field_truncated` 命名惯例)。
- 缺陷1 drift 场景 + 缺陷2 warn 场景下 scan.py exit code 从 0 → **10** (软错误, snapshot 仍可用) —— 符合退出码契约。
- **合法「全归档终态」持续 soft_error** (code-reviewer Minor): 项目所有 spec 归档、git 丢弃空 `changes/` 后每次 scan 恒发 `layout_drift` + exit 10 —— 这是**预期且 actionable** (补 `.gitkeep` → `changes_dir.is_dir()=True` → 不再报, 即 Aether `1493823` 自救), soft_error detail 内嵌该补救提示, 非 bug。
- **缺陷3 跨字段联动** (backend-architect Minor): `Completed`→`done` 使受影响 spec 从 `design_deferred[]` 迁出、入 `pending_archive[]` (SC-9 显式覆盖)。
- `errors[]` / `warnings[]` 追加, 既有字段不改; 无破坏性变更 (Rule #4)。

**非目标 (out-of-scope, 留 follow-up)**:
- **[follow-up 待开]** `gate_result` 完整支持 `detailed-tasks.yaml` 数据源 (解析 `tasks[].status` + `deferred_out_of_scope` 精确填 `d_payload`) —— 将以精确 per-spec verdict 取代缺陷2 的 blanket warn, **并顺带修复** collector 快照侧 `carry_forward_inventory=0` 对 yaml 项目的展示假绿 (同根: yaml 未解析)。Phase D 收尾时开 issue, cross-link #166。
- Aether 消费方自救 (`10CG/Aether 1493823`) 已完成, 非本 change。
- git 同步 collector / #110 / 主 spec —— 不相交。

---

## 设计决策记录 (供 R2 对焦)

1. **缺陷2 修 `gate_result` (option A, owner 2026-07-18)**: 修真实位置 (归档安全网) 而非快照展示字段; 先 warn 可见, 完整 yaml 解析留 follow-up。接受 yaml-only 类 blanket warn 的诚实「无法核验」态 (follow-up 取代)。
2. **drift 路径 `configured=False`** (M1): 保守于 schema 文档语义, 消歧靠 soft_error; 无代码消费方故安全。
3. **`layout_drift` 仅高置信才发** (M4 负控): `archive/` 非空或有裸 proposal 才尖叫; 纯冷启动静默 (SC-2)。
4. **三缺陷同 change**: 同域 (OpenSpec 维度)、同失效模式 (沉默假绿)、共享 baseline-failing 测试范式; 一次审计闭合。缺陷 3 顺带 (trivial 单 token)。
5. **缺陷2 surfacing 走 `unverified_claims` 双通道 (post_spec R2 + R3)**: 经源码核验, 仅 `verdict=warn` 不足以让 headless 归档可见 (D-tracker 门控 `d_payload!=null`, warn_overlay 落盘 `unverified_claims`); 故填 `unverified_claims` (含 `symbols:[]`) + 构造非 None `d_payload`, 复用 #95 既有机制点亮 frontmatter 持久化 + Forgejo tracker。此模式**恰为主线 `_fold_runtime_probe` warn/invalid 分支 (`:1235-1256`) 的既有双写先例** (docstring `:1197-1200` 明示双写正为达 warn_overlay + D auto-issue 两消费方) —— 缺陷2 与之同型, 非背离 (R3 更正: 原引 `:1429-1440` 系崩溃兜底另一类)。
