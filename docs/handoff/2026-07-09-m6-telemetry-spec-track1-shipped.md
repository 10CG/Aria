---
track-id: aria-2.0-m6-cost-model-telemetry
owner-container: aria-runner-bot/023236f2
phase: session-close
status: complete
updated-at: 2026-07-09T16:06:33Z
---

# Aria — Session Handoff (2026-07-09) — M6 遥测 Spec 起草→批准→Track-1 实施 (+ runtime-probe v1.54.0 已另交接)

## §0 入口 (新 session 优先读)

本 session 两条主线: (1) **runtime-probe-archive-gate-integration ship v1.54.0** 全周期 (B→C→D, PR#97 merged 565e214a, 归档) —— **已有独立 handoff `2026-07-09-runtime-probe-shipped-v1.54.0.md`, 本文不复述**; (2) **M6 遥测 Spec `aria-2.0-m6-cost-model-telemetry` 从零起草到 Track-1 实施** —— 本 handoff 主体。

遥测 Spec 现态: **Approved (owner 2026-07-09) + Track-1 (Layer1 遥测管道) 动态工作流实施完成**。头号 carry = **Track-1 合并** (gate input-delivery) + **Track-2/3 待起** (见 §2/§6)。

## §1 已完成 (遥测 Spec 线, 按时间顺序)

1. **probe-first grounding** (memory 强规矩): Explore 侦察「Layer2→Layer1 cost/model 遥测链现状」→ code-grounded 抓到 **2 断点** (result.json 跨节点不可读 + claude_usage 无 model) + **模型接线 5 处糊涂账** + **glm-5.2 cutover 疑 inert 红旗** (--model smart-sonnet 非 canonical alias 使 ANTHROPIC_DEFAULT_OPUS_MODEL 结构性 inert)。
2. **owner 决策** (交互, 大白话澄清): Q1 token 全维 (含 cache) / Q2 config 真源清 smart-sonnet / Q3 独立表 / scope A 含返工路径 / 兜底配置驱动可见 / 单源 ANTHROPIC_DEFAULT_OPUS_MODEL opus 档。
3. **DEC-20260709-001 v2**: 决策 SOT + **4-agent code-grounded 设计审议** (tech-lead/backend/qa/km) → **2 OBJECTION** (O1 记 config 非 served 是套套逻辑检不出 inert / O2 返工路径盲区 + marker 覆盖不全) + 2 CONCERNS 全折入。O1 折入使设计诚实度实质提升 (served-model 观测 + echo 失效模式)。
4. **L3 Spec 起草**: proposal (5 部件 A-E + 12 AC 含硬前置 AC-10) + tasks (8 Phase, 3 相位 Track-1/2/3)。
5. **post_spec 5-agent** (tech-lead/qa/ai-engineer/km/backend): **R1 (~30 findings 全 spec-doc 层)** → R1-fix → **R2 (tech-lead CONVERGED / backend·qa 机械 REVISE)** → R2-fix → **R3 backend 0 新 CONVERGED**。真跑到稳定轮 (非 collapse)。报告 `.aria/audit-reports/post_spec-FINAL-1783602519132-*`。
6. **owner 批准** → Status Approved。
7. **⚠️ 开工前踩点抓协调发现**: DEC/post_spec 均判「Track-1 Layer1 可独立」**实测不成立** —— input-delivery 已占 migration 008 (5.0→5.1) + 改 schema.sql/db.py, 与 Track-1 建表**文件级重叠** (线性 migration 单链不可并行占号)。**owner 决策 A**: Track-1 叠 `feature/m6-dispatch-input-delivery` (migration 009 5.1→5.2)。
8. **动态工作流实施 Track-1** (owner「使用动态工作流」): Workflow 工具 5-agent 四阶段 (foundation → 2 consumer 并行 → code-reviewer PASS + silent-failure-hunter REVISE[1 Important echo-caveat] → 0 Critical 故 Fix 跳过)。**主控修 echo-caveat** (served_model_check 加 echo/AC-10 caveat + 软化 db.py/schema.sql「ground-truth/objective」过度声称)。独立复跑 **aria-layer1 979 OK + acceptance 196 OK**。提交 aria-orchestrator `92acce5`。
9. **主仓记录**: proposal Status/tasks Phase 4-5 勾选 + CLAUDE.md 项目状态更新 (Drafting→Approved+Track-1)。

## §2 未完成 / Carry-forward 清单 (AI 内省 + 机械补漏)

1. ⭐ **`{id: carry-telemetry-track1-merge, desc: Track-1 已实施 @ aria-orch 92acce5 待合并, gate input-delivery 合并主干 (选项 A stacked); input-delivery 卡 4 owner/infra 门}`** —— 代码就绪, merge 排 input-delivery 后。
2. **`{id: carry-telemetry-track2, desc: Track-2 容器侧 (模型接线统一 5 处 claude 调用点 + parser served 观测 + marker 发射) Phase 1-3}`** —— gate input-delivery 合并 (同文件 initial.sh + 同镜像重建)。
3. **`{id: carry-telemetry-track3-ac10, desc: Track-3 AC-10 活体验证 served==真跑 glm-5.2}`** —— gate Luxeno Blocker 4; **决定 echo 失效模式是否成立** (Luxeno verbatim-echo 请求名则 served 检测器降级客户端检测器)。
4. **`{id: carry-telemetry-phase6-docs, desc: Phase 6 文档同步 (layer-boundary-contract §6 marker 协议 + cutover-runbook §5 死指令改 served_model + architecture-decisions AD-M6-13/14/15)}`** —— 未做, 随 Track-1 merge / Phase C。
5. **`{id: carry-ad-m6-10-doubleclaim, desc: AD-M6-10 被 release-closeout 与 input-delivery 重复认领}`** (heads-up, owner 门): input-delivery 快合并, 现在改号成本最低; 本 Spec 避开从 AD-M6-13。
6. **机械补漏 (advisory, 已知非阻塞)**: consistency_check flag「active change 未列 UPM in-progress」×多 —— Aria **无 runtime UPM** (既知), 属预期噪音非真不一致。
7. **旧 carry (未动)**: 主仓 /VERSION 陈旧 (1.7.3 vs 1.6.0) / i18n README @1.51.0 vs 1.55.0。

## §3 关键风险 / 已知陷阱

- **线性 migration 是协调 singleton**: 两并发分支都往 schema_migrate `_MIGRATIONS`/`_LATEST_SCHEMA_VERSION` 加 migration **必撞** (号 + 版本单例)。「Layer X 独立」的判断**必须查 migration 文件本身**, 不能只看功能面。本 session 靠开工前 `git diff` 踩点才抓到 (spec + 5-agent 审计只查 `docker/` 漏查 `hermes-extensions/aria-layer1/`)。
- **served-model echo 盲区**: cost.json served_model_check 的「pass」是**客户端配置比对**, 不排除 Luxeno verbatim-echo (静默跑别的模型却回显请求名)。已加 caveat, 但真判定须 AC-10 活体 (Track-3, gate Luxeno)。别把离线测试的 pass 当「真跑验证」。
- **双子星并发**: 本 session 主仓 rebase ≥3 次 (双子星 ship agent-router v1.55.0 + handoff)。**每次 push 失败先 fetch+rebase, 查 CLAUDE.md 高争用段是否撞** (本 session 均不同行干净合并)。
- **主仓 aria-orchestrator 指针别误 bump**: Track-1 在未合并分支; `M aria-orchestrator` 是本地 checkout 在 Track-1 分支, **绝不 stage** (会把主仓指针指向未合并 Track-1)。

## §4 实战教训 (memory 沉淀)

- ✅ 新增 `feedback_cross_doc_claim_verify_at_target` (文档 A 写「已在 B 做 X」必去 B 实测; 本 session 3× 实证: dangling memory / tasks 4.4 未删 / runbook 项8)。双子星 session **独立**也补录了同款「claim-gate」教训 —— 两 session 并发撞同一课。
- ✅ 新增 `reference_forgejo_agit_pr_fallback` (API PAT stale 时 AGit `refs/for/master` 建 PR 无需 token)。
- **强化既有** `feedback_concurrent_feature_collision_claim_before_build`: 本 session 补一角 —— **审计判「disjoint」时只查了一个目录 (docker/), 重叠在另一目录 (hermes-extensions/aria-layer1/ 的 schema/migration)**; 线性 migration 序列是撞点。disjointness 声称须跨**所有触及目录**核 file-overlap, 尤其 migration 单链。
- **复用验证**: `feedback_probe_first_scope_reframe` (Explore 踩点抓 2 断点+红旗, 免架空 brainstorm) / `feedback_code_grounded_multiagent_review_catches_altitude_misses` (DEC 4-agent 抓 2 OBJECTION [O1 served / O2 返工] 我高度看漏) / `feedback_review_catches_critical_despite_green_tests` (979 绿仍核实既有 migration test 是合法版本 bump 非削弱) / `feedback_owner_invoked_convergence_loop` (post_spec 真跑 R1→R3 非提前 collapse)。

## §5 多维度同步状态 (Aria 4 维)

- **OpenSpec**: active — 遥测 Spec (Approved, Track-1 实施完成待合并) + M6×3 (input-delivery/e2e-resilience/release-closeout) + M7×2。0 pending_archive。
- **UserStory**: US-026 (M6, in_progress)。**UPM**: 无 runtime UPM (既知; consistency flag 属预期)。
- **版本**: 插件 aria-plugin **v1.55.0** (双子星 agent-router ship; 本 session runtime-probe v1.54.0 已被 v1.55.0 supersede) | 主项目 v1.7.3 | aria-orchestrator v2.0.0。
- **git**: main `dca8e0c` (含 CLAUDE.md 更新, 待推) | aria-orch Track-1 `92acce5` (origin, 分支) | aria `1a46350` (v1.55.0) | standards `9df1722`。

## §6 Next session 入口 + 优先级建议

1. **owner 门 (最高)**: input-delivery 清 4 门 (build 021/deploy/egress 028/E2E 029←Luxeno) → 合并主干 → **解锁 Track-1 合并 + Track-2 开工**。Luxeno Blocker 4 → 解锁 Track-3 AC-10。
2. **input-delivery 合并后**: Track-1 rebase 到 master + 合并 (migration 009 链干净) + 主仓 aria-orch 指针 bump。然后 Track-2 容器侧 (同镜像重建周期)。
3. **`{id: carry-ad-m6-10-doubleclaim}`** —— input-delivery 合并前理号成本最低。
4. **低优先随手**: `{carry-version-file-stale}` / `{carry-i18n-readme-stale}`。

> ⚠️ 新 cycle 开工前 fetch + 看双子星; 触 aria-orchestrator schema/migration 前先查 input-delivery 分支重叠。

## §7 提交清单 (multi-remote parity)

| repo | SHA | 内容 | parity |
|---|---|---|---|
| main | `dca8e0c` ← ... ← `662cfdd` (本 session: 遥测 DEC/spec/audit + Track-1 记录 + CLAUDE.md) | 待推 (前序均 origin=github) | 推后核 |
| aria-orchestrator (Track-1 分支) | `92acce5` (feature/m6-cost-model-telemetry, 叠 input-delivery, 3165 行) | origin ✓ (分支) |
| aria / standards | 1a46350 (v1.55.0 双子星) / 9df1722 | 未动 ✓ |

> runtime-probe v1.54.0 提交链见其独立 handoff。

## §8 Memory entries this session

- 新增 2: `feedback_cross_doc_claim_verify_at_target` / `reference_forgejo_agit_pr_fallback` (已入 MEMORY.md 索引)。
- 强化 1: `feedback_concurrent_feature_collision_claim_before_build` (审计查错目录 + migration 单链撞点, §4)。

## §9 会话收尾核验 (session-closer, 2026-07-09)

机械兜底: 各仓 sync 核实 (main 三方一致 / Track-1 分支已推 / standards 一致; CLAUDE.md commit 待推随本 handoff); scan exit 0; consistency flag 全 advisory 已知 (无 runtime UPM)。内省: 未完成线程全收入 §2 (Track-1 merge + Track-2/3 + Phase6 docs + AD-M6-10 + 旧 carry); 待固化经验 §4 (2 新 memory + 1 强化)。leaf 终结 —— 不调 phase-d/workflow-runner/openspec-archive (遥测 Spec 未走完 cycle, 无 shipped-未归档 cycle)。

## Cross-references

- 决策 SOT: `docs/decisions/DEC-20260709-001-layer2-cost-model-telemetry.md` v2 (§9 4-agent 审议 + §10 AD heads-up)
- Spec: `openspec/changes/aria-2.0-m6-cost-model-telemetry/{proposal,tasks}.md` (Approved)
- 审计: `.aria/audit-reports/post_spec-FINAL-1783602519132-*`
- Track-1 实施: aria-orchestrator `feature/m6-cost-model-telemetry` @ `92acce5`
- 姊妹 handoff: `2026-07-09-runtime-probe-shipped-v1.54.0.md` (runtime-probe v1.54.0 全周期)
- sibling Spec: `aria-2.0-m6-dispatch-input-delivery` (Track-1 串行前置)
