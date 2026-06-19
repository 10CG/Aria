# mid-post-spec-drift-checkpoint

> **Status**: ✅ **SHIPPED 2026-06-19** (aria-plugin v1.47.0, PR #88 merge `281388d` 双远程 parity)。代码侧完成 + reviewed (Cycle C of v1.47.0 issue-sweep release train)。实现 → **agent-team review (tech-lead)** → 全部 4 Important + 2 Minor 处置。
> **Review 处置 (tech-lead 根因洞察: 只更新了 user-facing surface, 漏了 engine-internal per-checkpoint 契约)**: Imp-1 (ship-blocking) pre-merge 完整性 gate 排除 mid_post_spec (事件条件触发可合法不产报告, 否则启用即误阻 pre_merge); Imp-2 max_rounds=1 clamp 写进模式选择屏蔽 clause (原仅 doc); Imp-3 anchor fallback 加 mid_post_spec 入 proposal 类 + 更新 #17/#79 边界 NOTE; Imp-4 report-format blocking 表加 mid_post_spec 行 (advisory 继续); Min-1 trigger 加 material-vs-incidental 判别 (防过/漏触发); Min-2 amendment neutralize 要求 (inline 标记防 amended-and-ignored, 同 memory `feedback_handoff_closure_neutralize_nextstep`) + qa-engineer 入 audit-points 对齐 config challenge team。
> **Level**: 2 (Minimal — proposal + tasks)
> **Target skills**: `aria/skills/audit-engine` + `aria/skills/agent-team-audit` + `aria/skills/phase-b-developer` + `aria/skills/config-loader`
> **Target version**: → **v1.47.0** (MINOR — 新增条件触发检查点; release-train 同批)
> **Forgejo issue**: [Aria #79](https://forgejo.10cg.pub/10CG/Aria/issues/79) — mid-implementation spec-drift detection trigger (post_spec mini-audit)
> **Rule #6**: prompt/process/config 变更 → structural 验证 + dogfood-by-construction (回放 TH v0.3.2 SMOKE-A drift incident)。

## Why

post_spec 审计只在 **Phase A.1 (spec 起草后)** 触发一次。但 Phase B 实施期, SMOKE / 集成测试常暴露 **spec 内陈述与运行实际不符** (spec 写时假设的 path/行为在跑起来后被推翻)。当前协议**无机制**在 Phase B 期重新校验 spec —— drift 被带着继续实施, 直到很晚才发现, 期间所有基于 stale 假设的 implementation 决策都要回滚。

**实战 (truffle-hound v0.3.2)**: 2026-05-02 SMOKE-A retest 翻掉了 spec 的 path A 假设, 但要到 2026-05-06 才在第 7 处 schema 漂移 + DEC §Q7+Q8 Amendment 时系统性发现 —— **中间隔 4 天**, 期间的 implementation 决策建立在已失效假设上。若有一个"drift 触发的 mini post_spec"在 SMOKE-A 翻案当时就暂停校验, 可省这 4 天 stale-assumption 实施。

## What Changes

新增 **条件触发** 检查点 `mid_post_spec` (现有 7 个检查点 + 1)。不动现有检查点列表语义。

- **TG-A (config)** — `config-loader/DEFAULTS.json`: `audit.checkpoints.mid_post_spec` (默认 `off`) + `audit.teams.mid_post_spec` (小队, 1-2 agent, scope 限漂移点) + `audit.mid_post_spec` trigger block。
- **TG-B (audit-engine)** — SKILL.md 检查点列表加 `mid_post_spec` 行 + **single-round 约束** (类 post_closure: `max_rounds=1`, scope 限漂移点, 非全量多轮收敛 — 快速校验非全审计)。mode 仍走 adaptive_rules (L1 off / L2 convergence / L3 challenge), 但**恒 single-round**。
- **TG-C (agent-team-audit)** — `audit-points.md` 加 `## mid_post_spec` 检查点节: trigger (Phase B SMOKE/集成测试暴露 spec 漂移) / agents (Tech Lead [+ 漂移点相关 agent]) / blocking=false / 输出 = **append-only spec amendment block** (类 DEC Amendment 模式) → resume Phase B。
- **TG-D (phase-b-developer)** — B.2 后加 **条件触发**: 检测到 spec 漂移信号 (机械: 测试/SMOKE 报告 `verdict_invalidated_assumptions` 字段非空; 概念: AI 识别运行实际与 spec 陈述矛盾) → 暂停 Phase B → 触发 audit-engine `mid_post_spec` (single-round) → spec amendment (append-only) → resume。
- **TG-E (config-loader doc)** — SKILL.md 配置表 + checkpoints 枚举同步 `mid_post_spec`。

### 设计原则
- **不动现有 post_spec 语义**: mid_post_spec 是**新增条件触发点**, post_spec (Phase A.1) 不变。
- **single-round / scope-limited**: 这是"漂移点快速校验", 不是全量审计。max_rounds=1 (镜像 post_closure 约束), scope 仅漂移涉及的 spec 陈述 — 避免 Phase B 被全量多轮审计打断。
- **advisory** (blocking=false): 触发 amendment 建议, 不硬阻断实施 (owner/AI 决定是否采纳 amendment); 与 #54/#95 同 advisory-over-hardlock 精神。

## Impact

- **版本**: v1.47.0 (release-train MINOR)。
- **向后兼容**: ✅ 新检查点默认 `off`; 旧配置映射不含 mid_post_spec (默认 off, 与 4 个 v1.18 新检查点同处理); 不触发则零影响。
- **受影响文件**: `audit-engine/SKILL.md` (checkpoint 列表 + 约束) + `agent-team-audit/references/audit-points.md` (新节) + `phase-b-developer/SKILL.md` (trigger flow) + `config-loader/DEFAULTS.json` + `config-loader/SKILL.md` + `config-example.md`。
- **Rule #6**: structural (checkpoint 落位 + single-round 约束 + trigger 语义) + dogfood-by-construction (回放 TH v0.3.2 SMOKE-A drift → mid_post_spec 当时即触发省 4 天)。

## Out of Scope

- **state-scanner `audit_status.mid_post_spec_pending` 字段** (#79 建议 3): 纯 surfacing, trigger 不依赖它 (trigger 由 phase-b-developer 运行期拥有); state-scanner collector 有 821 测试, 为纯展示字段触碰有回归风险 → defer 为 follow-up (低优)。
- 自动化 `verdict_invalidated_assumptions` 字段在所有测试 runner 强制产出: 本 Spec 把它作为**可选机械信号** (有则用), 主路径是 AI 识别漂移; 不强制改测试框架契约。
- 把 mid_post_spec 设为 blocking: 默认 advisory (amendment 建议); 不在本 Spec 强制硬阻断。
