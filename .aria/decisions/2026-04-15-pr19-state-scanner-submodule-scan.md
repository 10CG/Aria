# Decision Record — PR #19 state-scanner-submodule-issue-scan

> **Date**: 2026-04-15
> **Type**: Progress / Completion
> **Related Spec**: `openspec/archive/2026-04-15-state-scanner-submodule-issue-scan/` (Complete)
> **Related PR**: [aria-plugin#19](https://forgejo.10cg.pub/10CG/aria-plugin/pulls/19) (merged 8ec898a @ 11:35:04Z)
> **Related Issue**: [Aria#16 US-020 M0](https://forgejo.10cg.pub/10CG/Aria/issues/16) (side-work, not in M0 Core Path)

## 事件背景

2026-04-15 session 进行 M0 T5 (AD1-12 + AD-M0-1~7 收敛) 期间, 用户在状态扫描后追问 "aria-plugin 应该也有 issue, 为什么没查看到?"。追查发现 state-scanner Phase 1.13 显式不递归 `.gitmodules` 中的 submodule (原 Spec `state-scanner-issue-awareness` 2026-04-09 D6 "噪音控制"决策), 导致 Aria meta-repo 模式下漏报率 60% (5 open issues 中只扫到 2)。

漏报的 3 个 issue 全部与当前 M0 主线**直接相关**:
- aria-plugin#17 (audit-engine Drift Guard) — 2026-04-14 Agent Team 4 轮收敛评审漂移验证需求
- aria-plugin#18 (Token × Attention 估算) — M0 T4 Spike "52h 估实际 4.5h 节省 91.9%" 估算失效现象
- aria-orchestrator#1 (轻量化 Hermes) — T4 Spike Option C 已实质回答但未挂钩

## 决策

立新 Level 2 Spec `state-scanner-submodule-issue-scan`, 在 aria-plugin 中实现 `scan_submodules` opt-in 扩展, 默认 false 保持向后兼容。

## 执行流程

1. **Spec 起草** (proposal.md Level 2, D1-D12 初稿)
2. **aria-plugin 实现** (PR #19 created, commit 488e736)
3. **Aria 项目级 dogfooding** (config.json 开启 scan_submodules=true)
4. **本地实测** (4 repos 扫描, 5 issues 全部发现, 0% 漏报率)
5. **Forgejo Aria#16 评论同步** (M0 进度 + 次生发现报告)
6. **/skill-creator benchmark** (+41.7pp → 修正断言后 +50pp)
7. **PR #19 创建 + 合并前审计** (5-round multi-agent pre_merge challenge mode)

## 5 轮审计收敛轨迹

| Round | Agents | CRIT | IMP | MIN | Total | Outcome |
|---|---|---|---|---|---|---|
| R1 | 5 | 2 | 11 | 11 | **24** | FAIL → 22 fixes applied |
| R2 | 5 | 0 | 0 | 2 | **2** | PASS_WITH_WARNINGS → 2 doc fixes |
| R3 | 5 | 0 | 0 | 1 | **1** | PASS_WITH_WARNINGS → 1 doc fix |
| R4 | 5 | 0 | 0 | 0 | **0** | PASS (first clean) |
| R5 | 5 | 0 | 0 | 0 | **0** | **PASS — 稳定性确认 ✅ CONVERGED** |

**收敛条件满足**: Round 5 findings set identical to Round 4 findings set (both empty).

## Agent Team 配置

5 个 aria 项目 agents 参与全部 5 轮:
- **tech-lead** — 架构决策 / 跨服务影响 / 范围正确性
- **backend-architect** — Schema / API 契约 / 性能 / 数据流
- **qa-engineer** — 测试严谨度 / benchmark 方法论 / 风险评估
- **code-reviewer** — 两阶段 (Spec 合规 + 代码质量 / bash 可移植性)
- **knowledge-manager** — 版本一致性 / 文档对齐 / 引用完整性

## 修复的 22 个 findings 分类

**CRITICAL (2)** — backend-architect:
- C1 cache_schema_migration_gap — 新增 schema_version guard
- C2 per_repo_fetched_at_missing_in_write — writer/reader 对齐 per-repo 时间戳

**IMPORTANT (11)** — 跨所有 agent:
- I1 output_schema_key_rename_is_breaking (dual-write items + open_issues 别名)
- I2/I3 timeout 非 opt-in 副作用 + 不随 N 扩展 (D14 adaptive: false→12s, true→max(20,(N+1)×5))
- I4 submodule_path_with_spaces (bash 数组 + 带引号展开)
- I5 date_d_GNU_only (parse_iso8601_to_epoch POSIX wrapper)
- I6 cd_vs_gh_C (用 gh -C 代替 cd+gh)
- I7 benchmark_metadata_inconsistency (runs_per_configuration 3 → 1)
- I8 false_positive_assertion (mentions_4_repos → does_not_disclaim)
- I9 eval_coverage_gap_backward_compat (AC-9 tracking future work)
- I10 version-drift (RECOMMENDATION_RULES.md changelog)
- I11 schema-mismatch (§Output Schema top v1.0/v1.1 双视图)

**MINOR (9 applied, 2 accepted no-action)**:
- M2 now_ts_undefined / M3 failsoft inconsistency / M4 all_repos_json_undefined
- M5 D13 limit per-repo / M6 benchmark.md sign convention
- M7 rollback L1 shared-path caveat / M8 AC-5/6 live-data flagging
- M9 Parent/Sister Spec split / M10 CHANGELOG [1.16.0] entry
- M1/M11 accepted no-action (label_summary opacity + memory alignment positive confirm)

## 产物与版本

- **aria-plugin v1.16.0** (released 2026-04-15, MINOR SemVer bump)
- **Benchmark**: +50.0pp pass rate delta (old 50% → new 100%)
- **Audit records**: `.aria/audit-reports/pr19-submodule-scan/round-{1..5}/` (25 YAML + 5 AGGREGATE.md)
- **Archived Spec**: `openspec/archive/2026-04-15-state-scanner-submodule-issue-scan/`

## 对 M0 主线的影响

**非阻塞**: 本次工作是 M0 session 的**次生成果**, 不计入 M0 T1-T6 核心工时。M0 剩余关键路径保持不变 (T2 NFS + T3 Dockerfile + T6 Report)。但本次修复为 M0 过程本身提供了直接的方法论次生收益:

1. **Phase 1.13 覆盖提升**: 未来 session 不会再遗漏 aria-plugin / aria-orchestrator 的 issue
2. **Benchmark 流程验证**: 首次使用 /skill-creator benchmark 对 state-scanner 做 AB 对比, 并在修正假阳性断言后得到稳健 +50pp 数据
3. **Multi-agent audit 实战**: 首次完整执行 5-agent pre_merge challenge mode 审计 + 迭代至严格收敛, 为 audit-engine 未来实现提供范式样本
4. **元估算数据点**: 本次工作按旧体系估算约 6-8h, 实际执行 ~3.5h, 继续印证 Aria#18 Token×Attention 估算模型的必要性

## 后续 Follow-up

- [ ] 更新 `aria-plugin-benchmarks/ab-results/latest/state-scanner/` 指针到本次结果 (manual, 非阻塞)
- [ ] 考虑在未来 v1.17.x 补齐 AC-9 eval-backward-compat (低优先级)
- [ ] aria-orchestrator#1 Idea close (Spike 已回答, 本次未处理, 另立)
- [ ] 关注 sister Spec `state-scanner-mechanical-enforcement` 激活条件 (L1 探针告警 ≥ 2 次)

## 记录人

Claude Opus 4.6 (1M context) + 5 aria agent team (tech-lead / backend-architect / qa-engineer / code-reviewer / knowledge-manager)
