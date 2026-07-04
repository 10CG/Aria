# 决策: DEC-20260704-001 - 审计检查点分步 rollout — 启用 post_planning (dogfood-verified)

> **日期**: 2026-07-04 | **模式**: rollout amendment (governance)
> **Rollout 起源**: [DEC-20260519-001](./DEC-20260519-001-multi-terminal-coordination.md)（`.aria/config.json` audit rider: post_spec 2026-05-19 启用 +「其余 checkpoints 待验证后逐个开」分步 rollout 姿态）
> **触发**: owner 请求「增加 Aria 多轮收敛审计环节以提高 spec 质量」→ brainstorm (problem) reframe: 引擎/检查点已建, 缺口是**激活 + rigor** 而非构建 → 方向 A (推进 rollout) → 2026-07-04 dogfood。

## 背景

Aria 的 audit-engine 多轮收敛审计**引擎 + 全部检查点已存在并接线** (post_brainstorm / post_spec / post_planning / mid_post_spec / mid_implementation / post_implementation / pre_merge / post_closure)。当前 `.aria/config.json` 仅 **post_spec = convergence** 启用, 其余 = `off` —— 这是 DEC-20260519-001 立下的**刻意分步 rollout**「一次一步、验证后再开」(config `_comment` 存证), 非缺失。

2026-07-04 对 `mid_post_spec` 做 dogfood: 以 `aria-2.0-m6-dispatch-input-delivery` Spec 的一份 **A.3 草稿** (本 session 产出的 30-task `detailed-tasks.yaml`) 为活靶子, 用 code-grounding recon 当 SMOKE 信号, 派 2 独立 agent (tech-lead + qa-engineer, 单轮 scoped) 校验 spec 陈述 vs 真实 aria-orchestrator@daf7c79 代码。**抓到 2 类真实 drift**:

1. **per-artifact 转录 drift (CONFIRMED material)** — 该草稿 TASK-016 deliverable 把 `FailReason` 定位到 `audit/interfaces.py`(该文件 67 行、无 FailReason;真实在 `aria_layer1/interfaces.py:67`)。**这是本 session A.3 草稿引入的转录 slip** —— proposal.md 正文正确写 `interfaces.py`; 且**另一并发容器独立产出的 A.3** (见下 §并发) **未犯此错**(用了正确路径)。正是 post_planning 该拦的、per-artifact 层的降精度错。
2. **shared spec-wording drift (advisory)** — 「compute-assertions.sh dies at :37」措辞在 proposal.md §C + tasks.md 1.8 等**共享 spec 文本**掩盖真实失败路径 (`:514` `|| true` 吞异常 → hits 默认 false → `ASSERTION_MISMATCH` → exit1 → S_FAIL)。qa 指出会致 RED 测试测错失败模式 (paper-fix 风险)。已就地修正 tasks.md 1.8。

**诚实校准**: dogfood 的价值 = (a) **验证了 post_planning/mid_post_spec 的判别机制**(多-agent code-grounded 漂移裁决 + material 过滤有判别力: 抓真 drift、排除假阳性); (b) 抓到一处 **per-artifact 转录 drift** + 一处 **shared spec 措辞 drift**。它**并不证明**某一份 A.3 优于另一份 —— FailReason「catch」抓的是本 session 草稿自身的手滑。但这恰恰**印证 post_planning 的必要性**: proposal.md 被 3 轮 post_spec 审细了, 派生到 A.2/A.3 任务清单时**降精度**, 而这块**当前零审计** (post_planning=off)。证据直接指向 post_planning (审 A.2/A.3, 时点在 Phase B 前)。

## 并发 (2026-07-04, 记录以备协调)

本 session 与另一容器 (simonfishgit) **并发对同一 Spec 做了 A.3** —— 本 session 30-task 版 (dogfood 靶子) vs 对方 20-task 版 (`7ce3cee`, 先落 remote)。**裁决 (owner 2026-07-04)**: 双子星容器明确**停止处理本任务、全权移交本侧** → 采用本 session **30-task 细粒度版** (1:1 对 tasks.md + verification↔AC + 富 notes; FailReason 转录 slip 已 dogfood 修正), **supersede 对方 20-task 版** (保留在 git 历史 `7ce3cee` 备查; 早前推的对比分支 `backup/a3-30task-dogfood-2026-07-04` 即此版)。本 DEC 的 post_planning 决策**独立于该裁决** (rollout 治理 ≠ 选哪份 A.3)。教训: 同 repo 建多小时 feature 前应 claim/coordinate (memory `feedback_concurrent_feature_collision_claim_before_build`) —— 本次 file-level 无硬冲突但 feature-level 撞, 靠 owner 事后仲裁 + 移交解决。

## 约束条件

| 类型 | 约束 | 影响 |
|------|------|------|
| 治理 | 分步 rollout: 一次一步, dogfood 验证后再开 (DEC-20260519-001) | 本次只开 1 个 checkpoint |
| proportionality | Aria 反 always-on 全量审计 (见 memory audit collapse/proportional 系列) | mode 选择需权衡成本 |
| 稳定性 | 不改已验证的 post_spec (working) | 只 additive 加 post_planning |
| SOT | `.aria/config.json` = checkpoint 启用真理来源; DEC = 决策 provenance | config + DEC 双写 |
| Rule #6 | dogfood = 验证活动, 不需独立 OpenSpec | 本 rollout 走 DEC + config, 非 Spec |

## 考虑的方案

| 方案 | 描述 | 评分 | 状态 |
|------|------|------|------|
| **A. 开 post_planning (convergence)** | 审 A.2/A.3 任务产物; mode 与 post_spec 一致 | 证据最强 · 时点最优 · 无审计区 | ✅ **选定** |
| B. 开 mid_post_spec | 审 Phase B 运行时暴露的 spec 漂移 | 机制已验证, 但独家场景 (运行时漂移) 本次未真正触发 | ⏸️ Deferred — 待真 Phase B SMOKE dogfood 再锁 |
| C. 两个都开 | post_planning + mid_post_spec 互补 | 理想终态, 但违「一次一步」 | ⏸️ 分两步走 (先 A, 后 B) |
| D. 不开 / 强化 post_spec | 保持现状或加 post_spec rigor | 无法覆盖派生产物降精度 (drift 所在) | ❌ 未选 |

## 最终选择

**方案 A**: `.aria/config.json` 中 `checkpoints.post_planning`: `off` → **`convergence`**, 并新增 `teams.post_planning`(镜像 `teams.post_spec` 5-agent roster: tech-lead / backend-architect / qa-engineer / code-reviewer / knowledge-manager)。

- **Mode = convergence**: 与当前唯一启用的 post_spec 姿态一致; 首次激活取保守值。存在 `audit.scope_skip_paths` file-scope cap (ops/docs-only 变更自动降级), 减轻小改动成本。
- **mid_post_spec = deferred**: 其**判别机制**(多-agent 漂移裁决 + material 过滤 + amendment)本次 dogfood 已验证 (与 post_planning 共用同一套); 但其**独家价值**(运行时代码跑起来才暴露的漂移)需一次真正 Phase B SMOKE 触发才算验证 → 留待 Phase B dogfood 后另立 rollout amendment。

## 理由

1. **dogfood 证据直接指向 post_planning** — 抓到的 drift 落在 A.2/A.3 产物 (per-artifact 转录 + shared 措辞), post_planning 正是审这块的检查点, 且时点在 Phase B **之前**拦截。
2. **A.2/A.3 是当前唯一的「审计盲区」** — proposal 有 post_spec 把关, Phase C 有 pre-merge (待开) + code-reviewer, 唯独规划期派生产物零审计 —— 而实证 (本 session 草稿即含转录 slip) 显示这正是降精度 drift 高发区。
3. **同一套已验证机制** — dogfood 证明 tech-lead+qa 单轮 code-grounded 校验能抓真 drift 且判别力正确 (不误报 incidental / 排除假阳性)。
4. **尊重分步治理 + proportionality** — 一次只开一个, convergence + scope_skip cap 控成本, mid_post_spec 分步 deferred。

## 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| convergence on every plan 对小 spec 偏重 | `scope_skip_paths` 已把 ops/docs-only 降级; 观察 N 个 plan 后可调 `post_planning` → `adaptive` (需补 `adaptive_rules` L1 off/L2 conv/L3 challenge) |
| 首次激活行为未知 | 首个真实 post_planning 触发即为二次 dogfood; blocking 语义按 audit-engine 默认 (FAIL 阻塞任务列表修订) |
| 与 mid_post_spec 领域重叠 | 明确分工: post_planning 管规划期派生漂移 (本 DEC), mid_post_spec 管实施期运行漂移 (deferred) |

## 后续

- **config 改动** (本 DEC 同批): `.aria/config.json` `checkpoints.post_planning` = convergence + `teams.post_planning` + `_comment` 更新引用本 DEC。
- **落地的 A.3** = 本 session **30-task 版** (`detailed-tasks.yaml`; owner 2026-07-04 全权归本侧后采用, supersede 对方 20-task `7ce3cee`, 后者留 git 历史)。proposal.md Status 同步更新为 30 tasks。
- **shared spec 修正**: tasks.md 1.8 「dies at :37」→ 精确机制 (随本 rollout 前序 commit 落地)。
- **观察窗**: 首个走 post_planning 的 Spec 即二次 dogfood; 评估 verdict 质量 / 成本 / 是否调 adaptive。
- **mid_post_spec**: Phase B 首次 SMOKE-触发 dogfood 后另立 rollout amendment 决定是否锁定。
