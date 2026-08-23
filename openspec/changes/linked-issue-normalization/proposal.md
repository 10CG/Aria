# Proposal: linked-issue-normalization

> **Status**: 📝 **Draft (A.3 done, post_planning 未收敛)** — post_spec R1/R1′/R2′/R3′ 四轮 (均 REVISE, 算法本体零问题) → owner 2026-08-07 切分交付面/审计史 → A.2/A.3 2026-08-08 → post_planning R1→R4 全 FAIL (`max_rounds=4` 耗尽, 拐点形态) → owner 2026-08-22 加 1 轮 R5 (两席新鲜眼睛) → **R5 FAIL (2C+7M, 全为 fix 副产品)** → **owner 2026-08-23 裁定: 修 R5 九条后 override 进 Phase B.1** (Rule #10 留痕见审计轨 §10; 下一步 B.1 分支 + claim)
> **Created**: 2026-08-02 | **重构**: 2026-08-07 (owner 裁定: 交付面与审计史切开)
> **Spec Level**: **3** (原 2; R3′ 因 Q5 的 AB 任务需 `tasks.md` 承载而升级 — 单域 — `lib/collision.py` 的一个比较谓词 + 一个导出单元)
> **关联 Issue**: 无
> **代码落点**: `aria/` 子模块 `skills/state-scanner/`; Spec 落主仓 (Rule #5)
> **ship target**: aria-plugin v1.67.0 (MINOR — 行为面扩大)。*2026-08-22 改: 原写 v1.66.0, 已被 #137 占用; 1.66.x 现已到 v1.66.4 (并发轨 #152 预占 v1.66.5)。按本 Spec 自判 MINOR ⇒ v1.67.0; **若 owner 改判 PATCH (谓词 bug 修复) 则为 v1.66.6, 请复议**。2026-08-23 Phase B 中并发轨 #152 已 ship **v1.66.5** (aria `a0fe720`), 本轨 feature 分支已 merge 之 (`394cffd`) ⇒ 基线 = 1.66.5, CHANGELOG 新条目接在 [1.66.5] 之上。*

> **📌 本文件只规定「要建什么」。** 「规定是怎么来的」(三轮审计轨迹 / 总体定义与判族 / 未审表面清单 / 跨 Spec 裁定史 / 全部订正留痕) 已于 2026-08-07 整体移出至 **[审计轨](../../../.aria/audit-reports/linked-issue-normalization-audit-trail.md)**。
>
> **⚠️ 该审计轨是 append-only 的, 且显式不维护与本文件的一致性。** 二者出现不一致时**以本文件为准**; 不得因审计轨的历史记述而回改本文件。这条切分是 R1′→R3′ 三轮的直接产物 —— 那三轮 26 条 major 里, 落在纯交付面的接近于零, 而 append-only 的审计叙事与交付面的强耦合正是缺陷生成机制本身。

---

## Why
### 缺陷 (R1 四席独立命中 + 主控实跑复验)

`aria/skills/state-scanner/lib/collision.py:217` 的 `linked_issue` 匹配是**裸字符串 `!=`**:

```python
if c.linked_issue != own_linked_issue:
    continue
```

而生产数据里**三个格式族并存**:

### 为什么这是 live 缺陷, 不是未来的事

**`linked_issue_overlaps` 已经在生产中被调用** —— `scripts/phase1_gate.py:1233`, 由 Phase B 入口的认领路径经 CLI 触达 (`phase-b-developer/SKILL.md:88-93` 的 `[--linked-issue]`)。⇒ **该机制今天就在跑, 谓词一旦遇到跨格式输入就漏报。**

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

比较键 = `(normalize(repo_basename), int(number))`, 其中 `normalize` = 规则 1 的**每段 strip** + 规则 3 的 **`./_ → -` 译码** + **`casefold()`** 三者复合。

> **三者的施加顺序不影响结果 (R1′/backend 实证, 建议写作 `strip → 译码 → casefold`)**: 已扫描全部 **1,114,112 个 Unicode 码点**确认 `str.casefold()` 不产生也不吞噬 `#` / `/` / `.` / `_` / `-` / 空白 (0 命中); 并对 3019 个 basename (含 ß / İ / 连字 / 组合字符) 实跑 `{strip, 译码, casefold}` 全部 6 种排列做差分 —— **0 处不一致**。⇒ 实现可任意链式调用, 但**本 Spec 建议固定写作 `strip → 译码 → casefold`** 以便阅读与 review。

> **⚠️ 该键 ≠ R2 穷举验证过的那一版**。R2 验的是 `(repo_basename.casefold(), number)` —— **不含** strip、**不含**译码。⇒ **§审计资产继承 (a) 的免审范围只覆盖 R2 那一版键**; 本 Spec 现用键的三个分量里有两个是本轮新增, 全部在审计范围内。**读本节时不得把两者当成同一个键。**

1. **先判存在性**: 若字符串**不含** `#`, 直接判该值**不可解析** (即规则 4 枚举项 (i)), **不得**对其执行拆分。含 `#` 时按**最后一个** `#` 拆为 `left` / `number_str`;
   - **⛔ 实现不得对不含 `#` 的字符串执行无守卫的 unpack/下标取值 (R1′/C2, 与规则 2 对 `int()` 的要求同等严格)**: `'no-hash-here'.rsplit('#',1)` 返回单元素列表 ⇒ 解包抛 `ValueError: not enough values to unpack`, 下标写法抛 `IndexError`。**该异常不在规则 2 的 `try/except ValueError` 覆盖范围内** (规则 2 只包 `int()`), 会一路逃出函数被 `scripts/phase1_gate.py:1236` 的 `except Exception` 吞掉 —— 使**该次调用的全部** `linked_issue_overlap` 结果 (含已正确算出的其他命中项) 一并退化为 `[]`。
     > **⚠️ 这个失效面比本 Spec 要治的原缺陷更宽**: 原缺陷是「跨格式认领同一 issue 的双方互相认不出」(影响限于该 issue 双方); 此处是「**任意一条畸形 `linked_issue` 使全体 session 的重叠检测集体失明**」(影响全体, 直到该 claim 过期)。而 `--linked-issue` 是零格式校验的自由文本 CLI 参数, `lib/claim_schema.py:288-295` 的 `parse_claim()` 对 `linked_issue` 只做 `isinstance(str)` —— 一次键入疏漏 (如忘记带 `#`) 即原样写入共享的 `refs/aria/coordination`。**本 Spec 若不显式钉住这条守卫, 就是亲手引入一个新的「已装填未击发」击发点。** 回归护栏见 SC-10。
   - **空白处置的唯一规则 (R1/m1)**: 切分出的**每一段** (`left` / `number_str` / `org` / `repo_basename`) 在使用前**各自 `str.strip()`。无例外。** 后果: `10CG / aria-plugin#1` ≡ `10CG/aria-plugin#1`, `aria-plugin# 122` ≡ `aria-plugin#122`, `aria-plugin #95` ≡ `aria-plugin#95`。
   - **边界**: strip 只消除**每段首尾**空白; **段内空白既不删除也不译码** (`aria plugin` ≠ `aria-plugin`, SC-5c 钉死)。
   - **授权来源**: 本规则属规则 3 ⭐ 子项边界条款授权清单第 **(ii)** 条。*(⚠️ Q7-3 全称句 sweep 订正: 原写「它是本轮**唯一一条**主动扩大匹配面的改动」—— 三条授权重写 `casefold` / `strip` / `./_→-` **都**扩大匹配面, 「唯一」只在「R1-fix 那一轮新加的只有它」这个已过期的时间语境下成立。改为: 三条**各自**需要显式授权来源, 本条的来源是 (ii)。)*
2. `number_str` (已 strip) **可解析当且仅当** `number_str.isascii() and number_str.isdigit()` 为真 —— 即**非空、全为 ASCII `0`-`9`**; 否则该值**不可解析** (见 4)。解析为 **`int`** 后按十进制值比较 (故 `aria-plugin#007` ≡ `aria-plugin#7`)。**前导零不剥、不截断**。
   - **为什么必须钉到这个谓词 (R1/M3: 母 Spec 写「纯数字」, 抽出时漂成更宽的「能解析为非负整数」)**: `int()` 与 `isdigit()` 双向分叉, 逐值实跑 (CPython 3.11.2) —— `int('+7')==7` / `int('1_0')==10` / `int(' 122')==122` 而三者 `isdigit()` 全 False; 反向 `'１２３'.isdigit()` 与 `'²'.isdigit()` 为 True 而 `int('²')` **抛 ValueError**。⇒ 必须同时钉住 `isascii()` 与 `isdigit()`。
   - **⚠️ 长度上界**: 取 `limit = sys.get_int_max_str_digits()`; **仅当 `limit > 0` 且 `len(number_str) > limit` 时**判不可解析, 退回步骤 4 原串比较 (CPython 默认 `limit = 4300`)。
     > **`limit > 0` 这个前置判断不可省 (R1′/backend)**: `0` 是 Python 文档化的「**无限制**」哨兵值 (`sys.set_int_max_str_digits(0)` 后 `int('9'*100000)` 正常返回)。若照抄成裸的 `len > limit`, 在 `limit == 0` 时退化为 `len > 0` ⇒ 对**任意非空** `number_str` (含最普通的 `"7"`) 恒真 ⇒ 把全部正常输入判为不可解析、退回裸串比较 —— **本 Spec 要修的缺陷原样复活**, 且看起来「实现完全照抄了 Spec」。当前生产路径无风险 (`phase1_gate.py` 每次全新子进程), 但长驻进程或与调用过 `set_int_max_str_digits(0)` 的第三方库共享解释器时会触发。**且实现不得依赖 `int()` 不抛异常** —— `int()` 调用必须包在 `try/except ValueError → 判不可解析` 里。实测: `('9'*4301).isascii() and .isdigit()` 为 **True**, 而 `int('9'*4301)` 抛 `ValueError: Exceeds the limit (4300 digits)`; 该异常在生产路径上会被 `scripts/phase1_gate.py:1236` 的 `except Exception` 吞成 `out["linked_issue_overlap"] = []` (静默漏报, **与本 Spec 要治的病同形**)。
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
     >   **判别性准则 (R2′/backend-M1 订正 —— 原写「重写后仍能区分**任意两个**真实存在的仓名」, 那是个全称句, 而本清单第 (iii) 条自己就是反例)**:
>   - **否决判据 (硬)**: 重写**不得跨越分隔位、不得改变段数**。反例:「忽略全部非字母数字」把 `a-b` 与 `ab` 合并 ⇒ 跨越分隔位 ⇒ **不授权**;「把段内空格也译成 `-`」同理 (SC-5c 钉死)。
>   - **残余碰撞的处置 (软)**: 满足硬判据后**仍可能**有残余碰撞 —— 第 (iii) 条即如此 (`:128` 自认「若 `a.b` 与 `a-b` 恰是两个不同真仓, 译码会误配」)。此时**比照 D2 极性接受**: advisory 下误配 = 多一行告警, 由回显对方原串人工甄别。
>   - ⚠️ **本准则用于解释现有三条为何可接受, 不构成未来新增第四条的自动授权测试。** 任何新增仍须**独立 D 行论证 + owner 裁定**, 不得仅以「满足判别性准则」为由绕过「其余一律不授权」。
>
>   > **为什么必须这么改**: 原全称句严格读 ⇒ 连它要授权的第 (iii) 条都通不过 (判据反噬自身); 宽松读 ⇒ 实质等价于「任何可人工甄别的误配都行」, 而这个更弱的真实标准从未写出 —— 下一版作者可援引字面判据、暗用宽松读法, 审计者对照字面找不到抓手。**这条自陈是「最可能被引用来放宽别的东西」的一条, 后门原本开在它自己身上。**
     >
     > **已撤回的两条原理由 (R1/M2 判定不成立, 留痕)**: (a)「与 `derive_track_id` 对齐」—— `derive_track_id` **不消费 `linked_issue`** (全仓 grep 零命中), 且 track-id 派生是本 Spec 的**显式非目标**; (b)「不是理论风险」的原举证取自 **handoff prose 总体**, 与 SC-5 降级所用总体不同 —— 那正是 S4 指控 R2 的同一错误。**结论 (加译码) 保留, 理由已换。**
4. **不可解析的值** ⇒ **不参与归一, 退回原字符串精确比较** —— 绝不因解析失败就判「不匹配」而静默放行。**不可解析枚举 (母 §0 抽出时丢失, R1/m10 补回)**: (i) 无 `#`; (ii) `number_str` 不满足规则 2 的谓词; (iii) `repo_basename` 为空;
5. 匹配当且仅当 `repo_basename.casefold()` (经规则 3 译码后) 相等 **且** `number` 相等。**`org` 不参与匹配**。

> ## ⚠️ 两条**规范性但行为不可观测**的条款 (Q7-1 穷举变异测试实证, 2026-08-06)
>
> 穷举变异测试逐维度检验「每个维度是否至少有一条 SC 能杀死它的疏漏实现」时, 有两条条款的疏漏变异体**在任何输入上都产生与正确实现完全相同的行为** —— 对 **47,211** 个候选串做单值层全枚举 + 配对层抽样, **零差异**:
>
> | 条款 | 为什么不可观测 | 处置 |
> |---|---|---|
> | **规则 1 对 `left` 的 strip** (三个 strip 点里的**第一个**) | `org` 段**不参与匹配**, 而 `repo_basename` 在 `/`-split 之后**还会再 strip 一次** (第三个 strip 点) ⇒ 第一次 strip 的效果被第三次完全吸收 | **保留条款** (它让 `org` 段在未来被使用时是干净的), 但**不为它写 SC** —— 写了就是恒绿断言 |
> | **规则 2 的 4300 位长度上界** (D7) | 同条规则已**强制** `int()` 包 `try/except ValueError`, 而 `int()` 抛 `ValueError` 的**充要条件**就是超过该上界 ⇒ 两条路径产出**同一个**「不可解析」判决 | **保留条款** (它避免一次昂贵的大整数转换, 属**性能**而非正确性), 但**不为它写 SC** |
>
> **⇒ 这两条不是覆盖缺口, 是「无法被测试钉住的规范性条款」。** 显式成文的目的有二: (a) 防下一位读者为它们写测试 —— 那会得到一条**恒绿**的断言 (memory `feedback_false_green_dual_is_permanent_red`: 假绿的反面是恒红, 同样零信息); (b) 防有人以「没有测试覆盖」为由删掉它们 —— 它们有非行为价值。
>
> **⛔ 禁令 (母 §0 抽出时丢失, R1/m10 补回)**: 匹配**不得**使用模糊匹配 / 编辑距离 / 前缀包含 / 子串包含。比较只在上述归一键上做**精确相等**, 或在不可解析路径上做**原串精确相等**。二者之外无第三条路径。

> **⚠️ 举例约束 (R1/C1 防复发)**: R1 的 C1 根因是 SC-4 用了裸 `#007` × `#7` —— 按规则 3「`repo_basename` 空 ⇒ 不可解析」, 该例走的是步骤 4 原串比较, `'#007' != '#7'` ⇒ **不命中**, 与 SC-4 期望的「命中」直接冲突。
> **故本 Spec 全文的举例按路径分轴, 不按正例/反例分**:
> - 凡期望**经归一命中**的正例, **必须带 repo 段** (`aria-plugin#007` 而非 `#007`);
> - 凡期望**经步骤 4 原串精确比较命中**的正例, **必须**使用逐字相同的不可解析串 (如 `#5` × `#5`) —— 这类正例**不带 repo 段是规则 4 的直接推论, 不构成矛盾**;
> - 反例 (期望不命中) 不受 repo 段约束。

### 极性: org 轴 fail-toward-reporting, basename 轴是已知限

**org 轴**: 本机制是 advisory。漏报 = 静默无用 (昂贵, 已致 5 次重复劳动); 误报 = 多一行告警 (便宜, 人一眼可辨) ⇒ **fail toward reporting**, org 不参与匹配。代价: `otherorg/aria-plugin#122` 与 `10CG/aria-plugin#122` 会误配 ⇒ 需**回显双方 `linked_issue` 原始串**让人一眼判别。

> **⚠️ 该缓解在本 Spec 交付窗内只成立一半 (R1/M1, 实读复核)**: 对方那一侧**已经有** —— `collision.py:228` 逐字回显 `c.linked_issue` 未归一原串, docstring `:204-205` 已列该键。**自己那一侧没有** —— `scripts/phase1_gate.py` 的 `_claim_to_dict` (`:1119-1131`) 与 `_gate_result_to_dict` (`:1134-1169`) **均无 `linked_issue` 字段**, 而补它要动 `phase1_gate.py`, 那是本 Spec 的**显式非目标**。
> ⇒ **成文已知限 (与 basename 截断轴同一处置形式 —— 成文落 D4 + 本段, 不写进任何 SC 的期望列)**: 本 Spec **不**补自己那一侧。D2 的代价**永久只缓解一半**: 看得见对方写的是什么, **看不见自己传的是什么**。
>
> **⚠️ 归属已裁 —— 两边都不做 (Q1 = (c), owner 2026-08-06)**。原文写「该半缺口由母 Spec 闭合, 其 Impact 表已列 `phase1_gate.py`」, **该说法经 R1′/R2′ 两席各自去母 Spec 实读后证伪**: 母 Impact 表 `:347` 那行只列 `--include-terminal` / `_main():1232` 关键字参数 / `error` 带 `fetch_degraded` **三项**, **无** `linked_issue` 投影; 母 SC-1~19 **无一条**断言输出含该字段; 母 Spec `:289` 自陈行为类 SC「只能由 eval 覆盖, **不冒充结构化测试**」⇒ **两边都无 owner**。
> **裁定理由**: 该缺口的后果是「看不见自己传的是什么」, 而 advisory 的消费者是**人**, 人知道自己传了什么; 真正致盲的只有「转述该 JSON 的下游」—— 今天不存在的假设消费者。**用一个成文已知限换掉一条跨 Spec 依赖。**
> **凡引用「回显原串」作为代价缓解的落点, 一律带半幅限定 —— 已知落点: D2 要点列 (已带)、规则 3 的译码论据 (已带)。**

**basename 轴 (诚实标注, R2/M2)**: `repo_basename` 用**精确相等**, 对真实的**截断型**别名**恒漏** ⇒ **本机制在 basename 轴是 fail-toward-silence, 与 org 轴方向相反**。

> **basename 轴降为已知限的依据**: S4 与 R1-fix 分别实测 **复制源总体** 与 **已落盘总体** 上截断型别名各为 **0 实例** (两个总体各自为 0, 非跨总体推断)。*(该结论背后的「R2 24/10 口径之争」属审计叙事, 已移至 [审计轨 §8](../../../.aria/audit-reports/linked-issue-normalization-audit-trail.md)。)*

> **⚠️ 三处已知限的关闭时点全押在母 Spec 上, 且母 Spec 双阻塞 (R1′/tech-lead-m2)**: basename 截断轴 (D4) · 回显原串半幅 (X1) · `include_terminal` 归属 (X3) —— 三条的关闭都单向依赖 `a1-entry-claim-duplicate-work-guard`, 而它 `proposal.md:3` 实读为「⛔ 有两个阻塞性未决项, **不具备进 A.2 的条件**; 待 owner 裁」, **无任何条件性回退**。⇒ 本 Spec 可独立 ship (三条都是「已知限」不是「阻塞项」), 但**若母 Spec 长期不解封, 这三条会无限期悬空**。已列入 §闸门待裁 供 owner 知悉交付顺序风险。

**本 Spec 不解决 basename 截断型别名** (那需要别名表或书写强制, 属母 Spec 范围)。此处**只做三件事**: (a) **SC-5** 用纯行为断言把该轴的行为钉死 (`10CG/aria-orch#5` × `10CG/aria-orchestrator#5` **不命中**); (b) 该行为**作为已知限成文于 D4 与本段**, 防它被误读成「已覆盖」; (c) **不新增任何 surface 文案** —— 现有 `SKILL.md:176` 与 `collision.py` docstring 的同步措辞 (见 Impact 表, U-2 裁定方案 A 后两处都在范围内) **不得**出现「已穷尽核实 / 已覆盖全部别名」一类暗示。

### 存量数据不迁移

归一发生在**比较时**, **16** 条已有记录原样有效 (计数与 §Why 的已落盘总体一致)。改写共享 ref 是外向且难撤销动作, **非本 Spec 范围**。

### 接口面

`linked_issue_overlaps` 的签名与返回 schema **不变**; 只改内部比较谓词。⇒ Phase B 现有调用方**零改动**。

> **行为变化清单 (R1/M5: 「仅为原漏报现能报」不完整)**:
> 1. 跨格式同号的 claim 从不可见变为可见 (本 Spec 的目的);
> 2. **`yielded` 状态的 claim 会一并被归一后的谓词命中** —— `collision.py:210` 的 `_TERMINAL = ("done","abandoned","unknown")` **不含 `yielded`**。ref 现有 **3 条 `yielded` 且带 `linked_issue`** (均 `10CG/aria-plugin#110`, claimed_at `2026-07-14T11:26:09Z` / `12:32:51Z` / `17:10:32Z`, track_id 均 `state-scanner-stale-refs-false-parity`) 因此是**新的可命中目标**;
> 3. `int()` 与解析失败路径新增的异常面 (规则 2 长度上界), 会被 `scripts/phase1_gate.py:1236` 的 `except Exception` fail-soft 吞掉 —— **这条兜底本身就是静默漏报**, 已按规则 2 要求实现侧不得依赖它。
>
> **⚠️ 第 2 条不与 §Why 的「零 delta」冲突, 二者说的是不同东西**: 把现有 16 条逐条回放为**查询方**, 新旧输出 delta = **0** (那 3 条 `yielded` 与查询方共享 track_id, 被 `:219-220` 自排除); 但若**未来**有人以裸格式 `aria-plugin#110` 从**另一个 track_id** 认领, 新谓词会一次性浮出这 3 条 `yielded` (实测 old `[]` → new 3 条)。⇒ **「零 delta」限定于存量回放, 「yielded 变可达」限定于未来输入。两句都必须带这个限定词。**
>
> **⚠️ terminal 集合在本仓有三个互不相同的取值, 分布在 ≥7 个定义站点 (R1-fix 发现, R1′/code-reviewer-M4 补全站点)**:
> - `{done, abandoned, unknown}` — `collision.py:210` (本谓词用的就是它)
> - `{done, abandoned}` — `collision.py:307` · **`collision.py:155`** · `reconcile.py:62` · `worktree_manager.py:615` · `gc.py:213`
> - `{done, yielded, abandoned}` — `claim_lifecycle.py:317` + `:408` (另 `release_gate.py:219` 的 `choices` 同值)
>
> 三个取值两两不同 —— `unknown` 只在第一个里, `yielded` 只在第三个里; 穷举确认**无第四个 distinct 取值**。**其中 `collision.py:155` 就在本 Spec 唯一要改的那个文件里。**
> **⚠️ 且存在一处正面冲突**: `reconcile.py:55-60` 有注释逐字写着 `"yielded" is NOT terminal — it is a voluntarily PAUSED session`, 与 `claim_lifecycle.py:317` 把 `yielded` 当 terminal **直接矛盾**。这是「三个取值」背后的**真实语义分歧**, 比行号清单更值得进 issue。**属既有分歧, 非本 Spec 引入**; 本 Spec 只披露不改 (改它会动 `include_terminal` 语义, 已列非目标)。**建议单开 issue** (编辑清单 `post_spec-R1-fix-editlist-linked-issue-normalization.md` §本轮 deferred D-1 已记, 但当时只知两个变体)。

---

## 决策记录

| # | 决策 | 要点 |
|---|------|------|
| D1 | 比较键 = `(normalize(basename), int(number))` —— `normalize` = strip + `./_ → -` 译码 + `casefold()` (定义见 §归一规则) | **等价关系已被验证但证据不可复核**: R2 曾用 18 元语料穷举自反/对称/传递零违例, **该语料未入库、现已不存在**; R1/BA 在加入 `./_ → -` 译码后**用本 Spec 文本内的字面值重新穷举**, 同样零违例 —— 那是 R1 的实测, **不是可继承的 R2 资产** (R2 验的键是 `(repo_basename.casefold(), int(number))` —— **不含**译码、**不含** strip, 与 §审计资产继承 (a) 逐字同一写法)。⇒ **Q6 裁定后本 Spec 不再交付 fixture** (SC-7 与 §fixture 口径整节已移出) ⇒ **D1 的等价关系主张永久按「已论证、未留证」计, 并成文为已知限**。留证依据是 R1′/R2′ 两轮的独立 fuzz (backend 席: 400+ 串 / 45 元子语料 91,125 三元组 · 新守卫下复测 200,000 三元组, 均 0 违例) —— **审计报告可查, 但不入仓、不构成 committed 回归护栏**。若后续需要该护栏, 见 §移出范围 |
| D2 | `org` 不参与匹配 | advisory 下漏报昂贵、误报便宜 ⇒ fail-toward-reporting; 代价由「回显**对方**原串」兜 —— **仅半幅** (自己那一侧不在 CLI 输出中), 对转述该 JSON 的下游不成立。**Q1 裁定 (2026-08-06) = (c): 该半幅缺口成文为已知限, 本 Spec 与母 Spec 均不补** —— 理由见 §极性段 |
| D3 | 不可解析值退回**原串精确比较** | R2 复核: 两类不可能跨类相等, **论域被干净划分, 不破坏传递性** (此结论撤销了母 Spec R1-fix 自己的担忧) |
| D4 | basename 轴的 fail-toward-silence **成文为已知限**, 不在本 Spec 解决 | **首要依据 = 成本形状**: 截断型别名的处置需要「别名表」或「书写强制」, 二者都要**持续维护一份语料决策**, 与 D8 授权的三条**封闭规则**性质不同 ⇒ 属母 Spec 的 spike 范围。**次要说明**: S4 实测复制源总体 0 实例 + R1-fix 实测已落盘总体 0 实例 (两个总体各自为 0, 非跨总体推断) —— **但 0 实例只说明「不紧迫」, 本身不构成不修的理由**: §Why 对同一形状 (已落盘总体 0 实例) 给的是**相反**处置 (「修的是击发概率不是存量症状」)。⚠️ **不得逐字引用本行的「0 实例 ⇒ 已知限」形状去否定本 Spec 自身** (R1′/tech-lead-m1)。**「回显原串」半幅限度同挂本条, 见 §极性段** |
| D5 | 存量 ref 不迁移 | 归一在比较时发生; 改写共享 ref 外向难撤销 |
| D6 | 签名与 schema 不变 | Phase B 现有调用方零改动 |
| **D7** ⭐ | **可解析谓词** = `number_str.isascii() and number_str.isdigit()`; `limit = sys.get_int_max_str_digits()` 且 `limit > 0 and len > limit` 判不可解析; `int()` **必须**包 `try/except ValueError`; **不含 `#` 先判不可解析, 不得无守卫拆分** | 双向分叉逐值实跑 (CPython 3.11.2); 不可解析枚举三条 (无 `#` / 谓词不满足 / basename 空); **异常若逃逸会被 `phase1_gate.py:1236` 的 `except Exception` 吞成 `[]` —— 与本 Spec 要治的病同形, 且波及整批而非单条** (R1′/C2)。`limit > 0` 前置不可省 —— `0` 是官方「无限制」哨兵 (R1′/backend) |
| **D9** ⭐ | **归一以可导出纯函数交付**: `lib/collision.py::normalize_linked_issue(value: str) -> tuple[str, int] \| None`; `None` 与规则 4 的不可解析枚举**一一对应** | **Q2 裁定 (owner 2026-08-06) = (a) 导出**。母 Spec §2.1 (`:117`) 逐字规定 track-id 派生的 `basename`「经前置 Spec 归一 (含 S5 的 `./_ → -`)」⇒ 需要可 import 的单元。**成本极低 —— 该函数无论如何都要写, 本条只决定它是不是私有**; 不导出的代价是母 Spec 重实现一遍字符级算法, 而把算法钉到字符级的全部理由正是防这个 (memory `feedback_spec_underdetermination_two_implementer_test`)。返回契约由 SC-12 钉住。**注**: 本 Spec 同批移出了 SC-8a/8b 两条冻结断言 (见 §移出范围), 而此处新增 SC-12 —— **二者不矛盾**: 前者冻的是既有私有函数的签名 (baseline 恒绿、零证据面、且与母 Spec 撞车), 后者钉的是**新公开 API** 被下游依赖的语义 |
| **D8** ⭐ | **归一只授权三条重写**: `casefold()` / 每段 `strip()` / `repo_basename` 内 `./_ → -`。判别性准则 = **硬否决判据「不跨越分隔位、不改变段数」+ 软处置「残余碰撞比照 D2 极性接受」** (R2′/backend-M1 订正 —— 原写「重写后仍能区分**任意两个**真实存在的仓名」是全称句, 被本条自己的第 (iii) 项反证) | 本 Spec 全文**最可能被下一版引用来放宽别的东西**的一条 (§审计资产继承 自陈), 故必须有独立 D 行而非只藏在规则 3 的引用块里。反例逐字留档: 「忽略全部非字母数字」把 `a-b` 与 `ab` 合并 ⇒ 跨越分隔位、改变段数; 「段内空格也译 `-`」同理 ⇒ **均不在授权范围** (SC-5c 钉死) |

**Rule #6 (rule6_note)**: 改动面 = `lib/collision.py` 的一个内部比较谓词 + 导出单元 + 其测试 + **三处纯描述性文档同步** (`collision.py` docstring `:182-206`、`claim_schema.py:107-114` 的字段文档、`SKILL.md:176` 的括注); **零 `description` / 零 frontmatter / 零运行时指令流程变更**。

**⛔ 按 hunk 分两路 (Q5 裁定, owner 2026-08-06) —— 本条是本 Spec 的 Rule #6 唯一结论, 不得从别处推出相反结论**:

| hunk | 判据 | 处置 |
|---|---|---|
| `collision.py` docstring `:182-206` · `claim_schema.py:107-114` | 纯 Python docstring, 零 AI 指令面 ⇒ 判据表**第一行「描述性 (schema / 字段 / 命令 / 勘正)」** | **substitute: SC 级 baseline-failing 结构化测试替代** (证据面见下方 baseline 表)。与 v1.65.2 (#124) 同一判据路径 |
| **`SKILL.md:176` 的括注** | 属「行为变更后的语义追加」, **落不进** `standards/conventions/skill-benchmark-exemption.md` §2 具名的三个子类型 (溯源注释 / 行号勘正 / 术语修正) ⇒ 覆盖外分支 | **⛔ Phase B 照跑 AB (`/skill-creator`), 不申请豁免、不走 substitute。** 依据: 该 convention §4 明写「AI 不可以在决策表之外自创理由…落进『拿不准』格时**默认照跑**」 |

**⚠️ AB 的时点与落地载体**: AB 测的是该 hunk 的行为影响, 而 hunk 是 Phase B 交付物 ⇒ **AB 在 Phase B 实施该 hunk 之后、发版之前跑**。**本 Spec 为此升 Level 3, 该任务写进 `tasks.md`** (原 Q5 裁定要求「进 tasks.md」而本 Spec 当时是 Level 2 无该产物 —— R3′ 两席命中, 此处一并解决)。

**不申请豁免。**



**baseline 实测结果 —— ✅ 已实跑留证 (2026-08-05 首测, 2026-08-07 复跑)**:
> **留证 artifact**: [`.aria/repro/sc-baseline-linked-issue-normalization.py`](../../../.aria/repro/sc-baseline-linked-issue-normalization.py) —— 自包含、stdlib-only、只读、目标路径走 argv。复现:
> ```
> python3 .aria/repro/sc-baseline-linked-issue-normalization.py aria/skills/state-scanner
> cd aria/skills/state-scanner && python3 -m pytest tests/test_release_by_track.py \
>     -k "TestLinkedIssueOverlaps or TestPhase1GateLinkedIssueCli" -q     # 既有测试回归
> ```
> **结果: 15/15 与下表逐格一致** (Q6 缩范围移出 SC-7/8a/8b/8c/9 后, 表内为 SC-1/1b/2/3/4/5/5b/5c/6/6b/10/11; 全量套件另由 `run_all_tests.sh` 承担回归)。
> **脚本自带三重 fail-closed 守卫**: (a) **从本文件现场解析** baseline 表, 解析不到即 `sys.exit` —— **不回退硬编码** (R1′/tech-lead-m3: 此前它把表手抄成常量, 本文件改了它不会红 —— 而本 Spec 却对 SC-7 fixture 强制要求漂移守卫。**对别人强制的守卫必须施加给自己**); (b) **双向**漂移检查 (脚本测了表里没有的 / 表里有脚本没测, 两个方向都红; SC-8c 因由 pytest 另测而**显式豁免**, 非静默忽略); (c) 「实测红集合 == 声称证据面」不符即 exit 1。
> ⇒ owner 2026-08-02 裁定 (`db2e983`) 要求的「substitute 须**实证而非声称**, 全部实跑」**在 A.1 阶段即已闭环**, 不再是 Phase B 的待办。
> *(下表原署名「R1 三席 + R1-fix 起草者 + R1-fix 综合者三方独立复跑」—— 三次复跑均**无留证 artifact**, 即「声称已跑」而不可复核。本次实跑证实其结论正确, 但**结论正确不等于当时留了证**; 这条区别正是本 Spec 要治的病的同一形状。)*

| SC | baseline | 性质 | 算进 substitute 证据面? | 取证方式 |
|----|---------|------|---|---|
| SC-1 | **红** | 主判据 (跨族归一) | ✅ | 实跑生产 `linked_issue_overlaps` |
| **SC-1b** ⭐ | **红** | 主判据 (`/`-split 后的第三次 strip) | ✅ | 实跑生产 `linked_issue_overlaps` |
| SC-2 | 绿 | 负控 (不同仓不得命中) | ❌ | 实跑生产 `linked_issue_overlaps` |
| SC-3 | **红** | 主判据 (org 不参与) | ✅ | 实跑生产 `linked_issue_overlaps` |
| SC-4 | **红** | 主判据 (int 比较 + 段首尾空白 strip) | ✅ | 实跑生产 `linked_issue_overlaps` |
| SC-5 | 绿 | 已知限 (截断型不归一) | ❌ | 实跑生产 `linked_issue_overlaps` |
| SC-5b | **红** | 主判据 (`./_ → -` 译码) | ✅ | 实跑生产 `linked_issue_overlaps` |
| SC-5c | 绿 | 负控 (段内空格不译码) | ❌ | 实跑生产 `linked_issue_overlaps` |
| SC-6 | 绿 | 回落语义 (原串比较) | ❌ | 实跑生产 `linked_issue_overlaps` |
| SC-6b | 绿 | 边界负控 | ❌ | 实跑生产 `linked_issue_overlaps` |
| **SC-10** ⭐ | 绿 | **护栏 (防修复自身引入的回归)** —— 现状是裸 `!=`, **根本没有拆分动作**, 那条异常路径不存在; 它防的是**新实现**的病 | ❌ | 实跑生产 `linked_issue_overlaps` (混合批次) |
| **SC-11** ⭐ | **红** | 主判据 (取最后一个 `#` 的切分方向) | ✅ | 实跑生产 `linked_issue_overlaps` |
| **SC-9** ⭐ | 绿 | **D2 极性论证的唯一守护** (现状即回显原串; 本条防修复顺手改掉它) | ❌ | 实跑生产 `linked_issue_overlaps` |
| **SC-13** ⭐ | **红** | 主判据 (casefold 维度, Q7-1) | ✅ | 实跑生产 `linked_issue_overlaps` |
| **SC-14** ⭐ | 绿 | **护栏 (防修复自身丢掉 number 条件)** —— 现状裸 `!=` 本就不把不同号判同, 该风险由**修复**引入 | ❌ | 实跑生产 `linked_issue_overlaps` |
| **SC-15** ⭐ | **红** | 主判据 (`/` 取最后一段的切分方向, Q7-1) | ✅ | 实跑生产 `linked_issue_overlaps` |

⇒ **substitute 的证据面 = SC-1 / SC-1b / SC-3 / SC-4 / SC-5b / SC-11 / SC-13 / SC-15 八条 baseline-failing** (R1′ 新增 SC-1b 与 SC-11 后由四条扩到六条, 实测); 其余为负控 / 已知限 / 回落语义 / 冻结断言 —— 它们锁住「修复后不应退化」的行为, 有价值但**不能算进 substitute 的证据面** (负控恒绿是正确的, 不是证据)。
**⚠️ 两处订正留痕**:
1. 原文的「SC-1~6 均在现状代码上可红」经三方实测不成立, 已按实测改写。
2. **原文另写「SC-7 / SC-8a / SC-8b 结构上不可能由调用该函数测得」—— 该全称句被本 Spec 自己的 artifact 逐字证伪** (R1′ **三席独立命中**)。**Q6 缩范围后这三条 SC 已整体移出 (见 §移出范围), 该全称句连同它的适用对象一并消失。** 留痕于此以记形状: 那句话写在一段以「须实证而非声称」为前提的文字里, 而它自己声称了一个未实测的范围。
   > 这一处的形状值得记: 该段紧接着就在批评「保留全称句 = 在引用『须实证而非声称』之后声称一个未实测范围」, 而**它自己那句全称句正是同款**。修法与被修对象出自同一次编辑。

**⚠️ 上述「语料替换未披露」问题已随 Q6 缩范围消解**: SC-7 与其 fixture 整节已移出本 Spec (见 §移出范围), 不再有「表内规定 fixture 而 artifact 用内联串」的落差。

> **框定合规 (owner 2026-08-02 裁定 `db2e983`)**: 本条走 **substitute 框定** —— 判据表某一行 + 对应处置, **不**声称「Rule #6 不适用 / Rule #10 白名单第四类」。owner 该次裁定确立: **提供 substitute 与声称「不适用」逻辑上二选一**, 前者才对 (先例 `openspec/archive/2026-06-19-secret-guard-exfil-coverage-iteration/`)。**substitute 须实证而非声称** —— **SC-1 / SC-1b / SC-3 / SC-4 / SC-5b / SC-11 / SC-13 / SC-15 八条**的 baseline-failing 状态**已于 2026-08-05 实跑留证**, artifact 见上方 baseline 表 (`.aria/repro/sc-baseline-linked-issue-normalization.py`, 14/14 一致)。该裁定要求的「全部实跑, 非声称」**已满足**, 非 Phase B 待办。

> *(订正留痕: 本段原写「SC-1~6 的 baseline-failing 状态」—— 与上方 baseline 实测表直接矛盾 (SC-2/5/6 实测为绿)。**该假声明在同一节内出现两次, 上方一处已由 FIX-11 改掉, 这一处编辑清单未点名、险些残留** —— 属「多簇 fix 互相拆台」的同一形状, 由 R1-fix 落盘后的交叉一致性检查抓到。)*

---

## Success Criteria

| SC | 场景 | 期望 | 怎么会红 |
|----|------|------|---------|
| **SC-1** | 四族两两配对 (6 对): `aria-plugin#122` × `10CG/aria-plugin#122` × `10CG/aria-plugin #122` × `aria-plugin #122` (**第四元 = 裸仓名 + 空格, 无 org**) | **两两互相命中** | 现状裸 `!=` 在**全部 6 对**上必红 |
| **SC-1b** ⭐ | **`/` 两侧与整串首尾的空白**: `10CG / aria-plugin#122` × `10CG/aria-plugin#122` · `" 10CG/aria-plugin#122 "` (整串前后空白) × `10CG/aria-plugin#122` · `10CG/ aria-plugin #122` × `10CG/aria-plugin#122` | **两两互相命中** | **规则 1 要求三个切分点各自 strip; 本条是唯一覆盖第三个切分点 (`/`-split 之后) 的用例。** 「`#`-split 后 strip 了、`/`-split 后忘了」的实现 —— 恰好漏三次 strip 中的第三次 —— 在此必红, 而它对 SC-1/SC-4 全部子用例**零发红** (R1′/C1 变异测试实证) |
| **SC-2** | `10CG/Aria#147` × `10CG/aria-plugin#147` (同 org 同号, **不同仓**) | **不得**命中 | 「只比 number」的退化实现必红 |
| **SC-3** | `10CG/aria-plugin#1` × `otherorg/aria-plugin#1` (**两侧都有 org 且不同**) | **命中** (org 不参与) | 能区分「org 不参与」与「两侧有 org 才比 org」两种实现 (SC-1/SC-2 均不能)。**⚠️ 「唯一」已不成立 (Q7-3 全称句 sweep 实测)**: 本轮新增的 **SC-15 第二对** (`10CG/sub/aria-plugin#5` × `othergroup/aria-plugin#5`, 两侧都有 org 且不同) **同样杀得死该变异体** ⇒ 两条互为冗余覆盖, **可互为回归护栏但不可据「唯一」论证不可删** |
| **SC-4** | (a) `aria-plugin#007` × `aria-plugin#7`; (b) `aria-plugin# 122` × `aria-plugin#122` | **两组各自命中** (number 按十进制值比较; **前导零与各段首尾空白不影响**; 段内空白不归一, 见 SC-5c) | 字符串比较必红; 不 strip `number_str` 的实现在 (b) 上必红 |
| **SC-5** | `10CG/aria-orch#5` × `10CG/aria-orchestrator#5` (**截断型**别名) | **不命中** | 锁定 basename 轴 fail-toward-silence。*(该结果作为已知限成文于 D4 + §极性段, **不写进本列** —— 「期望列写『被记为已知限』」是循环定义, R1/minor 已判)* |
| **SC-5b** ⭐ (spike S5) | `10CG/10cg.local#20` × `10CG/10cg-local#20` × `10CG/10cg_local#20` (**分隔符型**别名, 真实仓) | **两两命中** | 只做 casefold 的实现必红。**与 SC-5 是两类**: 分隔符型**能**归一, 截断型不能 —— 两者处置不同, SC 须分开钉 |
| **SC-5c** ⭐ | `10CG/aria plugin#1` × `10CG/aria-plugin#1` (**段内空格**) | **不命中** | 把段内空格也译成 `-` 的**过宽**实现必红 (钉住规则 3 边界清单只授权三条重写) |
| **SC-6** | 不可解析值的**显式配对**: (a) `#5` × `#5` ⇒ **命中**; (b) `#5` × `#7` ⇒ 不命中; (c) `10CG/#7` × `otherorg/#7` ⇒ **不命中** (原串不同, 尽管归一后会同键 —— **D3 论域划分的承重断言**); (d) `no-hash-here` × `no-hash-here` ⇒ **命中**; (e) `repo#abc` × `repo#abc` ⇒ **命中** | 全部走步骤 4 **原串精确比较**; **不抛异常**; **不因解析失败判「不匹配」** | 解析失败即 `return False` 的实现在 (a)(d)(e) 三个自配对上必红 |
| **SC-6b** ⭐ | `number_str` 边界**配对**: `aria-plugin#+7` × `aria-plugin#7` / `aria-plugin#1_0` × `aria-plugin#10` / `aria-plugin#１２３` × `aria-plugin#123` / `aria-plugin#²` × `aria-plugin#2` 四对; 外加四个左值**各自与自身配对**; 外加 `aria-plugin#<4301 个 9>` 与自身配对 | 四对**均不命中**; 五个自配对**均命中** (原串相同, 走步骤 4); **全程不抛异常** | 裸 `int()` 的实现在前三对上命中 ⇒ 红; 裸 `isdigit()` 的实现在 `#²` 上 `int()` 抛 ValueError ⇒ 红; 「判定在前、`int()` 在后且不 catch」的实现在 4301 位自配对上抛 ValueError ⇒ 红; 「解析失败即判不匹配」的实现在五个自配对上不命中 ⇒ 红 |
| **SC-10** ⭐ | **批次内异常隔离**: `claims = [良构且应命中的 A, `linked_issue` 为 `"no-hash-here"` 的畸形项, 良构且应命中的 B]`, 查询方传良构值 | 返回**仍含 A 与 B 两项**; **全程不抛异常** | 照规则 1 字面直译且**不加存在性守卫**的实现在此抛 `ValueError`/`IndexError` ⇒ 红。**这是全表唯一构造「一条畸形 + 数条良构」混合批次的用例** —— 其余 SC 全部只用单条或自配对 claims 列表, 抓不到「一条坏值毒死整批」这一更严重形态 (R1′/C2) |
| **SC-13** ⭐ | **`casefold` 维度** (Q7-1 穷举变异测试): `10CG/Aria-Plugin#122` × `10CG/aria-plugin#122` · `ARIA-PLUGIN#5` × `aria-plugin#5` | **两组均命中** | **漏掉链式三步最后一步 `.casefold()` 的实现必红。** 在本条之前, 该维度**零覆盖** —— 变异体在全部 SC 上零发红 |
| **SC-14** ⭐ | **`number` 相等这一必要条件** (Q7-1): `aria-plugin#122` × `aria-plugin#7` · `aria-plugin#122` × `aria-plugin#123` | **两组均不命中** | **比较键只用 basename、丢掉规则 5 的「**且** number 相等」的实现必红。** 在本条之前零覆盖; 且现有全部「不命中」用例都靠**不同 basename** 触发, 没有一条是「同 basename 不同 number」 |
| **SC-15** ⭐ | **`/` 的切分方向** (Q7-1): `10CG/sub/aria-plugin#5` × `aria-plugin#5` · × `othergroup/aria-plugin#5` | **两组均命中** (basename 取**最后一段**) | 规则 3「取最后一段」写成 `split` 而非 `rsplit` 的实现必红。**与 SC-11 (`#` 方向) 是姊妹条** —— R1′ 只堵了 `#` 那一半, 真实数据 0 实例但按 D4 的道理「0 实例只说明不紧迫, 不构成不测的理由」 |
| **SC-9** ⭐ | 命中条目的 `linked_issue` 值 | **回显未归一的原始串** (如 `10CG/aria-plugin #122` 原样, 不是归一后的 key) | 把归一结果写回该键的实现必红。**⚠️ 本条 R1′ 曾被移出、R3′ 恢复**: Q1 裁定「自己那一侧永不补」后, **回显对方原串成为 D2 fail-toward-reporting 的唯一缓解** —— 移出时的理由「与 D2 半幅配对, 配对对象消失」**因果反了** (拿掉一边使另一边承重变重)。且 `normalize_linked_issue` 返回 `(basename, number)` **丢弃 org** ⇒ 本字段是输出里**唯一**携带 org 的通道; 无本条则 Phase B 顺手把回显改成归一键即全绿, 而跨 org 误配与真命中在人眼里不可区分, D2 的整个极性论证 (「人一眼可辨」) 落空 |
| **SC-12** ⭐ *(baseline 期无法实测 —— `normalize_linked_issue` Phase B 才存在, 故无 baseline 行)* | **导出单元的返回契约** (Q2 裁定): `normalize_linked_issue(v)` 对可解析值返回 `(basename, number)` 二元组、对**全部三类不可解析值**返回 `None` —— 逐类各一例: 无 `#` (`no-hash-here`) · 谓词不满足 (`repo#abc`) · basename 空 (`10CG/#7`) | 如左 | 用异常 / 空串 / `(None, None)` 之类替代 `None` 的实现必红。**母 Spec §2.1 的 track-id 派生依赖 `None` 这一语义**, 不钉住它母 Spec 就得靠猜 |
| **SC-11** ⭐ | **多 `#` 值的切分方向**: `repo#7#8` × `repo#7#008` ⇒ **命中** (按最后一个 `#` 拆, `number_str` 为 `8`/`008`, `left` 同为 `repo#7`); `repo#7#8` × `repo#8` ⇒ **不命中** | 如左 | 用**第一个** `#` (`split` 而非 `rsplit`) 的实现必红。**规则 1「取最后一个 `#`」是为处置 E 族 markdown 锚点特意钉死的措辞, 而在本条之前全表与 G1–G5 无一要求语料含 2 个以上 `#` 的值 ⇒ 该措辞写反不会被任何断言察觉** (R1′/qa-M1) |

## 非目标

- **不改** `phase1_gate.py` 的 CLI / `run_gate` 签名 (本 Spec 只动 `collision.py` 内部谓词);
- **不做** A.1 入口认领前移 —— 那是母 Spec 的范围 (其 spike S1–S6 已完成、已据此重写为 v2, 现停在 Draft v2 待 owner 裁两个阻塞项);
- **不做** basename 别名归一 (D4 已成文为已知限);
- **不改写**存量 coordination ref 数据 (D5);
- **不动** `_TERMINAL` 的 skip 语义 (`include_terminal` 属母 Spec, 且 R3 已证其接线点描述有误);
- **不引入** track-id 形态变更 (母 Spec 范围, R3 判其有碰撞域风险);
- ⭐ **`include_terminal` 形参由 `a1-entry-claim` 引入, 不属本 Spec 变更面** (owner 裁定 2026-08-08)。
  > **本条按母 Spec `:172` 的逐字请求加入**, 关闭该跨 Spec 协调项。母 Spec §2.4 第 0 段要求给 `lib/collision.py::linked_issue_overlaps` 增 keyword-only 形参 `include_terminal: bool = False` (不加则其 `_main():1232` 传参直接 `TypeError`), 并建议**由母 Spec 承担该签名变更**、前置 Spec 只改内部谓词。
  > ⇒ **D6 与 §接口面 的「签名与 schema 不变」自此限定于本 Spec 的变更面**: 本 Spec 不改签名; 母 Spec 落地时追加 keyword-only 形参**不视为对本 Spec 的违反, 也不构成回归**。
  > *(R2′ 曾把该协调项记为「随 Q6 消失」—— 那只消掉了测试层冲突 (SC-8a 移出), 母 Spec 请求的这一句一直未落; R3′/tech-lead M7 命中。)*

---

## Impact

| 文件 | 变更 |
|------|------|
| `skills/state-scanner/lib/collision.py` | 归一比较谓词 (§What Changes 五步) + **导出纯函数 `normalize_linked_issue()` (D9/SC-12)**; `linked_issue_overlaps` 的签名与 schema 不变 |
| `skills/state-scanner/lib/collision.py` docstring `:182-206` | 文案同步 — 说明匹配按归一后的 `<repo>#<n>`, org 不参与; **措辞不得暗示「已穷尽核实 / 已覆盖全部别名」** |
| `skills/state-scanner/lib/claim_schema.py:107-114` (**R1′/code-reviewer-M1 补**) | `ClaimRecord.linked_issue` 字段文档同步 — 两处失准**且都被本 Spec 加剧**: (a) 「Two active claims with the **SAME** `linked_issue`」—— 归一后不再是 SAME 而是 same normalized key; (b) 「Two **active** claims」—— 实现跳的是 `_TERMINAL = (done, abandoned, unknown)`, **`yielded` 不在内**, 而 §接口面第 2 条正是要把 3 条 `yielded` 变为新可命中目标。**它是 schema 文档 (读者最可能当权威), 不改则 ship 后成为唯一仍描述旧语义的面 ⇒ 违 Rule #3。** hunk 性质为 Python docstring, 判据路径与 `collision.py` docstring 完全相同 |
| `skills/state-scanner/tests/test_release_by_track.py` (既有宿主) | 扩展 — **SC-1 / 1b / 2 / 3 / 4 / 5 / 5b / 5c / 6 / 6b / 10 / 11 / 12 / 13 / 14 / 15 / 9** (17 条); 既有 6 条 (`:206-247` 4 条 + `:527-575` 2 条) 逐字不改, 回归由全量套件承担 |
| `skills/state-scanner/SKILL.md:176` | 文案同步 — 「同 issue 不同 track-id 的『同一件事两个名字』」补「(按归一后的 `<repo>#<n>` 比较, org 不参与)」。**纯事实勘正 hunk, 见 rule6_note 的逐 hunk 判定** (U-2 裁定方案 A) |
| **发版同步面 (R3-fix 2026-08-08: 改为**版本引用点**口径 — 原「文件数」口径经 post_planning R1 Critical 实测漏 7 处)** | **普通引用文件 18 个引用点**: 主仓 14 (`README.md` badge + `Plugin Version:` 行 = 2 · `README.{zh,ja,ko}.md` 各 translated-from + badge + `Plugin Version:` 行 = 9 · `CLAUDE.md` 版本区间行 + 「版本:」行 = 2 · `VERSION` 子模块表行 = 1) + aria 侧 4 (`plugin.json` 1 · `marketplace.json` **2** 个 version 字段 · `aria/README.md` 1); **append-only 账本 2 个** (`aria/VERSION` / `aria/CHANGELOG.md`) 判据不同 —— 头部当前版本行 == SOT **且文件行数不减** (R4-fix/R5 统一口径; 原「旧值命中数不减」对部分 bump 恒红), 不做零命中; 外加主仓 **gitlink** (非文本引用)。**⛔ 两条 enabled custom check 不是机械兜底**: `m6-version-badge-match` 只比 `README.md` 的 badge, `i18n-readme-translation-currency` 只比 `translated-from` 标记 ⇒ **10 处** (R2-fix 写 7, R4 实算 10: 漏计 CLAUDE.md 2 + VERSION 1) 残留旧版本时二者仍全绿 = 假绿。齐备性判据见 `tasks.md` **5.11** 的双向断言。类级根因 (`CLAUDE.md:81` 同款错误清单) 已开 **Aria #177**。 |
| 版本号 | v1.67.0 **MINOR** (行为面扩大 —— 原本漏报的现在能报出来; rule6_note 引的先例 v1.65.2 是 PATCH, 因其为纯脚本修复无行为面扩大) |

测试基线: state-scanner 现 **1322** tests, 本 change 新增按 SC 子用例下界 **≥45**。全量跨 skill 套件须绿 (`run_all_tests.sh`)。

> **下界推导 (可证伪, 逐条从 SC 表数)**: SC-1 六对 **6** + SC-1b 三对 **3** + SC-2 **1** + SC-3 **1** + SC-4 两组 **2** + SC-5 **1** + SC-5b 三元两两 **3** + SC-5c **1** + SC-6 五配对 **5** + SC-6b (四对 + 五自配对) **9** + SC-10 **1** + SC-11 两配对 **2** + SC-12 三类各一 **3** + SC-13 **2** + SC-14 **2** + SC-15 **2** + SC-9 **1** = **≥45**。
> *(订正史: `≥12` (8 条 SC 旧表) → `≥35` (**加总算错, 应 36**, R1′ 两席独立命中) → `≥43` (R1′-fix 增 3 条 SC) → `≥38` (Q6 缩范围) → `≥44` (Q7-1 补 SC-13/14/15) → **`≥45`** (R3′ 恢复 SC-9)。**本行每次改 SC 表都必须重算 —— 已三次因漏改而失准。**)*

---
