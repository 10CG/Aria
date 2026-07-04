# 决策: DEC-20260704-002 — 交互 session 重复工作防护 (接活改造 Layer L, advisory + carry-id)

> **日期**: 2026-07-04 | **模式**: technical (brainstorm) | **范围**: aria-plugin (state-scanner + handoff 机制) | **spec_level**: Level 3 (预估)
> **状态**: Approved (brainstorm 收敛; post_brainstorm 审计门 off)
> **触发**: 2026-07-04 双子星 (dev-claude + dev-claude2 并行交互 session) 独立重复做同一件 Blocker3 carry-forward 活。owner: "如何修正机制、避免再发生"。

## 背景

两个并行交互 session 读同一份 handoff §6 的**自由文本** carry-forward ("⭐ Blocker3 → 起 Level 3 OpenSpec"), 各自独立做了完整 Blocker3 Spec+A.3, 数小时后才在 git push 时发现重复。

排查发现 Aria **本就为此造过防护** (`multi-terminal-coordination`, DEC-20260519-001, v1.22.0) 但**没生效**:
- Layer H (handoff frontmatter 看板, state-scanner Phase 1.16/1.17) — **真 ship 且在跑**, 能 surface 跨-owner track。
- Layer L (急切认领闸门 phase1_gate + refs/aria/coordination + reconcile) — **2,934 行有测试的完整引擎, 但从没接线** (scan.py 零调用; 归档 spec 里"集成"任务被勾 `[x]` 却从未在代码发生 — 见 [aria-plugin #95](https://forgejo.10cg.pub/10CG/aria-plugin/issues/95))。

**病根**: carry-forward 是**无主、无稳定 id 的共享待办队列** → 就算认领机制完美也无法判定两 session 在做"同一件事"。次因: 认领闸未接线 (#94) + owner-container 手填漂移 (`dev-claude` / `simonfish/dev-claude` / `simonfishgit/dev-claude`)。

## 约束条件

| 类型 | 约束 | 影响 |
|------|------|------|
| 哲学 | DEC-20260519-001 advisory-over-hardlock (可见可对账优于硬锁) | 姿态 = advisory 非 block |
| 复用 | Layer L = 2,934 行有测试引擎 (identity/reconcile/lifecycle 齐全, 含**已写好的稳定身份**) | 接活改造 > 退役重建 |
| 反模式 | #95: 死代码 on-arrival (造好不接线) 是本次病根之一 | 修法 = 接活 + runtime 探针, 非留着或再造 |
| 涌现性 | 重复是并发+稀有事件, 不能像单-session skill 那样 AB | trigger 选择须走遥测/合成-harness AB |
| 向后兼容 | 旧 handoff 无 carry-id / 旧 owner-container 手填串 | graceful degrade, 不破既有看板 |

## 考虑的方案

| 方案 | 描述 | 状态 |
|------|------|------|
| **接活改造 Layer L (选)** | 接线 phase1_gate 进 scan.py + block→advisory + 喂 carry-id key + handoff 用 identity.py + runtime 探针 | ✅ 采纳 |
| 退役 L + 在 H 上重建三件事 | 删 L, 在已跑的看板上重做 claim/surface/identity | ❌ 撤回 (brainstorm 中段修正): 等于扔 2,934 行有测试引擎 + 重造 reconcile/lifecycle; 连"稳定身份"都是 L 已写好的 |
| 硬闸 block | 认领真拦第二个 session | ❌ 逆 advisory 哲学 + 身份漂移会自拦自 |
| 纯行为约定 (无代码) | "领活前手写认领" ritual | ❌ 靠自律 — 正是这次失效的环节 |
| 两套 (H+L) 并存 | 看板显示 + 账本认领各一套 | ❌ 一致性负担; 更多机制 ≠ 更安全 |

## 最终选择: **接活改造 Layer L (advisory + carry-id key)**

不退役、不重建。把 Layer L 从"死代码"改造成"活代码 advisory 认领":复用其 identity/reconcile/lifecycle 引擎, 只改 5 处。

## 决策点清单 (供 spec-drafter 无歧义引用)

1. **执行姿态 = 响亮 advisory** (Q1): 非 block、非纯约定。第二个 session 领同一 carry-id 时, state-scanner **推荐步骤 🔴 显眼提示** ("dev-claude2 2h 前已认领 X"), 非阻塞但必须看到。符合 DEC-20260519-001。
2. **承载 = 接线并改造 Layer L** (Q2 修正): 复用 2,934 行引擎, **不退役不重建**。
3. **认领 key = 结构化 carry-forward id** (Q4, 根治病根): handoff §6 "Next" 项从自由文本 → `{id, desc}` (写交接时给稳定 slug, 如 `carry:m6-blocker3-spec`); 喂 phase1_gate 的 `derive_track_id()` 规范化槽。两 session 读同一 handoff = 同一 id = 认领必撞。
4. **稳定身份 = handoff-write 改用 `identity.py::get_identity()`**: 修复代码**本就存在** (owner=git email 本地部分 + container_id=`~/.aria/container-id` 文件 UUID, 均持久), 只是 handoff 模板 `{owner_container}` 被 AI 手填绕过。改为写入时调用 → 根除漂移。
5. **block→advisory 改造**: `run_gate()` 最后一步从"拦截/abort"改为"响亮 surface + 放行"; **reconcile 仍是最终仲裁** (最早 claimed_at 胜), 但"输的一方"是**提示**不是 abort。
6. **接线**: scan.py 调用 `run_gate()` (opt-in config, 但默认建议开; 修 #95 死代码 — 接活非删)。
7. **runtime-invocation 探针** (#95): custom-check / 遥测验 `run_gate()` 生产真被调用 (防再次烂成死代码)。
8. **claim 触发点 (auto/semi/manual) = AB 定夺** (Q3): spec 标 pending, 走下方 AB 链路科学选。
9. **surfacing 通道**: 复用 state-scanner Phase 2 推荐步骤显示 (与已跑的 Layer H 看板同位); refs/aria/coordination 账本继续作 claim 存储 (激活, 非新建)。

## AB 测试数据收集链路 (决策点 8 的科学定夺手段)

**难点**: 重复是涌现+稀有, 且须量"生产真防没防住"非"结构对不对" (Layer L 当年只跑 structural benchmark 才漏了没接线)。

- **① 埋点** (append-only JSONL `.aria/coordination-telemetry.jsonl`, 可放共享 coordination ref 汇总): `claim_written` / `collision_surfaced` (+latency) / `collision_missed` (事后才发现的重复=失败指标) / `false_positive` / `claim_friction`(steps/tokens)。每条打 **arm** 标签。
- **② 指标**: 检出率 = surfaced/(surfaced+missed) [首要] · 假阳性率 · 摩擦 · 检出时延。
- **③ 实验臂**: trigger 三变体 (auto/semi/manual) + control(不认领=现状)。
- **④ 信号来源**: **合成双-session harness** (确定性 spawn 2 session 领重叠 carry-id, 量每臂检出) [推荐, 可复现] + 真实用量遥测 [并行长期验证]。
- **⑤ 决策规则预注册**: 跑前先定阈值 (检出≥90% / 假阳性≤5% / 摩擦≤X token), 避免事后找理由 (`[[feedback_static_benchmark_unfit_as_oneshot_selection_gate]]`)。

## 连带文档同步 / 依赖边

- **关闭 [#94](https://forgejo.10cg.pub/10CG/aria-plugin/issues/94)** 核心 (本 DEC 实施 = 双子星防重复的落地): 接线 + 身份 + carry-id + advisory。
- **部分回应 [#95](https://forgejo.10cg.pub/10CG/aria-plugin/issues/95)**: 决策点 6/7 (接活 + runtime 探针) 是 #95 "死代码/勾选≠运行" 的具体修法示范; #95 的系统性修复 (archive gate 增强 / pre-#134 sweep) 仍独立排期。
- **撤销 multi-terminal-coordination 归档 spec 的"退役"念头**: L 不退役, 改为 amend/激活; 归档 spec 状态需 errata (P3/集成从未完成, 现由本 DEC 接续)。
- **handoff 机制文档** (handoff-mechanics.md / session-handoff.md §2.3): 结构化 carry-forward id + 写入用 get_identity + 开工认领时机。
- **CLAUDE.md**: Rule #9 Extension 段更新 (Layer L 从"P3 未接线"→"advisory 认领已接活")。

## 风险与缓解

| 风险 | 缓解 |
|------|------|
| 接活 L 又烂成死代码 | runtime 探针 (决策点 7) 每扫描验其真被调 |
| 身份 bootstrap: 现有容器无 `~/.aria/container-id` | get_identity 首次生成持久 UUID; spec 前置核实 bootstrap 路径 |
| 结构化 carry-forward 破旧 handoff | 旧 handoff 无 id → graceful skip / legacy 标记 (复用 Layer H 既有 legacy 处理) |
| advisory 仍被无视 (人/AI 忽略提示) | 🔴 显眼 + 放在推荐步骤 (决策前必经); 但 advisory 上限即此, 接受 (DEC-20260519-001 #4) |
| AB 拿不到信号 (涌现稀有) | 合成 harness 确定性造重叠, 不靠碰运气 |

## 待核实项 (spec Phase A 前置)

1. `~/.aria/container-id` bootstrap: 现有 dev-claude / dev-claude2 容器如何获得稳定持久身份 (首跑生成? owner 预置?)。
2. `derive_track_id(raw)` 当前把 raw 派生成什么 — carry-id 能否干净喂入不被二次改写。
3. `refs/aria/coordination` 账本激活 (休眠自 2026-05-24) — claim 读写路径核实, coordination_fetch collector 复用。
4. block→advisory 改造对 reconcile 语义的影响 (reconcile 仍仲裁, 但下游是提示非 abort — 核实无副作用)。
5. handoff §6 结构化 carry-id 的模板改动 + 向后兼容 (phase-d-closer / session-closer / handoff-mechanics)。

## spec_level / 落地
- **Level 3** (proposal + tasks): 跨 state-scanner scan.py 接线 + phase1_gate advisory 改造 + identity 接入 handoff-write + carry-forward 结构化 + AB harness + runtime 探针。
- **独立 Spec** 落 aria-plugin (state-scanner + handoff 机制), 主仓 Aria 侧同步 handoff 模板/CLAUDE.md。

---

**关联**: [#94](https://forgejo.10cg.pub/10CG/aria-plugin/issues/94) (双子星防重复) / [#95](https://forgejo.10cg.pub/10CG/aria-plugin/issues/95) (勾选≠运行流程病根) / DEC-20260519-001 (multi-terminal-coordination 母决策) / 归档 spec `openspec/archive/2026-05-20-multi-terminal-coordination` (Layer L 引擎所在) / 事故 handoff `docs/handoff/2026-07-03-m6-blocker3-spec-approved-claude-md-hygiene.md`
**下一步**: spec-drafter 据本 DEC 起 Level 3 OpenSpec (proposal + tasks), 落 aria-plugin。
