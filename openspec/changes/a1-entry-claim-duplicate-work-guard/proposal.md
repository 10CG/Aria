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

### ⭐ 第五次实证 + 主机制 dogfood (2026-08-02 补, 起草后新增)

**第五次碰撞, 且这次最难辩解**: 本 Spec 于 2026-07-30 起草, 论点是「闸门审产物质量, 不审产物是否该存在」。**起草后的第二天 (07-31), 起草者自己在做 A3 修订前没有 fetch** —— 而并发轨已于 07-31 把同一个 #122 走完十步循环 ship 为 v1.65.0 并归档。08-02 才发现, 三天投入 (A1/A2/A3 + R5 五席 + R6 一席) 的修订对象**在修订期间已经归档**。

⇒ **提出这条纪律的人, 在提出后的第二天违反了它。** 这是「纪律不足以替代机制」的最强证据 —— 不是不知道, 是知道也做不到。

**主机制已 dogfood 成功 (同日)**: 在起手修 aria-plugin #124 **之前**, 按本 Spec §1 的调用形态实跑:

```bash
python3 .../phase1_gate.py --raw-track-id "aria-plugin-124-path-coverage-z-flag" \
  --phase A.1 --mode advisory --linked-issue "aria-plugin#124" --repo-path .
```

返回 `outcome=passed` / `proceed=true` / **`push_success=true`** / `linked_issue_overlap=[]`。⇒ **`--phase A.1` 无需改 phase1_gate 代码这一前提已实测坐实** (D6), claim 确实立即写并推远端 (主机制不依赖 spec 是否 push 的关键前提亦坐实)。

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

⇒ 机制只在 **Phase B 入口**认领。而碰撞发生在 **A.1 起草**。

**⚠️ R1-fix/minor 事实订正 (TL 查 ref 实据)**: 原文写「两轨都没走到 Phase B, 所以谁都没认领过」—— **不准确**。ref 实测: **R 轨于 `07-27T11:53:12Z` 确实认领过**, 但那是**在它跑完 4 轮 post_spec 之后**。L 轨则全程未认领。⇒ 真实论据比原文**更强**: 不是「没有认领机制可用」, 而是**认领发生在投入之后** —— 认领点在 Phase B 意味着它只能保护「已经做完 Phase A 的人不被打扰」, 保护不了「正要开始 Phase A 的人不做重复功」。**认领必须早于投入, 否则它记录的是既成事实而非预防碰撞。**

**反事实**: 若 L 在 07-25 A.1 时认领, R 在 07-27 起草时的 A.1 认领会返回 `linked_issue_overlap` 非空 ⇒ R 的整个 4 轮审计不会发生。

---

## What Changes

### 0. ⭐ `linked_issue` 归一 (R1-fix/C1 — **上游, 不修则下面全部白修**)

**R1 四席独立命中 + 主控实跑复验**: `lib/collision.py:217` 的匹配是**裸字符串 `!=`**, 无任何归一; 而生产 ref `refs/aria/coordination` 与 proposal 头部**三个变体族并存**:

| 族 | 形态 | 来源 | 实测条数 |
|---|---|---|---|
| A | `aria-plugin#122` | CLI 直传 (含本 Spec §Why 的 dogfood) | **4** |
| B | `10CG/aria-plugin#110` | CLI 直传 (org 限定), `phase1_gate` help 示例即此形 | **9** |
| C | `10CG/aria-plugin #122` | **proposal 头部「关联 Issue」字段的书写格式**, AI 逐字照抄即得 | ref 中 0, 但语料中存在且是最自然的复制源 |

⇒ 轨 A 认领 B 族、轨 B 认领 A 族 ⇒ `linked_issue_overlap` **恒 `[]`** ⇒ 与「真没人在做」不可区分。**这正是本 Spec 要根治的漏报, 原样复现在它自己的机制里。**

**归一规则 (钉到字符级)** —— 比较键 = `(repo_basename.casefold(), issue_number)`:

1. 剥首尾空白; 按**最后一个** `#` 拆为 `left` / `number`; `number` 必须是纯数字, 否则该值**不可解析** (见下方 4);
2. `left` 剥尾部空白 (处置 C 族); 若含 `/`, 取**最后一段**为 `repo_basename`, 其前为 `org`; 否则 `repo_basename = left`, `org = None`;
3. 匹配当且仅当 `repo_basename.casefold()` 相等 **且** `number` 相等。**`org` 不参与匹配**;
4. **不可解析的值** (无 `#` / `number` 非数字 / `repo_basename` 空) ⇒ **不参与归一, 退回原字符串精确比较** —— 绝不因为解析失败就判「不匹配」而静默放行。

**极性论证 (为什么 org 不参与匹配)**: 本机制是 **advisory**。漏报 = 机制静默无用 (昂贵, 已发生 5 次); 误报 = 多一行告警 (便宜, 人一眼可辨)。⇒ **fail toward reporting**。代价: `otherorg/aria-plugin#122` 与 `10CG/aria-plugin#122` 会误配 —— 故 surface 必须**回显双方 `linked_issue` 原始串** (见 §1 消费面), 让人一眼看出是不是同一个仓。

**实测负例保护**: `10CG/Aria#147` 与 `10CG/aria-plugin#110` 的 basename 分别是 `Aria` / `aria-plugin` ⇒ **不匹配** (正确)。`Aria` 与 `aria` 经 casefold 视为同仓 —— 本 Lab 无大小写相异的同名仓, 且误配方向仍是 fail-toward-reporting。

**存量数据不迁移**: 归一发生在**比较时**, 13 条已有记录原样有效, 无需改写 ref (改写共享 ref 是外向且难撤销动作, 不在本 Spec 范围)。

> ⚠️ **本条改 `lib/collision.py`, 打破了原 §非目标「不改 phase1_gate 自身代码」** —— 该非目标条款已作废并在 §非目标 就地更正。R1 前的判断 (「机制已 ship, 只需换调用点」) 被证伪: **机制 ship 了不等于机制能用**, 它的匹配谓词在真实语料上是坏的。这与本 Spec 自己援引的 `feedback_completion_signals_vs_runtime_invocation` 同形 —— 「已 ship」不是「已验证在生产语料上工作」。

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

- **`--phase` 是自由字符串** (CLI 无 `choices` 约束, 已核 + 实跑) ⇒ `A.1` 无需改 phase1_gate 代码。
- **⭐ `--raw-track-id` 取值单一来源 (R1-fix/M1-CR — 原文「spec-slug 或 carry-id」双来源无优先级)**: A.1 时 spec-slug 尚未定型且极易改名 (见 §3c)。⇒ **A.1 一律用 issue 派生的稳定串** `<归一后 repo_basename>-<number>` (如 `aria-plugin-122`); 无关联 issue 的 spec 才回落 spec-slug。该串在 A.1→B 全程不变, 使 §3c 的改名孤儿问题从源头消失, 且与 D.2b 的 release 按同一 key 定位。
- **⭐ `--repo-path` 必须钉死 (R1-fix/M8-TL)**: 一律传**主仓根** (`openspec/` 与 `.aria/` 所在仓), **不是**代码落点所在的子模块根。否则两容器各按所在仓传参 ⇒ `auto_bootstrap` 静默建出**两条不同的 coordination ref** ⇒ 双方永远看不见对方。本 Spec 自述跨仓落点 (Spec 落主仓 / 代码落 aria), 该歧义是现实的。
- **`--linked-issue` 在 A.1 是条件必需**: spec 有「关联 Issue」字段时**必传**; 无关联 issue 的 spec (纯内部重构) 可省。与 Phase B 的「可选」不同 —— A.1 正是 issue 维度碰撞的发生点。取值格式见 §0 (三族任一均可, 归一在 `linked_issue_overlaps` 内完成; **建议统一书写 org 限定形**以减少人工判别成本)。
- **⭐ 与 `coordination.enabled` 的关系 (R1-fix/M3)**: A.1 认领**受同一开关控制** —— `state_scanner.coordination.enabled == false` ⇒ **零调用**, 与 Phase B 现状对称。已核实 `phase1_gate.py` **本身不读 config**, skip 判断全在调用方 SKILL.md 层 ⇒ 该 skip 条件必须在 phase-a-planner/SKILL.md **显式写出**, 否则 opt-out 项目在 A.1 仍被强制写 claim + push 远端 (对未配 coordination ref 的第三方项目是外向副作用)。`mode` 沿用同一配置, 不新增开关。
- **⭐ fetch 降级必须进 JSON `error` 契约 (R1-fix/M7-BA)**: BA 实跑复现 —— 首次真实调用即触发 fetch 失败而 `error: null`。⇒ SC-1/SC-2 赖以成立的「读到的是最新 claim」这一新鲜度前提**当前不成立**。处置: `phase1_gate` 输出的 `error` 字段须携带 fetch 降级状态, A.1 消费面见到降级时**按「未能核实」措辞告警**, 不得渲染成「无碰撞」(零证据不得当正证据 —— 与 state-scanner 的 QA-C1 不变量同源)。
- **消费**: `linked_issue_overlap[]` 非空 ⇒ 在 A.1 起草**前**渲染 🔴 告警, 列出对方 track-id / owner-container / claimed_at / **双方 `linked_issue` 原始串** (§0 归一后 org 不参与匹配, 回显原串是误配的唯一人工判别手段) / **`status`**。
  - **报告形态钉死 (R1-fix/C3-CR)**: 用 `AskUserQuestion` 显式请裁, 选项至少含「另起/接手/并轨」。**不是**渲染一行就自行决定 —— 「继续起草」是对已知碰撞的处置决定, 属 owner 权限面 (Rule #10); 也**不是**硬阻断 (那撞 §非目标与 AD10 的单人类参与点)。advisory 的含义是**机制不阻断**, 不是**AI 可自行放行**。
- **⭐ `done` 状态的同 issue claim 必须可见 (R1-fix/C2)**: `collision.py:210` 的 `_TERMINAL = ("done","abandoned","unknown")` 把它们直接 skip。**A.1 场景下 `done` 恰恰是最该看见的信号** —— 它意味着「对方已经把这件事做完了」。改为: `linked_issue_overlaps` 增可选参数 `include_terminal`(默认 False 保持既有调用方语义不变), A.1 调用点传 True, 命中 `done` 时**降级为提示**「⚠️ 同 issue 已有 track 标记 done —— 该 issue 可能已被解决, 起草前请核实」。`abandoned` / `unknown` 同样回显但措辞区分。
  > **为什么这条是 critical**: 第 5 次事故的**最终形态**就是「对方已 ship 并把 claim 置 done」。按 A2 前的设计, 那一刻 overlap 恒空 ⇒ **机制对自己的 motivating case 失明**。

### 2. audit-engine 每轮入口竞品扫描 (副机制, 覆盖不同盲区)

`audit-engine` Step 0 (anchor 固化) 旁加 **Step 0.5**: 每轮 (非仅首轮) 入口 fetch 后, 对本 spec 的「关联 Issue」grep 全部远端 ref 上的 `openspec/changes/*/proposal.md`。

- **新增** `aria/skills/audit-engine/scripts/sibling_spec_probe.py` (stdlib-only; audit-engine 目前零 `scripts/`, 本 change 新建该目录 —— 已核实对 `run_all_tests.sh` 扫描与 skill 打包无影响)。
- **⭐ 扫描范围含归档 (R1-fix/C2)**: glob 为 `openspec/{changes,archive}/*/proposal.md` —— **不是**只有 `changes/`。实跑证据: 第 5 次事故的真竞品在 `openspec/archive/2026-07-31-phase-c-gate-path-coverage-not-applicable/`, 而 `openspec/changes/*/proposal.md` 对 path-coverage **只命中作者自己那份**。归档命中的措辞与活跃命中区分 (「该 issue 已有已完成的 Spec」vs「同 issue 有活跃 Spec」)。
- **每轮跑而非仅首轮** —— 本次事故里 R 恰好在 L 的最后一轮之后落地; 多轮审计跨小时甚至跨天, 首轮扫描不够 (同 memory 「每次实质动作前」而非「仅起点」)。
  > **命名订正 (R1-fix/M5)**: 原文叫「Step 0.5」, 而 `audit-engine/SKILL.md:85` 明写 Step 0 是「Round 1 启动前**一次性**」—— 挂在它旁边与「每轮」自相矛盾。改称 **per-round 入口探针**, 接在 **`references/execution-modes.md` 的每轮循环入口**(该文件须入 §Impact 表)。audit-engine 现无任何 fetch 能力, 探针须自带 fetch 或复用 state-scanner 的 remote_refresh 缓存 —— **二选一须在 Phase A.2 定死**。
- **⭐ 规模与代价上限 (R1-fix/M6)**: 「全部远端 ref」无界。同代码库 `handoff_multibranch.py` 已因 **440 条远端分支**踩过同一坑并做了 scan cap —— 本探针**必须复用同款上限策略**: 只扫 `enforced_remotes` × 各自默认分支 (非全部 ref), 超限时按 `log()` 显式披露被丢弃的范围 (no silent caps)。
- **消费面 (R1-fix/M4 — 原文只定义了「检测」半)**: 探针命中 ⇒ 在该轮审计报告的入口段渲染 🔴 一行 + 写入 `.aria/audit-reports/` 的聚合报告; **不阻断审计** (与主机制同为 advisory)。exit code: 0=无命中 / 0=有命中 (命中不是错误) / **非 0 仅用于探针自身失败**。
- **诚实声明其盲区 (不得当作主防线)**: 本机制只能看见**已 push 到远端的**竞品 spec。对方 spec 仍 untracked 时它一无所获 —— 这正是本次事故**前半段**的实况。它覆盖的是**另两个**场景: (a) 对方 spec 已落地但**没走 claim** (未用 phase1_gate / legacy 轨); (b) 对方**已 ship 并归档** (C2 修复后)。

### 3. ⭐ claim 生命周期 — A.1 认领引入的三条新路径 (R1-fix/C3+M2)

A.1 认领**不是** Phase B 认领的简单前移: 它引入了 Phase B 没有的退出路径与时长特征。

**(3a) 保护窗必须覆盖事故窗 (C3, TL 报生产实例)**: A.1 claim 无 heartbeat 回路, `SWEEP_TTL=24h` 到期即被跨容器 sweep 成 `abandoned`, 再被 `_TERMINAL` skip。而本 Spec 自述的事故窗:

| 事故 | 起草 → 发现 | 时长 |
|---|---|---|
| 第 4 次 (#122 L 轨) | 07-25 → 07-27 | **~48h** |
| 第 5 次 (本 Spec 自身) | 07-30 → 08-02 | **~72h** |

⇒ **保护窗 (24h) 比它要防的事故窗短 2-3 倍** —— 机制在最需要它的时刻已经过期。处置 (Phase A.2 二选一定死): (i) A.1 认领后由 phase-a-planner 在每次实质推进时打 heartbeat; 或 (ii) 为 `phase` 以 `A` 开头的 claim 单独配置更长 TTL。**(i) 更可取** —— TTL 加长会让真正废弃的 A.1 claim 挂更久, 与 sweep 的设计意图相反。

**(3b) 探索性放弃 (M2)**: A.1 是探索性最强的阶段, 起草者可能试三个方向弃两个。**每个被弃的方向都留一条 active claim** ⇒ 僵尸 claim。处置: phase-a-planner 在 A.1 判定「不起该 Spec」时**必须调 `release_gate.py --status abandoned`**; 该义务写进 SKILL.md 与 SC。

**(3c) slug 改名 (M2 / BA)**: A.1 期间改 spec-slug 极常见, 而 `track_id` 由裸串归一产生、**无重命名迁移**。改名后 `release_claim_by_track` 按新 slug 定位 ⇒ 静默 `claim_not_found` ⇒ 旧 claim 成孤儿, 存活 ≥24h。处置: 改名时**先 release 旧 track 再 acquire 新 track**, 两步都写进 SKILL.md; 或 A.1 统一用 **issue 号派生的稳定 track-id** (见 §1 的 `--raw-track-id` 取值订正)。

**(3d) D.2b 对偶**: 原文全文零处提 release/sweep/D.2b。A.1 认领的对偶仍是 phase-d-closer D.2b 的 release —— 但**只有走完循环的轨**才会到 D.2b, (3b)/(3c) 两条新路径**不经过它**, 故必须各自显式 release。

### 4. 残余缺口 (成文, 不假装覆盖 — R1-fix/M6 修正低估)

**两个机制都不覆盖**:

| 缺口 | 窗口 | 原文估计 | 实际 |
|---|---|---|---|
| 双方都未 claim 且未 push | claim 推送延迟 | 秒级 ✅ | 秒级 |
| 一方**跳过 A.1** 直调 `/spec-drafter` (它 `user-invocable: true`) | 无界 | ❌ 未列 | **无界** |
| 一方 `coordination.enabled=false` (opt-out) | 无界 | ❌ 未列 | **无界** |
| legacy 轨 (不用 phase1_gate 的历史/第三方容器) | 无界 | ❌ 未列 | **无界** |

⇒ 原文只写「秒级」是**实质低估**, 且 **D5「不做中心化登记表」的裁决建立在该低估之上** —— 该裁决须在 Phase A.2 按真实缺口面重新评估 (本 Spec 不预判结论)。

- 入口覆盖不对称 (M7): Phase B 有**双落点** (phase-b-developer + branch-manager 各自点名绕过路径), A.1 若只在 phase-a-planner 单点接线, `/spec-drafter` 可直接绕过 ⇒ **A.1 也须双落点** (phase-a-planner + spec-drafter)。
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
| D6 | `--phase A.1` 不改 phase1_gate 代码 | 已核 CLI `--phase` 无 `choices` 约束; **2026-08-02 实跑坐实** (aria-plugin#124 起手前真调, `outcome=passed` / `push_success=true`) |
| D7 (08-02) | 主机制的承重前提「claim 立即推远端」**已实测**, 非推断 | dogfood 返回 `push_success: true`。这是主机制优于原建议 (grep 远端 spec) 的**唯一**理由 —— spec 可以本地躺两天, claim 不能。前提若不成立整个方案坍塌, 故必须实测而非援引文档 |

**Rule #6 (rule6_note) — R1-fix/C4 改判至第三行**:

原文判第二行「照跑 AB, 零裁量」。**QA 双套件实测证伪**: `phase-a-planner` (5 eval) 与 `audit-engine` (2 eval) 的现有 AB 套件**结构性覆盖不到**本 Spec 新增的行为 (A.1 入口认领 / overlap 消费 / per-round 探针) ⇒ 「照跑 AB」跑的是**测不到该行为的套件**, 是空头支票。

⇒ 按判据表**第三行「处方性 · 套件覆盖外 (典型: authoring 向导)」**处置, 三条缺一不可:
1. **点名行为**: (a) A.1 起草前必调 phase1_gate 并传 `--linked-issue`; (b) overlap 非空时经 `AskUserQuestion` 请裁而非自行放行; (c) fetch 降级时按「未能核实」措辞而非「无碰撞」;
2. **建可证伪定向 fixture**: 为上述三条各建一个定向 eval (放 `phase-c`… 不, 放 `ab-suite/phase-a-planner-*.json`), 双臂须能分辨;
3. **套件缺口开 issue**: AB 套件缺「A.1 入口协同」维度 —— 与既有 `aria-plugin#117` (缺 authoring 维度) 同族, 开新 issue 或并入 #117 由 Phase A.2 定。

**缺一照跑** (判据表原文)。确定性代码层 (`sibling_spec_probe.py` + `collision.py` 归一) 由 SC 覆盖, 与上述并行不互替。**不申请豁免。**

---

## Success Criteria

> **⚠️ 验证面前提 (R1-fix/C4)**: 原 SC-1~3 挂在「`skills/phase-a-planner/` 既有测试」上, 而**该目录只有 SKILL.md, 零 `scripts/` 零 `tests/`** —— 宿主不存在。本轮据此把 SC 按**被测对象是否为代码**分两类, 并为「AI 行为」类给出真实宿主:
>
> | 类 | 被测对象 | 宿主 | 能否机械断言 |
> |---|---|---|---|
> | **代码类** (SC-1a/4~9) | `collision.py` 归一 / `sibling_spec_probe.py` | `state-scanner/tests/` (既有) + `audit-engine/tests/` (新建) | ✅ |
> | **行为类** (SC-2/3) | AI 在 A.1 记得调用并正确消费 | **定向 AB fixture** (见 rule6_note 第 2 条) | ⚠️ 只能由 eval 覆盖, **不冒充结构化测试** |

| SC | 场景 | 期望 | 怎么会红 |
|----|------|------|---------|
| **SC-1a** ⭐ (C1) | `linked_issue` 三族两两配对: `aria-plugin#122` × `10CG/aria-plugin#122` × `10CG/aria-plugin #122` | **两两互相命中** (归一后 `(basename, number)` 相等) | 现状代码 (裸 `!=`) 在**全部三对**上必红 |
| **SC-1b** ⭐ (C1 负控) | `10CG/Aria#147` × `10CG/aria-plugin#147` (同 org 同号, **不同仓**) | **不得**命中 | 「只比 number」的退化实现在此必红 |
| **SC-1c** (C1 兜底) | 不可解析值 (`no-hash-here` / `repo#abc` / `#5`) | 退回**原字符串精确比较**, 不抛异常, 不因解析失败判「不匹配」 | 解析失败即 return False 的实现必红 |
| **SC-2** (行为类) | A.1 起草前, 同 issue 已有他轨 active claim | AI **在起草前**经 `AskUserQuestion` 请裁, 选项含另起/接手/并轨; 告警含对方 track-id / owner-container / claimed_at / **双方 linked_issue 原始串** / status | 定向 AB fixture; 「渲染一行后自行继续」的臂应可分辨 |
| **SC-3** (行为类) | spec 有「关联 Issue」字段但调用未传 `--linked-issue` | AI 不得跳过该参数 | 定向 AB fixture (**不冒充结构化测试** — 原文 SC-3 声称「A.1 流程断言」而无任何拥有者) |
| **SC-4** ⭐ (C2) | 副机制: 同 issue 竞品**在 `openspec/archive/` 下** | **命中**, 措辞标「已完成的 Spec」 | glob 只写 `changes/` 的实现必红 —— 这正是第 5 次事故的真实形态 |
| **SC-5** ⭐ (C2) | 主机制: 同 issue 他轨 claim 状态为 `done` | **可见** (降级提示, 非 skip) | `_TERMINAL` 直接 skip 的现状必红 |
| **SC-6** | 副机制: 远端存在同 issue 的他名**活跃** spec 目录 | 报告命中, 含目录名 + 所在 ref | |
| **SC-7** | 副机制: 远端无同 issue spec | 报告空, **exit 0**, 不阻断 | |
| **SC-8** | 副机制: fetch 失败 / 无远端 | **不静默** — 报告 `degraded` + 注明「本轮竞品扫描未执行」+ **exit 非 0** (与 SC-7 的 exit 0 形成可辨对照, 原文缺此契约) | 静默返回空报告的实现必红 |
| **SC-9** | 反向对照 (三条): (a) 本轨自己的 spec 目录**不得**自命中; (b) 本轨自己的 claim (同 track_id) 不得计入 overlap; (c) 扫描范围超上限时**必须** `log()` 披露被丢弃范围 | 三条各自可红 | (c) 抓 silent cap |
| **SC-10** ⭐ (C3) | A.1 claim 在 `SWEEP_TTL` 内被 heartbeat 刷新后, 超过原 TTL 仍为 `active` | 保护窗覆盖 ≥72h (实测事故窗上界) | 无 heartbeat 的现状在 24h+ 必红 |
| **SC-11** ⭐ (M2/3b+3c) | (a) A.1 判定「不起该 Spec」后 claim 状态为 `abandoned`; (b) issue 派生 track-id 在 slug 改名前后**不变** | 两条各自可红 | (a) 抓僵尸 claim; (b) 抓孤儿 claim |
| **SC-12** (M3) | `coordination.enabled == false` | A.1 **零调用** phase1_gate, 不写 claim, 不推远端 | 无条件调用的实现必红 (对第三方项目是外向副作用) |
| **SC-13** (M7) | fetch 降级发生时 | `error` 字段非空; A.1 消费面渲染「未能核实」而**非**「无碰撞」 | 现状 (`error: null`) 必红 — BA 已实跑复现 |

---

## 非目标

- 不做中心化 spec 登记表 (D5) —— ⚠️ **该裁决建立在「残余缺口仅秒级」之上, 而 §4 已证其为实质低估** (跳 A.1 / opt-out / legacy 轨三条窗口无界)。**须在 Phase A.2 按真实缺口面重新评估**, 本 Spec 不预判结论;
- 不把 advisory 升级为 block (advisory-over-hardlock 是既有设计立场, 正交);
- ~~不改 `phase1_gate` 自身代码 (只改调用点与调用参数)~~ ⛔ **该条 R1-fix 作废**。C1 证明 `lib/collision.py:217` 的匹配谓词在真实语料上是坏的 (三族格式并存 + 裸 `!=`), 不改它则整个主机制静默失效; C2 的 `_TERMINAL` skip 同理。**改为**: 只改 `lib/collision.py` 的匹配谓词与 `include_terminal` 参数 + `phase1_gate` 的 `error` 契约 (M7), **不改 claim 的读写/推送机制本体**;
  > **R1 前的判断被证伪**: 原文的核心卖点是「机制已 ship, 只需换调用点」。R1 证明**已 ship ≠ 能用** —— 与本 Spec 自己援引的 `feedback_completion_signals_vs_runtime_invocation` 同形 (勾选/单测/结构 benchmark ≠ 代码真在生产语料上工作)。
- 不动 Phase B 入口现有认领 (它照旧; `include_terminal` 默认 False 保持既有调用方语义逐字节不变);
- 不改写存量 coordination ref 数据 (归一在比较时发生, 13 条已有记录原样有效; 改写共享 ref 是外向且难撤销动作)。

---

## Impact

| 文件 | 变更 |
|------|------|
| `skills/state-scanner/lib/collision.py` | ⭐ **R1-fix/C1+C2**: `linked_issue` 归一比较 (§0 四步规则) + `linked_issue_overlaps` 增 `include_terminal` 可选参数 (默认 False) |
| `skills/state-scanner/tests/` (既有宿主) | 扩展 — SC-1a/1b/1c (归一三族 + 负控 + 不可解析兜底) / SC-5 (`done` 可见) / SC-9b |
| `skills/state-scanner/scripts/phase1_gate.py` | **R1-fix/M7**: fetch 降级进 JSON `error` 契约 (SC-13) |
| `skills/phase-a-planner/SKILL.md` | A.1 入口认领步骤 + overlap 消费 (`AskUserQuestion` 请裁) + `--raw-track-id` 用 issue 派生串 + `--repo-path` 钉主仓根 + `coordination.enabled` skip 条件 + §3b/3c 的 release 义务 |
| `skills/spec-drafter/SKILL.md` | ⭐ **R1-fix/M7-CR**: 第二落点 (它 `user-invocable: true`, 可绕过 phase-a-planner) —— 与 Phase B 的双落点对称 |
| `skills/audit-engine/SKILL.md` + `references/execution-modes.md` | per-round 入口探针 (**非** Step 0.5, 见 §2 命名订正) + 盲区声明; `execution-modes.md` 是每轮循环所在处, **原 Impact 表漏列** |
| `skills/audit-engine/scripts/sibling_spec_probe.py` | **新增** (目录也新建; 已核对 `run_all_tests.sh` / 打包无影响) |
| `skills/audit-engine/tests/test_sibling_spec_probe.py` | **新增** (SC-4/6/7/8/9a/9c) |
| `skills/state-scanner/references/layer-l-integration.md` | ⭐ **R1-fix/M8-KM**: 该活文档明确断言「闸门仅在 Phase B 触发」, 本 Spec 实施后即过时 —— **原 Impact 表完全未提** |
| `skills/spec-drafter/` 模板 + `standards/` | ⭐ **R1-fix/M1**: 「关联 Issue」进 proposal 模板并成文 —— 现状全语料 **14/139 (10%)** 有该字段, **本 Spec 自己头部就没有** ⇒ 省字段即免义务且不可观测, D2「条件必需」形同虚设 |
| `skills/config-loader/SKILL.md` | coordination 在 A.1 的 skip 语义登记 (第二权威 config schema) |
| AB 套件 | 定向 fixture ×3 (rule6_note 第 2 条) + 套件缺口 issue (第 3 条) |
| 发版 5 文件 + 主仓 gitlink | v1.66.0 MINOR |

---

## 修订记录

### R1-fix (2026-08-02) — post_spec R1 五席 5/5 REVISE 全量吸收

**输入**: config `teams.post_spec` 5 席全上, **5/5 REVISE**, `scope_ok` 5/5 true。去重后 4 critical + 8 major + 7 minor。聚合报告 `.aria/audit-reports/post_spec-R1-1785640000000-*-aggregated.md`。owner 裁定「跑 R1-fix, 从 C1 起手」。

| 簇 | 席位 | 处置 |
|---|---|---|
| **C1** `linked_issue` 无归一 ⇒ 主机制静默失效 | 4 席 + 主控实跑 | **新增 §0** (上游): 三族格式实测表 + 四步归一规则 (比较键 `(basename.casefold(), number)`, org 不参与) + fail-toward-reporting 极性论证 + 不可解析值退回精确比较。SC-1a/1b/1c |
| **C2** 对「竞品已归档」结构性失明 | 2 席 + 主控实跑 | 副机制 glob 扩 `{changes,archive}`; 主机制 `include_terminal` 参数使 `done` 可见 (降级提示)。SC-4 / SC-5 |
| **C3** 保护窗 24h < 事故窗 48-72h | TL (含生产实例) | **新增 §3**: heartbeat vs 长 TTL 二选一 (倾向 heartbeat), Phase A.2 定死。SC-10 |
| **C4** 验证面无宿主 + Rule #6 误判 | QA 3 条 + TL/CR | SC 表按「代码类 / 行为类」**分层**并给真实宿主 (原文挂的 `phase-a-planner` 既有测试**不存在**); rule6_note **改判至第三行**「套件覆盖外」+ 三条落地 |
| **M1** 「关联 Issue」不是模板字段 | TL/CR/QA | 进 §Impact — spec-drafter 模板 + standards。现状全语料 **14/139 (10%)**, **本 Spec 自己头部就没有** |
| **M2** 生命周期对偶未覆盖 A.1 新路径 | TL/BA | §3b (探索性放弃须 release) + §3c (改名孤儿 → issue 派生稳定 track-id) + §3d (D.2b 对偶范围)。SC-11 |
| **M3** 与 `coordination.enabled` 关系未写 | TL/KM | §1 补: 受同一开关控制, 零调用; 且因 `phase1_gate` 不读 config, skip 须在 SKILL.md 显式写。SC-12 |
| **M4** 副机制只有检测半 | QA/CR | §2 补消费面 + exit code 契约 |
| **M5** 「Step 0.5」与「每轮」互斥 | TL/CR | 改称 **per-round 入口探针**, 接 `execution-modes.md` (该文件补进 Impact 表) |
| **M6** 副机制规模代价未定义 | BA/CR | 复用 `handoff_multibranch.py` 的 scan cap 策略 + `log()` 披露丢弃范围。SC-9c |
| **M7** fetch 降级不进 `error` 契约 | BA (实跑) | §1 补: 降级须进 `error`, 消费面按「未能核实」而非「无碰撞」。SC-13 |
| **M8** `layer-l-integration.md` 同步缺口 + `--repo-path` 未钉 | KM/TL | 两者均补进 §1 与 §Impact |
| **M7-CR** 入口覆盖不对称 | CR | `spec-drafter` 作第二落点 (它 `user-invocable: true` 可绕过) |
| **minor ×7** | 各席 | §Why:74 事实订正 (**R 轨确实认领过, 但在 4 轮 post_spec 之后** —— 比原文更强的论据) · 自指注记更新至 08-02 (三次机会错一次忘一次) · rule6_note 与 Impact 表的 SC 覆盖范围对齐 · SC-8 补 exit 契约 · SC-9 补三条反向对照 · §4 残余缺口按真实四项重写 (原「秒级」是实质低估) · D5 裁决标注「建立在低估之上, 须 A.2 重评」 |

**未吸收**: 无。

**§非目标 有一条被作废**: 「不改 phase1_gate 自身代码」—— C1/C2 证明匹配谓词在真实语料上是坏的, 不改则全盘失效。已就地更正并写明作废理由。

**⚠️ R1-fix 引入的新表面 (供下轮)**:
1. **§0 的归一规则本身是新承重逻辑**, 未经任何席位审过。尤其: casefold 跨仓误配的边界 / 「最后一个 `#`」拆分对含 `#` 的仓名 / 不可解析值的退回路径。
2. **`include_terminal` 参数改的是既有生产函数** —— 默认 False 保既有语义, 但 Phase B 调用方是否真的一处都不受影响, 需实测而非推断。
3. **issue 派生 track-id (`<basename>-<number>`)** 与既有 `derive_track_id` 归一的交互未验。

**本轮教训**: R1 推翻了本 Spec 的核心卖点「机制已 ship, 只需换调用点」。**已 ship ≠ 能用** —— `linked_issue_overlaps` 在生产语料上从来就没工作过, 而它已经存在了很久且有测试。这是 memory `feedback_completion_signals_vs_runtime_invocation` 的又一实例, 且这次的「完成信号」是**最有迷惑性的一种: 代码存在、有测试、被调用过、返回值合法** —— 只是它的匹配谓词对真实数据恒假。

---

## ⚠️ 闸门待裁 (Rule #10 — AI 不自行判定)

`.aria/config.json` 的 `audit.checkpoints.post_spec = "convergence"` **enabled**, 封闭豁免白名单四类无一适用 (非 config off / 无 adaptive_rules 映射 / 无成文 lane / 结构性前提成立 —— 审的对象即本 proposal)。⇒ **默认应跑 post_spec**。

同时: 本 session 硬约束「未经用户要求不得调用 Agent」与闸门执行相撞 (与 2026-07-27 session 同形状)。**两者均须 owner 显式裁, AI 不以任一方为由跳过另一方。**

**自指注记 (R1-fix/minor 更新至 08-02)**: 本 Spec 若照自己的 §1 执行, A.1 起草前应先认领。

- **07-30 起草时**: 人工代偿 (fetch 双远程 + 核实 `openspec/changes/` 无同主题 spec, 主仓 `4e034d2`)。⚠️ **R1 指出: 那次核实用的正是被本 Spec 自己证伪的那一招** —— 只扫 `openspec/changes/`, 恰好漏掉归档区 (即 C2)。
- **08-02**: 作者为 aria-plugin#124 认领了 (§Why 的 dogfood), 却**没有为本轨认领** —— TL 查 ref 实测零命中。⇒ **同一个 session 内, 作者对别的轨用了这个机制, 对本轨没用。**
- **R1-fix 时 (本次)**: 已按 §1 的形态为本轨补认领, track-id 用 §1 订正后的 issue 派生形。

> 这三条本身就是本 Spec 的论据: 三次机会里人工代偿**错了一次** (07-30 漏归档区)、**忘了一次** (08-02)。纪律的执行率在作者自己身上都不到 1/3。
