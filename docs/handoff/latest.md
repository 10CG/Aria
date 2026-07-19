# Aria Handoff — Latest

> 此文件指向最近一次 session handoff。Aria 项目内部约定:
> 始终 Read 本文件作为 next session 入口,内容指向具体的日期版 handoff。
> 自 v1.21.0 起 (H0 spec ship), `/aria:state-scanner` Phase 1.15 collector
> 会自动 surface 本 pointer + handoff doc 路径,AI 在阶段 2 推荐前必读。
>
> **自 v1.22.0 起** (multi-terminal-coordination ship,本日 2026-05-20 master `b0c9c3a`):
> state-scanner Phase 1.16 + 1.17 跨分支重建多 track 看板 — 当多 track 并发时,
> 看板才是语义权威;本 latest.md 单指针保留向后兼容,但**多 track 场景请用看板**。

---

## 最新 handoff

**[2026-07-19 — 会话收尾: 主 spec false-parity marathon (README 修 → Phase 0→1→2/3 → ship v1.60.0)](./2026-07-19-session-close-mainspec-marathon.md)**

- track-id: `session-close-20260717-0719-mainspec-marathon` | phase: **session-close** | status: **done**
- 会话总账 (2026-07-17→07-19): 5 个 `/goal` 把主 spec `state-scanner-stale-refs-false-parity` 四段式**从零推到
  ship v1.60.0** (F1′-F10″ false-parity 根治 + R5-C-A gitlink 事故解药); 6 agent-team 动态工作流 + 主 loop 亲验
  (抓修 gitlink ok BLOCKER false-green); 全套件 1219 绿 + dogfood; 三仓×双远程 parity ✓
- ⚠️ **行为变更 13.6**: overall_parity 事故形态 true→false; Fetch1 --prune
- 🔴 **主 spec 仍 active (未归档)**: 79/119 done, k_eff DEFERRED, **29 TODO** — 下个专门 session 收口实质 TODO 后归档
- 本 session cycle handoff: [主 spec 核心 ship v1.60.0](./2026-07-19-mainspec-false-parity-core-ship-v1.60.0.md) |
  前序: [Phase 0 v1.59.0](./2026-07-17-mainspec-phase0-v1.59.0-ship.md) / [specC-ship](./2026-07-16-specC-ship-falseparity-signoff.md)
