# Proposal: a1-entry-claim-duplicate-work-guard

> **Status**: 📝 **Draft (rewrite v2 + R1-fix + C1/C2 落版 + rework r1–r3)** — **post_spec R2 (2026-08-23, 5 席) REVISE 未收敛**: 3 critical 簇 (C-A §1 抽取规则 defer 恒红 [R1 遗留] / C-B track-id 无方向区分 release 连坐 [R1 遗留升级] / C-C A.1 track-id 含容器段与 Phase B/D carry-id 不一致 [新]) + 17 major 簇 (与 R1 持平; CR 实核 R1-fix editlist 12 项未落) — **待 owner 方向裁定** (换人执笔一次性清 R1 editlist + 三 critical 后 R3 / 缩 scope 拆 §4 探针与 §1 抽取规则 / (iii) 维持或撤销), 见 `.aria/audit-reports/post_spec-R2-1787481000000-a1-entry-claim-rewrite-aggregated.md` §处置建议 与本文 §2.2「请 owner 复议」。AI 不自行选。
> **Created**: 2026-07-30 · **重写**: 2026-08-02
> **Spec Level**: 2
> **代码落点**: `aria/` 子模块; Spec 落主仓 (Rule #5)
> **ship target**: 待定
> **前置依赖**: **[`linked-issue-normalization`](../linked-issue-normalization/proposal.md) 已 ship** (**R1 rework 核验订正**: 原文写「v1.66.0 已认领」, 实际以 **v1.67.0** 合并提交 `ca52d1c` 于 **2026-08-23T09:14:07Z** 合入 `origin/master`, 早于本文件本轮修订落盘) —— 前置依赖已满足, 本 Spec 的 overlap 检测可建立在其归一之上; `linked_issue_overlaps` 三参数签名未变 (详见「事实断言逐条实读清单」#16)。

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
| `phase-b-developer` :88-93 / `branch-manager` :149 | ✅ Phase B 入口 |

**ref 实测**: 竞品轨于 `07-27T11:53:12Z` **确实认领过** —— 但那是**在它跑完 4 轮 post_spec 之后**。

⇒ **认领点在 Phase B, 只能保护「已做完 Phase A 的人不被打扰」, 保护不了「正要开始的人不做重复功」。认领必须早于投入, 否则它记录的是既成事实而非预防碰撞。**

### ⚠️ spike 推翻的两条上游结论 (若不重写会被原样吸收)

| 上游结论 | spike 实测 |
|---|---|
| R2/M2:「basename 截断型别名恒漏是活跃问题」 | **S4 (⚠️ 2026-08-04 订正)**: 在**真正会被传给 `--linked-issue` 的总体**里截断型别名 **= 0 实例**, ref 已落盘总体同样 0 ⇒ 降为已知限。**但 S4 原报的「比例是反的 / R2 量错了总体」已作废** —— 逐字复跑 R2 的口径得 25/11 (与其 24/10 一致), 两组口径与范围都不同, **S4 自己做了一次跨总体比较, 与它指控 R2 的错误同形**。R2 的口径其实更贴近 `--linked-issue` 真实取值 |
| R3/M3a:「`./_` 分隔符碰撞属 dormant, 本组织无含 `.`/`_` 的仓名」 | **S5**: `10CG/10cg.local` 是**真实仓** (Forgejo API 实测, 11 open issues, handoff 引用过) ⇒ **活跃, 非 dormant** |

---

## ⭐ 真正的瓶颈 (S4 的意外发现, 决定本版结构)

**「关联 Issue」字段在 141 篇 proposal 语料中只有 13 篇有 —— 9%。**

主机制靠 `linked_issue` 匹配。**九成的 proposal 根本不提供这个输入。** 别名归一、track-id 派生、heartbeat 全都建立在「字段存在」之上 —— 而它九成时候不存在。

⇒ **本版把「字段可得性」提为 §1**, 排在认领机制之前。这是原版三轮都没摆正的优先级: R1/M1 提过「省字段即免义务」, 但被当成一条 major 混在其他 11 条里, 而它其实是整个机制的入口条件。

---

## What Changes

### §1 「关联 Issue」字段可得性 (S4 — 最高优先)

1. **进模板**: `spec-drafter` 的 proposal 模板增「关联 Issue」字段。无关联时**显式写 `无`**, 不留空 —— 空与「忘了写」不可区分;
2. **格式固定**: `<org>/<repo>#<n>` 单一形态。`phase1_gate` help 示例即此形; 写全 org 可让「org 不参与匹配」在人工判别时有据 (回显原串时看得出是不是同一个仓);
3. **机械校验**: 新增 custom check —— proposal 有该字段且**从字段值中抽出的 canonical token** 可被前置 Spec 的归一解析, 或显式为 `无`。**severity: warning** (advisory-over-hardlock);
   > **⚠️ 必须先定「抽取规则」, 否则 check 上线即恒红 (R1-fix/C3, 2 席实跑)**: 实跑 141 篇 —— 13 篇有该字段者, 直接拿字段值喂前置 Spec 的归一 **OK = 0 / 不可解析 = 13**。原因: **真实写法是 markdown 链接形**, 例如
   > ```
   > > **关联 Issue**: [10CG/aria-plugin #122](https://forgejo.10cg.pub/10CG/aria-plugin/issues/122) (open; ...)
   > ```
   > 而 §1.2 规定的是裸形 `<org>/<repo>#<n>` 且**没给抽取规则**。⇒ (a) check 恒红 (129 篇存量恒黄); (b) 若照抄字段值传 `--linked-issue`, 收到的是**整个 markdown 链接** ⇒ **前置 Spec 要治的格式病在上一层复现**。
   > **抽取规则须在 A.2 定死并给可证伪 SC** (候选: 取字段值内第一个匹配 `[\w.-]+/[\w.-]+\s*#\d+` 的片段并剥内部空白)。**本 Spec 现有措辞不足以实现。**
4. **不追溯**: 存量 128 篇无字段的 proposal 不回填 (多为已归档)。

> **为什么校验而非仅模板**: 模板只影响新建, 且 AI 可以删。本 Spec 的 §Why 自证「AI 会遗漏步骤」—— **无机械回声的义务会退化**。

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
> `linked_issue_overlaps` **只在 `own_linked_issue` falsy 时短路** (`collision.py:207-208` 实读: `if not own_linked_issue: return []`), 而 `"无"` 是 **truthy** ⇒ **两份毫无关系的 Spec 只要都写 `无`, 就会互相命中 overlap**。实跑复现:
>
> ```
> linked_issue_overlaps([claimA(linked_issue='无'), claimB(linked_issue='无')], 'spec-a-uuid1', '无')
> → [{'track_id': 'spec-b-uuid2', 'linked_issue': '无', ...}]   # ❌ 误报
> ```
>
> ⇒ **`无` 的语义是「已核实无关联」(一条正证据), 不是一个可参与相等比较的 token。** 此时 track-id 走 §2.1 的回落形 `<spec-slug>-<container_uuid>`, 主机制对该轨**不产生输入** —— 该已知限须写进 §6 缺口表。
>
> **这条是 §1 的「显式写 `无`」与本节「实参逐字节取 token」两条 fix 之间的接缝** —— 三个对抗验证镜头都没抓到 (M3 只在 §4 探针层处理了 `无` 的归属, 没下移到 CLI 实参层), 由整合者实测发现。**属「多条 fix 互相拆台」的第二类形状。**

**触发时机**: A.1 **起草前**, 作为**独立标题级步骤** (仿 `phase-b-developer` 的 `### B.0`), **不塞进现有 A.1 的 YAML 动作列表** —— §Why 已证埋进长列表的单行指令会被静默跳过 (R3/M6)。

> **⚠️ `### B.0` 是形态类比而非实存锚点 (R1-fix/M8)**: `phase-b-developer/SKILL.md` 里**没有**字面的 `### B.0` 标题。此处引它是指「**独立标题级、与主流程动作列表平级**」这一形态, 不是要求实现者去找那个字符串。

#### §2.1 track-id 派生 (spike S3 定案)

`<归一后 basename>-<str(int(number))>-<container_uuid>`; 无关联 issue 时回落 `<spec-slug>-<container_uuid>`。

| 段 | 规则 | 依据 |
|---|---|---|
| `basename` | 经前置 Spec 归一 (含 S5 追加的 `./_ → -`) | 与 `derive_track_id` 两层对齐 |
| `number` | **`str(int(number))`** | 否则 `#007` 与 `#7` 派生两个 id ⇒ 自排除失效 ⇒ 自己较早的 claim 被误判为他人碰撞 |
| `container_uuid` | container-id 文件的 **`uuid` 字段本身**, **不截断、跳过 `label`** | `get_container_id()` 是 label 优先, 而文件模板**明确邀请**用户设 label ⇒ `devbox-A1`/`devbox-A2` 截断后碰撞。uuid 是机器生成定长 hex, 碰撞域 16⁸≈4.3e9 可算 (实测 Lab 仅 2 容器) |

**需新增**直取 `uuid` 字段的 accessor (现有 `get_container_id()` 不能直接用)。**hostname 兜底分支** (只读 fs) 同样返回 hostname, 接受其碰撞域 —— 该分支本身已是降级路径。

> **为什么必须含容器段**: 不含则两轨做同一 issue 派生出**同一** track_id, 而 `collision.py:219-220` 明写 `if c.track_id == own_track_id: continue` ⇒ **互相被排除 ⇒ overlap 恒空 ⇒ 主机制死** (R2/C1 实证)。
> **职责分离**: 「是不是同一个 issue」由 `linked_issue` 承载; 「是不是同一条轨」由 `track_id` 承载。原 R1-fix 把前者塞进后者, 两轨遂在 track_id 维度失去可辨性 —— 而 overlap 正靠它工作。

#### §2.2 保护窗 (spike S1 定案)

事故窗实测 **48–72h**, 而 `STALE_TTL` = 30min、`SWEEP_TTL` = 24h ⇒ 保护窗短于事故窗。

**处置 = heartbeat 匹配键改 `(container_id, normalized track_id)`**, 刷新**全部**匹配的 active claim。

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
> **(ii) 调用点 = `state-scanner` 入口的 AI 编排层, 每次 `/state-scanner` 必跑**:
> - **具体 CLI 入口 (R1 rework 核验 major-1 补钉)**: 「AI 编排层调用 heartbeat CLI」原文未点名具体入口, 现定为 `skills/state-scanner/scripts/phase1_gate.py` 新增 **`--heartbeat-only` 模式** —— 复用其既有 identity/fetch/push 管道; 只刷新**本容器本 track** 的 `heartbeat_at`, **不写新 claim, 不判碰撞** (与 A.1 acquire 调用是同一 CLI 文件下的两个独立模式)。若 A.2 落地时改为独立脚本 `scripts/heartbeat_gate.py`, 亦属同一变更面 (已按此登记进 Impact 表, 见下方)。自本条起, 本节及 SC-21 提到的「heartbeat CLI」均特指该入口;
> - **既有同构先例**: `phase1_gate` 的 Phase B-entry 挂法就是这个模式 —— **实读** `skills/state-scanner/SKILL.md:149`「接线点 = AI 编排层, 不是 `scan.py`」+ `references/layer-l-integration.md:15`「Design A 条件触发: 闸门仅在用户确认要进入 Phase B 时调用, 不在 scan.py 内自动执行」。heartbeat 挂同一层 (AI 编排层调用 `--heartbeat-only`, collector 内不跑), `skills/state-scanner/scripts/scan.py` 的 collector 逻辑**保持只读, 零改动**;
> - **与 B-entry 的关键差异**: B-entry 是**条件触发** (`coordination.enabled==true` 且 `tracks_multibranch.collision.kind` 非空才调); heartbeat 是**无条件** —— 只要本会话在 coordination ref 里持有 active claim, **每次 `/state-scanner` 被调用都刷新**, 不依赖碰撞检测结果 (它是维持性动作, 不是碰撞响应动作);
> - **落点**: `skills/state-scanner/SKILL.md` 的 Layer L Phase B 集成段 (`:143-178` 一带) 新增对称的「Layer L A.1 heartbeat 集成」小节, 写明触发条件/调用形态 (`--heartbeat-only`) /失败处置 (fail-soft, 不阻断 `/state-scanner` 主流程);
> - 关联 Aria#180 (heartbeat 零调用) 由本裁定一并解。
>
> **(iii) `STALE_TTL` 30min → 24h 量级** —— **实读落点 = `lib/constants.py:36`** (`STALE_TTL: int = 1800  # seconds`)。
> - **⚠️ 事实订正 (rework, 主控实读 aria@cb6bd5d)**: §2.3 原版称「所有 claim 在 `STALE_TTL`=30min 后即 stale ⇒ `--sweep-stale` 对几乎所有并发轨可达」, **这条因果链不成立**。实读 `lib/gc.py:341`—— `sweep_stale_active` 的 `stale_ttl_seconds` 默认值是 **`SWEEP_TTL`** (`lib/constants.py:51`, 86400s/24h), **不是** `STALE_TTL`; 且 `release_gate.py:141`(`sweep_stale_active(repo, now=ts)`) **未传** `stale_ttl_seconds` 覆盖, 故 `--sweep-stale` 的实际清扫阈值从来就是 24h, 与 `STALE_TTL` 的取值**无关**。`STALE_TTL` 实际控制的是 `reconcile._is_stale()` (`lib/reconcile.py:154-163`) 判定的「takeover-eligible」软信号 —— advisory、可在下次 read 时逆转 (`lib/constants.py:40-42` 逐字), 与 `--sweep-stale` 的**不可逆**改写是两回事。⇒ `release_gate.py:225` 的 help 文本 (`「顺带扫描: active 且 heartbeat 超 STALE_TTL → abandoned」`) 与 `state-scanner/SKILL.md:176` 的同款描述本身用词不准 (把 `SWEEP_TTL` 的行为记成了 `STALE_TTL`) —— 本 Spec 沿用了这处不准确描述, 现订正; 文档措辞本身的勘正**不在本 Spec 变更面** (非目标, 留 follow-up)。
> - **落版后的准确效果**: `STALE_TTL` 30min→24h 把 reconcile 的「stale/可 takeover」软信号窗口, 从「30min 未刷新即标 stale」**放宽**对齐到与 `SWEEP_TTL` 同量级 (owner 采 (iii) 的**收窄版**: 只到 24h, 不无限延长 —— 「收窄」修饰的是 (iii) 候选本身相对「无限延长」的克制, 不是 `STALE_TTL` 数值方向; `STALE_TTL` 数值本身是**放宽/变大**) —— 不再出现「heartbeat 编排层偶尔漏跑一次 (\<24h) 就被判 takeover-eligible」的假阳性。`--sweep-stale` 的**破坏性**清扫窗口本就是 24h, 不因本次改动而变。两个信号收敛到同一量级后, **残余风险**: 若 (ii) 的 `/state-scanner` 编排层调用**连续缺席超过 ~24h** (即 `SWEEP_TTL`), claim 仍会被 (a) reconcile 标 takeover-eligible 且 (b) `--sweep-stale` 清成 `abandoned` —— 但只要两次 `/state-scanner` 间隔 **≤24h**, claim 不 stale, 也不进 sweep 候选;
> - **不变量注释处置** (R1 rework 核验 minor-1 改标题 —— 原标题「TTL 变更量化的 sweep 语义代价」与内容不符: 内容讲的是常量注释同步, 不是 sweep 代价): `lib/constants.py:32` 现有注释断言不变量「`STALE_TTL == 3 × HEARTBEAT_INTERVAL`」(`HEARTBEAT_INTERVAL=600s`, `:28`) —— 若只改 `STALE_TTL` 不动 `HEARTBEAT_INTERVAL`, 该注释所述不变量将不再成立, 须在 B 阶段二选一: 显式改写注释承认「不变量在 heartbeat 编排层落地后已由『AI 编排层调用节律』替代『HEARTBEAT_INTERVAL 常量』」, 或按比例调 `HEARTBEAT_INTERVAL`。**sweep 语义代价 = 0**(阈值是 `SWEEP_TTL`, 见上方「落版后的准确效果」) —— 这里唯一要处理的是**文档不变量注释**要不要同步改, 与 sweep 行为本身无关。**本 Spec 不预判**, 留 A.2 任务项;
>
> **候选 (i) 未采纳**: 挂在 A.1 机械步骤上 (如每次写 proposal 文件后) 被 (ii)「每次 `/state-scanner` 必跑」覆盖同一诉求且触点更集中, 不再单独引入第二个挂载面。
>
> **⚠️ 实读订正 · 请 owner 复议** (R1 rework 核验 major-3(a)): owner 裁定原文的理据——「`STALE_TTL` 30min → 24h 量级收窄版兜底, 使『漏跑一次扫描』不至于立即暴露在 `--sweep-stale` 下」——**与实读不符**: 上方「⚠️ 事实订正」已确认 `--sweep-stale` 的实际阈值从来就是 `SWEEP_TTL` (24h), 从未读取过 `STALE_TTL`; 改 `STALE_TTL` 对 `--sweep-stale` **零影响**, 其真实效果只是把 `reconcile._is_stale()` 的 advisory「takeover-eligible」软信号窗口从 30min 放宽到 24h。⇒ 裁定理据所指向的风险 (「漏跑一次扫描就暴露在不可逆清扫下」) 本来就不成立 —— 无论改不改 `STALE_TTL`, `--sweep-stale` 的不可逆窗口一直是 24h; 真正因 (iii) 改善的是 advisory 软信号面, 不是理据描述的那个 sweep 风险。**请 owner 确认**: 订正后是否仍采 (iii) (改 `STALE_TTL` 至 24h 量级, 效果落在 advisory/takeover-eligible 面, 是把两个原本量级悬殊的软硬信号对齐的一个自洽改动, 与原理据描述的 sweep 风险无关), 还是改为只采 (ii) (heartbeat 编排层每次 `/state-scanner` 必跑落地后, 30min 的 advisory 窗口触发面已收窄, 或许不必再动常量)? **AI 不替裁**, 本版按「暂按裁定字面 (iii) 落版, 标 pending owner」处理 —— 上方「落版」段的 (iii) 内容维持不变, 待 owner 回应后再定是否回撤。
>
> **✅ 协调项已解** (`origin/feature/linked-issue-normalization` 分支状态, R1 rework 核验 major 订正, 主控实读): 该分支已于合并提交 `ca52d1c` (v1.67.0, `2026-08-23T09:14:07Z`) 合入 `origin/master` (`git merge-base --is-ancestor origin/feature/linked-issue-normalization origin/master` 成立), **早于本轮 rework 落盘**。实读 `origin/master` 上的 `lib/collision.py`: 新增 `normalize_linked_issue()` (`:178`) / `_linked_issue_matches()` (`:219`) 两个 helper, 插在 `linked_issue_overlaps` (`:230`) 定义之前 —— **确认未改** `linked_issue_overlaps` 的三参数签名 (`claims, own_track_id, own_linked_issue`)。行号已整体下移: `_TERMINAL` 由 `cb6bd5d:210` → `origin/master:268`; `if not own_linked_issue`/`return []` 由 `:207-208` → `:265-266`; `if c.track_id == own_track_id`/`continue` 由 `:219-220` → `:278-279`。**本节引用的 `lib/gc.py`/`lib/constants.py` 行号已核, 未漂移** (`git diff --stat ca52d1c^1 ca52d1c` 实测只触及 `SKILL.md` / `claim_schema.py` / `collision.py` / **一个** test 文件 `test_release_by_track.py`, 外加发布同步面文件 `marketplace.json`/`plugin.json`/`CHANGELOG.md`/`README.md`/`VERSION`; **R1 rework 核验 minor-2 订正**: 原文「两个 test 文件」为误记, 实为一个; 不含 `gc.py`/`constants.py`)。详见下方「事实断言逐条实读清单」#3/#5/#6/#16。已按 R1 rework 核验 major-2 补入 Impact 表 `lib/collision.py` 一行 (原表零覆盖), 见下方。

#### §2.3 overlap 消费

`linked_issue_overlap[]` 非空 ⇒ **在起草前**经 `AskUserQuestion` 请裁。

- **告警须含**: 对方 track-id / owner-container / claimed_at / **双方 `linked_issue` 原始串** (org 不参与匹配, 回显原串是误配的唯一人工判别手段) / `status`;
- **选项**: 「另起」/「**我去释放对方的 claim 后再开始 (两步人工)**」/「并轨」。
  > **「接手」不是一键动作 (spike S3 实测)**: `release_claim_by_track` 只匹配调用者**自己的** container (`claim_lifecycle.py:425`), **无任何函数支持*定向*释放某个指定容器的 claim**; 且既有 `_takeover_eligible` 因含容器段后两轨必然不同 track_id 而**对本场景不可达**。
  >   **⚠️ 事实订正 (R1-fix/C5, 主控实读)**: 原文写「无任何函数支持释放别的容器的 claim」**为假** —— `release_gate.py --sweep-stale` 的 help 逐字写着「active 且 heartbeat 超 STALE_TTL → abandoned (**跨 container**)」。存在的是**无差别的陈旧清扫**, 不是定向接手。⇒ 「两步人工」的结论仍成立 (sweep 不能用来「接手某条特定的轨」), 但理由须改为「**只有无差别 sweep, 没有定向 release**」。
  >   **⚠️ 与 §2.2 复合的风险 (R1-fix/C2 关联) — 已解决 + 残余风险**: §2.2 的「谁调 heartbeat」现已落版 (AI 编排层挂 `/state-scanner` 入口, 每次必跑 + `STALE_TTL` **放宽**到 `SWEEP_TTL` 同量级, 即 (iii) 的收窄版——只到 24h、不无限延长)。phase-d-closer 逐周期带 `--sweep-stale` flag, 故这条不是理论风险, 但已从「无人认领的裸暴露」降为「有界残余」: **残余风险 = 若 A.1 期间连续 ≥24h 未触发任何 `/state-scanner` 调用** (heartbeat 编排层随之连续 ≥24h 未刷新), claim 才会先被 reconcile 标 takeover-eligible, 继而落入 `--sweep-stale` 的清扫窗口; **反之, 两次 `/state-scanner` 间隔 ≤24h, claim 不 stale**。⇒ 措辞即定义, 避免实现者以为有一键路径。**跨容器 release 不在本 Spec 引入** (写别人的 claim 是权限面变更, 应独立评估);
- **不硬阻断** (撞 §非目标与 AD10), 但**也不是 AI 渲染一行后自行决定** —— 「继续起草」是对已知碰撞的处置决定, 属 owner 权限面 (Rule #10)。**advisory 的含义是机制不阻断, 不是 AI 可自行放行。**

#### §2.4 终态可见 + 传递链 (R3/C2)

`done` / `abandoned` 的同 issue claim **必须可见** —— A.1 场景下 `done` 恰恰是最该看见的信号 (「对方已经做完了」)。`collision.py:210` 的 `_TERMINAL` 会直接 skip 它们。

> **⚠️ 事实订正 (R1-fix/C4, 3 席 + 主控实读)**: 实读 `collision.py:210` —— `_TERMINAL = ("done", "abandoned", "unknown")`。
> - **不含 `yielded`** ⇒ `yielded` **今天就已可见**, 不需要本机制去救; 原文把它列进来是**错的事实断言**, SC-8 的该子例 **baseline 即绿**;
> - **含 `unknown`** ⇒ 它被 skip 而原文**完全没讨论**。`unknown` 的证据方向与 `done`/`abandoned` **相反** —— 后两者是「对方明确结束了」(正证据), 前者是「读不出对方状态」(**零证据**)。⇒ **不得与 done/abandoned 合并措辞**: `unknown` 命中时须按「未能核实对方状态」呈现, 与 §2.5 的 fetch 降级同一极性 (零证据不得当正证据)。

**`include_terminal` 的传递链 (**四**段缺一不可 — R1-fix/C6 补第 0 段)**:

0. **`lib/collision.py` 的 `linked_issue_overlaps` 增 keyword-only 形参** `include_terminal: bool = False` —— 实读现签名为 `(claims, own_track_id, own_linked_issue)`, **无该形参**; 不加则 `_main():1233` 传参直接 `TypeError`。**⇒ `lib/collision.py` 已补入 Impact 表** (R1 rework 核验 major-2 补, 原表零覆盖)。⚠️ **行号订正 (rework)**: 原文写 `:1232`, **实读** (aria@cb6bd5d) 调用语句 `out["linked_issue_overlap"] = linked_issue_overlaps(` 在 **`:1233`**; `:1232` 是其前一行 `claims = read_claims(repo).claims`。
   > ⚠️ 与前置 Spec 的边界: `linked-issue-normalization` 的 §非目标写「签名与返回 schema 不变」。本段**要改签名** ⇒ 两 Spec 须协调: 建议由**本 Spec** 承担该签名变更 (前置 Spec 只改内部谓词), 并在前置 Spec 的非目标处加一句「`include_terminal` 形参由 `a1-entry-claim` 引入, 不属本 Spec 变更面」。**该协调项须 owner 确认。**
   > **✅ 协调项现状已解 (R1 rework 核验 major 订正, 主控实读 `origin/master`)**: `origin/feature/linked-issue-normalization` 已于 `ca52d1c` (v1.67.0, 2026-08-23T09:14:07Z) 合入 `origin/master`, 早于本文件落盘。该分支在 `lib/collision.py` 落地的 `normalize_linked_issue()` / `_linked_issue_matches()` 两个 helper, 插在 `linked_issue_overlaps` 定义之前 —— **确认未改** `linked_issue_overlaps` 的三参数签名 (`claims, own_track_id, own_linked_issue`, 现 `origin/master:230-234`), 与本 Spec 「由本 Spec 承担签名变更」的协调建议**不冲突**。合并已使行号整体下移约 53-59 行: `_TERMINAL` 由 `cb6bd5d:210` → `origin/master:268`; `if c.track_id == own_track_id` 由 `:219-220` → `:278-279`; `phase1_gate.py:1233` (调用处) **不受影响** (该合并未触及 `phase1_gate.py`)。本 Spec 正文与 Impact 表引用的 `collision.py` 行号统一以 `origin/master` 为准, 已在下方「事实断言逐条实读清单」#3/#5/#6/#16 逐条核对。
1. `phase1_gate.py` 新增 CLI flag `--include-terminal` (store_true);
2. **在 `_main()` 的现有调用处** (`phase1_gate.py:1233`) 加关键字参数 —— **不碰** `run_gate` / `_run_gate_impl` 签名;
   > R3/C2 实测: `linked_issue_overlaps` 生产代码**只有这一处调用**, 位于 `_main()`、在 `run_gate` 返回**之后**独立追加; `_run_gate_impl` (**`:335`–`:1032`**, 至下一个顶层定义 `run_gate` 前 —— R1 rework 核验 minor-4 订正: 原文误记 `334-1075`, 见「事实断言逐条实读清单」#17) 对它 grep 命中 **0**。原 R2-fix 写「`run_gate` 签名透传」**架构上就是错的** —— 照它做会改错函数, 精确复现它自己要修的「生产不可达」。
3. A.1 调用模板**显式带该 flag**。

**SC 的断言层必须是 CLI 全链路**, 不是直调库函数 —— 否则「参数没接到 CLI」的实现仍能绿。

#### §2.5 开关与降级

- **受 `state_scanner.coordination.enabled` 控制**, `false` ⇒ **零调用** (与 Phase B 对称)。`phase1_gate` **本身不读 config**, skip 判断在调用方 SKILL.md 层 ⇒ 该条件须**显式写出**, 否则 opt-out 项目在 A.1 仍被强制写 claim + 推远端 (对未配 coordination ref 的第三方是外向副作用);
- **fetch 降级须进 `error` 契约**: `GateResult.error` 的 docstring (`:210`) **早已预留 `"fetch_degraded"` token 但从未被赋值** (又一个「已 ship ≠ 能用」)。降级时消费面按「**未能核实**」措辞, **不得**渲染成「无碰撞」(零证据不得当正证据)。

### §3 入口覆盖 (S6)

**实测差距**: coordination ref 里 **2 个**容器, 而 handoff 的 `owner-container` 出现过 **9 种** ⇒ **至少 7 种身份从未留下 claim**。

⇒ **A.1 须双落点**, 与 Phase B 对称 (后者有 `phase-b-developer` + `branch-manager` 两处):
1. `phase-a-planner/SKILL.md`;
2. **`spec-drafter/SKILL.md`** —— 它 `user-invocable: true` (实测 `:9`), 可直接绕过 phase-a-planner。

> ## ✅ 阻塞性前提 — 已裁 (R1-fix/C1 — 4 席独立命中 + 主控实读 → 2026-08-22 owner 裁定落版)
>
> **两个指定落点的 `allowed-tools` 都不支持本机制的核心动作。** 实读 frontmatter (rework 复读 aria@cb6bd5d 未变, 见下方「事实断言逐条实读清单」#1/#2):
>
> | Skill | `allowed-tools` (逐字, 变更前) | 缺 |
> |---|---|---|
> | `phase-a-planner/SKILL.md:9` | `Read, Write, Glob, Grep, Task, Skill` | **无 `Bash`** · **无 `AskUserQuestion`** |
> | `spec-drafter/SKILL.md:10` | `Read, Write, Glob, Grep, AskUserQuestion` | **无 `Bash`** |
>
> ⇒ §2 的 `python3 .../phase1_gate.py` 命令**在两个宿主上都跑不了**; §2.3 的 `AskUserQuestion` 请裁**在 phase-a-planner 上也跑不了**。
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
> **⚠️ 实读订正 · 请 owner 复议** (R1 rework 核验 major-3(b)): 上一轮把 owner 原话「落版义务: ... + Rule #6 按能力面变更申报 benchmark」改写成「不单独申请豁免、也不需要单独判据」, 二者语义相悖 (原话要求「去申报/跑 benchmark」, 改写读作「不需要单独判据、可并入覆盖外档定向 fixture 同批带过」) 且未经复议即落版 —— 已按上方「落版执行」项 2 撤销该改写。**所幸核实结论 (两套件实存 ⇒ 应照跑) 与 owner 原话字面 (「申报 benchmark」) 本就一致**, 本项技术处置**无需另行复议**, 此处仅记录订正过程供 owner 核对上一轮偏差; 如 owner 认为「申报 benchmark」另有所指 (例如指走一遍 `/skill-creator` 完整流程, 而非本版采用的「现有两套件全量跑一遍, 零裁量」), 请指出。

> **口径待定 (S6 附带发现)**: `owner-container` (形如 `simonfish/bfe8285d`) 与 claim 的 container 段 (`bfe8285d`) **口径已经不同**。本 Spec 采用 claim 侧口径 (uuid), 并把「两标识关系需成文」记为 follow-up —— **不在本 Spec 统一二者** (那会牵动 handoff frontmatter 规范, 属 standards 变更)。

### §4 竞品 spec 探针 (副机制)

`audit-engine` 每轮入口扫远端同 issue 的竞品 spec。

- **新增** `aria/skills/audit-engine/scripts/sibling_spec_probe.py` (stdlib-only; audit-engine 现零 `scripts/`, 已核对 `run_all_tests.sh` 与打包无影响);
- **扫描范围含归档**: `openspec/{changes,archive}/*/proposal.md` —— 实测第 5 次事故的真竞品在 `archive/` 下, 而只扫 `changes/` 时对 path-coverage **只命中作者自己那份**;
- **每轮跑**, 接在 `references/execution-modes.md` 的每轮循环入口。**Convergence (`:84-111`) 与 Challenge (`:113-144`) 两段都要改** —— 本仓 post_spec pin 死 convergence 不受影响, 但 aria-plugin 跨项目分发, `DEFAULTS.json:124-128` 的 `adaptive_rules.level_3 → challenge` 意味着下游 Level-3 会走 Challenge, 只 patch 前者会让那些项目**静默漏掉探针**;
  > **命名**: 称 **per-round 入口探针**, **不叫「Step 0.5」** —— `audit-engine/SKILL.md:85` 明写 Step 0 是「Round 1 启动前**一次性**」, 挂它旁边与「每轮」自相矛盾;
- **fetch: 自带, 且它不轻量 (spike S2 实测)**:

  | 项 | 实测 |
  |---|---|
  | 双远端 fetch ×5 | 12.5 / 13.4 / 14.1 / 15.9 / 13.0 s (均值 **~13.8s**) |
  | 3 轮审计净增 | ~41s |
  | 瞬时失败 | 本会话 github 2 次 SSH 失败, 重试即恢复 |

  ⇒ 配 **30s 超时预算** + **重试** + 超时按 `degraded` 处置。**文档不得称其「轻量」** (R3/M4 原措辞), 须写明实测代价让采用者自判。
  > **复用 `remote_refresh` 缓存判否**: 缓存唯一写入点 `remote_refresh.py:691` 只被 `scan.py` Phase 0.5 调用 ⇒ audit-engine 轮间无机制保证跑过 state-scanner ⇒ 跨天审计会读到首轮陈旧缓存 = D3 要修的病换条更深路径复现;
- **规模上限**: 只扫 `enforced_remotes` × 各自默认分支 (**非全部 ref**) —— 同库 `handoff_multibranch.py` 已因 **440 条远端分支**踩坑并做了 scan cap。超限须 `log()` 披露被丢弃范围 (no silent caps);
- **消费面**: 命中 ⇒ 该轮审计报告入口段渲染 🔴 一行 + 写入聚合报告; **不阻断**。exit code: **0 = 无命中 / 0 = 有命中** (命中不是错误) / **非 0 仅用于探针自身失败**;
- **盲区声明 (不得当主防线)**: 只看得见**已 push** 的竞品。它覆盖的是主机制够不到的两个场景: (a) 对方**没走 claim** (S6 实测 7/9 身份如此); (b) 对方**已 ship 并归档**。

### §5 claim 生命周期 — A.1 引入的三条新退出路径

| 路径 | 处置 |
|---|---|
| **探索性放弃** (A.1 试三个方向弃两个) | 判定「不起该 Spec」时**必须**调 `release_gate.py --status abandoned`; 义务写进 SKILL.md + SC |
| **slug 改名** | track-id 不含 slug (§2.1) ⇒ **改名不改 id**, 问题从源头消失。**但无关联 issue 的回落分支仍含 slug** ⇒ 该分支须走 **release 旧 + acquire 新** 两步 (`release_claim_by_track` 按 `(container, track_id)` 定位、**不依赖 session**, 可直接照字面实现) |
| **D.2b 对偶** | 只有**走完循环**的轨才到 D.2b; 上面两条**不经过它**, 故各自显式 release |

### §6 残余缺口 (成文, 不假装覆盖)

| 缺口 | 窗口 | 覆盖它的机制 |
|---|---|---|
| 双方都未 claim 且未 push | 秒级 (claim 推送延迟) | 无 |
| 一方跳过 A.1 直调 `/spec-drafter` | — | **§3 双落点已覆盖** |
| 一方 `coordination.enabled=false` | 无界 | 无 (设计如此, opt-out 是项目的权利) |
| legacy 轨 (不用 phase1_gate 的历史/第三方容器) | 无界 | **§4 探针部分覆盖** (S6: 7/9 身份属此类) |

**中心化 spec 登记表: 仍然不做 (spike S6, 依据全换)**。原依据「残余缺口仅秒级」是实质低估, 已作废。新依据: **登记表解决不了这些缺口** —— 它们共同根因是「**没走进入口**」, 换个存储位置不改变这一点, 它是同一问题的另一载体而非解法; 真正的杠杆是**入口覆盖率** (实测 9 vs 2), 即 §3 的方向。登记表的一致性/并发写/GC 是常驻成本, 收益却依赖同一个前提。

---

## 事实断言逐条实读清单 (rework, R1 聚合报告处方)

> **触发**: post_spec R1 聚合报告 (`.aria/audit-reports/post_spec-R1-1785710000000-a1-entry-claim-rewrite-aggregated.md`) 判定「三条最重 critical 都是设计对了但对既有代码的事实断言与实读不符」⇒ 下一版须补本清单。该聚合报告实际给出**两条** CR 处方: (i) 本清单 (已落, 见下表); (ii) **track-id 形态 × 生命周期动词影响矩阵** —— 本轮 **defer 到 A.2**, 理由: 该矩阵需要「track-id 形态」(含容器段 vs §2.1 回落 slug 形) 与「生命周期动词」(acquire/heartbeat/release/sweep/gc) 两轴逐格核对, 而各动词的具体调用点/参数在 A.2 任务拆解前尚未定形 (例如 §2.1 「需新增直取 uuid 字段的 accessor」尚未有任务编号), Spec 文档层面此刻构建该矩阵只能停留在猜测态; A.2 派生任务时矩阵会随任务自然成形, 届时补更实。
> **方法**: 本表逐条列出 Spec 全文引用的 `文件:行号` 事实断言, 与 rework 时**现在实读**结果比对。**实读环境**: aria 子模块 `git -C aria rev-parse --short HEAD` = **`cb6bd5d`** (分支 `fix/issue-batch-149-151-155-134`)。**`collision.py` 相关行 (#3/#4/#5/#6/#16) 额外复核 `origin/master`** (`ca52d1c`, v1.67.0, 已含 `linked-issue-normalization` 合并, 2026-08-23T09:14:07Z 落地 —— **早于本轮 rework 落盘**, R1 rework 核验 minor-2 订正: 原文引用具体 mtime `09:32:38Z` 会随每次落盘漂移, 改为只用相对顺序描述; 详见 §2.2/§2.4 协调项)。行号漂移是预期内的 (spec 写于 v1.65.x 附近, aria 现已到 v1.66.5+); **不一致的已在正文对应处订正**, 本表汇总一份可核对的清单, 不重复正文的完整论证。

| # | 断言原文 (Spec 引用) | 现在实读结果 (aria@cb6bd5d, collision.py 相关另核 origin/master@ca52d1c) | 一致性 |
|---|---|---|---|
| 1 | `phase-a-planner/SKILL.md:9` — `allowed-tools: Read, Write, Glob, Grep, Task, Skill` | 确认 `:9` 逐字一致 (`origin/master` 上该合并未触及此文件, 行号同样未变) | ✅ 一致 |
| 2 | `spec-drafter/SKILL.md:10` — `allowed-tools: Read, Write, Glob, Grep, AskUserQuestion`; `:9` — `user-invocable: true` | 确认 `:10`/`:9` 逐字一致 (`origin/master` 未触及此文件) | ✅ 一致 |
| 3 | `collision.py:210` — `_TERMINAL = ("done", "abandoned", "unknown")`, 在 `linked_issue_overlaps` 内 | `cb6bd5d:210` 逐字一致。**R1 rework 核验 major 补**: `origin/master` (`ca52d1c`, 已含前置 Spec 合并) 上同一行下移至 **`:268`**, 取值逐字未变。**附注**: `collision.py` 内还有第二处同名 `_TERMINAL = ("done", "abandoned")` (cb6bd5d `:307` / origin/master `:366`, 在 `classify()` 内, **不含** `unknown`) —— 两处同名不同值, 属**不同函数的局部变量**, 本 Spec 引用的都是这一处, 未混淆, 但记于此避免后续实现者看错函数 | ✅ 一致 (+ 新增附注 + master 行号已核) |
| 4 | `linked_issue_overlaps` 现签名 `(claims, own_track_id, own_linked_issue)`, 无 `include_terminal` 形参 | `cb6bd5d:177-181` 逐字一致, 三参数, 无该形参。**R1 rework 核验 major 补**: `origin/master` 上该签名下移至 `:230-234`, **仍为三参数, 未加 `include_terminal`** | ✅ 一致 (+ 见 §2.4 协调项: sibling 分支未改签名, master 行号已核) |
| 5 | `collision.py:207-208` — `if not own_linked_issue: return []` | `cb6bd5d:207`/`:208` 逐字一致。**R1 rework 核验 major 补**: `origin/master` 上下移至 **`:265`/`:266`**, 逐字未变 | ✅ 一致 (+ master 行号已核) |
| 6 | `collision.py:219-220` — `if c.track_id == own_track_id: continue` | `cb6bd5d:219`/`:220` 逐字一致。**R1 rework 核验 major 补**: `origin/master` 上下移至 **`:278`/`:279`**, 逐字未变 | ✅ 一致 (+ master 行号已核) |
| 7 | `phase1_gate.py:1232` — `_main()` 调用 `linked_issue_overlaps` 处 | **不一致**: `:1232` 是 `claims = read_claims(repo).claims`; 实际调用语句 `out["linked_issue_overlap"] = linked_issue_overlaps(` 在 **`:1233`** | ❌ 不一致 → **已订正** (§2.4 item 0/2, D5, Impact 表, 共 4 处 `:1232`→`:1233`) |
| 8 | `claim_lifecycle.py` `heartbeat()` 定义, 按 `(container_id, session_id)` 匹配 | 确认 `def heartbeat(` 在 `:178`, 机制 (读 claims → 按 container+session 定位 → 写回) 描述准确 | ✅ 一致 |
| 9 | `release_claim_by_track` docstring 逐字引用 (「release_claim locates by (container, session), but a later invocation runs with a FRESH session_id...this variant locates by (normalized track_id, container) and ignores session」) | 确认 `def release_claim_by_track(` 在 `:377`, docstring `:387-393` 实质内容逐句对应 (措辞小幅改写但语义与用词一一对应) | ✅ 一致 |
| 10 | `claim_lifecycle.py:425` — `release_claim_by_track` 只匹配调用者自己的 container | 确认 `:425` 逐字 `if rec.container == resolved.container_id` | ✅ 一致 |
| 11 | `identity.py` — `get_container_id()` label 优先, 现有 accessor 不能直接拿 `uuid` 字段 | 确认 `def get_container_id(` 在 `:191`, label-优先 return 在 `:222` (`return label if label else uuid`), hostname 兜底在 `:242`; grep 全文无独立的「只返回 uuid 不看 label」accessor, 「需新增」判断成立 | ✅ 一致 |
| 12 | `GateResult.error` docstring (`phase1_gate.py:210`) 早已预留 `"fetch_degraded"` token 但从未被赋值 | 确认 `:210` 逐字 (「Possible values: ... "fetch_degraded", ...」); 全文 grep `"fetch_degraded"` 字面量**仅此一处**, 无任何 `error=` 赋值语句用到它。**附注**: `:475` 有一条 `logger` 日志消息文案含「fetch degraded」字样 (检测逻辑客观存在, 只是没有把结果写进结构化 `error` 字段) —— 支持而非削弱原断言 | ✅ 一致 (+ 新增附注) |
| 13 | `STALE_TTL` = 30min, 定义处 | 确认 **`lib/constants.py:36`** — `STALE_TTL: int = 1800  # seconds`; 同文件 `:51` `SWEEP_TTL: int = 86400  # seconds (24h)`; `:32` 有「`STALE_TTL == 3 × HEARTBEAT_INTERVAL`」不变量注释 (`HEARTBEAT_INTERVAL=600s`, `:28`) | ✅ 一致 (落点已写入 Impact 表 + §2.2) |
| 14 | **新增发现 (原文未列, rework 审出)**: §2.3 称「所有 claim 在 `STALE_TTL`=30min 后即 stale ⇒ `--sweep-stale` 对几乎所有并发轨可达」 | **不一致**: 实读 `gc.py:341` (`sweep_stale_active` 的 `stale_ttl_seconds` 默认值是 `SWEEP_TTL` 非 `STALE_TTL`) + `release_gate.py:141` (`sweep_stale_active(repo, now=ts)` 未传覆盖值) ⇒ `--sweep-stale` 的实际阈值从来就是 `SWEEP_TTL`(24h), 与 `STALE_TTL` 取值无关。`STALE_TTL` 实际控制的是 `reconcile.py:154-163` 的 `_is_stale()`(takeover-eligible 软信号, 可逆)。**该混淆同样出现在 `release_gate.py:225` 的 help 文本、`state-scanner/SKILL.md:176` 与 `phase-d-closer/SKILL.md:56` 三处描述里** (三处都把 `SWEEP_TTL` 的行为写成了 `STALE_TTL`; `phase-d-closer/SKILL.md:56` 一处为 R1 rework 核验 minor-3 补) —— 本 Spec 沿用了这处代码库既有的不准确表述, 非本 Spec 独有 | ❌ 不一致 → **已订正** (§2.2/§2.3), 文档措辞本身的勘正记为 follow-up (非本 Spec 变更面) |
| 15 | `state-scanner/SKILL.md:149` + `references/layer-l-integration.md:15` — B-entry「接线点 = AI 编排层, 不是 `scan.py`」/「Design A 条件触发」 | 确认两处逐字一致, 用作 heartbeat 编排层挂载点的既有先例引用 (§2.2 C2 落版) | ✅ 一致 (新增引用, 供 C2 落版佐证) |
| 16 | `origin/feature/linked-issue-normalization` (原记「另一容器在改」) 是否已改 `linked_issue_overlaps` 签名 | **R1 rework 核验 major 订正**: 该分支**已合并** —— `git -C aria merge-base --is-ancestor origin/feature/linked-issue-normalization origin/master` 成立, 合并提交 `ca52d1c` (v1.67.0) 时间戳 `2026-08-23T09:14:07Z`, **早于本轮 rework 落盘** (R1 rework 核验 minor-2 订正: 不再引用会漂移的具体 mtime); 「另一容器在改」在本轮实读时已是过期描述。实读 `origin/master:lib/collision.py` diff: 新增 `normalize_linked_issue()` (`:178`) / `_linked_issue_matches()` (`:219`) 两 helper, **未改**三参数签名; `_TERMINAL`/`linked_issue_overlaps` 等下游行号已整体下移 53-59 行 (逐行对照见 #3/#4/#5/#6) | ✅ 已合并, 签名未变, 行号已按 origin/master 核对完毕 (不再是「待重新核验」的悬置项) |
| 17 | `_run_gate_impl` (原文标 `334-1075` 行) 对 `linked_issue_overlaps` grep 命中 0 (§2.4 item 2, R3/C2 实测结论) | **不一致**: `def _run_gate_impl` 实际起始行是 **`:335`** (非 `:334`), 其后至下一个顶层定义 `def run_gate` (**`:1032`**) 前结束, 并非 `:1075`。**grep 命中 0 的结论本身不受行号误差影响, 仍成立** (R1 rework 核验 minor-4 补) | ❌ 不一致 → **已订正** (§2.4 item 2 行号改引 `:335`–`:1032` 区间, 不再用误记的 `334-1075`) |

**未逐条实读的低风险断言**: S1/S3/S4/S5/S6 各 spike 报告内部的实测数据 (语料统计 141/13 篇、事故窗 48-72h、fetch 耗时 ~13.8s 等) 属**一次性历史测量**, 非可重复 grep 的代码事实, 不纳入本清单 (清单聚焦「代码当前状态」类断言); spike 报告本身的可信度已由 owner 2026-08-02 的 A+B 裁定认可, 不在本次 rework 复核范围。

---

## 决策记录

| # | 决策 | 依据 |
|---|------|------|
| D1 | 「关联 Issue」字段可得性提为 §1, 排在机制之前 | **S4**: 141 篇语料仅 13 篇有该字段 (9%) —— 主机制九成时候没有输入 |
| D2 | 字段格式固定 `<org>/<repo>#<n>` + custom check (warning) | 模板只影响新建且可被删; 无机械回声的义务会退化 (§Why 自证) |
| D3 | track-id = `<basename>-<str(int(n))>-<container_uuid>` | **S3**: 不含容器段则两轨同 id ⇒ 被 `:219-220` 互斥 ⇒ 主机制死 (R2/C1); uuid 不截断不用 label (label 碰撞域不可控且模板鼓励设置) |
| D4 | heartbeat 匹配键改 `(container, track_id)`, 刷新全部匹配 | **S1**: `release_claim_by_track` 为**同一 defect** 做过同款修法, 照抄即可; session 落盘方案被它取代 |
| D5 | `include_terminal` 在 **`_main()` 现有调用处**加参数, 不碰 `run_gate` 签名 | **R3/C2** 实测: `linked_issue_overlaps` 只在 `:1233` 被调用 (rework 订正: 原 R3 记 `:1232`, 实读为其下一行), `_run_gate_impl` 零命中 |
| D6 | 「接手」= **两步人工**, 不引入跨容器 release | **S3** 实测无该函数; 既有 takeover 路径对本场景不可达; 写别人的 claim 是权限面变更 |
| D7 | 探针自带 fetch, **不称轻量**, 配 30s 预算 + 重试 | **S2** 实测 ~13.8s/轮; 复用缓存判否 (缓存只由 scan.py 刷新) |
| D8 | A.1 双落点 (phase-a-planner + spec-drafter) | **S6** 实测入口覆盖率是杠杆 (9 身份 vs 2 在 ref); `spec-drafter` `user-invocable: true` 可绕过 |
| D9 | 不建 basename 别名表 | **S4**: 在真实输入总体上别名实例 = 0; 分隔符型别名已由前置 Spec 的 S5 追加覆盖 |
| D10 | 不做中心化登记表 | **S6**: 解决不了「没走进入口」这个共同根因 |
| D11 | 探针不阻断, 命中 exit 0; 非 0 仅用于探针自身失败 | 与主机制同为 advisory |

**Rule #6 (rule6_note)**: 本 Spec 涉及**五处** SKILL.md 改动 (R1 rework 核验 minor-3 订正 —— 原版只列「四处/两档」, 未纳入 Impact 表已有的 `skills/config-loader/SKILL.md` 一行, 与 Impact 表互相矛盾, 现补齐第三档避免遗漏): **四处**处方性 · 运行时指令面改动 (按 CLAUDE.md 判据表分两档) + **一处**描述性改动:

- **`state-scanner/SKILL.md`「Layer L A.1 heartbeat 集成」小节** (C2 落版新增, 见 Impact 表): `aria-plugin-benchmarks/ab-suite/state-scanner.json` 套件实存 (`880060d` 刚对 `SKILL.md:176` 跑过 AB) ⇒ 落判据表**第二行「处方性 · 运行时指令面 / 能 / 照跑 AB, 零裁量」**。点名行为 **(d)**: 「持有 active claim 时, 每次 `/state-scanner` 入口调用都触发 `phase1_gate.py --heartbeat-only` 刷新该 claim」(R1 rework 核验 major-1 补钉具体 CLI, 原文泛称「heartbeat CLI」未点名入口) —— 该套件当前 eval case 未覆盖此新分支, A.2 须在既有套件内**新增 1 个 eval case** 钉住它 (与下方 SC-21 呼应; 这是「照跑 AB」义务的一部分, **不是**另起「覆盖外」fixture —— 刻意不把 (d) 塞进下面 (a)(b)(c) 那份「覆盖外」清单, 否则会把同一处 SKILL.md diff 同时判进两档, 复现本条要修的内部矛盾);
- **`phase-a-planner` / `spec-drafter` / `audit-engine` 三处 SKILL.md**——本 Spec 各自新增的 A.1/per-round 处方性行为——R1/QA **双套件实测**证明**现有固定 eval case** (与套件文件是否实存是两回事) **结构性覆盖不到**这批新行为 ⇒ 落判据表**第三行「套件覆盖外」**, 三条缺一不可:
  1. **点名行为**: (a) A.1 起草前必调 phase1_gate 且传 `--linked-issue`; (b) overlap 非空时经 `AskUserQuestion` 请裁而非自行放行; (c) fetch 降级时按「未能核实」而非「无碰撞」;
  2. **建可证伪定向 fixture**: 上述三条各一个 eval, 双臂须能分辨;
  3. **套件缺口开 issue**: 与 `aria-plugin#117` (缺 authoring 维度) / `#127` (缺 D9 surface 维度) 同族, 归并或新开由 A.2 定。
- **`config-loader/SKILL.md`** (R1 rework 核验 minor-3 新增归档) —— `coordination` 在 A.1 的 skip 语义**登记** (记录既有 `coordination.enabled` 字段在新增 A.1 skip 分支下的行为, 不新增判定规则、不改变任何 AI 决策路径) ⇒ 纯**描述性**内容, 落判据表**第一行「描述性」**; substitute = **SC-9** (状态类结构化测试, 断言 `enabled==false` 时 A.1 零调用/不写 claim/不推远端), 不需 AB。

**能力面附注 (C1 落版义务, 2026-08-22; R1 rework 核验 major-4 重判)**: `phase-a-planner` / `spec-drafter` 两处 frontmatter `allowed-tools` 扩权 (加 `Bash, AskUserQuestion` / 加 `Bash`) 是**能力面**变更, 影响该 skill **全部**运行场景 (含既有 AB 套件的既有 eval case), 与上面「套件覆盖外」三条**指令面**变更 (点名行为 a/b/c) 性质不同, 虽落在同一份 SKILL.md diff 里, 但按`standards/conventions/skill-benchmark-exemption.md` §1「**逐 hunk 判, 不逐文件判**」: `aria-plugin-benchmarks/ab-suite/phase-a-planner.json` / `spec-drafter.json` **两套件均实存** (2026-08-23 实核, 各 2 eval case) ⇒ 该能力面 hunk 独立落判据表**第二行「处方性 · 运行时指令面 / 能 / 照跑 AB, 零裁量」** —— **须照跑现有两套件**, 验的是「扩权后 skill 在既有 eval 场景下行为是否漂移」; 与上方 (a)(b)(c) 那部分的「覆盖外」定向 fixture **各自独立、互不替代**, 后者验的是「新增 A.1 claim 行为本身, 现有 eval 结构性覆盖不到」。**订正**: 上一版此处误判「能力面部分不单独申请豁免、也不需要单独判据, 由覆盖该 diff 的定向 fixture 同批带过即可」——两套件确实实存, 该误判与 owner 原话「Rule #6 按能力面变更申报 benchmark」(即: 该去申报/跑一次 benchmark) 实质相悖, 现改按「照跑」执行, 与 §3「落版执行」项 2 的订正同源 (详见 §3「⚠️ 实读订正 · 请 owner 复议」major-3(b) —— 该处核实结论与 owner 原话字面本就一致, 不构成新的复议项)。

确定性代码层由 SC 覆盖, 与上述并行不互替。**不申请豁免。**

---

## Success Criteria

> **验证面分层** (R1/C4: 原版把 SC 挂在**不存在的** `phase-a-planner` 测试宿主上):
>
> | 类 | 宿主 | 可机械断言 |
> |---|---|---|
> | 代码类 | `state-scanner/tests/` (既有) + `audit-engine/tests/` (新建) | ✅ |
> | 行为类 | **定向 AB fixture** (rule6_note 第 2 条) | ⚠️ 只能由 eval 覆盖, **不冒充结构化测试** |

### 四个被推翻版本的红窗 (spike S3 强调: 缺一则第五版会再踩)

| SC | 钉住哪一版的失败 | 场景 → 期望 |
|----|---|---|
| **SC-1** | 原始版 (spec-slug ⇒ 改名孤儿) | slug 改名前后 track-id **不变** |
| **SC-2** | R1-fix 版 (纯 issue 派生 ⇒ 主机制死) | 两**不同容器**同 issue 各自 A.1 认领 ⇒ 双方 `linked_issue_overlap` **各含对方** |
| **SC-3** | R2-fix 版 (`container-short` 前 8 位 ⇒ label 碰撞) | container-id 的 `label` 设为长字符串时, track-id 仍用 **`uuid` 字段** |
| **SC-4** | R3 指出的 number 表示不一致 | `#007` 与 `#7` 派生**同一** track-id |

### 主机制

| SC | 场景 | 期望 | 怎么会红 |
|----|------|------|---------|
| **SC-5** (代码) | heartbeat 跨 subprocess 两次调用 | 同一 track 的 claim 被刷新 | 按 `(container, session)` 匹配的现状必红 |
| **SC-6** (代码) | 同 (container, track) 有多条 active claim | **全部**刷新 | 只刷新一条必红 |
| **SC-7** (代码) | 超 `SWEEP_TTL` 未刷新 | 仍被 sweep | heartbeat 变成「永不过期」必红 |
| **SC-8** (代码, **CLI 全链路**) | 同 issue 他轨 claim 为 `done`/`abandoned`/`yielded` | **经 CLI 可见**, 措辞按 status 分档 | `_TERMINAL` skip 的现状必红; **且只测库函数的 SC 在「参数没接到 CLI」的实现上会绿** ⇒ 断言层必须是 CLI |
| **SC-9** (代码) | `coordination.enabled == false` | A.1 **零调用**, 不写 claim, 不推远端 | 无条件调用必红 |
| **SC-10** (代码) | fetch 降级 | `error` 非空; 消费面渲染「未能核实」而非「无碰撞」 | 现状 (`error: null`) 必红 |
| **SC-11** (行为) | overlap 非空 | AI 起草**前**经 `AskUserQuestion` 请裁; 告警含双方原始串 + status | 定向 fixture; 「渲染一行后自行继续」的臂应可分辨 |
| **SC-12** (行为) | spec 有「关联 Issue」但未传 `--linked-issue` | AI 不得跳过该参数 | 定向 fixture (**不冒充结构化测试**) |

### 字段可得性 / 生命周期 / 探针

| SC | 场景 | 期望 |
|----|------|------|
| **SC-13** (代码) | proposal 无「关联 Issue」字段 / 值不可解析 | custom check **warning**; 显式 `无` 则通过 |
| **SC-14** (代码) | A.1 判定「不起该 Spec」 | claim 状态为 `abandoned` |
| **SC-15** (代码) | 无关联 issue 的回落分支改名 | release 旧 + acquire 新两步后无孤儿 |
| **SC-16** (代码) | 竞品在 `openspec/archive/` 下 | **命中**, 措辞标「已完成的 Spec」 |
| **SC-17** (代码) | 远端无同 issue spec | 报告空, **exit 0**, 不阻断 |
| **SC-18** (代码) | 探针 fetch 失败 / 无远端 | `degraded` + 「本轮竞品扫描未执行」+ **exit 非 0** (与 SC-17 的 exit 0 形成可辨对照) |
| **SC-19** (代码) | 反向对照三条 | (a) 不得自命中本轨 spec 目录; (b) 不得把自己的 claim (同 track_id) 计入 overlap; (c) 扫描超上限**必须** `log()` 披露丢弃范围 |

### 保护窗可生产验证性 (heartbeat, R1 rework 核验 major 补)

> **触发**: 上一轮核验指出 —— §2.2 已自陈「换匹配键不产生刷新者 ⇒ SC-5~7 可以全绿而问题原样存在」, C2 裁定 (谁调/何时调 heartbeat + `STALE_TTL` 量级) 落版后, 全文却没有任何 SC 或 fixture 钉住这两点; 这正是 `feedback_completion_signals_vs_runtime_invocation` 同形的坑 (「已落版的一段 SKILL.md 文字」≠「会被生产调用的机制」)。下两条补上, **编号追加在 SC-19 之后**而非插入既有 SC-16/17 —— 遵守「不改 SC 编号」硬约束, 不重排已有 SC:

| SC | 类 | 场景 | 期望 | 怎么会红 |
|----|---|------|------|---------|
| **SC-20** | 代码 | 读取 `constants.STALE_TTL`; 对一条 23h 未刷新的 active claim 跑 `reconcile._is_stale()` | `STALE_TTL >= 86400` (24h 量级); `_is_stale()` 对 23h 未刷新返回 **False** (未 stale, 不可 takeover) | 现状 `STALE_TTL=1800`(30min) 时, 23h 未刷新必被判 stale ⇒ 必红 |
| **SC-21** | 行为 (定向 fixture, 与 rule6_note state-scanner 档呼应) | `/state-scanner` 入口被调用, 本会话在 coordination ref 持有 active claim | 两臂可辨 (R1 rework 核验 major-1 补钉具体 CLI, 原文泛称「heartbeat CLI」): (A) heartbeat 编排层已挂载 ⇒ 每次调用**都**触发 `phase1_gate.py --heartbeat-only` 刷新该 claim —— **可辨臂 (A) 的判据 = 该 CLI 被 subprocess 调用且 `claim.heartbeat_at` 被刷新**; (B) 未挂载 ⇒ 不触发, `heartbeat()` 生产调用点仍为 0 | 当前实现两臂**不可辨** —— `constants.py:43-44` 自陈「NO production heartbeat loop exists」, 无论挂不挂都是同一 (未触发) 结果 |

---

## 非目标

- **不改** `linked_issue` 归一本身 —— 属前置 Spec [`linked-issue-normalization`](../linked-issue-normalization/proposal.md);
- **不做** basename 截断型别名归一 (D9; 分隔符型已由前置 Spec 覆盖);
- **不做**中心化 spec 登记表 (D10);
- **不引入**跨容器 release (D6);
- **不把** advisory 升级为 block;
- **不动** Phase B 入口现有认领 (`include_terminal` 默认 False 保既有语义逐字节不变);
- **不改写**存量 coordination ref 数据;
- **不统一** `owner-container` 与 claim container 段的口径 (§3 已记为 follow-up, 属 standards 变更);
- **不回填**存量 128 篇无「关联 Issue」字段的 proposal。

---

## Impact

| 文件 | 变更 | 来源 |
|------|------|------|
| `skills/state-scanner/lib/claim_lifecycle.py` | heartbeat 增 by-track 变体 (仿 `release_claim_by_track` 并存模式) | **S1** (原版 Impact 表零覆盖) |
| `skills/state-scanner/lib/identity.py` | 新增直取 `uuid` 字段的 accessor (跳过 label); hostname 兜底分支成文 | **S3** (原版 Impact 表零覆盖) |
| `skills/state-scanner/lib/collision.py` | `linked_issue_overlaps` 增 keyword-only 形参 `include_terminal: bool = False` (现三参数签名 `origin/master:230-234`; `_TERMINAL` 定义 `origin/master:268`; 详见「事实断言逐条实读清单」#3/#4/#5/#6/#16) | **R1-fix/C6** (R1 rework 核验 major-2 补, 原表零覆盖) |
| `skills/state-scanner/lib/constants.py` | `STALE_TTL` (**`:36`**, 现 `1800` 秒/30min) 改为 **`86400` 量级/24h**; `:32` 的「`STALE_TTL == 3 × HEARTBEAT_INTERVAL`」不变量注释需同步改写或按比例调 `HEARTBEAT_INTERVAL` (`:28`, 二选一, A.2 定)。**R1 rework 核验 minor-1 补**: `:40`「Deliberately much longer than STALE_TTL」/ `:43-44`「NO production heartbeat loop exists」/ `:50`「Revisit when a heartbeat loop ships」三处 `SWEEP_TTL` 注释在 heartbeat 落地 (本 Spec) 后全部过期, 须随 A.2 实现同步改写 (三处描述的前提——「无生产 heartbeat」——本 Spec 之后不再成立) | **C2 落版** (owner 2026-08-22) |
| `skills/state-scanner/scripts/phase1_gate.py` | CLI flag `--include-terminal`; **在 `_main():1233` 加关键字参数**; `error` 契约携带 `fetch_degraded` | **R3/C2** (rework 订正行号 1232→1233) |
| `skills/state-scanner/scripts/phase1_gate.py` (第二处变更, 与上一行同文件不同能力) | 新增 **`--heartbeat-only` 模式** (复用其 identity/fetch/push 管道; 只刷本容器本 track 的 `heartbeat_at`, 不写新 claim, 不判碰撞) —— §2.2 (ii)「AI 编排层调用 heartbeat CLI」指的即此入口; 若 A.2 落地时改为独立脚本 `scripts/heartbeat_gate.py` 亦属同一变更面 | **C2 落版** (owner 2026-08-22, 采 (ii); R1 rework 核验 major-1 补, 原表零覆盖该具体入口) |
| `skills/state-scanner/tests/` (既有宿主) | SC-1~10, 14, 15, **20** | R1/C4 (SC-20: R1 rework 核验 major 补) |
| `skills/phase-a-planner/SKILL.md` | A.1 **独立标题级**认领步骤 + overlap 消费 + release 义务 + `coordination.enabled` skip | R3/M6 |
| `skills/phase-a-planner/SKILL.md` frontmatter `allowed-tools` | **`:9`** `Read, Write, Glob, Grep, Task, Skill` → `Read, Write, Glob, Grep, Task, Skill, Bash, AskUserQuestion` | **C1 落版** (owner 2026-08-22, 采 (a)) |
| `skills/spec-drafter/SKILL.md` | 第二落点 + proposal 模板增「关联 Issue」字段 | **S6** + **S4** |
| `skills/spec-drafter/SKILL.md` frontmatter `allowed-tools` | **`:10`** `Read, Write, Glob, Grep, AskUserQuestion` → `Read, Write, Glob, Grep, AskUserQuestion, Bash` | **C1 落版** (owner 2026-08-22, 采 (a)) |
| `skills/state-scanner/SKILL.md` | Layer L Phase B 集成段 (`:143-178` 一带) 新增对称的「Layer L A.1 heartbeat 集成」小节: AI 编排层挂载点、无条件触发 (每次 `/state-scanner`)、fail-soft 处置 | **C2 落版** (owner 2026-08-22, 采 (ii)) |
| `skills/audit-engine/SKILL.md` + `references/execution-modes.md` | per-round 探针; **Convergence 与 Challenge 两段都改** | R3/M5 |
| `skills/audit-engine/scripts/sibling_spec_probe.py` + `tests/` | **新增** (目录也新建) | — |
| `skills/state-scanner/references/layer-l-integration.md` | 该活文档明确断言「闸门仅在 Phase B 触发」, 本 Spec 后即过时 | R1/M8 |
| `skills/config-loader/SKILL.md` | coordination 在 A.1 的 skip 语义登记 | R1/M3 |
| `.aria/state-checks.yaml` | 新增「关联 Issue」字段校验 check | **S4** |
| AB 套件 — `phase-a-planner.json` / `spec-drafter.json` (能力面 hunk, 照跑档) | `allowed-tools` 扩权 hunk 影响全场景, 两套件均实存 (2026-08-23 实核) ⇒ **现有 AB 全量照跑, 零裁量**; 验「扩权后既有 eval 场景行为是否漂移」 | rule6_note 能力面附注 (R1 rework 核验 major-4 订正, 原判「不单独申请豁免」有误) |
| AB 套件 — `phase-a-planner` / `spec-drafter` / `audit-engine` (覆盖外档) | 定向 fixture ×3 (a/b/c) + 缺口 issue; 验「新增 A.1 claim 行为本身, 现有 eval 结构性覆盖不到」, 与上一行「照跑现有 AB」互不替代 | rule6_note |
| `aria-plugin-benchmarks/ab-suite/state-scanner.json` (照跑 AB 档) | 新增 1 eval case 钉 (d) 「持 active claim 时 `/state-scanner` 入口每次触发 `phase1_gate.py --heartbeat-only`」, 与 SC-21 呼应 | rule6_note (R1 rework 核验 major 补; CLI 具体化见 major-1) |

**follow-up (不在本 Spec)**: `owner-container` 与 claim container 段的口径统一 (S6 附带发现)。

---

## 审计与 spike 轨迹

| 阶段 | 产出 |
|---|---|
| post_spec R1 (5 席) | 4C/8M/7m — 发现 `linked_issue` 无归一 (主机制静默失效) |
| R1-fix | 全量吸收, SC 7→15 |
| post_spec R2 (新眼睛, type-design-analyzer) | 2C/4M/4m — **两条 critical 都在 R1-fix 自己写的逻辑上** |
| R2-fix | 全量吸收, SC 15→19 |
| post_spec R3 (第三双新眼睛, code-architect) | 2C/6M/3m — **同口径 major 4→6 上升 ⇒ 判定不收敛** |
| **owner 裁定 A+B** | §0 抽出独立交付; 其余转 spike |
| **spike S1–S6** | 六条全完成; **S4/S5 各推翻一条上游审计结论** |
| **重写 v2** | 据 spike 结论重写 (非打补丁) |
| **post_spec R1 (rewrite v2, 5 席: TL/BA/QA/CR/KM)** | **5/5 REVISE** — 去重后 **5 个 critical 簇**; **三条最重 critical 都是「设计对了但对既有代码的事实断言与实读不符」** (与旧版 R3/C2 同形) |
| **R1-fix** | 全量吸收 (C1~C6 事实订正 + NEW-01), **C1 (allowed-tools 阻塞) / C2 (heartbeat 谁调) 两项转 owner 裁定, 未即时落版** |
| **owner 裁定 C1/C2 (2026-08-22)** | C1=(a) 扩 allowed-tools / C2=(ii)+(iii) heartbeat 挂 state-scanner 编排层 + STALE_TTL 放宽 (30min→24h 量级, (iii) 收窄版: 只到 24h 不无限延长) |
| **rework 第 1 轮** | C1/C2 落版 + 新增「事实断言逐条实读清单」(R1 聚合报告处方) |
| **上一轮核验 (6 findings: 3 major/2 minor/1 待归属确认)** | rule6_note 四处 SKILL.md 分类内部矛盾 / heartbeat 无 SC 或 fixture 钉住 / collision.py 协调项已过期 (sibling 分支已合并) / STALE_TTL 方向词误写 / 「附注」悬空引用 / R1 报告第二条处方 (ii) 未处置 |
| **rework 第 2 轮** | 逐条处理上一轮 6 findings: rule6_note 改四处二档 + 新增 (d) 点名行为; 新增 SC-20/SC-21 (追加编号, 不重排既有 SC); collision.py 协调项按 `origin/master@ca52d1c` (已合并, 早于本文件落盘) 改写为已解事实 + 补 master 行号; 方向词/悬空引用订正; R1 报告 (ii) 处方 defer 到 A.2 并写明理由 |
| **上一轮核验 (第 2 轮独立核验, 8 findings: 4 major/4 minor)** | owner 裁定原文两处被整段删除换 AI 转述且与原文有实质偏差 (major-3, 最重) / heartbeat 具体 CLI 入口未点名 (major-1) / `lib/collision.py` 缺 Impact 表行 (major-2) / rule6_note 能力面 hunk 误判「不单独申请豁免」而两套件实存 (major-4) / constants.py 三处过期注释未列 (minor-1) / mtime 引用会漂移 + diff --stat 文件数误记 (minor-2) / rule6_note「四处」计数漏 config-loader (minor-3) / `_run_gate_impl` 行号误记 (minor-4) |
| **rework 第 3 轮 (本次)** | 逐条落实上一轮 8 findings: §2.2/§3 两处 owner 裁定原文按 `git show 86540f2` 逐字恢复 (blockquote), 下接「落版 (AI)」与「⚠️ 实读订正 · 请 owner 复议」两段 (major-3, 含 STALE_TTL/sweep 理据矛盾请 owner 复议 + Rule #6 措辞误改已撤销); heartbeat 具体入口钉为 `phase1_gate.py --heartbeat-only` (major-1, 同步改 §2.2/(d)/SC-21/Impact 表); Impact 表补 `lib/collision.py` 行 (major-2); rule6_note 能力面附注按逐 hunk 判重写为「两套件均实存 ⇒ 照跑」, Impact 表 AB 行拆两行 (major-4); constants.py 行补三处过期注释 (minor-1, 含标题订正); mtime 引用改相对表述 + diff --stat 订正为一个 test 文件 (minor-2); rule6_note「四处」改「五处」补 config-loader 描述性档 (minor-3, 含 STALE_TTL/SWEEP_TTL 混用第三处引用); `_run_gate_impl` 行号订正为 `:335`–`:1032` (minor-4); 事实清单新增 #17 — **待 post_spec R2 (convergence 续审)** |

报告: 旧版三轮 `.aria/audit-reports/post_spec-R{1,2,3}-*-a1-entry-claim-duplicate-work-guard-*` (`b7c4933` 之前) · **重写 v2 R1** `.aria/audit-reports/post_spec-R1-1785710000000-a1-entry-claim-rewrite-*` (5 席 + 聚合 + R1-fix editlist) · spike: `.aria/spikes/2026-08-02-*`

---

## 闸门状态 (Rule #10 — AI 不自行判定)

`audit.checkpoints.post_spec = "convergence"` **enabled**, 封闭豁免白名单四类无一适用 ⇒ **本版按默认跑 post_spec, 不豁免**。

**已裁事实** (取代原「⚠️ 闸门待裁」段的未决措辞 — 该段写于重写 v2 刚成文、尚未提交审计之时; 现 post_spec **R1 已跑**):

1. **重写 v2 的 post_spec R1 (5 席) 已跑完**, 判定 **5/5 REVISE**, 去重后 5 个 critical 簇 —— **不是豁免, 是走了正常闸门**, 结果证实「重写本身是新表面」的顾虑成立 (原第 4 点预判命中): §1/§2.1/§2.2 的新增条款确实被审出事实断言与实读不符的问题;
2. **R1-fix 已全量吸收**, 其中 C1 (两处 SKILL.md `allowed-tools` 缺 `Bash`/`AskUserQuestion`, 主机制不可执行) 与 C2 (heartbeat 换了匹配键但无人调) 两项因涉及 skill 能力面扩权 / TTL 常量变更, 判断超出「审计聚合报告直接吸收」的裁量范围, 转 owner 裁定;
3. **owner 已于 2026-08-22 下裁**: C1 采 (a) 扩权, C2 采 (ii)+(iii) 组合; **本次 rework 已把两项裁定落版本文** (§2.2/§2.3/§3 + Impact 表), 并按 R1 聚合报告的处方补齐「事实断言逐条实读清单」;
4. **下一步**: 本版进 **post_spec R2 (convergence 续审)** —— 审 rework 新落的 C1/C2 落版内容与新增的事实核验清单本身, 而非从零重审整份 Spec。

**AI 不预判 R2 的裁决结果。** 本 Spec 在 R2 通过并经 owner 批准前不进 A.2/A.3。
