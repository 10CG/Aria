# Proposal: a1-entry-claim-duplicate-work-guard

> **Status**: 📝 **Draft (A.1)** — 待 post_spec 闸门 (见文末「闸门待裁」)
> **Created**: 2026-07-30
> **Spec Level**: 2 (单域 — 把已 ship 的 claim 机制的调用点从 Phase B 前移到 A.1; 无新机制)
> **触发**: owner 2026-07-30 「接受方法论建议」—— 源于 aria-plugin #122 双 Spec 碰撞 (两轨互不知情各跑 4 轮 post_spec, 合计 10 轮 / 33+ agent 实例)
> **⚠️ 本 Spec 修正了触发它的那条建议本身** — 见 §Why「原建议为何无效」
> **代码落点**: `aria/` 子模块 (`skills/phase-a-planner/` + `skills/audit-engine/`); Spec 落主仓 (Rule #5)
> **ship target**: aria-plugin v1.66.0 (MINOR — SKILL.md 指令面扩展)

---

## Why

### 症状 (实证: aria-plugin #122, 2026-07-25~27)

两个容器 (`aria-runner-bot/023236f2` 与 `simonfishgit`) 对**同一个 issue** 各自起草了一份 Spec, 核心设计同构, 各跑满 4 轮 post_spec。第二份 (`R`) 于 07-27 11:52 落地远端时, 第一份 (`L`) 已跑完 10 轮闸门并写完 handoff — 双方全程互不知情。

**代价**: L 侧 10 轮 / 33 agent 实例 + R 侧 4 轮 / 13 agent 实例, 其中一整份的 Phase A 成为重复劳动。

**这是 memory `feedback_concurrent_duplicate_audit_fetch_before_start` 的第四次实证** (前三次: #133 / 2026-07-11 secret-guard 一 session 三重复现)。前三次的处置都是「记住要重扫」—— 纯纪律, 没有机械化, 所以复发。

### 根因: 闸门审产物质量, 不审产物是否该存在

L 的 proposal 头部写着「关联 Issue ... **无 in-flight — 本地 fetch + Forgejo API 双核实**」。这个核实**做过, 且当时是对的** —— 它发生在 2026-07-25 起草时, 而 R 在 07-27 才创建。

10 轮闸门 (post_spec ×4 + post_planning ×6) 的入口断言里, **没有任何一条问过「远端是否已出现同 issue 的竞品 Spec」**。闸门的 SCOPE_OK / anchor 固化都是在审**这份产物做得对不对**, 从不问**这份产物该不该存在**。

### ⚠️ 原建议为何无效 (本 Spec 的核心修正)

触发本 Spec 的原建议是:

> 在 `audit-engine` 的 post_spec 入口断言里加一条机械检查: 对 spec 的「关联 Issue」字段, fetch 后 grep `openspec/changes/*/proposal.md` 是否已有同 issue 引用。

**该建议在它要防的这次事故里会一无所获**:

| 时点 | L 在任一远端? | R 在任一远端? |
|------|--------------|--------------|
| L 跑 post_spec R1→R4 (07-25~26) | ❌ untracked | ❌ 尚未创建 |
| L 跑 post_planning R1→R6 (07-26~27) | ❌ untracked | ❌ 11:52 前不在 |
| R 跑 post_spec R1→R4 (07-27) | ❌ **L 全程零提交** | ❌ 11:52 前不在 |

两份 Spec 在各自审计的**全部时间里都是本地 untracked**。「grep 远端 spec 目录」这个判定机制, **它要判的输入在需要它的时刻不存在** —— 正是 memory `feedback_verify_predicate_inputs_exist` 的形状 (「审计判定机制必分两层: 逻辑对吗 + 它要判的输入真会被生成吗」)。

**claim 机制没有这个缺陷**: claim 由 `phase1_gate` **立即写并推到远端 coordination ref** (advisory 模式的定义即「放行 + 写推自己 claim + 返回 surface」), 不像 spec 文件能在本地躺两天。

### 已 ship 但接错位置的机制

`aria/skills/state-scanner/scripts/phase1_gate.py` 已支持 `--linked-issue`, 产出 `linked_issue_overlap[]` —— CLI help 原文: 「同 linked_issue 不同 track-id 的 active claim (advisory 告警, 不阻断)」。**这正是本问题的解**。

实测接线现状:

| Skill | 是否调 phase1_gate | 备注 |
|-------|-------------------|------|
| `phase-a-planner` (A.1-A.3) | ❌ **零调用** (grep 全文无命中) | ← 缺口 |
| `phase-b-developer` :88-93 | ✅ `--phase B` + `[--linked-issue]` **(可选)** | |
| `branch-manager` :149 | ✅ `--phase B --mode advisory` | |

⇒ 机制只在 **Phase B 入口**认领。而碰撞发生在 **A.1 起草**。L 的 handoff §6 把「经 phase1_gate 认领 `--linked-issue aria-plugin#122`」列为**未来的 Phase B 步骤** —— 两轨都没走到 Phase B, 所以谁都没认领过。

**反事实**: 若 L 在 07-25 A.1 时认领, R 在 07-27 起草时的 A.1 认领会返回 `linked_issue_overlap` 非空 ⇒ R 的整个 4 轮审计不会发生。

---

## What Changes

### 1. A.1 入口认领 (主机制)

`phase-a-planner` 在 **A.1 起草前**调用 phase1_gate 认领:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --raw-track-id "<spec-slug 或 handoff §6 carry-id>" \
  --phase A.1 \
  --mode advisory \
  --linked-issue "<repo>#<n>" \
  --repo-path "<repo root>"
```

- **`--phase` 是自由字符串** (CLI 无 `choices` 约束, 已核) ⇒ `A.1` 无需改 phase1_gate 代码。
- **`--linked-issue` 在 A.1 是条件必需**: spec 有「关联 Issue」字段时**必传**; 无关联 issue 的 spec (纯内部重构) 可省。与 Phase B 的「可选」不同 —— A.1 正是 issue 维度碰撞的发生点。
- **消费**: `linked_issue_overlap[]` 非空 ⇒ 在 A.1 起草**前**渲染 🔴 告警, 列出对方 track-id / owner-container / claimed_at, 并**要求 AI 先向用户报告再决定是否继续起草**。advisory 不阻断, 但**不得静默吞掉**。

### 2. audit-engine 每轮入口竞品扫描 (副机制, 覆盖不同盲区)

`audit-engine` Step 0 (anchor 固化) 旁加 **Step 0.5**: 每轮 (非仅首轮) 入口 fetch 后, 对本 spec 的「关联 Issue」grep 全部远端 ref 上的 `openspec/changes/*/proposal.md`。

- **新增** `aria/skills/audit-engine/scripts/sibling_spec_probe.py` (stdlib-only; audit-engine 目前零 `scripts/`, 本 change 新建该目录)。
- **每轮跑而非仅首轮** —— 本次事故里 R 恰好在 L 的最后一轮之后落地; 多轮审计跨小时甚至跨天, 首轮扫描不够 (同 memory 「每次实质动作前」而非「仅起点」)。
- **诚实声明其盲区 (不得当作主防线)**: 本机制只能看见**已 push 到远端的**竞品 spec。对方 spec 仍 untracked 时它一无所获 —— 这正是本次事故的实况。它覆盖的是**另一个**场景: 对方 spec 已落地但**没走 claim** (未用 phase1_gate / legacy 轨)。

### 3. 残余缺口 (成文, 不假装覆盖)

**两个机制都不覆盖**: 对方既未 claim 又未 push 的窗口。若两轨在同一小时内各自 A.1 起步且都尚未 claim 成功推远端, 仍会碰撞。

- 该窗口由 claim 的推送延迟界定 (秒级), 远小于本次的 2 天。
- 彻底消除需中心化 spec 登记表 (owner 未授权, **非本 Spec 目标**)。
- 按「no silent caps」原则显式记录, 不写进承诺面。

---

## 决策记录

| # | 决策 | 要点 |
|---|------|------|
| D1 | 主机制用**已 ship 的 claim**, 不新造检查 | claim 立即推远端, 结构上没有「本地躺两天」的盲区; 且 `linked_issue_overlap[]` 语义逐字对口 |
| D2 | A.1 的 `--linked-issue` **条件必需**, 非可选 | 与 Phase B 的可选不同 — A.1 是 issue 维度碰撞的发生点, 可选=多数人不传=机制空转 |
| D3 | 副机制**每轮**跑, 非仅首轮 | 本次事故 R 恰在 L 末轮后落地; 多轮审计跨天 |
| D4 | 副机制的盲区**写进 Spec 正文**, 不藏进脚注 | 假绿的反面是恒红, 但「以为覆盖了其实没有」比两者都糟 |
| D5 | 不做中心化 spec 登记表 | owner 未授权; 残余窗口秒级, 性价比不成立 |
| D6 | `--phase A.1` 不改 phase1_gate 代码 | 已核 CLI `--phase` 无 `choices` 约束 |

**Rule #6 (rule6_note)**: `phase-a-planner/SKILL.md` 与 `audit-engine/SKILL.md` 的改动均为**处方性·运行时指令面** (新增 AI 必须执行的步骤 + 告警消费义务) → 判据决策表第二行, **照跑 AB, 零裁量**。新增 `sibling_spec_probe.py` 为确定性代码 → 结构化测试覆盖 (SC-4~6), 与 AB 并行不互替。**不申请豁免。**

---

## Success Criteria

| SC | 场景 | 期望 |
|----|------|------|
| SC-1 | A.1 起草前, 同 issue 已有他轨 active claim | phase1_gate 返回 `linked_issue_overlap[]` 非空; AI **在起草前**渲染 🔴 告警含对方 track-id / owner-container / claimed_at |
| SC-2 | A.1 起草前, 同 issue 无他轨 claim | `linked_issue_overlap == []`; 正常起草; 本轨 claim 已写且已推 (`push_success` 真) |
| SC-3 | spec 有「关联 Issue」字段但调用未传 `--linked-issue` | **可红** — A.1 流程断言该参数在场 (条件必需的机械落实, 防退化成可选) |
| SC-4 | 副机制: 远端存在同 issue 的他名 spec 目录 | `sibling_spec_probe.py` 报告命中, 含对方目录名 + 所在 ref |
| SC-5 | 副机制: 远端无同 issue spec | 报告空, 退出码 0, 不阻断 |
| SC-6 | 副机制: fetch 失败 / 无远端 | **不静默** — 报告 `degraded` 且注明「本轮竞品扫描未执行」(零证据不得当正证据) |
| SC-7 | 反向对照 — 本轨自己的 spec 目录 | **不得**自命中 (排除自身 track-id / 自身目录) |

---

## 非目标

- 不做中心化 spec 登记表 (D5);
- 不把 advisory 升级为 block (advisory-over-hardlock 是既有设计立场, 正交);
- 不改 `phase1_gate` 自身代码 (只改调用点与调用参数);
- 不动 Phase B 入口现有认领 (它照旧, 本 change 只**新增** A.1 一处)。

---

## Impact

| 文件 | 变更 |
|------|------|
| `skills/phase-a-planner/SKILL.md` | A.1 入口新增认领步骤 + `linked_issue_overlap` 消费义务 → Rule #6 照跑 AB |
| `skills/audit-engine/SKILL.md` | 新增 Step 0.5 每轮竞品扫描 + 盲区声明 → Rule #6 照跑 AB |
| `skills/audit-engine/scripts/sibling_spec_probe.py` | **新增** (目录也新建) |
| `skills/audit-engine/tests/test_sibling_spec_probe.py` | **新增** (SC-4~7) |
| `skills/phase-a-planner/` 既有测试 | 扩展 (SC-1~3) |
| 发版 5 文件 + 主仓 gitlink | v1.66.0 MINOR |

---

## ⚠️ 闸门待裁 (Rule #10 — AI 不自行判定)

`.aria/config.json` 的 `audit.checkpoints.post_spec = "convergence"` **enabled**, 封闭豁免白名单四类无一适用 (非 config off / 无 adaptive_rules 映射 / 无成文 lane / 结构性前提成立 —— 审的对象即本 proposal)。⇒ **默认应跑 post_spec**。

同时: 本 session 硬约束「未经用户要求不得调用 Agent」与闸门执行相撞 (与 2026-07-27 session 同形状)。**两者均须 owner 显式裁, AI 不以任一方为由跳过另一方。**

**自指注记**: 本 Spec 若照自己的 §1 执行, A.1 起草前应先认领 `--linked-issue`。本次起草时 **该机制尚不存在** (这正是本 Spec 要建的), 故人工代偿: 已 fetch 双远程 + 核实 `openspec/changes/` 无同主题 spec (2026-07-30, 主仓 `4e034d2`, origin=github=`257a20d`)。
