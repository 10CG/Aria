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

**[2026-07-12 — state-scanner「陈旧 ref 假同步」缺陷: 发现 + Spec + post_spec R1-R4 + 拆 3 Spec](./2026-07-12-state-scanner-false-parity-spec-r4.md)**

- track-id: `state-scanner-stale-refs-false-parity` | phase: **A.1-postspec-R4** | status: **active**
- 发现并实证 state-scanner (十步循环统一入口) 报**假的「已同步」** —— 本 session 自身即受害者
  (开局报 parity=equal, 实际落后 origin/master 4 commit)
- 核心洞察: **新鲜度不能「测量」, 只能「获取」**
- Phase A.1 完成 + post_spec 4 轮 × 5 agent 对抗审计 (收敛单调, 待 R5)
- 拆 3 个 Spec: 主 Spec (L3 核心机制) + secret-leak (L2, Rule #7, 先落地) + issue-cache (L2, 正交)
- **下一步**: post_spec R5 → owner sign-off → A.2/A.3。落地顺序: Spec C → Spec B → 主 Spec
