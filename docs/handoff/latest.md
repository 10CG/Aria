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

**[2026-07-17 — 主 spec Phase 0 (prereq) 独立 ship v1.59.0 + 镜像修复 + #165](./2026-07-17-mainspec-phase0-v1.59.0-ship.md)**

- track-id: `state-scanner-stale-refs-false-parity` | phase: **D-phase0-shipped** | status: **done**
- 主 spec 第一个 sub-cycle (Phase 0 prereq) 独立 ship **v1.59.0** (B→C→D; F5′ INERT + sync_freshness
  键 + D16 表骨架 + 8 测试 / 1072 绿); 修 aria-orchestrator 镜像 + 开 Aria #165 + 追平 3 版 badge drift
- 🔴 **下一步 = 主 spec Phase 1 (core, 最高风险 F3′ remote_refresh collector, 专门 session)**;
  #165 建议并入 Phase 2 Track A (复用 F10″); owner 门 (M6 4 门 / 168h / #136 / #151)
- claim **yielded**; 四仓 parity ✓ (ls-remote 独立核验); ⚠️ clock_skew 20663s 容器时钟待查
- 前序: [specC-ship + 三 spec sign-off](./2026-07-16-specC-ship-falseparity-signoff.md) / [六 cycle marathon](./2026-07-15-session-close-six-cycle-marathon.md)
