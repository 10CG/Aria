# session-closer 综合方案 — Task Breakdown

> **Spec**: proposal.md
> **Created**: 2026-06-25
> **Status**: ✅ Approved (Phase A.2 CONVERGED 2026-06-25, R1 REVISE×3 → Rev1 → R2 PASS×3; 待 A.3 → Phase B.1)
> **Supersedes**: session-closeout-internalization (复用其 ~70-80% 实现, 据 DEC-20260625-001 架构修订)

## Overview

会话收尾 = 与十步循环正交平级的 leaf skill 仪式。独立入口 (对话内省优先 + 机械兜底) + 共享 handoff-write canonical 原语 + phase-d description 收紧消歧 + 复用前序机械采集/校验/触发器。

---

## Dependencies

### External
- state-scanner collectors: `sync.py`/`multi_remote.py`/`upm.py`/`openspec.py`/`requirements.py` (已存在, 接口已验证完好)
- `aria-token-telemetry`/`aria-context-monitor` (v1.33.0 #104) — context occupancy
- 既有 `phase-d-closer/references/handoff-mechanics.md` (复用为共享 SOT, 不新建)

### Internal
- `aria/templates/session-handoff.md` (9 段, 复用)
- `standards/conventions/session-handoff.md` (Rule #9 SoT)
- **前序复用件** (cherry-pick from `origin/feature/session-closeout-internalization`): `handoff_autofill.py` / `consistency_check.py` / `closeout_trigger.py` + 3 测试 + phase-b/c 钩子 (路径需重映射 session-closeout→session-closer; 字段漂移见 §TASK-003/004)。**standards §2.2.1 不复用** (旧版描述被否决的 closeout_only 委托 → TASK-008 重写)

---

## Task List

### Phase 0: 复活准备 (cherry-pick, D2)

#### TASK-000: cherry-pick 复用件到新分支 (含路径重映射 + 字段漂移修正) [R1 Major]
- **Description**: aria 子模块新分支 (off 当前 master v1.49.0) 拷贝前序复用件: `handoff_autofill.py` / `consistency_check.py` / `closeout_trigger.py` + 3 测试, **路径从 `skills/session-closeout/`→`skills/session-closer/` 重映射** (测试内 import/path 引用同步改)。phase-b/c 钩子留 TASK-007。**弃** closeout_only(+29) + 薄入口(+86)。standards §2.2.1 **不拷** (旧版描述 closeout_only 委托, 被否决架构 → TASK-008 重写)。旧 3 feature 分支保留归档 trail (OOS-7)。
- **Complexity**: S | **Estimated**: 1h | **Dependencies**: None | **Agent**: tech-lead
- **Acceptance**:
  - [ ] 脚本/测试落 `session-closer/`; `grep -rn session-closeout aria/skills/session-closer/` 无残留旧 skill 名 ([[feedback_verify_edit_landed_grep_count]])
  - [ ] 旧测试 cherry-pick 后跑 (注意: 旧测试手造 fixture 假绿, 真接口修正在 TASK-003/004)
  - [ ] 无 closeout_only/薄入口残留; §2.2.1 未拷入

### Phase 1: 共享原语 + leaf 入口 + 消歧

#### TASK-001: 复用既有 handoff-mechanics.md 当共享 SOT (AD-1) [R1 Critical 修正]
- **Description**: **不新建文件**。canonical SOT = **既有** `aria/skills/phase-d-closer/references/handoff-mechanics.md` (已含 9 段 variable 字典 / latest.md 2 子步骤 + decision table / Rule #9 L1+L5 / slug / Forbidden patterns)。动作: (a) audit 该 ref 是否覆盖 session-closer step4 所需机制; (b) 若有缺口**仅 additive 补段** (既有锚点不删改); (c) 文档内加一行说明「共享 handoff-write 机制 SOT (phase-d D.3 + session-closer 共用)」; (d) session-closer step4 交叉引用它。**phase-d-closer D.3 完全不动** (L161 引用不变)。
- **Complexity**: S | **Estimated**: 0.5h | **Dependencies**: TASK-000 | **Agent**: knowledge-manager
- **Acceptance**:
  - [ ] 无新建 `handoff-write-mechanics.md` 或第二份 handoff-write ref; 仓库仅一份 (AC-11)
  - [ ] session-closer step4 + phase-d D.3 均 grep 命中引用 `handoff-mechanics.md` (AC-11)
  - [ ] 若补段则 additive: 既有锚点 grep 仍在 (AC-8b); phase-d SKILL.md D.3 段 git diff 为空 (AC-8a)

#### TASK-002: 独立 session-closer leaf skill (AD-1 + AD-2)
- **Description**: 新建 `aria/skills/session-closer/SKILL.md`。强绑会话触发词 ("对话收尾"/"执行对话收尾"/"session closeout"/"收尾这次对话"/"写交接"/"收工")。自有编排 (不穿 phase-d): step1/2 AI 内省优先 (未完成线程 + 待固化经验) → step0/3 autofill+consistency 机械交叉核验补漏 → step4 按 ref 写 handoff → 终结 (leaf)。发现未归档 cycle 仅 surface 提议。
- **Complexity**: M | **Estimated**: 2h | **Dependencies**: TASK-001 | **Agent**: knowledge-manager
- **Acceptance**:
  - [ ] 独立可调, 不路由 phase-d, 不触发 D.1/D.2 (AC-1)
  - [ ] leaf: 不调 phase-a/b/c/d/workflow-runner; 未归档 cycle 仅 advisory (AC-1b)
  - [ ] step1/2 对话内省为 load-bearing 段 (AC-3); step2 主动提炼未固化经验 (AC-5b)

#### TASK-002b: phase-d-closer description 收紧 (AD-3)
- **Description**: `phase-d-closer/SKILL.md` description 中度 rebind — 删「写 session handoff」+ 裸「收尾」, rebind cycle-explicit (「Phase D / 周期收尾 / 归档 Spec / 更新 cycle 进度」)。纯 description 字面, **不改任何执行逻辑**。
- **Complexity**: S | **Estimated**: 0.3h | **Dependencies**: TASK-002 | **Agent**: knowledge-manager
- **Acceptance**:
  - [ ] grep phase-d description 不含「写 session handoff」与裸「收尾」(AC-9a)
  - [ ] phase-d 执行逻辑 byte 不变 (AC-8)

### Phase 2: 机械采集 + 校验 (复用前序)

#### TASK-003: handoff_autofill 重建 adapter + 字段修正 + 补漏 (AD-2) [R1 Critical/M-1]
- **Description**: `handoff_autofill.py` 只有纯函数 (`fill_sync_section`/`assemble_unfinished`/`four_dim_status`), **无 snapshot adapter/main — 解析编排层原在被弃薄入口 prose, 需重建**。含 3 处归一化: ① §7 `sync_status.multi_remote` 嵌套路径 ② §2 carry_forward `dict{by_change}`→list ③ followup `dict`→可读 item。**字段漂移修正**: `upm.cycle_number`→`current_cycle`。接入 step0/3 交叉核验补漏 (静态输入对: snapshot 有 X + §2 草稿无 X → flag X)。
- **Complexity**: M | **Estimated**: 1.5-2h (重建 adapter + 3 归一化, 非"仅接线") | **Dependencies**: TASK-002 | **Agent**: backend-architect
- **Acceptance**:
  - [ ] §7 用 `snapshot.sync_status.multi_remote` 嵌套路径填真实 SHA/parity + ahead 告警 (AC-2)
  - [ ] §5 四维 UPM.cycle 读 `current_cycle` 非 None when configured (字段修正)
  - [ ] 补漏: 静态输入对 (snapshot 有 followup X + 草稿无 X) → flag X (AC-3b, 机械单测)
  - [ ] **真 snapshot 集成测试**: `four_dim_status` 喂真 snapshot 逐字段非空断言 (非手造 fixture, AC-7)

#### TASK-004: consistency_check.py 字段修正 + 真 adapter 测试 [R1 Critical C-1]
- **Description**: `consistency_check.py` **字段漂移修正**: `openspec.active_changes`→`openspec.changes` (class-1); `upm.in_progress_change_ids` 在 Aria 自身**不存在** → class-2 显式标 **fixture-only + 第三方 manual** (不静默 no-op, 注释说明该维需 UPM in-progress 字段, 当前 schema 无)。4 类 advisory flag exit 0 + committed fixture。
- **Complexity**: S | **Estimated**: 0.5h | **Dependencies**: TASK-003 | **Agent**: backend-architect
- **Acceptance**:
  - [ ] `data_from_snapshot` 跑**真 snapshot** 集成测试: class-1 active_ids 提取非空 (字段修正后), 非 no-op (AC-4 adapter 子项)
  - [ ] class-2 显式标 fixture-only (非静默退化); 4 类 fixture 命中 exit 0 (AC-4); drift guard 逐字段 (AC-7)

#### TASK-005: §8 memory 枚举 + step2 主动提炼 (复用 + 新)
- **Description**: 照搬 §8 memory 枚举 (mtime>started_at) + §4 audit 洞见; **新增** session-closer step2 主动审视对话提炼**未写下**的值得固化经验 → 候选 memory (非仅枚举既有)。
- **Complexity**: S | **Estimated**: 0.5h | **Dependencies**: TASK-002 | **Agent**: backend-architect
- **Acceptance**:
  - [ ] §8 枚举 fixture (固定戳) count=2+表 (AC-5)
  - [ ] step2 有主动提炼段, 非仅枚举既有文件 (AC-5b)

### Phase 3: context 触发器 (复用前序)

#### TASK-006: closeout_trigger.py 照搬 (复用)
- **Description**: 照搬 `closeout_trigger.py` (按 source 分流 `used_percentage`/`_proxy` 不混用 + 未交接信号 → advisory nudge) + 5 档单测。
- **Complexity**: S | **Estimated**: 0.3h (照搬验证) | **Dependencies**: TASK-005 | **Agent**: backend-architect
- **Acceptance**:
  - [ ] 5 档 + 口径不混用 + unavailable 不报错 (AC-6)

#### TASK-007: phase-b/c context-monitor 接触发器 (复用)
- **Description**: 照搬 phase-b/c context-monitor step 的 closeout_trigger 钩子 (SKILL.md 编辑, 非 settings.json hook)。**路径重映射**: 旧钩子硬编码 `../session-closeout/scripts/closeout_trigger.py`→`../session-closer/scripts/closeout_trigger.py` (R1 K-3, 否则运行时 FileNotFoundError)。当前 master phase-b/c SKILL.md 落位 (verify 落点未被 v1.40-49 覆盖)。
- **Complexity**: S | **Estimated**: 0.5h | **Dependencies**: TASK-006 | **Agent**: tech-lead
- **Acceptance**:
  - [ ] `grep -n 'session-closer/scripts/closeout_trigger.py' phase-b-developer/SKILL.md` 命中 ==1 (路径已重映射, 无 `session-closeout` 残留)
  - [ ] phase-b/c step 显式调 trigger; 阈值 surface, 正常静默; 不引入 settings.json hook
  - [ ] manual acceptance 验 occupancy≥阈值确实 emit (不凭文字 review)

### Phase 4: 文档 + Rule #6 + 发版

#### TASK-008: 规范/文档同步 + 消歧锚 (AD-3) [R1 K-1/K-5]
- **Description**: `standards/conventions/session-handoff.md`: **重写 §2.2.1** (按独立 leaf skill 架构, **非旧 closeout_only 委托描述** — 旧版被否决, K-1) + **新增「周期收尾 (Phase D) vs 会话收尾 (session-closer)」消歧节 + 消歧矩阵** (第三方 load-bearing); CLAUDE.md nav + 两种收尾 note + **Rule #9 L5 补 session-closer 作第二 handoff enforcement 路径** (K-5); phase-d-closer ↔ session-closer 互引; Parent US 锁定 (US-010~019)。
- **Complexity**: M | **Estimated**: 0.8h | **Dependencies**: TASK-002b, TASK-004, TASK-006 | **Agent**: knowledge-manager
- **Acceptance**:
  - [ ] §2.2.1 重写 (grep 不含 `closeout_only` 委托措辞); standards 含消歧节 + 矩阵 (AC-9b/c)
  - [ ] `grep -c 'session-closer' CLAUDE.md` ≥3 (nav + 两种收尾 note + Rule #9 L5); Rule #9 L5 含 session-closer 路径 (K-5)
  - [ ] 架构文档与代码同步 (Rule #3); Parent US 回填 frontmatter

#### TASK-009: Rule #6 capability AB benchmark (D5)
- **Description**: Rule #6 **两段** (R1 M-2 拆分): **(a) deterministic** 触发命中率 — AC-9 消歧矩阵词实测路由正确 (机械, 硬门); **(b) capability** `/skill-creator` with/without AB 测内省完整性 (catch 未完成线程+未固化经验), 归 capability-class metric。**in-repo delta 可能 ≤0 仍可 ship** (旧实证 delta=0, 保守下界), 凭 owner sign-off 判正向价值, **不设 delta≤0 硬 FAIL 门** ([[feedback_goal_hook_precondition_must_be_in_session_achievable]])。结果存 `aria-plugin-benchmarks/ab-results/`。
- **Complexity**: M | **Estimated**: 1-1.5h | **Dependencies**: TASK-002, TASK-007 | **Agent**: qa-engineer
- **Acceptance**:
  - [ ] (a) 触发命中率: 消歧矩阵词路由正确 (deterministic, AC-9c/AC-10a)
  - [ ] (b) capability AB 跑出 + owner sign-off (delta≤0 不阻塞 ship, AC-10b)

#### TASK-010: 版本发布 v1.50.0 (MINOR)
- **Description**: **已 cat plugin.json 复验: 当前 v1.49.0 → v1.50.0** (旧写 v1.40.0 作废)。6 面 SoT: plugin.json + marketplace.json (version+plugins[].version+**user-facing Skills count +1**) + VERSION + CHANGELOG + README + 主仓 /VERSION。merge 顺序 standards → aria → 主仓 gitlink (子模块先于父, [[feedback_sequenced_multirepo_gitlink_bump]])。Phase C.2.5 多远程推送 (Forgejo+GitHub)。**ship 前再 re-check 版本防并发抢占**。
- **Complexity**: M | **Estimated**: 1h | **Dependencies**: TASK-008, TASK-009 | **Agent**: tech-lead
- **Acceptance**:
  - [ ] 6 面版本字面一致 (grep 验, 不信 commit msg)
  - [ ] marketplace.json Skills count = ship 时现值 +1 (jq/grep 验)
  - [ ] 双远程 parity 验证

---

## Execution Order

```
TASK-000 ──▶ TASK-001 ──▶ TASK-002 ──┬──▶ TASK-002b ──────────────┐
                                      ├──▶ TASK-003 ──▶ TASK-004 ──┤
                                      └──▶ TASK-005 ──▶ TASK-006 ──▶ TASK-007 ──┐
                                                                                │
                                            TASK-008 ◀──────────────────────────┤
                                            TASK-009 ◀──────────────────────────┘
                                                │
                                                ▼
                                            TASK-010
```

---

## Risk Assessment

| Risk ID | Description | Level | Mitigation |
|---------|-------------|-------|------------|
| R1 | context occupancy `used_percentage` vs `_proxy` 混用 | P1 | source 分流 + AC-6 口径 fixture |
| R2 | phase-d D.3 输出被误伤 | P1 | **R1 修正**: D.3 + ref 完全不动, 仅 description 收紧; AC-8a git diff 验 D.3 段零 diff |
| R3 | 一致性校验器误报 | P2 | advisory exit 0 + committed fixture |
| R4 | **复用脚本字段漂移 (已确认非假设, R1 C-1/C-2)** | **P1** | TASK-003/004 字段修正 (cycle_number→current_cycle / active_changes→changes / in_progress_change_ids fixture-only) + 真 snapshot 集成测试 (非手造 fixture 假绿) |
| R5 | session-closer ↔ phase-d-closer 触发撞车未根治 | P1 | AD-3 description 收紧 + standards 锚 + AC-9 三重验 (grep + 消歧节 + benchmark 准确率) |
| R6 | autofill 覆写 owner 已手填段 | P2 | idempotent write (仅未替换 placeholder) |
| R7 | 并发 session 同名 handoff 碰撞 | P2 | slug 唯一 + collision 检测 (共享 ref 含) |
| R8 | 出现第二份 handoff-write ref (drift 源) | P1 | **R1 Critical 修正**: 复用既有 `handoff-mechanics.md` 不新建; AC-11 grep 验仓库仅一份 + 两处引用同一文件 |
| R9 | 对话内省 capability AB in-repo 稀释 (旧实证 delta=0) | P2 | 接受保守下界, 跨项目价值更高 ([[feedback_process_vs_content_skills]]) |

---

## Progress Tracking

| Task | Status | Assignee | Started | Completed |
|------|--------|----------|---------|-----------|
| TASK-000 | Pending | tech-lead | - | - |
| TASK-001 | Pending | knowledge-manager | - | - |
| TASK-002 | Pending | knowledge-manager | - | - |
| TASK-002b | Pending | knowledge-manager | - | - |
| TASK-003 | Pending | backend-architect | - | - |
| TASK-004 | Pending | backend-architect | - | - |
| TASK-005 | Pending | backend-architect | - | - |
| TASK-006 | Pending | backend-architect | - | - |
| TASK-007 | Pending | tech-lead | - | - |
| TASK-008 | Pending | knowledge-manager | - | - |
| TASK-009 | Pending | qa-engineer | - | - |
| TASK-010 | Pending | tech-lead | - | - |

---

## Notes

- 本 Spec supersedes `session-closeout-internalization`; 复用其 3 脚本/3 测试/benchmark 方法; 改入口架构 (leaf + 共享原语 + 对话内省优先) per DEC-20260625-001。
- A.3 agent 分配见 Progress Tracking Assignee 列 (无新 agent, 现有 roster 覆盖)。
- TASK-009/010 Rule #6 + 版本规范强制项, 不可跳过 (新 Skill)。
- Phase D.2 归档前锁定 Parent US (TASK-008 checklist)。
- 旧 3 feature 分支 (b398557/776e140/f7b7f42) 保留归档 trail, 不合并不删 (owner 后续清理)。
