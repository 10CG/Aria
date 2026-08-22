# Proposal: a1-entry-claim-duplicate-work-guard

> **Status**: 📝 **Draft (rewrite v2 + R1-fix + 两阻塞项已裁)** — **C1/C2 owner 裁定 2026-08-22 已下** (C1=(a) 扩 allowed-tools / C2=(ii)+(iii) heartbeat 挂 state-scanner 入口编排层 + STALE_TTL 30min→24h 量级): 待 rework 把两裁定落版 (§2.2/§3/阻塞性前提三处 + Impact 表补 allowed-tools 变更面) 后进 A.2
> **Created**: 2026-07-30 · **重写**: 2026-08-02
> **Spec Level**: 2
> **代码落点**: `aria/` 子模块; Spec 落主仓 (Rule #5)
> **ship target**: 待定 (v1.66.0 已由 [`linked-issue-normalization`](../linked-issue-normalization/proposal.md) 认领)
> **前置依赖**: **[`linked-issue-normalization`](../linked-issue-normalization/proposal.md) 必须先 ship** —— 本 Spec 的 overlap 检测建立在它的归一之上; 它不落地则主机制在真实语料上恒漏报。

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

> ## ⛔ 未决项 (R1-fix/C2 — 3 席命中): **换了匹配键, 但没说谁调、什么时机调**
>
> `heartbeat()` 的**生产调用点仍为 0** (`constants.py:43-44` 自陈:「NO production heartbeat loop exists」)。**换匹配键不产生刷新者** ⇒ 保护窗实质仍是 24h ⇒ **SC-5~7 可以全绿而问题原样存在**。
>
> **spike S1 §6 明确把「谁在什么时机调」交还给 Spec** (「属 Spec 范围不属 spike」), 而重写**没有接住**。
>
> **且判否「再调 phase1_gate」的理由原样适用于 heartbeat** —— 若 heartbeat 也靠 AI 记得调, 两者没有区别。⇒ **必须给它一个不依赖 AI 记性的触发点**, 候选:
> - (i) 挂在 A.1 内已有的**机械步骤**上 (如每次写 proposal 文件后), 由 skill 指令强制;
> - (ii) 挂在 `state-scanner` 的 Phase 0.5/1.16 (它每次 `/state-scanner` 必跑, 且已在 coordination 链路上);
> - (iii) 承认做不到, 改走延长 TTL 并量化 sweep 语义代价 (spike S1 的选项 c)。
>
> **A.2 前必须定死其一。** 在此之前 §2.2 只是「把匹配键修对了」, 不构成保护窗的解决方案。**这也是 §2.3 的 `--sweep-stale` 风险 (C5) 是否升级为数据面风险的判定条件。**
>
> **✅ owner 裁定 (2026-08-22): 采 (ii)+(iii) 组合** —— heartbeat 挂 state-scanner 入口的 **AI 编排层** (scan.py collector 保持只读, 与 phase1_gate B-entry 既有挂法同构; 每次 `/state-scanner` 必跑, 不依赖 AI 记性); 同时 `STALE_TTL` 30min → **24h 量级**收窄版兜底, 使「漏跑一次扫描」不至于立即暴露在 `--sweep-stale` 下。落版义务: (ii) 的挂载点写进 state-scanner SKILL.md 编排契约 + (iii) 的 TTL 变更量化 sweep 语义代价 (spike S1 选项 c 的评估框架); 关联 Aria#180 (heartbeat 零调用) 由本裁定一并解。

#### §2.3 overlap 消费

`linked_issue_overlap[]` 非空 ⇒ **在起草前**经 `AskUserQuestion` 请裁。

- **告警须含**: 对方 track-id / owner-container / claimed_at / **双方 `linked_issue` 原始串** (org 不参与匹配, 回显原串是误配的唯一人工判别手段) / `status`;
- **选项**: 「另起」/「**我去释放对方的 claim 后再开始 (两步人工)**」/「并轨」。
  > **「接手」不是一键动作 (spike S3 实测)**: `release_claim_by_track` 只匹配调用者**自己的** container (`claim_lifecycle.py:425`), **无任何函数支持*定向*释放某个指定容器的 claim**; 且既有 `_takeover_eligible` 因含容器段后两轨必然不同 track_id 而**对本场景不可达**。
  >   **⚠️ 事实订正 (R1-fix/C5, 主控实读)**: 原文写「无任何函数支持释放别的容器的 claim」**为假** —— `release_gate.py --sweep-stale` 的 help 逐字写着「active 且 heartbeat 超 STALE_TTL → abandoned (**跨 container**)」。存在的是**无差别的陈旧清扫**, 不是定向接手。⇒ 「两步人工」的结论仍成立 (sweep 不能用来「接手某条特定的轨」), 但理由须改为「**只有无差别 sweep, 没有定向 release**」。
  >   **⚠️ 与 §2.2 复合的风险 (R1-fix/C2 关联)**: 若 heartbeat 最终仍无人调 (见 §2.2 的未决项), 所有 claim 在 `STALE_TTL`=30min 后即 stale ⇒ **`--sweep-stale` 对几乎所有并发轨可达**。phase-d-closer 逐周期带该 flag ⇒ 这不是理论风险。**§2.2 的「谁调 heartbeat」不落地, 本条即从「已知限」升级为「数据面风险」。**⇒ 措辞即定义, 避免实现者以为有一键路径。**跨容器 release 不在本 Spec 引入** (写别人的 claim 是权限面变更, 应独立评估);
- **不硬阻断** (撞 §非目标与 AD10), 但**也不是 AI 渲染一行后自行决定** —— 「继续起草」是对已知碰撞的处置决定, 属 owner 权限面 (Rule #10)。**advisory 的含义是机制不阻断, 不是 AI 可自行放行。**

#### §2.4 终态可见 + 传递链 (R3/C2)

`done` / `abandoned` 的同 issue claim **必须可见** —— A.1 场景下 `done` 恰恰是最该看见的信号 (「对方已经做完了」)。`collision.py:210` 的 `_TERMINAL` 会直接 skip 它们。

> **⚠️ 事实订正 (R1-fix/C4, 3 席 + 主控实读)**: 实读 `collision.py:210` —— `_TERMINAL = ("done", "abandoned", "unknown")`。
> - **不含 `yielded`** ⇒ `yielded` **今天就已可见**, 不需要本机制去救; 原文把它列进来是**错的事实断言**, SC-8 的该子例 **baseline 即绿**;
> - **含 `unknown`** ⇒ 它被 skip 而原文**完全没讨论**。`unknown` 的证据方向与 `done`/`abandoned` **相反** —— 后两者是「对方明确结束了」(正证据), 前者是「读不出对方状态」(**零证据**)。⇒ **不得与 done/abandoned 合并措辞**: `unknown` 命中时须按「未能核实对方状态」呈现, 与 §2.5 的 fetch 降级同一极性 (零证据不得当正证据)。

**`include_terminal` 的传递链 (**四**段缺一不可 — R1-fix/C6 补第 0 段)**:

0. **`lib/collision.py` 的 `linked_issue_overlaps` 增 keyword-only 形参** `include_terminal: bool = False` —— 实读现签名为 `(claims, own_track_id, own_linked_issue)`, **无该形参**; 不加则 `_main():1232` 传参直接 `TypeError`。**⇒ `lib/collision.py` 必须进 Impact 表** (原表零覆盖)。
   > ⚠️ 与前置 Spec 的边界: `linked-issue-normalization` 的 §非目标写「签名与返回 schema 不变」。本段**要改签名** ⇒ 两 Spec 须协调: 建议由**本 Spec** 承担该签名变更 (前置 Spec 只改内部谓词), 并在前置 Spec 的非目标处加一句「`include_terminal` 形参由 `a1-entry-claim` 引入, 不属本 Spec 变更面」。**该协调项须 owner 确认。**
1. `phase1_gate.py` 新增 CLI flag `--include-terminal` (store_true);
2. **在 `_main()` 的现有调用处** (`phase1_gate.py:1232`) 加关键字参数 —— **不碰** `run_gate` / `_run_gate_impl` 签名;
   > R3/C2 实测: `linked_issue_overlaps` 生产代码**只有这一处调用**, 位于 `_main()`、在 `run_gate` 返回**之后**独立追加; `_run_gate_impl` (334-1075 行) 对它 grep 命中 **0**。原 R2-fix 写「`run_gate` 签名透传」**架构上就是错的** —— 照它做会改错函数, 精确复现它自己要修的「生产不可达」。
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

> ## ⛔ 阻塞性前提 (R1-fix/C1 — 4 席独立命中 + 主控实读)
>
> **两个指定落点的 `allowed-tools` 都不支持本机制的核心动作。** 实读 frontmatter:
>
> | Skill | `allowed-tools` (逐字) | 缺 |
> |---|---|---|
> | `phase-a-planner/SKILL.md:9` | `Read, Write, Glob, Grep, Task, Skill` | **无 `Bash`** · **无 `AskUserQuestion`** |
> | `spec-drafter/SKILL.md:10` | `Read, Write, Glob, Grep, AskUserQuestion` | **无 `Bash`** |
>
> ⇒ §2 的 `python3 .../phase1_gate.py` 命令**在两个宿主上都跑不了**; §2.3 的 `AskUserQuestion` 请裁**在 phase-a-planner 上也跑不了**。
>
> **这是整份 Spec 的阻塞项** —— 主机制在它自己指定的执行位置上不可调用, 而三轮审计 + 六条 spike 全都没查过 frontmatter。
>
> **处置 (须与 owner 确认, 二选一)**:
> - **(a) 扩 `allowed-tools`**: `phase-a-planner` 加 `Bash, AskUserQuestion`; `spec-drafter` 加 `Bash`。⚠️ 扩权是 skill 能力面变更, 会影响 Rule #6 的判据 (从「指令面」升到「能力面」), 且 `Bash` 是最宽的一项 —— **须 owner 明确批准**, 不由本 Spec 自行决定;
> - **(b) 改由已持 `Bash` 的宿主代调**: 例如经 `Task`/`Skill` 委派, 或把认领动作前移到 `state-scanner` 的阶段 4 (它已在 workflow-runner 链路上)。⚠️ 这会改变「A.1 起草前」这个时点的语义, 须重新论证。
>
> **两条 Impact 都未列 `allowed-tools` 字段变更** —— 无论选哪条都要补进 §Impact。**本前提未解决前, §2/§3 不具备实施条件。**
>
> **✅ owner 裁定 (2026-08-22): 采 (a) 扩权** —— phase-a-planner 加 `Bash, AskUserQuestion`; spec-drafter 加 `Bash`。理由: (b) 放弃 `/spec-drafter` 直调路径的覆盖, 而入口覆盖 (S6: 9 种身份 7 种无 claim) 正是本 Spec 核心目标; 扩权风险由 harness 权限系统兜底 (Bash 调用仍逐条过 permission 配置)。落版义务: Impact 表补两个 SKILL.md 的 `allowed-tools` 变更 + Rule #6 按能力面变更申报 benchmark。

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

## 决策记录

| # | 决策 | 依据 |
|---|------|------|
| D1 | 「关联 Issue」字段可得性提为 §1, 排在机制之前 | **S4**: 141 篇语料仅 13 篇有该字段 (9%) —— 主机制九成时候没有输入 |
| D2 | 字段格式固定 `<org>/<repo>#<n>` + custom check (warning) | 模板只影响新建且可被删; 无机械回声的义务会退化 (§Why 自证) |
| D3 | track-id = `<basename>-<str(int(n))>-<container_uuid>` | **S3**: 不含容器段则两轨同 id ⇒ 被 `:219-220` 互斥 ⇒ 主机制死 (R2/C1); uuid 不截断不用 label (label 碰撞域不可控且模板鼓励设置) |
| D4 | heartbeat 匹配键改 `(container, track_id)`, 刷新全部匹配 | **S1**: `release_claim_by_track` 为**同一 defect** 做过同款修法, 照抄即可; session 落盘方案被它取代 |
| D5 | `include_terminal` 在 **`_main()` 现有调用处**加参数, 不碰 `run_gate` 签名 | **R3/C2** 实测: `linked_issue_overlaps` 只在 `:1232` 被调用, `_run_gate_impl` 零命中 |
| D6 | 「接手」= **两步人工**, 不引入跨容器 release | **S3** 实测无该函数; 既有 takeover 路径对本场景不可达; 写别人的 claim 是权限面变更 |
| D7 | 探针自带 fetch, **不称轻量**, 配 30s 预算 + 重试 | **S2** 实测 ~13.8s/轮; 复用缓存判否 (缓存只由 scan.py 刷新) |
| D8 | A.1 双落点 (phase-a-planner + spec-drafter) | **S6** 实测入口覆盖率是杠杆 (9 身份 vs 2 在 ref); `spec-drafter` `user-invocable: true` 可绕过 |
| D9 | 不建 basename 别名表 | **S4**: 在真实输入总体上别名实例 = 0; 分隔符型别名已由前置 Spec 的 S5 追加覆盖 |
| D10 | 不做中心化登记表 | **S6**: 解决不了「没走进入口」这个共同根因 |
| D11 | 探针不阻断, 命中 exit 0; 非 0 仅用于探针自身失败 | 与主机制同为 advisory |

**Rule #6 (rule6_note)**: `phase-a-planner` / `spec-drafter` / `audit-engine` 三处 SKILL.md 的改动均为**处方性 · 运行时指令面**。但 R1/QA **双套件实测**证明现有 AB (`phase-a-planner` 5 eval / `audit-engine` 2 eval) **结构性覆盖不到**本 Spec 的新行为 ⇒ 落判据表**第三行「套件覆盖外」**, 三条缺一不可:
1. **点名行为**: (a) A.1 起草前必调 phase1_gate 且传 `--linked-issue`; (b) overlap 非空时经 `AskUserQuestion` 请裁而非自行放行; (c) fetch 降级时按「未能核实」而非「无碰撞」;
2. **建可证伪定向 fixture**: 上述三条各一个 eval, 双臂须能分辨;
3. **套件缺口开 issue**: 与 `aria-plugin#117` (缺 authoring 维度) / `#127` (缺 D9 surface 维度) 同族, 归并或新开由 A.2 定。

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
| `skills/state-scanner/scripts/phase1_gate.py` | CLI flag `--include-terminal`; **在 `_main():1232` 加关键字参数**; `error` 契约携带 `fetch_degraded` | **R3/C2** |
| `skills/state-scanner/tests/` (既有宿主) | SC-1~10, 14, 15 | R1/C4 |
| `skills/phase-a-planner/SKILL.md` | A.1 **独立标题级**认领步骤 + overlap 消费 + release 义务 + `coordination.enabled` skip | R3/M6 |
| `skills/spec-drafter/SKILL.md` | 第二落点 + proposal 模板增「关联 Issue」字段 | **S6** + **S4** |
| `skills/audit-engine/SKILL.md` + `references/execution-modes.md` | per-round 探针; **Convergence 与 Challenge 两段都改** | R3/M5 |
| `skills/audit-engine/scripts/sibling_spec_probe.py` + `tests/` | **新增** (目录也新建) | — |
| `skills/state-scanner/references/layer-l-integration.md` | 该活文档明确断言「闸门仅在 Phase B 触发」, 本 Spec 后即过时 | R1/M8 |
| `skills/config-loader/SKILL.md` | coordination 在 A.1 的 skip 语义登记 | R1/M3 |
| `.aria/state-checks.yaml` | 新增「关联 Issue」字段校验 check | **S4** |
| AB 套件 | 定向 fixture ×3 + 缺口 issue | rule6_note |

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
| **本次重写** | 据 spike 结论重写 (非打补丁) |

报告: `.aria/audit-reports/post_spec-R{1,2,3}-*-a1-entry-claim-*` · spike: `.aria/spikes/2026-08-02-*` · 原版全文见 git 史 (`b7c4933` 之前)

---

## ⚠️ 闸门待裁 (Rule #10 — AI 不自行判定)

`audit.checkpoints.post_spec = "convergence"` **enabled**, 封闭豁免白名单四类无一适用 ⇒ **默认应跑 post_spec**。

**本版与前三轮的关键不同, 供 owner 参考**:
1. 三处曾反复出错的承重逻辑 (heartbeat / track-id / `include_terminal` 接线) **现在都有实测支撑**, 不再是「Phase A.2 定」的占位符;
2. 原版 **7 处「A.2 待办」已清零** —— 每一条要么有 spike 结论, 要么被明确判为非目标;
3. **S4/S5 推翻了两条上游审计结论** ⇒ 继续打补丁会把那两条错误原样吸收。这是重写而非修订的直接理由;
4. 但**重写本身是新表面** —— 尤其 **§1 (字段可得性) 是全新章节**, 以及 §2.1/§2.2 的具体条款措辞, **从未经任何席位审过**。

**AI 不预判裁决。** 本 Spec 在裁决前不进 A.2/A.3。
