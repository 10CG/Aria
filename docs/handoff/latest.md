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

**[2026-07-14 — false-parity 轨接手: v7 (F10″ 重写 + D15-D17 代裁 + CE 结案) → R7 FAIL 3/3](./2026-07-14-false-parity-v7-r7-fail-d15-triple-hit.md)**

- track-id: `state-scanner-stale-refs-false-parity` | phase: **A.1-postspec-R7** | status: **active**
- simonfish 接手 bot 轨 (claim 带 linked_issue #110): CE 归因结案 (custom_checks 确是通道,
  条件=缓存缺失/mtime>30min, 通道 4→6, 根治=offline 旁路为主) + 3 待裁代裁 (DEC §3c D15-D17)
  + v7 `ed21aba` (§13 按 F10″ 重写 + AC-16/17 重述含反惯例 fixture + R6 7 Major 全折)
- **R7 三视角 FAIL 3/3** (去重 8C/12M): D15 三中弹 (split-brain / k-rotation 脱钩 / hard_cap
  放宽) + F10″ 定义域被真 git 证伪 (rc=129 / **no-prune 视图 = 第十次复发最强候选**)
- **下一步**: 按 R7 聚合报告折 v8 (两个非机械点: D15′ 双角色窗 + RC-8 升格, 建议 owner 过目)
  → R8。聚合: `.aria/audit-reports/post_spec-R7-2026-07-14-*-aggregated.md`
- 前序: [R5/R6 + F10″ 换原语](./2026-07-12-false-parity-r5-r6-f10-primitive-swap.md) (bot)
