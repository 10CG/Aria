# Proposal: linked-issue-normalization

> **Status**: 📝 **Draft (A.1)** — 待 post_spec 闸门
> **Created**: 2026-08-02
> **Spec Level**: 2 (单域 — `lib/collision.py` 的一个比较谓词; blast radius 限 `linked_issue_overlaps` 的匹配行为)
> **关联 Issue**: 无 (由 `a1-entry-claim-duplicate-work-guard` 的 post_spec R1 发现; 该母 Spec 的 spike S1–S6 **已全部完成**并据此**全量重写为 v2**, 现因两个阻塞性未决项停在 Draft v2 —— 见其 `proposal.md:3` 的 Status 与 `:8` 的前置依赖声明)
> **代码落点**: `aria/` 子模块 `skills/state-scanner/lib/collision.py`; Spec 落主仓 (Rule #5)
> **ship target**: aria-plugin v1.66.0 (MINOR — 修复既有机制的匹配语义, 行为面扩大)

> **📌 本 Spec 的来历 (owner 2026-08-02 裁定 A+B)**: 母 Spec `a1-entry-claim-duplicate-work-guard` 经 **post_spec R1 (5 席) → R2 (新眼睛) → R3 (第三双新眼睛)** 三轮, 同口径 major **4→6 上升**, 判定**不收敛**。owner 裁定拆分: **本 Spec = 从母 Spec 抽出的、唯一被三轮审计反复确认「可直接实现」的一块**, 独立交付; 母 Spec 其余部分转 spike-first —— **S1–S6 六条 spike 已全部完成**, 母 Spec 据此全量重写为 v2, 现停在 Draft v2 待 owner 裁两个阻塞项 (见 `../a1-entry-claim-duplicate-work-guard/proposal.md`)。
>
> **它为什么能独立成立**: 见 §Why —— 该缺陷**不依赖任何未落地的机制**; 它是一个**已装填但尚未击发**的静默失效 —— 一旦两轨用不同格式认领同一 issue 即漏报, 且漏报不可观测 (与「真没人在做」返回同一个 `[]`)。

---

## Why

### 缺陷 (R1 四席独立命中 + 主控实跑复验)

`aria/skills/state-scanner/lib/collision.py:217` 的 `linked_issue` 匹配是**裸字符串 `!=`**:

```python
if c.linked_issue != own_linked_issue:
    continue
```

而生产数据里**三个格式族并存**:

> 🚧 **TODO(U-5, U-6) — 本表待 owner 裁决后整体替换为六族表 (R1-fix FIX-02, 未落)**。
> 待裁两项: (a) **U-5** 分族规则按语义 (F=2/D=4) 还是按结构 (F=5/D=1) —— `Forgejo [#137]` 与 `aria-plugin [#95]` **结构同形**, 解析器区分不了; (b) **U-6** 「141 篇中 12 个字段值」的 12 是**字段行数**, 其中 1 行是本 Spec 自己的「无」⇒ 真正带值的是 **11**。
> 裁决后须一并落地: 六族表 (新增 **D 族**无 repo 段 / **F 族**裸仓名+空格 / **E 族**markdown 链接外壳, E 与前五族正交) + **三总体定义** (已落盘 / 复制源 / 未来输入, 全文唯一定义处)。
> **下表的族划分与计数均为 R1 之前的旧值, 已知不准, 勿引用。**

| 族 | 形态 | 来源 | 实测 (⚠️ 旧值待替换) |
|---|---|---|---|
| A | `aria-plugin#122` | CLI 直传 (裸形) | ref 中 **4** 条 |
| B | `10CG/aria-plugin#110` | CLI 直传 (org 限定); `phase1_gate` help 示例即此形 | ref 中 **9** 条 (R1-fix 复核实为 **11**) |
| C | `10CG/aria-plugin #122` | **proposal 头部「关联 Issue」字段的书写格式** —— AI 逐字照抄即得 | ref 中 0, 但**它是最自然的复制源** |

⇒ **一旦**轨 A 认领 B 族、轨 B 认领 A 族, `linked_issue_overlap` **即恒 `[]`** ⇒ 与「真没人在做」**不可区分**。*(条件句 —— 该条件至今未在生产中成真, 见下节实测; 不得读作「现在正在漏」。)*

### 为什么这是 live 缺陷, 不是未来的事

**`linked_issue_overlaps` 已经在生产中被调用** —— `scripts/phase1_gate.py:1232`, 由 Phase B 入口的认领路径经 CLI 触达 (`phase-b-developer/SKILL.md:88-93` 的 `[--linked-issue]`)。⇒ **该机制今天就在跑, 谓词一旦遇到跨格式输入就漏报。**

> **⚠️ 但「今天已经在漏」当前无实例 (R1/M6, R1-fix 实跑复核)**: 对 `refs/aria/coordination` 全枚举 (16 个带 `linked_issue` 的 claim) 实测 —— 裸形族的号集合 `{116, 118, 122, 124}` 与 org 限定族同仓的号集合 `{110, 113, 121, 125}` **交集为空** ⇒ **从未发生过跨格式同号认领**。有多条同号 claim 的共 **2** 个 issue: `10CG/aria-plugin#110` (4 条, track_id 均 `state-scanner-stale-refs-false-parity`, 被 `collision.py:219-220` 自排除挡掉) 与 `10CG/aria-plugin#113` (2 条, track_id 均 `aria-plugin-113-gate-result-yaml-20260719`, 且均 `done` ⇒ 先被 `:210` 的 `_TERMINAL` skip)。**两组都与格式无关。**
>
> ⇒ **本 Spec ship 后, 把现有 16 条逐条回放为查询方, 输出零 delta** (以生产 `linked_issue_overlaps` + 归一实现双跑逐行比对, delta 行数 = 0)。**修的是击发概率不是存量症状。**

> **⚠️ 措辞同批约束**: 凡本文出现「今天就在漏 / 对真实数据恒假 / 正在生产中失效」一类措辞的落点, **一律同批订正**。已知落点 = §本 Spec 的来历 (已订正) + §它是「已 ship ≠ 能用」的实例 (已订正) + §缺陷 的「恒 `[]`」结论句 (已加条件句限定)。**新增此类措辞时须同批加限定, 否则与本节实测直接矛盾。**

这与母 Spec 的其余部分不同: 那些依赖尚未落地的 A.1 接线; **本条不依赖任何新机制**。

### 它是「已 ship ≠ 能用」的实例

`linked_issue_overlaps` 代码存在、有测试、被调用过、返回值合法 —— **只是它的匹配谓词在跨格式输入上恒假**, 而恒假的返回值 (`[]`) 与「真没人在做」完全相同 ⇒ 击发时不可察觉。这是 memory `feedback_completion_signals_vs_runtime_invocation` 最有迷惑性的一种形态: 所有表面信号都是绿的。

---

## What Changes

### 归一规则 (钉到字符级)

比较键 = `(normalize(repo_basename), int(number))`, 其中 `normalize` = 规则 1 的**每段 strip** + 规则 3 的 **`./_ → -` 译码** + **`casefold()`** 三者复合:

> **⚠️ 该键 ≠ R2 穷举验证过的那一版**。R2 验的是 `(repo_basename.casefold(), number)` —— **不含** strip、**不含**译码。⇒ **§审计资产继承 (a) 的免审范围只覆盖 R2 那一版键**; 本 Spec 现用键的三个分量里有两个是本轮新增, 全部在审计范围内。**读本节时不得把两者当成同一个键。**

1. 按**最后一个** `#` 拆为 `left` / `number_str`;
   - **空白处置的唯一规则 (R1/m1)**: 切分出的**每一段** (`left` / `number_str` / `org` / `repo_basename`) 在使用前**各自 `str.strip()`。无例外。** 后果: `10CG / aria-plugin#1` ≡ `10CG/aria-plugin#1`, `aria-plugin# 122` ≡ `aria-plugin#122`, `aria-plugin #95` ≡ `aria-plugin#95`。
   - **边界**: strip 只消除**每段首尾**空白; **段内空白既不删除也不译码** (`aria plugin` ≠ `aria-plugin`, SC-5c 钉死)。
   - **授权来源**: 本规则属规则 3 ⭐ 子项边界条款授权清单第 **(ii)** 条 —— 它是本轮**唯一一条主动扩大匹配面**的改动, 故必须有显式授权来源。
2. `number_str` (已 strip) **可解析当且仅当** `number_str.isascii() and number_str.isdigit()` 为真 —— 即**非空、全为 ASCII `0`-`9`**; 否则该值**不可解析** (见 4)。解析为 **`int`** 后按十进制值比较 (故 `aria-plugin#007` ≡ `aria-plugin#7`)。**前导零不剥、不截断**。
   - **为什么必须钉到这个谓词 (R1/M3: 母 Spec 写「纯数字」, 抽出时漂成更宽的「能解析为非负整数」)**: `int()` 与 `isdigit()` 双向分叉, 逐值实跑 (CPython 3.11.2) —— `int('+7')==7` / `int('1_0')==10` / `int(' 122')==122` 而三者 `isdigit()` 全 False; 反向 `'１２３'.isdigit()` 与 `'²'.isdigit()` 为 True 而 `int('²')` **抛 ValueError**。⇒ 必须同时钉住 `isascii()` 与 `isdigit()`。
   - **⚠️ 长度上界**: `number_str` strip 后长度 **> `sys.get_int_max_str_digits()` (CPython 默认 4300) 时判不可解析**, 退回步骤 4 原串比较。**且实现不得依赖 `int()` 不抛异常** —— `int()` 调用必须包在 `try/except ValueError → 判不可解析` 里。实测: `('9'*4301).isascii() and .isdigit()` 为 **True**, 而 `int('9'*4301)` 抛 `ValueError: Exceeds the limit (4300 digits)`; 该异常在生产路径上会被 `scripts/phase1_gate.py:1235` 的 `except Exception` 吞成 `out["linked_issue_overlap"] = []` (静默漏报, **与本 Spec 要治的病同形**)。
3. 若 `left` (已 strip) 含 `/`, 取**最后一段**为 `repo_basename` (再 strip), 其前为 `org`; 否则 `repo_basename = left`, `org = None`。`repo_basename` 空 ⇒ 不可解析;
   - **⭐ `repo_basename` 内的 `.` 与 `_` 一律译为 `-` (spike S5 追加)**: `10cg.local` ≡ `10cg-local` ≡ `10cg_local`。
     > **本 Spec 范围内成立的理由 (R1/M2 判定原两条理由落空后重写)**: 该译码是一条**封闭、可照写、无需语料决策**的规则 —— 三个字符固定映射到一个字符, 实现者零裁量。它与「别名表」的区别正在于此: 别名表要求持续维护一份仓名清单 (S4 已判不划算, 属母 Spec), 译码不要求。
     > **它顺带修好的真实子集**: `10CG/10cg.local` 是**真实仓** (Forgejo API 实测 11 个 open issue, 本项目 handoff 引用过 `10cg.local #20`)。post_spec R3 曾判此类「dormant, 本组织无含 `.`/`_` 的仓名」—— **R3 的仓名清单不完整**, S5 穷举时发现。
     > **误配代价对称于 D2**: 若 `a.b` 与 `a-b` 恰是两个不同真仓, 译码会误配 —— advisory 下误配 = 多一行告警, 由**回显的对方原串**人工判别 (同 D2 极性, **同 D2 的半幅限度**: 判别者须自行掌握本侧传入值; 母 Spec ship 前该限度不缓解, 见 §极性段)。
     >
     > **⚠️ 该判据的边界 (防止被引用来放宽别的东西)**: 「封闭规则」不等于「可放宽」。**本 Spec 授权的重写穷尽为三条, 其余一律不授权**:
     >   (i) `casefold()` —— repo 名大小写不敏感, 折叠不损失**区分性**信息;
     >   (ii) 每段 `str.strip()` —— 首尾空白**不是合法 repo 名字符**, 删除它不损失区分性信息;
     >   (iii) `repo_basename` 内 `.` `_` → `-` —— 同一分隔位的三种写法, **不跨越分隔位、不改变段数**。
     >   判别性准则 = **重写后仍能区分任意两个真实存在的仓名**。反例:「忽略全部非字母数字」把 `a-b` 与 `ab` 合并 ⇒ 跨越分隔位、改变段数 ⇒ **不在授权范围内**;「把段内空格也译成 `-`」同理 (SC-5c 钉死)。
     >
     > **已撤回的两条原理由 (R1/M2 判定不成立, 留痕)**: (a)「与 `derive_track_id` 对齐」—— `derive_track_id` **不消费 `linked_issue`** (全仓 grep 零命中), 且 track-id 派生是本 Spec 的**显式非目标**; (b)「不是理论风险」的原举证取自 **handoff prose 总体**, 与 SC-5 降级所用总体不同 —— 那正是 S4 指控 R2 的同一错误。**结论 (加译码) 保留, 理由已换。**
4. **不可解析的值** ⇒ **不参与归一, 退回原字符串精确比较** —— 绝不因解析失败就判「不匹配」而静默放行。**不可解析枚举 (母 §0 抽出时丢失, R1/m10 补回)**: (i) 无 `#`; (ii) `number_str` 不满足规则 2 的谓词; (iii) `repo_basename` 为空;
5. 匹配当且仅当 `repo_basename.casefold()` (经规则 3 译码后) 相等 **且** `number` 相等。**`org` 不参与匹配**。

> **⛔ 禁令 (母 §0 抽出时丢失, R1/m10 补回)**: 匹配**不得**使用模糊匹配 / 编辑距离 / 前缀包含 / 子串包含。比较只在上述归一键上做**精确相等**, 或在不可解析路径上做**原串精确相等**。二者之外无第三条路径。

> **⚠️ 举例约束 (R1/C1 防复发)**: R1 的 C1 根因是 SC-4 用了裸 `#007` × `#7` —— 按规则 3「`repo_basename` 空 ⇒ 不可解析」, 该例走的是步骤 4 原串比较, `'#007' != '#7'` ⇒ **不命中**, 与 SC-4 期望的「命中」直接冲突。
> **故本 Spec 全文的举例按路径分轴, 不按正例/反例分**:
> - 凡期望**经归一命中**的正例, **必须带 repo 段** (`aria-plugin#007` 而非 `#007`);
> - 凡期望**经步骤 4 原串精确比较命中**的正例, **必须**使用逐字相同的不可解析串 (如 `#5` × `#5`) —— 这类正例**不带 repo 段是规则 4 的直接推论, 不构成矛盾**;
> - 反例 (期望不命中) 不受 repo 段约束。

### 极性: org 轴 fail-toward-reporting, basename 轴是已知限

**org 轴**: 本机制是 advisory。漏报 = 静默无用 (昂贵, 已致 5 次重复劳动); 误报 = 多一行告警 (便宜, 人一眼可辨) ⇒ **fail toward reporting**, org 不参与匹配。代价: `otherorg/aria-plugin#122` 与 `10CG/aria-plugin#122` 会误配 ⇒ 需**回显双方 `linked_issue` 原始串**让人一眼判别。

> **⚠️ 该缓解在本 Spec 交付窗内只成立一半 (R1/M1, 实读复核)**: 对方那一侧**已经有** —— `collision.py:228` 逐字回显 `c.linked_issue` 未归一原串, docstring `:204-205` 已列该键。**自己那一侧没有** —— `scripts/phase1_gate.py` 的 `_claim_to_dict` (`:1119-1131`) 与 `_gate_result_to_dict` (`:1134-1169`) **均无 `linked_issue` 字段**, 而补它要动 `phase1_gate.py`, 那是本 Spec 的**显式非目标**。
> ⇒ **成文已知限 (与 basename 截断轴同一处置形式 —— 成文落 D4 + 本段, 不写进任何 SC 的期望列; 理由同 SC-5 去循环定义)**: 本 Spec **不**补自己那一侧。D2 的代价在本 Spec 交付窗内**只缓解一半**: 看得见对方写的是什么, **看不见自己传的是什么** —— 对**转述该 JSON 的下游**尤其致盲。母 Spec §2.3 逐字要求「双方 `linked_issue` 原始串」、其 Impact 表已列 `phase1_gate.py`, 该半缺口由母 Spec 闭合。
> **凡引用「回显原串」作为代价缓解的落点, 一律带半幅限定 —— 已知落点: D2 要点列 (已带)、规则 3 的译码论据 (已带)。**

**basename 轴 (诚实标注, R2/M2)**: `repo_basename` 用**精确相等**, 对真实的**截断型**别名**恒漏** ⇒ **本机制在 basename 轴是 fail-toward-silence, 与 org 轴方向相反**。

> **⚠️ R2 的 24/10 未被推翻 —— 它是另一个口径 (R1-fix 复核订正, 主控实跑)**:
> - **R2 的口径** = issue **引用位置**, 范围含 `docs/`。2026-08-04 逐字复跑 `grep -rhoE '\baria-orch[a-z]* ?#[0-9]+' openspec/ docs/ | sed -E 's/ ?#[0-9]+//' | sort | uniq -c` → **25 `aria-orch` / 11 `aria-orchestrator`**, 与 R2 报的 24/10 一致 (数据长了 1)。拆开看 **`docs/` 独占 24/8**, `openspec/` 只有 1/3。
> - **spike S4 的口径** = **全文裸 token**, 范围只有 `openspec/`。**逐字复跑 (2026-08-04, HEAD `65f17de`)**: 文件集 `openspec/*/*/*.md` = **250 文件**; `grep -oh 'aria-orchestrator' openspec/*/*/*.md | wc -l` → **735**; `grep -ohP 'aria-orch(?!estrator)' openspec/*/*/*.md | wc -l` → **16**。
>   **⚠️ 文件集与计数法都必须照抄** (U-1 裁定钉 250 口径, 即 `changes/<name>/` + `archive/<name>/` 两级): 换成 `find openspec -name '*.md'` (276 文件) 得 **744**; 用 `grep -c` (数行不数次) 得另一个数。**数字只承载定性 (「截断写法在正式文档里是少数」), 不承载阈值。**
>   *(订正留痕: 本条原写 `16 / 799` —— `799` 在上述三种口径下均复现不出, 无出处, 已按实跑值改。编辑清单 FIX-08 报的 736/745 是 `ca4db78` 之前的树, 各差 1。)*
> - ⇒ **两组口径不同、范围也不同, 不可比, 谁也没推翻谁。** S4 报告里「比例是反的 / R2 量错了总体」**本身就是一次跨总体比较** —— 与它指控 R2 的错误**同形**。该措辞已作废, S4 报告须同批订正。
> - **真正让本轴降为「已知限」的是 S4 的另一半结论**: 在**真实输入总体** (会被传给 `--linked-issue` 的「关联 Issue」字段值) 上截断型别名 **= 0 实例**; R1-fix 补测**已落盘总体** (coordination ref 的 16 个值) 同样 **0 实例** (basename 只有 `aria-plugin` / `Aria` / `AUDIT-TEST-DO-NOT-USE`)。**两个总体各自为 0, 不是跨总体推断。本 Spec 不以「比例反了」为依据。**
> - **R2 的口径其实更贴近 `--linked-issue` 的真实取值** (它量的是 issue 引用形态), 这也是为什么不能把它当作被推翻。

**本 Spec 不解决 basename 截断型别名** (那需要别名表或书写强制, 属母 Spec 范围)。此处**只做三件事**: (a) **SC-5** 用纯行为断言把该轴的行为钉死 (`10CG/aria-orch#5` × `10CG/aria-orchestrator#5` **不命中**); (b) 该行为**作为已知限成文于 D4 与本段**, 防它被误读成「已覆盖」; (c) **不新增任何 surface 文案** —— 现有 `collision.py` docstring 的同步措辞 (见 Impact 表) **不得**出现「已穷尽核实 / 已覆盖全部别名」一类暗示。*(`SKILL.md:176` 是否一并同步, 待 U-2 裁决, 见 rule6_note 的 TODO。)*

### 存量数据不迁移

归一发生在**比较时**, **16** 条已有记录原样有效 (计数与 §Why 的已落盘总体一致)。改写共享 ref 是外向且难撤销动作, **非本 Spec 范围**。

### 接口面

`linked_issue_overlaps` 的签名与返回 schema **不变**; 只改内部比较谓词。⇒ Phase B 现有调用方**零改动**。

> **行为变化清单 (R1/M5: 「仅为原漏报现能报」不完整)**:
> 1. 跨格式同号的 claim 从不可见变为可见 (本 Spec 的目的);
> 2. **`yielded` 状态的 claim 会一并被归一后的谓词命中** —— `collision.py:210` 的 `_TERMINAL = ("done","abandoned","unknown")` **不含 `yielded`**。ref 现有 **3 条 `yielded` 且带 `linked_issue`** (均 `10CG/aria-plugin#110`, claimed_at `2026-07-14T11:26:09Z` / `12:32:51Z` / `17:10:32Z`, track_id 均 `state-scanner-stale-refs-false-parity`) 因此是**新的可命中目标**;
> 3. `int()` 与解析失败路径新增的异常面 (规则 2 长度上界), 会被 `scripts/phase1_gate.py:1235` 的 `except Exception` fail-soft 吞掉 —— **这条兜底本身就是静默漏报**, 已按规则 2 要求实现侧不得依赖它。
>
> **⚠️ 第 2 条不与 §Why 的「零 delta」冲突, 二者说的是不同东西**: 把现有 16 条逐条回放为**查询方**, 新旧输出 delta = **0** (那 3 条 `yielded` 与查询方共享 track_id, 被 `:219-220` 自排除); 但若**未来**有人以裸格式 `aria-plugin#110` 从**另一个 track_id** 认领, 新谓词会一次性浮出这 3 条 `yielded` (实测 old `[]` → new 3 条)。⇒ **「零 delta」限定于存量回放, 「yielded 变可达」限定于未来输入。两句都必须带这个限定词。**
>
> **⚠️ terminal 集合在本仓有三个互不相同的定义 (R1-fix 实读新发现, 编辑清单未列)**: `collision.py:210` = `("done","abandoned","unknown")` / `collision.py:307` = `("done","abandoned")` / `claim_lifecycle.py:317`+`:408` = `{"done","yielded","abandoned"}`。三者两两不同 —— `unknown` 只在第一个里, `yielded` 只在第三个里。**属既有分歧, 非本 Spec 引入**; 本 Spec 只披露不改 (改它会动 `include_terminal` 语义, 已列非目标)。**建议单开 issue** (编辑清单 `post_spec-R1-fix-editlist-linked-issue-normalization.md` §本轮 deferred D-1 已记, 但当时只知两个变体)。

---

## 决策记录

| # | 决策 | 要点 |
|---|------|------|
| D1 | 比较键 = `(normalize(basename), int(number))` —— `normalize` = strip + `./_ → -` 译码 + `casefold()` (定义见 §归一规则) | **等价关系已被验证但证据不可复核**: R2 曾用 18 元语料穷举自反/对称/传递零违例, **该语料未入库、现已不存在**; R1/BA 在加入 `./_ → -` 译码后**用本 Spec 文本内的字面值重新穷举**, 同样零违例 —— 那是 R1 的实测, **不是可继承的 R2 资产** (R2 验的键是 `(repo_basename.casefold(), int(number))` —— **不含**译码、**不含** strip, 与 §审计资产继承 (a) 逐字同一写法)。⇒ **Phase B 必须建 committed fixture** (`tests/fixtures/linked_issue_corpus.txt`, 口径见 SC-7) 取代上述两次口头引用; fixture 入库前, D1 的等价关系主张按「**已论证、未留证**」计 |
| D2 | `org` 不参与匹配 | advisory 下漏报昂贵、误报便宜 ⇒ fail-toward-reporting; 代价由「回显**对方**原串」兜 —— **仅半幅** (自己那一侧不在 CLI 输出中, 见 §极性段成文已知限 + SC-9), 对转述该 JSON 的下游不成立 |
| D3 | 不可解析值退回**原串精确比较** | R2 复核: 两类不可能跨类相等, **论域被干净划分, 不破坏传递性** (此结论撤销了母 Spec R1-fix 自己的担忧) |
| D4 | basename 轴的 fail-toward-silence **成文为已知限**, 不在本 Spec 解决 | 依据 = S4 实测**复制源总体** 0 实例 + R1-fix 实测**已落盘总体** 0 实例 (两个总体各自为 0, **非跨总体推断**); 别名表 / 书写强制均需语料决策 ⇒ 属 spike 范围 (母 Spec)。**「回显原串」半幅限度同挂本条, 见 §极性段** |
| D5 | 存量 ref 不迁移 | 归一在比较时发生; 改写共享 ref 外向难撤销 |
| D6 | 签名与 schema 不变 | Phase B 现有调用方零改动 |

**Rule #6 (rule6_note)**: 改动面为 `lib/collision.py` 的一个内部比较谓词 + 其测试 + `collision.py` docstring `:182-206` 的纯描述性同步, **零 `description` / 零 frontmatter / 零运行时指令流程变更** ⇒ 判据表**第一行「描述性 (schema / 字段 / 命令 / 勘正)」** ⇒ **substitute: SC 级 baseline-failing 结构化测试替代**。与 v1.65.2 (#124 纯脚本修复) 同一判据路径。**不申请豁免。**

> 🚧 **TODO(U-2) — 前提句待 owner 裁决后可能改写 (R1-fix FIX-11 + FIX-13, 未落)**。若裁**方案 A** (保留 `SKILL.md:176` 文案同步), 本条前提句须改为「按 CLAUDE.md『同文件两性质并存时逐 hunk 判』**逐 hunk 判定**: `SKILL.md:176` 的 hunk 仅追加事实勘正括注, 不改任何指令 / 触发条件 / 判断流程 ⇒ 仍落第一行」, 且 Impact 表须同批补 `SKILL.md:176` 行 —— **FIX-11 与 FIX-13 不得只落其一**。若裁**方案 B** (撤下 SKILL.md 同步), 当前措辞即为终稿。**AI 建议 A, 但不自行拍板 (Rule #10)。**

**baseline 实测结果 (R1 三席 + R1-fix 起草者 + R1-fix 综合者三方独立复跑, 逐格一致)**:

| SC | baseline | 性质 | 算进 substitute 证据面? | 取证方式 |
|----|---------|------|---|---|
| SC-1 | **红** | 主判据 (跨族归一) | ✅ | 实跑生产 `linked_issue_overlaps` |
| SC-2 | 绿 | 负控 (不同仓不得命中) | ❌ | 实跑生产 `linked_issue_overlaps` |
| SC-3 | **红** | 主判据 (org 不参与) | ✅ | 实跑生产 `linked_issue_overlaps` |
| SC-4 | **红** | 主判据 (int 比较 + 段首尾空白 strip) | ✅ | 实跑生产 `linked_issue_overlaps` |
| SC-5 | 绿 | 已知限 (截断型不归一) | ❌ | 实跑生产 `linked_issue_overlaps` |
| SC-5b | **红** | 主判据 (`./_ → -` 译码) | ✅ | 实跑生产 `linked_issue_overlaps` |
| SC-5c | 绿 | 负控 (段内空格不译码) | ❌ | 实跑生产 `linked_issue_overlaps` |
| SC-6 | 绿 | 回落语义 (原串比较) | ❌ | 实跑生产 `linked_issue_overlaps` |
| SC-6b | 绿 | 边界负控 | ❌ | 实跑生产 `linked_issue_overlaps` |
| SC-7 | 绿 | **结构上不可红** (任何「算 key 再比较」的实现自动满足三性质) | ❌ | **结构推理, 未跑** |
| SC-8a | 绿 | 签名冻结 | ❌ | `inspect.signature` 内省, **未调用本函数** |
| SC-8b | 绿 | 返回 key-set 冻结 | ❌ | key-set 内省, **未调用本函数** |
| SC-8c | 绿 | 既有测试回归 | ❌ | 跑既有测试 |
| SC-9 | 绿 | 回显未归一原串 (现状即如此) | ❌ | 实跑生产 `linked_issue_overlaps` |

⇒ **substitute 的证据面 = SC-1 / SC-3 / SC-4 / SC-5b 四条 baseline-failing**; 其余为负控 / 已知限 / 回落语义 / 冻结断言 —— 它们锁住「修复后不应退化」的行为, 有价值但**不能算进 substitute 的证据面** (负控恒绿是正确的, 不是证据)。
**⚠️ 原文的「SC-1~6 均在现状代码上可红」经三方实测不成立, 已按实测改写。** 表内不设「直接调用生产函数实跑」的全称句 —— SC-7 / SC-8a / SC-8b 结构上不可能由调用该函数测得, 保留全称句就是在引用「须实证而非声称」之后紧接着声称一个未实测范围。

> **框定合规 (owner 2026-08-02 裁定 `db2e983`)**: 本条走 **substitute 框定** —— 判据表某一行 + 对应处置, **不**声称「Rule #6 不适用 / Rule #10 白名单第四类」。owner 该次裁定确立: **提供 substitute 与声称「不适用」逻辑上二选一**, 前者才对 (先例 `openspec/archive/2026-06-19-secret-guard-exfil-coverage-iteration/`)。**substitute 须实证而非声称** —— **SC-1 / SC-3 / SC-4 / SC-5b 四条**的 baseline-failing 状态在 Phase B 须实跑留证 (同该裁定要求的「全部实跑, 非声称」)。

> *(订正留痕: 本段原写「SC-1~6 的 baseline-failing 状态」—— 与上方 baseline 实测表直接矛盾 (SC-2/5/6 实测为绿)。**该假声明在同一节内出现两次, 上方一处已由 FIX-11 改掉, 这一处编辑清单未点名、险些残留** —— 属「多簇 fix 互相拆台」的同一形状, 由 R1-fix 落盘后的交叉一致性检查抓到。)*

---

## Success Criteria

| SC | 场景 | 期望 | 怎么会红 |
|----|------|------|---------|
| **SC-1** | 四族两两配对 (6 对): `aria-plugin#122` × `10CG/aria-plugin#122` × `10CG/aria-plugin #122` × `aria-plugin #122` (**第四元 = 裸仓名 + 空格, 无 org**) | **两两互相命中** | 现状裸 `!=` 在**全部 6 对**上必红 |
| **SC-2** | `10CG/Aria#147` × `10CG/aria-plugin#147` (同 org 同号, **不同仓**) | **不得**命中 | 「只比 number」的退化实现必红 |
| **SC-3** | `10CG/aria-plugin#1` × `otherorg/aria-plugin#1` (**两侧都有 org 且不同**) | **命中** (org 不参与) | **唯一能区分「org 不参与」与「两侧有 org 才比 org」两种实现的用例** (R2/M1: SC-1/SC-2 都无法区分) |
| **SC-4** | (a) `aria-plugin#007` × `aria-plugin#7`; (b) `aria-plugin# 122` × `aria-plugin#122` | **两组各自命中** (number 按十进制值比较; **前导零与各段首尾空白不影响**; 段内空白不归一, 见 SC-5c) | 字符串比较必红; 不 strip `number_str` 的实现在 (b) 上必红 |
| **SC-5** | `10CG/aria-orch#5` × `10CG/aria-orchestrator#5` (**截断型**别名) | **不命中** | 锁定 basename 轴 fail-toward-silence。*(该结果作为已知限成文于 D4 + §极性段, **不写进本列** —— 「期望列写『被记为已知限』」是循环定义, R1/minor 已判)* |
| **SC-5b** ⭐ (spike S5) | `10CG/10cg.local#20` × `10CG/10cg-local#20` × `10CG/10cg_local#20` (**分隔符型**别名, 真实仓) | **两两命中** | 只做 casefold 的实现必红。**与 SC-5 是两类**: 分隔符型**能**归一, 截断型不能 —— 两者处置不同, SC 须分开钉 |
| **SC-5c** ⭐ | `10CG/aria plugin#1` × `10CG/aria-plugin#1` (**段内空格**) | **不命中** | 把段内空格也译成 `-` 的**过宽**实现必红 (钉住规则 3 边界清单只授权三条重写) |
| **SC-6** | 不可解析值的**显式配对**: (a) `#5` × `#5` ⇒ **命中**; (b) `#5` × `#7` ⇒ 不命中; (c) `10CG/#7` × `otherorg/#7` ⇒ **不命中** (原串不同, 尽管归一后会同键 —— **D3 论域划分的承重断言**); (d) `no-hash-here` × `no-hash-here` ⇒ **命中**; (e) `repo#abc` × `repo#abc` ⇒ **命中** | 全部走步骤 4 **原串精确比较**; **不抛异常**; **不因解析失败判「不匹配」** | 解析失败即 `return False` 的实现在 (a)(d)(e) 三个自配对上必红 |
| **SC-6b** ⭐ | `number_str` 边界**配对**: `aria-plugin#+7` × `aria-plugin#7` / `aria-plugin#1_0` × `aria-plugin#10` / `aria-plugin#１２３` × `aria-plugin#123` / `aria-plugin#²` × `aria-plugin#2` 四对; 外加四个左值**各自与自身配对**; 外加 `aria-plugin#<4301 个 9>` 与自身配对 | 四对**均不命中**; 五个自配对**均命中** (原串相同, 走步骤 4); **全程不抛异常** | 裸 `int()` 的实现在前三对上命中 ⇒ 红; 裸 `isdigit()` 的实现在 `#²` 上 `int()` 抛 ValueError ⇒ 红; 「判定在前、`int()` 在后且不 catch」的实现在 4301 位自配对上抛 ValueError ⇒ 红; 「解析失败即判不匹配」的实现在五个自配对上不命中 ⇒ 红 |
| **SC-7** | 等价关系性质: 对 **committed fixture** `tests/fixtures/linked_issue_corpus.txt` 断言自反 / 对称 / 传递 | 三性质零违例 | 非等价关系的实现 (如单向前缀匹配) 必红。**本 fixture 同时是 D1 的证据载体** (D1 引的 18 元语料已不存在)。⚠️ **判别力自陈**: 任何「算 key 再比较」的实现都自动满足三性质 ⇒ 本条是**回归护栏, 不是主判据** |
| **SC-8a** | `inspect.signature(linked_issue_overlaps)` 逐字 == `(claims, own_track_id, own_linked_issue)`, 后两参**无默认值** | 逐字不变 | 改签名 / 加默认值的实现必红 |
| **SC-8b** | 返回条目 `sorted(keys())` 逐字 == `['claimed_at','container','linked_issue','owner','session','status','track_id']` | 逐字不变 | 增删键的实现必红 |
| **SC-8c** | 既有 **6** 条测试逐字不改全绿 + **新增 CLI 全链路 near-miss 负控** | 全绿 | 见下方 SC-8c 展开 |
| **SC-9** ⭐ | 命中条目的 `linked_issue` 值 | **回显未归一的原始串** (如 `10CG/aria-plugin #122` 原样, 不是归一后的 key) | 把归一结果写回该键的实现必红。*(现状即如此, `collision.py:228`; 本条是冻结断言, baseline 绿)* |

> 🚧 **TODO(U-3) — SC-7 的 fixture 内容口径尚未定义**。D1 说「口径见 SC-7」、SC-7 说「fixture 是 D1 的证据载体」—— **两处互指, 没人真的定义了 fixture 该装什么** (memory `feedback_verify_predicate_inputs_exist` 的形状: 判据打磨到位, 它要判的输入不存在)。
> **编辑清单的建议 (未采纳为定案, 待 owner/主控裁)**: 至少含各族各 2 例 + SC-5/5b/5c/6/6b 的全部字面值 + R2 那 18 元的可复原部分。**Phase B 开工前必须写死, 否则 SC-7 无法实现。**

**SC-8c 展开 (R1/M7 + 实读订正)**:

既有测试 **6** 条构成 `linked_issue_overlap` 的既有冻结面, 逐字不改必须全绿:

- **lib 层 4 条** (`tests/test_release_by_track.py`, `class TestLinkedIssueOverlaps` 位于 **`:206-247`**): `test_same_issue_different_track_flagged` (`:224`) / `test_same_track_not_flagged` (`:232`) / `test_terminal_and_no_issue_ignored` (`:236`) / `test_none_own_issue_short_circuits` (`:245`);
- **CLI 层 2 条** (`class TestPhase1GateLinkedIssueCli`, `:527-575`): `test_linked_issue_written_and_overlap_surfaced` (`:533`) —— **唯一端到端驱动本谓词**的既有测试 (subprocess 跑 `phase1_gate.py --linked-issue`, `:554-557` 断言 `out["linked_issue_overlap"]` 的长度与 `track_id`), 也是 §接口面第 3 条点名的 `phase1_gate.py:1235` fail-soft 吞异常路径的**唯一现成观测点**; `test_no_linked_issue_no_overlap_key` (`:563`) —— 它**不调用本谓词** (`phase1_gate.py:1229` 的 `if args.linked_issue:` 守卫短路), 锁的是「未传参 ⇒ 该键不出现」的 additive 契约。
  ⇒ **6 条中 5 条真正驱动本谓词, 第 6 条锁调用侧守卫。**
- **⚠️ 判别力自陈**: 这 6 条在「匹配」这一侧**全部使用逐字相同的字面串**, 在「不匹配」这一侧全部靠 status / None / track_id 分支 ⇒ **对新比较逻辑的 near-miss 判别力为零**。SC-8c 证明的是「没有破坏无关分支」, **不是**「新逻辑没有引入误配」—— 后者全压在 SC-1~SC-7 上。
- **故 SC-8c 必须新增 near-miss 负控, 且至少一组走 CLI 全链路** (仿 `test_linked_issue_written_and_overlap_surfaced` 的 subprocess 形式)。**怎么会红**: 归一只落在 `collision.py` 而 **CLI 那侧未接上**的实现在该组上必红 —— 母 Spec §2.4 逐字点名的失败模式:「**SC 的断言层必须是 CLI 全链路**, 不是直调库函数 —— 否则『参数没接到 CLI』的实现仍能绿」。

---

## 非目标

- **不改** `phase1_gate.py` 的 CLI / `run_gate` 签名 (本 Spec 只动 `collision.py` 内部谓词);
- **不做** A.1 入口认领前移 —— 那是母 Spec 的范围 (其 spike S1–S6 已完成、已据此重写为 v2, 现停在 Draft v2 待 owner 裁两个阻塞项);
- **不做** basename 别名归一 (D4 已成文为已知限);
- **不改写**存量 coordination ref 数据 (D5);
- **不动** `_TERMINAL` 的 skip 语义 (`include_terminal` 属母 Spec, 且 R3 已证其接线点描述有误);
- **不引入** track-id 形态变更 (母 Spec 范围, R3 判其有碰撞域风险)。

---

## Impact

| 文件 | 变更 |
|------|------|
| `skills/state-scanner/lib/collision.py` | 归一比较谓词 (§What Changes 五步); 签名与 schema 不变 |
| `skills/state-scanner/lib/collision.py` docstring `:182-206` | 文案同步 — 说明匹配按归一后的 `<repo>#<n>`, org 不参与; **措辞不得暗示「已穷尽核实 / 已覆盖全部别名」** |
| `skills/state-scanner/tests/test_release_by_track.py` (既有宿主) | 扩展 — SC-1~9; 既有 6 条 (`:206-247` 4 条 + `:527-575` 2 条) 逐字不改 |
| `skills/state-scanner/tests/fixtures/linked_issue_corpus.txt` (**新建**) | SC-7 语料全集 + D1 的证据载体 (**内容口径待 U-3 裁**) |
| 发版 5 文件 + 主仓 gitlink | v1.66.0 MINOR |

> 🚧 **TODO(U-2) — 若裁方案 A, 本表须补一行**: `skills/state-scanner/SKILL.md:176` 文案同步 (给「同一件事两个名字」补「(按归一后的 `<repo>#<n>` 比较, org 不参与)」, 纯事实勘正 hunk)。**该行与 rule6_note 的前提句必须同批落地并互相引用, 不得只落其一。**

测试基线: state-scanner 现 **1322** tests, 本 change 新增按 SC 子用例下界 **≥35**。全量跨 skill 套件须绿 (`run_all_tests.sh`)。

> **下界推导 (可证伪, 逐条从 SC 表数)**: SC-1 六对 **6** + SC-2 **1** + SC-3 **1** + SC-4 两组 **2** + SC-5 **1** + SC-5b 三元两两 **3** + SC-5c **1** + SC-6 五配对 **5** + SC-6b (四对 + 五自配对) **9** + SC-7 三性质 **3** + SC-8a **1** + SC-8b **1** + SC-8c 新增 near-miss **≥1** + SC-9 **1** = **≥35**。
> *(订正留痕: 原写 `≥12` —— 那是 8 条 SC 的旧表算出的, SC 表经 FIX-12 扩到 14 条后未同步。)*

---

## 审计资产继承

本 Spec 的内容**已经过三轮审计**, 作为母 Spec 的 §0 章节:

| 轮 | 席位 | 对本内容的结论 |
|---|---|---|
| R1 | 5 席 | **发现**该缺陷 (4 席独立命中) |
| R2 | type-design-analyzer | **穷举验证**比较键是良定义等价关系 (18 元语料, 零违例); **撤销**了「不可解析值破坏传递性」的担忧; 指出 org 轴与 basename 轴极性不同 (已吸收为 D4/SC-5); 指出 SC 无法区分两种 org 实现 (已吸收为 SC-3) |
| R3 | code-architect | 「§0 四步归一算法钉到字符级…**`collision.py` 改动核心逻辑可直接照写, 不需要实现者猜**」—— 是其评估中**唯一无缺口**的核心项 |

⇒ 本 Spec 的 post_spec 应聚焦**抽出过程本身**是否引入偏差 (措辞漂移 / SC 遗漏 / 与母 Spec 的边界)。**可不重审的只有两项**:

(a) **R2 用 18 元语料穷举验证过的那一版比较键** —— `(repo_basename.casefold(), int(number))`, **不含** S5 的 `./_ → -` 译码 / **不含**统一 strip / **不含** `isascii()+isdigit()` 谓词 —— 的自反 · 对称 · 传递三性质 (且该语料已不存在, 见 D1);
(b) 「**org 不参与匹配**」的极性判断。

**其余一律在审计范围内。本轮对比较键的三处修改 (S5 译码 / 统一 strip / `isascii()+isdigit()` 谓词) 全部在审计范围内。**

**⚠️ 本轮新增未审表面 (R3 之后新增, 零审计记录)**:

1. **规则 2 的 `isascii() and isdigit()` 谓词 + 4300 位长度上界 + 强制 `try/except ValueError`** — 全新, 承重的字符级判据, **且新增了一条异常路径**;
2. **「每段各自 `str.strip()`」的统一空白规则** — 全新, 且**改变了行为面** (本轮唯一主动扩大匹配面的改动);
3. **`./_ → -` 译码 (S5)** — R2 的穷举**不含**它;
4. **规则 3 的「封闭重写 vs 语料决策」判据 + 三条授权清单 + 判别性准则** — 全新, 是**通用授权形状**, 最可能被下一版引用来放宽别的东西;
5. **6 条新 SC** (SC-5c / SC-6b / SC-8a / SC-8b / SC-8c / SC-9) — 全新;
6. **rule6_note 的 baseline 实测表** — 全新, 且是 **Rule #6 合规论证**;
7. **§Why 的「已装填未击发」重述 + 零 delta 断言 + yielded 变可达的一对限定词** — 全新, 无任何镜头审过;
8. **三个 terminal 集合互不相同的披露** — R1-fix 实读新发现, 编辑清单未列。
   *(另: 六族表 / 三总体定义 / rule6_note 前提句 / SC-7 fixture 口径 尚未落地, 见各处 🚧 TODO。)*

**R3 的三条订正 (留痕)**: R3 原文是 6 项要点、**无「可实现性评估表」这一措辞**、`release-by-track` 同样无 caveat —— 上表 R3 行原写的「在其可实现性评估表中」是**合理复述非逐字引用**, 已改为不带该措辞的表述。

---

## ⚠️ 闸门待裁 (Rule #10 — AI 不自行判定)

`.aria/config.json` 的 `audit.checkpoints.post_spec = "convergence"` **enabled**, 封闭豁免白名单四类无一适用 (非 config off / 无 adaptive_rules 映射 / 无成文 lane / 结构性前提成立) ⇒ **默认应跑 post_spec**。

**但本 Spec 的情形特殊, 提请 owner 一并裁**: 其内容已经过 R1/R2/R3 三轮审计并被逐轮确认 (见上表)。可选处置:

(1) **照跑完整 post_spec**;
(2) **定向轮 —— 审计范围 = 抽出偏差 ∪ 上文「本轮新增未审表面」清单全部 8 项** (含规则 2 的 `isascii()+isdigit()` 谓词与长度上界、统一 strip 规则、S5 译码、规则 3 的封闭重写判据与授权清单、6 条新 SC、rule6_note 的 baseline 表、§Why 的一对限定词、三 terminal 集合披露)。**仅**「比较键的等价关系 (R2 验过的那一版)」与「org 不参与匹配的极性」两项可凭三轮资产免审 —— **「不重审算法本体」的旧措辞在本轮已失效, 撤回**;
(3) ~~判定审计资产可继承、免跑并留痕请复议~~ —— **已被 R1 自身证伪, 从选项中撤回** (R1 的 2 条 critical 都是「抽出/新增时引入」的, 不在被继承的三轮资产里)。

⇒ 处置 (3) 撤回; 处置 (2) 已按「本轮新增未审表面」清单重新定界 —— **旧措辞会豁免掉本轮全部零审计的承重条款, 触 Rule #10**。

**AI 不预判。** 本 Spec 在裁决前不进 A.2/A.3。

---

## ⚠️ R1-fix 落地状态 (2026-08-04, 供下一席位读)

R1 编辑清单 (`.aria/audit-reports/post_spec-R1-fix-editlist-linked-issue-normalization.md`) 共 **17 条 FIX + 6 项待裁 (U-1…U-6)**。

- **`ca4db78` 实际只落了 1 处** (§极性段的 R2 24/10 口径订正), **其余 16 条从未落地** —— 2026-08-04 本轮补落。
- **本轮已落 14 条**: FIX-01 / 03 / 04 / 05 / 06 / 07 / 08(补齐另一半) / 09 / 10 / 12 / 14 / 15 / 16 / 17。
- **仍未落 3 条, 均卡 owner 裁决**: **FIX-02** (六族表 + 三总体定义, 卡 U-5/U-6) · **FIX-11** (rule6_note 前提句, 卡 U-2) · **FIX-13** 的 `SKILL.md:176` 行 (卡 U-2, 须与 FIX-11 同批)。全部落点已就地打 🚧 TODO 标记。
- **本轮实跑订正的数字**: `aria-orchestrator` 全文裸 token 计数原写 `799`, 三种口径下均复现不出 ⇒ 按实跑改为 **735** (250 文件口径); 存量 ref 计数 `13` → **16**; 已落盘总体 B 族 `9` → **11**。
- **本轮新发现 (无审计记录)**: 本仓 terminal 集合有**三个互不相同**的定义 (见 §接口面)。

**⇒ 下一轮闸门审的是「本轮补落后」的文本, 不是 `ca4db78` 那一版。**
