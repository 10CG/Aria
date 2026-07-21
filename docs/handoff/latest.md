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

**[2026-07-21 — 会话收尾: 版本一致性债清理 + meta-repo tag 规范分流](./2026-07-21-version-consistency-cleanup-and-meta-repo-tag-convention.md)**

- track-id: `session-close-20260721-version-consistency-tag-convention` | phase: **session-close** | status: **done**
- 从一次 `/state-scanner` 起步: 扫出 aria v1.63.0 主仓 release-closeout 漏做 (3 红 check 同源) → 清掉, 顺势清完主仓一批**版本一致性债**
- 已完成: (1) v1.63.0 closeout 4 派生面同步 + CLAUDE.md 645→639 压预算 (2) VERSION 116→37 行按 §4.2 重写 (清 1.6.0/1.7.3 矛盾 + changelog dump + 校正子模块版本) (3) CLAUDE.md orchestrator SHA `f3848b2`→`86bb684` (4) **standards §4.3 tag 规则分流** (owner 选方案 B)
- ⚖️ **方法论增量**: §4.3 从「VERSION 必须与 tag 一致」一刀切 → 按判据「有无下游按本仓 git tag 拉取」分流 (分发型严格 / meta-repo VERSION-file-only) —— 消主仓「VERSION≠tag」**永久假 drift**。→ memory `feedback_perpetual_red_check_may_encode_stale_convention`
- ✅ **#165 观察期加正面证据**: standards 改动全程约束 1 (本地合并) + 约束 2 (ls-remote 核验 ×4 全 MATCH), 零 orphan gitlink —— 一次干净正向 dogfood
- 🔴 **下一步**: 凭据轮换 (**第五次未回**) / #165 观察期 / Rule #6 成文首次实战 / #169 #168 #116
- custom checks **8/8 绿** (起点 3 红全转绿); 三仓双远程一致 (主仓 `faebb3d`)

**[2026-07-21 — 会话收尾: Rule #6 判据成文 + #165 从基建收敛成两条规范](./2026-07-21-session-close-rule6-formalization-and-165-convergence.md)** (predecessor, 同容器同日前序)

- track-id: `session-close-20260720-0721-rule6-formalize-165-converge` | phase: **session-close** | status: **done**
- 承接上一份 session-close 之后的增量: Rule #6 判据 **从「按文件目录」改为「按内容是否影响 AI 行为」** (下沉 `standards/conventions/skill-benchmark-exemption.md`, 新增「AB 测不到的处方性内容」第三行) + **#165 从「配 push mirror」收敛成两条零基建规范** (方案 D 消除服务端合并 + 纪律层 ls-remote 核验)
- 🔴 本段核心教训: **我把「观察」直接滑成「行动建议」** —— 撞见 standards 漏推就说「该配 push mirror」, 而漏推是纪律类 (本地双推就能防), 不是 push mirror 的机制类 (服务端合并)。owner 一句「本地双推不就够了」纠正。→ memory `feedback_match_evidence_class_to_solution_class`
- 🔴 两条规范**都当场约束了我自己**: Rule #6 成文后 Phase 4 应照跑 (已补); 多远程约束 1 (禁 Forgejo 服务端合并) 正是本会话给 aria 子模块一直在做的
- ⚠️ 执行纪律衰减: cwd 混淆本会话第 3 次 / 反引号吃内容第 2 次 —— **均已有 memory 但仍在犯, 靠「记住」不够**
- **下一步**: 凭据轮换 (第四次未回) / #165 观察期 (下个跨子模块 ship 走约束 1) / Rule #6 成文的首次实战 / #169 #168 #116

> ⚠️ **并发轨 (本指针不代表全部)**: 同期 in-flight 轨 **仍未完成** —
> **[aria-plugin #113 Phase B 实施 + pre-merge review](./2026-07-20-issue113-phase-b-impl-premerge-review.md)**
> (track-id `aria-plugin-113-gate-result-yaml-20260719`, phase **B-complete**, status **active — Phase C 待续**,
> spec `state-scanner-gate-yaml-datasource` 未归档, claim 未释放, aria `13f9582` 未推送)。
> 本会话两次收尾均接管指针但保留标注该轨; **它跨了两次收尾仍 active, 不要因指针换了就当它结束**。
> 多 track 并发以看板 (`tracks_multibranch`) 为语义权威。

---

**[2026-07-20 — 会话收尾: aria-plugin #113 gate yaml 数据源 cycle, Phase A 完整收官](./2026-07-20-issue113-phase-a-yaml-datasource.md)**

- track-id: `aria-plugin-113-gate-result-yaml-20260719` | phase: **A-complete** | status: **active** (Phase B 待下 session)
- triage confirmed/major → **claim 先行** (上 session 血泪兑现) → A.1 Spec **post_spec R1→R5 CONVERGED** (owner 裁决延长 R5; R4 双实现者相反结果=规格欠定实证) → A.2/A.3 10 任务 path B → **post_planning R1→R2 CONVERGED** (规则 #10 照跑首战, R1 抓 6 Major 全属派生盲区) → owner sign-off (Approved)
- **下一步**: Phase B.1 直接开工 (claim 在手无需重 gate; 任务 DAG + 全部规格钉子就绪; ship target v1.63.0, bump 前 re-check SOT)
- 主仓 `2f4ada6`+handoff; aria 未动 (v1.62.0); 27 审计报告入库

---

> ⚠️ **2026-07-19 是双轨并发日** — 同日两个 session 在同一 repo 各自 ship 一个版本 (v1.60.0 / v1.61.0),
> 两篇 handoff **都要读**。本页按结束时间倒序并列; 语义权威仍以多 track 看板为准 (见页首说明)。

### 轨 A — Aria #166 OpenSpec 假绿三缺陷 (较晚结束)

**[2026-07-19 — 会话收尾: #166 triage → 完整十步循环 → ship v1.61.0](./2026-07-19-issue166-openspec-false-green-cycle-v1.61.0.md)**

- track-id: `issue166-openspec-false-green-20260717-0719` | phase: **session-close** | status: **done**
- 单 cycle 会话: `/state-scanner` 开局 → triage Aria #166 → A→B→C→D 一气走完 → ship aria-plugin **v1.61.0**
- 三缺陷: changes/ 缺失静默全零+不扫 archive (`layout_drift`) / gate_result 对 yaml-only spec 归档安全网失明 / `Completed`→unknown
- post_spec **R1→R4 CONVERGED** (R1 Critical: 缺陷2 位置钉错 —— 继承 issue 自身 mis-citation; R2 Major: surfacing 机制假设被源码证伪) + silent-failure-hunter 抓 fix-introduced regression
- 🔴 **最贵一课**: 开局 scan 已报 `self_multi_container` collision, 判为 benign 跳过 claim → 精确撞上轨 B (同 skill 同文件 + 抢注 v1.60.0), 被迫让位 v1.61.0 + rebase
- Spec 已归档; #166 closed; follow-up aria-plugin #113/#114 open
- ⚖️ **收尾后追加治理变更**: 新增**不可协商规则 #10**「已启用的审计检查点不得由 AI 自行豁免」(触发: 本 cycle AI 自行跳过 post_planning; owner 裁决照跑, 并否决「跟踪 AI 判断准确率再放权」方案)

### 轨 B — 主 spec false-parity marathon (并发, 抢注 v1.60.0)

**[2026-07-19 — 会话收尾: 主 spec false-parity marathon (README 修 → Phase 0→1→2/3 → ship v1.60.0)](./2026-07-19-session-close-mainspec-marathon.md)**

- track-id: `session-close-20260717-0719-mainspec-marathon` | phase: **session-close** | status: **done**
- 会话总账 (2026-07-17→07-19): 5 个 `/goal` 把主 spec `state-scanner-stale-refs-false-parity` 四段式**从零推到
  ship v1.60.0** (F1′-F10″ false-parity 根治 + R5-C-A gitlink 事故解药); 6 agent-team 动态工作流 + 主 loop 亲验
  (抓修 gitlink ok BLOCKER false-green); 全套件 1219 绿 + dogfood; 三仓×双远程 parity ✓
- ⚠️ **行为变更 13.6**: overall_parity 事故形态 true→false; Fetch1 --prune
- 🔴 **主 spec 仍 active (未归档)**: 79/119 done, k_eff DEFERRED, **29 TODO** — 下个专门 session 收口实质 TODO 后归档
- 本 session cycle handoff: [主 spec 核心 ship v1.60.0](./2026-07-19-mainspec-false-parity-core-ship-v1.60.0.md) |
  前序: [Phase 0 v1.59.0](./2026-07-17-mainspec-phase0-v1.59.0-ship.md) / [specC-ship](./2026-07-16-specC-ship-falseparity-signoff.md)
