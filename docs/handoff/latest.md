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

**[2026-07-17 — reconcile clock-skew #111 fix ship v1.59.1 (含诊断纠正)](./2026-07-17-reconcile-clock-skew-111-v1.59.1.md)**

- track-id: `reconcile-yielded-terminal-fix` | phase: **D-shipped** | status: **done**
- 修 aria-plugin #111 (Layer-L reconcile clock_skew 20663s 误报): 真因 = clock_skew 检测纳入
  stale 历史 candidate → 修为只算 fresh candidate; aria **v1.59.1** `19dad0b` / 主仓 `3e209d3`
- 🔴 **诊断纠正**: 初始 #111 诊断 (yielded→terminal) 被 TDD RED-前影响面 + 现有 golden 测试推翻
  (yielded=可恢复暂停, 是 active candidate); 现象对、修复层错。code-review PASS 0C/0I
- claim **done**; 四仓 parity ✓ (F10″ gitlink 全可达); ⚠️ clock_skew 不是时钟问题 (容器时钟准)
- 前序 (同 session): [Phase 0 ship v1.59.0](./2026-07-17-mainspec-phase0-v1.59.0-ship.md) / [specC-ship](./2026-07-16-specC-ship-falseparity-signoff.md)
