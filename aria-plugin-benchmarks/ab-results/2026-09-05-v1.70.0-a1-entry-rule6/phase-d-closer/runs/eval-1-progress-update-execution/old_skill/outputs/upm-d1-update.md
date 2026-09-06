# D.1 进度更新产物 — spec `oauth2-social-login` (PR #143)

> 本文件是 Phase D D.1 应写入 UPM 文档 (`{module}/docs/project-planning/unified-progress-management.md`)
> 的内容。因 AB 评测隔离约束, 未写入仓内 UPM 路径, 改落本目录。
> 模式: single-pass (`.aria/config.json` 无 `upm.milestone_driven` → 默认 false)

## 1. UPMv2-STATE 机读区块 (5 字段更新)

```yaml
# <!-- UPMv2-STATE:BEGIN -->
cycleNumber: <N> → <N+1>            # 本 cycle 随 PR #143 合并收束, cycle 计数 +1
lastUpdateAt: 2026-09-05T00:00:00Z  # D.1 执行时刻 (UTC)
stateToken: <recompute>             # 按 UPM 规范对归一化后的 STATE 区块重算, 不得沿用旧值
completedTasks:                     # 追加本 cycle 6 项 (ID 以 tasks.md 实际编号为准)
  - TASK-001
  - TASK-002
  - TASK-003
  - TASK-004
  - TASK-005
  - TASK-006
kpiSnapshot:
  specsCompleted: +1                # oauth2-social-login
  tasksCompleted: +6
  prsMerged: +1                     # PR #143
  coverage: <本 cycle 测试覆盖率>    # 有 CI 覆盖率产出时回填, 否则保持上轮值并注明 stale
# <!-- UPMv2-STATE:END -->
```

## 2. 人读 Story 记录 (single-pass 完整更新)

```markdown
- [x] COMPLETED — OAuth2 Social Login (spec: oauth2-social-login)
  - status: completed / merged
  - pr: #143 (merged to main)
  - tasks: 6/6 完成 (TASK-001 ~ TASK-006 全部 [x])
  - completedAt: 2026-09-05
  - archive: openspec/archive/oauth2-social-login/   # ← 待 D.2 归档完成后回填, D.1 阶段可留 TODO
```

## 3. 校验清单

- [x] spec 状态 = completed / merged (不再是 in-progress)
- [x] PR 号 #143 记入进度记录 (Story 行 + kpiSnapshot.prsMerged)
- [x] 6 个任务全部标记完成, 且计入 completedTasks
- [x] lastUpdateAt / cycleNumber / stateToken 同批更新 (stateToken 必须重算)
- [ ] archive 路径回填 (依赖 D.2, 本次未执行)
