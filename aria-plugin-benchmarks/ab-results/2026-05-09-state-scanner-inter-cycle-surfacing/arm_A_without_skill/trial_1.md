# 项目当前进度 — Bench Project

## 项目状态摘要

**仓库:** `/tmp/state-scanner-bench-fixture` (git, branch `master`, 工作树 clean)

**最近提交:**
- `e40043e` Fix US-042 status placement
- `8166d41` Initial bench fixture

**关键状态信号 (来自 UPM 机读区块):**
- `current_phase: PhaseB`
- `current_cycle: Cycle3`
- `active_module: backend`
- 入口指针 → `docs/handoff/2026-05-09-bench-handoff.md`

**上次 Handoff (2026-05-09) 已记录:**
- 已交付: TX.0 `status_clean` + 启动 TX.1 schema doc
- 下次优先: P1 followups (auth + payment) 复核 + 继续 US-042

**Pending Followups 表 (UPM):**

| 优先级 | 事项 | Next Action |
|--------|------|-------------|
| P1 | Ship payment gateway integration (issue#42, sprint-3) | review |
| P1 | Hotfix auth race condition (incident#9, active) | deploy |
| P2 | Refactor user model (abc123) | none |
| P2 | Improve test isolation (issue#67) | scope |
| P3 | Doc update for new API | author |
| P3 | Cleanup deprecated endpoints (issue#88) | review |

**User Stories:**
- **US-042** Payment Gateway Integration — *In Progress*, gateway adapter 60%, 等 cancel flow QA
- **US-043** Refactor user model — *Pending*

**没有发现的内容:** 仓库下没有 `openspec/` 目录，`.aria/` 为空，所以本次回到项目无未归档 OpenSpec change 等收尾负担。

---

## 推荐的接下来优先级 (Top 3)

1. **P1 — Auth race condition hotfix (incident#9, Next Action: deploy).** 这是事故型 P1 且 next action 已是 `deploy`，意味着代码大概率就绪，只差走 Phase C/D 的发布流程。先把已完成的工作落地，避免阻塞其他人。
2. **P1 — Payment gateway integration / US-042 (Next Action: review).** Handoff 明确点名要继续，且实现已 60%，剩 cancel flow 等 QA。需要先 review 当前 60% 的产出，再继续推进剩余 40%。
3. **P2 — Improve test isolation (issue#67, Next Action: scope).** P1 deploy/review 等待外部反馈期间的并行项，且只需 "scope"，本周期就能产出 OpenSpec proposal。

US-043 (Refactor user model) 仍处 Pending，建议本 cycle 不启动，避免 WIP 过载。

---

## 建议的工作流 (十步循环)

我们目前在 **PhaseB / Cycle3 / backend module**，建议按以下顺序执行:

**第 1 步 — Phase A.0 状态对齐 (5 min)**
确认 UPM 的 `current_phase=PhaseB` 与实际是否一致：检查是否还有未合并分支或未归档变更。当前 working tree clean + master only，状态对齐。

**第 2 步 — 处理 Auth Hotfix (Next Action: deploy)**
- A.0 → 直接进入 **Phase C (集成)**: 因为 hotfix 通常已完成开发
- C.1 提交 → C.2 合并/推送 → D.1 在 UPM Pending Followups 表把 auth 行从 P1/active 移除或标记 done → D.2 归档
- 若实际尚未实现完毕，则回到 **B.2 执行验证 + B.3 测试**

**第 3 步 — 推进 US-042 Payment Gateway**
- A.1 检查是否有 OpenSpec proposal；若无则用 `/aria:spec-drafter` 起草 cancel flow 的 Level 2 proposal
- A.2 `/aria:task-planner` 拆任务 (剩余 40%)
- B.1 `/aria:branch-manager` 建分支 `feat/us-042-cancel-flow`
- B.2 实现 + B.3 跑测试
- 完成后走 C → D，并把 US-042 状态从 In Progress 推到 Done

**第 4 步 — Test isolation scoping (并行)**
仅做 A.1 spec-drafter 起草 proposal，不进入 B，等 P1 清完后再排期。

**第 5 步 — 收尾**
`/aria:phase-d-closer` 更新 UPM Pending Followups 表、写下一份 handoff 到 `docs/handoff/2026-05-10-*.md`，把入口指针指过去。

**建议立即执行的命令:**
```
/aria:phase-c-integrator      # 先把 auth hotfix 推上线
/aria:spec-drafter             # 紧接着起草 US-042 cancel flow 的 proposal
```

需要我直接开始第 1 步还是先确认其中某项的细节？
