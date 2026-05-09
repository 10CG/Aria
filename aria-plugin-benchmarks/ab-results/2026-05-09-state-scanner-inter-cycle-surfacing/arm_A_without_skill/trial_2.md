# Bench Project — 当前进度与下一步建议

欢迎回来。我扫了项目根目录下的关键文件 (UPM、handoff、user stories、git 状态) ，下面是我整理的状态和建议。

## 项目状态摘要

**Git**: 在 `master` 分支，工作树干净，最近 2 次提交：
- `e40043e` Fix US-042 status placement
- `8166d41` Initial bench fixture

**UPM 当前状态** (`docs/project-planning/unified-progress-management.md`):
- Phase: PhaseB / Cycle3
- Active module: backend
- 入口指针: `docs/handoff/2026-05-09-bench-handoff.md`

**上一会话交接** (handoff 文档):
- 已交付: TX.0 status_clean，启动 TX.1 schema doc
- 下次优先级: P1 followups 审阅 (auth + payment)、继续 US-042

**Pending Followups (UPM 表格)**:

| 优先级 | 事项 | 状态 |
|---|---|---|
| P1 | Ship payment gateway integration (issue#42) | review |
| P1 | Hotfix auth race condition (incident#9) | deploy |
| P2 | Refactor user model (US-043) | backlog |
| P2 | Improve test isolation (issue#67) | scope |
| P3 | Doc update for new API | author |
| P3 | Cleanup deprecated endpoints | review |

**User Stories**:
- US-042 Payment Gateway: **In Progress** — gateway adapter 60% 完成，待 QA 审 cancel flow
- US-043 Refactor user model: Pending (映射到 P2 followup)

## Top 优先级 (推荐顺序)

1. **P1 — Auth race condition hotfix (incident#9)**：incident 标记为 `deploy`，最快路径，建议先收尾。生产风险类项优先级最高。
2. **P1 — Payment gateway / US-042**：两条线索同源 (issue#42 + US-042)。当前 60%，blocker 是 cancel flow QA。建议要么推进 QA、要么把 adapter 剩 40% 闭环。
3. **P2 followups**：等 P1 清掉再排，US-043 (user model refactor) 与 issue#67 (test isolation) 都在 backlog/scope 阶段，需要先写 Spec。

## 建议工作流 (十步循环)

考虑到当前在 PhaseB/Cycle3 中段，且有 P1 deploy-ready 项，建议：

**路径 A — 优先收尾 P1 (推荐)**:
1. **A.0 状态确认**：确认 auth hotfix 是否真已 deploy-ready (查 issue#9 / branch / PR)
2. **B.2 → C.1 → C.2**：如果代码已就绪，直接补测试、提交、合并；如果需要小改动，走完整 B 阶段
3. **D.1 进度更新**：把 hotfix 状态从 `deploy` 改为 done，更新 UPM
4. 然后切 US-042：联系 QA 推进 cancel flow，或继续 adapter 剩余 40%

**路径 B — 继续 US-042**:
若 auth hotfix 实际还需较多工作 (与 handoff "review" 提示不一致)，则保持当前 active_module=backend，继续 PhaseB.2 开发循环。

## 我需要你确认

- 上一会话停在哪一步？handoff 说"启动 TX.1 schema doc"——这块是否已经有未提交分支或 WIP？(目前 master 干净，未见 WIP 分支)
- Auth hotfix 的 `deploy` 状态是"待部署"还是"已部署待验证"？这决定下一步是 Phase C 还是 Phase D。
- 是否要我先创建 OpenSpec proposal (Level 2/3) 给 P1 项，再走十步循环？

确认这两点后，我建议从 **auth hotfix 收尾** 开始。
