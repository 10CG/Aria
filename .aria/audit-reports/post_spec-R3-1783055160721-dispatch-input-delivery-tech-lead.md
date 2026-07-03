---
checkpoint: post_spec
round: 3
agent: tech-lead
verdict: PASS
vote: PASS
spec_id: aria-2.0-m6-dispatch-input-delivery
timestamp: 1783055160721
prior_round_verdict: PASS
---

# post_spec R3 (convergence) — tech-lead — Dispatch Input Delivery

**Verdict: PASS** · **Vote: PASS** · Round 3 (convergence)

R2 我 PASS。本轮 spec 据 backend-architect R2 两 Critical 又修订 (seed additive 列 +
outcome-class DB 持久化 + sibling acceptance 协调)。从架构/依赖边视角逐项对**真代码** (`daf7c79`)
核实这轮修复自洽、无新结构缺口。三个重点全部通过；C' 双通道主线与 11 决策点经三轮修订仍完整。

---

## 本轮重点核实 (架构/依赖边视角)

### 1. Seed-time additive 列 (TG-2.1 / B.2) — 数据流无断裂 ✅ 代码印证

**架构主张**: seed 阶段确有 `raw_issue_number` / `target_repo` / `base_branch` / `files_hint`；
`_handle_s4_launch` 只能读 `dispatch_row`；additive 列桥接二者。

对 `daf7c79` 逐点核实:
- **seed 有原始 number**: `_phase1_scan_and_seed` `extension.py:1176` = `str(issue.get("id") or
  issue.get("number") or "")` → `issue.get("number")` (per-repo 原始 number) **在 seed 循环内可得**。
- **seed 有 repo**: seed 经 lazy-wired `ForgejoCliClient(org=FORGEJO_ORG, repo=FORGEJO_REPO)`
  (`:1133-1136`) 知道 `target_repo`。
- **S4 只见 dispatch_row + 硬编码 env**: `_handle_s4_launch:2109` = `ctx.dispatch_row.get("issue_id")`；
  `:2149-2152` `forgejo_org/repo = os.environ.get(...)` + `issue_url` 直插 `issue_id`。
  **与 §B.2/B.4 陈述逐字吻合** —— S4 今天物理上拿不到 seed 的 raw number/repo，additive 列是唯一
  无重构桥梁。
- **迁移先例成立**: `migrations/` 有 `002..007_schema_vN_additive.sql` (M3 v2 / M4 v3 / M5 +
  spec_id / is_synthetic)，additive nullable 列是本代码库标准范式，**非键重构**。

**结论**: 数据流 seed→dispatch_row(additive 列)→`_handle_s4_launch`→META/ISSUE_URL **闭合无断裂**。
承重的 fetch 字段 (raw_number + target_repo) 确在 seed 可得；`base_branch`/`files_hint` 是可空增强
metadata + 有 default_branch 兜底 (AC-12 NULL 优雅降级)，即便 seed 未填也不破 fetch。R2 Critical B
的诊断 (S4 只见 dispatch_row) 与修复 (additive 列) **架构正确且代码印证**。

### 2. Cross-Spec coordination (改 sibling 验收脚本) — 显式化、无隐性掉线 ✅

这是本轮引入的**新架构耦合**，重点确认它被正确显式化：

- **编辑目标真实**: `acceptance/check-m6-e2e-acceptance.py` 存在；AC-2 在 `:224-227` 正是
  `SELECT COUNT(*) ... WHERE state='S9_CLOSE'` → `total_s9`，即 §C.3 所指查询。
- **属 Spec #2 制品**: 该文件近期 commit (`c5d863d`/`f267c97` = AC-6 R1/R2 审计收口) 与 CLAUDE.md
  记录的 Spec #2 e2e-resilience「AC-6 false-green 修复 #146」吻合 → 确为**未归档 sibling** 的文件。
- **跨界被显式化**: spec 专设 **§Cross-Spec coordination (in scope)** (line 323-329) + **AC-4(c)** +
  **TG-2.7** + Out-of-Scope 交叉引用，四处锚定「本 Spec 交付此编辑」。无隐性掉线。
- **与「遥测 Spec 依赖边」清晰区分** (本轮关键关注点):
  - **Cross-Spec coordination** = 编辑**既有** sibling (Spec #2) 文件，**本 Spec 内交付** (in-scope)。
  - **Downstream dependency edge** (header line 11 + §Out of Scope) = **未来独立** telemetry Spec
    (output 侧 disjoint)，**本 Spec 不交付**，168h 跑 AC-6 可评分仍依赖它。
  两者语义正交 (改现有 vs 依赖未来)，分属不同 section，措辞无 conflate。**区分干净**。

**结论**: 跨 Spec 耦合被四点锚定显式化；与遥测依赖边无混淆。R2 Critical A 的核心 (outcome-class
必须在 acceptance 实际查询的通道可区分，而非只在 Layer1 永不读的 `result.json`) 经 §B.6 (stderr
marker) + §C.3 (DB 持久化 + acceptance outcome-class-aware) 闭合。持久化载体给出 additive
`outcome_class` 列 **或** `dispatch_audit_log` payload (#147 B4 `json_extract`, `db.py:622` 先例) —
二者皆 DB 持久 + 可查询，AC-4/AC-12 钉死「非 result.json」需求，目标两路皆达 (见下 M-1 minor)。

### 3. TG task 排序 — 无依赖倒置 ✅

TG-2 现含 schema 迁移 (2.1 additive)，TG-3 亦含迁移 (3.1 value reformat) — 复核是否倒置:

- **TG-2 内序正确**: 2.1 (additive 列 + seed 写) 列于 2.3 (META 读列) / 2.4 (ISSUE_URL 读列) / 2.6
  之前。tasks.md 顺序 2.1→2.7 满足此依赖。
- **TG-2 不依赖 TG-3**: 2.4 ISSUE_URL 显式**读 additive 列** (raw_issue_number/target_repo)，
  **不 parse 复合 issue_id** → 与 TG-3.1 (issue_id 值重排) **解耦**。这正是 R2 additive-列修复的
  架构价值：把 fetch 通道从复合键剥离。
- **两迁移 disjoint 且已消歧**: tasks.md `:51` 明写「TG-3.1 值重排 distinct from TG-2.1 additive
  input columns (separate additive migrations, not a key change)」→ 读者不会误认两迁移触点冲突。
- **门控链自洽**: TG-4 (镜像) gates TG-1 only；TG-6 (E2E) gates TG-1+2+3+4；TG-2/TG-3 parallel-safe
  (line 22)。与 DEC §落地 排序一致 (container+assertion RED-first → Layer1 同 scope → key 迁移 →
  镜像冻结 → doc → E2E)。

**结论**: 无依赖倒置。两个 DB 迁移触点 disjoint 且经 tasks.md 显式消歧。

---

## 主线完整性复核 (三轮修订后)

- **C' 双通道**架构主线未受扰动: title/body→Forgejo fetch + metadata→Nomad META + 自主 always-fetch
  + file 模式仅 DEMO-/TEST- (§What + How 表 + Alternatives 完整)。
- **11 DEC 决策点无遗漏** (逐点比对 DEC `:74-84`): DP1 C' → §What/AD-M6-10 · DP2 ISSUE_ID → A.1/B.1 ·
  DP3 分工 → §What · DP4 always-fetch → §What · DP5 Layer1 同 scope → B.1-B.5 · DP6 fetch 失败契约 →
  A.3/C.4/B.6 · DP7 消毒 → A.4/A.7 · DP8 键+迁移 → D.1/D.2 · DP9 假绿 RED-first → C.1/C.2 · DP10
  base_branch → A.5/B.3 · DP11 镜像冻结 → E.1/E.2。**全覆盖**。
- **DP8 recon 修正强化非弱化**: DEC 忧「issue_id join 断 AC-2」；spec §D.2 code-ground 纠正为 AC-2 用
  `json_extract('$.issue_type_hint')` (非 issue_id join)，我核实 acceptance 脚本 AC-2 stratify 确读
  audit payload → 影响面更窄。这是 R1 「让 agent 读真代码抓设计者 altitude 漏」的正向产物，非漂移。
- **AD4-cell / AD-M0-5 消歧未回退**: R1 4-agent 抓出 DEC line 22 misattribution (bind-mount 假设误挂
  AD-M0-5)；spec §F.2/AD4-cell 修 `:384` mislabel + **不动 AD-M0-5 body (`:1035` m0-handoff schema)**。
  R3 保持此纠正 (F.2 + AC-10 + TG-5.2)。TG-5.3 更补 R2 km caveat (AD-M1-4 body `:1360` 有既存 9-enum
  doc/code drift，编辑前先核字面) — 依赖边诚实标注。

---

## Findings

| # | Sev | Class | Finding | Disposition |
|---|-----|-------|---------|-------------|
| M-1 | Minor | R2遗留(非阻塞) | outcome-class 持久化载体留「additive `outcome_class` 列 **OR** `dispatch_audit_log` payload」二选一 (B.6/C.3/AC-12)。二者皆 DB 持久 + 可被 acceptance 查询；AC-4/AC-12 已钉死「非 result.json」硬需求 + 两先例 (additive 002-007 / json_extract db.py:622) 均已印证。 | **接受**。Level 3 spec 粒度允许实现择一；架构目标 (acceptance-query-readable) 两路皆达，非结构缺口。Phase B 实施时任选其一即可，建议 A.3 task-planner 在 detailed-tasks 收敛为单一载体以免实现分叉。 |
| M-2 | Minor | 全新(观察) | `base_branch`/`files_hint` 的 seed-time 可得性弱于 raw_number/target_repo (后者代码印证在 seed 循环；前者依赖 triage/default_branch 兜底)。 | **非缺口**。二者为可空增强 metadata，AC-12 明定 NULL 优雅降级 + §A.5 容器 default_branch 兜底；承重 fetch 字段 (raw_number+repo) 确在 seed 可得，fetch 通道不受影响。仅记录，无需改。 |

无 Critical / 无 Important / 无新回归 / 无新结构缺口。

---

## Rationale

三个本轮重点 (seed additive 数据流 / cross-Spec 显式化 / TG 排序无倒置) 全部对真代码 `daf7c79`
核实通过:
1. **数据流闭合**: seed 有 raw_number(`:1176`)+repo(`:1133`)；S4 只见 dispatch_row(`:2109`)+硬编码
   env(`:2149`)；additive 列 (先例 002-007) 是唯一无重构桥梁 — R2 Critical B 诊断与修复**代码印证**。
2. **跨界耦合正确显式化**: acceptance 脚本 (`:224-227` `WHERE state='S9_CLOSE'`) 确为 Spec #2 未归档
   制品；四处锚定 (§Cross-Spec + AC-4 + TG-2.7 + OoS) 交付本 Spec 内；与遥测依赖边语义正交、无 conflate。
3. **排序自洽**: TG-2 内 2.1 先于读列任务；TG-2.4 读 additive 列**不 parse 复合键** → 与 TG-3.1 解耦；
   两迁移 disjoint 且已消歧；门控链与 DEC §落地 一致 — **无依赖倒置**。

C' 双通道主线 + 11 决策点经三轮修订仍完整；DP8 recon 修正、AD4-cell/AD-M0-5 消歧均为强化非回退。
两条 Minor 皆非结构缺口 (载体二选一 + 弱字段有兜底)，不阻塞收敛。

**架构自洽、无新结构缺口 → PASS (convergence, R2→R3 一致 PASS)。**
