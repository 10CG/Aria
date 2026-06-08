# aria-submodule-gate-block-flip — v1.29.0 warn→block 翻转

> **Level**: 2 (Minimal — proposal.md only; mechanism 全部继承自 parent Spec #124)
> **Status**: ⏸️ **DEFERRED (2026-06-07 D+14, NOT flipped)** — Trigger C (0 gate executions) + tripwire 验活 5/5 失败 → 两层防御无 live 证据 → owner-approved 规则降级 defer (见下 §D+14 OUTCOME)。机制层经 `aria-submodule-gate-operationalize` (R-fix-1 v1.40.0 + R-fix-2 v1.41.0, 已归档) **已 unblock**; 重启剩 owner 动作 (b) 攒 ≥3 真实 gate executions (host-cron 已装, tripwire 已绿)。新 hard date TBD (max D+42=2026-07-05)。*(原 Phase A.2 CONVERGED Approved 2026-05-25 via R1→Rev1→R2 PWW unanimous 3/3; ship deadline 2026-06-07 已过, 转 defer)*。
> **Change ID**: `aria-submodule-gate-block-flip`
> **Parent Spec**: `openspec/archive/2026-05-24-aria-submodule-pointer-regression-gate/` (Approved 2026-05-24, R1+R2 4-agent CONVERGED 3/3 unanimous)
> **Parent Forgejo issue**: [Aria #124](https://forgejo.10cg.pub/10CG/Aria/issues/124) (state=closed, closed_at 2026-05-24T17:19:41Z — verified via API)
> **Target version**: aria-plugin **v1.29.0** (Aria main repo **v1.7.1** patch for submodule pointer + tripwire cron; bump 升级为 minor v1.8.0 仅在 Phase B 实施时发现 main repo 实质 doc/流程变更 — bump 升级前必先 `grep '1.8.0' VERSION CHANGELOG.md` 验 slot 空闲)
> **Ship deadline**: 2026-06-07 (D+14 hard date,parent v1.28.0 ship 2026-05-24)。*若 2026-06-07 (Sunday) owner 不在线, 顺延 06-08 Monday 不视为 deferral*
> **Effort baseline (revised per R1 I-tl-5)**: ~5-6h end-to-end (Phase A.1 ~1h skeleton + A.2 audit ~1h + 2026-06-07 当天 §观察期数据汇总 ~1.5h + Phase B 实施 ~1.5h + Phase C dual-PR sequenced merge ~1h + Phase D archive + handoff ~0.5h)
> **Risk class**: Backward-compatible (ecosystem 14d 已有警告;override 机制 已存在;config flag `phase_c_integrator.submodule_gate.mode` 仍可显式 `"warn"` 回退;`mode="off"` 紧急 bypass 保留)
>
> ---
> **🔴 D+14 OUTCOME (2026-06-07): DEFERRED — NOT flipped.** Trigger C (0 gate executions) + tripwire 验活 run #11 = FAILURE (历史 5/5 全失败, 兜底从未运行) → option b 的"独立兜底"前提不满足 → owner-approved 规则降级 (c) defer。根因待修: R-fix-1 telemetry invocation gap (git 直驱绕过脚本) + R-fix-2 tripwire run failure。新 hard date TBD (max D+42=2026-07-05)。详见 `.aria/decisions/2026-06-07-v1.40.0-block-flip.md` §FINAL DECISION。Spec 保留在 changes/ 不归档。
>
> **⚠️ Ship-day prep amendment (2026-06-05, D+12 — per [[feedback_dec_ship_target_staleness_verify]])**:
> 1. **版本目标校正**: `aria-plugin v1.29.0` → **v1.40.0** (插件本 session 已 ship 到 v1.39.0;v1.29.0 slot 早跳过)。全文 `v1.29.0+` 表述 (= block 成默认的版本) → `v1.40.0+`。main repo v1.7.1 slot 仍空闲 ✓。
> 2. **§A flip 行号已漂移**: A1 `submodule_gate.sh` 仍 L33 ✓;A2 SKILL.md inline bash L378→**L450**;A3 config/wording 全集见决策记录 (06-07 grep-batch 复核)。
> 3. **观察数据 = 0**: `aria/metrics/` 仅 .gitkeep → `total_gate_executions=0` → **Trigger C (insufficient warm observation)**,非 Trigger B 正常翻转。14 天内三仓 10 PR merged 但 gate 0 执行 (gitlink bump 走 git 直驱绕过 telemetry 脚本)。06-07 owner 在 Risk R1 fallback (a) extend / (b) risk-accept flip / (c) defer 中选 + 签字。
> 4. **prep 不动 flip/SOT/merge** — 全部留 2026-06-07 (D+14 hard date)。详见 `.aria/decisions/2026-06-07-v1.40.0-block-flip.md` (DRAFT skeleton)。
> ---

---

## Why

**Direct trigger**: Parent Spec [`aria-submodule-pointer-regression-gate`](../../archive/2026-05-24-aria-submodule-pointer-regression-gate/proposal.md) §Two-phase rollout 明确承诺 v1.28.0 ship 后 14 天 (2026-05-24 → 2026-06-07) 内若 FP rate < 2% (over ≥20 WOULD-BLOCK events) 或 hard date 到达 (with ≥3 minimum **gate executions** observed,**不是** WOULD-BLOCK events — 详见 §决策框架 trigger B note) → 翻转 default mode `warn`→`block`。本 Spec 是该承诺的执行单元。

**Why now (D+1) draft skeleton, ship D+14**:
- Spec 结构 / 决策框架 / SOT 文件清单 可早期固化, 减少 deadline 当天起草压力
- post_spec audit 在 D+1 跑可早期发现结构问题 (audit baseline = R1+R2 unanimous PASS_WITH_WARNINGS per [[feedback_post_spec_audit_pragmatic_convergence]] + Level 2 per [[feedback_post_spec_audit_two_round_pragmatic_for_l2]])
- §观察期数据 section 留 TBD-2026-06-07 占位, ship 当天填入真实 FP 统计 + 决策记录
- Phase B+C+D (SOT bump / flag flip / tripwire cron / CHANGELOG / PR) 留到 2026-06-07 当天一气呵成 ship,避免 in-flight Spec 被其他工作打断

**Why mechanical flip, not "monthly review continues" path**:
- Parent Spec §Risk R2 明确: warn-only 模式无 trigger 翻转 = MEDIUM 风险 (gate 形同虚设, 操作者逐渐忽略 WOULD-BLOCK 日志)
- Hard date default-on policy (per qa R3 + code-reviewer R3 in parent R2 audit, see `.aria/audit-reports/post_spec-R2-2026-05-24T1515Z-aria-submodule-pointer-regression-gate.md`) = 沉默 (无显式 OpenSpec defer) → 自动翻转
- Override 机制 (commit trailer + PR label) 已存在 ≥14 天, ecosystem 有充分时间学习

**Why strengthens downstream (NOT blocks)** *(per R1 I-tl-3 correction)*: M6 sub-Spec `aria-2.0-m6-docs` 的 `T-B0.10` (standards submodule pointer bump precondition check) 是 **inline self-contained gate** (3-zone ancestry check,见 `openspec/changes/aria-2.0-m6-docs/tasks.md` L180-218),**不依赖** 本 Spec ship。但 M6 整体 PR 走 phase-c-integrator merge 时会被 §C.2.4.5 二次验证 — 形成 **dual-layer defense**: T-B0.10 inline (caller-side pre-stage) + §C.2.4.5 (PR-side merge gate)。Sequencing 推荐: 本 Spec v1.29.0 先 ship → M6 PR 享受 dual-layer。Layer L claim 协调避免共改 standards/。

---

## What

本 Spec ships **6 项 deliverables** (A-F), 全部为 minimal-cascade (无新机制, 无 SKILL.md 行为变更, 仅默认值翻转 + cron enable + SOT 同步):

### A. Default flip in **3 places** *(per R1 I-tl-1 — script + inline doc-Bash + config table 三处并行存在, 必须同步翻转)*

**A1. Bash script env-var default** — runtime SOT:
- File: `aria/skills/phase-c-integrator/scripts/submodule_gate.sh` (注意下划线, NOT 连字符)
- Line: **L33** (已 Phase A.0 verified)
- Change: `MODE="${ARIA_SUBMODULE_GATE_MODE:-warn}"` → `MODE="${ARIA_SUBMODULE_GATE_MODE:-block}"`

**A2. SKILL.md inline doc-Bash example** — illustrative SOT, 必须与 script 同步:
- File: `aria/skills/phase-c-integrator/SKILL.md`
- Line: **L378** (已 Phase A.0 verified)
- Change: 同 A1

**A3. SKILL.md config table default values** — config doc SOT (多行):
- File: `aria/skills/phase-c-integrator/SKILL.md`
- Lines: L47 / L184 / L192 / L300-301 / L307 / L443 等所有 `"warn"` 默认表述位置
- Ship 当天用 `grep -nE 'v1\.28\.0|v1\.29\.0|warn-only|warn\".*default|default.*warn' aria/skills/phase-c-integrator/SKILL.md` 取全集再 batch-review
- 例如 L47 `"warn"` v1.28.0 / `"block"` v1.29.0+ 表述 → 改为 `"block"` (v1.29.0+) | `"warn"` (legacy opt-out) | `"off"` (emergency bypass)

**Backward compatibility guarantee**: `mode="warn"` 仍可显式设置 (legacy opt-out), `mode="off"` 紧急 bypass 不变。env-var override `ARIA_SUBMODULE_GATE_MODE` 优先级仍 > config。

### B. Tripwire workflow: workflow_dispatch + schedule cron

**位于 Aria main repo, NOT aria-plugin** (per parent Rev1 R1-tl-3 fix)。**该 workflow 文件位于 Aria main repo, schedule cron 追加属 Aria main repo PR (Phase B.4) 范围, NOT aria-plugin PR (Phase B.3)** *(per R1 cr-Imp6)*。

`.forgejo/workflows/submodule-gate-tripwire.yml`:
- v1.28.0: 仅 `on: workflow_dispatch` (手工触发)
- v1.29.0: 追加 `on: schedule: - cron: "0 4 * * 0"` (每周日 04:00 UTC,与 parent CHANGELOG L57 承诺一致)

### C. 5+1 SOT bump (aria-plugin) per [[feedback_release_phase_d_5_files_synchronization]]

| 文件 | 字段 | 当前 v1.28.0 | 目标 v1.29.0 | 验证命令 |
|------|------|--------------|--------------|----------|
| `aria/.claude-plugin/plugin.json` (SOT) | `version` + `description` (verify Skills count 未变 = 32) | `"1.28.0"` | `"1.29.0"` | `grep -E '"(version\|description)"' aria/.claude-plugin/plugin.json` |
| `aria/.claude-plugin/marketplace.json` | **顶层 L3 `version` + L16 `plugins[].version` 两处都需同步** + `description` *(per R1 cr-Imp1+Imp4)* | `"1.28.0"` × 2 | `"1.29.0"` × 2 | `grep -n '"version"' aria/.claude-plugin/marketplace.json` (期望 2 命中) |
| `aria/VERSION` | `**版本**` + 发布日期 + minor 说明 | 1.28.0 | 1.29.0 | — |
| `aria/CHANGELOG.md` | **NEW `## [1.29.0]` entry** *(per R1 I-tl-2 — 不改 v1.28.0 历史 entry, 仅在 v1.28.0 entry 加 inline 注释 `<!-- shipped 2026-06-07 see [1.29.0] -->`)* | — | new entry | — |
| `aria/README.md` | `**Version**: X.Y.Z` (若有) | 1.28.0 | 1.29.0 | `grep -n 'Version' aria/README.md` |
| Aria 主项目 submodule pointer | `git add aria` (must point to v1.29.0 ship commit on master) | parent v1.28.0 SHA | v1.29.0 ship SHA | `git submodule status aria` |

### D. Aria main repo v1.7.1 patch bump

| 文件 | 当前 | 目标 |
|------|------|------|
| `VERSION` | 1.7.0 | 1.7.1 |
| `CHANGELOG.md` | `[Unreleased]` | `[1.7.1]` entry (submodule pointer bump + tripwire cron enable) |

**Note** *(per R1 cr-Min 3 strict)*: Aria main repo bump 是 patch (1.7.0→1.7.1),因为本 Spec 对 main repo 仅 (i) submodule pointer; (ii) `.forgejo/workflows/submodule-gate-tripwire.yml` schedule 追加 — 无 doc / 流程 / CLAUDE.md 实质变更。若 Phase B 实施中发现 main repo CLAUDE.md 需 cross-ref 更新 (e.g., Rule #8 / 新加 Rule for submodule hygiene),则 bump 升级为 minor (1.7.0→1.8.0),**升级前必先 verify v1.8.0 slot 未占** (`grep '1.8.0' VERSION CHANGELOG.md`),再决定。

### E. 决策记录 doc (Flip Decision Record)

新建 `.aria/decisions/<ship-date>-v1.29.0-block-flip.md`:
- **文件名 ship-date 占位** *(per R1 cr-Imp5 — 若 R1 fallback (a) extend window 导致 ship 实际日期 ≠ 2026-06-07,文件名按实际 ship 日期改, 不 hardcoded)*
- §1 决策日期 + 决策者 (simonfishgit per parent Rev1 M-qa-6 fix)
- §2 观察期数据汇总 (见本 Spec §观察期数据 section, ship 当天 copy 过去)
- §3 翻转依据 (FP-threshold OR hard-date + minimum-observation guard OR override-rate)
- §4 若 <3 events fallback decision (extend window / explicit risk-accept / defer)
- §5 Cross-ref to parent Spec + this Spec + audit reports
- **§6 (NEW per R1 I-tl-4)**: ship 当天 open PRs 审查结果 (stale-branch-first-merge-after-flip 风险 mitigation,见 §Risk R7)

### F. SKILL.md / 跨引用文档措辞更新 (wording sync only — NOT default flip; default flip 由 §A 负责)

| 文件 | 改动 |
|------|------|
| `aria/skills/phase-c-integrator/SKILL.md` | wording sync (非 default flip): 所有 `v1.28.0` / `v1.29.0+` 时态说明改为现在时 (v1.29.0+ mode=block 默认),保留历史叙述行 (e.g., L294 "v1.28.0 ships warn-only" 不改, 体现 changelog 风格);ship 当天用 `grep -nE 'v1\.28\.0\|v1\.29\.0' aria/skills/phase-c-integrator/SKILL.md` 取全集再 review *(per R1 cr-Imp3 + tl m-tl-1 — 不 hardcode 行号)* |
| `aria/CHANGELOG.md` | **NEW v1.29.0 entry**: "flips v1.28.0 warn→block per Two-phase rollout 承诺, observation 数据见 `.aria/decisions/<ship-date>-v1.29.0-block-flip.md`";v1.28.0 entry L32 "v1.29.0 (planned, ...)" **保留原文** + 可选 inline 注释 `<!-- shipped <ship-date> see [1.29.0] -->` *(per R1 I-tl-2 immutability)* |
| `standards/conventions/submodule-pointer-hygiene.md` | **确定要改** *(per R1 cr-Min 2 — `standards/conventions/submodule-pointer-hygiene.md` L6/L8/L76-83 多处直接说 v1.28.0+ warn-only / v1.29.0+ block, 非 "若")*: §Mechanical enforcement (v1.28.0+) → (v1.29.0+);L80 删除 14-day observation window 段(已 elapsed);L81 改 block 为现在时 |
| `Aria/CLAUDE.md` | §不可协商规则 表格 cross-ref `aria-plugin v1.28.0+ §C.2.4.5 mechanical gate companion` → `v1.29.0+`;`description` 字段 verify (本 Spec 无 Skill 数变化,应保持 "32 Skills") |
| `aria/.claude-plugin/{plugin,marketplace}.json` | `description` 字段 verify 一致性 *(per R1 cr-Imp4 — 历史 patch 1 Skills count 31→32 typo 失同步前车之鉴)* |

---

## How

### 实现序列 (Phase B,2026-06-07)

```
B.1 分支创建: feature/v1.29.0-block-flip (aria-plugin)
              feature/v1.29.0-bump (Aria 主仓, 等 aria-plugin merge 后再起)
              Layer L claim: track-id "aria-submodule-gate-block-flip"
                             含文件 aria/skills/phase-c-integrator/SKILL.md + scripts/submodule_gate.sh
                             写 claim YAML 到 refs/aria/coordination
                             *(per R1 cr-Min 2 — parent §R8 Phase B.1 claim 模式继承)*

B.2 执行验证 (aria-plugin) — 估时 ~1.5h:
  step 0 (NEW per R1 I-tl-5): §观察期数据汇总 ~1h
    - 读 aria/metrics/submodule-gate-warns.jsonl (warn-only 14d 事件)
    - 读 aria/metrics/submodule-gate-blocks.jsonl (含 fetch/refspec error events)
    - 读 aria/metrics/submodule-gate-overrides.jsonl (override 使用率)
    - 读 aria/metrics/submodule-gate-misses.jsonl (tripwire detection events)
    - cross-ref Forgejo PR merge log: `forgejo GET /repos/10CG/Aria/pulls?state=closed&base=master&merged=true`
      获取 total_pr_merges_in_window (口径: 主项目 + aria-plugin + standards 三仓 master 在 window 内所有 merge commits, NOT dev/feature 分支) *(per R1 tl m-tl-2)*
    - 计算 total_gate_executions (= 上述 4 个 jsonl 行数总和 + 无事件 PR 推算 fallback)
    - 计算 FP rate (= human_reviewed_as_fp_true / (true + false), 排除 null per parent §FP labeling L237)
    - 填入本 Spec §观察期数据 section
  step 1: 起草 .aria/decisions/<ship-date>-v1.29.0-block-flip.md (Flip Decision Record) — owner signoff
  step 2: §决策框架 trigger 选择 (A/B/C/D/E/F),写决策依据
  step 3: 应用 §A (3 处 default flip): script L33 + SKILL.md L378 + config table grep-batch
  step 4: 应用 §F (措辞同步): CHANGELOG L32 注释 + standards convention + CLAUDE.md cross-ref + description 字段 verify
  step 5: 应用 §C (aria-plugin 5+1 SOT bump 到 1.29.0)
  step 6: dogfood 验证 — 明确测试命令 *(per R1 QA m-2 + m-3)*:
    ```bash
    unset ARIA_SUBMODULE_GATE_MODE
    cd /tmp && git clone <test-fixture-repo> && cd test-fixture-repo
    ./submodule_gate.sh  # 期望: MODE 从 L33 ${:-block} 读取,verdict 取决于 fixture 状态
    ```
    + 若 13 现有 assertions 未覆盖 default-block path → 新增 T-replay-14: default mode=block (no env var), regression PR, expect exit 1
  step 7: replay test (parent Spec 13 assertions × 10 scenarios) 重跑确认未 regress
  step 8: Phase B exit — git diff 自审, 提交分支

B.3 phase-c-integrator (aria-plugin PR) — 估时 ~0.5h:
  step 1: C.2.4 (Rule #8 aether ci status gate, Aria 项目无 aether 走 skip_with_warning)
  step 2: C.2.4.5 (per `standards/conventions/submodule-pointer-hygiene.md` convention, NOT numbered Rule per parent AD-FOLLOWUP-4) — 本次是首个 cross-validate dogfood — 本 PR 不动 submodule,gate 应 verdict=pass *(per R1 tl m-tl-5)*
  step 3: C.2.5 (multi-remote push: forgejo origin + github)
  step 4: PR merge

B.4 Aria main repo PR (post aria-plugin merge) — 估时 ~0.5h:
  step 1: git submodule update --remote aria → 拿到 v1.29.0 SHA
  step 2: .forgejo/workflows/submodule-gate-tripwire.yml 追加 schedule cron (cron 改动属本 PR scope)
  step 3: §D (main repo VERSION + CHANGELOG 1.7.1 entry)
  step 4: PR open → C.2.4 + C.2.4.5 *(chicken-and-egg 注: 此时主项目 phase-c-integrator runtime 仍是 v1.28.0 warn-mode — 主项目 PR 的目的就是 bump aria submodule 到 v1.29.0;主项目 PR merge 完成后,**下一个 PR** (D+15 或更晚) 才是 first real block-mode dogfood, per R1 tl m-tl-3)*
  step 5: PR merge
  step 6: post-merge 验证 — 在 aria-plugin 或 standards submodule 有变更的**下一次** PR merge 中,确认 §C.2.4.5 workflow 输出包含 `MODE=block`(无论 verdict 是 PASS / BLOCK / override)*(per R1 QA m-5 — 明确 acceptance criteria)*

Phase D 收尾 — 估时 ~0.5h:
  D.1 进度更新 (UPM N/A per Aria 项目)
  D.2 archive Spec → openspec/archive/<ship-date>-aria-submodule-gate-block-flip/
  D.3 session handoff in docs/handoff/<ship-date>-aria-submodule-gate-block-flip-shipped.md (Rule #9)
```

### Mechanism 引用

完整 gate 机制 (fail-loud fetch / refspec assertion / 双向 ancestry / override / telemetry) 均继承自 parent Spec, 详见:
- `openspec/archive/2026-05-24-aria-submodule-pointer-regression-gate/proposal.md` §How
- `aria/skills/phase-c-integrator/SKILL.md` §C.2.4.5 (v1.28.0 ship)
- `standards/conventions/submodule-pointer-hygiene.md` (companion convention)

本 Spec **零新机制**, 仅 default flag 翻转 + cron enable + 文档措辞同步 + SOT bump。

---

## §标注操作流程 (FP labeling workflow, D+0 → D+14) — NEW per R1 QA C-2

parent Spec L237 定义 `human_reviewed_as_fp: true|false|null` 字段由 simonfishgit (owner) monthly review 标注。本 Spec 14d 观察窗口 (D+0 = 2026-05-24 → D+14 = 2026-06-07) 恰为第一个 monthly review 周期。**ship 当天 (D+14) 数据填充依赖此字段, 必须有可执行流程**:

| 项 | 规则 |
|----|------|
| **标注时机** | 每次 WOULD-BLOCK 事件发生后 **24h 内** 标注。Phase D 当天 (D+14) 批量回顾未覆盖 null 条目。 |
| **标注 owner** | simonfishgit (与 parent §FP labeling L237 一致) |
| **标注操作方式** | (a) JSONL 文件位于 `aria/metrics/` (`.gitignore` 内, 不随 PR 提交);(b) 手工编辑对应行,追加 `,"human_reviewed_as_fp":true\|false` 字段;(c) 在 `.aria/decisions/<ship-date>-v1.29.0-block-flip.md` §2 数据汇总段记录标注结果 (含每个 event 的 cross-ref PR URL + 判定理由) |
| **判定依据** | 对每个 WOULD-BLOCK event cross-ref 对应 PR 的 merge commit message + PR intent:legitimate rollback (revert bug / hotfix backout) → `true` (FP);actual regression (stale ref / 跨终端冲突) → `false` (true block);under investigation → `null` (pending) |
| **D+14 null 条目处理** | 若 D+14 当天仍存在 null 条目:(a) 默认 **保守视为 `false` (not FP)** — 即 conservative true-block,不计入 FP rate 分子;(b) 备选: 延迟 1-2 天待标注完成再决策 (R1 fallback (c));(c) 决策 doc §3 必须显式记录 null-pending 处理方式 |
| **Owner sign-off** | 参照 Rule #7 `secret-leak-ok-explicit` 模式,标注 + 决策操作均须 owner sign-off 记录在决策 doc |

---

## 决策框架 (Flip Decision Criteria)

ship 当天 (D+14 = 2026-06-07) 依据下表选择翻转 trigger,记录于 `.aria/decisions/<ship-date>-v1.29.0-block-flip.md` §3:

| Trigger | 条件 | 决策 |
|---------|------|------|
| **A. FP-threshold (preferred)** | `FP_count / total_WOULD-BLOCK_events < 2%` sustained over **≥20 WOULD-BLOCK events** | 翻转 block, 决策 doc 记 FP rate + raw 事件列表 |
| **B. Hard-date + minimum-observation guard (default fallback)** | `now >= 2026-06-07` AND **`total_gate_executions >= 3`** (NOT WOULD-BLOCK events — per R1 QA C-1 + parent L234 原文 "≥3 minimum gate executions observed") AND `no FPs requiring redesign` | 翻转 block, 决策 doc 记 hard date 触发 + total_gate_executions + total_would_block + FP分布 |
| **C. Insufficient warm observation (< 3 gate executions)** | `now >= 2026-06-07` AND **`total_gate_executions < 3`** | 见下文 §Risk R1 fallback (默认推荐 (a) extend per R1 QA I-3 — gate executions 不可知 / 极少时, 保守路径优于风险接受翻转) |
| **D. High FP rate (≥ 2%)** | FP rate ≥ 2% sustained over ≥20 events **OR** intermediate 3-19 events 区间出现 FP rate > 2% (e.g., 5 events / 1 FP = 20% — 视为 requiring redesign, 转入此 trigger 处理) *(per R1 QA I-2 中间地带覆盖)* | **不翻转**;file 新 OpenSpec 重新设计 gate 灵敏度 (parent §AD-FOLLOWUP 范围) |
| **E. Explicit defer** | owner 显式判断需延后 (e.g., ecosystem 大型 PR window 临近) | **不翻转**;file 显式 OpenSpec defer with 理由 + 新 hard date (受 §Risk R1 max defer outer bound 约束) |
| **F. High override-usage (>15%)** *(NEW per R1 I-tl-7 + cr Min 6)* | `override_rate = (trailer + label) / total_PR_merges_in_window > 15%` | **不翻转**;file 新 OpenSpec 重审 gate 灵敏度 + 是否扩展 override 机制 (e.g., persistent label class)。可与 trigger A/B 平行评估; F 优先级 > A/B (高 override 表明合理 rollback 频繁, block 模式翻转会引发更多 friction) |

**Default-on policy** (per parent Spec): 沉默 (无显式 OpenSpec defer 在 D+14 前 file) = ready to flip at hard date IF minimum-observation guard met (trigger B) AND override rate ≤ 15% (trigger F not triggered)。

---

## §观察期数据 (TBD-2026-06-07)

> **NOTE**: 本 section 在 ship 当天 (D+14) 填入。Phase A 起草时 (D+1) 仅留 schema 占位。
> 数据源: `aria/metrics/{submodule-gate-warns,blocks,overrides,misses}.jsonl` (JSONL race-safe, parent Spec 已建立) + Forgejo Aria PR merge log (`forgejo GET /repos/10CG/Aria/pulls?state=closed&base=master&merged=true`)。
> `pr_url` 构造模板: `https://forgejo.10cg.pub/10CG/Aria/pulls/<NUM>` *(per R1 cr-Min 5)*

```yaml
# 填入示例 (D+14 当天):
observation_window:
  start: "2026-05-24T17:09Z"  # aria-plugin v1.28.0 ship 6c07727
  end: "2026-06-07T??:??Z"    # flip decision 时刻
  duration_days: 14
  metrics_dir_used: "aria/metrics/" | "metrics/" | <other via ARIA_METRICS_DIR>  # 口径 per R1 Q-tl-4

events:
  # CRITICAL fields (drive 决策框架 trigger 判定)
  total_gate_executions: <int>            # = 含 PASS + WOULD-BLOCK + override + fetch_failure 全部 gate 调用次数
                                          # 数据源: warns.jsonl 行数 + blocks.jsonl 行数 + overrides.jsonl 行数 + misses.jsonl 行数 +
                                          #         (total_pr_merges_in_window - 已 telemetry PR count) 推算 PASS 数
                                          # 触发 trigger B/C minimum-observation guard 条件
  total_would_block: <int>                # = warns.jsonl 行数 (warn-only 模式 detection events)
  human_reviewed_as_fp_true: <int>        # 误报数 (legitimate rollback misidentified, per §标注操作流程)
  human_reviewed_as_fp_false: <int>       # 真实拦截数 (actual regression)
  human_reviewed_as_fp_null: <int>        # 未审查 (pending); D+14 默认按保守 false 处理 per §标注操作流程
  fp_rate: <float>                        # = true / (true + false)

  # Gate health diagnostics
  gate_errors:                            # *(per R1 QA m-1)*
    fetch_failure_count: <int>            # exit code 2 (3-attempt 1s/2s/4s 全失败)
    origin_rewrite_count: <int>           # exit code 3 (force-push history rewrite detected)

per_pr_breakdown:
  - pr_url: "https://forgejo.10cg.pub/10CG/Aria/pulls/<NUM>"  # 若 pr_id="unknown" → 手动 cross-ref git log
    timestamp: "..."
    submodule: "..."
    master_ptr: "..."
    feature_ptr: "..."
    verdict: "WOULD-BLOCK | BLOCK | override | fetch_failure | origin_rewrite"
    classification: "fp | true_block | pending"
    note: "..."

override_usage:
  trailer_count: <int>                    # Submodule-Rollback: trailer 触发
  label_count: <int>                      # submodule-rollback-approved label 触发
  total_pr_merges_in_window: <int>        # 口径: 主项目 + aria-plugin + standards 三仓 master merge commits, NOT dev/feature 分支
  override_rate: <float>                  # = (trailer + label) / total_pr_merges_in_window
                                          # >15% triggers §决策框架 Trigger F deferral

tripwire_health:                          # *(per R1 I-tl-6 — parent §R9 NEW Rev1 R1-qa M-qa-3)*
  workflow_dispatch_runs_in_window: <int> # v1.28.0 期 workflow_dispatch only, owner 手工触发次数
  last_manual_run_timestamp: "..."
  ready_for_schedule_enable: true | false # ship 当天验证 workflow 在 schedule cron 之前可正常 run
  notes: "..."

decision_trigger: "A | B | C | D | E | F"  # 对应 §决策框架 表格
decision_rationale: "..."                  # 自由文本, owner 签字
```

**Phase A.2 audit 应验证**: 本 section schema 完整;不需要审阅数据 (D+1 尚无)。

---

## Risk + Mitigations

| ID | Risk | Likelihood | Mitigation |
|----|------|-----------|------------|
| R1 | **观察期 <3 gate executions** (insufficient warm observation, parent §qa R3) | MEDIUM (Aria 项目 PR 频次低) | **Fallback 3 路径**: (a) extend warn-only window 下一 20 PR merges,新 hard date 写决策 doc;(b) flip with explicit risk-acceptance note (owner 显式签字 "接受零数据风险, 依据机制设计已 13 assertions 覆盖");(c) 延迟 1-2 周 file 显式 OpenSpec defer。**默认推荐 (a) extend** *(per R1 QA I-3 — gate executions 不可观测 / 极少时 (b) 风险接受路径无证据基础, 保守 extend 路径优先)*。**最大延迟上界 (max defer outer bound)**: `D+42 (= D+28 for fallback-a 20-PR window + D+14 buffer)`。超过此日期若仍无足够数据,默认执行 (b) flip with risk-acceptance 并记录 *(per R1 QA I-4)*。 |
| R2 | **FP rate > 2%** → gate 灵敏度需调整 | LOW (parent audit 已大量 stress test) | 不翻转;file 新 OpenSpec 重新设计 gate 灵敏度 (parent §AD-FOLLOWUP 范围)。FP source 候选: nil-SHA (parent §R5) / force-push race (parent §R6) — 优先审查这两类 |
| R3 | **First post-flip PR 误 block** (override 机制不熟悉) | LOW | parent Spec override 已 14d 教育期;`standards/conventions/submodule-pointer-hygiene.md` 已 ship;BLOCK 输出包含 override hint (commit trailer + PR label 两种方式) |
| R4 | **Tripwire cron schedule 触发噪音** (weekly cron alert fatigue) | LOW | tripwire 仅在 detect 到 escaped regression 时报警, 无 regression 静默;parent §Tripwire location 已设计 |
| R5 | **跨 Spec 协调** — M6 sub-Spec `aria-2.0-m6-docs` T-B0.10 与本 Spec 关系 *(per R1 I-tl-3 重写)* | LOW-MEDIUM | (a) M6 T-B0.10 inline ancestry check 已 self-contained, **不依赖** v1.29.0 ship;(b) 但 M6 整体 PR 走 phase-c-integrator merge 时会被 §C.2.4.5 block-mode 二次验证 (dual-layer defense)。若 M6 PR 在 v1.29.0 ship **之前** 合 master, 则只有 T-B0.10 inline check 生效; 若在 v1.29.0 ship **之后**, 则 dual-layer 都生效。**实际 sequencing 推荐**: 本 Spec v1.29.0 先 ship → M6 PR 享受 dual-layer。Layer L claim 协调避免共改 `standards/` 路径 (per [[feedback_concurrency_advisory_over_hardlock]])。 |
| R6 | **Spec 起草 D+1 → ship D+14 漂移** *(per R1 tl m-tl-6 — 区分 Spec doc immutable vs SKILL.md code mutable)* | LOW | (a) parent Spec **已 archived**,doc 字面 immutable;(b) `aria/skills/phase-c-integrator/SKILL.md` §C.2.4.5 code **可 hotfix** (若发现 bug)——但任何 hotfix 都会反映在 §观察期数据 (新版本 SHA + 行为变化), 在 ship 当天 step 0 数据汇总时会 surface, 不会 silent drift |
| R7 | **stale-branch-first-merge-after-flip** *(NEW per R1 I-tl-4)* — long-lived feature branch 在 v1.28.0 warn-only 期间最后 push, 但 v1.29.0 ship 后才走 merge | LOW-MEDIUM (Aria 项目 PR 频次低, long-lived branch 少) | (a) ship 当天审 open PRs 列表 (`forgejo GET /repos/10CG/Aria/pulls?state=open`), 对涉及 submodule pointer 改动的 PR 主动 ping owner 提醒 override;(b) BLOCK 输出已含 override hint (parent ship);(c) 决策记录 doc §6 记录 ship 当天 open PRs 审查结果 + 是否触发 ping |

---

## Validation Checklist

### Phase A.1 (本 commit + Rev1)
- [x] proposal.md skeleton 起草
- [x] §决策框架 + §观察期数据 schema 占位
- [x] §Risk 含 R1 insufficient warm observation fallback + max defer outer bound (D+42)
- [x] Version slots 验证 (aria-plugin v1.29.0 / Aria v1.7.1 均未占用)
- [x] Cross-ref to parent Spec + DEC-20260524-002 + M6 T-B0.10 协调 (NOT blocking)
- [x] Aria #124 state=closed verified via API (closed_at 2026-05-24T17:19:41Z)
- [x] **Rev1 applied (R1 → R2 待跑)**: 2 Critical (QA C-1 gate executions / C-2 FP labeling workflow) + 13 Important + 8 Minor fixed

### Phase A.2 (本 session 内)
- [ ] post_spec R1 audit (**3 agents per Level 2 baseline**: tech-lead + qa + code-reviewer per [[feedback_post_spec_audit_two_round_pragmatic_for_l2]]) *(per R1 tl m-tl-9 + cr Min 4)*
- [x] R1 audit completed (3 agents, 1 REVISE + 2 PASS_WITH_WARNINGS)
- [x] Rev1 applied (本 commit)
- [x] post_spec R2 audit CONVERGED (3/3 unanimous PASS_WITH_WARNINGS, 2 Critical CLOSED, 0 new Critical;Level 2 baseline per [[feedback_post_spec_audit_pragmatic_convergence]] 满足)
- [x] Spec Status 更新为 Approved (2026-05-25)

### 2026-06-07 当天 (Phase B+C+D) — pre-ship checklist
- [ ] **(NEW per R7)** ship 前审 open PR 列表 (`forgejo GET /repos/10CG/Aria/pulls?state=open`),identify submodule-touching PRs,主动 ping owner override
- [ ] **(NEW per R1 I-tl-6)** tripwire workflow 至少手工 dispatch 触发 1 次, 确认 ready for schedule cron enable
- [ ] §观察期数据 section 填入真实 14d FP 数据 (Phase B step 0)
- [ ] §标注操作流程 D+14 null 条目处理 (默认保守 false)
- [ ] `.aria/decisions/<ship-date>-v1.29.0-block-flip.md` 起草并签字 (含 §6 ship-day open PRs 审查)
- [ ] §决策框架 trigger 选择 (A/B/C/D/E/F) + rationale + override_rate ≤ 15% 验证
- [ ] §A 3 处 default flip 应用 (script L33 + SKILL.md L378 + config table grep-batch)
- [ ] §F wording sync (CHANGELOG v1.28.0 entry 保留 + 加 inline 注释 + v1.29.0 new entry / standards convention / CLAUDE.md cross-ref / description 字段 verify 一致)
- [ ] §B (tripwire schedule cron) 追加 (Aria main repo PR scope)
- [ ] §C (aria-plugin 5+1 SOT bump) + §D (Aria main repo 1.7.1 bump,若 minor 升级先 verify v1.8.0 slot 空闲)
- [ ] dogfood: `unset ARIA_SUBMODULE_GATE_MODE && ./submodule_gate.sh` 确认 MODE default = block
- [ ] replay test 13/13 PASS unchanged + (optional) T-replay-14 default-block path 新增
- [ ] aria-plugin PR merge → main repo PR merge → 双 PR multi-remote push verified
- [ ] post-merge dogfood: 下一 PR 触发 §C.2.4.5 时 MODE=block 出现在 workflow output
- [ ] Phase D archive: `openspec/archive/<ship-date>-aria-submodule-gate-block-flip/`
- [ ] D.3 session handoff in `docs/handoff/<ship-date>-aria-submodule-gate-block-flip-shipped.md`

---

## Cross-references

### Parent Spec & decision records
- `openspec/archive/2026-05-24-aria-submodule-pointer-regression-gate/proposal.md` (Approved 2026-05-24,完整 audit trail 见 parent proposal.md §Audit trajectory L18-22)
- `.aria/decisions/2026-05-24-aria-124-submodule-pointer-regression-gate.md` (DEC-20260524-002, brainstorm origin)
- `.aria/audit-reports/post_spec-R1-2026-05-24T1459Z-aria-submodule-pointer-regression-gate.md`
- `.aria/audit-reports/post_spec-R2-2026-05-24T1515Z-aria-submodule-pointer-regression-gate.md`

### This Spec's audit reports
- `.aria/audit-reports/post_spec-R1-tl-2026-05-25-aria-submodule-gate-block-flip.md` (PASS_WITH_WARNINGS)
- `.aria/audit-reports/post_spec-R1-qa-2026-05-25-aria-submodule-gate-block-flip.md` (REVISE → 已 Rev1)
- `.aria/audit-reports/post_spec-R1-cr-2026-05-25-aria-submodule-gate-block-flip.md` (PASS_WITH_WARNINGS)

### Companion artifacts
- `standards/conventions/submodule-pointer-hygiene.md` (parent ship, §F 确定需更新)
- `aria/skills/phase-c-integrator/SKILL.md §C.2.4.5` (parent ship, mechanism unchanged; §A2+A3 default flip)
- `aria/skills/phase-c-integrator/scripts/submodule_gate.sh` (parent ship; §A1 runtime SOT default flip)
- `aria-plugin-benchmarks/submodule-gate/` (parent Rule #6 structural substitute, 10-scenario README)
- `.forgejo/workflows/submodule-gate-tripwire.yml` (parent ship workflow_dispatch only; §B 追加 schedule cron 属 Aria main repo PR scope)

### Downstream strengthened (dual-layer defense, NOT blocked)
- M6 sub-Spec `openspec/changes/aria-2.0-m6-docs/tasks.md` T-B0.10 (standards submodule pointer bump precondition,inline self-contained; v1.29.0 ship 强化为 dual-layer 而非解除 block)

### Rule references
- Aria CLAUDE.md §不可协商规则 #6 (Skill benchmark — Rule #6 substitute artifacts inherited from parent, no re-benchmark needed since no behavior change, per [[feedback_deterministic_structural_skill_rule6_substitute]])
- Aria CLAUDE.md §版本管理规范 (5+1 SOT bump checklist, per [[feedback_release_phase_d_5_files_synchronization]])
- Aria CLAUDE.md §不可协商规则 #7 (`secret-leak-ok-explicit` 模式 — §标注操作流程 owner sign-off 借鉴)
- Aria CLAUDE.md §不可协商规则 #8 (Rule #8 aether CI gate, runs BEFORE this Spec's §C.2.4.5 gate per parent ship)
- Aria CLAUDE.md §不可协商规则 #9 (Session handoff D.3 in `docs/handoff/`)

### Memory references
- [[feedback_release_phase_d_5_files_synchronization]] — 5+1 SOT atomic bump (Phase B step 5 + Aria main repo D step 3)
- [[feedback_post_spec_audit_pragmatic_convergence]] — convergence rule (unanimous + verdict 改善 + 无振荡)
- [[feedback_post_spec_audit_two_round_pragmatic_for_l2]] — Level 2 R1+R2 unanimous baseline + 3 agents
- [[feedback_dec_ship_target_staleness_verify]] — Phase A.0 完成 (VERSION + plugin.json + CHANGELOG 已 verify)
- [[feedback_sequenced_multirepo_gitlink_bump]] — Phase B.3→B.4 顺序 (aria-plugin merge → re-bump → main repo merge)
- [[feedback_deterministic_structural_skill_rule6_substitute]] — deterministic Skill Rule #6 substitute, 本 Spec 零行为变化继承 parent artifacts
- [[feedback_concurrency_advisory_over_hardlock]] — Layer L claim advisory 协调 (§Risk R5)

---

**Created**: 2026-05-25T~12:00Z (Phase A.1 skeleton)
**Rev1 applied**: 2026-05-25T~13:30Z (post-R1 audit, 2 Critical + 13 Important + 8 Minor fixed)
**Author**: spec-drafter (Claude Opus 4.7 1M context) via /aria:phase-a-planner
**Ship target**: 2026-06-07 (D+14 hard date from parent v1.28.0 ship 2026-05-24; Sunday → 顺延 06-08 Monday 不视为 deferral)
**Phase A.2 R2 CONVERGED**: 2026-05-25T~14:30Z (3/3 unanimous PASS_WITH_WARNINGS; 2 Critical CLOSED; 4 new Minor batched for Phase B.1 — N-1 PASS 推算 telemetry 超过 PR merge 总数 fallback / N-2 trigger 优先级 / N-3 B.4 step 6 cross-ref / N-4 monthly review cadence 假设 / n-tl-1 acceptance window outer bound / n-tl-2 events 口径)
**Next**: Phase B+C+D ship 2026-06-07 (D+14 hard date)
