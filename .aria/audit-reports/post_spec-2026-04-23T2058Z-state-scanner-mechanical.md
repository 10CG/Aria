---
checkpoint: post_spec
timestamp: "2026-04-23T20:58Z"
spec: state-scanner-mechanical-enforcement
verdict: PASS_WITH_WARNINGS
converged: true
mode: convergence
round: 1
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer]
votes: 4_PASS_WITH_WARNINGS
recommendation: activate_with_revisions
---

# post_spec Audit — state-scanner-mechanical-enforcement

## 投票结果

| Agent | Verdict | Recommendation |
|---|---|---|
| tech-lead | PASS_WITH_WARNINGS | activate_with_revisions |
| backend-architect | PASS_WITH_WARNINGS | activate_with_revisions |
| qa-engineer | PASS_WITH_WARNINGS | activate_with_revisions |
| code-reviewer | PASS_WITH_WARNINGS | activate_with_revisions |

**收敛**: 4/4 一致 PASS_WITH_WARNINGS + activate_with_revisions (Round 1 即收敛，无需二轮)

## Critical Findings (B.2 前必须 revise)

### CF-1: Target Version 过期 (tech-lead + code-reviewer)
- Spec 写 "v1.16.0 或 v1.15.x patch"，实际 aria-plugin 已至 v1.16.4
- 影响: AD-SSME-5 "v1.17.0 起移除 opt-out" 时间表同步作废
- Revision: 激活时 Target Version 追到 v1.17.0+，AD-SSME-5 改为 "v1.18.0 起移除"

### CF-2: T7.1 diff 等价性缺机械标准 (qa-engineer)
- "diff 为空或仅时间戳差异" 是主观判断
- Revision: 新增 T7.0 "定义 JSON canonical normalizer (jq -S + float 精度 + null/absent 归并)" 作为 T7.1 前置

### CF-3: schema_version 命名冲突 (backend-architect)
- `state-snapshot.json` 顶层 schema_version 与 `issue_status.schema_version` 同名不同义
- Revision: 顶层重命名为 `snapshot_schema_version`，T4.1 schema 文档明示作用域边界

### CF-4: T4.3 AD-SSME-6 工时低估 (code-reviewer)
- 0.5h 自动 docstring → schema.md 不现实 (stdlib-only 无 pydantic，AST 解析 + markdown 渲染实际 2-4h)
- Revision 二选一:
  - (a) T4.3 扩至 3h，明确工具链选择
  - (b) 降级为手维 schema.md，AD-SSME-6 改为 "source-of-truth = schema.md，scan.py docstring 引用 schema.md 版本号"

## Important Findings (开工 1 周内评估)

- IF-1 工时 staleness: 46h 原基准对齐 v2.9，当前 v2.10 + scan_submodules 扩展，至少 +4h → 50h 含 buffer
- IF-2 跨 session partial-delivery gate 缺失: tasks.md 应在 T3 末尾插入 "可中断恢复" checkpoint
- IF-3 stdlib-only 边界: YAML/.aria/state-checks.yaml 解析、git porcelain 解析、Windows subprocess 信号处理需明文化 (接受最小依赖 vs 手搓正则)
- IF-4 超时预算无全局视图: Phase 1.11 (60s) + 1.12 (N×5s) + 1.13 (12-20s) 最坏 100s+，远超 1.2x 目标
- IF-5 Benchmark scenarios 未设计 (calibration 风险 per feedback_process_vs_content_skills)
- IF-6 "minimal fixture repo" 验收点无对应任务 (T8 只有 Kairos)
- IF-7 Activation Gate "告警 ≥2 次" 计数手段不清 (audit.log 无持久化计数器)
- IF-8 opt-out fallback 与 scan.py 存在时的共存交互未定义

## Minor Findings (不阻塞激活)

- 多处 "0h" 任务标注应改 "(归并)" 或删除
- SKILL.md v3.0.0 major bump vs plugin minor/patch 语义不对齐
- 后置动作 "观察 mechanical_mode=false 使用量" 无 telemetry 收集手段

## 激活决议

**本轮投票**: 4/4 activate_with_revisions → **Status: Draft → Approved (with revisions pending)**

**工程纪律**:
- Phase A.1 完成: 更新 Spec Status = Approved
- Phase A.1.5 (本次新增): 将 4 条 CF 写入 Spec 头部 "Revisions Required Pre-B.2" 章节
- Phase A.2 complete (tasks.md 保留原内容，revisions 作为 T0 前置加入)
- Phase A.3 Agent 分配: tech-lead (CF-1), qa-engineer (CF-2), backend-architect (CF-3), code-reviewer (CF-4)
- Phase B.1 可立即启动 (branch creation)
- Phase B.2 T1 骨架开工前需先解决 CF-1/CF-3 (T0 revisions)
