# session-closer 综合方案 — 会话收尾正交仪式 (独立 leaf skill + 共享 handoff-write 原语)

> **Level**: 3 (Full — 1 net-new leaf skill + 共享 handoff-write canonical 原语 + phase-d description 收紧 + 复用机械采集/校验/触发器 + 对话内省 capability)
> **Status**: ✅ **Approved** (Phase A.2 CONVERGED 2026-06-25 via R1→R2; **post_spec R1 REVISE×3 → Rev1 全落地 → R2 PASS×3 unanimous** [2 Critical: 既有 handoff-mechanics.md 复用 / collector 字段漂移修正; 4 Major: §2.2.1 重写·AC-8 机械化·消歧矩阵·路径重映射; 5 Minor 全 CLOSED; R2 二次核实字段漂移事实非 paper-fix]; ready for Phase A.3 → Phase B.1)
> **Change ID**: `session-closer-synthesis`
> **Supersedes**: `session-closeout-internalization` (Approved, Phase B 9/10, 搁浅未 ship — 本 Spec 据 DEC-20260625-001 架构修订, 复用其 ~70-80% 实现)
> **Brainstorm Source**: [.aria/decisions/DEC-20260625-001-session-closer-synthesis.md](../../../.aria/decisions/DEC-20260625-001-session-closer-synthesis.md) (5 决策收敛; 承接 DEC-20260605-001 轴 2)
> **Parent US**: 待分配 — "对话管理流程 / handoff 强化" (US-010~019 区间); 暂以 DEC 为锚 (D.2 归档前锁定, TASK-008 checklist 项)
> **Authored by**: Claude Opus 4.8 via `aria:phase-a-planner` + `aria:spec-drafter`, 2026-06-25
> **Effort baseline**: ~5-6.5h (cherry-pick 重组 ~1h + handoff_autofill adapter 重建 ~1.5-2h [R1 M-1] + 复用既有 ref audit ~0.5h + leaf 重写 ~2h + 消歧 ~0.5h + capability AB ~1-1.5h + 发版 ~1h); 复用旧 3 脚本+3 测试省 ~3h
> **ship_target**: aria-plugin **v1.49.0 → v1.50.0** (MINOR, 新 skill; 旧 spec 的 v1.40.0 已过期, 已 cat plugin.json 复验 2026-06-25)

---

## Why

Aria 十步循环成熟, 但**缺会话维度的收尾仪式**。owner 在第三方项目输入 "执行对话收尾", 期望走 5 步会话收尾 (0 本地/远程同步 / 1 未完成任务讨论 / 2 待固化经验 / 3 UPM·US·Spec·PRD 四维一致 / 4 收尾+交接), 但实际命中**十步循环 Phase D** (phase-d-closer)。三处根因:

1. **会话收尾被建模为周期收尾的子模式 (概念缺口)**: 前序 Spec `session-closeout-internalization` 把会话收尾做成 phase-d-closer 的 `closeout_only` flag。这是 leaky abstraction —— 会话 (可含 0..N 个 cycle + 探索/讨论) 与开发周期是**不同工作单元**, 强行同构使 session 级关注点渗进 cycle 收尾器。

2. **trigger 撞车未根治 (owner 核心痛点)**: 正因 phase-d-closer 仍当 handoff 引擎, 它的 description 摘不掉「收尾 / 写 session handoff」卖点 (实测前序 feature 分支与 master 一字不差)。→ "执行对话收尾" 仍命中 phase-d。

3. **对话内省被降级 (owner 真实诉求被弱化)**: owner step 1/2 字面是「查看当前对话」= 对话内省, 但前序 Spec AC-3 把「对话上下文」标 best-effort 不计入 falsify, 机械 autofill 才是承重。owner 最在意的那部分被机械化掉了。

**综合方案** (DEC-20260625-001): 独立 **leaf skill** (概念干净 + 正交平级) + **共享既有 `phase-d-closer/references/handoff-mechanics.md` canonical 原语** (中和 DRY 顾虑, phase-d 与 session-closer 都引用同一既有文件不复制; R1 修正: 该 ref 已存在非新建) + **AI 对话内省优先, 机械 autofill 兜底** (对话一等公民 + 机械可靠性) + **description 收紧 + standards 消歧锚** (第三方 load-bearing)。复用前序 ~70-80% 实现 (3 脚本 + 3 测试 + benchmark 方法与入口架构无关)。

---

## What

### In scope

#### A. 独立 leaf skill `session-closer` (D1 + D3, ~2h)

**Target**: `aria/skills/session-closer/SKILL.md` (NEW)。user-facing 入口, 强绑会话触发词: "对话收尾" / "执行对话收尾" / "session closeout" / "收尾这次对话" / "写交接" / "收工" / "close out"。

**职责 = 自有编排 (不路由穿过 phase-d-closer)**, 顺序体现 D3「对话内省优先 + 机械兜底」:
1. **step 1/2 (AI 内省, 一等公民)**: AI 审视**本对话** → ① 未闭合线程/待办 (step 1) ② 值得固化但未写下的经验 (step 2, 主动提炼非仅枚举)。
2. **step 0/3 (机械交叉核验兜底)**: 跑 `handoff_autofill.py` (§7 sync / §2 / §5) + `consistency_check.py` (四维 flag) → **交叉核验**: snapshot 有但 AI 内省没提的 (followups / carry_forward / uncommitted / 四维不一致) → flag 为「机械补漏」。
3. **step 4 (写 handoff)**: 按既有 `phase-d-closer/references/handoff-mechanics.md` (B, 共享 SOT) 写 `docs/handoff/{date}-{slug}.md` (复用 9 段模板 + latest.md 指针 + Rule #9 L1/L5)。
4. **终结 (leaf)**: 写完即止, **绝不调** phase-a/b/c/d / workflow-runner / openspec-archive。若 step 3 发现"有 shipped 未归档 cycle" → **仅 surface + 提议** "可另跑 Phase D 归档", 不自动执行 (advisory-over-hardlock)。

#### B. 共享 handoff-write canonical 原语 = 复用既有 ref (D1, ~0.5h) [R1 Critical 修正]

**事实核实 (R1)**: `aria/skills/phase-d-closer/references/handoff-mechanics.md` **已存在** (6808 字节, 含 9 段模板 variable 字典 / latest.md 2 子步骤 + 3-row decision table / Rule #9 L1+L5 落点 / slug 规则 / Forbidden patterns), 且 phase-d-closer SKILL.md L161 **已引用它**。D.3 **不是内嵌待提炼**, 而是早已引用一份既有 ref。原 proposal「新建 + 提炼」前提错误 (起草未 recon, [[feedback_recon_real_code_before_implementing_spec_test_suite]])。

**修正方案 (C)**: **canonical SOT = 既有 `phase-d-closer/references/handoff-mechanics.md`, 不新建、不搬移、不复制**。
- phase-d-closer D.3 **完全不动** (仍引用同一 ref, byte 不变 → AC-8 trivially 成立)。
- session-closer step 4 **交叉引用同一份既有 ref** (leaf → 共享机制文档; 依赖方向正确: 不是 phase-d 反向引用 leaf)。
- TASK-001 = audit 既有 ref 是否覆盖 session-closer 所需机制; **若有缺口仅 additive 补段** (既有锚点不删不改); 让 session-closer 引用它。
- 该 ref 历史上位于 phase-d-closer namespace, 但语义上是**共享 handoff-write 机制 SOT** (文档内加一行说明); 不为消除"归属感"而搬移 (搬移需改 phase-d L161 引用, 引入回归风险, 收益不抵)。

#### C. phase-d-closer description 收紧 (D4 消歧, ~0.3h)

`phase-d-closer/SKILL.md` description 中度 rebind: 删「写 session handoff」+ 裸「收尾」, rebind 到 cycle-explicit: 「Phase D / 周期收尾 / 归档 Spec / 更新 cycle 进度」。**不改任何执行逻辑**, 纯 description 字面。

#### D. 机械采集/校验/触发器 (复用前序 + 字段漂移修正, D2 cherry-pick) [R1 Critical 修正]

cherry-pick 前序实现, 但 **R1 实测 (跑旧测试 + 查真 snapshot) 发现 3-4 处字段漂移** (v1.39→v1.49), 旧测试手造 fixture 绕过真 adapter → **假绿**。必须修正 + 加真 snapshot 集成测试:

| 脚本 | 漂移字段 | 旧读 (错) | 当前真值 | 后果 |
|------|---------|----------|---------|------|
| `consistency_check.py` | openspec | `openspec.active_changes` | `openspec.changes` (openspec.py:273) | class-1 提取 active_ids 全失效 → no-op |
| `consistency_check.py` | upm | `upm.in_progress_change_ids` | **不存在** | class-2 advisory 永不触发 |
| `handoff_autofill.py` | upm | `upm.cycle_number` | `upm.current_cycle` (upm.py:391) | §5 UPM.cycle 永 None |
| `handoff_autofill.py` | openspec | `carry_forward_inventory` 当 list 遍历 | dict `{total,active_change_count,by_change}` | 遍历 dict keys 产垃圾 |

照搬件 (修正后):
- `handoff_autofill.py` — **R1 M-1: 无 snapshot adapter/main, 解析编排层原在被弃薄入口 prose 里, 需重建** + 3 处归一化 (sync_status 嵌套路径 / carry_forward dict→list via by_change / followup dict→可读 item) + `current_cycle` 修正; 接入 (A) step2 补漏语义。
- `consistency_check.py` — `active_changes`→`changes` 修正; `in_progress_change_ids` 在 Aria 自身无此维 → 显式标 fixture-only + 第三方 manual (不静默 no-op); 4 类 advisory flag exit 0。
- `closeout_trigger.py` — 接口零漂移 (token-telemetry 字段稳定), 照搬; 按 source 分流 `used_percentage`/`_proxy` 不混用。
- `phase-b/c` context-monitor step 接 trigger (SKILL.md 编辑, **含路径 `session-closeout`→`session-closer` 重映射**)。
- `§8 memory 枚举` + `§4 audit 洞见` (D.post 可选)。

> **强制**: cherry-pick 件须对 `data_from_snapshot` / `four_dim_status` 跑**真 snapshot 集成测试** (非手造 fixture), 逐字段断言提取非空, 把 falsify 边界从纯函数推到 adapter (AC-7 子项)。

#### E. 文档 + 消歧锚 (D4, ~0.5h)

- `standards/conventions/session-handoff.md`: §2.2.1 按需会话收尾入口 (复用前序) + **新增「周期收尾 (Phase D) vs 会话收尾 (session-closer)」消歧节** (跨项目 load-bearing)。
- `CLAUDE.md`: nav + 「两种收尾」note (Aria 自用)。
- phase-d-closer ↔ session-closer 互引。

### Out of scope

| ID | 描述 | drop 理由 |
|----|------|----------|
| OOS-1 | phase-d-closer `closeout_only` 模式 | D1 决策删除 — session-closer 独立, 不再借道 phase-d |
| OOS-2 | 自动执行收尾 (无 owner 确认即 commit) | advisory-over-hardlock |
| OOS-3 | 自动修复四维不一致 | 校验器只 flag (OOS, 修复是 owner/后续) |
| OOS-4 | 改 9 段模板结构 / Rule #9 五层 enforcement | 纯增量复用, 不动既有契约 |
| OOS-5 | 跨 session resume / 自主多 task 编排 | DEC-20260605-001 轴 3, 独立 Spec |
| OOS-6 | 新建 state-scanner collector | probe 已证数据源齐备, 消费而非新增 |
| OOS-7 | rebase/合并前序 3 feature 分支 | D2 决策 cherry-pick 重组; 旧分支保留为归档 trail |
| OOS-8 | DEC-20260605-001 轴 1 (agent 补全) | 独立未来工作 |

---

## Constraints

- **概念正交**: session-closer 是与十步循环平级的会话仪式, leaf, 不路由穿过 phase-d, 不拖入 cycle。
- **共享原语单一 SOT**: handoff-write 机制**引用不复制** (既有 `phase-d-closer/references/handoff-mechanics.md`); structural test 守 drift。
- **对话内省一等公民**: step 1/2 AI 内省优先; 机械 autofill 是 backstop (补漏), 非承重。
- **第三方消歧 load-bearing**: description + standards (第三方不加载 Aria CLAUDE.md); CLAUDE.md 仅自用。
- **两种收尾职责边界 (R1 Major)**: cycle 内 handoff (走完 D.2 归档后) 仍由 phase-d-closer D.3 承担; session-closer 服务**无 active cycle 的纯会话收尾** (探索/调试/讨论 session 或 cycle 之外)。易混词 (写 handoff / 写交接 / 收工) 由消歧矩阵 (AC-9) 裁定期望命中。
- **advisory-over-hardlock**: 触发器/校验器/未归档 cycle 提议均 advisory, 不硬 block (承袭 v1.37.0 #133)。
- **向后兼容**: phase-d-closer description 收紧 + D.3 改引用 ref, **不改 D.1/D.2/D.3 byte 行为** (AC-8 回归)。
- **context 口径不混用**: `used_percentage` (relay) vs `used_percentage_proxy` (transcript) 按 source 严格分流。
- **Python 3.9+ stdlib only** / **幂等写入** (仅写未替换 placeholder) / **并发写安全** (slug 唯一 + collision 检测)。

---

## Assumptions (Phase B kick 前 verify, [[feedback_per_spec_assumption_recheck]])

| # | 假设 | 验证 |
|---|------|------|
| A-1 | snapshot 含 `upm.followups[]` | grep `followups` collectors/upm.py |
| A-2 | snapshot 顶级 `sync_status` (ahead/behind), `multi_remote` 嵌套其内 | grep collectors; 已验证 0 漂移 |
| A-3 | `aria-token-telemetry` 返回 `source`/`used_percentage(_proxy)` | 跑 token_telemetry.py 出 JSON |
| A-4 | **既有** `phase-d-closer/references/handoff-mechanics.md` 覆盖 session-closer 所需机制 (否则 additive 补) | **已核实存在** (6808B, D.3 L161 引用); TASK-001 audit 缺口 |
| A-5 | memory 目录 `~/.claude/projects/*/memory/*.md` 可解析 | ls 可达 |
| A-6 | `openspec.carry_forward_inventory` 仍产出 (dict 形态, 非 list) | 已验证: snapshot 在, dict `{total,active_change_count,by_change}` |
| A-7 | **(修正)** 前序脚本接口**部分漂移** (非零漂移): sync_status/multi_remote/requirements 兼容; upm(2)+openspec(2) **4 处漂移** (见 §D) → cherry-pick 必修正 + 真 snapshot 集成测试 | R1 实测: 旧测试假绿 (手造 fixture 绕 adapter), C-1/C-2 confirmed |

---

## How

### 技术路径

```
   owner: "对话收尾"/"执行对话收尾"        phase-b/c context-monitor 消费点
            │                                     │ (occupancy≥阈值 + 未交接)
            ▼                                     ▼
   aria:session-closer (独立 leaf)         closeout_trigger.py → advisory nudge
            │
            ├── step1/2: AI 内省本对话 → 未完成线程 + 待固化经验   ← 一等公民
            ├── step0/3: handoff_autofill + consistency_check
            │            → 机械交叉核验: snapshot 有但 AI 没提 → 补漏 flag   ← backstop
            ├── step4: 按既有 phase-d-closer/references/handoff-mechanics.md 写 docs/handoff/
            └── 终结 (leaf; 发现未归档 cycle → 仅 surface 提议, 不自动调 phase-d)

   phase-d-closer D.3 ──► 同一既有 handoff-mechanics.md (canonical SOT, 不动)
   closeout_only: 删除 | phase-d 仅 description 收紧 (D.3 + ref 完全不动)
```

### 关键设计决策

| ID | 主题 | 决策 (DEC-20260625-001) |
|----|------|------|
| AD-1 (D1) | 结构基石 | **独立 leaf skill + 共享 ref canonical 原语**; 删 closeout_only。session-closer 自有编排不穿 phase-d; handoff-write 单一 SOT = **既有 `phase-d-closer/references/handoff-mechanics.md`, 引用不复制不搬移** (R1 修正)。否决「薄入口委托」(前序 AD-1) — 它致 trigger 撞车未根治。 |
| AD-2 (D3) | 结合模型 | **AI 内省优先 + autofill 机械兜底**。对话 awareness 一等公民; 机械 = 补漏 backstop (snapshot 有但 AI 没提 → flag), 非承重。否决前序「机械承重 + 对话 best-effort」。 |
| AD-3 (D4) | trigger 消歧 | **中度 description rebind + standards 锚 + 消歧矩阵**。phase-d 删「收尾/handoff」裸词; session-closer 强绑会话; standards 加消歧节; **易混词 (写handoff/写交接/收工) 消歧矩阵** (R1 Major); cycle 内 handoff 仍归 phase-d D.3, session-closer 服务无 active cycle 的纯会话收尾。第三方 load-bearing = description + standards。 |
| AD-4 | 触发器/校验器 | **advisory, 不阻塞** (承前序 AD-2/3)。按 source 分流字段不混用。 |
| AD-5 (D5) | Rule #6 benchmark | **capability AB 重跑 + deterministic 拆分** (R1 M-2)。旧 +28.5% (thin-entry 机械重心) 不可迁移; 新重心=对话内省。AC-10 拆: deterministic 触发命中率 (机械可验) + capability owner sign-off (in-repo delta 可能 ≤0 仍可 ship, 保守下界, **不设 delta≤0 硬 FAIL 门** 避不可达前置 [[feedback_goal_hook_precondition_must_be_in_session_achievable]])。 |
| AD-6 (D2) | 分支策略 | **cherry-pick 重组到当前 master 新分支** (弃 closeout_only/薄入口包袱); 含 `session-closeout`→`session-closer` 路径重映射 (R1 Major)。旧 3 feature 分支保留归档 trail。 |

---

## Acceptance criteria

全部 binary-falsifiable ([[feedback_falsifiable_evidence_for_binary_acceptance]])。**继承**前序 AC-2/4/5/6/7 (复用脚本), **新增/改** AC-1/1b/3/3b/5b/8/9/10。

### AC-1 — 独立 leaf skill 可调 (不路由 phase-d)
`session-closer/SKILL.md` 存在; "对话收尾" 调用 → 走 session-closer **自有 handoff-write 编排** (引用 ref), **不执行** D.1 progress-update / D.2 archive / 不路由穿过 phase-d-closer。falsify: 触发了 D.2 归档 或 调用了 phase-d-closer → FAIL。

### AC-1b — leaf 终结 (不拖入十步循环)
session-closer 不调 phase-a/b/c/d / workflow-runner / openspec-archive。发现未归档 cycle → 仅输出 advisory 提议, 不自动执行。falsify: 自动触发任一 phase skill → FAIL。

### AC-2 — §7 git 同步自动填 + 告警 (继承, reuse handoff_autofill)
fixture: 本地 ahead origin 1。closeout → §7 含真实 SHA + parity + 告警行。falsify: §7 仍 placeholder 或无告警 → FAIL。

### AC-3 — §2 未完成: AI 内省优先 (改 — 对话一等公民)
session-closer 先 AI 内省本对话出未完成线程 (load-bearing, 非 best-effort), 写入 §2。falsify: §2 缺对话内省段 (仅机械来源) → FAIL。

### AC-3b — autofill 交叉核验补漏 (新, AD-2; R1 Minor 改为机械静态输入对)
**机械可证伪 (脱离 "AI 故意遗漏" 的不确定性)**: 给定静态输入对「snapshot 有 followup X + 已写入 §2 草稿不含 X」→ autofill 补漏函数必须 flag X 为「机械补漏」。纯函数单测 (与 deterministic 脚本测试同构, Rule #6 structural substitute)。owner-facing 的「AI 内省优先」语义由 AC-10 capability 承载, 两者分层。falsify: 输入对中 snapshot 有但 §2 草稿无的项未被 flag → FAIL。

### AC-4 — 一致性校验器 4 类 advisory flag (继承, reuse consistency_check)
`consistency_check.py` 跑 4 committed fixture (cycle↔archive / active↔UPM / 高优US↔§2 / PRD broken ref), 各命中, exit 0。falsify: 漏报 或 非 0 退出 → FAIL。

### AC-5 — §8 memory 枚举 (继承, reuse)
fixture: 2 新 memory (mtime+started_at 固定戳)。closeout → §8 count=2 + 文件表。falsify: count≠2 → FAIL。

### AC-5b — step2 对话内省主动提炼经验 (新, owner step2; R1 Minor 加结构钩子)
session-closer step2 输出**必须含结构标记段** `[候选 memory]` / `[未写下经验]` (审视本对话识别未写下的值得固化经验, 非仅枚举既有文件)。该结构检查纳入 AC-7 drift guard (机械: grep 标记段存在)。内省**质量** (提炼得准不准) 属 capability, 由 AC-10 AB 承载 — AC-5b 仅验**结构存在**, 不验质量 (避与 AC-10 边界模糊)。falsify: step2 输出无 `[候选 memory]`/`[未写下经验]` 标记段 → FAIL。

### AC-6 — context 触发器 5 档 + 口径不混用 (继承, reuse closeout_trigger)
relay 90%+uncommitted → nudge; 50% → 静默; 90% 无未交接 → 静默; 第三信号独立 → nudge; `source=unavailable` → 静默 exit 0; `transcript_fallback` 只读 `_proxy`。falsify: 任一档错 或 混用字段 → FAIL。

### AC-7 — 测试覆盖 drift guard (继承, reuse + 新增 leaf 测试)
`tests/` 校验器 + 触发器 + 填充单测跑 committed canonical, 逐字段匹配。falsify: 任一字段偏差 → FAIL。

### AC-8 — phase-d-closer 向后兼容 (改 — 机械可证伪, R1 Major)
**两层机械验证** (替换不可证伪的「byte 行为不变」措辞):
- (a) `git diff` phase-d-closer/SKILL.md = **仅 description 段变化** (删裸「收尾/handoff」词), D.1/D.2/D.3 action 描述文本零 diff (D.3 仍引用同一既有 ref, 不动)。
- (b) 既有 `handoff-mechanics.md` 若被 TASK-001 补段则**additive-only**: grep 既有锚点 (9 段 variable 字典 / latest.md 2 子步骤 / Forbidden patterns) 仍在, 无删改。
falsify: phase-d D.1/D.2/D.3 action 文本有 diff, 或既有 ref 锚点被删改 → FAIL。

### AC-9 — trigger 消歧可验 (新, AD-3, owner 核心痛点; R1 Major 加消歧矩阵)
(a) `grep` phase-d-closer description **不含**「写 session handoff」与裸「收尾」(已 rebind cycle-explicit); (b) standards 含「周期收尾 vs 会话收尾」消歧节; (c) **消歧矩阵**: 列至少 5 个触发词的期望命中 skill + 理由 —

| 触发词 | 期望命中 | 理由 |
|--------|---------|------|
| "对话收尾" / "执行对话收尾" / "会话收尾" / "收工" | session-closer | 纯会话语义 |
| "Phase D" / "归档 Spec" / "周期收尾" | phase-d-closer | cycle 语义 |
| "写交接" / "写 handoff" | **session-closer (默认)** | 收紧后 phase-d 不再宣传; cycle 内由 phase-d D.3 自动承担 (用户不显式调) |
| "收尾阶段" | phase-d-closer | 保留「阶段」=Phase 语义 |

(d) benchmark (AC-10) 触发命中率覆盖上述**易混词** (非仅「对话收尾」)。falsify: 任一不满足, 或矩阵词实测命中错 skill → FAIL。

### AC-10 — Rule #6 benchmark: deterministic + capability 两段 (改, D5; R1 Major 拆分诚实化)
**(a) deterministic 段 (机械可验, 硬门)**: 触发命中率 — AC-9 消歧矩阵词实测路由正确 (session-closer 词 → session-closer, 非 phase-d)。falsify: 命中错 → FAIL。
**(b) capability 段 (AI-judgment, owner sign-off)**: `/skill-creator` with/without AB 测「内省完整性」(catch 未完成线程 + 未固化经验)。归类 **capability-class metric** (非 deterministic)。**in-repo delta 可能 ≤0 仍可 ship** (旧实证 delta=0, in-repo 对 process skill 是保守下界 [[feedback_process_vs_content_skills]]); 凭 owner sign-off 判正向价值, **不设「delta≤0 即 FAIL」硬门** (避不可达前置自锁 [[feedback_goal_hook_precondition_must_be_in_session_achievable]])。脚本 deterministic 单测照搬 (非 AB, 属 AC-7)。falsify: (a) 触发命中错, 或 (b) owner 未 sign-off → FAIL。

### AC-11 — 共享 ref 单一 SOT = 既有文件 (改, AD-1; R1 Critical)
canonical = **既有** `aria/skills/phase-d-closer/references/handoff-mechanics.md` (不新建第二份); phase-d D.3 (L161) + session-closer step4 均**引用同一份** (grep 验两处引用 `handoff-mechanics.md`); 仓库内**无** `handoff-write-mechanics.md` 或其他第二份 handoff-write ref。falsify: 存在第二份 handoff-write ref 文件, 或任一处复制机制而非引用 → FAIL。
