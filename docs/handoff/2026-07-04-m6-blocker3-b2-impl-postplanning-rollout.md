---
track-id: m6-blocker3-b2-impl-postplanning-rollout
owner-container: simonfish/f9c6e8cd
phase: B
status: in_progress
updated-at: 2026-07-04T10:49:05Z
---

# Aria — Session Handoff (2026-07-04) — M6 Blocker 3 Phase B.2 完整实现 (agent-team workflow) + post_planning rollout + 并发和解

## §0 入口 (新 session 优先读)

本 session 一路做到 **M6 Blocker 3 (`aria-2.0-m6-dispatch-input-delivery`) 的 Phase B.2 完整实现**:A.3 收敛 → dogfood mid_post_spec → **启用 post_planning 检查点 (rollout)** → 与并发容器 A.3 碰撞 → owner 移交全权用我方 30-task 版 → **完整 post_planning 5-agent 审计 (R1→R2 CONVERGED)** → **agent-team 动态 workflow 实现 B.2 (26/30 task, 1239 测试绿)** → **pre-merge code-review (3 审员)** → **修掉 1 Critical**。

> **🟢 B.2 可实现部分 100% 落地并审过**;卡在 **4 个 owner/infra 门** (build/deploy/egress/E2E),其中 **AC-1 E2E dogfood 受 Blocker 4 (Luxeno 延迟)**。清门前不能进 Phase C.2 合并。

**代码位置**:aria-orchestrator `feature/m6-dispatch-input-delivery @ 1ee225a` (B.2 + Critical 修 + pre-merge review follow-ups),**WIP 未 merge**,主仓 submodule 指针仍 `daf7c79`。主仓 master 有 doc-sync + CLAUDE.md 项目状态 (`1ec600f`)。

**Next**:owner 清 4 门 (⭐ 尤其 Blocker 4 Luxeno) → Phase C (PR+pre-merge gate+bump 指针) → Phase D 归档。**AI-side pre-merge code-review + follow-ups 已全部完成** (§1 item 12);分支 merge-ready,残留仅少数非阻塞 Minor (§2)。

## §1 已完成 (按时间顺序)

1. `/state-scanner` + **reconcile 三仓双远程** → 核实**双子星 (并发容器) 昨天已把 CLAUDE.md 瘦身/立卫生规矩 (claude-md-hygiene Option A)**,本地已含,byte-identical。
2. **推 Blocker 3 → Phase A.3**:task-planner 产出 `detailed-tasks.yaml` (30 task, 1:1 对 tasks.md, verification↔AC + agent 分配 21/4/5)。
3. **dogfood `mid_post_spec`** (方向 A rollout 验证):2-agent 抓 2 drift (我 A.3 草稿 TASK-016 FailReason 误路径 `audit/interfaces.py` + tasks.md 1.8 "dies at :37" 措辞掩盖 `\|\| true` 真路径),已修。
4. **启用 `post_planning` 检查点** — **rollout amendment [DEC-20260704-001]**(延续 DEC-20260519-001 分步 rollout)+ `.aria/config.json` `post_planning: off→convergence` + `teams.post_planning`。
5. **并发碰撞**:提交 A.3 时发现并发容器 (simonfishgit) 对**同一 Spec** 也做了 A.3 (20-task `7ce3cee` 已落 remote)。先按最不破坏原则保留他们的 + 落我两独立赢面。
6. **owner 移交全权**:双子星停止本任务 → **采用我方 30-task 细粒度版 supersede 20-task** (`5f7a001`);删对比 backup 分支。
7. **完整 `post_planning` 官方 gate** (首次,亦观察窗二次 dogfood):**5-agent convergence, R1 (4 REVISE/1 PASS, 6 Major+minors) → 16 处任务清单订正 → R2 (5 PASS) → CONVERGED** (`fa19b91`)。比 2-agent dogfood 多抓 6 Major (依赖漏边/schema_migrate 静默跳过/corpus 防线缺测/single-carrier 歧义/DEC self-correction 落空/协调对象指错)。审计报告 `.aria/audit-reports/post_planning-R2-CONVERGED-*.md`。
8. **Phase B.1**:aria-orchestrator 建 `feature/m6-dispatch-input-delivery` (from master daf7c79)。
9. **Phase B.2 — agent-team 动态 workflow** (7 agent, 文件域分 track 防并行写冲突):容器 TG-1 ‖ Layer1 TG-2 ‖ DocSync TG-5 并行 → barrier (016+017) → TG-3 keymig ‖ TG-4/6 gated prep → verify。容器 track 因 API 断线**仅返回报告失败, 工作完整**。**验证: 1239 tests passed / 0 regression** (Layer1 940 + 容器 89 断言含 initial-sh-integration 真 call-site)。marker 跨-track 契约 byte-match。B.2 批次 `a3a4e2d` (36 files, +3879)。
10. **Pre-merge code-review** (3 审员, code-grounded + 实跑): Phase1 PASS / Phase2 PASS_WITH_WARNINGS, **1 Critical + 2 Important + minors**。对抗性确认干净 (secret 卫生/无 SQL 注入/fail-closed 穷尽/pyright 非本 PR 引入)。
11. **修 Critical #1** (`ef61f55`):render invariant 在 rendered output 上 grep `$ARIA_` → fetch 到的不可信 body 含字面 `$ARIA_` 误触发 die → 误判 CONTAINER_CRASH → 破 AC-1。修法 = invariant 改查 **TEMPLATE (envsubst 前)** 非 rendered output + scenario 5 复现。integration 5/5 绿。
12. **AI-side pre-merge review follow-ups 全部完成**:(a) 补 `initial-sh-unit/test.sh` (`a908d10`, **23/23** — 消灭幽灵引用 + 闭合 AC-2/3/6/7 unit gap: is_valid_issue_id / classify_http_result / fetch retry 退避-耗尽+retriable-then-OK / sanitize / resolve_base_branch);(b) 清 TASK-015 重言式断言 + image-freeze §6 deploy-order「镜像先」note (`1ee225a`);(c) 4 memory 沉淀写入 + MEMORY.md 压缩 24.7→9.99KB;(d) CLAUDE.md 项目状态段更新 (主仓 `1ec600f`)。**分支 merge-ready** (残留仅少数非阻塞 Minor)。

## §2 未完成 / Carry-forward 清单

### 高优先级 (owner/infra 门 — 阻 Phase C.2 合并)
1. **TASK-021 镜像 build** — `aether-build-container` 是 **owner-triggered** 原语,AI 跑不了。build-readiness 已验,命令已文档化 (`aria-orchestrator/docs/m6-dispatch-input-delivery-image-freeze.md`)。
2. **TASK-022 真 IMAGE_SHA** — 依赖 021,freeze/rollback 表模板已建。
3. **TASK-028 heavy-node egress live-test** — 需 Aether 集群,探针脚本已就绪 (`...task028-egress-probe.md`)。
4. **⭐ TASK-029 E2E dogfood (AC-1 门)** — 受 **Blocker 4 (Luxeno 45-54s 延迟)** + 全栈部署,dogfood plan 已文档化 (`...task029-e2e-dogfood-plan.md`)。**这是真正闭环 M6 的命门,Blocker 4 是 owner/基建活。**

### 中优先级 (code-review deferred) — ✅ AI 已完成 2026-07-04 (feature `1ee225a`)
- ✅ **[Important] AC-3 retriable 测试 + `initial-sh-unit` 幽灵引用** → 补齐 `initial-sh-unit/test.sh` (`a908d10`, 23/23): AC-2 reject / AC-3 classify 矩阵 + retry 退避-耗尽+retriable-then-OK / AC-6 base_branch fallback / AC-7 sanitize。消灭 `initial.sh:78,311` 的幽灵引用。
- ✅ **[Important] 部署顺序耦合** → image-freeze doc §6 deploy-order note「镜像先、Layer1 后」+ 前置探针建议 (`1ee225a`)。
- ✅ **[Minor] TASK-015 重言式测试** → 删 f-string-vs-字面 断言, 保留 2 条真断言 + 注明真覆盖在 test_t_pr_timing.py (`1ee225a`)。
- ✅ **[Minor] AC-7 sanitize** → 随 initial-sh-unit 覆盖 (CRLF→LF + 超限截断标记)。
- ⏳ **残留 Minor (仍 deferred, 非阻塞)**:UTF-8 截断切多字节字 / base_branch fallback (unit 覆盖但非 integration) / migration 008 命中通用 backfill (预存模式) / exit0 双 get_alloc_logs (效率) / `<repo>` 分量取全局 env (单-repo 正确, 多-repo latent)。

### 流程记账
- **`detailed-tasks.yaml` 30 task 仍全标 `status: pending`** — 与已实现代码不符。Phase D progress-updater 时更新。

## §3 关键风险 / 已知陷阱
- **Blocker 4 (Luxeno 单点)**:AC-1 dogfood 的真门,owner/基建/SilkNode 侧 (#147 / SilkNode #830)。别优化 mihomo (前 session 实测无效)。
- **并发容器碰撞** (本 session 亲历):file-level 无硬冲突但 **feature-level 撞** (双容器同做 A.3)。双子星已就此起 **#94/#95/DEC-20260704-002 (Layer L 接活改造防重复)**。教训 memory `feedback_concurrent_feature_collision_claim_before_build`。**下次同 Spec Phase B 前先 claim/coordinate。**
- **submodule 指针纪律**:aria-orchestrator 在 feature 分支 (未 merge),主仓指针**故意保持 daf7c79**。Phase C 才 bump。别误 bump。
- **多远程 parity 竞态**:本 session push 被并发拒 3 次,每次 fetch+rebase 解 (无冲突)。双子星活跃, push 前必 fetch。

## §4 实战教训 (memory 沉淀来源)
- **post_planning 抓 A.2/A.3 派生盲区**:同一 A.3 产物,2-agent dogfood 抓 2, 完整 5-agent convergence 多抓 6 Major —— A.2/A.3 派生产物是审计盲区,proportional-但-别过省。(印证 DEC-20260704-001)
- **agent 断线 ≠ 工作丢失**:容器 track "failed" 只是返回报告失败,工作完整 (语法/测试/契约全验)。诊断 workflow 失败先查工作树实际状态 + verify agent 结果,别只看 failure flag。
- **pre-merge code-review 抓真 Critical**:6 并行 agent 的 TDD+verify 全绿,仍有 1 reproduced Critical ($ARIA_ token 误触发 render invariant)。**测试绿 ≠ 无 bug**;独立 adversarial review 不可省。
- **render invariant 该查 source 非 output**:校验「模板变量是否遗漏展开」要查**模板本身** (envsubst 前),查 rendered output 会把用户数据里的字面 sigil 误判。(通用:validate at the source, not the mixed output)

## §5 多维度同步状态 (Aria 4 维度)
- **代码/git**:aria-orchestrator `feature/m6-dispatch-input-delivery @ ef61f55` (push origin, WIP 未 merge)。主仓 master (见 §7, 双远程 parity)。**submodule 指针 daf7c79 未动**。
- **文档**:主仓 CLAUDE.md M6 状态 + DEC-20260702-001 勘误 + tasks.md §3.2 决策 + DEC-20260704-001 (rollout);aria-orchestrator AD-M6-10 + AD-M1-4 amend + layer-boundary §5 (在 feature 分支)。
- **决策**:**DEC-20260704-001** (post_planning rollout);消费 DEC-20260702-001 (Blocker 3 架构)。
- **配置**:`.aria/config.json` `post_planning: convergence` 启用 (首个官方 gate 已跑通)。
- **审计**:post_spec CONVERGED + **post_planning R1→R2 CONVERGED** + pre-merge code-review (1 Crit fixed)。
- **运行时**:无部署变更 (镜像未 build, Layer1 未 deploy — 都是 owner 门)。

## §6 Next session 入口 + 优先级建议
1. **⭐ 清 4 个 owner/infra 门** (真闭环命门):Blocker 4 (Luxeno) → build (021) → deploy → egress (028) → E2E dogfood (029, AC-1)。E2E 绿才进 Phase C.2。
2. **AI-side 可先做** (非阻塞, 提升 merge 就绪度):补 AC-3 retriable 测试 + 写 `initial-sh-unit/test.sh` (消灭幽灵引用) + 清 TASK-015 重言式测试 + deploy runbook 加「镜像先」约束。
3. **Phase C** (门清 + E2E 绿后):aria-orchestrator 开 PR → pre-merge gate (Rule #8) → merge → **bump 主仓 submodule 指针** → Phase D 归档 + `detailed-tasks.yaml` status 更新。
4. **协调**:同 Spec 任何后续工作**先 fetch + 查看板/handoff** (双子星活跃, DEC-20260704-002 Layer L 防重复在建)。

## §7 提交清单 (commit hash + multi-remote parity)
主仓 (origin+github parity, 本 session 头):
- `44aad86` docs(spec): tasks.md 1.8 机制精修 (mid_post_spec dogfood)
- `c9f5067` chore(audit): 启用 post_planning — DEC-20260704-001 (rebased)
- `5f7a001` feat(spec): 采用 30-task A.3 supersede 20-task (双子星移交全权)
- `fa19b91` chore(audit): post_planning R1→R2 CONVERGED (首个 post_planning gate)
- `55f7221` docs(m6): Phase B.2 doc-sync (CLAUDE.md M6 状态 + DEC 勘误 + TASK-019)
  (期间并发 rebase 掉双子星 `dfab74e` DEC-20260704-002 + `e9d8104` dedup handoff)

aria-orchestrator (feature/m6-dispatch-input-delivery @ `1ee225a`, origin only, **未 merge**):
- `a3a4e2d` feat(m6): Phase B.2 — dispatch input delivery TG-1~TG-5 + TG-6 fixture (36 files, +3879)
- `ef61f55` fix(m6): render invariant Critical #1 ($ARIA_ token false-fire) + scenario 5
- `a908d10` test(m6): initial-sh-unit — fetch/retry/sanitize/regex 单测 (23/23, 消灭幽灵引用)
- `1ee225a` chore(m6): code-review follow-ups (TASK-015 重言式清理 + deploy-order §6 note)

主仓 (续, doc 交付, parity):
- `068898c` docs(handoff): 本 session 收尾 handoff
- `1ec600f` docs(claude): 项目状态段 → B.2 完整实现 + code-reviewed

## §8 Memory entries this session (✅ 已写入 memory/ + MEMORY.md 压缩 24.7→9.99KB, ~90 窄条移 archive)
- `feedback_postplanning_catches_a3_derivation_blindspot` — A.2/A.3 派生产物是审计盲区;完整 post_planning 5-agent 比 2-agent dogfood 多抓 3× Major
- `feedback_agent_disconnect_not_worklost` — workflow agent "failed" 常只是返回报告断线, 工作完整;诊断先查工作树+verify 结果
- `feedback_premerge_review_catches_reproduced_critical_after_green_tests` — 6 agent TDD+1239 测试绿仍有 1 reproduced Critical;adversarial review 不可省
- `feedback_validate_invariant_at_source_not_mixed_output` — 校验"模板变量遗漏展开"要查模板 (source) 非 rendered output (混入用户数据会误判 sigil)

## Cross-references
- Spec: `openspec/changes/aria-2.0-m6-dispatch-input-delivery/` (proposal + tasks + detailed-tasks.yaml)
- DEC: `docs/decisions/DEC-20260704-001` (post_planning rollout) / `DEC-20260702-001` (Blocker 3 架构)
- 审计: `.aria/audit-reports/post_planning-R2-CONVERGED-dispatch-input-delivery.md`
- 并发: 双子星 `docs/handoff/2026-07-04-dedup-coordination-brainstorm-dec.md` (#94/#95/DEC-20260704-002)
- Blocker 4: Aria #147 / SilkNode #830
- 前次 (本 track): `2026-07-03-m6-blocker3-spec-approved-claude-md-hygiene.md` (A.1→A.2 CONVERGED)
