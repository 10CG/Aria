# State Scanner Recommendation — Arm B (v1.17.7 + T5 fallback), Trial 2

## 当前进度概览

**Project**: `/tmp/state-scanner-bench-fixture`
**Phase / Cycle / Module**: PhaseB · Cycle3 · backend
**Git**: `master` @ `e40043e` ("Fix US-042 status placement"), clean working tree, no upstream configured
**OpenSpec**: 未配置 (无 changes / archive)
**Audit**: 无近期审计记录
**Requirements**: 2 个 User Story — US-042 (in_progress), US-043 (pending)

Snapshot 字段无 `upm.followups[]` / `upm.handoff_doc` / `priority_items[]` (PRE-G2/G3/G4 collectors)。按 T5 fallback 指引,我已直接 Read UPM 源文件以提取跨周期延续信息。

---

## T5 Fallback 提取结果

### 1. Handoff Pointer (regex `> .*Next session 入口.*\((.+\.md)\)`)

匹配命中 UPMv2-STATE 块内第 7 行:
```
> 🚪 Next session 入口: 见 [docs/handoff/2026-05-09-bench-handoff.md](docs/handoff/2026-05-09-bench-handoff.md)
```

**Handoff doc**: `docs/handoff/2026-05-09-bench-handoff.md` (上一会话出口/本会话入口)

### 2. Pending Followups (来自 UPM `## Pending Followups` 表)

| Priority | Item | Tracking | Next Action |
|---|---|---|---|
| P1 | Ship payment gateway integration | sprint-3 | review |
| P1 | Hotfix auth race condition | active (incident#9) | deploy |
| P2 | Refactor user model | backlog | none |
| P2 | Improve test isolation | backlog | scope |
| P3 | Doc update for new API | — | author |
| P3 | Cleanup deprecated endpoints | backlog | review |

共 6 项: 2× P1, 2× P2, 2× P3。

---

## 推荐下一步 (优先级排序)

### 第一优先: 阅读 handoff 文档对齐上下文

**Action**: Read `docs/handoff/2026-05-09-bench-handoff.md`

理由: 你"刚回到这个项目"。Handoff 是上一会话明确为本会话准备的入口,包含未结决策、blocker、下一步意图。**先读 handoff,再决定攻什么**,避免重复别人已经做过的判断。

### 第二优先: 处理 P1 followup (二选一)

读完 handoff 后,从两条 P1 中选一条立即推进:

1. **Hotfix auth race condition** (incident#9, action=deploy)
   - 信号最强: `tracking=active` + `next=deploy` 表明已实现待发布,属于"最后一公里"。
   - 风险维度: incident 级别,延迟即风险。
   - 推荐工作流: 直接进入 Phase C (集成) — `/aria:phase-c-integrator`,合并 + 部署。

2. **Ship payment gateway integration** (sprint-3, action=review)
   - `next=review` 表明实现已完成等代码审查。
   - 推荐工作流: `/aria:requesting-code-review` → 通过后进入 Phase C。

**建议顺序**: 先 hotfix (incident 优先于 feature ship),再 payment gateway。

### 第三优先: 与 in_progress US-042 对齐

US-042 status 是 `in_progress`,最近一次提交 (`e40043e`) 是 "Fix US-042 status placement",说明它仍是当前焦点。需要在 handoff 中确认: US-042 与 P1 followups 是否同一条工作流,或独立并行项。如独立,继续推进 US-042;如同一,合并处理。

---

## 不推荐的动作

- **不要起新 Spec / 开新任务** (US-043 pending): 在 P1 followup + US-042 in_progress 未结之前开新工作会拉长 WIP。
- **不要急于 Phase A 规划**: 现状是 Phase B 收尾 + 跨周期延续项,不是"该去哪"模糊期。
- **不需要 OpenSpec for hotfix**: Level 1 (简单修复) 可跳过 proposal。

---

## 工作流推荐

```
1. Read docs/handoff/2026-05-09-bench-handoff.md          (3 min, 对齐上下文)
2. /aria:phase-c-integrator  → P1 hotfix auth race        (优先级最高)
3. /aria:requesting-code-review → P1 payment gateway      (次优)
4. 回到 US-042 in_progress 推进                            (现有焦点)
5. P2/P3 followups 进 backlog,下个 cycle 再 scope
```

---

**T5 fallback 状态**: PASS (snapshot 缺字段 → AI 直接读 UPM 源文件 → 成功提取 handoff pointer + 6 条 followups → 跨周期延续信息浮现到推荐中,未因 collector 缺失而丢失)。
