---
track-id: aria-m7-fleet-planning
owner-container: simonfishgit/dev-claude
phase: A-complete
status: done
updated-at: 2026-06-19T05:00:08Z
---

# Aria — Session Handoff (2026-06-18→19) — M7 aria-fleet 双 brainstorm + M7 OpenSpec **Phase A 全闭环** (planning, 无 ship)

> **Status**: ✅ **DONE**（planning + **Phase A 全流程闭环** session，**非 ship cycle / 不动插件版本**）。owner "M7 aria-fleet brainstorm" → "先 1 再 2" 双 brainstorm → deep-research 对标 → /goal 触发 agent-team 动态工作流起草 2 个 M7 OpenSpec → **post_spec R1→R2 CONVERGED → owner Approved → Phase A.3 agent 分配 LOCKED**。
> **Cycle period**: 2026-06-15 → 2026-06-19（跨多日单 session）
> **Next session 入口**: 读本 doc → `/aria:state-scanner` → §6。**M7 Phase A 已全完成; 唯一阻塞 = M6 ship (owner 运营) 解 D3 → Phase B**。

---

## §0 入口（新 session 优先读）

1. 运行 `/aria:state-scanner`，Phase 1.15 自动 surface 本 doc。
2. **本 session 无 in-flight 可 resume** — 所有产物已 commit 双远程（主仓 `3bf99e0`）。
3. **核心产出**：M7 aria-fleet **两个 OpenSpec ✅ Approved**（`openspec/changes/aria-2.0-m7-{fleet-aggregation,agent-lifecycle}/`，**Phase A 全闭环**：A.1 起草 → A.2 post_spec **R1→R2 CONVERGED** [R2 unanimous PASS 6/6] → owner Approved → **A.3 agent 分配 LOCKED**）。规范先行前置已补（PRD §里程碑 M7 stub + **US-028**）。
4. **M7 Phase A 已全完成** —— 唯一阻塞是 **Phase B 的 D3 时机门 = M6 ship**。可立即做的 AI 动作已无（A.3 已锁）。
5. **M6 ship 是 owner/外部依赖**（见 §3）：7 天运营跑（`.aria/probes/` 空，从未启动）+ AC-5 owner 人工评分（corpus `[FILL]` 空模板）。session 内无法完成，不可伪造。M6 ship 后我接手 acceptance 编排 → v2.0.0 → M7 Phase B（按已锁 agent 分配 dispatch）。

---

## §1 已完成（按时间顺序）

| 阶段 | 事件 | 产物 |
|------|------|------|
| brainstorm 轮 1 | **agent 生命周期管理**（fleet 子能力）: 对内通用定位 / 撤 marketplace 改 git 集合库 / 六阶段双向飞轮 / AB 吸收矩阵 / usage-telemetry 活体库 / 零游离不变式 | memo `.aria/notes/2026-06-16-agent-lifecycle-management-for-aria-fleet.md` |
| deep-research | agent 评测/择优 prior-art 调研（22 源 / 25 对抗核实 / 24 确认 1 驳回）→ 4 处方法论修正 | 综合写入 memo §6 |
| brainstorm 轮 2 | **fleet 整体 MVP**（核心指挥塔）: 第一刀 = 跨项目只读聚合 tool pack / 取数 ①读②刷新③推迟 / boundary-audit P0 已 ship 确认 | memo `.aria/notes/2026-06-18-aria-fleet-mvp-cross-project-aggregation.md` |
| 收尾 1 | 2 memory + #128 tracker 评论 + CLAUDE.md 项目状态 | commit `8d50cb8` / `1926654` |
| /goal → 工作流 | agent-team 动态工作流（12 agents: 4 recon + 2 draft + 6 对抗审计）起草 2 M7 OpenSpec | — |
| 落地修正 | post_spec R1 = PASS_WITH_WARNINGS（0 Critical / 11 Important 全主 loop 落地）+ grounding 验真 | commit `fe93af5` |
| M6 ship 核查 | 亲跑 `check-m6-e2e-acceptance.py` → AC-1 FAIL（0/7 probe）+ AC-5 owner 评分 `[FILL]` → **确认 M6 ship 外部受阻** | — |
| /goal clear | goal 含 session 内不可达前置（M6 ship）→ 无限 Stop-hook loop → owner clear | — |
| **收尾 + 规范先行**（06-18→19） | session handoff 写入 + latest.md pointer 更新；补 PRD §里程碑 M7 stub + §US US-028 + 新建 US-028.md；两 Spec frontmatter 悬空引用 → 锚定 US-028/PRD M7 | commit `6ce393e` |
| **post_spec R2 复审**（agent-team 3 lens × 2 Spec = 6 agents，新 run） | **6/6 unanimous PASS**，r1_landed=true 全条，0 Critical/Important residual/regression；2 Minor 处置（#128 标题 forgejo 核实 = "M7: aria-fleet implementation tracker" / audit-traj 措辞）→ **R1→R2 CONVERGED** | commit `e0f7517` |
| **owner Approved** | 两 Spec Status Draft → Approved（+ US-028 + CLAUDE.md 同步） | commit `d2bd047` |
| **Phase A.3 agent 分配 LOCKED** | 现有 roster 覆盖无 gap；两 Spec tasks.md 加 §Phase A.3 分配表（backend-architect 核心 / qa-engineer 测试 / knowledge-manager 文档 / tech-lead 架构评审 / code-reviewer post-impl） | commit `3bf99e0` |

**本 session 无 ship cycle**（纯 planning + **Phase A 全闭环**：A.1 起草 → A.2 R1→R2 CONVERGED → Approved → A.3 LOCKED；插件版本不变 v1.46.5；主项目版本不变）。

---

## §2 未完成 / Carry-forward

### 高优先级
| # | 项 | 性质 | 下一步 |
|---|---|------|--------|
| ~~H1~~ | ✅ **DONE — M7 两 Spec Phase A 全闭环**（2026-06-19） | — | A.2 R1→R2 CONVERGED + owner Approved + A.3 agent 分配 LOCKED；规范先行前置已补（PRD §里程碑 M7 + US-028）。**Phase B 待 H2（M6 ship）解 D3 时机门** |
| **H2** | **M6 ship**（= M7 Phase B 的 D3 时机门） | **owner/外部** | 启动 aria-layer1 7 天运营跑（168h Nomad uptime）+ 跑完 owner 评分 10 corpus 样本（AC-5）→ 我接手 `check-m6-e2e-acceptance` → `check-m6-release-readiness` → 归档 → v2.0.0 |
| H3 | block-flip flip | telemetry 已修 v1.46.5 | 待 ≥3 真实 gate executions 累积（future ships）→ owner 确认 Trigger B；max D+42=2026-07-05 |
| H4 | #136 Feishu secret 轮换 | owner | 代码脱敏已做，待 owner 轮换 webhook |

### M7 Spec 实施顺序（approval 后，Phase B 待 M6 ship）
- 两 sub-Spec disjoint，无 ship 顺序硬依赖；各自 Phase B 受 D3（M6 release-closeout ship）门控。
- fleet-aggregation：~26h（TG-A 取数+聚合 / TG-B 降维+接口 / TG-C workspace+文档）。
- agent-lifecycle：~24h（TG-A 集合库 / TG-B 推荐+加载 orchestrator / TG-C 更新-基础版）。

---

## §3 关键风险 / 已知陷阱

| 风险 | 触发 | 缓解 |
|------|------|------|
| **/goal 条件含 session 内不可达前置 → 无限 Stop-hook loop**（本 session 核心教训） | goal = "M6 ship 后起 M7 OpenSpec"，而 M6 ship 需 7 天 wall-clock + owner 人工评分 | 不要把外部时间/人工/基建依赖写进单 session `/goal`；发现后 `/goal clear`。memory `feedback_goal_hook_precondition_must_be_in_session_achievable` |
| **M6 ship acceptance 是真实外部闸，不可伪造** | 168h 运营跑（`.aria/probes/` 空）+ AC-5 owner 评分（`[FILL]`）+ Nomad/CF-Access 基建 | 绝不伪造 probe/corpus/评分（作废 acceptance 闸的全部意义）；待 owner 真实运营窗口 |
| M7 Spec 引用了尚不存在的 PRD §M7 / US-027（已修正为「待补」） | 起 Spec 时 memo 把 #128↔US-027 误并 | R1 审计已抓+改；H1 补 PRD M7 + 独立 US 时按 PRD 为 SOT 核对（memory `feedback_calibrate_source_of_truth_before_translating`） |
| M7 Spec 实施时误把 ⑤吸收/AB/observation 卷入下行半环 MVP | deep-research 4 修正是 forward-context | 两 Spec 已显式 OOS 标注；实施严格只做下行 pull 半环 / 只读聚合 |

---

## §4 实战教训（memory 沉淀来源）

1. **`/goal` 条件必须 session 内可达**：含外部时间（7 天 wall-clock）/ 人工评分（AD10 human gate）/ 基建（Nomad/CF）依赖的条件，任何迭代都凑不出来 → Stop-hook 无限挡停。这不是"上限"问题（无 limit 可调），是条件设定过宽。→ memory `feedback_goal_hook_precondition_must_be_in_session_achievable`（本 session 新增）。
2. **acceptance 闸不可伪造**：M6 ship 的 7 天 probe / corpus / owner 评分存在的全部意义就是诚实证明"已验证自主运行"；伪造 = 作废闸门。受阻时诚实上报 + 交还 owner，是正确行为。
3. **起 Spec 前回 PRD/US 核 SOT**（已有 memory `feedback_calibrate_source_of_truth_before_translating` 覆盖）：memo 的 #128↔US-027 误并被 draft 继承，R1 审计才抓出。

---

## §5 多维度同步状态

| 维度 | 涉及? | 状态 |
|------|------|------|
| OpenSpec | yes | 2 M7 sub-Spec **Approved**（changes/，Phase A 全闭环 A.1→A.2 CONVERGED→Approved→A.3 LOCKED）；M6 2 Spec 仍 approved 待 ship；block-flip deferred |
| aria-plugin | **no** | 版本不变 v1.46.5（无 ship） |
| 主项目 | yes | CLAUDE.md 项目状态 2 次更新（brainstorm + OpenSpec 起草）；commit `8d50cb8`/`1926654`/`fe93af5` |
| Auto-memory | yes | 2 new（见 §8） |
| Forgejo | yes | #128 评论 `#issuecomment-13165` |
| standards | no | 未碰 |

---

## §6 Next session 入口 + 优先级建议

```bash
/aria:state-scanner
```

1. ⭐ **H2 M6 ship**（owner 外部运营，**M7 唯一阻塞**）：启动 aria-layer1 7 天运营跑（168h Nomad uptime）+ 跑完 owner 评分 10 corpus 样本（AC-5）→ 我接手 `check-m6-e2e-acceptance` → `check-m6-release-readiness` → 归档 → v2.0.0 → 解 M7 Phase B 时机门（D3）→ 按已锁 agent 分配 dispatch Phase B。
2. H3 block-flip flip（待真 executions）/ H4 #136 轮换（owner）。
3. **M7 Phase A 已全闭环**（A.1→A.2 CONVERGED→Approved→A.3 LOCKED），**无剩余 AI-doable 前置**；Phase B 纯 gated on H2。

**不应该做的**：
- 不要把"M6 ship"这类外部依赖写进单 session `/goal`（本 session 教训）。
- 不要伪造 M6 probe / corpus / owner 评分。
- M7 Spec 实施时不要把上行 ⑤⑥ / AB / 影子观测卷入下行 MVP（OOS 已标）。

---

## §7 提交清单（multi-remote parity）

```
[主仓 Aria]  master = 3bf99e0 | origin (forgejo) = github ✅ (parity 实测, 每 commit 后验)
  ├─ 8d50cb8  docs(notes): M7 双 brainstorm 2 设计备忘录
  ├─ 1926654  docs(claude-md): 项目状态记 M7 brainstorm
  ├─ fe93af5  feat(openspec): 起 M7 OpenSpec 2 sub-Spec 草稿 + post_spec R1
  ├─ 6ce393e  docs(m7): handoff + PRD M7 stub + US-028 (规范先行前置)
  ├─ e0f7517  docs(m7): post_spec R2 CONVERGED — unanimous PASS
  ├─ d2bd047  feat(openspec): M7 两 Spec owner Approved
  └─ 3bf99e0  feat(openspec): M7 两 Spec Phase A.3 agent 分配 LOCKED
[aria 子模块] 未碰 (28c1a4d)
[standards]   未碰
```

**PRs**: 无（planning session，无插件 ship）
**Issues**: #128 评论 `#issuecomment-13165`（M7 设计收敛关联）
**Tags**: 无

---

## §8 Memory entries this session（2 new）

| File | Type | Theme |
|------|------|-------|
| `feedback_static_benchmark_unfit_as_oneshot_selection_gate` | feedback | 固定测试集 pass/fail 不可当 agent/skill 择优 one-shot gate（基准可 harness-game + 排名不稳）；改 pairwise LLM-judge + live 集 + pass^k |
| `reference_llm_judge_debiasing_trio` | reference | LLM-judge 去偏三件套（disjoint-family PoLL / position-swap / 五维 forced-choice）+ 引用源 |
| `feedback_goal_hook_precondition_must_be_in_session_achievable` | feedback | `/goal` 条件不可含 session 内不可达的外部前置（时间/人工/基建）否则 Stop-hook 无限挡停；非"上限"可调，解法 /goal clear；受阻诚实上报不伪造 |

（3 new this session；MEMORY.md 索引已同步）

---

## Cross-references

- M7 设计备忘录: `.aria/notes/2026-06-16-agent-lifecycle-management-for-aria-fleet.md` + `.aria/notes/2026-06-18-aria-fleet-mvp-cross-project-aggregation.md`
- 三层架构基线 (D1-D6 Approved): `.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md`
- M7 OpenSpec 草稿: `openspec/changes/aria-2.0-m7-fleet-aggregation/` + `aria-2.0-m7-agent-lifecycle/`
- M7 tracker: Forgejo Aria #128（US 待新建 US-028+）
- M6 ship acceptance: `aria-orchestrator/acceptance/check-m6-e2e-acceptance.py` + `evals/m6-prompt-quality/`（corpus 待运营 + owner 评分）
- Predecessor handoff: [2026-06-14-block-flip-restart-telemetry-fix.md](./2026-06-14-block-flip-restart-telemetry-fix.md)

---

**Created**: 2026-06-18 | **Updated**: 2026-06-19（Approve + A.3 补入）
**Status**: ✅ DONE（planning + **Phase A 全闭环**：A.1 起草 → A.2 R1→R2 CONVERGED → owner Approved → A.3 agent 分配 LOCKED）— 两 M7 Spec 可实施就绪；**唯一阻塞 = M6 ship（owner 运营窗口）解 D3 → Phase B**
