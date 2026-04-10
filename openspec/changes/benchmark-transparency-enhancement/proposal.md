# benchmark-transparency-enhancement — Dual Delta Reporting (非 gate)

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-04-10
> **Parent Issue**: [Aria#8](https://forgejo.10cg.pub/10CG/Aria/issues/8) (Phase 3 修正后 Spec, 替代原 3 个 Level 3 Spec 草案)
> **Source**: `docs/analysis/spike-report-2026-04-10.md` (spike 实测证伪原 RCA 量化假说)
> **Target Version**: aria-plugin v1.11.1 (patch release, 非 minor)
> **DRI**: knowledge-manager
> **Depends**: —
> **Blocks**: —

## Why

原 Aria#8 Phase 1-2 RCA 的量化结论 ("state-scanner v2.9 ~50% 虚高", "commit-msg-generator 100% 虚高") 被 2026-04-10 spike 实测**证伪**:

| Skill | 原 RCA 估算 inflation | **Spike 实测** |
|-------|----------------------|---------------|
| state-scanner v2.9.0 | ~50% | **4.9%** (噪音) |
| commit-msg-generator v2.0.1 | ~100% | **11.3%** |

**核心修正**: Aria 内部 benchmark 的 internal delta **基本准确**, 不需要"修正". Kairos 测出的 delta 差异源自 **eval scenario calibration** (不同项目测不同难度场景), 不是数据造假. Rule #6 不需要大改, Release Gate 2.0 不需要, Escape Valve 不需要.

**保留的有效发现**: `category` 字段对透明度有价值, `calc_dual_delta.py` 作为 reporting 工具有实用性, `/skill-creator` 是上游插件的约束依然正确.

本 Spec 将 spike prototype 产物制度化 (从 spike 升格为正式工具), 但**不改变任何发版门禁**. 范围从原计划的 3 个 Level 3 Spec (~7-10 cycles) 降级为 1 个 Level 2 Spec (~1-2 cycles).

## What

### 1. 定型 spike 产出的 calc_dual_delta.py

Spike 已产出可工作的 ~270 行 Python 工具, 本 Spec 只做**收尾硬化**:

- **路径**: 已在 `aria-plugin-benchmarks/tools/calc_dual_delta.py`
- **添加**: `__doc__` 使用示例 (已存在, 仅校对) + `--help` 显式支持 (检测 `--help`/`-h` 参数前缀打印 docstring 并 exit 0)
- **添加**: 缺失 category 时输出 stderr warning (`WARNING: unmapped assertion "<key>", defaulting to aria_convention`), 与 What §2 描述一致
- **添加**: 3-5 个 unit test 覆盖 (`tests/test_calc_dual_delta.py`):
  - 正常双维度计算
  - 空 evals / 空 grading
  - INSUFFICIENT_SAMPLE (cross-project assertion_count < 3)
  - 缺失 category (默认 aria_convention + warning 验证)
- **保留**: 现有 category_map_commit_msg.json / category_map_state_scanner.json 作为参考样本

### 2. `category` 字段 — 可选透明度层

在 `eval_metadata.json` 的 `assertions[]` 可添加 **optional** `category` 字段:

```json
{
  "text": "Output lists each submodule with tree_commit fields",
  "weight": 1.0,
  "category": "aria_convention"
}
```

**规则**:
- 完全 optional, 不加就是 unknown (工具默认视为 aria_convention + warning)
- 3 个 enum 值: `aria_convention` / `generic_capability` / `behavior_contract`
- **不**升级为 required (与原 Spec 3 截然不同)
- **不**影响 /skill-creator 的任何 benchmark 流程 (上游工具不读此字段)

### 3. 分类指南 (简化版)

创建 `aria-plugin-benchmarks/ASSERTION_CATEGORY_GUIDE.md` (约 60 行), 包含:
- 3 个 category 的简短定义
- 5 个正反例 (而非原 Spec 的 10 个分层)
- 歧义时默认 aria_convention 的保守规则
- **不包含** Devil's Advocate checklist (原 Spec 的过度工程)

### 4. AB_TEST_OPERATIONS.md 新增章节 "Dual Delta Reporting"

在现有 runbook 末尾新增一节 (~30 行):
- 介绍 calc_dual_delta.py 作为 **reporting 工具** (非 gate)
- 两步运行: `/skill-creator benchmark <skill>` → `python3 tools/calc_dual_delta.py <dir> <category_map>`
- 解读示例: inflation < 20% 表示 internal 可信, > 20% 提示应补 generic eval scenarios
- **明确声明**: 本工具不改变 Rule #6, 发版仍基于 /skill-creator 原流程

### 5. HISTORICAL_CAVEATS.md — 透明度补充 (非警告)

创建 `aria-plugin-benchmarks/HISTORICAL_CAVEATS.md`, 记录 spike 实测数据:

```markdown
> **Note**: This file is a TRANSPARENCY supplement, NOT a warning register.
> All Skills listed below have been validated via spike testing; entries
> document measurement nuance (internal vs cross-project), not quality problems.

## state-scanner v2.9.0
- Internal +0.818 | Cross-project +0.778 | Inflation 4.9%
- Verdict: VALIDATED (原发版决策 100% 合法)

## commit-msg-generator v2.0.1
- Internal +0.846 | Cross-project +0.75 | Inflation 11.3%
- Verdict: MOSTLY VALIDATED (11% 的虚高在可接受范围)
- Note: Kairos delta 0.0 源自 eval scenario calibration 差异, 非数据造假
```

**不**追溯修改 CHANGELOG 或 US-008 (它们的数据依然准确).

### 6. MEMORY 更新 (已提前完成)

`feedback_process_vs_content_skills.md` 已在本 session 预先更新, 记录 spike 实测修正. 本 Spec 仅追认这项修改.

## Why NOT (Non-Goals)

- ❌ **不改 Rule #6** — 数据基本准确, 门禁不需要重构
- ❌ **不做 Release Gate 2.0** — 初版立项根据失效
- ❌ **不做 Escape Valve for Process Skills** — 问题不存在 (state-scanner cross-project delta 是 +0.778, 无需豁免)
- ❌ **不把 `category` 升级为 required** — 保持 optional, 过度工程化风险
- ❌ **不做 Kairos CI 集成** — 未来可选 feature, 不阻塞本 Spec
- ❌ **不做 Top 5 Skills retrofit** — 留给各 Skill 下次修改时顺带
- ❌ **不修改 /skill-creator 上游插件** — wrapper pattern 约束依然有效
- ❌ **不做 schema v1→v2 migration** — 纯 additive 改动, 无需 migration
- ❌ **不追溯修改 CHANGELOG / US-008** — 历史数据依然准确

## Design Decisions

### D1: Level 2 vs Level 3
**选择**: Level 2 (Minimal, proposal-only, 无 tasks.md)
**替代**: Level 3 (原计划)
**理由**: Spike 证伪核心假说后, scope 大幅缩小. 仅 5 个小型交付物 + 无 breaking change + 无审计开销, Level 2 足够.

### D2: category 保持 optional
**选择**: Optional with no planned promotion — 若 R3 监控数据 (3 个月填写率) 显示高价值, 未来 Spec 可促进; 否则 indefinitely optional
**替代**: 原 Spec 计划 "3 MINOR 版本后升级 required"
**理由**: 升级 required 没有实际意义 — calc_dual_delta 已能处理缺失情况, Rule #6 不依赖 category, 强制填写只会增加 Skill 作者负担. R3 的填写率监控会决定未来是否值得 Promotion.

### D3: 工具保留为 prototype 品质 (不加 jsonschema 依赖)
**选择**: stdlib only, 不引入 jsonschema 依赖
**替代**: 原 Spec 2 计划 "jsonschema 库用于 schema 校验"
**理由**: 本 Spec 不引入 benchmark.schema.json v2, 没有 schema 需要校验. 保持 stdlib only = 零依赖安装成本.

### D4: 不做 wrapper script
**选择**: 用户手工两步运行 (/skill-creator + calc_dual_delta.py)
**替代**: 原 Spec 2 计划 `run_benchmark_wrapper.sh`
**理由**: 在 AB_TEST_OPERATIONS.md 两行文档说明两步编排足够. Shell wrapper 增加维护成本 + 上游 /skill-creator 如果变更会引入脆弱依赖.

### D5: 简化 GUIDE (5 例而非 10 分层例)
**选择**: 单层 5 例
**替代**: 原 Spec 1 计划 "Novice 5 + Advanced 5"
**理由**: category 已从"gate 关键"降级为"透明度辅助", 过度详细的 GUIDE 没有对应复杂度.

## Acceptance Criteria

### AC1: calc_dual_delta.py 定型
- [ ] 文件位于 `aria-plugin-benchmarks/tools/calc_dual_delta.py`
- [ ] 顶部 docstring 包含 usage 示例
- [ ] `python3 calc_dual_delta.py --help` 打印 docstring 并 exit 0
- [ ] Positional args 错误时打印用法到 stderr 并 exit 1
- [ ] 缺失 category_map 键时输出 stderr warning (`WARNING: unmapped assertion ...`)
- [ ] Python 3.9+ stdlib only
- [ ] 3-5 个 pytest unit test cases 在 `aria-plugin-benchmarks/tools/test_calc_dual_delta.py`
- [ ] Unit tests 可通过 `python3 -m pytest tools/test_calc_dual_delta.py`

### AC2: category_map 样本就位
- [ ] `aria-plugin-benchmarks/tools/category_map_commit_msg.json` 存在 (已交付)
- [ ] `aria-plugin-benchmarks/tools/category_map_state_scanner.json` 存在 (已交付)

### AC3: ASSERTION_CATEGORY_GUIDE.md 就位
- [ ] 新建 `aria-plugin-benchmarks/ASSERTION_CATEGORY_GUIDE.md`
- [ ] 包含 3 个 category 的简短定义
- [ ] 包含 5 个正反例
- [ ] 包含 "歧义默认 aria_convention" 规则
- [ ] 长度 ≤ 100 行

### AC4: AB_TEST_OPERATIONS.md 新增章节
- [ ] 末尾新增 "Dual Delta Reporting (Optional)" 章节
- [ ] 明确声明: 非 gate, 是 reporting
- [ ] 两步运行示例
- [ ] Inflation 解读指南

### AC5: HISTORICAL_CAVEATS.md 就位
- [ ] 新建 `aria-plugin-benchmarks/HISTORICAL_CAVEATS.md`
- [ ] state-scanner v2.9 entry (internal/cross-project/inflation)
- [ ] commit-msg-generator entry
- [ ] 透明度级别 (非警告级)
- [ ] 引用 `docs/analysis/spike-report-2026-04-10.md`

### AC6: MEMORY 追认
- [ ] `feedback_process_vs_content_skills.md` 已记录 spike 修正 (本 session 已完成)
- [ ] MEMORY.md 索引描述准确

### AC7: 版本号 patch release
- [ ] `aria/CHANGELOG.md` 新增 v1.11.1 条目 (patch release, 非 minor)
- [ ] plugin.json / marketplace.json / VERSION / README badge 同步到 v1.11.1
- [ ] CHANGELOG 注明这是 transparency enhancement, 无 breaking change
- [ ] **主 repo submodule 指针**: `git add aria` + 新 commit 引用 plugin v1.11.1 (Q3 已解决)

### AC8: Level 2 post_spec 审计通过
- [ ] 2-agent 并行审计 (tech-lead + knowledge-manager) 完成
- [ ] 审计结果记录在 openspec/changes/benchmark-transparency-enhancement/ (commit message 或 .aria/audit-reports/)
- [ ] 双方最终投票 PASS 或 PASS_WITH_WARNINGS (无 REVISE)

### AC9: 不破坏性保证 (代码 + 历史)
- [ ] **代码层**: `calc_dual_delta.py` 仅写 stdout, 不调用 `open(..., 'w')` 写任何 ab-results 路径 (可由 `grep -n "open.*'w'" tools/calc_dual_delta.py` 验证)
- [ ] **历史层**: `git log --all --diff-filter=M -- aria-plugin-benchmarks/ab-results/2026-04-09/` 显示无 spike 后的 modification commits
- [ ] state-scanner v2.9.0 的 CHANGELOG 条目和 US-008.md **不被修改** (本 Spec 的 commit 不包含这些文件)
- [ ] 归档的 OpenSpec (`openspec/archive/2026-04-09-state-scanner-*`) 不被修改

## Risks

### R1: calc_dual_delta.py 的 join 逻辑在新 Skill 格式上失败
- **缓解**: spike 已验证 3 种已知 eval_metadata 格式 + 2 种 grading 格式. 遇到第 4 种新格式时, 新增一个 extract_assertions 分支即可, 不影响其他 Skills
- **监控**: 每次运行工具对新 Skill 时, 遇到 0 matched assertions 时输出 warning 而非 silent fail

### R2: 用户误把工具当 gate
- **缓解**: AC4 章节明确声明 "Reporting, 非 gate"; HISTORICAL_CAVEATS 中写 "v2.9.0 VALIDATED" 明确信号
- **Fallback**: 若 3 个月内发现误用率高, 追加一行提醒到 AB_TEST_OPERATIONS 即可

### R3: category 字段长期不被填写 (废弃风险)
- **缓解**: category 是 opt-in 透明度增强, 不填写也不影响发版. 如果长期无人填写, 说明 category taxonomy 对 Aria 场景价值不大, 可在未来 Spec 中废弃此字段 (无破坏性成本)
- **监控**: 3 个月后审计 Top 10 Skills 的 category 填写率

## Rollback

**Level 1**: 删除 `tools/test_calc_dual_delta.py` + `ASSERTION_CATEGORY_GUIDE.md` + `HISTORICAL_CAVEATS.md`. 保留 spike 工具 (无害)
**Level 2**: 额外回退 AB_TEST_OPERATIONS.md 新章节和 CHANGELOG v1.11.1 条目
**Level 3**: 完全 revert, 包括 spike 工具本身 (不建议, 工具实际可用)

## Resolved Decisions (was Open Questions in draft)

- **Q1 → Decision**: GUIDE 5 例覆盖 = 2 state-scanner + 2 commit-msg-generator + 1 generic Conventional Commits
- **Q2 → Decision**: HISTORICAL_CAVEATS.md 仅记录 spike 实测的 2 个 Skills (state-scanner v2.9, commit-msg v2.0.1). 其他 Skills 留给未来 benchmark 运行时自然积累.
- **Q3 → Decision**: 是 — submodule 指针更新已纳入 AC7

## Meta-Lesson Reference (km_m5)

本 Spec 验证的 meta 教训 ("spike-first for data-driven hypotheses") 在 `docs/analysis/spike-report-2026-04-10.md` 末尾的 Meta 教训章节有完整记录. 本 Spec **不**追加到 standards/ 或 CLAUDE.md (避免 scope 扩张), 但 Spike 报告作为 archived analysis 永久可查. 未来类似问题的处理者应阅读 spike-report-2026-04-10.md 的 Meta 教训章节作为前置参考.

---

**Spec 作者**: `/aria:state-scanner` deep-dive session (2026-04-09 → 2026-04-10)
**审计状态**: 待 2-agent post_spec 审计
**预计 cycles**: 1-2 (大幅简化自原 3 Spec 方案)
