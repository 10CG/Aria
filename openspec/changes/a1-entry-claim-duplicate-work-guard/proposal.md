# Proposal: a1-entry-claim-duplicate-work-guard

> **Status**: 📝 **Draft (rework v3 — owner 2026-08-23 方向 b「缩 scope」已落, 换人执笔) — 待 post_spec R3 (convergence 续审, `max_rounds` 剩 2)**
> - **裁定 1 已执行**: C2 **(iii) 撤销, 只采 (ii)** —— `STALE_TTL` 维持 `1800` 不改; 四个落点 (SC-20 / Impact 表 `lib/constants.py` 行 / §2.3 残余风险段 / 闸门状态 item 3) 已逐一回撤;
> - **裁定 2 已执行**: 本 Spec 主体**只留 A.1 入口认领 + track-id 契约**。原 §1「关联 Issue」字段可得性/抽取规则 → 拆出 [`linked-issue-field-availability`](../linked-issue-field-availability/proposal.md); 原 §4 竞品 spec 探针 → 拆出 [`sibling-spec-probe`](../sibling-spec-probe/proposal.md)。两份子 Spec 由另外的执笔席并行起草, **均非本 Spec 的阻塞前置** (依赖方向见 §1 / §4 指针段);
> - **R2 三 critical**: C-A 随 §1 迁出; **C-B (连坐 release) 见 §5 + SC-27**, **C-C (carry-id 断链) 见 §2.1b「carry-id 契约」+ SC-23** —— owner 点名必须在此解, 已解;
> - **R1 editlist 残项**: FIX-01…19 的逐条对账见下方「R1-fix editlist 逐条对账」段 (**不写「已全量吸收」**, R2/M-13 零容忍);
> - 前置依赖 `linked-issue-normalization` 已于 2026-08-23 ship (v1.67.0, aria `ca52d1c`), 不再阻塞。
> - R2 聚合: `.aria/audit-reports/post_spec-R2-1787481000000-a1-entry-claim-rewrite-aggregated.md` · R1-fix editlist: `.aria/audit-reports/post_spec-R1-fix-editlist-a1-entry-claim.md`。
> **Created**: 2026-07-30 · **重写**: 2026-08-02 · **rework v3 (换人执笔)**: 2026-08-25
> **Spec Level**: 2
> **关联 Issue**: `无` — 本 Spec 源自 5 次并发起草事故的直接观察 (§Why), 无独立 issue 号。
> **代码落点**: `aria/` 子模块; Spec 落主仓 (Rule #5)
> **ship target**: 待定
> **前置依赖**: **[`linked-issue-normalization`](../../archive/2026-08-23-linked-issue-normalization/proposal.md) 已 ship 并归档** (**rework v3 链接订正**: 旧链接 `../linked-issue-normalization/` 在归档后已失效) (**R1 rework 核验订正**: 原文写「v1.66.0 已认领」, 实际以 **v1.67.0** 合并提交 `ca52d1c` 于 **2026-08-23T09:14:07Z** 合入 `origin/master`, 早于本文件本轮修订落盘) —— 前置依赖已满足, 本 Spec 的 overlap 检测可建立在其归一之上; `linked_issue_overlaps` 三参数签名未变 (详见「事实断言逐条实读清单」#16)。

> **📌 本文件只规定「要建什么」。** 「规定是怎么来的」(旧版三轮 + 重写 v2 两轮的审计轨迹 / C2 (iii) 撤销前的落版原文 / 各处**已闭环**的「⚠️ 实读订正 · 请 owner 复议」叙事 / **34 行「事实断言逐条实读清单」核验表**) 已于 rework v3 (2026-08-25) 整体移出至 **[审计轨](../../../.aria/audit-reports/a1-entry-claim-audit-trail.md)** (§1–§5)。
>
> **⚠️ 该审计轨是 append-only 的, 且显式不维护与本文件的一致性。** 二者出现不一致时**以本文件为准**; **不得**因审计轨的历史记述而回改本文件。切分依据: R2 聚合判定「major 17→17 持平, 每轮 fix 引入 ≈ 等量同形缺陷」, 与 memory `audit-trail-not-in-spec` 点名的耦合形状同形; 处方是**切开不重写** —— 搬运按字节, 未改写任何一句。
>
> **⚠️ 本次切分是执笔侧的流程判断, 不是 owner 裁定** (rework v3 说明书 D-J 已标「请 owner 复议」) —— 若 owner 认为审计轨应留在本文件内, 按 Rule #10 撤回即可, 审计轨文件本身是无损搬运。

> ## 📌 这是一次**重写**, 不是修订
>
> 原版经 **post_spec R1 (5 席) → R2 (新眼睛) → R3 (第三双新眼睛)** 三轮, 同口径 major **4→6 上升**, 判定**不收敛**。每一版 fix 都在自己新写的条款上引入等量缺陷 (R2/C1 与 R3/C2 都是「上一版 fix 自己写的逻辑」)。
>
> owner 2026-08-02 裁定 **A+B**: **A** = 抽出 §0 独立交付; **B** = 关键决策转 spike 实测, **完成后重写而非继续打补丁**。
>
> **S1–S6 六条 spike 已全部完成** (`.aria/spikes/2026-08-02-*`)。本版据其结论重写 —— 其中 **S4 与 S5 各推翻了一条上游审计结论**, 若继续打补丁, 那两条错误会被原样吸收进 Spec。

---

## Why

### 问题

两个 AI 容器对**同一个 issue** 各自起草 Spec、各跑数轮审计闸门、互不知情, 直到一方 ship 才发现。**已发生 5 次。**

第 5 次的形态最完整: 本 Spec 于 07-30 起草, 论点是「闸门审产物质量, 不审产物是否该存在」; **起草者在 07-31 做修订前自己没有 fetch**, 而并发轨已把同一个 #122 走完十步循环 ship 并归档 —— 三天投入的修订对象**在修订期间已经作废**。

⇒ **提出这条纪律的人, 在提出后的第二天违反了它。** 不是不知道, 是知道也做不到。这是「纪律不足以替代机制」的最强证据。

### 根因: 闸门审产物质量, 不审产物是否该存在

10 轮闸门的入口断言里**没有任何一条**问过「远端是否已出现同 issue 的竞品 Spec」。SCOPE_OK / anchor 固化都在审**这份产物做得对不对**, 从不问**它该不该存在**。

### 已 ship 但接错位置的机制

`phase1_gate.py --linked-issue` 产出 `linked_issue_overlap[]`, CLI help 原文即「同 linked_issue 不同 track-id 的 active claim (advisory 告警, 不阻断)」。实测接线:

| Skill | 认领 |
|---|---|
| `phase-a-planner` (A.1-A.3) | ❌ **零调用** |
| `phase-b-developer` `:86-96` (B.0 块) / `branch-manager` `:146-152` | ✅ Phase B 入口 |

> **rework v3 行号订正**: 旧版写 `phase-b-developer :88-93 / branch-manager :149`。实读 aria `d50f9c3`: `phase-b-developer/SKILL.md` 的 B.0 块起于 `:86` (`B.0 - REQUIRE claim (…)`) 至 `:96` (`skip_if:` 注释段起始一带), 其中调用模板在 `:91-93`; `branch-manager/SKILL.md` 的标题在 **`:146`** (`### 前置: REQUIRE claim …`), 正文至 `:152`。命令 `git -C aria show d50f9c3:skills/phase-b-developer/SKILL.md | sed -n '86,96p'` / 同法读 `branch-manager` `146,152p`。

**ref 实测**: 竞品轨于 `07-27T11:53:12Z` **确实认领过** —— 但那是**在它跑完 4 轮 post_spec 之后**。

⇒ **认领点在 Phase B, 只能保护「已做完 Phase A 的人不被打扰」, 保护不了「正要开始的人不做重复功」。认领必须早于投入, 否则它记录的是既成事实而非预防碰撞。**

### ⚠️ spike 推翻的两条上游结论 (若不重写会被原样吸收)

| 上游结论 | spike 实测 |
|---|---|
| R2/M2:「basename 截断型别名恒漏是活跃问题」 | **S4 (⚠️ 2026-08-04 订正)**: 在**真正会被传给 `--linked-issue` 的总体**里截断型别名 **= 0 实例**, ref 已落盘总体同样 0 ⇒ 降为已知限。**但 S4 原报的「比例是反的 / R2 量错了总体」已作废** —— 逐字复跑 R2 的口径得 25/11 (与其 24/10 一致), 两组口径与范围都不同, **S4 自己做了一次跨总体比较, 与它指控 R2 的错误同形**。R2 的口径其实更贴近 `--linked-issue` 真实取值 |
| R3/M3a:「`./_` 分隔符碰撞属 dormant, 本组织无含 `.`/`_` 的仓名」 | **S5**: `10CG/10cg.local` 是**真实仓** (Forgejo API 实测, 11 open issues, handoff 引用过) ⇒ **活跃, 非 dormant** |

---

## ⭐ 真正的瓶颈: 主机制的输入九成缺席 (S4 的意外发现)

**实测口径 (rework v3 重测, 主仓 `cc1bdef`; 旧版写的 `141 / 13 / 9%` 是 2026-08-04 的过期计数, 已作废)**:

```
find openspec -name proposal.md | wc -l                              # 147
grep -rl '\*\*关联 Issue\*\*' openspec --include=proposal.md | wc -l   # 15  (14 在 archive/, 1 在 changes/)
find openspec/changes -name proposal.md | wc -l                      # 7
```

⇒ 在**在制**语料 (`openspec/changes/` 7 份) 里, **rework v3 落盘前真有该字段的 = 0 份**: 当时 grep 的唯一 `changes/` 命中来自本文件**旧 §1 里被引用的示例行** (行首 `> > **关联 Issue**: [10CG/aria-plugin #122](…)`) —— 即**形状匹配会在讨论该字段的 Spec 上假阳性** (同 memory `reference_secret_guard_false_positive_on_spec_docs`)。⇒ 「15」这个数**含至少 1 条假阳**, **不可直接当作可得性**。
**落盘后的现状 (可当场复核)**: 旧 §1 连同那行示例已迁出, 本文件按 FIX-19 补了**真的**字段 (第 12 行) ⇒ `changes/` 下的 1 条命中现在是**真阳**。主机制靠 `linked_issue` 匹配, 而该输入在在制语料上仍基本不存在。

⇒ **本 Spec 不再承担「把字段搞出来」** (owner 2026-08-23 方向 b): 字段可得性 / 抽取规则 / 机械校验整体迁至 **[`linked-issue-field-availability`](../linked-issue-field-availability/proposal.md)**, 依赖方向见下方 §1 指针段。**本 Spec 只承担「字段在场时怎么用它认领, 以及 track-id 契约」**; 字段缺席时主机制退化为零输入, 成文于 §6, 不假装覆盖。

---

## What Changes

### §1 「关联 Issue」字段可得性 — ⛔ **整节已迁出** (owner 2026-08-23 方向 b)

> **迁往**: [`openspec/changes/linked-issue-field-availability/proposal.md`](../linked-issue-field-availability/proposal.md) —— 原 §1 的四条 (进模板 / 格式固定 / 机械校验 custom check / 不追溯) 与「抽取规则」承重问题整体由该 Spec 承担, 连同 R2 簇 **C-A** (抽取规则 defer ⇒ check 上线恒红)、**M-10** (§1.3 custom check 无实现宿主 + SC-13 零验证宿主)、**M-2** (`standards/openspec/templates/proposal-minimal.md` 跨项目 SOT 未入 Impact), 以及 R1 editlist **FIX-06/07/08**; 原 **SC-13** 一并迁出 (见 Success Criteria 表内保留的迁出行); 本 Spec 不再对「字段怎么产生、怎么校验、怎么抽 token」作任何断言。
> **为什么迁**: R2 判定 C-A (抽取规则 defer 到 A.2 ⇒ check 上线恒红) 是 **R1/C3 still-open** 且承重, 与 A.1 认领机制**没有共同的收敛面**; owner 2026-08-23 裁定**方向 b 缩 scope**, 主体只留 A.1 入口认领 + track-id 契约。
> **依赖方向 (逐字, 不得读成隐式前置)**:
> - **字段 spec 与探针 spec 都不是主体的阻塞前置。** 主体在「字段缺席」时退化为**零输入** (`phase1_gate.py:1230` 的 `if args.linked_issue:` 门控整块, 见 §2.5 / §6), 该缺口成文于主体 §6, 不假装覆盖。
> - **主体是两个子 Spec 的语义母体**: 子 Spec 的 track-id / claim 语义一律引用主体, 不得自行重定义。
> - ⇒ 本 Spec 可**先于**两个子 Spec ship; 子 Spec ship 后主机制的输入覆盖率上升, 但主机制的**正确性不依赖它们**。

### §2 A.1 入口认领 (主机制)

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --raw-track-id "<basename>-<number>-<container_uuid>" \
  --phase A.1 --mode advisory \
  --linked-issue "<org>/<repo>#<n>" \
  --include-terminal \
  --repo-path "<主仓根>"
```

> **⚠️⚠️ token 为 `无` 时: 整个 `--linked-issue` 参数必须省略, 绝不可传 `--linked-issue 无` (R1-fix/NEW-01, 主控实跑复现)**
>
> `linked_issue_overlaps` **只在 `own_linked_issue` falsy 时短路** (**rework v3 行号订正**: 实读 aria `d50f9c3` 的 `lib/collision.py:265-266` = `if not own_linked_issue:` / `return []`; 原写 `:207-208` 是 `cb6bd5d` 口径, 已随前置 Spec 合并下移), 而 `"无"` 是 **truthy** ⇒ **两份毫无关系的 Spec 只要都写 `无`, 就会互相命中 overlap**。实跑复现:
>
> ```
> linked_issue_overlaps([claimA(linked_issue='无'), claimB(linked_issue='无')], 'spec-a-uuid1', '无')
> → [{'track_id': 'spec-b-uuid2', 'linked_issue': '无', ...}]   # ❌ 误报
> ```
>
> ⇒ **`无` 的语义是「已核实无关联」(一条正证据), 不是一个可参与相等比较的 token。** 此时 track-id 走 §2.1 的回落形 `<spec-slug>-<container_uuid>`, 主机制对该轨**不产生输入** —— 该已知限须写进 §6 缺口表。
>
> **这条是 (已迁出的) §1「显式写 `无`」与本节「实参逐字节取 token」两条 fix 之间的接缝** —— 三个对抗验证镜头都没抓到 (M3 只在 (已迁出的) §4 探针层处理了 `无` 的归属, 没下移到 CLI 实参层), 由整合者实测发现。**属「多条 fix 互相拆台」的第二类形状。**
> **rework v3 归属**: 「字段值为 `无` 时怎么写」归 [`linked-issue-field-availability`](../linked-issue-field-availability/proposal.md); 「**实参必须省略 `--linked-issue`**」是 CLI 调用面, **留在本 Spec** (本节 + §6 缺口表首行)。

**触发时机**: A.1 **起草前**, 作为**独立标题级步骤** (仿 `branch-manager/SKILL.md:146` 的 `### 前置: REQUIRE claim (Part A1, MUST — 与 phase-b-developer B.0 同一条约束)`), **不塞进现有 A.1 的 YAML 动作列表** —— §Why 已证埋进长列表的单行指令会被静默跳过 (R3/M6)。锚点字面钉为 **`前置: REQUIRE claim`** (与 Phase B 的 `B.0` 对称), 断言形态见 **SC-22**。

> **⚠️ 为什么换锚点 (R1-fix/FIX-13, rework v3 落)**: `phase-b-developer/SKILL.md` 的 `B.0 - REQUIRE claim` 在 **`:86`**, 位于 ```` ```yaml ```` 块内 (`:88` `check:` / `:89` `if_missing:` / `:92` `--raw-track-id "<本 cycle carry-id/Spec id>"`), 是 **YAML 键、不是标题**; 该文件 `grep -n "^#\+ "` 的全部标题里**无任何 `B.0`**。⇒ 旧版「仿 `### B.0`」引的是一个**不存在的锚点**, 不可作样板。实存的标题级样板是 `branch-manager/SKILL.md:146`。
> **B.0 自身的 YAML-键形态是既有欠缺**, 与本 Spec 的「前置: REQUIRE claim」落点正交, **不在本 Spec 修** (另开 issue) —— SC-22 的 docstring 须写明这处强度差异是有意的。

#### §2.1 track-id 派生 (spike S3 定案)

`<归一后 basename>-<str(int(number))>-<container_uuid>`; 无关联 issue 时回落 `<spec-slug>-<container_uuid>`。

| 段 | 规则 | 依据 |
|---|---|---|
| `basename` | 经前置 Spec 归一 (含 S5 追加的 `./_ → -`) | 与 `derive_track_id` 两层对齐 |
| `number` | **`str(int(number))`** | 否则 `#007` 与 `#7` 派生两个 id ⇒ 自排除失效 ⇒ 自己较早的 claim 被误判为他人碰撞 |
| `container_uuid` | container-id 文件的 **`uuid` 字段本身**, **不截断、跳过 `label`** | `get_container_id()` (`lib/identity.py:191`) 在 `:222` 是 `return label if label else uuid` (**label 优先**), 而文件模板**明确邀请**用户设 label ⇒ `devbox-A1`/`devbox-A2` 截断后碰撞。uuid 是机器生成定长 hex, 碰撞域 16⁸≈4.3e9 可算 (实测 Lab 仅 2 容器)。**hostname 兜底分支实读落点 = `:242` (`return _hostname()`)**; `:244` 是**另一条**「新生成 uuid」路径 (`return uuid`), 二者不可混。<br>⚠️ **S3 spike 勘误 (editlist FIX-18)**: `.aria/spikes/2026-08-02-S3-track-id-derivation.md:72` 记「`:244` 是 hostname 兜底」为**行号误记** —— 实读 `:242` 才是 `return _hostname()`。**spike 记录不追改, 本 Spec 引用 S3 时以此处为准。** |

**需新增**直取 `uuid` 字段的 accessor (现有 `get_container_id()` 不能直接用)。**hostname 兜底分支** (只读 fs) 同样返回 hostname, 接受其碰撞域 —— 该分支本身已是降级路径。

> **为什么必须含容器段 (rework v3 加强 — 备选方案已被实测证伪, 见决策记录 D3 补注)**:
>
> **备选方案**: 去掉 `container_uuid` 段, 让两容器对同一 issue 派生**同一** track_id, 靠 reconcile 的**同名碰撞** (`phase1_gate.py` 7c 分支的 `AdvisorySurface(kind="occupied", …)`) 报警。它更简、不动 §2.1 拼接规则。**该方案已被实读证伪, 不采**:
>
> 1. **7c 只在竞品 claim 未 stale 时触发** —— 实读 `phase1_gate.py` 7c 分支条件 `verdict.winner is not None and not _takeover_eligible(verdict)`; 一旦 `_takeover_eligible(verdict)` 命中 (`phase1_gate.py:283-294`: `"stale_takeover_eligible" in reason or reason in {"no_active_candidates","empty_claims"}`) 就走 7d, 而 7d 的注释逐字是 `# No prompt needed: stale / terminal tracks are safe to acquire.` ⇒ **stale 竞品零 surface**;
> 2. **竞品 claim 必然 stale** —— `lib/constants.py:43-44` 逐字自陈 `NO production heartbeat loop exists (heartbeat() has zero production call sites; phase1_gate self-resume does not refresh either)`, 而 `STALE_TTL: int = 1800` (`:36`, 30min); 本 Spec 的事故窗实测 **48–72h** ⇒ 同名通道在整个事故窗内**结构性静默** (= Aria #180);
> 3. **overlap 通道则新鲜度免疫** —— 实读 `lib/collision.py:265-292` (`linked_issue_overlaps` 全函数体) **不含任何 heartbeat/新鲜度过滤**, 对 stale claim 同样可见。
>
> ⇒ **容器段的作用不只是「防 overlap 恒空」**(旧版理据), 更是**把碰撞检测从新鲜度脆弱的同名通道 (7c/7d), 挪到新鲜度免疫的 overlap 通道**。这是它承重的真正原因。
> **原理据仍成立且是同一结论的另一半**: 不含容器段则两轨派生出同一 track_id, 而 `lib/collision.py:278-279` 明写 `if c.track_id == own_track_id:` / `continue  # same-name collision — reconcile's job, not ours` ⇒ **互相被排除 ⇒ overlap 恒空 ⇒ 主机制死** (R2/C1 实证; **rework v3 行号订正**: 旧版写 `:219-220` 是 `cb6bd5d` 口径, aria `d50f9c3` 上为 `:278-279`)。该注释本身也印证了第 1 点 —— 同名碰撞被显式**推给 reconcile**, 而 reconcile 那条路径正是上面证伪的那条。
> **职责分离**: 「是不是同一个 issue」由 `linked_issue` 承载; 「是不是同一条轨」由 `track_id` 承载。原 R1-fix 把前者塞进后者, 两轨遂在 track_id 维度失去可辨性 —— 而 overlap 正靠它工作。

##### §2.1a 拼接的落点与被测对象 (R2/M-17 第 1 项)

**拼接由谁做**: 上表三段的拼接**发生在 A.1 模板里** (`phase-a-planner` / `spec-drafter` 两处 SKILL.md 的 `--raw-track-id "…"` 实参), **没有代码宿主** —— 实读 `lib/track_id.py:61` 的 `derive_track_id(` 只做归一四步 (lower / `./_`→`-` / 截断 `MAX_TRACK_ID_LENGTH: int = 64` / 非 ASCII 走 sha256 回落, `:70-76`), **不含任何拼接或 `str(int(n))` 语义**。

⇒ **SC-1 / SC-4 的被测对象分两层, 缺一即无被测对象** (旧版把它们标成无宿主的断言, 是 R2/M-17 的命中点):

| 层 | 被测对象 | 宿主 | 怎么会红 |
|---|---|---|---|
| **文本层 (可机械)** | 两处 SKILL.md 的 A.1 步骤块里, `--raw-track-id` 占位串**字面**含 `<container_uuid>` 段, 且 number 段写作 `str(int(number))` 而非裸 `<number>` | `state-scanner/tests/test_coordination_default_lockin.py` (与 SC-22 同宿主, 扩它) | 当前两处 SKILL.md **根本没有** A.1 步骤块 ⇒ baseline 必红; 写成 `<basename>-<number>-<uuid>` (漏 `str(int())`) 的实现也红 |
| **行为层 (定向 fixture)** | AI 实际拼出的串是否遵守该规则 (`#007` → `7`; label 不参与) | 定向 AB fixture (rule6_note 覆盖外档) | 「照抄 `#007`」的臂与「归一成 `7`」的臂可分辨 |

**本 Spec 不新增拼接函数** —— 新增代码落点只有 `lib/identity.py` 的直取 `uuid` accessor (见 Impact 表)。「拼接无代码宿主」这一半**成文交付**, 不用「以后加个 helper」把它糊过去 (memory `knob-granularity`: 诚实交付一半 + 说明哪半是哪半)。

> ## 🔴 K3 (R4) — 「不新增拼接函数」的**另一半代价**必须一并成文 (2026-08-27 补, 未经审计轮)
>
> **R4 实跑证据**: SC-2 的两臂在 `d50f9c3` 上**都是绿的** —— 臂(i) 含容器段绿; 主控 R3 加的负控臂(ii)
> 「容器段置空 ⇒ overlap 必须变空」**也绿**, 因为今天的代码本来就这样。根因: **夹具手写字符串**,
> **全程不执行任何派生逻辑** —— 而派生逻辑**没有代码宿主可执行**。
> (R3 主控还一度把 SC-2 的夹具约束写成「必须由 §2.1a 的 compose 函数派生」, 而本节明说不存在该函数 ——
> 那是「要求调一个不存在的函数」, 已订正。)
>
> **⇒ 交付一半是允许的, 但必须把另一半的代价写下来** (memory `knob-granularity` 只写了前半):
>
> **本 Spec 声明: 只要 track-id 派生没有代码宿主, 以下 SC **不能是代码类**, 一律降级为**行为类定向 fixture**,
> 并**明说它们只能由 AB eval 覆盖、不冒充结构化测试**: **SC-1 / SC-2 / SC-4 / SC-15**。
> - 降级**不是**放弃: 每条仍须在 rule6_note 的「覆盖外」档建**可证伪定向 fixture** (双臂须能分辨 AI 是否按 §2.1 规则拼串);
> - **禁止**把它们写成「代码 (CLI 全链路)」—— 那是本项目 R1/C4 点名过的「把 SC 挂在不存在的宿主上」;
> - **若 owner 采纳 R4 的选项 (d)「给派生一个代码宿主」, 本段连同这四条 SC 的类别一并回滚为代码类** —— 届时它们才真有牙齿。
>
> **未降级的相邻条目 (仍是代码类, 因为它们的被测对象确实存在)**: SC-23 (release CLI 往返) / SC-27 / SC-29 / **SC-30** / **SC-31**。

##### §2.1b carry-id 契约 — A.1 原串**即**本 cycle 的 carry-id (R2/C-C, editlist FIX-14 选项 A)

**问题 (KM-C1/C2 三处宿主独立复读)**: A.1 派生的 track-id 含 `container_uuid` 段, 而 Phase B / D.2b 既有的 carry-id 占位措辞不含容器段 ⇒ 走完循环时 **B-entry 认领与 D.2b 释放都匹配不到 A.1 那条 claim** —— 这比 §5 的连坐 (C-B) **更早发作**, 且发生在 happy path 上。

**处置 = 统一到一个串, 三处逐字节复用** (owner 的 U-3 选项 A):

> **A.1 认领时派生的那一串, 即本 cycle 的 carry-id。** `phase-b-developer` B.0 (`skills/phase-b-developer/SKILL.md:92` 的 `--raw-track-id "<本 cycle carry-id/Spec id>"`)、`branch-manager` (`skills/branch-manager/SKILL.md:146` 的 `### 前置: REQUIRE claim`)、`phase-d-closer` D.2b (`skills/phase-d-closer/SKILL.md:51-52`, `:55` 逐字「carry-id = Phase B-entry 时传给 phase1_gate 的同一原始串」) **三处逐字节复用同一串, 不再各自派生**。

- **三处 SKILL.md 的占位措辞须改为明示**: 「**A.1 认领时派生的那一串**; 未走 A.1 的 session 沿用 Spec id」⇒ Impact 表补这三行;
- `standards/conventions/session-handoff.md` **§2.3.8** 结构化 `{id, desc}` 的 `id` **同为该串** (**R3/KM-1 订正**: 原写 §2.3 —— 实读该文件 `:101` §2.3 是「机读 frontmatter schema」, `:217` §2.3.8 才是「结构化 Carry-id schema (§6 prose 层, **非 frontmatter**)」, 且 `:238` §2.3.8.3 逐字把「留 §6 prose, 不进 frontmatter」列为**硬约束** ⇒ 引 §2.3 会把实现者引向违反该硬约束) ⇒ Impact 表补该行 (R2/M-14 的一半);
- **为什么必须统一而不是在 D.2b 打补丁**: 实读 `lib/track_id.py:61-76` 的归一四步**不含任何去容器段逻辑** ⇒ 两个不同原串归一后必是两个不同 `track_id`, 而 `release_claim_by_track` 按 `(container, 归一 track_id)` 定位 (`lib/claim_lifecycle.py:377` 定义, `:425` `if rec.container == resolved.container_id`) ⇒ 不统一就**没有任何**归一层能把它们接上;
- **已知限 (成文, 不假装覆盖)**: 存量 active claim 仍是**旧形态** (无容器段), 本 Spec **不改写存量 ref** (见 §非目标) ⇒ 过渡期两形态并存, **新轨用新形态、旧轨自然随 GC 退场**。这段过渡期内, 旧形态轨的 A.1↔D.2b 断链**仍然存在**;
- **闭环由 SC-23 钉住** (A.1 认领 → 走完循环 → D.2b `release_gate.py --raw-track-id <A.1 原串>` ⇒ 该 claim 不再 active)。

> **与 §非目标「不动 Phase B 入口现有认领」的边界 (U-3 的争点, 此处明确)**: 改的是**三处模板里 carry-id 占位串的取值口径**, **不改** Phase B 闸门的调用形态、参数集与判定语义; `--include-terminal` 仍默认 False, Phase B 输出逐字节不变。若 owner 判此仍属「动 Phase B」, 备选是 editlist 的**选项 B** (D.2b 额外用 A.1 原串再调一次 `release_gate.py`) —— 本版按 owner 2026-08-23「主体必须解 C-C」采选项 A, **请 owner 在 R3 时确认**。

#### §2.2 保护窗 (spike S1 定案)

事故窗实测 **48–72h**, 而 `STALE_TTL` = 30min、`SWEEP_TTL` = 24h ⇒ 保护窗短于事故窗。

**处置 = 新增一个 by-track 的 heartbeat 变体**, 按 `(container_id, normalized track_id)` 定位, 刷新**全部**匹配的 active claim。

> **⚠️ 挂载点的真实触发密度 (R3/TL-M1, 主控 2026-08-25 补 —— 原文把常态写成了「漏跑一次」)**: (ii) 把 heartbeat 挂在 `/state-scanner` 入口, 但**审计轮内不会触发它** —— 实读 `skills/audit-engine/references/execution-modes.md` 的 convergence 与 challenge 两个模式块, **轮内均无 `/state-scanner` 调用**。⇒ 一次 post_spec 多轮审计 (本 Spec 自己就跑了 3 轮, 每轮数十分钟) 期间 heartbeat **一次都不刷**, 这是**常态而非「漏跑一次」**。**成文的残余风险**: `STALE_TTL` 维持 30min (owner 撤销 (iii)) ⇒ 长审计轮期间本轨 claim 对 reconcile 呈 stale、7c occupied surface 静默 (= Aria #180 的窗口), **只有 overlap 通道 (新鲜度免疫) 仍可见**。本 Spec **不**为此新增第二个挂载点 (会重蹈 (i) 被否的理由), 而是把它列为**已知限**并指向 follow-up: 若要覆盖长审计轮, 应在 audit-engine 轮间挂一次 heartbeat —— 属 audit-engine 变更面, 不在本 Spec。
>
> **⚠️ 口径统一 (R2/M-17 第 2 项)**: 旧版正文写「匹配键**改**」而 Impact 表写「**增**并存变体」, 两读矛盾。**以「增并存变体」为准** —— 既有 `heartbeat()` 的 `(container, session)` 匹配键**保持不动** (实读 `lib/claim_lifecycle.py:228`: `if rec.container == resolved.container_id and rec.session == resolved.session_id:`), 新增变体与之并存, 形态照抄 `release_claim` / `release_claim_by_track` 的并存模式 (`lib/claim_lifecycle.py:274` / `:377`)。**理由**: 改既有键会改变 Phase B 现有认领路径的行为, 撞 §非目标; 并存则 Phase B 逐字节不变。全文自此只用「增并存变体」这一种措辞。

> **这不是新设计, 是照抄隔壁函数**: `release_claim_by_track` 的 docstring 逐字记载**同一个 defect 已被同款修法解决过** ——「`release_claim` locates by `(container, session)`, but a later invocation runs with a **FRESH session_id** and cannot match... this variant **locates by (normalized track_id, container) and ignores session**」。它顺带给了两个细节: 一对多时**全部**刷新 (release 侧同款选择, review I1 已论证只放最早那条不够); raw→normalized 走 `derive_track_id` 与 acquire 同路径。
>
> **session_id 落盘复用方案判否** —— 被本方案取代, 且引入并发/过期新面。
> **冗余**: 每次调 `phase1_gate` 都写一条新 claim (生产 ref 实证 27+ 条) ⇒ 再调即自然续期。但它依赖「AI 记得再调」—— 而那正是本 Spec 存在的理由 ⇒ **heartbeat 为主, 再调作冗余, 不可只靠后者**。

> ## ✅ 已定项 (R1-fix/C2 — 3 席命中 → 2026-08-22 owner 裁定落版): **谁调、什么时机调**
>
> `heartbeat()` 的**生产调用点仍为 0** (`constants.py:43-44` 自陈:「NO production heartbeat loop exists」)。**换匹配键不产生刷新者** ⇒ 保护窗实质仍是 24h ⇒ **SC-5~7 可以全绿而问题原样存在**。
>
> **spike S1 §6 明确把「谁在什么时机调」交还给 Spec** (「属 Spec 范围不属 spike」), 而重写当时**没有接住**, 转 owner 裁定。**以下逐字取自 `git show 86540f2:openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md`** (R1 rework 核验 major-3 订正 —— 上一轮此处曾被整段删除换成 AI 转述且与原文有实质偏差, 未请复议; 现按硬约束恢复原文字面, 不再转述):
>
> > **✅ owner 裁定 (2026-08-22): 采 (ii)+(iii) 组合** —— heartbeat 挂 state-scanner 入口的 **AI 编排层** (scan.py collector 保持只读, 与 phase1_gate B-entry 既有挂法同构; 每次 `/state-scanner` 必跑, 不依赖 AI 记性); 同时 `STALE_TTL` 30min → **24h 量级**收窄版兜底, 使「漏跑一次扫描」不至于立即暴露在 `--sweep-stale` 下。落版义务: (ii) 的挂载点写进 state-scanner SKILL.md 编排契约 + (iii) 的 TTL 变更量化 sweep 语义代价 (spike S1 选项 c 的评估框架); 关联 Aria#180 (heartbeat 零调用) 由本裁定一并解。
>
> **落版 (AI, 2026-08-23)** ((i) 见下方「候选 (i) 未采纳」, 以下 (ii)/(iii) 即本节落版):
>
> **(ii) 调用点 = `state-scanner` 入口的 AI 编排层; `coordination.enabled == true` 时每次 `/state-scanner` 必跑** (**rework v3 按 R2/M-7 给标题补上门控限定** —— 旧标题的裸「每次必跑」与 §2.5 的 opt-out 条款字面冲突, 详见下方「与 B-entry 的关键差异」):
> - **具体 CLI 入口 (R1 rework 核验 major-1 补钉)**: 「AI 编排层调用 heartbeat CLI」原文未点名具体入口, 现定为 `skills/state-scanner/scripts/phase1_gate.py` 新增 **`--heartbeat-only` 模式** —— 复用其既有 identity/fetch/push 管道; 只刷新**本容器本 track** 的 `heartbeat_at`, **不写新 claim, 不判碰撞** (与 A.1 acquire 调用是同一 CLI 文件下的两个独立模式)。若 A.2 落地时改为独立脚本 `scripts/heartbeat_gate.py`, 亦属同一变更面 (已按此登记进 Impact 表, 见下方)。自本条起, 本节及 SC-21 提到的「heartbeat CLI」均特指该入口;
> - **既有同构先例**: `phase1_gate` 的 Phase B-entry 挂法就是这个模式 —— **实读** `skills/state-scanner/SKILL.md:149`「接线点 = AI 编排层, 不是 `scan.py`」+ `references/layer-l-integration.md:15`「Design A 条件触发: 闸门仅在用户确认要进入 Phase B 时调用, 不在 scan.py 内自动执行」。heartbeat 挂同一层 (AI 编排层调用 `--heartbeat-only`, collector 内不跑), `skills/state-scanner/scripts/scan.py` 的 collector 逻辑**保持只读, 零改动**;
> - **与 B-entry 的关键差异 —— 并且「无条件」限定的是什么 (R2/M-7 修正, rework v3)**: B-entry 是**条件触发** (实读 `skills/state-scanner/SKILL.md:149`: 触发条件为 `coordination.enabled == true` **且** `tracks_multibranch.collision.kind` 非空); heartbeat 的「**无条件**」**只**限定后半条 —— 即**不依赖 `tracks_multibranch.collision.kind` 是否非空** (它是维持性动作, 不是碰撞响应动作), 只要本会话在 coordination ref 里持有 active claim, 每次 `/state-scanner` 都刷新。
>   > **⚠️ 它不是「无视 opt-out」**: heartbeat **同样受 `state_scanner.coordination.enabled` 门控** —— `enabled == false` ⇒ **heartbeat 零调用**, 与 §2.5 是**同一条开关**, 不是两条。旧版「每次 `/state-scanner` 必跑」的字面读法会让只读型命令在 opt-out 项目上每次写 claim + 推远端 (对未配 coordination ref 的第三方是外向副作用), 这是 R2/M-7 的命中点。**由 SC-28 钉住** (`enabled == false` ⇒ 入口零 heartbeat 调用), 与 SC-9 是同一开关的两半;
> - **落点**: `skills/state-scanner/SKILL.md` 的 Layer L Phase B 集成段 (`:143-178` 一带) 新增对称的「Layer L A.1 heartbeat 集成」小节, 写明触发条件/调用形态 (`--heartbeat-only`) /失败处置 (fail-soft, 不阻断 `/state-scanner` 主流程);
> - **`--heartbeat-only` 刷哪条 track (R2/M-12 + R2-CR-M1 补, rework v3 —— 旧版只写「只刷本容器本 track」而 track 来源未定义, 且 claim 按 `(container, session)` 键控在跨 subprocess 时不可判定)**。**来源是三级回落, 顺序固定**:
>   - **① 本 session 已跑过 `phase1_gate` ⇒ 该 claim 在 coordination ref 内可按 `(container, session)` 直接定位, 从 `claims/<container>/<session>.yaml` 的 `track_id` 字段读出** —— **机读持久化状态, 非记忆**;
>     > **⚠️ 先例引用订正 (R3/TL-M6 —— 上一轮主控指令误引, 主控担责)**: 上一版此处引 `skills/phase-b-developer/SKILL.md:88` 的 `check: phase1_gate telemetry / 编排层记忆 (本 session 是否已跑 phase1_gate)` 作「同一个 telemetry 通道取 track_id」的逐字先例。**实读证伪**: 该行是**布尔谓词** —— 它回答「**跑没跑**」, **不携带 `track_id`**; Phase B 的 track_id 在同文件 `:92` 另取自 `--raw-track-id "<本 cycle carry-id/Spec id>"`。⇒ 该先例**不能**用来论证「telemetry 提供 track 来源」, 已撤。替代的机读来源见本行正文 (coordination ref 内本 session 自己的 claim)。
>   - **② 回落 = handoff §6 的结构化 carry-id**, 与 B-entry 闸门取 `raw_track_id` 的**同一个来源** —— 即 §2.1b 定义的那一串 (`standards/conventions/session-handoff.md` **§2.3.8** 的 `{id, desc}` 之 `id`);
>   - **③ 两级都取不到 ⇒ 跳过, 但**必须留下可观测的持久化痕迹** (fail-soft)。**⚠️ K7 (R4) 订正 —— 原文写「跳过 + `log()`」是个空信号**: 实读 `def log(` 在全 aria **零命中**; `scripts/phase1_gate.py:56` 只有 `logger = logging.getLogger(__name__)` 而**无 handler** (`basicConfig` 只在 `scan.py`) ⇒ 独立 subprocess 的 `logger.*` **全丢**。叠加 R3/TL-M2 禁写 production 遥测分区 + SC-28 正向断言计数不增 ⇒ **「跑了但 skip」与「根本没挂载」在任何持久化产物里逐字节相同**, 连续三天静默 skip **无一处会红**。**落版 (2026-08-27, 未经审计轮)**: `--heartbeat-only` **每次调用都向遥测 JSONL 追加一条 `_source="heartbeat"` 记录** (该分区 `coordination_probe` 不计入, 见 R3/TL-M2, 故不会把那条 enabled check 变恒绿), 记录含 `outcome ∈ {refreshed, skipped_no_track, skipped_disabled, error}` 与 `reason`。⇒ 「跑了但 skip」在磁盘上**可辨**。「猜一个 track 去刷」仍禁止 —— 会刷错**别人**的 claim。**新增 SC-32 (代码)**: 在无 carry-id 的环境下跑 `--heartbeat-only` ⇒ 遥测 JSONL **新增恰一条** `_source="heartbeat"` 且 `outcome="skipped_no_track"`; **怎么会红**: 只 `logger.debug` 不落盘的实现 ⇒ 零新增记录 ⇒ 必红。**baseline 必红** (该模式今天不存在)。
>   - **CLI 形态**: `python3 .../phase1_gate.py --heartbeat-only --raw-track-id "<carry-id>" --phase A.1 --repo-path <主仓根>` (**`--phase` 不可省 — R3/BA-M1**: `phase1_gate.py:1191` 的 `--phase` 是 `required=True`, 主控实跑 `--raw-track-id x --heartbeat-only` → `error: the following arguments are required: --phase` ⇒ 旧版字面形态**第一次实跑即被 argparse 拒**, 到不了 heartbeat 分支。本 Spec 取「文档补 `--phase`」而**不**放开该参数: 零代码改动; `--heartbeat-only` 不写新 claim, `--phase` 仅作占位不落盘) —— 由 AI 编排层**显式传入**, CLI 侧**不做任何推断**;
>   - **匹配**: 按 `(container, 归一 track_id)` 刷新**全部**匹配的 active claim (与本节「增并存变体」的匹配键一致), **不写新 claim、不判碰撞**;
>   - **⛔ 遥测分区边界 (R3/TL-M2, 主控实读证实 —— 不划这条界会把一个 enabled 的 check 变成恒绿)**: `--heartbeat-only` **不得**写生产遥测分区。实读 `skills/state-scanner/scripts/coordination_probe.py:4-25`: 它是**反死代码探针**, 只数 `.aria/coordination-telemetry.jsonl` 里 `_source=="production"` 的**近期** `run_gate` 记录, 而该分区「written only by the CLI production path (`_main` → `_gated` with `_source="production"`)」(逐字)。⇒ 若 `--heartbeat-only` 复用同一条产线, **每次 `/state-scanner` 都会写一条** ⇒ 该 check **永远 OK**, 无论真正的碰撞闸门是否还被调用 —— 它要防的「机制接线了但没人调」正好被自己的心跳掩盖 (memory `feedback_false_green_dual_is_permanent_red` 的镜像)。**落版**: `--heartbeat-only` 走 `_gated(_source="heartbeat")` 或完全跳过 `_emit_telemetry`; `coordination_probe` 的计数口径**保持只认 `production`**, 不放宽。**Impact 表已补 `coordination_probe.py` 行 (仅注释/口径声明, 不改逻辑)**;
>
>   > **⚠️ 对 R2-CR-M1 反对意见的答复 (R3/TL-M6 后重写)**: CR-M1 指「给 heartbeat 指定 track 来源等于回到依赖 AI 记性, 而那正是 (ii) 要消灭的」。**答复**: **① 是 coordination ref 内本 (container, session) claim 的 `track_id` 字段**, **② 是 handoff §6 的结构化机读字段** —— **两级都不是「AI 记性」**, 都是磁盘上可被机械读取、可被测试夹具构造的持久化状态。**⚠️ 但须诚实声明该答复的边界**: ① 只在**同一 session 内**可用 (跨 session 时 `session_id` 是 FRESH 的, 按 `(container, session)` 找不到旧 claim —— 这正是 §2.2 存在的理由); 跨 session 场景**只剩 ②**, 而 ② 依赖「上一次会话写过 handoff §6」。⇒ **本条不主张已彻底消除人为环节, 只主张两级来源都是机读的**; 「handoff §6 缺失时 heartbeat 静默不跑」是**成文的已知限**, 见本节 ③。
>   >
>   > **⚠️ 显式否决 CR-M1 的 B 方案 (「不指定 track, 直接刷新本容器全部 active claim」)**: **不采。** 该方案会把**被遗忘、未 release 的 claim 永久 keep-alive** —— 它们将永不 stale、永不进 `--sweep-stale` 候选, 变成僵尸 claim 长期占据 overlap 告警面。这与 §5.2 的显式 release 义务和 **SC-7**（超 `SWEEP_TTL` 未刷新仍被 sweep）**直接相反**: B 方案下 SC-7 结构性无法为真。
> - **`--heartbeat-only` 的 fetch 代价与复用 (R2-CR-m6 补, rework v3)** —— **它不得自带第二次 fetch**:
>   - **编排层的调用位置保证了这一点**: heartbeat 跑在 `/state-scanner` 入口、即 `scan.py` 之后 ⇒ snapshot 的 `coordination_fetch` 区块里已经有一次**刚完成**的 `refs/aria/coordination` fetch 结果。**复用它, 不重跑。** 该区块自 F6′ 起是 Phase 0.5 `remote_refresh` 的**纯派生**产物 (实读 `skills/state-scanner/references/state-snapshot-schema.md:1029-1041`: 「本区块不再独立发起网络 I/O」), 字段见 `:1043-1056`;
>   - **⚠️ 新鲜度谓词必须用 `coordination_ref_present`, 不能只用 `success` (执笔席实读订正 —— 主控口述的「`coordination_fetch.success == false` ⇒ degraded」按 schema 实读是 fail-OPEN 的)**: 实读 `:1043` 逐字 —— `success: bool  # Reflects FETCH 1 (branch heads, load-bearing)`; 而 coordination ref 是 **Fetch 2**, 其结果在 `:1056` 的 `coordination_ref_present: bool | null`, 语义 `:1061-1064` 逐字 = `true` 已取到 / `false` benign absent (ref 未发布) / `null` unknown (Fetch 1 失败短路, 或 Fetch 2 非 benign 失败)。⇒ **`success == true` 与「coordination ref 没取到」完全可以并存**, 只判 `success` 会把「没取到协调数据」当成「取到了」。**本 Spec 的判据 (fail-CLOSED)**: **仅当 `coordination_fetch.success == true` 且 `coordination_ref_present == true` 时**才视为「本轮协调 ref 已新鲜」; 其余一切取值 (`false` / `null` / 键缺失) 一律按 **degraded** 处理;
>   - **degraded 时的处置**: heartbeat **只写本地** ref, push **尝试一次**, 失败 **fail-soft** (log + 不阻断 `/state-scanner` 主流程), **不重跑 fetch**;
>   - **⚠️ 代价披露 (与原 §4 探针「不得称其轻量」同等义务, 此处不沉默)**: 复用路径下 heartbeat 的**增量网络代价 = 0** (不发起 fetch); 但**若实现者违反本条自带 fetch**, 代价参照 spike S2 的历史实测 —— 双远端 fetch 5 次均值 **~13.8s/次** ⇒ 每次 `/state-scanner` 加 ~13.8s。**这正是「不得自带 fetch」是硬约束而非偏好的原因。** 本 Spec **未实测** `--heartbeat-only` 的本地写 + 单次 push 耗时, 该数字留 A.2 补;
> - 关联 Aria#180 (heartbeat 零调用) 由本裁定一并解。
>
> **(iii) `STALE_TTL` 30min → 24h 量级 — ⛔ 已撤销 (owner 裁定 2026-08-23, 见本节末)**: `STALE_TTL` **维持 `1800` 不改**, 本 Spec **不再对该常量提出任何断言**。
> - **撤销的四个落点** (R3 核验席 minor-1 点名, rework v3 逐一执行): ① **SC-20** 整行改为「⛔ 撤销」; ② **Impact 表 `lib/constants.py` 行**删去「TTL 改 86400 量级」与「不变量注释二选一」, 只保留与 TTL 数值无关的注释同步项; ③ **§2.3 残余风险段**删去「放宽到 `SWEEP_TTL` 同量级」整套推理, 改为成文残余风险; ④ **闸门状态 item 3** 改为「原采 (ii)+(iii), 复议后 (iii) 撤销」;
> - **(iii) 撤销后 R2/M-8 的处置**: M-8 指 (iii) 漏了第三消费者 (`track_board::_freshness_status` / `_takeover_eligible`) 且抹掉 `lib/constants.py:40-42` 的两级顺序 (实读该三行逐字: `Deliberately much longer than STALE_TTL: STALE_TTL only marks a claim` / `"takeover-eligible" (advisory, reversible on next read), but the sweep` / `REWRITES status=abandoned durably and the victim has no recovery path —`) —— **(iii) 既已撤销, 这些影响面整体消失** (常量不动 ⇒ 无消费者受影响 ⇒ 两级顺序原样保留)。M-8 唯一残留的要求是「残余风险分析不得单向」, 见 §2.3;
> - **(iii) 撤销前的落版原文** (含当时的「⚠️ 事实订正」与「落版后的准确效果」两段) **按字节搬入** [审计轨 §2](../../../.aria/audit-reports/a1-entry-claim-audit-trail.md#2-22-c2-iii-落版原文-2026-08-23-owner-撤销前) —— 那两段里唯一仍承重的实读事实 (`--sweep-stale` 的阈值是 `SWEEP_TTL` 不是 `STALE_TTL`) 已保留在 §2.3 与「事实断言逐条实读清单」#14, 未随搬运丢失。
>
> **候选 (i) 未采纳**: 挂在 A.1 机械步骤上 (如每次写 proposal 文件后) 被 (ii)「每次 `/state-scanner` 必跑」覆盖同一诉求且触点更集中, 不再单独引入第二个挂载面。
>
> **✅ 上述 (iii) 的「⚠️ 实读订正 · 请 owner 复议」已闭环** (R1 rework 核验 major-3(a) 提出 → owner 2026-08-23 回应 → 结论 = **撤销 (iii), 只采 (ii)**)。**该复议项不再未决**; 其原文 (逐字) 见 [审计轨 §3](../../../.aria/audit-reports/a1-entry-claim-audit-trail.md#3-22-实读订正--请-owner-复议原文-已闭环)。
>
> **✅ 协调项已解** (`origin/feature/linked-issue-normalization` 分支状态, R1 rework 核验 major 订正, 主控实读): 该分支已于合并提交 `ca52d1c` (v1.67.0, `2026-08-23T09:14:07Z`) 合入 `origin/master` (`git merge-base --is-ancestor origin/feature/linked-issue-normalization origin/master` 成立), **早于本轮 rework 落盘**。实读 `origin/master` 上的 `lib/collision.py`: 新增 `normalize_linked_issue()` (`:178`) / `_linked_issue_matches()` (`:219`) 两个 helper, 插在 `linked_issue_overlaps` (`:230`) 定义之前 —— **确认未改** `linked_issue_overlaps` 的三参数签名 (`claims, own_track_id, own_linked_issue`)。行号已整体下移: `_TERMINAL` 由 `cb6bd5d:210` → `origin/master:268`; `if not own_linked_issue`/`return []` 由 `:207-208` → `:265-266`; `if c.track_id == own_track_id`/`continue` 由 `:219-220` → `:278-279`。**本节引用的 `lib/gc.py`/`lib/constants.py` 行号已核, 未漂移** (`git diff --stat ca52d1c^1 ca52d1c` 实测只触及 `SKILL.md` / `claim_schema.py` / `collision.py` / **一个** test 文件 `test_release_by_track.py`, 外加发布同步面文件 `marketplace.json`/`plugin.json`/`CHANGELOG.md`/`README.md`/`VERSION`; **R1 rework 核验 minor-2 订正**: 原文「两个 test 文件」为误记, 实为一个; 不含 `gc.py`/`constants.py`)。详见下方「事实断言逐条实读清单」#3/#5/#6/#16。已按 R1 rework 核验 major-2 补入 Impact 表 `lib/collision.py` 一行 (原表零覆盖), 见下方。
>
> **⚠️ rework v3 基线订正 (本段写于上一轮, 其「`origin/master`」指的是当时的 `ca52d1c`)**: `origin/master` 此后已推进到 **`d50f9c3`** (v1.67.1 `58a49e7` + 2 commit)。上面列的三组行号 (`:268` / `:265-266` / `:278-279`) 在 `d50f9c3` 上**逐字复核仍成立** (清单 #3/#5/#6), 但**基线标签一律以 `d50f9c3` 为准**, 不再用会漂移的 `origin/master` 指代。姊妹 Spec 现**已 ship 并归档**, 协调项完全闭环 (含 editlist FIX-11 —— 姊妹自己在 ship 前写入了关闭条款), 详见 §2.4 传递链 item 0 与清单 #16。
>
> **✅ owner 裁定 (2026-08-23): (iii) 撤销, 只采 (ii)。** `STALE_TTL` 维持 30min 不改; 与之相关的 SC-20 / Impact 表 constants.py 行 / §2.3「放宽到 SWEEP_TTL 同量级」残余风险段 / 闸门状态 item 3 中 (iii) 落点, 在 rework v3 一并回撤 (R3 核验席 minor-1 已点名这四处)。

#### §2.3 overlap 消费

`linked_issue_overlap[]` 非空 (或 `unknown_schema_claims > 0`, 见 §2.4) ⇒ **在起草前**经 `AskUserQuestion` 请裁。

> **⚠️ 无人值守 (Layer 2) 降级分支 (R2/M-15, editlist FIX-16)** —— 否则本节与 AD10「唯一人类参与点在 S7_AWAITING_MERGE」正面冲突:
>
> **判据 (可机械)**: `state_scanner.coordination.unattended == true` (**新 config key**, type boolean, **default false**; 在 `config-loader` 登记并在 `DEFAULTS.json` 注册, 由 aria-runner 容器镜像 / Nomad task env 显式置 true) ⇒ 走本分支: **零 `AskUserQuestion` 调用**, 改为把碰撞写进 handoff 的待复议段并置 `awaiting_owner`, A.1 继续但结论待 owner 复议 (Rule #10: AI 不自行放行, 但也不在无人处死等)。
>
> **不得**以「`AskUserQuestion` 看起来不可用/没人应答」做运行期推断 —— `allowed-tools` 是随 plugin 分发的**静态 frontmatter**, Layer 2 容器加载同一份 SKILL.md, 声明面完全相同; 且 C1 已把 `AskUserQuestion` 加进 `phase-a-planner` (见 §3) ⇒ **两个宿主都声明持有该工具, 该谓词求值恒为「可用」, 本分支永不进入**。这正是「C1 扩权亲手抹平了旧判据」的形状。
>
> **配套三处 (缺一即互相拆台)**: ① `config-loader/SKILL.md` 登记该 key (Impact 表); ② `DEFAULTS.json` 注册 (Impact 表, 与 R2/M-17 第 5 项同一行); ③ **SC-26** 钉行为 (`unattended == true` 且 overlap 非空 ⇒ 零 `AskUserQuestion` + handoff 出现 `awaiting_owner`)。
> **已知限 (成文)**: 本 Spec 只定义 key 与 A.1 侧的消费; **Layer 1→2 的 env 传递三腿契约** (write + HCL declare + consumer import, memory `feedback_env_propagation_3_leg_contract`) **不在本 Spec** —— 缺 import 会静默 fallback 到 `false` (即「照问不误」), 转 A.2/follow-up。

- **告警须含**: 对方 track-id / owner-container / claimed_at / **双方 `linked_issue` 原始串** (org 不参与匹配, 回显原串是误配的唯一人工判别手段) / `status`;
- **选项 (按对方 `status` 分档 —— R2/M-17 第 3 项: §2.4 让终态可见之后, 旧的三选项集不再覆盖新出现的两档)**:

  | 对方 claim 的 `status` | 该档下的选项集 | 为什么不同 |
  |---|---|---|
  | `active` (原有唯一档) | 「另起」/「**我去释放对方的 claim 后再开始 (两步人工)**」/「并轨」 | 对方在做, 三选项都指向「怎么和一个活着的轨共处」 |
  | **`done`** (§2.4 新可见) | 「**复用对方产出, 本轨不起 Spec**」(⇒ 按 §5.2 走 `release_gate.py --raw-track-id "<本轨 A.1 原串>" --status abandoned`) /「基于其产出起后续 Spec」/「另起 (说明差异)」 | **「释放对方 claim」在本档机械上不可达, 不是推理而是实读结论 (rework v3 补证)**: `release_claim_by_track` 的匹配条件含 **`and rec.status == "active"`** (`lib/claim_lifecycle.py:427`), 非 active 的 claim 一律不匹配 ⇒ 对一条 `done` claim 调 release **必然返回 `claim_not_found`** (`:430`)。「并轨」则是**协作决定**而非机械动作, 对已完成的轨无对象可并。⇒ 两项在本档列出来即误导 |
  | **`abandoned`** (§2.4 新可见) | **⚠️ 必须先分辨来源 (R4/K6)** —— 实读 `lib/gc.py:324` 逐字「Number of stale active claims **rewritten to** `status='abandoned'`」, 而 `ClaimRecord` **无 swept 标记** ⇒ `abandoned` 有**两种来源**: (1) 对方**显式** release; (2) `--sweep-stale` 的 **GC 产物** (对方可能仍在做, 只是超 24h 没刷心跳)。**本 Spec 不得把二者合并渲染**: 在两者不可分辨的前提下, `abandoned` 一律按「**可能仍在制, 按 `active` 同档请裁**」处理, 并在告警里写明「该状态可能是 GC 产物」。**代价成文**: 这会让「对方真的退出了」也被请裁一次 —— 用一次多余的请裁换「不误判对方已退出」, 方向正确 (零证据不得当正证据)。**给 `ClaimRecord` 加 swept 标记以真正分辨二者, 记 follow-up, 不在本 Spec** | 见左 |
  | **`unknown`** (§2.4 独立键) | 「**按存在处理**: 视同 `active` 请裁」 | 存在性已确认、内容未知 ⇒ 不得降格为「无碰撞」, 也不得与 `done`/`abandoned` 同档 (§2.4 四态表) |

  上表**不新增机制**, 只是把 §2.4 已经让其可见的 status 值, 在消费面补上对应的选项集。
  > **「接手」不是一键动作 (spike S3 实测)**: `release_claim_by_track` 只匹配调用者**自己的** container (`claim_lifecycle.py:425`), **无任何函数支持*定向*释放某个指定容器的 claim**; 且既有 `_takeover_eligible` 因含容器段后两轨必然不同 track_id 而**对本场景不可达**。
  >   **⚠️ 事实订正 (R1-fix/C5, 主控实读)**: 原文写「无任何函数支持释放别的容器的 claim」**为假** —— `release_gate.py --sweep-stale` 的 help 逐字写着「active 且 heartbeat 超 STALE_TTL → abandoned (**跨 container**)」。存在的是**无差别的陈旧清扫**, 不是定向接手。⇒ 「两步人工」的结论仍成立 (sweep 不能用来「接手某条特定的轨」), 但理由须改为「**只有无差别 sweep, 没有定向 release**」。
  >   **⚠️ 与 §2.2 复合的残余风险 (R1-fix/C2 关联; rework v3 按 (iii) 撤销重写, 并按 R2/M-8 改为双向)**: §2.2 的「谁调 heartbeat」已落版 ((ii): AI 编排层挂 `/state-scanner` 入口, 受 `coordination.enabled` 门控)。**(iii) 已撤销 ⇒ `STALE_TTL` 维持 `1800` (30min)**, 旧版「放宽到 `SWEEP_TTL` 同量级」的整套推理**随之作废**, 不再是本 Spec 的一部分。**现在的准确状态**:
  >   - **信号 A — reconcile 的 takeover-eligible 软信号** (`lib/reconcile.py:154-163` 的 `_is_stale()`, 末行 `return age_seconds > STALE_TTL`): 阈值 = `STALE_TTL` = **1800s / 30min** (`lib/constants.py:36`), **可逆** (下次 read 即可翻转)。本 Spec 之后 **不变** —— 这是**已知的残余风险**: 编排层漏跑一次 (>30min) 即被标 takeover-eligible;
  >   - **信号 B — `--sweep-stale` 的不可逆清扫**: 阈值 = `SWEEP_TTL` = **86400s / 24h** (`lib/constants.py:51`) —— 实读 `lib/gc.py:338-344` 的 `def sweep_stale_active(` 其 `stale_ttl_seconds: int = SWEEP_TTL` (**默认即 `SWEEP_TTL`**), 且 `scripts/release_gate.py:141` 的 `sw = sweep_stale_active(repo, now=ts)` **未传覆盖**。本 Spec 之后 **不变**, 且**与 `STALE_TTL` 无关** (从来就不读它);
  >
  >   ⇒ **残余风险 (成文, 不假装覆盖)**: advisory 的 takeover-eligible 窗口**仍是 30min**。**主检测责任由 overlap 通道承担** —— 实读 `lib/collision.py:265-292` 全函数**不做新鲜度过滤**, 对 stale claim 同样可见 (这正是 §2.1「为什么必须含容器段」第 3 点); **同名通道 (7c) 只在 30min 内有效**, 30min 后走 7d「No prompt needed」零 surface。**两个方向都要说**: (a) 不改 `STALE_TTL` ⇒ 软信号假阳性窗口窄 (漏跑一次即标 stale), 代价是 advisory 噪声; (b) 改大 ⇒ 假阳性少但真 stale 的轨更久不可 takeover。owner 2026-08-23 选 (a), 本 Spec **不再对该权衡提出任何断言**。
  >   ⇒ 措辞即定义, 避免实现者以为有一键路径。**跨容器 release 不在本 Spec 引入** (写别人的 claim 是权限面变更, 应独立评估);
- **不硬阻断** (撞 §非目标与 AD10), 但**也不是 AI 渲染一行后自行决定** —— 「继续起草」是对已知碰撞的处置决定, 属 owner 权限面 (Rule #10)。**advisory 的含义是机制不阻断, 不是 AI 可自行放行。**

#### §2.4 终态可见 + 传递链 (R3/C2)

`done` / `abandoned` 的同 issue claim **必须可见** —— A.1 场景下 `done` 恰恰是最该看见的信号 (「对方已经做完了」)。`lib/collision.py:268` 的 `_TERMINAL` 会直接 skip 它们 (**rework v3 行号订正**: 旧版写 `:210` 是 `cb6bd5d` 口径, aria `d50f9c3` 上为 `:268`)。

> **⚠️ 事实订正 (R1-fix/C4, 3 席 + 主控实读; rework v3 复读 aria `d50f9c3`)**: `lib/collision.py:268` —— `_TERMINAL = ("done", "abandoned", "unknown")` (函数内局部变量)。
> - **不含 `yielded`** ⇒ `yielded` **今天就已可见**, 不需要本机制去救; 原文把它列进来是**错的事实断言**, SC-8 的该子例 **baseline 即绿** ⇒ **SC-8 的场景列已同步删去 `yielded`** (R2/M-9: 旧版订正了正文却没同步 SC, 是「订正与断言脱钩」);
> - **含 `unknown`** ⇒ 它被 skip 而原文**完全没讨论**。**但旧版对 `unknown` 的定性也是错的** (rework v3 按 editlist FIX-12 订正): `unknown` 是 **reader-only sentinel**, 它一定对应一个**真实存在**的 claim 文件 ⇒ 它是「**已确认存在一条竞品 claim, 只是本读者读不懂其 schema 版本**」的**正证据**, **不是**「零证据」。把它和 fetch 降级 (真的什么都没取到) 归为同一极性, 是把正证据降格 —— 与 §2.5「零证据不得当正证据」**互为镜像**的同一类错误。四态措辞见下方表。

##### §2.4a `unknown` 走独立通道 (editlist FIX-03, ⭐ 承重) —— 经 overlap 通道**结构性不可达**

> ## 🔴 K5 (R4) — `unknown_schema_claims` **必须有失败态**, 否则 R2/M-4 在它自己的修复里复发 (2026-08-27 补, 未经审计轮)
>
> **R4/silent-failure 实读**: 本键与 `linked_issue_overlap` 共用 `scripts/phase1_gate.py:1231-1238` 的**同一个 `try:`**, 
> 而现有 `except` **只赋 `linked_issue_overlap`**。按本 Spec 把门控放宽为 `if args.linked_issue or args.include_terminal:` 后,
> `read_claims` 抛异常时 `unknown_schema_claims` **静默缺席** ⇒ 而 §2.5 四态表把「键缺席」定义为「**未检测**」,
> 消费方 `.get(k, 0)` 读成「**0 条 unknown**」—— **零证据被当成正证据**, 正是 R2/M-4 要修的病, 在 M-4 自己的修复里复发
> (memory `feedback_fix_recurs_in_its_own_fallback_path`)。
>
> **落版**: `except` 分支**必须同时**赋两个键 —— `out["linked_issue_overlap"] = None` **与** `out["unknown_schema_claims"] = None`,
> 外加 `out["linked_issue_overlap_error"] = <非空 token>`。⇒ **§2.5 四态表的第四态相应改为**:
> 「`linked_issue_overlap == null` **且** `unknown_schema_claims == null` 且 `linked_issue_overlap_error` 非空 ⇒ 本轮未取到任何证据」。
> **`unknown_schema_claims` 的合法取值域自此为 `int | null`, `null` ≠ `0`** —— 消费方**不得**用 `.get(k, 0)`。
> **新增 SC-33 (代码, CLI 全链路)**: 夹具让 `read_claims` 抛异常, 带 `--include-terminal` 跑 CLI ⇒ 输出中 **两个键都是 `null`** 且 error 非空;
> **怎么会红**: 只赋 `linked_issue_overlap` 的实现会让 `unknown_schema_claims` 缺席 ⇒ 必红。**baseline 必红**。

**先说为什么不能走 overlap**: `unknown` 被**两道门**丢弃, 且第二道**与 `_TERMINAL` 无关** ——

1. `lib/collision.py:272-273` 的 `if c.status in _TERMINAL:` / `continue`;
2. `lib/collision.py:274-275` 的 `if not getattr(c, "linked_issue", None):` / `continue` ← **第二道门**。`lib/claim_schema.py:165` 的 `parse_claim(` 在 unknown 分支构造 sentinel 时 (`:222-229` 一带) **根本没传 `linked_issue`**, dataclass 默认为 `None` (`lib/claim_schema.py:130`: `linked_issue: Optional[str] = None`) ⇒ **即便把 `unknown` 移出 `_TERMINAL`, 下一行立刻丢弃, 行为逐字节不变**;
3. 且 sentinel 的 `track_id` / `container` / `claimed_at` **全为空串** ⇒ 即使强行放行, §2.3 要求回显的三项全是空字符串。

> **实测复现 (rework v3, 直调 lib)**: `parse_claim({... 'schema_version':'99', 'linked_issue':'10CG/aria-plugin#122' ...})` → `status='unknown'`, **`linked_issue=None`**, `track_id=''`, `container=''`, `claimed_at=''`; 随后 `linked_issue_overlaps([rec], 'my-track', '10CG/aria-plugin#122')` → **`[]`**。⇒ **无论加多少 flag, 该通道恒空**, 除非同时改 `parse_claim` 保留 sentinel 的 `linked_issue` (schema 读取语义变更, blast radius 超本 Spec)。

**⇒ 处置 = 另开一条 additive 输出键 `unknown_schema_claims: int`**:

- **取值**: `read_claims(repo).claims` 中 `status == "unknown"` 的**条数**, **不经 `linked_issue` 匹配** (它读不到);
- **门控**: 该键**仅在传 `--include-terminal` 时**出现。A.1 模板恒带该 flag ⇒ 恒有; Phase B 两个入口都不带 ⇒ **输出逐字节不变**, 与 §非目标「不动 Phase B 入口现有认领」自洽;
- **实现落点**: 把 `scripts/phase1_gate.py:1230` 的 `if args.linked_issue:` 改为 `if args.linked_issue or args.include_terminal:`, 块内 `read_claims(repo)` **只调一次**, 然后按 `args.linked_issue` / `args.include_terminal` 各自填键 (**rework v3 行号订正**: editlist 写于 2026-08-04, 引的是 `:1229`; 实读 aria `d50f9c3` 为 **`:1230`**);
- **消费面措辞**: 见下方四态表第三行, **不得**并入 `linked_issue_overlap[]`, **不得**与 `done`/`abandoned` 同档;
- **已知限 (成文, 只交付一半并说明哪半)**: 本轮**不给**这 N 条提供**路径/身份** —— `read_claims` 的返回类型 `ReadClaimsResult` (`lib/coordination_ref.py:119` 定义 `class ReadClaimsResult(NamedTuple)`, `:596` 定义 `def read_claims(`) 只有 `claims/errors/ref_exists`, unknown 记录进 `claims` 时既无 path 也不入 `errors` ⇒ 供路径要改 NamedTuple 字段, blast radius 超本 Spec, **转 follow-up**;
- **由 SC-24 钉住** (CLI 全链路)。

##### §2.4b 四态契约 (editlist FIX-12(a) + R2/M-4 的修复)

| 信号 | 含义 | 消费面措辞 |
|---|---|---|
| 键**缺席** | **未检测** (既未传 `--linked-issue` 也未传 `--include-terminal`) | 「本轮**未检测**」 |
| `linked_issue_overlap == []` | 已检测, 无碰撞 | 「无碰撞」 |
| `unknown_schema_claims > 0` | **已确认存在** N 条竞品 claim, 本读者读不懂其 schema | 「已检测到 N 条无法解析的 claim —— **存在性已确认、内容未知, 按存在处理**」 |
| `linked_issue_overlap == null` **且** `linked_issue_overlap_error` 非空 | 本轮**未取到任何证据** | 「**未能核实**, 建议重试」 |

> **⚠️ R2/M-4 的修复 (逐字)** —— 没有它, 上表第 2 行与第 4 行在实现上**不可分辨**: 实读 `scripts/phase1_gate.py:1236-1238` 现为 `except Exception as exc:` → `logger.warning(...)` → **`out["linked_issue_overlap"] = []`** ⇒ **异常路径把「什么都没取到」写成了「已检测, 无碰撞」, 且这一步在 `out` 层, 不受 `GateResult.error` 覆盖** (零证据当正证据)。
> **改为**: `except` 分支**不得再写** `out["linked_issue_overlap"] = []`; 改为 `out["linked_issue_overlap"] = None` + `out["linked_issue_overlap_error"] = <非空 token>`。
> **由 SC-25 钉住**「把『已确认存在竞品』与『本轮没取到证据』渲染成同一句的实现必红」+ 断言异常路径的 `null` / `error` 两字段。
> **与 §2.5 的关系**: §2.5 的 `GateResult.error = "fetch_degraded"` 管的是**取 ref 这一步**降级; 本条管的是**算 overlap 这一步**抛异常。**两条都要**, 少任何一条都有一段路径会静默返回 `[]`。

**`include_terminal` 的传递链 (**四**段缺一不可 — R1-fix/C6 补第 0 段)**:

0. **`lib/collision.py` 的 `linked_issue_overlaps` 增 keyword-only 形参** `include_terminal: bool = False` —— 实读 aria `d50f9c3` 的 `lib/collision.py:230-234` 现签名为 `def linked_issue_overlaps(claims, own_track_id, own_linked_issue)`, **三参数, 无该形参**; 不加则 `_main()` 的调用处 (`scripts/phase1_gate.py:1233-1235`) 传参直接 `TypeError`。**⇒ `lib/collision.py` 已补入 Impact 表** (R1 rework 核验 major-2 补, 原表零覆盖)。
   > ⚠️ 与前置 Spec 的边界 (**历史**): `linked-issue-normalization` 的 §非目标写「签名与返回 schema 不变」。本段**要改签名** ⇒ 两 Spec 须协调: 建议由**本 Spec** 承担该签名变更 (前置 Spec 只改内部谓词), 并在前置 Spec 的非目标处加一句「`include_terminal` 形参由 `a1-entry-claim` 引入, 不属本 Spec 变更面」。
   > **✅ 该协调项已完全闭环, 本轮无须再动姊妹 Spec (rework v3 实读复核, 取代旧版的「已解」记述)**: 姊妹 Spec **已 ship 并归档** (`openspec/archive/2026-08-23-linked-issue-normalization/`, v1.67.0 合并提交 `ca52d1c`), 且它在 ship 前**自己写入了**母 Spec 请求的关闭条款 —— 实读 `sed -n '256,260p' openspec/archive/2026-08-23-linked-issue-normalization/proposal.md` 得 `:257` 「⭐ **`include_terminal` 形参由 `a1-entry-claim` 引入, 不属本 Spec 变更面** (owner 裁定 2026-08-08)」+ `:260` 逐字「母 Spec 落地时追加 keyword-only 形参**不视为对本 Spec 的违反, 也不构成回归**」。⇒ **R1 editlist FIX-11 要求的「对姊妹 Spec 的必需编辑」已由姊妹自己完成**, 本 Spec **不编辑归档件** (归档件不可回改)。
   > **行号基线**: 姊妹 Spec 的合并使 `collision.py` 下游行号整体下移 —— `_TERMINAL` 由 `cb6bd5d:210` → **`d50f9c3:268`**; `if c.track_id == own_track_id` 由 `:219-220` → **`:278-279`**; `linked_issue_overlaps` 签名由 `:177-181` → **`:230-234`**。本 Spec 正文与 Impact 表引用的 `collision.py` 行号**统一以 aria `d50f9c3` 为准**, 逐条核对见下方「事实断言逐条实读清单」#3/#4/#5/#6/#16。
1. `phase1_gate.py` 新增 CLI flag `--include-terminal` (store_true);
2. **在 `_main()` 的现有调用处** (`scripts/phase1_gate.py:1233-1235`, 即 `out["linked_issue_overlap"] = linked_issue_overlaps(result.claims…)` 那条语句) 加关键字参数 —— **不碰** `run_gate` / `_run_gate_impl` 签名;
   > R3/C2 实测: `linked_issue_overlaps` 生产代码**只有这一处调用**, 位于 `_main()` (`scripts/phase1_gate.py:1173` 定义)、在 `run_gate` (`:1032` 定义) 返回**之后**独立追加; `_run_gate_impl` (`:335` 定义, 至下一个顶层定义 `run_gate` `:1032` 前 —— R1 rework 核验 minor-4 订正: 原文误记 `334-1075`, 见「事实断言逐条实读清单」#17) 对它 grep 命中 **0**。原 R2-fix 写「`run_gate` 签名透传」**架构上就是错的** —— 照它做会改错函数, 精确复现它自己要修的「生产不可达」。
3. A.1 调用模板**显式带该 flag**。

**SC 的断言层必须是 CLI 全链路**, 不是直调库函数 —— 否则「参数没接到 CLI」的实现仍能绿。

#### §2.5 开关与降级

- **受 `state_scanner.coordination.enabled` 控制**, `false` ⇒ **零调用** (与 Phase B 对称; 由 SC-9 钉 A.1 侧、SC-28 钉 heartbeat 侧, 是**同一条**开关的两半)。`phase1_gate` **本身不读 config**, skip 判断在调用方 SKILL.md 层 ⇒ 该条件须**显式写出**, 否则 opt-out 项目在 A.1 仍被强制写 claim + 推远端 (对未配 coordination ref 的第三方是外向副作用);
- **⚠️ 「不传 `--linked-issue`」是键缺席, 不是空列表 (R2/M-3, rework v3 补 —— 旧版全文零提及)**: 实读 `scripts/phase1_gate.py:1230` 的 `if args.linked_issue:` 是**整块门控** —— 不传该实参时, `out` 里**根本不出现** `linked_issue_overlap` 这个键, 而**不是**出现一个空列表。⇒ 消费面必须先判**键是否存在** (四态表第 1 行「本轮未检测」), 把「键缺席」读成 `[]` 就是把「没查」读成「查了没有」。这也是 §6 缺口表首行 (`无` token 轨零输入) 的机制来源;
- **fetch 降级须进 `error` 契约**: `GateResult.error` 的 docstring (`scripts/phase1_gate.py:210`) **早已预留 `"fetch_degraded"` token 但从未被赋值** (全文无任何 `error=` 赋值用到它 —— 又一个「已 ship ≠ 能用」)。降级时消费面按「**未能核实**」措辞, **不得**渲染成「无碰撞」(零证据不得当正证据)。**与 §2.4b 的 `linked_issue_overlap_error` 是两条不同路径, 不可互相顶替**。

### §3 入口覆盖 (S6)

**实测差距**: coordination ref 里 **2 个**容器, 而 handoff 的 `owner-container` 出现过 **9 种** ⇒ **至少 7 种身份从未留下 claim**。

⇒ **A.1 须双落点**, 与 Phase B 对称 (后者有 `phase-b-developer` + `branch-manager` 两处):
1. `phase-a-planner/SKILL.md`;
2. **`spec-drafter/SKILL.md`** —— 它 `user-invocable: true` (实测 `skills/spec-drafter/SKILL.md:9`), 可直接绕过 phase-a-planner。

> **⚠️ 双落点是本 Spec 的核心杠杆, 却在旧版 SC 全表零覆盖 (R2/M-11)** —— rework v3 补 **SC-22**: 断言两处 SKILL.md **各自**含标题级 `前置: REQUIRE claim` 步骤块 (正则形态 + 非围栏内 + 四字面量 + 幂等谓词), 宿主 = `skills/state-scanner/tests/test_coordination_default_lockin.py` (**扩它, 不另起文件**)。
>
> **两落点同时命中时谁让步 (幂等分工, R2/M-11 后半 + editlist FIX-13)**: `phase-a-planner` 是**主路径** (它的 A.1 会主动委派 `spec-drafter`); `spec-drafter` 的落点只在 (a) **未经 `phase-a-planner` 直接调用** (`user-invocable: true` 路径), 或 (b) `phase-a-planner` 因 skip 条件未走到认领 时生效。**幂等谓词** (`check:` + `if_missing:`, 即 SC-22 第 ③ 项) 保证正常委派路径上**只写一条 claim** —— 没有它, 一次 A.1 会写两条 claim + 两次外向推送, 该实现必须能被 SC-22 判红。
> **⚠️ 落点内部的具体行号 (`phase-a-planner` 的委派动作在第几行 / skip 条件在第几行) 本轮未实读 ⇒ 不写**; A.2 拆任务时须实读补钉 (零发明行号)。

> ## ✅ 阻塞性前提 — 已裁 (R1-fix/C1 — 4 席独立命中 + 主控实读 → 2026-08-22 owner 裁定落版)
>
> **两个指定落点的 `allowed-tools` 都不支持本机制的核心动作。** 实读 frontmatter (**rework v3 复读 aria `d50f9c3` 仍逐字未变**, 见下方「事实断言逐条实读清单」#1/#2):
>
> | Skill | `allowed-tools` (逐字, 变更前) | 缺 |
> |---|---|---|
> | `phase-a-planner/SKILL.md:9` | `Read, Write, Glob, Grep, Task, Skill` | **无 `Bash`** · **无 `AskUserQuestion`** |
> | `spec-drafter/SKILL.md:10` | `Read, Write, Glob, Grep, AskUserQuestion` | **无 `Bash`** |
>
> ⇒ §2 的 `python3 .../phase1_gate.py` 命令**在两个宿主上都跑不了**; §2.3 的 `AskUserQuestion` 请裁**在 phase-a-planner 上也跑不了**。
>
> **⚠️ 扩权与 AD10 的关系 (R2/M-15 配套, rework v3 补)**: 给 `phase-a-planner` 加 `AskUserQuestion` **不在 Layer 2 新增人类参与点** (AD10: 唯一人类参与点是 S7_AWAITING_MERGE) —— 该分支由 §2.3 的 `state_scanner.coordination.unattended` 谓词在**调用前**短路; 无人值守下走 handoff + `awaiting_owner`, 不发问。**反过来也成立**: 正因为扩权后两个宿主都声明持有 `AskUserQuestion`, 「工具是否可用」**不能**再作为无人值守判据 (详见 §2.3)。
>
> **这是整份 Spec 的阻塞项** —— 主机制在它自己指定的执行位置上不可调用, 而三轮审计 + 六条 spike 全都没查过 frontmatter。
>
> owner 2026-08-22 就此下裁。**以下逐字取自 `git show 86540f2:openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md`** (R1 rework 核验 major-3 订正 —— 上一轮此处只保留了「采 (a) 扩权」前半句, 「理由」与「落版义务」两个从句被删并换成下方另起的 (a)/(b) 转述, 与原文有实质偏差且未请复议; 现恢复完整原文字面):
>
> > **✅ owner 裁定 (2026-08-22): 采 (a) 扩权** —— phase-a-planner 加 `Bash, AskUserQuestion`; spec-drafter 加 `Bash`。理由: (b) 放弃 `/spec-drafter` 直调路径的覆盖, 而入口覆盖 (S6: 9 种身份 7 种无 claim) 正是本 Spec 核心目标; 扩权风险由 harness 权限系统兜底 (Bash 调用仍逐条过 permission 配置)。落版义务: Impact 表补两个 SKILL.md 的 `allowed-tools` 变更 + Rule #6 按能力面变更申报 benchmark。
>
> **落版 (AI, 2026-08-23)**:
> - **(a) 扩 `allowed-tools`** [已采纳]: 判否 (b) 是因为 (b) 放弃 `/spec-drafter` 直调路径的覆盖, 而入口覆盖 (S6: 9 种身份 7 种无 claim) 正是本 Spec 核心目标; 扩权风险由 harness 权限系统兜底 (`Bash` 调用仍逐条过 permission 配置);
> - **(b) 改由已持 `Bash` 的宿主代调** [已否]: 例如经 `Task`/`Skill` 委派, 或把认领动作前移到 `state-scanner` 的阶段 4。会改变「A.1 起草前」这个时点的语义且放弃 `/spec-drafter` 直调覆盖, 与 §3 核心目标冲突, 不采纳。
>
> **落版执行** (owner 裁定原文的「落版义务」):
> 1. **Impact 表补两行, 逐字标明变更前后** —— 见下方 §Impact 表 `skills/phase-a-planner/SKILL.md` / `skills/spec-drafter/SKILL.md` 两行 (frontmatter `allowed-tools`);
> 2. **Rule #6 判据影响** (R1 rework 核验 major-4 订正): `allowed-tools` 扩权是 skill **能力面**变更, 影响该 skill **全部**运行场景 (含既有 AB 套件的既有 eval case)。按 `standards/conventions/skill-benchmark-exemption.md` §1「逐 hunk 判, 不逐文件判」核验: `aria-plugin-benchmarks/ab-suite/phase-a-planner.json` / `spec-drafter.json` **两套件均实存** (2026-08-23 实核, 各 2 eval case) ⇒ 该能力面 hunk 落判据表**第二行「处方性 · 运行时指令面 / 能 / 照跑 AB, 零裁量」** —— **须照跑现有两套件**; 与此同时, 本 Spec 新增的 A.1 claim 行为 (a)(b)(c, 见下方 rule6_note 中段) 各自独立归入判据表**第三行「套件覆盖外」**并建定向 fixture。二者**不互相替代**: 照跑 AB 验的是「扩权后 skill 在既有 eval 场景下行为是否漂移」, 定向 fixture 验的是「新增 A.1 claim 行为本身, 现有 eval 结构性覆盖不到」。**订正**: 上一版此处误判「能力面部分不单独申请豁免、也不需要单独判据, 由覆盖该 diff 的定向 fixture 同批覆盖即可」——两套件确实实存, 该误判与 owner 原话「Rule #6 按能力面变更申报 benchmark」(即: 该去申报/跑一次 benchmark) 实质相悖, 现按核实结果订正为「照跑」, 与 owner 原话字面对齐。此判断记入下方 rule6_note 段, 供 A.2 复核。
>
> **✅ 上一轮的「⚠️ 实读订正 · 请 owner 复议」(R1 rework 核验 major-3(b)) 已闭环**: 该条自陈「核实结论 (两套件实存 ⇒ 应照跑) 与 owner 原话字面本就一致, 技术处置**无需另行复议**」, 仅为上一轮措辞偏差的订正留痕; owner 2026-08-23 裁定未对其提出异议。其原文 (逐字) 见 [审计轨 §4](../../../.aria/audit-reports/a1-entry-claim-audit-trail.md#4-3-实读订正--请-owner-复议原文-已闭环)。**若 owner 认为「申报 benchmark」另有所指 (例如指走一遍 `/skill-creator` 完整流程, 而非本版采用的「现有两套件全量跑一遍, 零裁量」), 请在 R3 时指出。**

> **口径待定 (S6 附带发现)**: `owner-container` (形如 `simonfish/bfe8285d`) 与 claim 的 container 段 (`bfe8285d`) **口径已经不同**。本 Spec 采用 claim 侧口径 (uuid), 并把「两标识关系需成文」记为 follow-up —— **不在本 Spec 统一二者** (那会牵动 handoff frontmatter 规范, 属 standards 变更)。

### §4 竞品 spec 探针 — ⛔ **整节已迁出** (owner 2026-08-23 方向 b)

> **迁往**: [`openspec/changes/sibling-spec-probe/proposal.md`](../sibling-spec-probe/proposal.md) —— 原 §4 的全部内容 (`sibling_spec_probe.py` 新脚本 / 扫描范围含 `archive/` / per-round 入口挂载 / fetch 代价与超时预算 / 规模上限 / 消费面与 exit code / 盲区声明) 由该 Spec 承担, 连同 R2 簇 **M-1** (「同 issue」匹配谓词未定义)、**M-5** (「各自默认分支」取法未定义 + in-flight 竞品不可见)、**M-6 的 audit-engine 档**、**M-17 的「§4 无 stdout 契约」子项**, 以及 R1 editlist **FIX-10**。原 SC-16/17/18/19 一并迁出 (见 Success Criteria 表内保留的迁出行)。
> **为什么迁**: R2 的 M-1/M-5 都是 **R1 still-open** 且落在 `audit-engine` 这个与 A.1 认领**不同的宿主**上; `ab-suite/audit-engine.json` 实测**不存在** (rework v3 实核), 使原 rule6_note 的「覆盖外」档按判据表「缺一照跑」根本不成立 —— 这三件都属探针自己的收敛面。
> **依赖方向 (逐字, 不得读成隐式前置)**:
> - **探针 spec 不是主体的阻塞前置。** 主体的 §6 缺口表里「legacy 轨 / 一方跳过入口」两行原写「§4 探针**部分**覆盖」(**R3/TL-M5**: 迁出时必须保留「**部分**」这个限定词 —— 探针自测覆盖率 90.5%, 非全覆盖; 丢掉限定词会把一个已知缺口读成已闭合), 现按实际改为「**由 `sibling-spec-probe` 覆盖, 未 ship 前该缺口无覆盖**」—— 成文, 不假装覆盖。
> - **主体是探针 spec 的语义母体**: 探针的「同一条轨」「同一个 issue」判据一律引用主体 §2.1 的 track-id 契约与 `linked_issue` 语义, 不得自行重定义。

### §5 claim 生命周期 — A.1 引入的新退出路径

> **⚠️ 本节整体按 R2/C-B 重写 (owner 点名必须在此解)**。**旧版的缺陷**: §2.1 的 track-id 不含 slug ⇒ 同一容器在**同一 issue 下试三个方向**时, 三个方向派生的是**同一个** track_id; 而 §5 旧版又写「探索性放弃必须 `release_gate.py --status abandoned`」(该命令形态本身也是错的, 见 §5.2 的命令形态订正)—— 一调即**连坐释放**该 `(container, track_id)` 下的**全部** claim (实读 `lib/claim_lifecycle.py:377` `def release_claim_by_track(` 按 `(container, 归一 track_id)` 定位, `:425` `if rec.container == resolved.container_id`), 把还在做的另外两个方向一并抹掉。

#### §5.1 二分谓词 —— **track-id 形态是否含 slug** (editlist FIX-15; §5 / SC-1 / SC-15 三处**必须用同一句谓词措辞**)

**release 的语义单元, 按 track-id 形态分档**:

| track-id 形态 | 语义单元 | 探索性放弃**一个方向** | **改名** |
|---|---|---|---|
| **issue 派生形** `<basename>-<n>-<uuid>` (**不含 slug**) | **(container, issue)** | **不 release** —— claim 表示「**本容器在做这个 issue**」, 换一个方向不改变该事实; **只有放弃整个 issue** 才调 `release_gate.py --raw-track-id "<本轨 A.1 原串>" --status abandoned` (必需参数见 §5.2 命令形态订正) | track-id **不变** (SC-1) |
| **回落形** `<spec-slug>-<uuid>` (**含 slug**) | **(container, spec)** | **必须 release** —— 每个方向自成 slug、自成一条 track | **release 旧 + acquire 新**两步 (SC-15) |

**判据一句话 (三处逐字复用)**: **「track-id 形态是否含 slug」** —— 含 slug ⇒ 语义单元是 (container, spec); 不含 slug ⇒ 语义单元是 (container, issue)。

> **⚠️ 判定式 (R3/TL-M4 补 —— 原文自称「可机械判定」却没给判定式)**:
>
> **两个看似显然的判定式都不成立, 逐条否决**:
> 1. **从 track_id 字符串反推** —— **有歧义**。反例逐字: `fix-issue-149-a1b2c3d4` 既可读成 `<basename=fix-issue>-<149>-<uuid>` (issue 派生形), 也可读成 `<spec-slug=fix-issue-149>-<uuid>` (回落形)。
> 2. **读 `claim.linked_issue` 是否非空** —— **对第三类给出相反答案**。本表 D12 的原依据 (editlist FIX-15) 已经点名过这一类: **「有 issue 却走回落形的后起 Spec」** —— 同 issue 的第二份 Spec 因 issue 派生形的 track_id 已被占用而落在**含-slug 形**, 它的 `linked_issue` **非空**却是回落形。
>    > **⚠️ 留痕 (主控 2026-08-25)**: 本轮修 TL-M4 时**一度采用了 (2)**, 并在恢复 D12 第三列时才发现原依据早已否决它 —— 即 memory `feedback_rationale_formula_contradiction_is_signal`「理据↔公式矛盾时别默认公式对, 理据常在保护公式漏掉的场景」。该误判已撤, 留此记形状。
>
> ⇒ **落版判定式 = 把形态显式记进 claim**: claim 增 additive 字段 **`track_form: "issue" | "slug"`**, 由**派生代码在 acquire 时按自己走的分支写入** (它当然知道自己走了哪支), 消费侧**零推断**。
> - 与 §5.3 的 `spec_slug` 同批引入, 同为 additive、同不 bump `schema_version`;
> - 旧 claim 无该字段 ⇒ 读作 `None`。**⚠️ K2 (R4) 订正 —— 此处原写「fail-CLOSED」是错的命名, 且与 §5.3 相反**:
> 「退回 ALL matching」正是 §5.3 自己逐字否决过的**连坐**, 它是 **fail-OPEN** (更危险的方向), 不是 fail-CLOSED;
> 且 §5.3 同时写着「只释放三元组匹配」⇒ **同一条 legacy claim 两个相反答案** (实跑: 释放 `[s1,s2,s3]` vs `[s2]`)。
> **落版 (2026-08-27, 未经审计轮)**: `track_form is None` ⇒ **不释放, 报错退出并点名该 claim**,
> 要求操作者显式传 `--spec-slug` 或 `--force-legacy-release-all` 二选一。理由: 上线当天**全部存量 claim** 都走这条路径,
> 让它默认走「释放全部」等于**默认连坐**; 而 release 是可重试的, 报错的代价远小于误释放。
> **新增 SC-31 (代码)**: 对一条无 `track_form` 的 legacy claim 跑 D.2b release ⇒ **非零退出 + 输出点名该 claim + 零 claim 被改写**;
> 带 `--force-legacy-release-all` 重跑 ⇒ 释放全部匹配。**怎么会红**: 默认释放全部的实现在第一臂必红。**baseline 必红**。
>
> 「含 slug」保留为**人类可读的名字**, `track_form` 字段是它的**机械定义**; SC-1 / SC-15 / SC-27 三处一律按该字段判, 夹具**不得预标形态**, 而应**跑派生代码让它自己写** (R3/TL-M4 点名: 预标形态的夹具对本缺陷免疫)。

#### §5.2 退出路径表 (按 §5.1 的谓词分档)

> **⚠️ 命令形态订正 (rework v3 实读)**: 旧版全文写的 `release_gate.py --status abandoned` **会直接 `parser.error` 退出** —— 实读 `git -C aria show d50f9c3:skills/state-scanner/scripts/release_gate.py | sed -n '236,237p'` 得
> ```python
>     if not args.raw_track_id and not args.sweep_stale and not args.gc:
>         parser.error("至少需要 --raw-track-id / --sweep-stale / --gc 之一")
> ```
> ⇒ 本节所有 release 调用**一律带 `--raw-track-id "<本轨 A.1 原串>"`** (`--status abandoned` 只指定写入的状态值, 不满足「三选一」)。**这条 baseline 即可证伪**: 照旧版字面写的实现连 CLI 都进不去。

| 路径 | 处置 |
|---|---|
| **探索性放弃一个方向** (A.1 试三个方向弃两个) | **按 §5.1 分档**: issue 派生形 ⇒ **不 release** (claim 继续代表「本容器在做这个 issue」); 回落形 ⇒ **必须**调 `release_gate.py --raw-track-id "<本轨 A.1 原串>" --status abandoned`。义务写进 SKILL.md + **SC-27** (两臂可辨) |
| **放弃整个 issue** (不再做这个 issue 的任何方向) | **两种形态都必须** `release_gate.py --raw-track-id "<本轨 A.1 原串>" --status abandoned` |
| **slug 改名** | **issue 派生形** (判定式 = `claim.track_form == "issue"`, 见 §5.1; **既不从 track_id 反推、也不看 `linked_issue`**): track-id 不含 slug ⇒ **改名不改 id**, 问题从源头消失 (SC-1)。**回落形 (含 slug)**: 须走 **release 旧 + acquire 新** 两步 (SC-15) —— `release_claim_by_track` 按 `(container, 归一 track_id)` 定位、**不依赖 session**, 可直接照字面实现 |
| **A.1 成功并走完循环** (最常见, R2/C-C) | **A.1 原串即 carry-id, B.0 与 D.2b 逐字节复用** (§2.1b) ⇒ D.2b 的 `release_claim_by_track` 能匹配到 A.1 那条 claim。**由 SC-23 钉住**。**不靠 sweep 兜底** —— sweep 只是 GC, 不是设计中的释放路径 ⚠️ **但 release 的作用域有缺陷 —— 见 §5.3 (R3/TL-C1)** |
| **D.2b 对偶** | 只有**走完循环**的轨才到 D.2b; 上面「探索性放弃 / 放弃整个 issue / 回落形改名」三条**不经过它**, 故各自显式 release。⚠️ **issue 派生形下 D.2b 的 release 会连坐同 issue 的其他在制方向 —— 处置见 §5.3** |

#### §5.3 D.2b 的 release 作用域 —— C-B 的另一半 (R3/TL-C1)

> **R3 判定 C-B「只闭一半」**: §5.1/§5.2 解决了「探索性放弃**一个方向**不 release」, 但**漏了对偶路径** ——
> 方向 1 **走完循环**到 D.2b 时, `release_claim_by_track` 的 docstring 逐字写着
> 「If several active claims match (**same container re-claimed a track across sessions — the NORMAL case, since every session mints a fresh session_id and B.0 REQUIRE-claim runs per session**), **ALL matching active claims are released**」
> (`lib/claim_lifecycle.py`, `release_claim_by_track` docstring; 实读基线 `d50f9c3`)。
>
> **⚠️ 引文订正 (R4/code-explorer 抓, 主控复核确认自己错了)**: 本段上一版把该 docstring 引成「If several active claims match **(same session)**, ALL matching…」。**原文没有「same session」这四个字** —— 实读 `claim_lifecycle.py:396-399` 逐字为上方新引文。**错法**: 主控当初跑的是 `sed -n '387,400p' | grep -iE "all|matching"`, grep **丢掉了不含关键词的 `:397-398` 两行**, 而主控把返回的 `:396` 与 `:399` 当作相邻行**拼接**成了一句 —— 造出一句原文不存在、且语义方向相反的引文。**机械核验器对此天然免疫** (两行都真实存在), 这是「该行存在 ≠ 该断言属实」的又一实例。
>
> **⇒ 订正后 C1 的结论不但不弱, 反而更强**: 原文明说多条 claim 匹配同一 track 是「**同一容器跨 session 重新认领 — the NORMAL case**」, 因为每个 session 都生成新 session_id 且 B.0 每 session 都跑 ⇒ **同 track 多 claim 是常态而非边角**, D.2b 的 ALL-matching 释放因此**几乎必然**触及仍在制的其他方向。
> 而 issue 派生形下, 同 issue 的 N 个方向**共用同一个 track_id** (各自 session 不同) ⇒
> **方向 1 收尾会把仍在制的方向 2/3 的 claim 一并释放**。SC-27 原本只有两臂, 结构性抓不到这条。

**处置 (落版) — claim 增 additive 字段 `spec_slug`, release 按 (container, 归一 track_id, spec_slug) 定位**:

| 项 | 内容 |
|---|---|
| **新增字段** | claim schema 增 `spec_slug: Optional[str]` (**additive**, 与 Part B1 引入 `linked_issue` 同款: 旧 reader 忽略未知字段, 不 bump `schema_version`) |
| **写入点** | A.1 acquire 时写入本 Spec 的目录名 (`openspec/changes/<slug>/`); 回落形的 track_id 本就含 slug, 该字段与其冗余但**不矛盾** |
| **release 定位** | D.2b 传 `--spec-slug "<本 cycle 的 spec 目录名>"` ⇒ 只释放 `(container, 归一 track_id, spec_slug)` 三元组匹配的 claim; **未传该参数时行为逐字节不变** (= 现状 ALL matching), 故 **Phase B/D 既有调用零影响** |
| **为什么不用 track_id 承载方向** | 把方向塞进 track_id 会同时破坏 C-B 的第一半 (三方向变三条 track ⇒ 同 issue 的 overlap 检测退化) 与 C-C (carry-id 一致性)。`spec_slug` 作**独立字段**让 track_id 继续只承载「哪条 issue」, release 另有维度可用 |

> ## 🔴 K1/K4 (R4) — 两个新字段的**透传面**与**写入路径** (2026-08-27 补, 未经审计轮)
>
> **R4/type-design A-C1 实读**: `heartbeat()` 在 `lib/claim_lifecycle.py:244-256` **逐字段重建** `ClaimRecord`
> (显式列 11 个字段, 含 `linked_issue=existing.linked_issue`), **不是** `dataclasses.replace`。
> ⇒ 不同步改这一段, `spec_slug`/`track_form` **每次 heartbeat 都被抹掉** —— 而本 Spec 的核心正是
> 「每次 `/state-scanner` 跑 heartbeat」⇒ **字段活不过第一次心跳, §5.3 的 release 三元组永不匹配, C-C 回归**。
>
> **R4/pr-test C-3 实读**: Impact 原只给 `release_gate.py` 加 `--spec-slug` (**读取端**),
> 而 `phase1_gate.py` 无对应 flag、Spec 又明写「不碰 `run_gate`/`_run_gate_impl` 签名」⇒ **写入端缺失**,
> SC-27(C) 的 CLI 全链路夹具**不可构造**。
>
> ### 透传面逐条枚举 (照 `linked_issue` 先例; **不枚举就等于没做**)
>
> 先例实测: `git -C aria grep -c "linked_issue=" d50f9c3 -- skills/state-scanner/` ⇒
> `claim_lifecycle.py:4` · `claim_schema.py:1` · `gc.py:1` · `phase1_gate.py:5` · `tests/test_release_by_track.py:6`
> = **17 处 / 5 个文件**。两个新字段**各自**需要同等覆盖:
>
> | # | 落点 | 动作 |
> |---|---|---|
> | 1 | `lib/claim_schema.py` `ClaimRecord` | 加两个 `Optional[str] = None` 字段 + `parse_claim` 读取 + `to_dict`/序列化写出 |
> | 2 | `lib/claim_lifecycle.py::acquire_claim` | **写入**两字段 (`track_form` 由派生分支自己写) |
> | 3 | **`lib/claim_lifecycle.py::heartbeat` `:244-256` 的逐字段重建** | **必须加两行** `spec_slug=existing.spec_slug` / `track_form=existing.track_form` —— **K1 的本体** |
> | 4 | `lib/claim_lifecycle.py::release_claim` / `release_claim_by_track` | 同样的重建/写回路径逐一核 (凡逐字段构造 `ClaimRecord` 的地方都要加) |
> | 5 | `lib/gc.py` (`sweep_stale_active` 改写 status 时) | 同上 |
> | 6 | **`scripts/phase1_gate.py` 的 A.1 acquire 路径** | **新增 `--spec-slug` CLI flag** 并透传给 `acquire_claim` —— **K4 的本体**; `track_form` 由派生逻辑内部决定, 不走 CLI |
> | 7 | `scripts/release_gate.py` | 已有 `--spec-slug` (读取端) |
> | 8 | `tests/` | 两字段各自的往返测试 (见 SC-30) |
>
> **⚠️ 关于「不碰 `run_gate`/`_run_gate_impl` 签名」**: 该承诺**维持** —— `--spec-slug` 与 `--include-terminal` 同款,
> 在 `_main()` 内解析并传给 `acquire_claim`, **不进** `run_gate` 的公开签名。若 A.2 发现无法绕开, 属**超出本 Spec 承诺**, 须上呈。
>
> **新增 SC-30 (代码, 往返)**: acquire (带 `--spec-slug`) → **跑一次 heartbeat** → 读回 claim ⇒ 两字段**逐字节不变**。
> **怎么会红**: 不改 `:244-256` 逐字段重建的实现, heartbeat 后两字段变 `None` ⇒ 必红。**baseline 必红** (字段今天不存在)。
> **这条是 K1 的验收本体, 缺它则 K1 的修复无法证伪。**

> **⛔ 已考虑并否决的替代**: 「不加字段, 接受连坐 —— 幸存方向在下一次 B-entry 的 `phase1_gate` 会自动重新 acquire」。
> **否决理由**: 从 D.2b 到下一次 B-entry 之间, 幸存方向**处于无 claim 状态** ⇒ 对其他容器不可见 —— 这正是本 Spec 存在要关闭的那个窗口。
> 用「事后自愈」换「窗口期不可见」是**本 Spec 自我否定**。该替代方案与其残余窗口一并成文, 供 R4 复核本裁断。

> **⚠️ 本条是 rework v3 之后新增的设计裁断 (主控 2026-08-25), 未经任何审计轮** —— 请 R4 优先审它。


### §6 残余缺口 (成文, 不假装覆盖)

| 缺口 | 窗口 | 覆盖它的机制 |
|---|---|---|
| **⭐ 本轨的「关联 Issue」token 为 `无` 或字段缺席** (R2/M-3 + editlist FIX-12(d) 补 —— 旧版全表没有这一行, 而它是**最大的单项缺口**) | 无界 | **无** —— 此时 A.1 模板**必须省略** `--linked-issue` (否则两份无关 Spec 互相误报, 见 §2 的 NEW-01), 而 `scripts/phase1_gate.py:1230` 的 `if args.linked_issue:` 是**整块门控** ⇒ 主机制**零输入**, 且输出里 `linked_issue_overlap` **键缺席** (不是 `[]`, 见 §2.5)。字段可得性由 [`linked-issue-field-availability`](../linked-issue-field-availability/proposal.md) 承担, **它 ship 前该缺口无覆盖**; 该子 Spec **不是本 Spec 的阻塞前置** —— 本 Spec 在字段缺席时的行为是**已定义的退化** (零输入 + 键缺席), 不是未定义行为 |
| 双方都未 claim 且未 push | 秒级 (claim 推送延迟) | 无 |
| 一方跳过 A.1 直调 `/spec-drafter` | — | **§3 双落点已覆盖** (由 SC-22 钉住两处落点各自存在) |
| 一方 `coordination.enabled=false` | 无界 | 无 (设计如此, opt-out 是项目的权利) |
| legacy 轨 (不用 phase1_gate 的历史/第三方容器) | 无界 | **原写「§4 探针部分覆盖」—— §4 已迁出** ⇒ 现由 [`sibling-spec-probe`](../sibling-spec-probe/proposal.md) 承担, **它 ship 前该缺口无覆盖** (S6: 7/9 身份属此类)。成文, 不假装覆盖 |
| 竞品**已 ship 并归档** (在 `openspec/archive/` 下) | 无界 | **同上** —— 原属 §4 探针的两个专有场景之一, 随 §4 迁出 |
| **存量 active claim 是旧形态** (无容器段) 的过渡期断链 | 至旧 claim 自然 GC 退场为止 | 无 (§2.1b 已知限: 本 Spec **不改写存量 ref**) |

**中心化 spec 登记表: 仍然不做 (spike S6, 依据全换)**。原依据「残余缺口仅秒级」是实质低估, 已作废。新依据: **登记表解决不了这些缺口** —— 它们共同根因是「**没走进入口**」, 换个存储位置不改变这一点, 它是同一问题的另一载体而非解法; 真正的杠杆是**入口覆盖率** (实测 9 vs 2), 即 §3 的方向。登记表的一致性/并发写/GC 是常驻成本, 收益却依赖同一个前提。

---

## 事实断言逐条实读清单 — ⛔ **整表已切出**

> **迁往**: [审计轨 §5](../../../.aria/audit-reports/a1-entry-claim-audit-trail.md#5-事实断言逐条实读清单) —— **⚠️ 搬运性质分节陈述 (R3/CR-M-M1 订正 —— 原写「按字节搬运, 未重写任何一句」对 §5 **为假**, 主控担责)**: 审计轨 **§1 (轮次轨迹表)** 是**逐字搬**, CR 席 diff 确认连续块命中; 审计轨 **§5 (事实断言实读清单)** **不是**纯搬运 —— 该表在本轮**先**按新基线 `d50f9c3` 重测重生成 (含新增 #18–#34), **然后**才移出, 与已提交前身相比 22/29 行找不到。§2/§3/§4 各含一条本轮新写的编者注。⇒ 「无损搬运 ⇒ 撤回成本低」这条安全性论证**只对 §1 成立**。34 行断言表 (原 #1–#17 订正 + rework v3 新增 #18–#34) 全部在那里。
> **切分理由 (主控 2026-08-25 裁定, 已标请 owner 复议)**: 该表是**核验证据**不是交付面 —— 与姊妹 Spec 2026-08-07 owner 裁定「交付面与审计史切开」同类; 且它可由 `verify_line_refs.py` 随时重新生成, 不需要人肉维护在交付面里。
> **本文件正文里所有 `文件:行号` 引用的实读基线 = aria 子模块 `d50f9c3`** (= v1.67.1 `58a49e7` + 2 commit)。**复核命令 (逐字)**: `git -C aria show d50f9c3:<path> | sed -n '<N>p'`。主仓语料口径的基线 = `cc1bdef`。
> **正文里形如「见清单 #N」的交叉引用**, 一律指审计轨 §5 表内的第 N 行。
> ⚠️ 审计轨是 append-only 且**不维护与本文件的一致性** —— 若二者行号不一致, **以本文件正文为准**, 并按上面的复核命令重新实读。

---

## 决策记录

| # | 决策 | 依据 |
|---|------|------|
| D1 | ~~「关联 Issue」字段可得性提为 §1~~ ⇒ **⛔ 已随 §1 迁至 [`linked-issue-field-availability`](../linked-issue-field-availability/proposal.md)** (owner 2026-08-23 方向 b) | 原依据 `141/13/9%` 已作废 —— rework v3 实测口径见「事实断言逐条实读清单」#30 |
| D2 | ~~字段格式固定 `<org>/<repo>#<n>` + custom check (warning)~~ ⇒ **⛔ 已随 §1 迁出** (同上) | 同上 |
| D3 | track-id = `<basename>-<str(int(n))>-<container_uuid>` | **S3**: 不含容器段则两轨同 id ⇒ 被 `lib/collision.py:278-279` 互斥 ⇒ 主机制死 (R2/C1); uuid 不截断不用 label (label 碰撞域不可控且模板鼓励设置)。**⭐ rework v3 补注 —— 更简的备选已被实测证伪**: 「去掉容器段, 靠 reconcile 同名碰撞 (7c) 报警」不成立 —— 7c 只在竞品未 stale 时触发 (`_takeover_eligible` 命中即走 7d「No prompt needed」零 surface), 而 `heartbeat()` 生产调用点为 0 (`lib/constants.py:43-44`) + `STALE_TTL`=1800 ⇒ 事故窗 (48–72h) 内同名通道**结构性静默** (= Aria #180); 而 overlap 通道 (`lib/collision.py:265-292`) **不做新鲜度过滤**, 对 stale claim 同样可见。⇒ **容器段的真正作用是把碰撞检测从新鲜度脆弱的通道挪到新鲜度免疫的通道** (详见 §2.1) |
| D4 (**⛔ 已被 D16 取代 — R3/BA-M2 订正**) | ~~heartbeat 匹配键**改** `(container, track_id)`~~ ⇒ **以 D16 为准: 增 by-track 并存变体, 不改既有 `heartbeat()` 的 `(container, session)` 键**。旧措辞是 R2/M-17 第 2 项点名的两读之一, §2.2 `:188` 与 D16 已统一而本行残留未同步 | **S1**: `release_claim_by_track` 为**同一 defect** 做过同款修法, 照抄即可; session 落盘方案被它取代 |
| D5 | `include_terminal` 在 **`_main()` 现有调用处**加参数, 不碰 `run_gate` 签名 | **R3/C2** 实测: `linked_issue_overlaps` 只在 `:1233` 被调用 (rework 订正: 原 R3 记 `:1232`, 实读为其下一行), `_run_gate_impl` 零命中 |
| D6 | 「接手」= **两步人工**, 不引入跨容器 release | **S3** 实测无该函数; 既有 takeover 路径对本场景不可达; 写别人的 claim 是权限面变更 |
| D7 | ~~探针自带 fetch, 不称轻量, 配 30s 预算 + 重试~~ ⇒ **⛔ 已随 §4 迁至 [`sibling-spec-probe`](../sibling-spec-probe/proposal.md)** (owner 2026-08-23 方向 b) | **S2** 实测数据一并移交该 Spec |
| D8 | A.1 双落点 (phase-a-planner + spec-drafter) | **S6** 实测入口覆盖率是杠杆 (9 身份 vs 2 在 ref); `spec-drafter` `user-invocable: true` 可绕过 |
| D9 | 不建 basename 别名表 | **S4**: 在真实输入总体上别名实例 = 0; 分隔符型别名已由前置 Spec 的 S5 追加覆盖 |
| D10 | 不做中心化登记表 | **S6**: 解决不了「没走进入口」这个共同根因 |
| D11 | ~~探针不阻断, 命中 exit 0; 非 0 仅用于探针自身失败~~ ⇒ **⛔ 已随 §4 迁出** (同 D7) | — |
| **D12** (新) | **release 的语义单元按 track-id 形态分档**; **形态的机械判定式 = 读 claim 的 additive 字段 `track_form`** (R3/TL-M4: 从 track_id 字符串反推**有歧义** —— 反例 `fix-issue-149-<uuid>`; 读 `linked_issue` 则对「有 issue 却走回落形的后起 Spec」**给相反答案**; 两者均已否决, 见 §5.1), 含 slug ⇒ (container, spec) 必 release; 不含 slug ⇒ (container, issue) | **R2/C-B** + **editlist FIX-15** (谓词选「是否含 slug」而非「有没有关联 issue」—— 后者对「**有 issue 却走回落形的后起 Spec**」这第三类给出相反答案) + **R3/TL-M4** (该谓词的机械判定式 = 新增 additive 字段 `track_form`, 见 §5.1) |
| **D13** (新) | **A.1 派生的原串即本 cycle 的 carry-id**, `phase-b-developer` B.0 / `branch-manager` / `phase-d-closer` D.2b 三处逐字节复用 (editlist FIX-14 **选项 A**) | **R2/C-C**: `lib/track_id.py:61-76` 归一四步不含去容器段逻辑 ⇒ 两个不同原串归一后必是两个 track_id, 没有任何归一层能把 A.1 与 D.2b 接上。选 A 而非 B (D.2b 额外再调一次 release) 是因为 A 是**一处定义三处复用**, B 是在收尾处打补丁。**边界**: 只改 carry-id 取值口径, 不改 Phase B 闸门语义 (见 §2.1b) |
| **D14** (新) | `unknown` **另开 additive 键 `unknown_schema_claims: int`**, 不并入 `linked_issue_overlap[]` (editlist FIX-03) | **实测证伪**了「加 flag 让它走 overlap」这一支: `parse_claim` 的 unknown sentinel 不带 `linked_issue` (`lib/claim_schema.py:130` 默认 `None`), 被 `lib/collision.py:274` 第二道门丢弃 ⇒ **该通道恒空**, 与 `_TERMINAL` 无关。只给 count 不给路径 —— 路径需改 `ReadClaimsResult` (`lib/coordination_ref.py:119`) 字段, 超本 Spec, 转 follow-up (**成文声明哪半没给**) |
| **D15** (新) | 无人值守判据 = **新 config key `state_scanner.coordination.unattended`** (boolean, default false), **禁止**用「`AskUserQuestion` 是否可用」做运行期推断 (editlist FIX-16) | **R2/M-15**: C1 扩权后两个宿主都声明持有 `AskUserQuestion` ⇒ 该谓词恒为「可用」, 分支永不进入 (「上一批 fix 亲手抹平了下一批 fix 的判据」)。key 须同时在 `config-loader/SKILL.md` 登记**与** `DEFAULTS.json` 注册 (后者现连 `coordination` 都没注册, 见清单 #26) |
| **D16** (新) | heartbeat **增 by-track 并存变体**, 不改既有 `heartbeat()` 的 `(container, session)` 键 | **R2/M-17 第 2 项**: 旧版正文「改匹配键」与 Impact「增并存变体」两读。改既有键会动 Phase B 现有认领路径 (撞 §非目标); 并存则 Phase B 逐字节不变, 且形态照抄同文件已有的 `release_claim` (`:274`) / `release_claim_by_track` (`:377`) 并存模式 |

**Rule #6 (rule6_note)** — **rework v3 整段重写** (R2/M-6: 旧版把 `audit-engine` 列进「覆盖外」档, 但点名行为 (a)(b)(c) **无一是 audit-engine 的**, 且 `ab-suite/audit-engine.json` **实测不存在** ⇒ 按判据表「缺一照跑」该档根本不成立; 另 R2/M-6 指出旧 substitute **SC-9 无效**):

**本 Spec 涉及的 SKILL.md / frontmatter 改动 = 实数 6 处**, 逐档列清 (**不写「五处」之类未逐项列的计数**):

| # | 落点 | 性质 | 判据表落档 | 处置 |
|---|---|---|---|---|
| 1 | `phase-a-planner/SKILL.md` frontmatter `allowed-tools` (`:9`, 加 `Bash, AskUserQuestion`) | **能力面** (影响该 skill **全部**运行场景, 含既有 eval case) | 第二行「处方性 · 运行时指令面 / 能 / 照跑 AB, 零裁量」 | **照跑现有 `ab-suite/phase-a-planner.json`** (实测存在, `evals` = 2) |
| 2 | `spec-drafter/SKILL.md` frontmatter `allowed-tools` (`:10`, 加 `Bash`) | 同上 | 同上 | **照跑现有 `ab-suite/spec-drafter.json`** (实测存在, `evals` = 2) |
| 3 | `phase-a-planner/SKILL.md` 正文新增「前置: REQUIRE claim」认领步骤 | 处方性 · **套件覆盖外** | 第三行 | 点名行为 (a)(b)(c) + 定向 fixture, 见下 |
| 4 | `spec-drafter/SKILL.md` 正文新增「前置: REQUIRE claim」认领步骤 (第二落点) | 同上 | 同上 | 同上 |
| 5 | `state-scanner/SKILL.md` 新增「Layer L A.1 heartbeat 集成」小节 | 处方性 · 运行时指令面 | 第二行「照跑 AB, 零裁量」 | **照跑现有 `ab-suite/state-scanner.json`** (实测存在, `evals` = 12) + 在**该既有套件内新增 1 个 eval case** 钉点名行为 (d) |
| 6 | `config-loader/SKILL.md` 登记 `coordination` 的 A.1 skip 语义 + `unattended` 新 key | **描述性** (登记既有/新增字段, 不改任何 AI 决策路径) | 第一行「描述性 / 不适用 / substitute」 | **substitute 见下方 (已换, 旧 SC-9 无效)** |

**⛔ 旧版的第 7 档 `audit-engine/SKILL.md` + `references/execution-modes.md` 随 §4 迁至 [`sibling-spec-probe`](../sibling-spec-probe/proposal.md)**, 连同它的 AB 缺口问题 (`ab-suite/audit-engine.json` 不存在) 一并由该 Spec 判据。本 Spec **不再对 audit-engine 提出任何 Rule #6 主张**。

**「覆盖外」档的三条 (缺一不可)** —— 对应上表 #3/#4:

1. **点名行为**: (a) A.1 起草前必调 `phase1_gate.py` 且传 `--linked-issue` (token 为 `无` 时**省略**该实参); (b) overlap 非空 (或 `unknown_schema_claims > 0`) 时经 `AskUserQuestion` 请裁而非自行放行 —— **`unattended == true` 时改走 handoff + `awaiting_owner`**; (c) fetch 降级 / overlap 异常时按「未能核实」而非「无碰撞」;
2. **建可证伪定向 fixture**: 上述三条各一个 eval, **双臂须能分辨**; 另加 (e) `unattended` 臂 (对应 SC-26);
3. **套件缺口开 issue**: 与 `aria-plugin#117` (缺 authoring 维度) / `#127` (缺 D9 surface 维度) 同族, 归并或新开由 A.2 定。

**「照跑 AB」档的点名行为 (d)** —— 对应上表 #5: 「**持有 active claim 且 `coordination.enabled == true` 时, 每次 `/state-scanner` 入口调用都触发 `phase1_gate.py --heartbeat-only` 刷新该 claim; `enabled == false` 时零触发**」(与 SC-21 / SC-28 呼应)。它**属于**「照跑 AB」义务的一部分 (在既有套件内加 case), **不是**另起「覆盖外」fixture —— 刻意不塞进上面 (a)(b)(c) 清单, 否则会把同一处 SKILL.md diff 同时判进两档。

**⭐ 描述性档的 substitute (R2/M-6 命中点, 已换)**: 旧版记 substitute = **SC-9**, 但 SC-9 断言的对象是 **SKILL.md 散文** (「A.1 零调用」这一 AI 行为), **无代码宿主、不可机械断言** ⇒ 作为描述性档的 substitute **无效**。**改为**:

> **substitute = 结构化测试「`DEFAULTS.json` 注册的 `coordination` 三键 (`enabled` / `mode` / `unattended`) 与 `config-loader/SKILL.md` 的登记值逐字一致」** (宿主 `skills/state-scanner/tests/` 或 config-loader 既有测试宿主, A.2 定)。
> **它怎么会红**: **baseline 必红** —— 实读 `git show d50f9c3:skills/config-loader/DEFAULTS.json` 的 `state_scanner` 段**根本没有 `coordination`** 这个键 (见「事实断言逐条实读清单」#26), 而 `config-loader/SKILL.md:134`/`:140` 已登记 `enabled`/`mode`。⇒ 这是一条**真的可机械断言、且现在就是红的**测试, 不是恒真的形式主义 (memory `check-runs-at-baseline-first` / `false-green-dual-is-permanent-red`)。
> **SC-9 本身不删**, 只是**类别订正为「行为 (定向 fixture)」** (见 Success Criteria 表)。

**能力面附注 (C1 落版义务, 2026-08-22; R1 rework 核验 major-4 重判, rework v3 复核数据未变)**: 上表 #1/#2 的 `allowed-tools` 扩权与 #3/#4 的**指令面**变更虽落在同一份 SKILL.md diff 里, 但按 `standards/conventions/skill-benchmark-exemption.md` §1「**逐 hunk 判, 不逐文件判**」分属两档: 能力面 hunk ⇒ **照跑现有两套件** (验「扩权后 skill 在既有 eval 场景下行为是否漂移」); 指令面 hunk ⇒ **覆盖外定向 fixture** (验「新增 A.1 claim 行为本身, 现有 eval 结构性覆盖不到」)。**二者各自独立、互不替代。** 上一版曾误判「能力面部分不单独申请豁免、也不需要单独判据」, 与 owner 原话「Rule #6 按能力面变更申报 benchmark」实质相悖, 已订正 (过程留痕见 [审计轨 §4](../../../.aria/audit-reports/a1-entry-claim-audit-trail.md#4-3-实读订正--请-owner-复议原文-已闭环))。

确定性代码层由 SC 覆盖, 与上述并行不互替。**不申请豁免。**

---

## Success Criteria

> **验证面分层** (R1/C4: 原版把 SC 挂在**不存在的** `phase-a-planner` 测试宿主上):
>
> | 类 | 宿主 | 可机械断言 |
> |---|---|---|
> | 代码类 | `skills/state-scanner/tests/` (既有宿主; `audit-engine/tests/` 随 §4 迁至 `sibling-spec-probe`) | ✅ |
> | 行为类 | **定向 AB fixture** (rule6_note「覆盖外」档第 2 条) | ⚠️ 只能由 eval 覆盖, **不冒充结构化测试** |
>
> **⚠️ 编号纪律 (rework v3 继续遵守)**: SC 编号**只追加, 不重排, 不复用**。迁至子 Spec 的 SC **保留行号并写明去处**, 不删行; 撤销的 SC **保留行号并标 ⛔**, 不删行。子 Spec 各自从 SC-1 重新编号 (独立命名空间), 并在其头部注明与本 Spec 旧编号的对应。

### 四个被推翻版本的红窗 (spike S3 强调: 缺一则第五版会再踩)

> **⚠️ 被测对象与宿主 (R2/M-17 第 1 项补 —— 旧版这四条没有宿主, 是「无被测对象的 SC」)**: §2.1 的拼接**没有代码宿主** (见 §2.1a), 故 SC-1~SC-4 一律**分两层**: **文本层**断言两处 SKILL.md 的 A.1 步骤块里 `--raw-track-id` 占位串的**字面**, 宿主 = `skills/state-scanner/tests/test_coordination_default_lockin.py` (与 SC-22 同宿主); **行为层**断言 AI 实际拼出的串, 宿主 = 定向 AB fixture。

| SC | 钉住哪一版的失败 | 场景 → 期望 | 宿主 | 怎么会红 |
|----|---|---|---|---|
| **SC-1** | 原始版 (spec-slug ⇒ 改名孤儿) | track-id 为 **issue 派生形** (`<basename>-<n>-<uuid>`, **不含 slug** —— 与 §5.1 / SC-15 **逐字同一句谓词**) 的轨: slug 改名前后 track-id **不变** | 文本层 + 行为层 | 占位串写成 `<spec-slug>-…` (含 slug) 的实现必红; 当前两处 SKILL.md **根本没有** A.1 步骤块 ⇒ baseline 必红 **⚠️ 类别 (R4/K3)**: **行为 (定向 fixture)** —— K3 降级 —— 派生无代码宿主 ⇒ 本条**不得**写成代码类; 它只能由 AB eval 分辨「AI 是否按 §2.1 规则拼串」, **不冒充结构化测试** |
| **SC-2** | R1-fix 版 (纯 issue 派生 ⇒ 主机制死) | 两**不同容器**同 issue 各自 A.1 认领 ⇒ 双方 `linked_issue_overlap` **各含对方** | 代码 (CLI 全链路) | 去掉容器段的实现被 `lib/collision.py:278-279` 自排除 ⇒ 双方 overlap 恒空 ⇒ 必红 **⚠️ 恒绿风险已堵 (R3/QA-F2)**: QA 席实读 `tests/test_release_by_track.py:533` 的 `test_linked_issue_written_and_overlap_surfaced` —— 它传**两个手写的、不含容器段的** track 名, **今天就绿** ⇒ 若 SC-2 的夹具照它写, 本条**测不出**「容器段被丢弃」这个它声称钉住的 R1-fix 回归。 ⇒ **SC-2 的夹具硬约束**: 两条 track-id **按 §2.1 规则手写拼接**(**R4/C-1 订正 —— 主控担责**: 上一版写「必须由 §2.1a 的 compose 函数派生」, 而 §2.1a `:164` 逐字写着「**本 Spec 不新增拼接函数**」, 全文 grep `compose` 仅命中 SC-2 自身 ⇒ **SC-2 引用了一个本 Spec 明说不存在的函数**, 实现者写夹具时字面上找不到可 import 的对象 —— 正是本项目三次最重 critical 的同一形状, 这次由主控 R3 清账时引入。**订正后**: 夹具手写字面串是**允许且必要的** (拼接无代码宿主是 §2.1a 成文交付的一半); 归一仍走 `lib/track_id.py::derive_track_id`), 且断言**两层**: (i) 双方 overlap 各含对方; (ii) **把 compose 的 container 段置空重跑同一夹具 ⇒ 双方 overlap 必须变空** (负控)。缺 (ii) 的实现视为未满足本条 **⚠️ 类别 (R4/K3)**: **行为 (定向 fixture)** —— K3 降级 —— 派生无代码宿主 ⇒ 本条**不得**写成代码类; 它只能由 AB eval 分辨「AI 是否按 §2.1 规则拼串」, **不冒充结构化测试** |
| **SC-3** | R2-fix 版 (`container-short` 前 8 位 ⇒ label 碰撞) | container-id 的 `label` 设为长字符串时, track-id 仍用 **`uuid` 字段** | 代码 (新 accessor 的单测) + 文本层 | 直接调 `get_container_id()` (`lib/identity.py:191`, `:222` label 优先) 的实现在设了 label 的夹具上必红 |
| **SC-4** | R3 指出的 number 表示不一致 | `#007` 与 `#7` 派生**同一** track-id | 文本层 (占位串须字面写 `str(int(number))`) + 行为层 | 占位串写裸 `<number>` 必红; 行为臂上「照抄 `007`」与「归一成 `7`」两臂可辨 **⚠️ 类别 (R4/K3)**: **行为 (定向 fixture)** —— K3 降级 —— 派生无代码宿主 ⇒ 本条**不得**写成代码类; 它只能由 AB eval 分辨「AI 是否按 §2.1 规则拼串」, **不冒充结构化测试** |

### 主机制

| SC | 场景 | 期望 | 怎么会红 |
|----|------|------|---------|
| **SC-5** (代码) | heartbeat by-track 变体跨 subprocess 两次调用 (第二次 session_id 不同) | 同一 track 的 claim 被刷新 | 只有既有 `heartbeat()` (按 `(container, session)` 匹配, `lib/claim_lifecycle.py:228`) 的现状必红 |
| **SC-6** (代码) | 同 (container, track) 有多条 active claim | **全部**刷新 | 只刷新一条必红 |
| **SC-7** (代码) | 超 `SWEEP_TTL` 未刷新 ⇒ 仍被 sweep; **且**调用新 by-track heartbeat 刷新后 ⇒ **不**被 sweep | 两臂可辨 | **⚠️ 恒绿风险已堵 (R3/QA-F3)**: QA 席实读既有 `test_sweep_stale_cross_container_fresh_untouched` (`tests/test_release_by_track.py:380`) —— 它已覆盖「超时被 sweep」这一臂且**全程不调用任何 heartbeat**, 故 SC-7 若只有那一臂就是**零新代码路径覆盖**。⇒ 本条**必须含第二臂**: 夹具显式调 §2.2 的 by-track heartbeat 变体后再 sweep, 断言该 claim **未被** abandoned; 不调用新变体的实现在第二臂上必红 |
| **SC-8** (代码, **CLI 全链路**) — **⚠️ 已按 R2/M-16 拆掉捆绑, 只留一个可机械断言** | 同 issue 他轨 claim 为 `done` / `abandoned`, A.1 模板带 `--include-terminal` | **该条出现在 `linked_issue_overlap[]` 里** (单一断言: 可见性) | `lib/collision.py:268` 的 `_TERMINAL` skip 的现状必红; **且只测库函数的 SC 在「参数没接到 CLI」的实现上会绿** ⇒ 断言层必须是 CLI。**⚠️ 场景列已删去 `yielded`** —— 实读 `_TERMINAL` 不含它, 该子例 baseline 即绿 (R2/M-9: 旧版订正了正文却没同步 SC)。**「措辞按 status 分档」这半移到 SC-11** (它是消费层措辞, 无代码宿主) |
| **SC-9** (**行为**, 定向 fixture — **⚠️ 类别按 R2/M-16 订正, 旧标「代码」有误**) | `coordination.enabled == false` | A.1 **零调用**, 不写 claim, 不推远端 | 它断言的是「AI 是否跳过调用」, 实测对象是 SKILL.md 散文 ⇒ **无代码宿主**; 定向 fixture 上「无条件调用」的臂与「读 config 后跳过」的臂可辨。**与 SC-28 是同一开关的两半** (SC-9 管 A.1 侧, SC-28 管 heartbeat 侧) |
| **SC-10** (代码, **CLI 全链路**) — **⚠️ 已按 R2/M-16 拆掉捆绑** | fetch 降级 | **`GateResult.error == "fetch_degraded"`** (单一断言: 字段非空且取该 token) | 现状 `error: null` 必红 (`scripts/phase1_gate.py:210` 的 docstring 预留了该 token 但全文无 `error=` 赋值)。**「消费面渲染『未能核实』而非『无碰撞』」这半移到 SC-25** |
| **SC-11** (行为) | overlap 非空 / `unknown_schema_claims > 0` | AI 起草**前**经 `AskUserQuestion` 请裁; 告警含双方 `linked_issue` 原始串 + 对方 `track_id`/`container`/`claimed_at`/`status`; **措辞按 status 分档** (§2.3 选项表: `active` / `done` / `abandoned` / `unknown` 四档选项集不同) | 定向 fixture; 「渲染一行后自行继续」的臂应可分辨; 「对 `done` 也给出『释放对方 claim』选项」的臂应可分辨 (该选项在 `done` 档语义不成立) |
| **SC-12** (行为) | spec 有「关联 Issue」但未传 `--linked-issue` | AI 不得跳过该参数 | 定向 fixture (**不冒充结构化测试**); 「跳过」与「传了」两臂在 `phase1_gate` 输出里可辨 —— 前者 `linked_issue_overlap` **键缺席** (`scripts/phase1_gate.py:1230` 整块门控), 后者键存在 |

### 生命周期 / 迁出行

| SC | 场景 | 期望 | 怎么会红 |
|----|------|------|---------|
| **SC-13** | ⛔ **已迁至 [`linked-issue-field-availability`](../linked-issue-field-availability/proposal.md)** —— 本 Spec 不再承担「proposal 无字段 / 值不可解析 ⇒ custom check warning」 | — | — (编号保留不复用) |
| **SC-14** — **⚠️ 已按 R2/M-16 拆两层** | (a) **代码**: 给定 A.1 原串调 `release_gate.py --raw-track-id "<原串>" --status abandoned` (`--raw-track-id` 是 `release_gate.py:236-237` 的「三选一」必需项之一, 省了会 `parser.error`) (b) **行为**: A.1 判定「不起该 Spec」时 AI 记得去调 | (a) 该 claim 状态变为 `abandoned` (b) 定向 fixture 两臂可辨 | (a) 现状 `release_gate.py` 已支持 `--status abandoned` ⇒ **该臂的红点在「传 A.1 原串能否匹配到」** (与 SC-23 同根: 不统一 carry-id 则匹配不到, 必红); (b) 「判定放弃后直接开下一个方向、不 release」的臂必红 |
| **SC-15** (代码) | track-id 为**回落形** (`<spec-slug>-<uuid>`, **含 slug** —— 与 §5.1 / SC-1 **逐字同一句谓词**) 的轨改名 —— 含「无关联 issue 者」**与「同 issue 后起 Spec 落在回落形者」** | release 旧 + acquire 新两步后**无孤儿** (旧 track 不再 active, 新 track active) | 只 acquire 不 release 的实现留下孤儿 claim ⇒ 必红; 用「有没有关联 issue」做谓词的实现在「有 issue 却走回落形」的第三类夹具上必红 **⚠️ 类别 (R4/K3)**: **行为 (定向 fixture)** —— K3 降级 —— 派生无代码宿主 ⇒ 本条**不得**写成代码类; 它只能由 AB eval 分辨「AI 是否按 §2.1 规则拼串」, **不冒充结构化测试** |
| **SC-16** | ⛔ **已迁至 [`sibling-spec-probe`](../sibling-spec-probe/proposal.md)** (竞品在 `archive/` 下须命中) | — | — |
| **SC-17** | ⛔ **已迁至 `sibling-spec-probe`** (远端无同 issue spec ⇒ exit 0) | — | — |
| **SC-18** | ⛔ **已迁至 `sibling-spec-probe`** (探针 fetch 失败 ⇒ degraded + exit 非 0) | — | — |
| **SC-19** | ⛔ (a)/(c) 两条**已迁至 `sibling-spec-probe`** (不得自命中本轨 spec 目录 / 扫描超上限必须 `log()` 披露)。**(b)「不得把自己的 claim (同 track_id) 计入 overlap」属主机制** ⇒ **由本 Spec 新增的 SC-29 承担** (**⚠️ rework v3 自查订正**: 上一版此处写「由 SC-2 反向臂承担」是**不实断言** —— 实读 SC-2 的期望列只有「双方 `linked_issue_overlap` **各含对方**」这一条正向断言, **没有任何反向臂**; 一个「既返回对方也返回自己」的实现能同时满足 SC-2 而违反 (b)。探针席独立地也判该子项不该迁入 —— claim/track_id 词汇与探针语境错配 —— 两边结论一致, 只是本侧的「接住」动作当时没做实) | — | — |

### 保护窗可生产验证性 (heartbeat, R1 rework 核验 major 补)

> **触发**: 上一轮核验指出 —— §2.2 已自陈「换匹配键不产生刷新者 ⇒ SC-5~7 可以全绿而问题原样存在」, C2 裁定落版后全文却没有任何 SC 或 fixture 钉住它; 这正是 memory `feedback_completion_signals_vs_runtime_invocation` 同形的坑 (「已落版的一段 SKILL.md 文字」≠「会被生产调用的机制」)。

| SC | 类 | 场景 | 期望 | 怎么会红 |
|----|---|------|------|---------|
| **SC-20** | — | ⛔ **撤销** (owner 裁定 2026-08-23: (iii) 不采) | **本 Spec 不再对 `STALE_TTL` 提出任何断言** —— 该常量维持 `1800`, 相关的 `reconcile._is_stale()` 行为保持现状 | — (行保留、编号不复用; 回撤的其余三个落点见 §2.2 (iii) 段) |
| **SC-21** | 行为 (定向 fixture, 与 rule6_note 第 5 档「点名行为 (d)」呼应) | `/state-scanner` 入口被调用, 本会话在 coordination ref 持有 active claim, **且 `coordination.enabled == true`** | 两臂可辨: (A) heartbeat 编排层已挂载 ⇒ 每次调用**都**触发 `phase1_gate.py --heartbeat-only --raw-track-id "<carry-id>"` 刷新该 claim —— **判据 = 该 CLI 被 subprocess 调用且 `claim.heartbeat_at` 被刷新**; (B) 未挂载 ⇒ 不触发, `heartbeat()` 生产调用点仍为 0。**⚠️ rework v3 补门控臂**: 本条的场景**显式限定 `enabled == true`**; `false` 的那一半由 **SC-28** 承担, 两条合起来才覆盖 R2/M-7 | 当前实现两臂**不可辨** —— `lib/constants.py:43-44` 自陈「NO production heartbeat loop exists」, 无论挂不挂都是同一 (未触发) 结果 |

### rework v3 新增 (追加编号, 不重排既有 SC)

| SC | 类 | 场景 | 期望 | 怎么会红 |
|----|---|------|------|---------|
| **SC-22** (新) | 代码 | `phase-a-planner/SKILL.md` 与 `spec-drafter/SKILL.md` **各自**的 A.1 认领步骤 (R2/M-11: 双落点是核心杠杆却零 SC 覆盖) | ① `assertRegex(text, r"(?m)^#{2,4}[ \t]+前置: REQUIRE claim\b")` **且匹配行不在 ``` 围栏内** (最省实现: 先按 ``` 切段, 只在围栏外的段跑正则); ② 步骤块内含 `phase1_gate.py` / `--linked-issue` / `--include-terminal` / `--phase A.1` **四个字面量**; ③ 步骤块内含幂等谓词 `check:` + `if_missing:` (或等价的「本 session 已跑过 phase1_gate 则跳过」)。**宿主 = `skills/state-scanner/tests/test_coordination_default_lockin.py`, 扩它不另起文件** | 两处 SKILL.md 现**均无** A.1 步骤块 ⇒ baseline 必红。**裸 `assertIn` 明确不可接受** —— 子串检查对「把 `前置: REQUIRE claim` 原样塞进 A.1 现有 ```yaml 动作列表」这一种失败**免疫**, 而那正是 §2 明令禁止、§Why 引 R3/M6 论证过的原病。**docstring 须写明**: 与先例 `test_phase_b_require_claim_present` (`:53`, `:55-56` 两条**裸 `assertIn`**) 的断言强度差异**是有意的** —— B.0 的 YAML-键形态是既有欠缺, 另开 issue, 不在本 Spec 修。缺 ③ 的实现 (一次 A.1 写两条 claim + 两次外向推送) 也必红 **⚠️ 锚点换名 (R3/QA-F1)**: 原用 `A.0 - REQUIRE claim`, 但 `A.0` 在 `spec-drafter/SKILL.md` 已被占用为 **state-scanner** 步骤标签 (`:30` `- 查询项目状态 → 使用 \`state-scanner\` (A.0)`, `:369` 流程图同名, 另有 `A.0.5` = brainstorm) ⇒ 同名不同义。 现改用 **`### 前置: REQUIRE claim`** —— 与 `branch-manager/SKILL.md:146` 的既有真实标题 `### 前置: REQUIRE claim (Part A1, MUST — 与 phase-b-developer B.0 同一条约束)` **同体例**, 该锚点是 editlist FIX-13 本来就点名的先例。正则相应改为 `r"(?m)^#{2,4}[ \t]+前置: REQUIRE claim\b"` |
| **SC-23** (新) | 代码 (CLI 全链路) | A.1 认领 (原串 X) → 走完循环 → D.2b 跑 `release_gate.py --raw-track-id X` (R2/C-C) | 该 claim **不再 active** | 现状 A.1 原串 ≠ carry-id ⇒ `release_claim_by_track` 按 `(container, 归一 track_id)` (`lib/claim_lifecycle.py:377`/`:425`) 匹配不到 ⇒ claim 悬挂到 sweep ⇒ 必红。**若实现改的是 `derive_track_id` 去掉容器段, SC-2 会同时变红** (两条互为对方的负控) |
| **SC-24** (新) | 代码 (CLI 全链路) | 夹具写入一份 `schema_version: "2"` (或任何非 `"1"`) 且带匹配 `linked_issue` 的 claim blob, 经 CLI 跑并带 `--include-terminal` | `unknown_schema_claims >= 1` **且**该条**不出现在** `linked_issue_overlap[]` 中 | 现状**无该键** ⇒ 必红; 试图经 `linked_issue_overlap[]` 输出的实现在真实 `parse_claim` 路径下**恒空** (sentinel 的 `linked_issue` 为 `None`, 被 `lib/collision.py:274` 丢弃) ⇒ 也必红。**第二个断言 (不出现在 overlap[]) 是负控**: 它拒绝「强行放行 sentinel」这个坏实现 —— 那样会往告警面塞三个空字符串字段 |
| **SC-25** (新) | 代码 (CLI 全链路) + 行为 | overlap 计算路径抛异常 (夹具: 让 `linked_issue_overlaps` 抛) | ① `linked_issue_overlap == null` **且** `linked_issue_overlap_error` 非空 (代码臂); ② 消费面把「已确认存在竞品」(`unknown_schema_claims > 0`) 与「本轮没取到证据」(`error` 非空) 渲染成**同一句**的实现**必红** (行为臂) | 现状 `scripts/phase1_gate.py:1236-1238` 的 `except` 写 `out["linked_issue_overlap"] = []` ⇒ 异常路径与「查了没有」不可分辨 ⇒ 代码臂必红。行为臂的两个坏实现 (都渲染「未能核实」/ 都渲染「无碰撞」) 均可被判红 |
| **SC-26** (新) | 行为 (定向 fixture) | `state_scanner.coordination.unattended == true` 且 overlap 非空 (R2/M-15) | **零** `AskUserQuestion` 调用 + handoff 待复议段出现 `awaiting_owner` | 「照问不误」的臂可分辨; 用「`AskUserQuestion` 是否可用」做判据的实现在本 fixture 上**恒走问的那一臂** (C1 扩权后该谓词恒为「可用」) ⇒ 必红 |
| **SC-27** (新) | 代码 (CLI 全链路) | **三臂**: (A) track-id 为 **issue 派生形**的轨, 在同一 issue 内**放弃一个方向**后; (B) 同一条轨**放弃整个 issue** 后 (R2/C-B) | (A) claim 仍 **`active`**; (B) claim 为 **`abandoned`** | 旧版「探索性放弃必 release」的实现在 (A) 臂上会把 claim 释放掉 ⇒ 必红 (这正是连坐)。**两臂必须可辨** —— 只做 (B) 的测试恒绿, 抓不到连坐 **(C) (R3/TL-C1 补)**: 同 issue 下**两个方向各自持有 active claim** (同 track_id, 不同 `spec_slug`), 对方向 1 跑 D.2b 的 `release_gate.py --raw-track-id <原串> --spec-slug <方向1 slug>` ⇒ **方向 2 的 claim 仍 `active`**; **不传 `--spec-slug` 的实现会把方向 2 一并释放 ⇒ 必红** (baseline 必红: 该参数今天不存在) |
| **SC-28** (新) | 行为 (定向 fixture) | `coordination.enabled == false`, `/state-scanner` 入口被调用, 本会话持有 active claim (R2/M-7) | **零** heartbeat 调用 (不跑 `--heartbeat-only`, 不写 claim, 不推远端) | 把 (ii) 的「每次 `/state-scanner` 必跑」实现成**无视 opt-out** 的臂必红。**与 SC-21 合起来**才覆盖「无条件」的正确语义 (无条件 = 不依赖 `collision.kind`, **不是**无视 `enabled`) **(第二臂, R3/TL-M2)**: 连跑 N 次 `--heartbeat-only` 后, `coordination_probe.py` 的 **recent production 计数不变** (仍只反映真正的 `run_gate` 调用); 把 heartbeat 记进 production 分区的实现 ⇒ 计数增长 ⇒ **必红** |
| **SC-29** (新, ⚠️ **回归守卫 — baseline 即绿**) | 代码 (CLI 全链路) | 单容器单轨: 本轨自己已有一条 active claim 且 `linked_issue` 与本次查询相同, 经 CLI 跑 A.1 认领 (带 `--include-terminal`) —— 承接原 SC-19 的 (b) 子项 | 返回的 `linked_issue_overlap[]` 中**不出现本轨自己的 claim** (同 `track_id` 者必须被排除) | **⚠️ 本条 baseline 即绿** —— `lib/collision.py:278-279` 现在就写着 `if c.track_id == own_track_id:` / `continue`。**它不是恒真装饰, 是回归守卫**: 本 Spec 动了 `include_terminal` 形参与 `:1230` 的门控条件, **有能力打破它** (例如把 `--include-terminal` 实现成「跳过全部 continue 分支」就会连自排除一起跳掉)。判据「它怎么会红」= **在该负控实现上必红**; A.2 须以「删掉 `:278-279` 两行」作为坏实现验证它确实会红 (memory `adversarial-fixture`)。**⚠️ 与 SC-2 的关系**: SC-2 只断言「各含对方」(正向, baseline 红), 本条断言「不含自己」(反向, baseline 绿) —— **两条分开列而不合并进 SC-2**, 因为把 baseline-红与 baseline-绿的断言捆进同一条会让「怎么会红」失去分辨力 (R2/M-16 的同一教训) **⚠️ 夹具补强 (R3/QA-F4)**: 原夹具 own claim = `active`, 而**本 Spec 真正新开的风险面**是 `--include-terminal` 放行终态后 —— own claim 为 `done`/`abandoned` 时是否仍被排除。⇒ 夹具**必须含第二组**: own claim 状态为 **terminal** 且带 `--include-terminal` 跑, 断言 `linked_issue_overlap[]` 中**仍不出现本轨自己**。只测 active 那组的实现视为未满足本条 |

---

## 非目标

- **不改** `linked_issue` 归一本身 —— 属前置 Spec [`linked-issue-normalization`](../../archive/2026-08-23-linked-issue-normalization/proposal.md) (**已 ship 并归档**, v1.67.0 `ca52d1c`);
- **不做** basename 截断型别名归一 (D9; 分隔符型已由前置 Spec 覆盖);
- **不做**中心化 spec 登记表 (D10);
- **不引入**跨容器 release (D6);
- **不把** advisory 升级为 block;
- **不动** Phase B 入口现有认领 —— `include_terminal` 默认 `False` 保既有语义逐字节不变; **`--heartbeat-only` 是同一 CLI 下的独立模式, 不改 acquire 路径; heartbeat 是增并存变体不改既有键** (D16)。**⚠️ 唯一的边界争点已成文**: §2.1b 的 carry-id 统一会改三处模板的 **占位串取值口径** (不改闸门语义), 见该节的 U-3 边界说明, **请 owner 在 R3 时确认**; **⚠️ 限定 (R3/BA-M3 + TL-M3)**: 本条指「不改 Phase B 的 **acquire 路径、默认参数与 outcome 语义**」; **不包括** advisory 键 `linked_issue_overlap` 的**类型放宽** (`list` → `list | null | 缺席`) —— 该放宽是 R2/M-4「零证据不得当正证据」修复的必然结果, 且 Phase B **可选传** `--linked-issue` (`phase-b-developer/SKILL.md:93`) ⇒ 它**会**看到新形态。二者原先并列成文即自相矛盾, 现按此拆开。
- **不改写**存量 coordination ref 数据 (⇒ §2.1b 的过渡期两形态并存已知限, §6 已列);
- **不统一** `owner-container` 与 claim container 段的口径 (§3 已记为 follow-up, 属 standards 变更);
- **不修** `release_gate.py:225` help / `state-scanner/SKILL.md:176` / `phase-d-closer/SKILL.md:56` 三处把 `SWEEP_TTL` 行为写成 `STALE_TTL` 的**代码库既有措辞缺陷** —— 实读事实见「事实断言逐条实读清单」#14, 记 **follow-up**, 不混进本 Spec 变更面;
- **不改 `STALE_TTL`** (owner 2026-08-23 撤销 (iii));
- **不承担**「关联 Issue」字段的产生/校验/抽取规则 (整节迁 [`linked-issue-field-availability`](../linked-issue-field-availability/proposal.md), 含**不回填存量 proposal** 这条);
- **不承担**竞品 spec 探针 (整节迁 [`sibling-spec-probe`](../sibling-spec-probe/proposal.md));
- **不编辑**已归档的姊妹 Spec (`openspec/archive/2026-08-23-linked-issue-normalization/`) —— editlist FIX-11 要求的编辑**已由姊妹自己在 ship 前完成** (清单 #16);
- **不给** `unknown_schema_claims` 提供**路径/身份** (只给 count; 需改 `ReadClaimsResult` 字段, 转 follow-up — D14);
- **不定义** `unattended` 的 Layer 1→2 env 传递三腿契约 (§2.3 已知限, 转 A.2/follow-up)。

---

## Impact

> **⚠️ 行号基线 = aria `d50f9c3`** (见「事实断言逐条实读清单」表头); 主仓 gitlink 现指向 `58a49e7` (v1.67.1), 落后 2 个不触及本表文件行的 commit, A.2 实施前须重新 fetch 复核。

| 文件 | 变更 | 来源 |
|------|------|------|
| `skills/state-scanner/lib/claim_schema.py` | **新增两个 additive 字段 `spec_slug: Optional[str] = None` 与 `track_form: Optional[str] = None`** (`"issue"`/`"slug"`; 缺省 `None` ⇒ 形态未知 ⇒ fail-CLOSED 退回现状并 log) (与 Part B1 引入 `linked_issue` 同款: 旧 reader 忽略未知字段, **不 bump `schema_version`**) —— C-B 另一半 (`spec_slug`) 与其形态判定式 (`track_form`, R3/TL-M4) 的载体 | **R3/TL-C1** (§5.3) |
| `skills/state-scanner/lib/claim_lifecycle.py` (第二处变更) | `acquire_claim` 写入 `spec_slug` **与 `track_form`** (后者由派生分支自己写, 消费侧零推断); `release_claim_by_track` 增 **keyword-only** `spec_slug: Optional[str] = None` —— 传值时按 `(container, 归一 track_id, spec_slug)` 三元组过滤, **不传时行为逐字节不变** (= 现状 ALL matching) ⇒ Phase B/D 既有调用零影响 | **R3/TL-C1** (§5.3) |
| `skills/state-scanner/scripts/coordination_probe.py` | **仅口径声明/注释**: 明确 `--heartbeat-only` 的遥测**不进** production 分区, 本探针计数口径不放宽 (防 enabled check 被心跳变恒绿) | **R3/TL-M2** |
| `skills/state-scanner/scripts/release_gate.py` | 新增 CLI flag `--spec-slug`; 透传至 `release_claim_by_track` | **R3/TL-C1** (§5.3) |
| `skills/phase-d-closer/SKILL.md` (第二处变更) | D.2b 的 `release_gate.py` 命令模板增 `--spec-slug "<本 cycle 的 spec 目录名>"` —— 不加则 issue 派生形下会连坐同 issue 其他在制方向 | **R3/TL-C1** (§5.3) |
| `skills/state-scanner/docs/coordination-ref-schema.md` (第二处变更) | §2.1 字段表增 `spec_slug` 行 + §2.2 说明其与 `track_id` 的分工 (track_id 承载「哪条 issue」, `spec_slug` 承载「哪个方向」) | **R3/TL-C1** (§5.3) |
| `skills/state-scanner/lib/claim_lifecycle.py` | heartbeat **增 by-track 并存变体** —— **签名 (R4/C-2 补, 镜像 `release_claim_by_track`)**: `def heartbeat_by_track(raw_track_id: str, identity: Optional[Identity] = None, repo_path: Optional[Path] = None, *, spec_slug: Optional[str] = None, now: Optional[datetime] = None) -> AcquireResult` (仿同文件 `release_claim` `:274` / `release_claim_by_track` `:377` 的并存模式; **既有 `heartbeat()` 的 `(container, session)` 匹配键 `:228` 不动** — D16) | **S1** (原版 Impact 表零覆盖) |
| `skills/state-scanner/lib/identity.py` | 新增直取 `uuid` 字段的 accessor —— **签名 (R4/C-2 补, 镜像 `get_container_id`)**: `def get_container_uuid(home_dir: Optional[Path] = None) -> str` (跳过 label) —— 现有 `get_container_id()` (`:191`) 在 `:222` 是 `return label if label else uuid`, 不能直接用; hostname 兜底分支 (`:242` `return _hostname()`) 成文, 与新生成 uuid 路径 (`:244` `return uuid`) 区分 | **S3** (原版 Impact 表零覆盖) |
| `skills/state-scanner/lib/collision.py` | `linked_issue_overlaps` 增 keyword-only 形参 `include_terminal: bool = False` (现三参数签名 `:230-234`; `_TERMINAL` 定义 `:268`; 详见清单 #3/#4/#5/#6/#16) | **R1-fix/C6** (R1 rework 核验 major-2 补, 原表零覆盖) |
| `skills/state-scanner/lib/constants.py` | ⚠️ **rework v3 回撤 (iii)**: **不改 `STALE_TTL`** (`:36` 维持 `1800`), **不动** `:32` 的「`STALE_TTL == 3 × HEARTBEAT_INTERVAL`」不变量注释 (前提未变)。**本行保留的唯一变更**: `:43-44`「NO production heartbeat loop exists (heartbeat() has zero production call sites…)」与 `:50`「Revisit when a heartbeat loop ships」两处注释, 在本 Spec 落地 heartbeat 编排层后**前提消失**, 须同步改写 —— **与 TTL 数值无关** | **C2 落版 (ii)** (owner 2026-08-22) + **(iii) 撤销** (owner 2026-08-23) |
| `skills/state-scanner/scripts/phase1_gate.py` | ① CLI flag `--include-terminal` (store_true); ② **在 `_main()` 的调用处 `:1233-1235` 加关键字参数** (不碰 `run_gate` `:1032` / `_run_gate_impl` `:335` 签名); ③ **门控 `:1230` 由 `if args.linked_issue:` 改为 `if args.linked_issue or args.include_terminal:`** + 新增 `unknown_schema_claims` 键 (D14); ④ **`:1236-1238` 的 `except` 分支不再写 `out["linked_issue_overlap"] = []`, 改写 `None` + `linked_issue_overlap_error`** (R2/M-4); ⑤ `error` 契约真正携带 `fetch_degraded` (`:210` docstring 已预留但从未赋值) | **R3/C2** + **R2/M-3, M-4** + editlist **FIX-03** |
| `skills/state-scanner/scripts/phase1_gate.py` (第二处变更, 与上一行同文件不同能力) | 新增 **`--heartbeat-only` 模式**: 复用其 identity/fetch/push 管道; 入参 `--raw-track-id "<carry-id>"` (**来源 = handoff §6 结构化 carry-id, 取不到则跳过 + log, 不猜**); 按 `(container, 归一 track_id)` 刷新全部匹配的 active claim 的 `heartbeat_at`, **不写新 claim, 不判碰撞**; 受 `coordination.enabled` 门控。若 A.2 落地时改为独立脚本 `scripts/heartbeat_gate.py` 亦属同一变更面 | **C2 落版 (ii)** + **R2/M-12** |
| `skills/state-scanner/tests/` (既有宿主) | SC-2 / SC-3 / SC-5~8 / SC-10 / SC-14(a) / SC-15 / **SC-22** (扩 `test_coordination_default_lockin.py`, 同时承载 SC-1/SC-4 的**文本层**) / **SC-23** / **SC-24** / **SC-25(代码臂)** / **SC-27** / **SC-29** + rule6_note 的 **`DEFAULTS.json` ↔ `config-loader/SKILL.md` 一致性 substitute 测试**。**⚠️ SC-20 已撤销, 从本行移除** | R1/C4 + rework v3 |
| `skills/phase-a-planner/SKILL.md` | A.1 **独立标题级** `前置: REQUIRE claim` 步骤块 (锚点形态见 SC-22) + overlap/`unknown` 消费 (§2.3 按 status 分档的选项集) + release 义务 (§5.2 按形态分档) + `coordination.enabled` skip + `unattended` 分支 | R3/M6 + R2/C-B + R2/M-15 |
| `skills/phase-a-planner/SKILL.md` frontmatter `allowed-tools` | **`:9`** `Read, Write, Glob, Grep, Task, Skill` → `Read, Write, Glob, Grep, Task, Skill, Bash, AskUserQuestion` | **C1 落版** (owner 2026-08-22, 采 (a)) |
| `skills/spec-drafter/SKILL.md` | 第二落点 (同上的「前置: REQUIRE claim」步骤块 + 幂等谓词)。**⚠️「proposal 模板增『关联 Issue』字段」已随 §1 迁至 [`linked-issue-field-availability`](../linked-issue-field-availability/proposal.md)**, 不在本 Spec | **S6** (原 **S4** 部分已迁出) |
| `skills/spec-drafter/SKILL.md` frontmatter `allowed-tools` | **`:10`** `Read, Write, Glob, Grep, AskUserQuestion` → `Read, Write, Glob, Grep, AskUserQuestion, Bash` | **C1 落版** (owner 2026-08-22, 采 (a)) |
| `skills/state-scanner/SKILL.md` | Layer L Phase B 集成段 (`:143-178` 一带, 触发条件在 `:149`) 新增对称的「Layer L A.1 heartbeat 集成」小节: AI 编排层挂载点、**受 `coordination.enabled` 门控**、不依赖 `collision.kind` (这是「无条件」的准确含义, R2/M-7)、`--heartbeat-only` 调用形态与 carry-id 来源、fail-soft 处置 | **C2 落版 (ii)** + **R2/M-7, M-12**; **(R3/BA-M3 补) `:176` 的 Layer L 消费契约段同步四态**: `linked_issue_overlap` 现为 `list \| null \| 缺席`, 须写明「`null` + `linked_issue_overlap_error` 非空 ⇒ 渲染『未能核实』, **不得**渲染成『无碰撞』」—— Phase B 编排层读的就是这一段 |
| **`skills/phase-b-developer/SKILL.md`** (新增行) | B.0 步骤块 `:92` 的 `--raw-track-id "<本 cycle carry-id/Spec id>"` 占位措辞改为明示「**A.1 认领时派生的那一串**; 未走 A.1 的 session 沿用 Spec id」(**只改占位串取值口径, 不改闸门语义**) | **R2/C-C** + editlist **FIX-14 选项 A** |
| **`skills/branch-manager/SKILL.md`** (新增行) | `:146` 的 `### 前置: REQUIRE claim` 步骤块内同款 carry-id 占位措辞同步 | 同上 |
| **`skills/phase-d-closer/SKILL.md`** (新增行) | D.2b (`:42` 表行, `:51-52` 调用) 的 `--raw-track-id "<本 cycle 的 carry-id 原始串>"` 与 `:55` 的说明句同步为同一口径。**⚠️ `:56` 的「超 STALE_TTL」误写属既有缺陷, 记 follow-up, 不在本 Spec 改** | 同上 + 清单 #14 |
| **`standards/conventions/session-handoff.md`** (新增行) | **§2.3.8** (非 §2.3 —— R3/KM-1) 结构化 `{id, desc}` 的 `id` 即本 cycle carry-id (= A.1 原串) —— **`track_id.py` 自称该文件为 SOT** ⇒ 不登记就是让 SOT 与实现脱钩 | **R2/M-14** (一半) |
| **`skills/state-scanner/docs/coordination-ref-schema.md`** (新增行) | **§3.2 (`:129` 起, 现枚举 reader 侧 unknown 行为 5 条于 `:133-139`)** 后**追加第 6 条**: unknown claim 在 A.1 消费面的可见性与措辞语义 (经独立键 `unknown_schema_claims`; 措辞「已检测到 N 条无法解析的 claim, 存在性已确认、内容未知」; **不得**并入 `linked_issue_overlap[]`, **不得**与 `done`/`abandoned` 同档)。**断言形登记** (该文件**已实读确认存在**, 见清单 #28), 不写「若存在」条件形 | **R2/M-14** (另一半) + editlist **FIX-17** |
| `skills/state-scanner/references/layer-l-integration.md` | **三处, 缺一即留悬空引用**: ① `:15` 断言「Design A 条件触发: 闸门仅在用户确认要进入 Phase B 时调用, 不在 scan.py 内自动执行」, 本 Spec 增 A.1 触发点后即过时, 须同步; ② **`:45` 的函数名是悬空的** —— 该行逐字 `` \| `heartbeat` \| `phase-b-developer` mid-cycle \| 每 10min (caller 负责调度) \| `lib/claim_lifecycle.py::update_heartbeat()` \| ``, 而 `git grep update_heartbeat` 全 aria **只命中这一行自身** (清单 #33) ⇒ **`update_heartbeat()` 这个函数不存在**, 真名是 `heartbeat()` (`lib/claim_lifecycle.py:178`), 须改名; ③ **同一行的 caller/节律也与事实矛盾** —— 它写 caller = `phase-b-developer` 每 10min, 而 `lib/constants.py:43-44` 逐字自陈 `NO production heartbeat loop exists (heartbeat() has zero production call sites…)` ⇒ 该行描述的是一个**从未存在过的调度**, 须改写为本 Spec 落地后的真实 caller/节律 (`/state-scanner` 入口 AI 编排层, 每次调用, 受 `coordination.enabled` 门控) | R1/M8 + **rework v3 实读新增 (A-8)** |
| `skills/config-loader/SKILL.md` | ① `coordination` 在 A.1 的 skip 语义登记 (既有 `enabled` `:134` / `mode` `:140` 同节); ② **新增 `state_scanner.coordination.unattended` (boolean, default false) 登记** | R1/M3 + **R2/M-15** (editlist FIX-16) |
| **`skills/config-loader/DEFAULTS.json`** (新增行) | **注册 `state_scanner.coordination.{enabled, mode, unattended}` 三键**, 值与 `config-loader/SKILL.md:134`/`:140` 的登记逐字一致。**实测现状: `state_scanner` 段根本没有 `coordination`** (清单 #26) ⇒ 这是「登记了但没注册」的实缺口, 也是 rule6_note 描述性档 substitute 的被测对象 | **R2/M-17 第 5 项** |
| ⛔ `skills/audit-engine/SKILL.md` + `references/execution-modes.md` | **已随 §4 迁至 [`sibling-spec-probe`](../sibling-spec-probe/proposal.md)** | (原 R3/M5) |
| ⛔ `skills/audit-engine/scripts/sibling_spec_probe.py` + `tests/` | **已随 §4 迁出** (含目录新建) | — |
| ⛔ `.aria/state-checks.yaml` | **已随 §1 迁至 [`linked-issue-field-availability`](../linked-issue-field-availability/proposal.md)** (「关联 Issue」字段校验 check) | (原 **S4**) |
| ⛔ `standards/openspec/templates/proposal-minimal.md` (跨项目 SOT) | **R2/M-2 指出旧版漏登记该 SOT** ⇒ 该项**随 §1 整体迁至 `linked-issue-field-availability`** —— 「机械回声只覆盖 Aria 仓」是**字段可得性**的问题, 不是 A.1 认领的问题 | **R2/M-2** |
| AB 套件 — `phase-a-planner.json` / `spec-drafter.json` (能力面 hunk, **照跑档**) | `allowed-tools` 扩权 hunk 影响全场景; **两套件均实存** (rework v3 实核: `evals` 各 **2**) ⇒ **现有 AB 全量照跑, 零裁量**; 验「扩权后既有 eval 场景行为是否漂移」 | rule6_note 能力面附注 |
| AB 套件 — `phase-a-planner` / `spec-drafter` (**覆盖外档**) | 定向 fixture: (a)(b)(c) 三条 + (e) `unattended` 臂 (SC-26); 与上一行「照跑现有 AB」**互不替代**。**⚠️ 旧版此行含的 `audit-engine` 已随 §4 迁出** (且 `ab-suite/audit-engine.json` **实测不存在**, 清单 #29) | rule6_note + **R2/M-6** |
| `aria-plugin-benchmarks/ab-suite/state-scanner.json` (照跑 AB 档) | 在**既有套件内**新增 1 eval case 钉点名行为 (d)「持 active claim 且 `enabled == true` 时 `/state-scanner` 入口每次触发 `phase1_gate.py --heartbeat-only`; `enabled == false` 时零触发」, 与 SC-21 / SC-28 呼应 (套件实存, `evals` = **12**) | rule6_note |

**follow-up (不在本 Spec, 各带去处)**:

| # | follow-up | 为什么不在本 Spec |
|---|---|---|
| 1 | `owner-container` (形如 `simonfish/bfe8285d`) 与 claim container 段 (`bfe8285d`) 的口径统一 | 牵动 handoff frontmatter 规范, 属 standards 变更 (S6 附带发现) |
| 2 | `release_gate.py:225` help / `state-scanner/SKILL.md:176` / `phase-d-closer/SKILL.md:56` 三处 `SWEEP_TTL`→`STALE_TTL` 措辞勘正 | 代码库**既有**缺陷, 非本 Spec 引入; 混进变更面会把「文档措辞勘正」和「机制变更」搅在一起 (清单 #14) |
| 3 | `unknown_schema_claims` 的**路径/身份**信息 | 需改 `ReadClaimsResult` (`lib/coordination_ref.py:119`) 的 NamedTuple 字段, blast radius 超本 Spec (D14) |
| 4 | `phase-b-developer` B.0 的 **YAML-键形态**升级为标题级 | 既有欠缺, 与本 Spec 的「前置: REQUIRE claim」落点正交; 拉平会扩大 Phase B 改动面, 撞 §非目标 (SC-22 docstring 已写明强度差异是有意的) |
| 5 | `unattended` 的 **Layer 1→2 env 传递三腿契约** (write + HCL declare + consumer import) | 会把 Layer 1/2 契约拉进本 Spec; 缺 import 时静默 fallback 到 `false` (即「照问不误」), 该风险已成文于 §2.3 |
| 6 | 跨容器**定向** release | 写别人的 claim 是权限面变更, 应独立评估 (D6) |

---

## 审计与 spike 轨迹 — ⛔ **整节已切出**

> **迁往**: [`.aria/audit-reports/a1-entry-claim-audit-trail.md`](../../../.aria/audit-reports/a1-entry-claim-audit-trail.md) §1 —— **按字节搬运, 未重写任何一句**, 只加了节标题。
> 一并搬出的还有: §2.2 的 **(iii) 落版原文** (2026-08-23 owner 撤销前) 与两处**已闭环**的「⚠️ 实读订正 · 请 owner 复议」叙事 (审计轨 §2/§3/§4)。
> **owner 裁定原文 blockquote 留在本文件内** (§2.2 的 2026-08-22 与 2026-08-23 两条、§3 的 2026-08-22 一条) —— 它们是**承重设计输入**, 不是审计叙事; 上一轮把它们删掉换 AI 转述已被核验席判 major。
> **切分的四条声明** (append-only / 不维护一致性 / 以本文件为准 / 不得因审计轨回改本文件) 见本文件头部。**本次切分是执笔侧的流程判断, 已标请 owner 复议。**

报告索引 (未搬, 留此便于定位): 旧版三轮 `.aria/audit-reports/post_spec-R{1,2,3}-*-a1-entry-claim-duplicate-work-guard-*` (`b7c4933` 之前) · **重写 v2 R1** `post_spec-R1-1785710000000-a1-entry-claim-rewrite-*` (5 席 + 聚合 + **R1-fix editlist**) · **重写 v2 R2** `post_spec-R2-1787481000000-a1-entry-claim-rewrite-aggregated.md` (5 席, 3C/17M, REVISE 未收敛) · spike `.aria/spikes/2026-08-02-*`

---

## R1-fix editlist 逐条对账 (R2/M-13 —— **零容忍自述不实**)

> **为什么有这一段**: R2/CR-M4 命中「Spec 三处自述『R1-fix 已全量吸收』, 而 editlist 的 12 项实际未落」。**本段用逐条对账取代任何形式的总结句**; 全文**不再出现**「已全量吸收 / 已全部处理」之类无锚点的自述 (memory `past-summary≠measurement`)。
> **锚点**: 「本文小节」列给的字符串可直接在本文件内 grep。editlist SOT = `.aria/audit-reports/post_spec-R1-fix-editlist-a1-entry-claim.md`。

| FIX | 主题 (editlist 原题) | 状态 | 锚点 / 去处 |
|---|---|---|---|
| FIX-01 | C1 — `spec-drafter` allowed-tools 行号错一行 + 表下补取证命令 | **已落 (上一轮)**, 本轮复核行号 | grep `spec-drafter/SKILL.md:10` (§3 表 + Impact 表 + 清单 #2) |
| FIX-02 | C6 — 「实读现签名」代码块与真实文本不符 | **已落 (上一轮)**, 本轮换 `d50f9c3` 口径 | grep `:230-234` (§2.4 传递链 item 0 + 清单 #4) |
| FIX-03 | C4 — `unknown` 改走独立 additive 键 ⭐ 承重 | **本轮落** | grep `§2.4a` + `unknown_schema_claims` (§2.4a / SC-24 / D14 / Impact `phase1_gate.py` 行③) |
| FIX-04 | C2 — 删 `A1_SWEEP_TTL` 72h 分档 | **已落 (重写 v2 起即无该分档)** | 全文 grep `A1_SWEEP_TTL` = 0 命中 |
| FIX-05 | C5 — `--sweep-stale` 阈值误写是**三处** | **本轮定性为 follow-up** (硬约束: 文档措辞勘正不混进变更面) | grep `超 STALE_TTL` (§非目标 + Impact follow-up #2 + 清单 #14) |
| FIX-06 | C3-a — 语料统计数字全文回灌 | **⛔ 随 §1 迁至 `linked-issue-field-availability`**; 本轮另把主体内残留的 `141/13/9%` **换成 rework v3 实测口径** | grep `⭐ 真正的瓶颈` + 清单 #30 |
| FIX-07 | C3-b — check 作用域 + 回填 6 篇 ⭐ 承重 | **⛔ 随 §1 迁出** | §1 指针段 |
| FIX-08 | C3-c — canonical token 抽取规则自相矛盾 | **⛔ 随 §1 迁出** | §1 指针段 |
| FIX-09 | ⭐ NEW-01 — `无` 绝不可作 `--linked-issue` 实参 | **已落 (上一轮)**, 本轮补行号订正 + 归属划分 | grep `token 为 \`无\` 时` (§2 模板下 blockquote); 「字段值怎么写」归子 Spec, 「实参必须省略」留主体 |
| FIX-10 | M3 — 探针「同 issue」谓词对 `无` 归属未定义 | **⛔ 随 §4 迁至 `sibling-spec-probe`** | §4 指针段 |
| FIX-11 | M1 — 姊妹 Spec SC-8 的字面禁止加 keyword-only 形参 ⇒ 必需编辑 | **不适用 (前提已消失)** —— 姊妹**已 ship 并归档**, 且**它自己**在 ship 前写入了关闭条款 (`archive/2026-08-23-linked-issue-normalization/proposal.md:257`/`:260`) ⇒ 本轮**不改归档件** | grep `该协调项已完全闭环` (§2.4 传递链 item 0) + 清单 #16 |
| FIX-12 | M5 — 三态扩为四态 + §6 缺口表补最大一项 | **本轮落** | grep `§2.4b 四态契约` + §6 缺口表首行 (grep `token 为 \`无\` 或字段缺席`) |
| FIX-13 | M8 — SC-21 断言形态对「塞进 YAML 列表」免疫; `### B.0` 不存在 | **本轮落** (三处: 锚点换 `branch-manager:146` / 新 **SC-22** 正则形态 / §3 幂等分工) | grep `前置: REQUIRE claim` (§2 触发时机 + §3 + SC-22) |
| FIX-14 | M2 — §5 漏「A.1 成功并走完循环」, D.2b 匹配不到 | **本轮落 (选项 A)** | grep `§2.1b carry-id 契约` + §5.2 第 4 行 + **SC-23** + Impact 三行 SKILL.md + `session-handoff.md` 行 |
| FIX-15 | CR-M1 — SC-1/SC-15 二分谓词换「track-id 形态是否含 slug」 | **本轮落 (三处逐字同一句)** | grep `形态是否含 slug` (§5.1 + SC-1 + SC-15) |
| FIX-16 | CR-M5 — 无人值守判据被 C1 抹平 | **本轮落** | grep `unattended` (§2.3 blockquote + §3 AD10 句 + D15 + **SC-26** + Impact `config-loader` / `DEFAULTS.json` 两行) |
| FIX-17 | KM — `coordination-ref-schema.md` **存在**, 改断言形 | **本轮落** | Impact 表 `coordination-ref-schema.md` 行 (断言形 + `:129`/`:133-139` 锚点) + 清单 #28 |
| FIX-18 | MINOR — S3 spike 的 `identity.py:244` 是「补」不是「改」, 且替换项本身也错 | **本轮落 (三处出处 + S3 勘误注)** | §2.1 表格 `container_uuid` 行的依据格 (grep `S3 spike 勘误`) + Impact 表 `identity.py` 行 (`:191`/`:222`/`:242`/`:244`) + 清单 #11。**存疑项见「本轮未做 / 存疑」#1** |
| FIX-19 | dogfood — 本 Spec 自身补「关联 Issue」字段 | **本轮落 (本文件头部)**; **姊妹 Spec 那一半不适用** (已归档, 不改归档件) | 本文件 `> **关联 Issue**: \`无\`` (第 12 行一带; 冒号后第一个非空白是 inline-code span) |

**editlist 的 deferred / owner 裁项**: D-a (sweep vs 自愿 abandon 的 provenance 可分辨) 与 D-b (`unknown` 的路径/身份) **维持 deferred**, 各自记入 Impact follow-up #3 与另开 issue; D-c (B.0 YAML-键形态) 记入 follow-up #4。U-1 (删 S1 产出) **未采** —— heartbeat by-track 变体保留, 但已按其备选要求成文写明「`heartbeat()` 至今零生产调用点 ⇒ 改匹配键不产生刷新者」(§2.2 首段 + SC-21), 不冒充保护窗。U-2 (回填 6 份 aria-orchestrator proposal) **随 §1 迁出**。U-3 (carry-id 选项 A/B) **本轮采 A 并标请 owner 确认** (§2.1b)。U-5 (改姊妹 Spec) **前提消失** (FIX-11)。U-6 (`unattended` 消费侧接线) **本轮按其倾向办**: 只登记 key + 加 SC-26, 接线转 A.2, 并成文声明三腿契约缺口 (§2.3)。

---

## 本轮 (rework v3) 引入的新表面 (未审)

> 按硬约束「不新增未被要求的机制; 任何新表面必须列出」逐条声明。**本段是给 R3 审计席的输入, 不是完成度自述。**

1. **`.aria/audit-reports/a1-entry-claim-audit-trail.md` 新文件 + 本文件头部的四条切分声明** —— 流程判断, 非 owner 裁定, **已标请 owner 复议** (D-J)。风险: 审计轨与 Spec 的指针若失效, 历史会变成孤儿; 缓解 = 审计轨内每节都标了它搬自哪个行区间。
2. **§2.3 的「按 status 分档的选项集」表** (R2/M-17 第 3 项的处置) —— **三个镜头都没提出这个具体形态**, 是本轮执笔的综合裁断。它把 §2.3 的选项面从 3 项扩到 4 档 × 2-3 项, **扩大了 AI 在 A.1 的决策面**。
3. **SC-1~SC-4 新增「宿主 / 怎么会红」两列, 并把它们拆成「文本层 + 行为层」** (R2/M-17 第 1 项的处置) —— 本轮裁断。它**没有**新增代码机制, 但把「拼接无代码宿主」这件事显式写成了交付面的一部分。
4. **rule6_note 的新 substitute (`DEFAULTS.json` ↔ `config-loader/SKILL.md` 一致性测试)** —— 新的测试面; 已在基线亲跑确认**当前必红** (清单 #26), 但**未验证**「它对一个坏实现 (只注册两键漏 `unattended`) 是否也红」—— A.2 须补该负控 (memory `adversarial-fixture`)。
5. **§2.1b 对三处 SKILL.md 占位措辞的改动** —— 与 §非目标「不动 Phase B 入口现有认领」的边界靠**成文定义**划开 (改取值口径不改闸门语义), **该划法本身未经审计席确认**, 已标请 owner 在 R3 确认。
6. **`linked_issue_overlap == null` 这个新的返回形态** (R2/M-4 的修复) —— 把该键的类型从「恒为 list」放宽为「list | null | 缺席」。**下游消费者未逐一核查**: 本 Spec 只核了 A.1 消费面; Phase B 消费面因不传 `--include-terminal` 且异常路径同样会走到 (它也调 `--linked-issue`) ⇒ **Phase B 的消费面也会看到 `null`**, 这一点**本轮未在 Phase B 侧做任何处置**, 是已知的未审边。
   > **⚠️ R3/BA-M3 订正 (主控 2026-08-25)**: 本条原自述「Phase B 两个入口都不带该参数」—— 那句话说的是 **`--include-terminal`**, 与本条的 **`--linked-issue`** **是两个不同的 flag, 被混为一谈**。 实读 `skills/phase-b-developer/SKILL.md:93` 逐字 `[--linked-issue "<repo>#<n>"] --repo-path "<repo root>"` ⇒ **Phase B 可选传 `--linked-issue`**, 传了就会走到本 Spec 改动的那段 (`phase1_gate.py:1230` 门控块) 并可能拿到 `null` 形态。 ⇒ **该消费路径真实存在, 不是理论风险**: Impact 表已补 `state-scanner/SKILL.md:176` 的四态契约同步行; 且 §非目标「不动 Phase B 入口现有认领」须按此**限定**为「不改 Phase B 的 **acquire 路径与默认参数**」, **不包括** advisory 键的类型放宽。
7. **`unknown_schema_claims` 输出键 + 门控改为 `or args.include_terminal`** (editlist FIX-03, 该 editlist 已自陈是其综合裁断) —— `--include-terminal` 时会**多跑一次 `read_claims`** (git ls-tree + 每文件 git show)。**未测其耗时。**

---


---

### R3 清账轮 (2026-08-25, owner 方向 a) **新引入且未经任何审计**的表面 — 请 R4 优先审

> 本段由主控在 R3 之后、R4 之前追加。下列每一条都是**为修 R3 的 critical 而新造的**, 因此**没有任何一轮审计看过它们**。

1. **claim schema 增两个 additive 字段 `spec_slug` / `track_form`** (§5.3 / §5.1) —— 是本轮最大的新表面。风险面: (a) 两个字段与既有 `linked_issue` 三者的**职责边界**是否真的互不重叠; (b) 旧 claim 无字段时的 fail-CLOSED 退化 (退回 ALL matching + log) 是否**真的比连坐更安全**; (c) 不 bump `schema_version` 的判断是否与 `coordination-ref-schema.md` §3 的演进契约相容。
2. **`release_claim_by_track` 增 keyword-only `spec_slug` 过滤** —— 声称「不传时行为逐字节不变」, **未实测**。
3. **`lib/linked_issue_field.py` 新模块 + `extract_linked_issue_field(text)` 纯函数** (字段 spec C3) —— 新的跨 Spec 复用面; 输入从「路径」改成「文本 blob」这个决定**未经审计**。
4. **`.aria/linked-issue-field-grandfathered.txt` 仓本地数据文件** (字段 spec C2) —— 新的数据面; 「文件不存在 ⇒ 空集而非错误」这条 fail-open 方向的选择**与本 Spec 别处的 fail-CLOSED 取向相反**, 需专门审它是否是对的例外。
5. **`--heartbeat-only` 的遥测分区隔离** (§2.2, R3/TL-M2) —— 新增一个 `_source` 取值或跳过遥测; 对既有 `coordination_probe` 计数口径的影响**只做了推理未实测**。
6. **锚点从 `A.0 - REQUIRE claim` 改为 `前置: REQUIRE claim`** (R3/QA-F1) —— 改了 SC-22 的正则与 5 处概念提法; **是否还有第 6 处兄弟位置未扫到**, 请复核。
7. **主控在本轮的一次误判留痕** (§5.1 判定式段): 一度把形态判定式换成被原依据明确否决过的「读 `linked_issue`」, 恢复 D12 第三列时才发现。⇒ 请 R4 特别检查**其余被我改动的条款里, 有没有同样覆盖掉了某条原依据**。

## 本轮未做 / 存疑 (给 R3 审计席)

> **写在这里而不是省略**: 隐瞒未做项会让下一轮审计在错误的完成度假设上工作 (memory `past-summary≠measurement`)。

| # | 未做 / 存疑 | 影响 |
|---|---|---|
| 1 | **editlist FIX-18 的 S3 勘误注已落**, 但 **`.aria/spikes/2026-08-02-S3-track-id-derivation.md:72` 本轮未实读复核** —— 该行号与内容沿用 editlist 的记述, 未自行验证 (零发明行号的边界: 引的是 editlist 的断言, 非本轮实读) | 若 editlist 记错了 spike 的行号, §2.1 的勘误注会指向错误位置; 勘误的**结论** (`:242` 是 hostname 兜底) 已由本轮实读独立确认, 不受影响 |
| 2 | **7c / 7d 两个分支的具体行号未实读** —— §2.1 的备选证伪引用了 7c 的条件表达式与 7d 的注释**原文**, 但**没有给行号** (清单 #22 已声明) | 论证成立与否不受影响 (引的是逐字原文), 但 A.2 实施时须先定位这两个分支 |
| 3 | **`phase-a-planner/SKILL.md` 内部的委派动作 / skip 条件行号未实读** —— §3 幂等分工段只给了语义, 没给锚点 (已在该段显式声明) | A.2 拆任务时须补钉 |
| 4 | **rule6_note 新 substitute 的负控未验** —— 只验了「baseline 必红」, 未验「对『只注册两键、漏 `unattended`』这种坏实现是否也红」 | 见「新表面」#4 |
| 5 | **`linked_issue_overlap == null` 对 Phase B 消费面的影响未处置** | 见「新表面」#6 —— 这是本轮**已知未闭**的一条 |
| 6 | **两个子 Spec 的内容本轮未读、未核** —— `linked-issue-field-availability` / `sibling-spec-probe` 由另外的执笔席并行起草, 本文件只给了**指针与依赖方向**, **未核对**它们是否真的接住了迁出的 C-A / M-1 / M-5 / M-6(audit-engine 档) / M-10 / M-17(§4 stdout) / FIX-06/07/08/10 | 若某条在两边都落空, 本轮的「迁出」就变成了「丢弃」。**R3 须跨三份 Spec 联审这一点** (memory `feedback_combined_mode_sister_spec_audit_value`) |
| 7 | **SC-2 与 SC-23 是一对负控, 但未验证它们不会同时为真** —— SC-2 要求 track-id 含容器段 (两轨可辨), SC-23 要求 A.1 原串与 carry-id 一致 | 二者在设计上相容 (carry-id 就是含容器段的那一串), 但**没有一条测试断言这个相容性**; A.2 须补 |

---

## 闸门状态 (Rule #10 — AI 不自行判定)

`audit.checkpoints.post_spec = "convergence"` **enabled**, 封闭豁免白名单四类无一适用 ⇒ **本版按默认跑 post_spec, 不豁免**。

**已裁事实** (rework v3 更新):

1. **重写 v2 的 post_spec R1 (5 席) 已跑完**, 判定 **5/5 REVISE**, 去重后 5 个 critical 簇 —— **不是豁免, 是走了正常闸门**;
2. **R2 (5 席) 已跑完**, 判定 **REVISE 未收敛**: 3 个 critical 簇 + **17 个 major 簇 (与 R1 持平)**。**⚠️ 本条取代旧版第 2 点的「R1-fix 已全量吸收」自述** —— 该自述**不实** (R2/CR-M4 命中: editlist 12 项未落), 现已删除并替换为上方「**R1-fix editlist 逐条对账**」段的逐项状态表 (FIX-01…19), **不再有任何无锚点的总结句**;
3. **owner 已于 2026-08-22 下裁 C1/C2**: C1 采 (a) 扩权; **C2 原采 (ii)+(iii), 2026-08-23 owner 复议后 (iii) 撤销, 只采 (ii)** —— `STALE_TTL` 维持 `1800` 不改, 四个落点已在 rework v3 逐一回撤 (SC-20 / Impact `lib/constants.py` 行 / §2.3 残余风险段 / 本段);
4. **owner 已于 2026-08-23 下裁方向 b (缩 scope)**: §1 → `linked-issue-field-availability`, §4 → `sibling-spec-probe`, 主体只留 A.1 入口认领 + track-id 契约 (C-B/C-C 必须在此解), **换人执笔**一次性清 R1 editlist 残项后再 R3;
5. **下一步**: 本版进 **post_spec R3 (convergence 续审, `max_rounds` 剩 2)**。**AI 不预判 R3 的裁决结果。**

**本轮的 AI 流程判断 (Rule #10 — 请 owner 复议, 不自行落定)**:

| # | 判断 | 为什么须复议 |
|---|---|---|
| 1 | **切出审计轨** (D-J): 把「审计与 spike 轨迹」整节 + 两处已闭环的「请 owner 复议」叙事 + (iii) 撤销前落版原文, 按字节搬到 `.aria/audit-reports/a1-entry-claim-audit-trail.md` | 仿姊妹 Spec 的 owner 2026-08-07 先例, 但**本 Spec 没有对应的 owner 裁定**; 搬运无损, 撤回成本低 |
| 2 | **carry-id 统一采 editlist 选项 A** (改三处 SKILL.md 占位串取值口径) | editlist U-3 明写「需 owner 判这算不算『动 Phase B』」; 本版按「owner 要求主体必须解 C-C」推定采 A, **推定本身未经确认** (§2.1b 边界段) |
| 3 | **§2.3 选项集按 status 分档** | 三个审计镜头都没提出该形态, 是执笔的综合裁断, 且它扩大了 A.1 的决策面 (见「本轮引入的新表面」#2) |

本 Spec 在 R3 通过并经 owner 批准前不进 A.2/A.3。
