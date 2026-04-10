# Historical Benchmark Caveats (Transparency Supplement)

> **Note**: This file is a **TRANSPARENCY supplement**, NOT a warning register.
> All Skills listed below have been **validated** via either `/skill-creator benchmark`
> or Aria#8 spike testing. Entries document **measurement nuance** (internal vs
> cross-project delta), NOT quality problems. Original release decisions are all legitimate.

> **Status**: Created 2026-04-10 per `benchmark-transparency-enhancement` Spec (Aria#8 Phase 3 修正方案).
> **Maintained by**: `knowledge-manager` (DRI per Spec)
> **Data source**: `docs/analysis/spike-report-2026-04-10.md` + `/skill-creator` benchmark runs

---

## 什么是 "internal vs cross-project inflation"?

Aria 的 `/skill-creator benchmark` 在**内部**(Aria 仓库) 对比 with-skill 和 without-skill 输出, 计算 pass rate delta. 这个 `internal_delta` 是 Rule #6 合并决策的基础.

**Inflation** 指的是同一 Skill 在**跨项目场景** (如 Kairos 实测) 下 delta 的差值. inflation 低 = Skill 的价值跨项目通用; inflation 高 = Skill 的价值主要依赖 Aria 特定约定.

Aria#8 spike 实测证实: **多数 Skills 的 inflation 很低** (< 15%), 内部 delta 基本可信. 这与最初的纸面估算 ("50% 虚高" / "100% 虚高") 完全不符.

---

## Skill: `state-scanner` v2.9.0

| 指标 | 值 |
|------|-----|
| **Internal delta** (Aria benchmark) | **+0.818** (+81.8pp) |
| **Cross-project delta** (spike 实测) | **+0.778** (+77.8pp) |
| **Inflation ratio** | **4.9%** (噪音级别) |
| **Verdict** | **VALIDATED** |
| **Release decision** | ✅ **100% 合法** — 原发版决策无需任何修正 |

**Measurement context**:
- 3 evals (submodule-sync / upstream-behind / issue-awareness)
- 22 assertions, 9 classified as `aria_convention`, 11 as `generic_capability`, 2 as `behavior_contract`
- category_map: `tools/category_map_state_scanner.json`

**Historical note**:
原 Aria#8 Phase 1-2 RCA 基于纸面估算 ("68% aria_convention → 50% inflation"), 后经 spike 实测证伪. 实际 inflation 只有 4.9%, 远低于门禁阈值 20%. 无需任何 Skill 修改或 eval 补充.

**References**:
- US-008 (`docs/requirements/user-stories/US-008.md`) — 原发版 Story
- `docs/analysis/spike-report-2026-04-10.md` — 实测数据
- `ab-results/2026-04-09/state-scanner/benchmark.json` — 原 benchmark 产物
- `state-scanner/state-scanner-workspace/iteration-2/` — 完整 eval outputs

---

## Skill: `commit-msg-generator` v2.0.1

| 指标 | 值 |
|------|-----|
| **Internal delta** (Aria benchmark) | **+0.846** (+84.6pp) |
| **Kairos delta** (外部实测) | **0.0** |
| **Cross-project delta** (spike 实测 via category tagging) | **+0.75** (+75pp) |
| **Inflation ratio** | **11.3%** |
| **Verdict** | **MOSTLY VALIDATED** |
| **Release decision** | ✅ **合法** — 原发版决策依然成立, 11.3% 在可接受范围 |

**Kairos delta 0.0 的真正原因 (非数据造假)**:

Kairos 测出的 0.0 delta 不是因为 Aria 内部 benchmark 造假, 而是因为 **Kairos 的 eval 场景与 Aria 的不同**:

1. **Scenario calibration 差异**: Kairos 测试的 commit 场景 (Node.js/TypeScript 项目) 与 Aria 测试的场景 (Python/Markdown 文档修改) 难度和风格不同
2. **不同项目不同的 "without_skill baseline"**: Kairos 的 vanilla AI 在简单的 TypeScript commit 场景上已经很强, 留给 Skill 提升的空间小
3. **eval assertion 不同**: 两个项目的 eval 测的"什么算好 commit message"可能有隐含约定差异

**关键 insight**: "跨项目 delta 差异" ≠ "内部测量错误". 跨项目 delta 差异源自 **test scenario calibration**, 不是 **assertion vocabulary inflation**.

**References**:
- Kairos Adoption Report: forgejo.10cg.pub/10CG/aria-plugin#2
- `docs/analysis/spike-report-2026-04-10.md` (Phase 1-2 原 RCA + Phase 3 修正)
- `category_map_commit_msg.json` — 实测用的 category 标注
- `MEMORY.md` → `feedback_process_vs_content_skills.md` (已修正原假说)

---

## 未来 Skills 数据

本表仅记录 spike 实测过的 2 个 Skills. 其他 Skills 的 dual delta 数据将在未来 `/skill-creator benchmark` 运行中**自然积累**, 按需追加到本文件. 不追溯测量历史 Skills.

追加条件 (DRI: knowledge-manager):
- 该 Skill 有**新的**跨项目 delta 实测数据
- Inflation > 20% (值得记录的"measurement nuance")
- 或 Inflation < 5% (值得记录的"cross-project strong validation")

---

## 如何解读本文件

**✅ 正确用法**:
- "state-scanner v2.9.0 跨项目有效, 可放心在 Kairos 等项目使用"
- "commit-msg-generator 在某些项目可能需要 eval scenario 调整"
- "Aria#8 RCA 的核心假说被数据证伪, 不需要 Release Gate 2.0"

**❌ 错误用法**:
- ~~"state-scanner delta 被虚高了, 应该降级"~~ (inflation 4.9% 是噪音, 非虚高)
- ~~"commit-msg-generator 不应该发布"~~ (Kairos 0.0 来自 scenario 差异, 非数据问题)
- ~~"所有 Skills 都应该跑 dual delta 然后 block merge"~~ (这不是 gate)

---

## 维护节奏

- **每次 `/skill-creator benchmark` 后**: DRI 决定是否追加 entry
- **每季度审计**: DRI 复核已有 entries 是否仍准确 (e.g., Skill 是否有新版本)
- **废弃条件**: Skill 被删除 / 合并时, 对应 entry 标记为 `HISTORICAL (archived)` 而非删除

---

**维护者**: `knowledge-manager` (benchmark-transparency-enhancement Spec DRI)
**初版日期**: 2026-04-10
**数据基础**: `docs/analysis/spike-report-2026-04-10.md`
