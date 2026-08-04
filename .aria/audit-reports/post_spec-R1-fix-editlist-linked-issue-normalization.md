I have verified the disputed claims independently. Now the edit list.

## 编辑清单 — `linked-issue-normalization` (R1-fix 综合)

> **综合者实读/实跑范围**: `proposal.md` 全文 159 行 · `lib/collision.py:180-233` · `scripts/phase1_gate.py:1119-1240` · `tests/test_release_by_track.py:200-250, 525-579` · `SKILL.md:1-12, 173-178` · `lib/track_id.py:61-75` · `refs/aria/coordination` 全 30 blob · 12 个「关联 Issue」字段行逐值 · 生产 `linked_issue_overlaps` 直调实跑 · R2 报告 `:164-175`。
> **三镜头互相冲突 4 处**, 已逐条裁断 (见 §裁断)。**新增 2 条镜头都没抓到的问题** (FIX-09b、FIX-02 的 12/11 口径)。

---

### [FIX-01] M6 (cross-clause) — 「今天就在漏」的三处落点必须同批订正

**位置**: `:12` · `:37-41` · `:45` (三处同批, 只改一处即视为未闭合)

**原文 `:12`**: `> **它为什么能独立成立**: 见 §Why —— 该缺陷**不依赖任何未落地的机制**, 它现在就在生产中让一个**已 ship 的**机制静默失效。`

**改为 `:12`**:
```
> **它为什么能独立成立**: 见 §Why —— 该缺陷**不依赖任何未落地的机制**; 它是一个**已装填但尚未击发**的静默失效 —— 一旦两轨用不同格式认领同一 issue 即漏报, 且漏报不可观测 (与「真没人在做」返回同一个 `[]`)。
```

**原文 `:45`**: `…**只是它的匹配谓词对真实数据恒假**。`

**改为 `:45`**:
```
`linked_issue_overlaps` 代码存在、有测试、被调用过、返回值合法 —— **只是它的匹配谓词在跨格式输入上恒假**, 而恒假的返回值 (`[]`) 与「真没人在做」完全相同 ⇒ 击发时不可察觉。这是 memory `feedback_completion_signals_vs_runtime_invocation` 最有迷惑性的一种形态: 所有表面信号都是绿的。
```

**`:37-41` 整节改为**:
```
### 为什么这是 live 缺陷, 不是未来的事

**`linked_issue_overlaps` 已经在生产中被调用** —— `phase1_gate.py:1232`, 由 Phase B 入口的认领路径经 CLI 触达 (`phase-b-developer/SKILL.md:88-93` 的 `[--linked-issue]`)。⇒ **该机制今天就在跑, 谓词一旦遇到跨格式输入就漏报。**

> **⚠️ 但「今天已经在漏」当前无实例 (R1/M6, 本轮实跑复核)**: 对 `refs/aria/coordination` 全枚举 (16 个带 `linked_issue` 的 claim) 实测 —— 裸形族的号集合 `{116, 118, 122, 124}` 与 org 限定族同仓的号集合 `{110, 113, 121, 125}` **交集为空** ⇒ **从未发生过跨格式同号认领**。有多条同号 claim 的共 **2** 个 issue: `10CG/aria-plugin#110` (4 条, track_id 均 `state-scanner-stale-refs-false-parity`, 被 `collision.py:219-220` 自排除挡掉) 与 `10CG/aria-plugin#113` (2 条, track_id 均 `aria-plugin-113-gate-result-yaml-20260719`, 且均 `done` ⇒ 先被 `:210` 的 `_TERMINAL` skip)。**两组都与格式无关。**
>
> ⇒ **本 Spec ship 后, 把现有 16 条逐条回放为查询方, 输出零 delta** (本轮以生产 `linked_issue_overlaps` + 归一实现双跑逐行比对, delta 行数 = 0)。**修的是击发概率不是存量症状。**

> **凡本文出现「今天就在漏 / 对真实数据恒假 / 正在生产中失效」措辞的落点, 一律同批订正 —— 已知落点 `:12` `:45`。**

这与母 Spec 的其余部分不同: 那些依赖尚未落地的 A.1 接线; **本条不依赖任何新机制**。
```

**依据**: cross-clause 镜头。原 M6 只改 `:37-41`, 落地后 `:12`/`:45` 与新节直接矛盾。lens 3 的「唯一」订正 (#110 → #110 + #113) 已并入, 我独立复跑 ref 全枚举确认 `#113` 确有 2 条同 track_id 的 `done` claim。零 delta 我用两版谓词回放 16 行实测 = 0, 属实。

---

### [FIX-02] M8 + fact-check — 三族表升为六族表, D 族 6→4, 新增 F 族

**位置**: `:29-33` (三族表) — 替换整表并补口径段

**原文**: 三行表 A / B / C, 「实测」列为 `ref 中 4 条 / 9 条 / 0`。

**改为**:
```
⇒ 轨 A 认领 B 族、轨 B 认领 A 族 ⇒ `linked_issue_overlap` **恒 `[]`** ⇒ 与「真没人在做」**不可区分**。

**三个总体 (全文唯一定义处, 其余各处只引用不重定义)**:

- **已落盘总体** = `refs/aria/coordination` 现有 **16** 个 `linked_issue` 值 (今天 CLI 直传的实际落点);
- **复制源总体** = proposal 头部「关联 Issue」字段值 (AI 起草时最可能的抄写来源) —— 141 篇 tracked proposal 中命中 **12** 个字段行, 其中 **11** 个带真实 issue 引用 (第 12 个是本 Spec 自己的「无」);
- **未来输入总体** = 母 Spec §1 落地后由字段值直接喂入 `--linked-issue` 的集合 (**今天尚不存在**)。

**三者不是同一个总体。S4 的 0 实例结论测的是复制源总体。**

| 族 | 形态 | 已落盘总体 (ref 16) | 复制源总体 (11 值) |
|---|---|---|---|
| A | `aria-plugin#122` (裸仓名, 无空格) | **4** | **1** |
| B | `10CG/aria-plugin#110` (org 限定, 无空格) | **11** | **0** |
| C | `10CG/aria-plugin #122` (org 限定 + 空格) | **0** | **4** |
| D | `#137` (**无 repo 段**) | **0** | **4** |
| **F** ⭐ | `aria-plugin #95` (**裸仓名 + 空格**, repo 名在链接文字**之外**) | **0** | **2** |
| E | 逐字照抄整个字段值 (markdown 链接外壳) | **0** | **11** |

*(已落盘总体另有哨兵 1 条 `AUDIT-TEST-DO-NOT-USE#0`, 不入族; 4+11+1 = 16。)*

> **口径 (四列不可相加)**: A/B/C/D/F 按**最内层链接文字**分族, **互斥**, 复制源合计 **11**; **E 族是外壳轴**, 与前五族**正交**, 复制源 **11/11 全覆盖** —— 逐字照抄整个字段值得到的一定是 E 族 (形如 `Forgejo [#137](https://…/issues/137#issuecomment-12236)`), 按规则 1 取**最后一个** `#` 会切到 `issuecomment-12236))` 这类串 ⇒ **E 族一律不可解析**, 退回步骤 4 原串比较。其中 **5** 条尾部带 `#issuecomment-NNNNN` 锚点 (`aria-plugin#17` / `Aria#137` / `Aria#139` / `aria-plugin#113` / `aria-plugin#122` 五篇), 复现: `grep -rhE '^\s*>?\s*\*\*关联 Issue\*\*' openspec/{changes,archive}/*/proposal.md | grep -c '#issuecomment-'` → **5**。
>
> **F 族即 R2/m4 与 R1/M8 点名的「第四族」, 本表已单列, 不再并入 D。** 该族在本 Spec 规则下**可解析且能命中** (`left` strip 后为 `aria-plugin`, 无 `/` ⇒ `repo_basename = aria-plugin`), 是 §What Changes「每段各自 strip」规则最主要的现实落点 ⇒ 已进 SC-1。
```

**依据**: **fact-check 镜头覆盖 self-recurrence 镜头**。self-recurrence 明文把 `A=1 / C=4 / D=6 / E=11` 认证为「复核属实」——这是该镜头的一次核验失败。我逐值实读全部 12 个字段行独立确认: 真正无 repo 段的是 4 条 (`Forgejo [#137]` / `Forgejo [#134]` / `Forgejo [#139]` / `[#154]+[#157]+[#152]+[#156]`), 被误算进 D 的 2 条是 `aria-plugin [#95](…)` ×2 (`archive/2026-07-05-aria-archive-gate-runtime-reality:8` 与 `archive/2026-07-09-runtime-probe-archive-gate-integration:23`), 即 F 族。1+0+4+4+2 = 11 ✓。issuecomment 计数 **两镜头都报 5**, 我复跑 = 5, 采纳。
**镜头都没抓到的**: 「141 篇中 12 个字段值」把 12 个**字段行**当成 12 个**值** —— 第 12 行是本 Spec 自己的「无」, 真实带值的是 11, 而族表合计恰是 11。上文已按 12 行/11 值分开写死。

---

### [FIX-03] M2 — S5 两条论据重写 + 通用授权边界改为封闭清单

**位置**: `:58-61` (规则 3 的 ⭐ 子项及其三条论据块)

**原文**: `> **为什么必须加 (S5 实测)**: 既有 derive_track_id …` / `> **且这不是理论风险**: …` / `> **副作用是正收益**: …`

**改为**:
```
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
```

**依据**: cross-clause 镜头对「不得删除信息」的证伪。我实读 `:53` 与 `:63` 确认两处都用 `casefold()` —— 原 M2 边界条款按字面执行会同时杀死同批的 m1 `strip` 和既有的 `casefold`, 即「新写的条款上复发要治的病」。改为封闭清单 + 判别性准则后, 三条重写各自有授权来源。self-recurrence 镜头对 M2 的修正 (总体术语) 已并入 FIX-02 的三总体定义, 此处不重复定义。

---

### [FIX-04] M3 — 规则 2 谓词封闭化 (删「无上界」, 加 `int()` 防抛)

**位置**: `:56` (归一规则 2)

**原文**: `2. `number_str` 必须能解析为非负整数, 否则该值**不可解析** (见 4)。解析为 **`int`** 后比较 (故 `#007` ≡ `#7`);`

**改为**:
```
2. `number_str` (已 strip) **可解析当且仅当** `number_str.isascii() and number_str.isdigit()` 为真 —— 即**非空、全为 ASCII `0`-`9`**; 否则该值**不可解析** (见 4)。解析为 **`int`** 后按十进制值比较 (故 `aria-plugin#007` ≡ `aria-plugin#7`)。**前导零不剥、不截断**。
   - **为什么必须钉到这个谓词 (R1/M3: 母 Spec 写「纯数字」, 抽出漂成更宽的「能解析为非负整数」)**: `int()` 与 `isdigit()` 双向分叉, 本轮逐值实跑 (CPython 3.11.2) —— `int('+7')==7` / `int('1_0')==10` / `int(' 122')==122` 而三者 `isdigit()` 全 False; 反向 `'１２３'.isdigit()` 与 `'²'.isdigit()` 为 True 而 `int('²')` **抛 ValueError**。⇒ 必须同时钉住 `isascii()` 与 `isdigit()`。
   - **⚠️ 长度上界 (本轮新发现)**: `number_str` strip 后长度 **> `sys.get_int_max_str_digits()` (CPython 默认 4300) 时判不可解析**, 退回步骤 4 原串比较。**且实现不得依赖 `int()` 不抛异常** —— `int()` 调用必须包在 `try/except ValueError → 判不可解析` 里。实测: `('9'*4301).isascii() and .isdigit()` 为 **True**, 而 `int('9'*4301)` 抛 `ValueError: Exceeds the limit (4300 digits)`; 该异常在生产路径上会被 `phase1_gate.py:1235` 的 `except Exception` 吞成 `out["linked_issue_overlap"] = []` (静默漏报, 与本 Spec 要治的病同形)。
```

**依据**: self-recurrence 镜头。我在本机独立复跑全部六条边界值 + 4301 位实验, 逐条属实 (`sys.get_int_max_str_digits()` = 4300; `isascii() and isdigit()` 对 `'９'` 全角与 `'²'` 均正确拒绝)。原 M3「`number` 无上界 (Python int 任意精度), 不设长度限」+「判定在前、`int()` 在后」在 CPython ≥3.11 上为假, 且会新造一条异常路径。

---

### [FIX-05] m1 + C1×m2 — 空白规则统一为「段首尾 strip」, 并与段内空白划清

**位置**: `:55` (规则 1) + `:57` (规则 3 首句)

**原文 `:55`**: `1. 剥首尾空白; 按**最后一个** `#` 拆为 `left` / `number_str`;`
**原文 `:57`**: `3. `left` 剥尾部空白 (处置 C 族); 若含 `/`, …`

**改为 `:55`**:
```
1. 按**最后一个** `#` 拆为 `left` / `number_str`;
   - **空白处置的唯一规则 (m1)**: 切分出的**每一段** (`left` / `number_str` / `org` / `repo_basename`) 在使用前**各自 `str.strip()`。无例外。** 后果: `10CG / aria-plugin#1` ≡ `10CG/aria-plugin#1`, `aria-plugin# 122` ≡ `aria-plugin#122`, `aria-plugin #95` ≡ `aria-plugin#95` (F 族)。
   - **边界**: strip 只消除**每段首尾**空白; **段内空白既不删除也不译码** (`aria plugin` ≠ `aria-plugin`, SC-5c 钉死)。
   - **授权来源**: 本规则属规则 3 ⭐ 子项边界条款授权清单第 **(ii)** 条 (它是本轮**唯一一条主动扩大匹配面**的改动, 故必须有显式授权来源)。
```

**改为 `:57` 首句**: `3. 若 `left` (已 strip) 含 `/`, 取**最后一段**为 `repo_basename` (再 strip), 其前为 `org`; 否则 `repo_basename = left`, `org = None`。`repo_basename` 空 ⇒ 不可解析;`

**依据**: cross-clause 镜头 C1×m2 —— 原 C1 的「前导零与**段内**空白不影响」与同批 m2 的 SC-5c (段内空白必须影响) 直接互斥, 且 m1 的 strip 只消除每段首尾。术语统一为「段首尾空白」/「段内空白」两个词, 三处 (规则 1、SC-4、C2 baseline 表) 同批改。原 `:57` 的「剥尾部空白」是 5 个位置只规定 2 个的残留 (R1 minor), 一并收进统一规则。

---

### [FIX-06] C1 — 举例约束注释按「归一路径 vs 原串路径」分轴 (不按正例/反例)

**位置**: 规则 5 之后 (`:63` 末), 新增注释块

**改为 (新增)**:
```
> **⚠️ 举例约束 (C1 防复发)**: R1 的 C1 根因是 SC-4 用了裸 `#007` × `#7` —— 按规则 3「`repo_basename` 空 ⇒ 不可解析」, 该例走的是步骤 4 原串比较, `'#007' != '#7'` ⇒ **不命中**, 与 SC-4 期望的「命中」直接冲突。
> **故本 Spec 全文的举例按路径分轴, 不按正例/反例分**:
> - 凡期望**经归一命中**的正例, **必须带 repo 段** (`aria-plugin#007` 而非 `#007`);
> - 凡期望**经步骤 4 原串精确比较命中**的正例, **必须**使用逐字相同的不可解析串 (如 `#5` × `#5`) —— 这类正例**不带 repo 段是规则 4 的直接推论, 不构成矛盾**;
> - 反例 (期望不命中) 不受 repo 段约束。
```

**依据**: self-recurrence 镜头。我实跑生产函数确认 `linked_issue_overlaps([claim('#5')], 'mine', '#5')` 返回**非空 (命中)** —— SC-6「解析失败即 `return False` 的实现必红」的红机制**只能**由裸 `#5` 的期望命中正例构成。原 C1 注释按「正例/反例」分轴会把这个唯一可红的形状划进全称禁令, 当场杀掉 SC-6。

---

### [FIX-07] M1 + M1×M2×D2 — 「回显原串」降为半幅, 三处同批带限定

**位置**: `:67` (org 轴末句) + `:88` (D2 要点列) + FIX-03 已含规则 3 的第三处

**原文 `:67` 末句**: `代价: `otherorg/aria-plugin#122` 与 `10CG/aria-plugin#122` 会误配 ⇒ **surface 必须回显双方 `linked_issue` 原始串**, 让人一眼判别。`

**改为 `:67` 末句**:
```
代价: `otherorg/aria-plugin#122` 与 `10CG/aria-plugin#122` 会误配 ⇒ 需**回显双方 `linked_issue` 原始串**让人一眼判别。

> **⚠️ 该缓解在本 Spec 交付窗内只成立一半 (R1/M1, 本轮实读复核)**: 对方那一侧**已经有** —— `collision.py:228` 逐字回显 `c.linked_issue` 未归一原串, docstring `:204-205` 已列该键。**自己那一侧没有** —— `phase1_gate.py` 的 `_claim_to_dict` (`:1119-1131`) 与 `_gate_result_to_dict` (`:1134-1169`) **均无 `linked_issue` 字段**, 而补它要动 `phase1_gate.py`, 那是本 Spec 的**显式非目标** (`:118`)。
> ⇒ **成文已知限 (与 basename 截断轴同一处置形式 —— 成文落 D4 + 本段, 不写进任何 SC 的期望列; 理由同 SC-5 去循环定义)**: 本 Spec **不**补自己那一侧。D2 的代价在本 Spec 交付窗内**只缓解一半**: 看得见对方写的是什么, **看不见自己传的是什么** —— 对**转述该 JSON 的下游**尤其致盲。母 Spec §2.3 逐字要求「双方 `linked_issue` 原始串」、其 Impact 表已列 `phase1_gate.py`, 该半缺口由母 Spec 闭合。
> **凡引用「回显原串」作为代价缓解的落点, 一律带半幅限定 —— 已知落点 `:88` (D2)、规则 3 的译码论据。**
```

**原文 `:88`**: `| D2 | `org` 不参与匹配 | advisory 下漏报昂贵、误报便宜 ⇒ fail-toward-reporting; 代价由「回显原串」兜 |`

**改为 `:88`**:
```
| D2 | `org` 不参与匹配 | advisory 下漏报昂贵、误报便宜 ⇒ fail-toward-reporting; 代价由「回显**对方**原串」兜 —— **仅半幅** (自己那一侧不在 CLI 输出中, 见 §极性段成文已知限 + SC-9), 对转述该 JSON 的下游不成立 |
```

**依据**: self-recurrence 镜头指出原 M1 的新指针「与 SC-5 同一处置形式」会被同批 m4 删掉 (悬空), cross-clause 镜头指出 `:88` 与 M2 两处仍无限定地把「回显原串」当完整缓解。两条修正合并采纳。四条代码事实我逐条实读复核, 全部属实 (`:228` 有 / `:1119-1131` 无 / `:1134-1169` 无, 且 `_gate_result_to_dict` 函数体**止于 `:1169`**, 不是 `:1170`)。

---

### [FIX-08] M4 (fact-check 覆盖原计划) — R2 的 24/10 **未被推翻**, 只是另一个口径

**位置**: `:69` (basename 轴) + `:90` (D4 要点列)

**原文 `:69`**: `**basename 轴 (诚实标注, R2/M2)**: `repo_basename` 用**精确相等**, 对真实别名**恒漏** —— R2 语料统计 `aria-orch` **24 次** vs `aria-orchestrator` **10 次**。⇒ **本机制在 basename 轴是 fail-toward-silence, 与 org 轴方向相反**。`

**改为 `:69`**:
```
**basename 轴 (诚实标注, R2/M2)**: `repo_basename` 用**精确相等**, 对真实别名 (截断型) **恒漏** ⇒ **本机制在 basename 轴是 fail-toward-silence, 与 org 轴方向相反**。

> - **R2 的 24/10 未被推翻, 它是另一个口径 (R1-fix 复核订正)**: R2 量的是 **issue 引用位置** (`grep -rhoE '\baria-orch[a-z]* ?#[0-9]+' openspec/ docs/ | sed -E 's/ ?#[0-9]+//' | sort | uniq -c`), 2026-08-04 逐字复跑仍得 **25 / 11** (其中 **24/8 落在 `docs/`**); S4 与下表量的是**全文裸 token**, 语料 `openspec/*/*/*.md`。**两组口径不同, 不可比, 谁也没推翻谁。**
> - **全文裸 token 口径 (2026-08-04 实跑, 命令逐字, 口径 = 出现次数不是行数)**: 文件集 `openspec/*/*/*.md` = **250 文件**; `grep -oh 'aria-orchestrator' openspec/*/*/*.md | wc -l` → **736**; `grep -ohP 'aria-orch(?!estrator)' openspec/*/*/*.md | wc -l` → **16**。
>   **⚠️ 文件集与计数法都必须照抄**: 换成 `find openspec -name '*.md'` (276 文件) 得 **745**; 用 `grep -c` (数行不数次) 得 **674**。数字只承载定性 (「截断写法在正式文档里是少数」), 不承载阈值。
> - **真正让 basename 截断轴降为「已知限」的只有 S4 的另一半结论** —— **复制源总体上截断型别名 = 0 实例**; 本轮补测**已落盘总体** (ref 16 值) 同样 **0 实例** (实测 basename 只有 `aria-plugin` / `Aria` / `AUDIT-TEST-DO-NOT-USE`, 无截断型、无含 `.`/`_` 者)。**两个总体各自为 0, 非跨总体推断。本 Spec 不以「比例反了」为依据。**
```

**原文 `:90`**: `| D4 | basename 轴的 fail-toward-silence **成文为已知限**, 不在本 Spec 解决 | 别名表 / 书写强制均需语料决策 ⇒ 属 spike 范围 (母 Spec) |`

**改为 `:90`**:
```
| D4 | basename 轴的 fail-toward-silence **成文为已知限**, 不在本 Spec 解决 | 依据 = S4 实测**复制源总体** 0 实例 + 本轮实测**已落盘总体** 0 实例 (两个总体各自为 0); 别名表 / 书写强制均需语料决策 ⇒ 属 spike 范围 (母 Spec)。**「回显原串」半幅限度同挂本条, 见 §极性段** |
```

**依据**: **fact-check 镜头覆盖原计划与 self-recurrence 镜头**。我按 R2 报告 `:170` 的命令逐字复跑得 `25 aria-orch / 11 aria-orchestrator`, 拆开看 `docs/` 独占 24/8 —— 原 M4 的「比例是反的 / spike S4 已推翻 / 作废」会给唯一一次在**最接近 `--linked-issue` 的总体**上做的测量盖假章, 恰是它自己声称要治的「换总体举证」反向犯一次。

---

### [FIX-09] M5 — `yielded` 归属披露 (接口面)

**位置**: `:79` (接口面末句)

**原文**: `⇒ Phase B 现有调用方**零改动**, 行为变化仅为「原本漏报的现在能报出来」。`

**改为**:
```
⇒ Phase B 现有调用方**零改动**。

> **行为变化清单 (R1/M5: 「仅为原漏报现能报」不完整)**:
> 1. 跨格式同号的 claim 从不可见变为可见 (本 Spec 的目的);
> 2. **`yielded` 状态的 claim 会一并被归一后的谓词命中** —— `collision.py:210` 的 `_TERMINAL = ("done","abandoned","unknown")` **不含 `yielded`** (而 `claim_lifecycle.py:317`/`:408` 的 `_TERMINAL_STATUSES` **含**它, 两处语义不一致, 属既有分歧, 非本 Spec 引入)。ref 现有 **3 条 `yielded`** (`10CG/aria-plugin#110`, claimed_at `2026-07-14T11:26:09Z` / `12:32:51Z` / `17:10:32Z`, track_id 均 `state-scanner-stale-refs-false-parity`) 因此是**新的可命中目标**;
> 3. `int()` 与解析失败路径新增的异常面 (规则 2 长度上界), 由 `phase1_gate.py:1235` 的 `except Exception` fail-soft 吞掉 —— **这条兜底本身就是静默漏报**, 已按规则 2 要求实现侧不得依赖它。
>
> **⚠️ 第 2 条不与 §Why 的「零 delta」冲突, 二者说的是不同东西**: 本轮实跑 —— 把现有 16 条逐条回放为**查询方**, 新旧输出 delta = **0** (那 3 条 `yielded` 与查询方共享 track_id, 被 `:219-220` 自排除); 但若**未来**有人以裸格式 `aria-plugin#110` 从**另一个 track_id** 认领, 新谓词会一次性浮出这 3 条 `yielded` (实测 old `[]` → new 3 条)。⇒ **「零 delta」限定于存量回放, 「yielded 变可达」限定于未来输入。两句都必须带这个限定词。**
```

**依据**: **这条 (`⚠️` 段) 是我作为综合者新增的, 三个镜头都没抓到。** M5 与 M6 在同一批交付里, 逐字读是互斥的 (「现有 3 条会变可达」vs「现有 16 条零 delta」)。我用两版谓词回放 16 行实测 delta=0, 又用假想输入 `('some-other-track', 'aria-plugin#110')` 实测 old `[]` → new 3 条 —— 两句各自成立, 但都必须带限定词, 否则下一轮读者会判其中一句是错的。这正是「多条 fix 互相拆台」的标准形状。

---

### [FIX-10] M8×m5 — D1 要点列合并为一条自洽文本 (两条 fix 共同署名)

**位置**: `:87` (D1 要点列)

**原文**: `| D1 | 比较键 = `(basename.casefold(), int(number))` | **R2 已用 18 元语料穷举验证**: 自反 / 对称 / 传递**零违例**, 是良定义的等价关系 |`

**改为**:
```
| D1 | 比较键 = `(basename.casefold(), int(number))` | **等价关系已被验证但证据不可复核**: R2 曾用 18 元语料穷举自反/对称/传递零违例, **该语料未入库、现已不存在**; R1/BA 在加入 `./_ → -` 译码后**用本 Spec 文本内的字面值重新穷举**, 同样零违例 —— 那是 R1 的实测, **不是可继承的 R2 资产** (R2 验的键是 `(basename.casefold(), number)`, **不含**译码)。⇒ **Phase B 必须建 committed fixture** (`tests/fixtures/linked_issue_corpus.txt`, 口径见 SC-7) 取代上述两次口头引用; fixture 入库前, D1 的等价关系主张按「**已论证、未留证**」计 |
```

**依据**: cross-clause 镜头。M8 与 m5 改同一个单元格且互不引用: M8 以「R2 的 18 元穷举验证」为前提做限定, m5 同时宣布该语料不存在不可复核。任一条单独落地都产生悬空引用。合并文本由两条共同署名。SC-7 条目须回指:「本 fixture 同时是 D1 的证据载体」。

---

### [FIX-11] C2 + m8 — rule6_note 前提句与 substitute 表同批重写

**位置**: `:94` (整条 rule6_note, **含前半句前提**)

**原文**: `**Rule #6 (rule6_note)**: 改动面为 `lib/collision.py` 的一个内部比较谓词 + 其测试, **零 SKILL.md / 零 description / 零 AI 指令面** ⇒ 判据表**第一行…** ⇒ **substitute: …**(SC-1~6 均在现状代码上可红)。…`

**改为 (推荐 = cross-clause 方案 A; 见 §不确定项 U-2)**:
```
**Rule #6 (rule6_note)**: 改动面 = `lib/collision.py` 的一个内部比较谓词 + 其测试 + **两处纯描述性文档同步** (`collision.py` docstring `:182-206`、`SKILL.md:176` 的括注); **零 `description` / 零 frontmatter / 零运行时指令流程变更**。按 CLAUDE.md「同文件两性质并存时逐 hunk 判」**逐 hunk 判定**: `SKILL.md:176` 的 hunk 仅追加「(按归一后的 `<repo>#<n>` 比较, org 不参与)」这一**事实勘正**, 不改任何指令 / 触发条件 / 判断流程 ⇒ 仍落判据表**第一行「描述性 (schema / 字段 / 命令 / 勘正)」** ⇒ **substitute: SC 级 baseline-failing 结构化测试替代**。与 v1.65.2 (#124 纯脚本修复) 同一判据路径。**不申请豁免。**

**baseline 实测结果 (R1 三席 + R1-fix 起草者 + R1-fix 综合者三方独立复跑, 逐格一致)**:

| SC | baseline | 性质 | 算进 substitute 证据面? | **取证方式** |
|----|---------|------|---|---|
| SC-1 | **红** | 主判据 (跨族归一) | ✅ | 实跑生产 `linked_issue_overlaps` |
| SC-2 | 绿 | 负控 (不同仓不得命中) | ❌ | 实跑生产 `linked_issue_overlaps` |
| SC-3 | **红** | 主判据 (org 不参与) | ✅ | 实跑生产 `linked_issue_overlaps` |
| SC-4 | **红** | 主判据 (int 比较 + **段首尾空白 strip**) | ✅ | 实跑生产 `linked_issue_overlaps` |
| SC-5 | 绿 | 已知限 (截断型不归一) | ❌ | 实跑生产 `linked_issue_overlaps` |
| SC-5b | **红** | 主判据 (`./_ → -` 译码) | ✅ | 实跑生产 `linked_issue_overlaps` |
| SC-5c | 绿 | 负控 (段内空格不译码) | ❌ | 实跑生产 `linked_issue_overlaps` |
| SC-6 | 绿 | 回落语义 (原串比较) | ❌ | 实跑生产 `linked_issue_overlaps` |
| SC-6b | 绿 | 边界负控 | ❌ | 实跑生产 `linked_issue_overlaps` |
| SC-7 | 绿 | **结构上不可红** (任何「算 key 再比较」的实现自动满足三性质) | ❌ | **结构推理, 未跑** |
| SC-8a | 绿 | 签名冻结 | ❌ | `inspect.signature` 内省, **未调用本函数** |
| SC-8b | 绿 | 返回 key-set 冻结 | ❌ | key-set 内省, **未调用本函数** |
| SC-8c | 绿 | 既有测试回归 | ❌ | 跑既有测试 |
| SC-9 | 绿 | 回显未归一原串 (现状即如此) | ❌ | 实跑生产 `linked_issue_overlaps`, 返回条目 `linked_issue` = `10CG/aria-plugin #122` 原串, keys 恰为那 7 个 |

⇒ **substitute 的证据面 = SC-1 / SC-3 / SC-4 / SC-5b 四条 baseline-failing**; 其余为负控 / 已知限 / 回落语义 / 冻结断言 —— 它们锁住「修复后不应退化」的行为, 有价值但**不能算进 substitute 的证据面** (负控恒绿是正确的, 不是证据)。R1 的 C2 原文「SC-1~6 均可红」经三方实测**不成立**, 已按实测改写。
```

**依据**: self-recurrence 镜头 (取证方式列 + 删全称出处句 + SC-9 落定) 与 cross-clause 镜头 (前提句必须连改) 合并。我实读 `SKILL.md:1-12` 确认 `description` 在 `:3-7` 未动、`:176` 是正文非 frontmatter, 两条前提事实成立。**表头的「直接调用生产 `linked_issue_overlaps` 实跑」全称句必须删** —— SC-7/8a/8b 结构上不可能由调用该函数测得, 保留全称句就是「在引用『须实证而非声称』之后紧接着声称一个未实测范围」的原病复发。

---

### [FIX-12] C1 + M3 + M7 + m2 — Success Criteria 表整体重写

**位置**: `:102-112` (整张 SC 表)

**改为**:
```
| SC | 场景 | 期望 | 怎么会红 |
|----|------|------|---------|
| **SC-1** | 四族两两配对 (6 对): `aria-plugin#122` × `10CG/aria-plugin#122` × `10CG/aria-plugin #122` × `aria-plugin #122` (**第四元 = F 族, 裸仓名 + 空格, 无 org**) | **两两互相命中** | 现状裸 `!=` 在**全部 6 对**上必红 |
| **SC-2** | `10CG/Aria#147` × `10CG/aria-plugin#147` (同 org 同号, **不同仓**) | **不得**命中 | 「只比 number」的退化实现必红 |
| **SC-3** | `10CG/aria-plugin#1` × `otherorg/aria-plugin#1` (**两侧都有 org 且不同**) | **命中** (org 不参与) | **唯一能区分「org 不参与」与「两侧有 org 才比 org」两种实现的用例** (R2/M1) |
| **SC-4** | (a) `aria-plugin#007` × `aria-plugin#7`; (b) `aria-plugin# 122` × `aria-plugin#122` | **两组各自命中** (number 按十进制值比较; **前导零与各段首尾空白不影响**; **段内空白不归一, 见 SC-5c**) | 字符串比较必红; 不 strip `number_str` 的实现在 (b) 上必红 |
| **SC-5** | `10CG/aria-orch#5` × `10CG/aria-orchestrator#5` (**截断型**别名) | **不命中** | 锁定 basename 轴 fail-toward-silence。*(该结果作为已知限成文于 D4 + §极性段 basename 轴, **不写进本列** —— 「期望列写『被记为已知限』」是循环定义, R1/minor 已判)* |
| **SC-5b** ⭐ | `10CG/10cg.local#20` × `10CG/10cg-local#20` × `10CG/10cg_local#20` (**分隔符型**别名, 真实仓) | **两两命中** | 只做 casefold 的实现必红。**与 SC-5 是两类**: 分隔符型**能**归一, 截断型不能 |
| **SC-5c** ⭐ | `10CG/aria plugin#1` × `10CG/aria-plugin#1` (**段内空格**) | **不命中** | 把段内空格也译成 `-` 的**过宽**实现必红 (钉住 M2 边界清单只授权三条重写) |
| **SC-6** | 不可解析值的**显式配对**: (a) `#5` × `#5` ⇒ **命中**; (b) `#5` × `#7` ⇒ 不命中; (c) `10CG/#7` × `otherorg/#7` ⇒ **不命中** (原串不同, 尽管归一后会同键 —— **D3 论域划分的承重断言**); (d) `no-hash-here` × `no-hash-here` ⇒ **命中**; (e) `repo#abc` × `repo#abc` ⇒ **命中** | 全部走步骤 4 **原串精确比较**; **不抛异常**; **不因解析失败判「不匹配」** | 解析失败即 `return False` 的实现在 (a)(d)(e) 三个自配对上必红 |
| **SC-6b** ⭐ | `number_str` 边界**配对**: `aria-plugin#+7` × `aria-plugin#7` / `aria-plugin#1_0` × `aria-plugin#10` / `aria-plugin#１２３` × `aria-plugin#123` / `aria-plugin#²` × `aria-plugin#2` 四对; 外加四个左值**各自与自身配对**; 外加 `aria-plugin#<4301 个 9>` 与自身配对 | 四对**均不命中**; 五个自配对**均命中** (原串相同, 走步骤 4); **全程不抛异常** | 裸 `int()` 的实现在前三对上命中 ⇒ 红; 裸 `isdigit()` 的实现在 `#²` 上 `int()` 抛 ValueError ⇒ 红; 「判定在前、`int()` 在后且不 catch」的实现在 4301 位自配对上抛 ValueError ⇒ 红; 「解析失败即判不匹配」的实现在五个自配对上不命中 ⇒ 红 |
| **SC-7** | 等价关系性质: 对 **committed fixture** `tests/fixtures/linked_issue_corpus.txt` 断言自反 / 对称 / 传递 | 三性质零违例 | 非等价关系的实现 (如单向前缀匹配) 必红。**本 fixture 同时是 D1 的证据载体** (D1 引的 18 元语料已不存在)。⚠️ **判别力自陈**: 任何「算 key 再比较」的实现都自动满足三性质 ⇒ 本条是**回归护栏, 不是主判据** |
| **SC-8a** | `inspect.signature(linked_issue_overlaps)` 逐字 == `(claims, own_track_id, own_linked_issue)`, 后两参**无默认值** | 逐字不变 | 改签名 / 加默认值的实现必红 |
| **SC-8b** | 返回条目 `sorted(keys())` 逐字 == `['claimed_at','container','linked_issue','owner','session','status','track_id']` | 逐字不变 | 增删键的实现必红 |
| **SC-8c** | 既有 **6** 条测试逐字不改全绿 + **新增 CLI 全链路 near-miss 负控** | 全绿 | 见下方 SC-8c 展开 |
| **SC-9** ⭐ | 命中条目的 `linked_issue` 值 | **回显未归一的原始串** (如 `10CG/aria-plugin #122` 原样, 不是归一后的 key) | 把归一结果写回该键的实现必红。*(现状即如此, `collision.py:228`; 本条是冻结断言, baseline 绿)* |

**SC-8c 展开 (R1/M7 + 本轮实读订正)**:

既有测试 **6** 条构成 `linked_issue_overlap` 的既有冻结面, 逐字不改必须全绿:

- **lib 层 4 条** (`tests/test_release_by_track.py`, `class TestLinkedIssueOverlaps` 位于 **`:206-247`**): `test_same_issue_different_track_flagged` (`:224`) / `test_same_track_not_flagged` (`:232`) / `test_terminal_and_no_issue_ignored` (`:236`) / `test_none_own_issue_short_circuits` (`:245`);
- **CLI 层 2 条** (`class TestPhase1GateLinkedIssueCli`, `:527-575`): `test_linked_issue_written_and_overlap_surfaced` (`:533`) —— **唯一端到端驱动本谓词**的既有测试 (subprocess 跑 `phase1_gate.py --linked-issue`, `:554-557` 断言 `out["linked_issue_overlap"]` 的长度与 `track_id`, 该键由 `phase1_gate.py:1232` 产出), 也是 §接口面第 3 条点名的 `phase1_gate.py:1235` fail-soft 吞异常路径的**唯一现成观测点**; `test_no_linked_issue_no_overlap_key` (`:563`) —— 它**不调用本谓词** (`phase1_gate.py:1229` 的 `if args.linked_issue:` 守卫短路), 锁的是「未传参 ⇒ 该键不出现」的 additive 契约。
  ⇒ **6 条中 5 条真正驱动本谓词, 第 6 条锁调用侧守卫。R1 报告的「6 个」属实, 无需订正。**
- **⚠️ 判别力自陈**: 这 6 条在「匹配」这一侧**全部使用逐字相同的字面串** (`"A#7"` × `"A#7"`, `"10CG/Aria#160"` × `"10CG/Aria#160"`), 在「不匹配」这一侧全部靠 status / None / track_id 分支 ⇒ **对新比较逻辑的 near-miss 判别力为零**。SC-8c 证明的是「没有破坏无关分支」, **不是**「新逻辑没有引入误配」——后者全压在 SC-1~SC-7 上。
- **故 SC-8c 必须新增 near-miss 负控, 且至少一组走 CLI 全链路** (仿 `test_linked_issue_written_and_overlap_surfaced` 的 subprocess 形式)。**怎么会红**: 归一只落在 `collision.py` 而 **CLI 那侧未接上**的实现在该组上必红 —— 母 Spec §2.4 逐字点名的失败模式:「**SC 的断言层必须是 CLI 全链路**, 不是直调库函数 —— 否则『参数没接到 CLI』的实现仍能绿」。
```

**依据**: 四镜头修正合并。**M7 上两镜头冲突, 我裁给「6 条 = 5 驱动 + 1 守卫」的精确表述** (见 §裁断 A-3), 实读 `phase1_gate.py:1229` 的 `if args.linked_issue:` 守卫作为判据。行号全部改用我实读的值 (`:206-247` / `:224` / `:527-575`), self-recurrence 镜头原文的 `:205-246` / `:223-246` 是 off-by-one。SC-6 / SC-6b 的显式配对我逐对实跑验证 (裸 `#5`×`#5` 现状命中; SC-6b 四个自配对三种实现全绿 ⇒ 原写法判别力为零, 必须跨值配对)。

---

### [FIX-13] m8 + M7 — Impact 表补文档同步行与测试宿主点名

**位置**: `:129-135` (Impact 表 + 测试基线句)

**改为**:
```
| 文件 | 变更 |
|------|------|
| `skills/state-scanner/lib/collision.py` | 归一比较谓词 (§What Changes 五步); 签名与 schema 不变 |
| `skills/state-scanner/lib/collision.py` docstring `:182-206` | 文案同步 — 说明匹配按归一后的 `<repo>#<n>`, org 不参与; **措辞不得暗示「已穷尽核实 / 已覆盖全部别名」** |
| `skills/state-scanner/SKILL.md:176` | 文案同步 — 「同 issue 不同 track-id 的『同一件事两个名字』」补「(按归一后的 `<repo>#<n>` 比较, org 不参与)」。**纯事实勘正 hunk, 见 rule6_note 逐 hunk 判定** |
| `skills/state-scanner/tests/test_release_by_track.py` (既有宿主) | 扩展 — SC-1~9; 既有 6 条 (`:206-247` 4 条 + `:527-575` 2 条) 逐字不改 |
| `skills/state-scanner/tests/fixtures/linked_issue_corpus.txt` (**新建**) | SC-7 语料全集 + D1 的证据载体 |
| 发版 5 文件 + 主仓 gitlink | v1.66.0 MINOR |

测试基线: state-scanner 现 **1322** tests, 本 change 新增按 SC 子用例下界 **≥12**。全量跨 skill 套件须绿 (`run_all_tests.sh`)。
```

**依据**: m8 (KM minor) + M7。`SKILL.md:176` 与 docstring `:182-206` 我实读确认存在且内容匹配。**该行与 FIX-11 的 rule6_note 前提句必须同批落地并互相引用 (cross-clause 镜头), 不得只落其一。**

---

### [FIX-14] m4 × `:71` — 「只做两件事」的载体订正

**位置**: `:71`

**原文**: `**本 Spec 不解决 basename 别名** … 此处**只做两件事**: (a) 把该限度**写进 SC-5 作为断言**, 防它被误读成「已覆盖」; (b) 在 surface 文案中不暗示「已穷尽核实」。`

**改为**:
```
**本 Spec 不解决 basename 截断型别名** (那需要别名表或书写强制, 属母 Spec 范围)。此处**只做三件事**: (a) **SC-5** 用纯行为断言把该轴的行为钉死 (`10CG/aria-orch#5` × `10CG/aria-orchestrator#5` **不命中**); (b) 该行为**作为已知限成文于 D4 与本段**, 防它被误读成「已覆盖」; (c) **不新增任何 surface 文案** —— 现有 `SKILL.md:176` 与 `collision.py` docstring 的同步措辞 (见 Impact 表) **不得**出现「已穷尽核实 / 已覆盖全部别名」一类暗示。
```

**依据**: cross-clause 镜头。m4 把「已知限成文」的责任从 SC-5 搬到 D4 + §极性段, 但 `:71`(a) 仍指名 SC-5 为载体 ⇒ 落地当天交叉引用变假。(b) 的「surface 文案」原本无落点, 现由 Impact 表的两个文档同步行承载, 成为可验收点。

---

### [FIX-15] M8 — 「审计资产继承」免审名目限定到被验证过的那一版

**位置**: `:149` (结论句) + 表后新增清单

**原文**: `⇒ 本 Spec 的 post_spec 应聚焦**抽出过程本身**是否引入偏差 …, 而非重审已被三轮确认的算法本体。`

**改为**:
```
⇒ 本 Spec 的 post_spec 应聚焦**抽出过程本身**是否引入偏差 (措辞漂移 / SC 遗漏 / 与母 Spec 的边界)。**可不重审的只有两项**:

(a) **R2 用 18 元语料穷举验证过的那一版比较键** —— `(repo_basename.casefold(), int(number))`, **不含** S5 的 `./_ → -` 译码 / **不含**统一 strip / **不含** `isascii()+isdigit()` 谓词 —— 的自反 · 对称 · 传递三性质 (且该语料已不存在, 见 D1);
(b) 「**org 不参与匹配**」的极性判断。

**其余一律在审计范围内。本轮对比较键的三处修改 (S5 译码 / 统一 strip / isascii+isdigit 谓词) 全部在审计范围内**, 见下方清单。

**⚠️ 本轮新增未审表面 (R3 之后新增, 零审计记录)**:
1. **规则 2 的 `isascii() and isdigit()` 谓词 + 4300 位长度上界** — 全新, 承重的字符级判据;
2. **「每段各自 `str.strip()`」的统一空白规则** — 全新, 且**改变了行为面** (本轮唯一主动扩大匹配面的改动);
3. **`./_ → -` 译码 (S5)** — R2 的穷举**不含**它;
4. **M2 的「封闭重写 vs 语料决策」判据与其三条授权清单边界** — 全新, 是通用授权形状;
5. **六族表 (含新增 F 族)** — 全新;
6. **6 条新 SC** (SC-5c / SC-6b / SC-8a / SC-8b / SC-8c / SC-9) — 全新;
7. **rule6_note 的 baseline 实测表与逐 hunk 判定** — 全新。

**R3 的三条订正 (留痕)**: R3 原文是 6 项要点、**无「可实现性评估表」这一措辞**、`release-by-track` 同样无 caveat —— `:147` 的「在其可实现性评估表中是唯一无缺口的核心项」是**合理复述非逐字引用**, 已按此标注。
```

**依据**: self-recurrence 镜头。原 M8 改写后仍把「比较键的等价关系」整体列为可不重审, 而本轮恰好改了比较键的三个分量 —— 免审名目在本轮之后指称的已不是被三轮确认过的那个键。

---

### [FIX-16] m9 × M8 — 闸门待裁处置 (2) 必须重写, 不是只追加一句

**位置**: `:157`

**原文**: `可选处置: (1) 照跑完整 post_spec; (2) **定向轮 —— 只审「抽出过程」** (…), 不重审算法本体; (3) 判定审计资产可继承、免跑并留痕请复议。`

**改为**:
```
可选处置:

(1) 照跑完整 post_spec;
(2) **定向轮 —— 审计范围 = 抽出偏差 ∪ 上文「本轮新增未审表面」清单全部 7 项** (含规则 2 的 `isascii()+isdigit()` 谓词与长度上界、统一 strip 规则、S5 译码、M2 的封闭重写判据与授权清单、六族表、6 条新 SC、rule6_note 的 baseline 表与逐 hunk 判定)。**仅**「比较键的等价关系 (R2 验过的那一版)」与「org 不参与匹配的极性」两项可凭三轮资产免审 —— **「不重审算法本体」的旧措辞在本轮已失效, 撤回**;
(3) ~~判定审计资产可继承、免跑并留痕请复议~~ —— **已被 R1 自身证伪, 从选项中撤回** (R1 的 2 条 critical 都是「抽出/新增时引入」的, 不在被继承的三轮资产里)。

⇒ 处置 (3) 撤回; 处置 (2) 已按 `:149` 与「本轮新增未审表面」清单重新定界 —— **旧措辞会豁免掉本轮全部零审计的承重条款, 触 Rule #10**。

**AI 不预判。** 本 Spec 在裁决前不进 A.2/A.3。
```

**依据**: cross-clause 镜头。m9 只撤回 (3), 未动 (2); 而同批 M8 把 `:149` 改成「其余一律在审计范围内」并新增清单 —— 相隔 8 行两条条款给出相反的审计范围, 且 owner 若选 (2), 按其字面将恰好豁免掉本轮全部零审计新条款, 与 M8 新增该清单的目的 180° 相反。**修正方向 = 收紧豁免面, 是 Rule #10 下的安全方向。**

---

### [FIX-17] minor 批 — 剩余小项 (无镜头异议, 原样采纳)

| id | 位置 | 改法 |
|---|---|---|
| m3 | `:39` | 「`phase1_gate.py`」补路径 `scripts/phase1_gate.py` (行号 `:1232` 本身准确) |
| m6 | `:6` `:10` `:41` `:119` | 三处「母 Spec 已 spike-first 挂起」→ 按母 Spec 实际状态改写 (母 Spec `:3` 已改 Draft v2, `:8` 前置依赖声明, S1–S6 全完成) |
| m7 | `:75` | ref 计数陈旧 13 → **16** (与 §Why 三总体段一致) |
| m10 | `:62` | 补回母 §0 抽出时丢失的两条约束: 「**不得用模糊匹配 / 编辑距离 / 前缀包含**」禁令 + 步骤 4 的三条不可解析枚举 |

---

## 镜头冲突与裁断

**A-1. M4 语料数字 — self-recurrence (276/745, 判「复现不出」) vs fact-check (250/736 ✓)**
**裁给 fact-check。** 我实测: `openspec/*/*/*.md` = **250 文件 → 736 次**; `find openspec -name '*.md'` = **276 文件 → 745 次**; `grep -c` = **674 行**。两镜头各自的数都对, 但 self-recurrence 只试了 276 那个文件集就宣布「在被审计的 commit 上复现不出」——**它自己犯了一次换总体举证**。修法采 fact-check 的「钉死文件集 + 钉死计数法」。

**A-2. M4「R2 24/10 是否作废」— 只有 fact-check 检查了这一点**
**裁给 fact-check, 且这条推翻了原修法计划的方向。** 我按 R2 报告 `:170` 逐字复跑得 `25 aria-orch / 11 aria-orchestrator`, 且 24/8 落在 `docs/` (M4 的文件集根本不含 `docs/`)。原计划的「比例是反的 / 已推翻 / 作废」会误杀一条有效测量。

**A-3. M7 既有测试计数 — self-recurrence (5) vs fact-check (6)**
**两者都对一半, 我裁「6 条冻结面, 其中 5 条驱动谓词」。** 判据: 我实读 `phase1_gate.py:1229` 的 `if args.linked_issue:` 守卫 —— `test_no_linked_issue_no_overlap_key` (`:563`) **不传参 ⇒ 谓词根本不被调用**, 故 self-recurrence 的「5 条驱动本谓词」是对的; 但 R1 的「6」出自 QA 报告 `:148` 的具名枚举 (4 lib + 2 CLI), **可直接导出、不是计数错误**, 故 fact-check 的「不该订正 R1」也是对的。两镜头共同的实质结论一致且我采纳: **CLI 端到端测试 (`:533`) 必须进冻结面, near-miss 负控必须有一组走 CLI 全链路。**

**A-4. M8 五族表 D 族计数 — self-recurrence 认证 D=6「属实」 vs fact-check 判 D=4 + 新增 F=2**
**裁给 fact-check。** 我逐值实读全部 12 个字段行独立复算: A=1 / B=0 / C=4 / D=4 / F=2 = 11 ✓。self-recurrence 在此条上核验失败 (它复核了 issuecomment 计数却把族计数整体放行)。

**A-5. 术语「输入总体」— self-recurrence 二分 vs cross-clause 三分**
**裁给 cross-clause 的三分口径** (已落盘 / 复制源 / 未来输入), 已落 FIX-02。二分会把「今天尚不存在的未来输入集合」和「今天 ref 里的 16 值」混为一谈, 而 S4/D4 的承重结论恰好要区分这两者。

---

## 本轮 deferred (不修, 留痕)

| # | 项 | 理由 |
|---|---|---|
| D-1 | `collision.py:210` 的 `_TERMINAL` 不含 `yielded` 而 `claim_lifecycle.py:317`/`:408` 的 `_TERMINAL_STATUSES` **含** `yielded` | **既有语义分歧, 非本 Spec 引入**。本 Spec 只披露 (FIX-09), 不改 —— 改它会改变 `include_terminal` 语义, 已列为非目标 `:122` 且属母 Spec。**建议单开 issue。** |
| D-2 | `phase1_gate.py` 侧不回显自己传入的 `linked_issue` (D2 代价的另一半) | 补它要动 `phase1_gate.py`, 属显式非目标 `:118`; 已成文为已知限 (FIX-07), 由母 Spec §2.3 闭合 |
| D-3 | `phase1_gate.py:1235` 的 `except Exception` fail-soft 吞异常 = 静默漏报 | 既有代码; 本 Spec 只在规则 2 侧要求实现不得依赖它 (FIX-04), 不改兜底本身 |
| D-4 | 「139 篇中 111 篇」这个数字 | **已复现, 口径订正**: 是 **111 次**不是「111 篇」(R1 aggregated `:39` 转述把「次」写成「篇」)。口径 = `Aria #124` / `aria-plugin #113` / `aria-plugin #122` 三个字面串出现次数之和, 语料 = 141 篇 proposal + `docs/` (R2/M2 原口径)。**仍不采纳为输入总体证据** (取自 prose 总体, S4 的换总体教训适用); 但**它指向的形态已单列为 F 族并进 SC-1**, 定性发现由此真正吸收。⚠️ **该复跑是 fact-check 镜头做的 (105 次), 我未独立复算, 见 U-4。** |
| D-5 | `collision.py:219-220` 自排除对 track_id 命名习惯的隐性依赖 | R1/QA 指出既有测试用 `mine`/`theirs` 规避; 是既有代码性质, 非本 Spec 范围 |

---

## 本轮引入的新表面 (未审, 已写进 FIX-15 清单)

1. 规则 2 的 `isascii() and isdigit()` 谓词 + **4300 位长度上界 + 强制 `try/except ValueError`** (FIX-04) — 全新, 承重字符级判据, **且新增了一条异常路径**;
2. 「每段各自 `str.strip()`」统一空白规则 (FIX-05) — 全新, **本轮唯一主动扩大匹配面的改动**;
3. M2 的「封闭重写 vs 语料决策」判据 + **三条封闭授权清单 + 判别性准则** (FIX-03) — 全新, 是**通用授权形状**, 最可能被下一版引用来放宽别的东西;
4. 六族表 + 三总体定义 (FIX-02) — 全新;
5. **6 条新 SC**: SC-5c / SC-6b / SC-8a / SC-8b / SC-8c / SC-9 (FIX-12);
6. rule6_note 的 14 行 baseline 实测表 + **逐 hunk 判定论证** (FIX-11) — 全新, 且是 **Rule #6 合规论证**;
7. `tests/fixtures/linked_issue_corpus.txt` 这一 committed fixture 的**内容口径本身**未定义 (FIX-10/SC-7 只说「见 SC-7」, 而 SC-7 说「见 fixture」——**这两处目前互指, 是我留下的一个循环, 见 U-3**);
8. FIX-09 的「零 delta 限存量回放 / yielded 变可达限未来输入」这对限定词 — 我本轮新加, 无任何镜头审过。

---

## 需要 owner / 主控裁的不确定项

**U-1 (中) — M4 的文件集该钉 250 还是 276?**
`openspec/*/*/*.md` (250) 只覆盖 `changes/<name>/` 与 `archive/<name>/` 两级, 漏掉 26 个更深层 md; `git ls-files` (276) 是全量。**没有原则性理由排除那 26 个**, 但文本里现有的 736 是 250 口径。我倾向**钉 250 + 写明「即 changes/ + archive/ 两级」**(零重算成本, 且数字只承载定性)。改 276 也对, 但要把 736 全部改成 745。**这是口径选择不是事实判断, 请主控定。**

**U-2 (高) — FIX-11 的 rule6_note 走方案 A 还是方案 B?**
A = 保留 `SKILL.md:176` 同步行, 前提句改成「逐 hunk 判定 ⇒ 仍落第一行」; B = 从 Impact 撤下 SKILL.md 行, 保「零 SKILL.md」原前提。我给的推荐文本是 A (CLAUDE.md 明写「同文件两性质并存时逐 hunk 判」, 该 hunk 确为纯事实勘正)。**但这是 Rule #6 的合规论证本身, 按 Rule #10 我不自行拍板。** 无论哪个方案, FIX-11 与 FIX-13 必须同批落地。

**U-3 (中) — SC-7 fixture 的内容口径谁来定?**
FIX-10 (D1) 说「口径见 SC-7」, FIX-12 (SC-7) 说「fixture 是 D1 的证据载体」——**两处互指, 没人真的定义了 fixture 该装什么**。这正是 memory `feedback_verify_predicate_inputs_exist` 点名的形状 (公式打磨到位, 它要判的输入不存在)。**建议在 Phase B 前由主控写死**: 至少含六族各 2 例 + SC-5/5b/5c/6/6b 的全部字面值 + R2 那 18 元的可复原部分。我不代拟。

**U-4 (低) — D-4 的 105 次我未独立复算**
fact-check 镜头报「2026-08-04 复跑 = 75+16+14 = 105 次」。我复算了它的**结论方向** (该数字取自 prose 总体, 不入输入总体证据面) 但**未复跑那三个计数**。若要写进文本, 请主控或下一席复跑一次。

**U-5 (中) — 六族分族规则对 `Forgejo [#137]` 的归属是语义判断, 不是结构判断**
`Forgejo [#137](…)` 与 `aria-plugin [#95](…)` **结构上完全同形** (裸 token + 空格 + 链接)。我把前者归 D (无 repo 段)、后者归 F (裸仓名 + 空格), **依据是「Forgejo 是平台名不是仓名」这一语义知识 —— 一个纯结构的解析器区分不了**。⇒ 若按纯结构分, F 族是 **5** 不是 2, D 族是 **1** 不是 4。**这直接影响 F 族「复制源总体 2」这个数字, 也影响 SC-1 第四元的现实频次论证。** 我按语义分 (与 R2/M8 点名的「裸仓名+空格」原意一致), 但**这条我拿不准, 请 owner 定**; 定完后表下须加一句分族规则的成文说明, 否则下一轮读者会重算出不同的数。

**U-6 (低) — 「141 篇中 12 个字段值」的 12/11 口径**
12 是**字段行数**, 其中 1 行是本 Spec 自己的「无」⇒ 真正带值的是 **11**, 而族表合计恰好是 11。**三个镜头都用了「12 个字段值」这个说法。** 我在 FIX-02 里按「12 个字段行 / 11 个带值」分开写了。若主控认为这属过度精确, 可退回「12」但须在族表下注明合计为何是 11。