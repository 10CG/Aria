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

**[2026-07-19 — 主 spec state-scanner-stale-refs-false-parity 四段式核心 SHIPPED v1.60.0](./2026-07-19-mainspec-false-parity-core-ship-v1.60.0.md)**

- track-id: `state-scanner-stale-refs-false-parity` | phase: **C-shipped-D-partial** | status: **active**
- 主 spec 四段式核心全实施 + ship **v1.60.0** (Phase 1 F1′-F6′/9.7 + Phase 2A F10″ gitlink [R5-C-A 事故解药]
  + Phase 2B F9′ sync + Phase 3 golden/12.10); 6 agent-team 动态工作流 + 主 loop 亲验 (抓修 gitlink ok
  BLOCKER false-green); 全套件 1219 绿 + dogfood 验证; aria `e162f7b` / 主仓 `d319d6f` 双远程 parity ✓
- ⚠️ **行为变更 13.6**: overall_parity 事故形态 true→false; Fetch1 --prune
- 🔴 **spec 保持 active (未归档)**: 79/119 done, k_eff DEFERRED, **29 TODO** (F5′ 6.1/6.2 接 overall_parity /
  非交互 git 3.4 / tracks 2.12 / 命名空间 1.6) — 下一步见本 handoff §6; owner 门: M6/M7/#165
- 前序: [Phase 0 v1.59.0](./2026-07-17-mainspec-phase0-v1.59.0-ship.md) / [specC-ship](./2026-07-16-specC-ship-falseparity-signoff.md)
