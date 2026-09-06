# Aria #174 留言草案 (TASK-040 / tasks.md 0.2) — 待 owner 授权后发帖

> 目标 issue: Forgejo 10CG/Aria#174 (a1-entry-claim-duplicate-work-guard 轨)
> 发帖人: aria-runner-bot (容器 bfe8285d) | 状态: **草案, 未发**
> 关联 Spec: `openspec/changes/owner-container-identity-key-and-collision-parser/` (Level 3, Approved 2026-09-05; post_planning 9 轮 CONVERGED 2026-09-06)

---

## 正文 (发帖时逐字使用)

来自并行轨 **owner-container-identity-key-and-collision-parser** (Aria #193 + aria-plugin#135 缺口 3) 的一条通知 + 一条征求 ack, 都与本轨 `lib/identity.py` 有耦合, 先说结论: **本轨 S1 形态 ship 不动 a1-entry 的任何契约与文本**。

### 1. 通知: D-0(a) 裁定 — Layer H 侧纯形状剥离

owner 裁定 (2026-09-05, 决策单 `.aria/decisions/2026-09-05-owner-container-identity-key-rulings.md` D-0 选 a): Layer H (handoff frontmatter) 的 `<owner>/<container-id>` 解析改为两段式 + `identity_key`, 族键剥离 (`-[0-9a-f]{8}$`) **只在** `track_to_claim_record` 内做, 不触碰 a1-entry 的 claim 契约、`get_container_uuid()` 与 SC-3。本轨新增 `get_container_label()` 只读 accessor, **不 flip** `get_container_id()` 的 label 优先语义。

### 2. 征求 ack: S2 条件下需改写贵轨 SC-3 的判据草案

本轨有一个**条件分支 S2** (激活条件三项同时成立: a1-entry B.2 进 master + 本条 ack + 本轨尚未 merge), 才会 flip `get_container_id()` 为 uuid 优先。flip 后贵轨 SC-3 现文「`get_container_id()` label 优先 ⇒ 直接调它必红」的前提消失, 需改写为:

> `get_container_uuid()` 与 flip 后 `get_container_id()` 同值; label 只经 `get_container_label()` 取得。

请求: 对上述改写措辞给一个 ack / 修改意见。**未取得 ack 本轨不动贵轨任何文本**; 今日 (2026-09-06) 实读 a1-entry 分支 `ab3dbd0` 未进 master, 本轨已判 **S1** ship, S2 后续将在本轨 merge 后、归档前由 tracker issue 承载 (tasks.md 5.8), 届时再回到这条线程。

### 3. 行号漂移

两轨都碰 `lib/identity.py`; 后落地方在 D 期 refresh 对方 proposal 里引用的行号 (本轨 proposal :104 已约定)。

---

*来源: `/openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md` :104 (两种 ship 形态) / tasks.md 0.2 · S2 后续表 S2-3*
