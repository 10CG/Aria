# Triage: aria-plugin#17 (Drift Guard) vs #18 (Token × Attention Estimator)

**Session**: 2026-04-23
**Triage owner**: main session (post Option 2 handoff)
**目的**: 在两个 open feature issue 中决定谁先走 Phase A.1 (Spec 起草)

---

## #17 — audit-engine Drift Guard

| 维度 | 评估 |
|---|---|
| **类型** | Bug-class feature (修补已知结构性盲点) |
| **Scope** | 单 Skill (`audit-engine`) + 2 references (challenge-mode-schema / convergence-algorithm) |
| **Level** | Level 2 (proposal.md 足够, 代码改动集中) |
| **估算** | ~8-12h (含 benchmark) |
| **影响** | 所有 challenge 模式 audit (post_spec / post_brainstorm / post_planning / pre_merge) |
| **Dogfooding 证据** | **本 session 刚跑 4 轮 post_spec audit 使用 convergence 模式 1 轮即收敛, 未触发 challenge 模式**, 但 #17 描述的漂移路径在本 session 审计中**理论上可能发生** (如 4 agent 在 Round 2/3 聚焦 T4.3 工具链而忘了 T7.1 diff 等价性) |
| **风险** | 低-中 (新增字段, 向后兼容, 默认关闭可选) |
| **价值** | 高 (audit-engine 是所有 Phase audit 的核心, 准确度提升直接放大到所有 Spec 评审) |
| **紧迫度** | P1 (越早引入, 所有未来 audit 受益越多) |

## #18 — Token × Attention Estimator

| 维度 | 评估 |
|---|---|
| **类型** | Paradigm shift (估算主轴从人工时 → Token × Attention 双轴) |
| **Scope** | 新 Skill `ai-native-estimator` + 改动 6 Skills (task-planner / progress-updater / state-scanner / phase-a-planner / phase-d-closer / requirements-sync) |
| **Level** | Level 3 Full (跨多 Skill methodology shift) |
| **估算** | ~60-80h (双轴计算公式 + 每个集成点 ~8h + 迁移文档) |
| **影响** | 全十步循环的 velocity / burn-down / 进度预测 |
| **Dogfooding 证据** | 本 session 的工时估算 "46h → 52h (revise 后) → 单 session 不可能完成" 正是 #18 所说的"4-8h 假设失效"的典型案例 |
| **风险** | 高 (methodology shift, 跨多 Skill 同步, 潜在破坏现有 KPI 语义) |
| **价值** | 高 (addresses 真实痛点) 但**偏研究** (双轴公式需要多次校准) |
| **紧迫度** | P2 (无硬阻塞, 当前 ad-hoc 估算仍可用, 且 Aria 2.0 M2 起草前不是必要) |

---

## 决议

**先 #17, 后 #18**, 理由:

1. **#17 是 bug, #18 是 paradigm** — bug 修复优先级天然 >新范式研究
2. **#17 放大 #18 的收益** — 如果先做 #18 在 audit-engine 修好前, audit 自身可能带 drift 漂到 #18 的估算争议上, 污染 methodology 设计
3. **#17 规模匹配可用 session** — 8-12h 可在下一个 session 完整走完 Phase A-C
4. **#18 需要先做 spike** — 建议 #18 的 Phase A 前先做 1 次 AB token measurement spike (参考 feedback_spike_first_for_data_hypotheses), 收集真实 token 消耗数据后再立 Spec, 否则容易产出"~60h 产出未经校准公式"
5. **#18 M2 前不阻塞** — Aria 2.0 US-022 M2 规划只需 ad-hoc 估算, 不需要 #18 的双轴公式

## 下一步 (独立 session)

### Path A (推荐): #17 Phase A.1
- 读 `aria/skills/audit-engine/references/challenge-mode-schema.md` + `convergence-algorithm.md`
- 起草 `openspec/changes/audit-engine-drift-guard/proposal.md` (Level 2)
- 参考 Issue body 的 4 段建议方案直接吸收 (anchor 冻结 / drift_ratio 阈值 / 报告字段 / 兼容)
- 估算: ~8-12h, 单 session 可完整 Phase A-C

### Path B (并行可行): #18 Pre-Spec Spike
- 不立 Spec, 先在 aria-plugin-benchmarks 开一个 `token-attention-spike/` 目录
- 在 1-2 个历史 session 上反算实际 token 消耗 (通过 Claude Code transcripts) 和 attention-minutes (通过 human-in-loop 决策点计数)
- 校准公式 `normalized_tokens × model_weight[tier]` 的权重
- 估算: ~4h spike, 产出决定是否立 #18 Spec

## 本 session 对 #17/#18 的执行边界

**本 session 不启动 Phase A.1 Spec 起草** (会严重超出 session 预算, 且与选项 2 handoff 冲突)。本 session 仅完成:

- ✅ Triage 决议输出 (本文件)
- ✅ 两个 Issue 的优先级排序
- ✅ 下 session 的明确起点 (Path A #17 起)
- ⬜ Spec 起草留给下一独立 session

**Forgejo 回写** (可选, 非本 session 强制): 把本 triage 结论以 comment 回写到 aria-plugin#17 + #18, 便于未来 GitHub / Forgejo 用户跟踪优先级。暂留作用户决定是否触发。
