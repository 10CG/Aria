# Proposal: linked-issue-field-availability

> **Status**: 📝 **Draft — 待 post_spec R1** (本文件 2026-08-25 首版, 未经任何审计轮; **不继承**母 Spec 的 R1/R2 轮次 — 那两轮审的是含旧 §1 的母文本, 本文件是新交付面)
> **Created**: 2026-08-25
> **Spec Level**: **2** (单域 — 一份跨项目模板 + 一处 SKILL.md 声明 + 一个 plugin 侧探针脚本 + 一条 check 注册; 无架构变更, 不出 `tasks.md`)
> **关联 Issue**: `无` — 本 Spec 从母 Spec 的 post_spec R2 簇 C-A / M-10 / M-2 与 R1 editlist FIX-06/07/08 拆出, 无独立 issue 号 (dogfood, editlist **FIX-19**: 本行写法本身就是本 Spec §3 抽取规则的合规输出, 已用规则原型实跑自校)
> **代码落点** (**三个仓**): `standards/` 子模块 `openspec/templates/proposal-minimal.md` (跨项目 SOT) + `aria/` 子模块 `skills/spec-drafter/SKILL.md` 与 `skills/state-scanner/scripts/linked_issue_field_probe.py` (**新建**) + 主仓 `.aria/state-checks.yaml` (注册) ; Spec 落主仓 (Rule #5)
> **母 Spec**: [`a1-entry-claim-duplicate-work-guard`](../a1-entry-claim-duplicate-work-guard/proposal.md) — 本 Spec 是 owner **2026-08-23「裁定 2: 方向 b 缩 scope」**拆出的两个小 Spec 之一 (另一个 = `sibling-spec-probe`)。拆分依据: R2 判定 **C-A**「§1 承重『抽取规则』defer 到 A.2 ⇒ check 上线恒红」是 **R1/C3 still-open** 且承重, 与 A.1 认领机制**没有共同的收敛面**; 母 Spec 主体只留 A.1 入口认领 + track-id 契约。

> **📌 「规定是怎么来的」已切出**: 实读与重测清单 (起草时全部实测命令与输出) 见 **[审计轨](../../../.aria/audit-reports/linked-issue-field-availability-audit-trail.md)**。四条声明: ① 本文件只规定「要建什么」; ② 审计轨 **append-only**; ③ 审计轨**显式不维护**与本文件的一致性, 二者不一致**以本文件为准**; ④ **不得**因审计轨的历史记述而回改本文件。

> **⚠️ 依赖方向 (逐字, 不得读成隐式前置)** — 与母 Spec `:92` 一带的声明同义, 两侧都成文:
> - **本 Spec 不是母 Spec 的阻塞前置。** 母 Spec 在「字段缺席」时退化为**零输入** —— `phase1_gate.py:1230` 的 `if args.linked_issue:` 是整块门控 (F-10), 无字段即整段不执行; 该缺口成文于**母 Spec §6**, 不假装覆盖。
> - **母 Spec 是本 Spec 的语义母体**: track-id / claim / `无` 的 CLI 实参语义一律引用母 Spec, 本 Spec **不自行重定义**。
> - ⇒ 两份可**任意顺序** ship。本 Spec ship 后母 Spec 主机制的**输入覆盖率**上升, 但母 Spec 的**正确性不依赖本 Spec**。

> **📌 本文件只规定「要建什么」。** 「规定是怎么来的」(全部实读命令与逐条输出 / 语料重测原始数 / 反例复跑核对 / 对抗夹具结果 / 与探针 Spec 的比对原始记录) 已整体移出至 **[审计轨](../../../.aria/audit-reports/linked-issue-field-availability-audit-trail.md)**。
>
> **⚠️ 该审计轨是 append-only 的, 且显式不维护与本文件的一致性。** 二者出现不一致时**以本文件为准**; **不得**因审计轨的历史记述而回改本文件。
>
> 切分依据 = 同批母 Spec / 探针 Spec 的同一刀 (仿已 ship 的姊妹 Spec `linked-issue-normalization` 于 2026-08-07 的 owner 裁定「交付面与审计史切开」, 见 [其审计轨](../../../.aria/audit-reports/linked-issue-normalization-audit-trail.md)); memory `audit-trail-not-in-spec`: **是 append-only 性质在造耦合, 不是「文档太大」**, 故处方是**切开不重写**。**本次切分是主控的流程判断, 非 owner 裁定 —— 已标请 owner 复议。**

---

## Why

母 Spec §瓶颈 的结论是: 主机制靠 `linked_issue` 匹配, 而**在制语料里这个输入基本不存在**。旧版引的 `141 篇 / 13 篇 / 9%` 是 **2026-08-04** 的计数, 已过期; R1 editlist FIX-06/07 里的 `12 篇 / 8.5% / changes 9 份 / 回填 6 篇` 同样过期。**本 Spec 全量重测**, 口径与命令逐字如下。

### 重测 — 终值 (主仓 `cc1bdef`, 测量时刻 `2026-08-25T02:02:42Z`, **三份拆分产物全部落盘后**)

> **⚠️⚠️ 规范是口径 (命令), 数字是当日观测。** 语料是**自修改**的 —— 每新建一份 Spec, `find`/`grep` 的结果就变一次 (本轮亲历: 三份产物落盘使总数 `147 → 149`、`changes/` `7 → 9`、松谓词 `15 → 17` 文件)。⇒ **本节表内的数字只是提交当日的观测值, 复核一律以下方命令为准, 不得把数字本身当规范。** FIX-06 那套 `141 / 12 / 8.5%` 之所以在 21 天里烂掉, 根因正是「把观测值写成了规范」——本 Spec 全文凡引数字处均适用本条。

```
$ find openspec -name proposal.md | wc -l                                        # 149
$ grep -rl '\*\*关联 Issue\*\*' --include=proposal.md openspec/ | wc -l           # 17   松谓词 · 文件
$ grep -rn '\*\*关联 Issue\*\*' --include=proposal.md openspec/ | wc -l           # 37   松谓词 · 行
$ grep -rlE '^> \*\*关联 Issue\*\*:' --include=proposal.md openspec/ | wc -l      # 17   严谓词 · 文件
$ grep -rnE '^> \*\*关联 Issue\*\*:' --include=proposal.md openspec/ | wc -l      # 19   严谓词 · 行
$ find openspec/changes -name proposal.md | wc -l                                # 9
$ find openspec/archive -name proposal.md | wc -l                                # 140
```

**两级假阳性剔除** —— 这一节是 §3 三条定位谓词各自的**实测依据**, 不是花絮:

**(1) 松 → 严** (`37 → 19` 行, 差 **18** 行)。差额按文件归属, 逐字命令与输出:

```
$ grep -rnE '\*\*关联 Issue\*\*' --include=proposal.md openspec/ \
    | grep -vE ':[0-9]+:> \*\*关联 Issue\*\*' | cut -d: -f1 | sort | uniq -c
      3 openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md
     11 openspec/changes/linked-issue-field-availability/proposal.md
      4 openspec/changes/sibling-spec-probe/proposal.md
```

**18 行全部落在三份「讨论该字段」的 Spec 里** (母 Spec / 本文件 / 探针 Spec), 无一是真字段。其中母 Spec 的那条最典型 —— 行首三个空格 + `> > ` (blockquote 深度 2), 是它旧 §1 里被引用的示例:

```
openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:88:   > > **关联 Issue**: [10CG/aria-plugin #122](https://forgejo.10cg.pub/10CG/aria-plugin/issues/122) (open; ...)
```

**(2) 严·行 → 严·文件** (`19 → 17`, 差 **2** 行)。**严谓词本身仍然过计** —— 多出的 2 行都在本文件内 (`:65` / `:86`), 是写在**围栏代码块里**的示例, 行首形态与真字段逐字节相同:

```
$ grep -rnE '^> \*\*关联 Issue\*\*:' --include=proposal.md openspec/ | grep linked-issue-field-availability
openspec/changes/linked-issue-field-availability/proposal.md:6    ← 真字段 (dogfood)
openspec/changes/linked-issue-field-availability/proposal.md:65   ← §1 引用的 markdown 链接形反例 (围栏内)
openspec/changes/linked-issue-field-availability/proposal.md:86   ← §1 的模板占位示例 (围栏内)
```

⇒ **形状匹配会在讨论该字段的 Spec 上假阳性** (与 memory `reference_secret_guard_false_positive_on_spec_docs` 同形), 且**两级都会**: 行首锚定只挡住第 (1) 级, 第 (2) 级须靠**围栏排除 + 取文档序第一条**。这就是 §3 的 E0 为什么是**三条**谓词而不是一条 —— 见 §3「⛔ check 不得被自己的文档触发」。

**当日观测值**:

| 口径 (规范) | 当日观测 |
|---|---|
| `find openspec -name proposal.md` | **149** (= `archive/` 140 + `changes/` 9) |
| `grep -rl` 松谓词 · 文件 / 行 | **17** / **37** |
| `grep -rlE '^> …'` 严谓词 · 文件 / 行 | **17** / **19** |
| 松→严 剔除的行 (全在 3 份讨论该字段的 Spec 内) | **18** |
| 严·行→严·文件 再剔除的行 (本文件围栏内示例) | **2** |
| **check 作用域** `openspec/changes/` | **9** 份 |
| §3 规则原型判定 · 全语料 | `NO_FIELD` **132** / `NO_TOKEN` **14** / `OK` **3** (合计 149) |
| §3 规则原型判定 · `archive/` 140 份 | `NO_FIELD` **126** / `NO_TOKEN` **14** / `OK` **0** |
| §3 规则原型判定 · `changes/` 9 份 | `OK` **3** (母 Spec `:12` / 本文件 `:6` / 探针 Spec `:6`) / `NO_FIELD` **6** |

> **⚠️ 与探针 Spec 的计数差异 = 总体不同, 不是矛盾** (memory `critique-repeats-error`: 反驳数字前必须并列总体/范围/计数法)。`sibling-spec-probe` 的 §实读清单 #14/#16 记 `147 篇 / 严谓词 14 行 / no_field 133`; 本节记 `149 篇 / 严谓词 19 行 / NO_FIELD 132`。**三项全部不同源**: (a) **总体不同** —— 它测的是 **committed `cc1bdef`** (三份拆分产物与母 Spec 的 FIX-19 字段都尚未落盘), 本节测的是**当前工作树**; (b) **范围不同** —— 它的层 0 无围栏排除, 故不产生「严·行 vs 严·文件」这一级差额; (c) **计数法不同** —— 它按「层」分类 (`no_field`/`url_fallback`/`no_token_no_url`), 本 Spec 按「合规裁决」分类 (`NO_FIELD`/`NO_TOKEN`/`BAD_TOKEN`/`OK`)。**两侧各自都对, 不可直接相减。**

### 承重事实: 现存字段**没有一条**能直接喂给归一

对严谓词命中的真字段行, 逐条把「冒号后整串 strip」喂给已 ship 的 `normalize_linked_issue()` (`aria/skills/state-scanner/lib/collision.py:178`, 实读见 §实读清单):

**结果 = 14/14 返回 `None`** (测于 dogfood 字段落盘前的 14 条存量字段)。原因是**真实写法是 markdown 链接形**, 例如:

```
> **关联 Issue**: [10CG/aria-plugin #122](https://forgejo.10cg.pub/10CG/aria-plugin/issues/122) (open; triage verdict=`confirmed`/`major`/`next-cycle`, ...)
```

⇒ 若不先定抽取规则: (a) check 上线**恒红**; (b) 若照抄字段值传 `--linked-issue`, 收到的是**整个 markdown 链接** —— 姊妹 Spec `linked-issue-normalization` 刚治好的格式病在上一层原样复现。**这就是 R2 的 C-A**, 母 Spec 三轮未收敛的那一条。

---

## What Changes

### §1 进模板 (SOT 归属 — 消解 M-2)

**SOT = `standards/openspec/templates/proposal-minimal.md`** (跨项目共享子模块)。实读该文件全文**无该字段**:

```
$ grep -c "关联 Issue" standards/openspec/templates/proposal-minimal.md
0
```

其头部 blockquote 现为三行 (`> **Level**:` / `> **Status**:` / `> **Created**:`), 本 Spec 在其后增一行:

```
> **关联 Issue**: `{<org>/<repo>#<n>}`
```

并在该模板既有的 `## Template Usage Notes` 段增一条: **无关联时逐字写 `` `无` ``, 不留空、不删行** —— 空与「忘了写」不可区分。

**第二处 = `aria/skills/spec-drafter/SKILL.md`**, 实读全目录 grep 该字段 **0 命中**:

```
$ grep -rn "关联 Issue" aria/skills/spec-drafter/ | wc -l
0
```

**二者关系 (M-2 要求成文)**:

| 维度 | `standards/openspec/templates/proposal-minimal.md` | `aria/skills/spec-drafter/SKILL.md` |
|---|---|---|
| 角色 | **SOT** — 模板正文的唯一权威 | **消费方** — 声明该字段为必填 + 指向本 Spec §3 的写法 |
| 现状 | 0 命中 (上方实测) | 0 命中 (上方实测) |
| 关系实证 | — | `:429` 逐字 `- [proposal-minimal 模板](../../../standards/openspec/templates/proposal-minimal.md)` ⇒ 该 SKILL 本就把模板委托给 standards |
| 覆盖面 | **全部**采用 Aria 方法论的项目 | 同上 (随 aria-plugin 分发) |
| 机械回声 | ❌ 无 (模板不自校) | ✅ **由 §4 探针承担** —— 探针与本 SKILL 同在 `state-scanner`/`spec-drafter` 所属的 plugin 分发面, 随 aria-plugin 一并到达采用方 |

> **⛔ 已知限 (M-2 的实质, 缩到实际边界, 成文不假装覆盖)** —— **本条已按 round-2 实读缩小**, 见下方「订正留痕」:
>
> 探针**脚本**随 aria-plugin 分发 (§4 D3 已改判宿主为 `aria/skills/state-scanner/scripts/`), 故采用方**拿得到**校验实现。**残余缺口只剩注册那一步**: 每个采用方须**自行在其 `.aria/state-checks.yaml` 里注册这条 check** —— 与既有的 `issue_cache_freshness_probe` / `coordination_probe` **完全同形** (二者同样是 plugin 分发脚本 + 项目侧注册, 实读 `.aria/state-checks.yaml:22` / `:235`)。
>
> ⇒ **未注册的采用方仍然没有机械回声**, 这一层本 Spec **不解决** (解法 = 让 `.aria/config.template.json` 或某个 init 流程自动写入该 check 条目, 属另一交付面, 且会改变「项目自主决定跑哪些 check」的既有语义)。**但它比「拿不到校验」弱得多**, 且与仓内既有的两条 plugin 侧 check 承担同一种残余风险 —— 不是本 Spec 独有的新缺口。
>
> > **📌 订正留痕 (round-1 → round-2)**: 本条原写「`.aria/` 不进 aria-plugin 分发面 ⇒ 机械回声只覆盖 Aria 仓」。该结论**基于一个错误的宿主选择**, 而非事实错误 —— `grep -rn "\.aria/probes" aria/` 零命中这条实读**本身仍然成立**, 但它只证明「`.aria/probes/` 不分发」, **不证明「check 无法分发」**。主控 round-2 实读指出 `.aria/state-checks.yaml` 里**两种宿主形态并存**且 plugin 侧已有两个实例 ⇒ 宿主选错了一档, 已按 D3 改判, 已知限随之缩小。**这是「把自己选错的路径写成了世界的限制」的形状**, 记于此防复发。

### §2 格式固定

**单一形态 `<org>/<repo>#<n>`**, 或表示「已核实无关联」的字面 `无`。写全 org 可让「org 不参与匹配」在人工判别时有据 (回显原串时看得出是不是同一个仓) —— 承姊妹 Spec 的 D2 极性。

> **⚠️ `无` 不是一个可参与相等比较的 token** (母 Spec §2 的 NEW-01, 逐字引母 Spec, 本 Spec 不重定义): `linked_issue_overlaps` 只在 `own_linked_issue` falsy 时短路, 而 `"无"` 是 **truthy** ⇒ 两份毫无关系的 Spec 只要都写 `无` 就会互相命中 overlap。⇒ **token 串为 `无` 时整个 `--linked-issue` 参数必须省略**, 见 §3 的 E6。

### §3 抽取规则 (钉到字符级 — 消解 C-A) ⭐ 承重

母 Spec 旧 §1 只写「从字段值中抽出的 canonical token」, 没给规则, 这正是 C-A 判「上线恒红」的原因。以下 **E0–E6 七条**是本 Spec 的承重交付面, **实现者零裁量**。

**E0 — 宿主行的定位** (三条谓词, 全部满足才算):

1. **行首锚定 (depth 恰为 1)**: 该行**逐字节**以 `> **关联 Issue**:` 开头 —— 行首**无任何空白**; `>` 之后**恰一个** U+0020; 字段名两侧各**恰两个** ASCII 星号; 冒号为 ASCII `:` (U+003A)。`>>` / `> > ` / 前置空格 / `>` 后零个或两个空格 / 全角冒号, **一律不算命中**。
2. **fenced code block 排除**: 自上而下扫描时维护一个开合布尔量, 凡匹配 ````^[ ]{0,3}(?:> ?)?(?:```|~~~)```` 的行**翻转**该量且**本身不参与谓词 1 的判定**; 布尔量为真时的行一律跳过。
   > **`(?:> ?)?` 这一段不可省 (本轮实测)**: 没有它, 写在**blockquote 内的围栏**里的示例 (即 `> ` + 三个反引号 开的块, 块内一行 `> **关联 Issue**: ...`) 会被判成真字段 —— 合成夹具 `j-bq-fence` 实跑 **`OK`(假阳性) → 加上后 `NO_FIELD`(正确)**。加它的**代价为零**: 在真实语料上加与不加的判定**差异数 = 0** —— **两次逐份对跑**, 147 份 (round-1) 与 **149 份 (round-2 重跑, 终值)** 均为 0。
3. **取文档序第一条**: 满足 1+2 的行可能有多条 (讨论该字段的 Spec 会举例), **只取第一条**, 其余一概忽略。

> **⛔ check 不得被自己的文档触发 (硬约束)** —— 本 Spec 与母 Spec 都在**讨论**这个字段, 都会举例; 一个只按形状匹配的 check 会把自己的例子当成自己的字段。真实实例见 §Why 的假阳性行 (母 Spec `:88`, 深度 2)。三条谓词各堵一类:
> - 谓词 1 堵**引用式加深** (`> > ` / 缩进后的 `> `);
> - 谓词 2 堵**代码块内的示例** (本文件 §3/§4 的全部示例都在 fence 内, 故对本文件零命中);
> - 谓词 3 堵**正文里的第二次出现** —— 真字段在头部 blockquote, 一定排在讨论之前。
>
> **⚠️ 明确不采用的替代**: 「只扫头部 blockquote 区」被**实测否决** —— 严谓词命中的真字段行里, `openspec/archive/2026-08-16-premerge-gate-branch-existence/proposal.md:61` 与 `openspec/archive/2026-08-16-premerge-gate-mainbranch-failclosed/proposal.md:45` 的字段落在**第 61 / 45 行**的超长头部 blockquote 内。任何「只扫前 N 行」的实现都会把这两条判成无字段 —— 假阴性, 且 N 取多少都是拍脑袋。**行首深度 + fence 状态 + 首条** 三条与行号无关, 不受长头部影响。

**E1 — 行内容**: 取该行去掉前缀 `> **关联 Issue**:` 之后的**剩余部分**, 含全部空白, **不 strip**。

**E2 — 冒号后第一个非空白内容必须是 inline-code span**: 剩余部分去掉前导 `[ \t]*` 后, **下一个字符必须是 U+0060 (`` ` ``)**。否则记 **`NO_TOKEN`** (不合规)。

> **为什么必须钉「第一个非空白」而非「第一个 code span」** —— 「第一个 code span」在**真实语料上抽错**, 实跑逐条 (坏实现取该行第一个 `` `…` ``):
>
> ```
> openspec/archive/2026-06-10-handoff-frontmatter-enforcement/proposal.md:4   -> 抽出 `partial-repro`   normalize=None
> openspec/archive/2026-06-11-audit-drift-guard/proposal.md:5                 -> 抽出 `confirmed`       normalize=None
> openspec/archive/2026-06-11-cross-worktree-handoff-discovery/proposal.md:4  -> 抽出 `confirmed`       normalize=None
> openspec/archive/2026-07-19-state-scanner-openspec-collector-false-green/proposal.md:14 -> 抽出 `confirmed` normalize=None
> openspec/archive/2026-07-22-state-scanner-gate-yaml-datasource/proposal.md:6  -> 抽出 `confirmed`     normalize=None
> openspec/archive/2026-07-31-phase-c-gate-path-coverage-not-applicable/proposal.md:6 -> 抽出 `confirmed` normalize=None
> ```
>
> **6 条**真实字段被抽成 triage verdict 而非 issue 号 (R1 editlist FIX-08 写于 2026-08-04 时记 4 条, **本轮重跑得 6 条**; 详见 §实读清单 的逐条核对 —— FIX-08 原列的第 1 条已因文件归档+内容改写而**不复现**, 其余 3 条复现, 另 3 条为本轮新增)。

**E3 — token 串**: = 该 code span 的内容 —— 从起始 `` ` `` 之后到**下一个** `` ` `` 之前的**全部字节**, 不含两端反引号, **不 strip, 不做任何加工**。若该行只有一个 `` ` `` (未闭合) ⇒ **`NO_TOKEN`**。

**E4 — token 元素**: token 串按 ASCII 逗号 `,` (U+002C) split, 每段各自 `str.strip()`。**术语二分**: code span 内整串称 **token 串**, split 后每段称 **token 元素** (消解母 Spec 旧文本里第 4/5 条互斥, editlist FIX-08(2))。

**E5 — 合法性**: token 串**合法当且仅当** —— 逐字节等于 `无` (单个 U+65E0, 无空白、无其他字符), **或** 每个 token 元素经 `normalize_linked_issue()` 返回**非 `None`**。任一元素返回 `None` ⇒ **`BAD_TOKEN`**, 并在输出里**点名**那个元素。

**E6 — `--linked-issue` 实参**: = **第一个 token 元素逐字节**, 不做二次加工。

> ## 🔴 K8 (R4) — E6 的门**太窄**, 未填写的模板 placeholder 会复现 NEW-01 且更易触发 (2026-08-27 补, 未经审计轮)
>
> **R4/type-design B-C1 实跑**: 本 Spec 自己给 SOT 模板的默认值是 `` `{<org>/<repo>#<n>}` `` (D8: 模板不要求自身过 E5),
> 它按 E5 判 **`BAD_TOKEN`**; 而 E6 **只对 `无` 设门** ⇒ **一份照模板新建、作者还没填 issue 号的 proposal**,
> 其 placeholder 会被**逐字节**喂进 `--linked-issue`。用真实 `linked_issue_overlaps` 实跑确认: **两份毫无关系的 Spec 互相命中**。
> ⇒ 这就是 NEW-01 (`无` 是 truthy 导致互相误报) 的原样复现, 而且**触发条件比 `无` 更弱** —— `无` 还要作者主动写,
> placeholder **什么都不做就中**。探针侧同时中招 (原串键相等)。
>
> **落版 — E6 的门从「等于 `无`」扩为按 verdict 分档 (穷尽四态)**:
>
> | verdict | `--linked-issue` |
> |---|---|
> | `OK` 且 token 串逐字节 `无` | **整个参数省略** (原 NEW-01 条款) |
> | `OK` 且为真 token | 传第一个 token 元素逐字节 |
> | **`BAD_TOKEN`** | **整个参数省略** + 消费面按「字段不合规, 本轮无 issue 输入」呈现 —— **不得**把脏串喂进匹配面 |
> | **`NO_TOKEN` / `NO_FIELD`** | **整个参数省略** (本就无 token 可传) |
>
> **一句话判据**: **只有 `OK` 且非 `无` 的那一格产生 `--linked-issue` 实参**, 其余三格一律省略。
> **新增 SC-9 (代码, CLI 全链路)**: 两份 proposal 的字段值都是模板 placeholder `` `{<org>/<repo>#<n>}` `` ⇒
> 二者经 A.1 认领后 `linked_issue_overlap[]` **互不命中** (因为都没传该参数);
> **怎么会红**: 把 `BAD_TOKEN` 的 token 串照传的实现 ⇒ 互相命中 ⇒ 必红。**baseline 必红** (今天没有 E0–E6 实现, 而朴素实现会照传)。
> **⚠️ 探针侧同批**: `sibling-spec-probe` 的层 1 对 `BAD_TOKEN` 取「层 1 ∪ 层 2 并集」——
> 其中层 1 的**原串键**同样会让两份 placeholder 相等。探针 Spec 须同批加一条: **原串键不得由 `BAD_TOKEN` 的常量串产生** (交叉点名)。

> ## 🔴 E0–E6 的**交付形态** — 可 import 的纯函数 (R3/C3, 主控 2026-08-25 补)
>
> **R3 判定**: 三条约束不可同时满足 —— 探针 Spec 声称 (逐字采纳本 Spec 的 E0) ∧ (不得内含第二份抽取实现) ∧ (不改 state-scanner);
> 而本 Spec round-1/2 的唯一宿主是**项目根扫描的 CLI check**, **无导出 API**, 且作用域写死 `changes/`;
> 探针要的是**远端 ref 上任意 blob** (含 `archive/`) 求四态 ⇒ **E0–E6 实现无归属**, 探针那句「姊妹非阻塞」在实现层为假。
>
> **处置 — 本 Spec 承诺把 E0–E6 交付为可 import 的纯函数** (先例: 已 ship 的姊妹 Spec `linked-issue-normalization` 的 **D9** 正是为同一理由把 `normalize_linked_issue` 从私有改为导出):
>
> ```python
> # aria/skills/state-scanner/lib/linked_issue_field.py  (新建模块, stdlib-only)
> def extract_linked_issue_field(text: str) -> "FieldVerdict":
>     """对一份 proposal 的**全文文本**求 E0–E6 四态。
>     输入是 str (不是路径) —— 探针要在远端 ref 的 blob 上调用, 没有本地文件。
>     返回 FieldVerdict(verdict, token_str, token_elements, line_no)
>       verdict ∈ {"NO_FIELD", "NO_TOKEN", "BAD_TOKEN", "OK"}
>     """
> ```
>
> - **输入是文本 blob 而非文件路径** —— 这是让探针能复用的**承重约束**: 探针读的是 `git cat-file` 出来的字节, 没有可 stat 的路径;
> - CLI check (`linked_issue_field_probe.py`) 与探针 (`sibling_spec_probe.py`) **都 import 它**, 二者都不自写第二份;
> - **作用域** (只扫 `changes/`) 是 **CLI check 的策略**, 不进纯函数 —— 纯函数只回答「这段文本的字段是什么态」;
> - ⇒ **Impact 表新增该模块行**; 探针 Spec 的「非阻塞」措辞同批订正 (它可先 ship 并全走层 2, 该函数 ship 后再接层 1)。
>
> **⚠️ 本条是 R3 之后新增的交付形态承诺 (未经审计轮) —— 请 R4 优先审。**
>
> ## 🔧 跨 skill import 的可运行模式 (R4/S-1 + R4/F-1 —— **本仓有先例, 审计席的「无先例」前提经主控实读推翻**)
>
> R4/code-architect 席判「跨 skill runtime import 在本仓无先例、且有反例」并据此给 Critical。
> **主控实读: 反例为真但不是禁令, 且先例确实存在** ——
> - **反例** (`skills/phase-d-closer/scripts/fetch_gate.py:111-112` 逐字): 「Mirrors state-scanner sync.py::_resolve_default_branch (replicated to keep phase-d-closer self-contained — **no cross-skill runtime import**)」。这是**那一处**的取舍 (为 self-contained 而复制), 不是仓级禁令;
> - **先例** (`skills/session-closer/scripts/handoff_autofill.py:403-407` 逐字, 主控实读):
>   ```python
>   # state-scanner/lib 是兄弟 skill 的包; 加其 skill root 使 `from lib.identity` 解析。
>   _ss_root = str(Path(__file__).resolve().parents[2] / "state-scanner")
>   if _ss_root not in sys.path:
>       sys.path.insert(0, _ss_root)
>   from lib.identity import get_identity
>   ```
>   同文件 `:48-51` 另有一处 (`.../state-scanner/scripts` + `from collectors.multi_remote import ...`)。
>   ⇒ **「兄弟 skill 的 lib 通过插入其 skill root 来 import」在本仓是已在生产运行的模式。**
>
> **⇒ 本 Spec 采用该模式, 逐字钉死** (不得指向 `.../state-scanner/lib` —— 那会因 `lib/collision.py` 的相对 import `from .claim_schema import ClaimRecord` 抛 `attempted relative import with no known parent package`, 姊妹 Spec 已实跑证实):
> ```python
> _SS_ROOT = str(Path(__file__).resolve().parents[2] / "state-scanner")
> if _SS_ROOT not in sys.path:
>     sys.path.insert(0, _SS_ROOT)
> from lib.linked_issue_field import extract_linked_issue_field   # 跨 skill 消费方 (sibling-spec-probe) 的用法
> ```
> **已知限 (成文)**: 该写法把 `state-scanner` 的 skill root 放进 `sys.path`, 于是**顶层包名 `lib` 与 `collectors` 被占用**。
> 若 `audit-engine` 将来自己长出 `lib/` 或 `collectors/`, 会与之**同名冲突** (`coordination_probe.py:80-83` 点名过同名包陷阱)。
> ⇒ **A.2 的一条显式约束**: `audit-engine` 内**不得**新建名为 `lib/` 或 `collectors/` 的顶层目录; 探针自己的 helper 一律放 `scripts/` 下并用模块名前缀。
> **降级说明**: R4/S-1 原判 Critical 的依据是「无先例 ⇒ 不可行」; 前提被推翻后, 真实缺陷是「**没给 import 代码**」—— 本段即补上, 严重度按 Major 处置。


**四态判定 (穷尽, 无第五态)**:

| verdict | 触发 | 处置 |
|---|---|---|
| `NO_FIELD` | E0 三谓词无任何行命中 | 不合规 |
| `NO_TOKEN` | E0 命中但 E2 不满足 (裸文本 / markdown 链接 / 反引号未闭合) | 不合规 |
| `BAD_TOKEN` | E2 满足但 E5 有元素解析失败 | 不合规, 点名元素 |
| `OK` | E5 满足 (含 `无` 分支) | 合规 |

> **⛔ 本规则**故意**不接受 markdown 链接形 —— 存量 14 条全判 `NO_TOKEN` 是预期, 不是缺陷。**
>
> 有人一定会问「既然真实语料 100% 是 markdown 链接形, 为什么不干脆兼容它」。答案是**写入侧与读取侧分工**, 两侧由两份 Spec 各管一半:
>
> | | 管什么 | 谁 | 对 markdown 链接形的处置 |
> |---|---|---|---|
> | **写入侧规范** | 新写的 proposal **应该**长什么样 + 机械回声 | **本 Spec** | **判 `NO_TOKEN` 并报 warning** —— 让作者改成 code span 形 |
> | **读取侧兼容** | 已经存在的 proposal **怎么读出 issue 号** | **[`sibling-spec-probe`](../sibling-spec-probe/proposal.md)** 的 §3 层 2「URL 回落」 | **从字段行里提 `/<org>/<repo>/issues/<n>` 片段**, 照样读得出 |
>
> ⇒ 存量 `archive/` 那 14 条判 `NO_TOKEN` **不影响任何人**: (a) 它们**不在本 check 的作用域内** (§5 D5, check 只扫 `changes/`); (b) 探针要读它们时走 URL 回落层, **不依赖本规则放宽**。**若本 Spec 为了「兼容」去接受 markdown 链接形, 反而会把脏串喂进 `--linked-issue` 实参** —— 那正是姊妹 Spec `linked-issue-normalization` 刚治好的病在上一层复现 (§Why 末段)。
>
> **⇒ 两侧的边界逐字**: 本 Spec 的抽取器**只产出** canonical token, 且**只有它**可以喂 `--linked-issue`; 探针的 URL 回落**只用于只读比对**, **绝不**产生 `--linked-issue` 实参 —— 该约束在探针 Spec 的 §3 层 2 已逐字成文 (「**⛔ 作用域分离是承重的**」), 本节与之**互为镜像**, 两侧任一被改都必须同批改另一侧。

> **📎 与 `sibling-spec-probe` 的术语对齐 (防 spec-underdetermination, memory `feedback_spec_underdetermination_two_implementer_test`)**
>
> 探针 Spec 的 §3 层 1 单方面声明「本 Spec 的抽取器返回**三态**: `TOKEN(s)` / 字面 `无` / `NO_TOKEN`」, 并在其「新表面」第 6 条自陈**未与本席交叉核对**、称之为「本轮最实的跨 Spec 风险」。本席已实读该文件, 逐条比对如下:
>
> | 项 | 本 Spec | `sibling-spec-probe` | 判定 |
> |---|---|---|---|
> | 定位规则 (行首) | E0 谓词 1: 逐字 `^> \*\*关联 Issue\*\*:`, 单个 `>` + 一个空格, 禁前导空白, 禁 `> >` | §3 层 0 (`:85`) 逐字同义 | ✅ **一致** |
> | 定位规则 (取第一条) | E0 谓词 3 | §3 层 0「文件中**第一条**」 | ✅ **一致** |
> | 定位规则 (围栏排除) | E0 谓词 **2** | **无该谓词** | ⚠️ **本 Spec 多一条**。在 `cc1bdef` 真实语料上两者判定差异 = 0 (探针 Spec 自己的三臂对照已证行首约束足够); 在**讨论该字段的 Spec** 上会分叉, 但因两侧都「取第一条」而真字段都在头部 ⇒ **当前无实际分叉**。**不要求探针 Spec 加这条**, 只点名 |
> | token 术语 | **token 串** (code span 内整串) / **token 元素** (按 `,` split 后每段) | 引用「canonical token 串」, 未用「token 元素」 | ✅ 兼容 (它不消费多值 split) |
> | `无` | E5 的合法分支 ⇒ verdict `OK`; `--linked-issue` **整参省略** | 独立成「层 1.5」, `layer` 枚举值 `"wu_empty"`, 比较键集合 ∅ 且不进 URL 回落 | ✅ **语义一致**, 命名空间不同 (本 Spec 是**合规裁决**, 它是**层枚举**) —— 两者不冲突, 此处点名对照 |
> | `NO_TOKEN` | 有字段行但冒号后首个非空白不是 code span | 同义 (其 `:103` 实测「canonical 合规 = 0 行」与本 Spec 的 14/14 一致) | ✅ **一致** |
> | `NO_FIELD` | 四态之一 | 它在**层 0** 处理为 `no_field`, **不进**其层 1 的三态契约 | ✅ 兼容 (分层位置不同, 语义一致) |
> | **`BAD_TOKEN`** | 四态之一: 有 code span 但**某个 token 元素**归一失败 | **无对应态** —— 其三态契约里没有这一格 | ❌ **实质差异, 需协调 (见下)** |
>
> **⇒ 唯一实质差异 = `BAD_TOKEN` 在探针的三态契约里无归宿。**
>
> **✅ 已闭环 (R3/M7 回灌, 主控 2026-08-25)**: 探针 Spec 已在其 §3「消解 SEAM-2」补了**逐格映射表**, 并对 `BAD_TOKEN` 采**层 1 与层 2 并集** —— 即**采纳**本席建议的「触发 URL 回落」那一半, 并在其上追加「层 1 已解析出的元素不丢弃」。其反例逐字: 字段行 `` `10CG/aria-plugin#122, TBD` `` 判 `BAD_TOKEN` 时, **只走层 2 会让有效的 `#122` 丢失 (∅)**。⇒ **本 Spec 的四态定义无需任何改动**; 下方「本席的建议映射」保留为当时的建议留痕, 以探针 Spec §3 的映射表为准。 本席的建议映射 (**建议, 非单方面裁定** —— 归属由主控协调):
> **`BAD_TOKEN` 在探针的层 1 应按 `NO_TOKEN` 处置** (即**触发** URL 回落)。理由: 在**读取侧**,「有 code span 但元素读不出 issue 号」与「读不到 code span」是**同一件事** —— 都没拿到可用的 canonical 键, 都该让 URL 回落去试。**⛔ 但写入侧必须仍报 warning** (E5), 两侧不得因此合并。
> **反向不成立**: 若探针把 `BAD_TOKEN` 映射成 `TOKEN(s)`, 脏元素会直接进它的比较键集合 —— 与它自己 §3 层 2 的「绝不把脏串喂进主机制匹配面」逐字冲突。
> **若探针 Spec 最终不采纳该映射**, 本 Spec 的四态**不改** (写入侧的分档有独立价值: `BAD_TOKEN` 的 fix 文案要点名坏元素, `NO_TOKEN` 的要点名「首个非空白不是反引号」), 但两份 Spec 须在各自文内**互相点名该分歧**, 不得任由它留在缝里。

### §4 机械校验 (custom check + 实现宿主 — 消解 M-10)

**既有 check 的宿主形态**, 实读 `.aria/state-checks.yaml` (共 **10** 条 check — `grep -c '^  - name:' .aria/state-checks.yaml` = 10):

```
$ grep -n "^  - name:\|python3 " .aria/state-checks.yaml
12:  - name: "issue-cache-freshness"
22:      python3 aria/skills/state-scanner/scripts/issue_cache_freshness_probe.py .
29:  - name: "silknode-contract-deferral-expiry"
88:  - name: "m6-version-badge-match"
96:      PLUGIN=$(python3 -c "import json; print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])")
104:  - name: "m6-claude-md-version"
116:  - name: "m6-arch-doc-stale"
123:      python3 -c "
141:  - name: "i18n-readme-translation-currency"
149:      python3 - <<'PYEOF'
190:  - name: "claude-md-changelog-free"
221:  - name: "coordination-gate-invocation"
235:      python3 aria/skills/state-scanner/scripts/coordination_probe.py .
244:  - name: "config-template-key-currency"
256:      python3 .aria/probes/config-template-key-currency.py
266:  - name: "plugin-cache-currency"
279:      python3 .aria/probes/plugin-cache-currency.py
```

⇒ 三种形态 (逐条归类实跑, 6+2+2=10): **(i)** 内联 shell / heredoc `command:` 块 (**6** 条: silknode-contract-deferral-expiry / m6-version-badge-match / m6-claude-md-version / m6-arch-doc-stale / i18n-readme-translation-currency / claude-md-changelog-free) · **(ii)** plugin 侧脚本 `aria/skills/state-scanner/scripts/*.py` (**2** 条: issue-cache-freshness / coordination-gate-invocation) · **(iii)** 项目侧探针 `.aria/probes/*.py` (**2** 条: config-template-key-currency / plugin-cache-currency —— 也是**最近两条新增**)。

**⭐ 本 Spec 取形态 (ii) — plugin 分发面**: 宿主 = **`aria/skills/state-scanner/scripts/linked_issue_field_probe.py`** (新建)。

> ## 🔴 分发面 × 白名单的冲突 (R3/C2 — TL 与 CR **两席独立同判**, 主控担责)
>
> **缺陷**: round-1 把白名单写成脚本内的 `GRANDFATHERED` 常量 (6 条 **Aria 本仓路径**)。
> round-2 主控把宿主改判到 **plugin 分发面**后, 二者冲突: 那 6 条路径**在采用方仓里不存在**
> ⇒ 陈旧守卫子情形 (a)「路径当前不存在」**全命中** ⇒ **采用方注册后首跑即 `exit 1` 恒红**;
> 而 `fix` 文案还让他们去改**随 plugin 分发的脚本** (改了下次 plugin 更新即被覆盖)。
> **根因 = 主控 round-2 的宿主改判只改了一半** —— 白名单**天然是仓本地的**, 脚本却变成了全局的。
>
> **处置**: **白名单移出脚本, 改为仓本地数据文件** `.aria/linked-issue-field-grandfathered.txt`
> (每行一条 `openspec/changes/<slug>` 路径; `#` 起首为注释)。
> - 探针经 `--grandfathered <path>` 接收; **该参数缺省或文件不存在 ⇒ 白名单为空集**, 不是错误;
> - ⇒ **分发件里零 Aria 路径**; 采用方拿到的是「白名单为空」= 其作用域内所有 proposal 都必须合规,
>   这对新采用方是**正确的默认**(他们没有需要 grandfather 的存量);
> - ⇒ 陈旧守卫的三个子情形只作用于**仓本地文件里的条目**, 采用方空文件 ⇒ 该守卫恒不触发, 不再恒红;
> - `fix` 文案改指仓本地文件, **明确禁止**改分发件。
>
> **⚠️ 本条是 R3 之后新增的处置 (主控 2026-08-25), 未经审计轮 —— 请 R4 优先审。**

> **📌 这是 round-2 的改判 (round-1 原取形态 iii `.aria/probes/`)。** 改判依据是主控实读指出的一个事实: **形态 (ii) 与 (iii) 并存, 且「随 plugin 分发的脚本被项目级 check 调用」已有两个既有实例** —— `.aria/state-checks.yaml:22` 与 `:235` 分别调 `aria/skills/state-scanner/scripts/issue_cache_freshness_probe.py` / `coordination_probe.py`, 二文件实存 (`ls -la` 得 7716 / 11115 bytes)。round-1 只看到「`.aria/probes` 不在 aria/ 内」这一条实读, 就推出「check 无法分发」—— **实读为真, 推论过头**。

**改判后的理由 (逐条钉到字符级)**:

1. **判定对象的性质决定归属**。既有两条 `.aria/probes/` 探针**都只对 Aria 本仓有意义**: `config-template-key-currency` 校验的是 `.aria/config.template.json` —— Aria **作为模板生产方**的产物; `plugin-cache-currency` 比对 Claude Code 已装 plugin 版本与 `aria/.claude-plugin/plugin.json` **SOT**, 需要 `aria/` 子模块存在。二者都是「Aria 对自己分发物的自检」。而「proposal 有没有『关联 Issue』字段」是**每个采用方都要的通用检查** —— 它校验的是**方法论产出**, 不是 Aria 的分发物。⇒ 与既有两条 `.aria/probes/` 先例**性质不同**, 不属同一族。
2. **选 `state-scanner/scripts/` 而非 `spec-drafter/scripts/`** —— 三条硬理由:
   - **既有两条 plugin 侧 check 宿主全在 `state-scanner/scripts/`**, 落它零新目录; 而 `aria/skills/spec-drafter/` 实读**只有 3 个文件** (`SKILL.md` / `LEVEL_GUIDE.md` / `LEVEL3_TEMPLATE.md`), **无 `scripts/` 目录**, 落它要新建目录;
   - custom check 由 **state-scanner Phase 1.11** 执行 —— 探针的**运行者**是 state-scanner, 按既有两条的归属惯例, 探针跟运行者走;
   - **`normalize_linked_issue()` 就在 `state-scanner/lib/collision.py`** ⇒ 落 `state-scanner/scripts/` 时它是**同 skill 内的相对定位** (`Path(__file__).parent.parent`), 落 `spec-drafter/scripts/` 则要跨 skill 硬编码路径, 凭空多一条会漂的耦合。
   ⇒ **语义归属 (字段义务属 spec-drafter) 与代码归属 (探针属 state-scanner) 分离是有意的**: SKILL.md 的义务声明落 `spec-drafter`, 探针实现落 `state-scanner`, 两者由本 Spec 的 §1/§4 各自成文, 不互相假装。
3. **命名照 plugin 侧两条既有探针, 不照 `.aria/probes/` 那条**: plugin 侧用 **snake_case + `_probe.py` 后缀**, 且**文件名与 check name 有意不同** (`issue-cache-freshness` ↔ `issue_cache_freshness_probe.py`; `coordination-gate-invocation` ↔ `coordination_probe.py`)。⇒ 本探针 = `linked_issue_field_probe.py`, check name = `linked-issue-field-availability`。*(round-1 曾据 `.aria/probes/` 的「文件名 == check name」惯例定名 —— 那条惯例只属形态 (iii) 族, 随宿主改判一并作废。)*
4. **入参照 plugin 侧两条**: 二者实读均为 `argv = argv if argv is not None else sys.argv[1:]` / `repo = Path(argv[0]) if argv else Path.cwd()` (`issue_cache_freshness_probe.py:148-149` / `coordination_probe.py:140-141`), 注册时逐字传 `.` 作 project root。**本探针照此**, **不得**假定 cwd —— 分发到采用方后 cwd 不由本仓决定。
5. **内联 shell (形态 i) 仍然出局**: 逻辑含 fence 状态机 + 归一 import + allowlist 漂移守卫, 写不下也不可单测。

**采用方注册 (M-2 残余缺口的具体形状)**: 脚本随 plugin 到达, 但**注册条目须采用方自己写进其 `.aria/state-checks.yaml`** —— 与既有两条 plugin 侧 check 完全同形。Aria 仓自己的注册行按既有两条的**字面路径**写 (下方骨架); 采用方按其安装形态替换前缀为 `${CLAUDE_PLUGIN_ROOT}/skills/state-scanner/scripts/…`。
> **⚠️ 未验事实 ⇒ 已升格为 A.2 显式验收项 (主控 2026-08-25 补: 只写「存疑」= 没有触发者的待办, 即 memory `feedback_completion_signals_vs_runtime_invocation` 的形状)**: A.2 须派生一条任务「实测 `${CLAUDE_PLUGIN_ROOT}` 是否被导出到 Phase 1.11 的 check 子进程」, 验收 = 在 `.aria/state-checks.yaml` 里临时注册一条 `command: echo "${CLAUDE_PLUGIN_ROOT:-UNSET}"` 的探针并跑一次 `/state-scanner`, 读回显判定; **实测前不得在文档里预写任何采用方可移植写法** (本 Spec 只给 Aria 仓字面路径注册行)。原始事实: `.aria/state-checks.yaml` 现有 10 条 check **无一使用 `${CLAUDE_PLUGIN_ROOT}`** (实读 `grep -n CLAUDE_PLUGIN_ROOT .aria/state-checks.yaml` **零命中**), 因此「Phase 1.11 起的 check 子进程里 `CLAUDE_PLUGIN_ROOT` 是否被导出」**本轮没有实测**。⇒ 本 Spec **只给 Aria 仓的字面路径注册行**; 采用方的可移植写法留待 A.2 实测后定, **不在此预写一个没验过的形态**。

**check 定义骨架 (可直接落 `.aria/state-checks.yaml`; 只用该文件 minimal YAML parser 支持的子集 —— `|` 块标量 + 引号标量 + bool + int, 与既有 10 条同形)**:

```yaml
  - name: "linked-issue-field-availability"
    description: |
      断言 openspec/changes/**/proposal.md 的「关联 Issue」字段可得且可抽取:
      按 Spec linked-issue-field-availability §3 的 E0-E6 定位并抽 token 串,
      token 元素经 lib/collision.normalize_linked_issue() 校验 (不自写第二份归一)。
      作用域只含 changes/: archive/ 140 份实测 0 份合规 (126 NO_FIELD + 14 NO_TOKEN),
      且不可改、不再被消费 -> 扫它 = 恒红 = 零信息。
      存量不合规项经 GRANDFATHERED 具名白名单在册 (fail-CLOSED: 白名单外一律 FAIL);
      白名单含已离开作用域的陈旧条目同样 FAIL — 防它退化成永久静默豁免。
      判据分割 (零证据不当正证据): 作用域缺失 / 归一 SOT 不可导入 -> ##SKIP##。
    command: |
      python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py . \
        --grandfathered .aria/linked-issue-field-grandfathered.txt
    severity: warning
    fix: |
      在被点名的 proposal.md 头部 blockquote 补一行 (行首无空白, `>` 后恰一个空格):
        > **关联 Issue**: `<org>/<repo>#<n>`      # 多个用 ", " 分隔
      无关联时逐字写: > **关联 Issue**: `无`
      被点名为「白名单陈旧条目」时: 删除本仓 .aria/linked-issue-field-grandfathered.txt
      里那一行 (该 proposal 已归档/改名/已合规)。注意: 白名单是**仓本地数据**,
      不在 plugin 分发件里 — 任何情况下都不要去改 aria/ 子模块下的探针脚本。
    timeout_seconds: 10
    enabled: true
```

> **⚠️ 骨架只用既有 check 已在用的键** (**R3/M6 订正**: 原写「10 条」—— 实测 `grep -c '^  - name:' .aria/state-checks.yaml` = **11** (第 11 条 `main-project-version-consistency` 由并发轨 `2ae012f` 于本 Spec 起草当日引入)。**口径 (命令) 才是规范, 数字是当日观测** —— 与本 Spec §Why 的同一条纪律一致, 复核一律重跑该命令) (`name` / `description` / `command` / `severity` / `fix` / `timeout_seconds` / `enabled`) —— `collectors/custom_checks.py:63` 自陈是「Minimal YAML parser — strictly scoped to state-checks.yaml shape」且 `:122-123` 逐字「This is a narrow parser — it / intentionally rejects YAML features outside the documented schema.」, 对**未知键**的行为**本轮未验**。⇒ 落地时**不得**为本 check 引入任何新键; 确有需要时须先在该 parser 上实跑确认不抛 `ValueError`。

**探针的判据分割 (fail-CLOSED, 五臂)**:

| 情形 | 输出 | 退出码 |
|---|---|---|
| `openspec/changes/` 不存在, 或作用域内 0 份 proposal | `##SKIP## <理由>` | 0 |
| `normalize_linked_issue` 导入失败 (aria 子模块未 checkout / 版本 < v1.67.0) | `##SKIP## <理由>` | 0 |
| 作用域内出现 `NO_FIELD`/`NO_TOKEN`/`BAD_TOKEN` **且不在 `GRANDFATHERED`** | `FAIL` + 逐条 `path:line verdict 细节` | 1 |
| `GRANDFATHERED` 含**陈旧条目** —— 三个子情形**逐条断言**, 任一命中即红: (a) 该路径**当前不存在** (目录被删/改名); (b) 路径存在但**已移出作用域** (已归档到 `openspec/archive/`); (c) 路径仍在作用域内但**已合规** (`OK`) | `FAIL allowlist 陈旧: <path> (<a\|b\|c>)` | 1 |
| 其余 | `OK (n 份在范围内, m 条在册)` | 0 |

**归一的导入方式 (字符级 — 这一条实现者最容易写错, 且与同目录邻居的写法相反)**:

```python
# 探针位于 aria/skills/state-scanner/scripts/ ⇒ parent.parent 即 state-scanner
_SS = str(Path(__file__).resolve().parent.parent)
if _SS not in sys.path:
    sys.path.insert(0, _SS)
try:
    from lib.collision import normalize_linked_issue
except Exception:
    print("##SKIP## normalize_linked_issue 不可导入 (aria 侧 lib/collision.py 缺失或版本 < v1.67.0)")
    sys.exit(0)
```

> **⚠️ 必须用「包父目录 + `from lib.collision import`」, 不得用同目录邻居 `coordination_probe.py` 的「裸模块」写法** —— 本轮**两种写法各实跑一次**, 结果相反:
>
> | 写法 | 实跑结果 |
> |---|---|
> | `sys.path.insert(0, <state-scanner>)` + `from lib.collision import normalize_linked_issue` | ✅ `('aria-plugin', 122)` |
> | `sys.path.insert(0, <state-scanner>/lib)` + `from collision import normalize_linked_issue` | ❌ `ImportError: attempted relative import with no known parent package` |
>
> 原因逐字: `lib/collision.py:46` 是 **`from .claim_schema import ClaimRecord`** (相对 import) ⇒ 它**必须**作为包成员被导入。而 `coordination_probe.py:80-85` 恰恰**明写**它「Deliberately NOT `import lib.runtime_probe`」并改用裸模块写法, 理由是「the top-level name `lib` resolves to state-scanner/lib (Layer L — a DIFFERENT package, claim_schema.py etc.), not scripts/lib」。
>
> ⇒ **两个探针的选择相反, 且各自都对**: `coordination_probe` 要的是 `scripts/lib/runtime_probe`, 必须**避开** `state-scanner/lib` 这个同名包; 本探针要的**正是** `state-scanner/lib`, 必须**绑定**它。**⛔ 由此产生一条实现约束**: 本探针在 `sys.path` 上绑定 `lib` → `state-scanner/lib` 之后, **不得再 import 任何 `scripts/lib` 下的模块** (会取到错的包)。本探针除 stdlib 外**只 import 这一个符号**, 该约束天然满足 —— 但须成文, 否则下一位加功能的人会踩 `collectors/openspec.py:29` 记录的同一个坑。

### §5 作用域与回填

**作用域 = `openspec/changes/**/proposal.md`, 不扫 `openspec/archive/`** (D5)。

**作用域内逐份现状** (**终值**: 测量时刻 `2026-08-25T02:02:42Z`, 三份拆分产物全部落盘后作用域内 **9 份**; 判定由 §3 规则原型对全部 9 份实跑, 命令与分布见 §Why「当日观测值」表):

| proposal | 规则原型判定 | 本 Spec 处置 |
|---|---|---|
| `a1-entry-claim-duplicate-work-guard` (母 Spec) | **OK** (`:12` token 串 `无`) | 不改 — 由母 Spec 执笔席落 FIX-19, 本轮实测已合规 |
| `aria-2.0-m6-cost-model-telemetry` | `NO_FIELD` | **不改** ⇒ 入 `GRANDFATHERED` |
| `aria-2.0-m6-dispatch-input-delivery` | `NO_FIELD` | **不改** ⇒ 入 `GRANDFATHERED` |
| `aria-2.0-m6-e2e-resilience` | `NO_FIELD` | **不改** ⇒ 入 `GRANDFATHERED` |
| `aria-2.0-m6-release-closeout` | `NO_FIELD` | **不改** ⇒ 入 `GRANDFATHERED` |
| `aria-2.0-m7-agent-lifecycle` | `NO_FIELD` | **不改** ⇒ 入 `GRANDFATHERED` |
| `aria-2.0-m7-fleet-aggregation` | `NO_FIELD` | **不改** ⇒ 入 `GRANDFATHERED` |
| **本 Spec** (`linked-issue-field-availability`) | **OK** (`:6` token 串 `无`) | dogfood, 已合规 |
| `sibling-spec-probe` (同批新建, 另一执笔席) | **OK** (`:6` token 串 `无`) | 该 Spec 已自行 dogfood (本席实读其 `:6` 为 `> **关联 Issue**: \`无\` — …); **不入** `GRANDFATHERED` |

⇒ **上线当日** (作用域 9 份): **3 份 `OK`** (母 Spec / 本 Spec / 探针 Spec, 三者头部 token 串均为 `无`) + **6 份具名在册** ⇒ 探针输出 **`OK`**。**不是「即绿」** (6 份靠在册而非合规), **也不是「恒黄」** (在册项不产生 warning)。**新建的 proposal 一律不在册, 必须合规。**
>
> **⚠️ 这三份 `OK` 是当日观测, 不是保证**: 三份都还在 Draft, 头部随时可能被各自执笔席改动。**check 的价值不来自这个 3, 来自「白名单外必须合规」这条不变量。**

> **为什么不直接回填那 6 份 (D6, 与 R1 editlist U-2 的关系)**: 那 6 份属 `aria-orchestrator` 轨的**活跃在制** Spec, 编辑它们是对他人在制产物的写入 —— memory `sync≠push-auth` + `feedback_concurrent_feature_collision_claim_before_build`: **不能自我授权**。R1 editlist 已把该项上呈为 **U-2**, **至今未见 owner 裁定**。
>
> **⭐ 两方案不互斥, allowlist 严格包含回填**: `GRANDFATHERED` 就是「尚未回填清单」。owner 若授权回填, **回填一份就删一条**, 探针逻辑零改动; 全部回填后 allowlist 为空, 陈旧守卫恒真、恒 OK。⇒ **本 Spec 落版取「不回填 + 具名在册」, 不因此排除回填**; 该项作为 **O-1** 留在 §闸门状态 待 owner 裁 (Rule #10: AI 不自行拍板范围决策)。

> **为什么 allowlist 而不是「就让它每次黄 6 条」**: 9 份里 6 份不合规 = 每次都黄 ⇒ **恒红**, 与假绿同样零信息 (memory `feedback_false_green_dual_is_permanent_red`)。且**换量而不是调阈值** (memory `redfix-change-quantity`): 被测的量不是「有几份缺字段」, 而是「**有没有 allowlist 之外的份缺字段**」。白名单是**封闭枚举 + 其余阻断** = fail-CLOSED (memory `feedback_invariant_needs_failclosed_default`), 且其粒度**恰等于**情形集 —— 6 条具名路径, 一条一条 (memory `knob-granularity`)。陈旧条目守卫是它的漂移护栏 (memory `feedback_validator_repo_drift_guard_test`)。

---

## 决策记录

| # | 决策 | 依据 |
|---|------|------|
| **D1** ⭐ | **抽取规则钉到字符级 (E0–E6), 不 defer 到 A.2** | 直接消解 R2 的 **C-A**。实测: 14/14 存量字段直喂归一 = `None`; 「取第一个 code span」的坏实现在 **6** 条真实字段上抽出 `confirmed`/`partial-repro`。规则不定 ⇒ check 上线恒红或抽错, 二者必居其一 |
| **D2** ⭐ | **定位谓词 = 行首 depth-1 + fence 排除 + 文档序第一条**; 明确否决「只扫头部 N 行」 | 该假阳性形态是**真实的** (**R3/M5 订正**: 原写「母 Spec `:88`」—— 该引用现已悬空: 母 Spec 的 §1 整节已于同批迁出本 Spec, 其 `:88` 现为 `## What Changes`, 全文 depth-2 `> > **关联 Issue**` 命中 **0**; 真身是**迁出前**的 `cc1bdef:75`, 本文件 §Why 的 grep 逐字输出保留了当时的原文, 探针 Spec `:99` 引的也是该 SHA。⇒ **稳定锚点改用**「本文件 §Why 的 grep 输出 + `cc1bdef:75`」, 不再引会随迁出漂移的行号) (memory `reference_secret_guard_false_positive_on_spec_docs` 同形)。否决「头部 N 行」的依据是实测: 两份归档件的真字段在 `:61` / `:45`, 任何 N 都是拍脑袋且造假阴性 |
| **D3** ⭐ *(round-2 改判)* | **check 宿主 = `aria/skills/state-scanner/scripts/linked_issue_field_probe.py`** —— **plugin 分发面** (形态 ii), 不用内联 shell (i), 不落 `.aria/probes/` (iii) | 消解 **M-10**。**改判依据**: 形态 (ii)/(iii) 并存且 (ii) 已有两个既有实例 (`.aria/state-checks.yaml:22` / `:235` 调 `issue_cache_freshness_probe.py` / `coordination_probe.py`, `ls -la` 得 7716 / 11115 bytes) ⇒ round-1 的「check 无法分发」推论过头。归属判据 = **判定对象的性质**: 既有两条 `.aria/probes/` 都是「Aria 对自己分发物的自检」(config 模板 / plugin 安装态), 而「proposal 有无该字段」是**每个采用方都要的通用检查**。选 `state-scanner` 而非 `spec-drafter`: 既有两条 plugin 侧宿主全在此、custom check 由 state-scanner Phase 1.11 执行、`normalize_linked_issue()` 就在 `state-scanner/lib/`。逐条见 §4 |
| **D4** | **复用 `normalize_linked_issue()`, 不自写第二份归一**; 导入失败 ⇒ `##SKIP##`, **不 fallback 到自写正则**; 导入方式 = **包父目录 + `from lib.collision import`** (**不是**同目录邻居 `coordination_probe.py` 的裸模块写法) | 姊妹 Spec `linked-issue-normalization` 的 **D9** 就是为此把它导出为公开单元 (`collision.py:178` 实读)。自写 fallback = 造出第二个归一实现, 两份必然漂移 (memory `feedback_spec_underdetermination_two_implementer_test`)。**导入方式两种写法本轮各实跑一次**: 包父目录 ✅ 得 `('aria-plugin', 122)` / 裸模块 ❌ 抛 `ImportError: attempted relative import with no known parent package` (因 `collision.py:46` 是 `from .claim_schema import ClaimRecord`) —— 与 `coordination_probe.py:80-85` 的相反选择**各自都对**, 理由见 §4 |
| **D5** | **作用域只含 `openspec/changes/`** | `archive/` 140 份不可改且不再被消费; 且实测 **0 份合规** (126 `NO_FIELD` + 14 `NO_TOKEN`) ⇒ 扫它 = **恒红** = 零信息 |
| **D6** | **存量处置 = `GRANDFATHERED` 具名白名单 + 陈旧条目守卫**, 不跨轨回填 | U-2 未裁 + 跨轨写入不可自我授权。白名单**严格包含**回填方案 (回填一份删一条, 探针零改动) ⇒ 不排除 owner 选回填 |
| **D7** | **severity = `warning`** (advisory-over-hardlock) | 承母 Spec **D2**。本 Spec **不**升 block —— 主机制本身就是 advisory, 校验面不该比被校验的机制更硬 |
| **D8** | **模板里用 placeholder `` `{<org>/<repo>#<n>}` ``, 不要求模板自身过 E5** | 模板不在 check 作用域 (`standards/` 非 `openspec/changes/`)。要求它过 E5 会逼出一个**假的 issue 号**写进跨项目模板。⇒ SC-6 只断言模板过 **E0 定位谓词** + Usage Note 存在, **不**断言 E5 |
| **D9** | **字段名维持单一中文 token `关联 Issue`** | 不新增英文别名 = 不新增第二个谓词面。**但后果成文**: SOT 模板 `proposal-minimal.md` 全文为英文 (`> **Level**:` / `> **Status**:` / `> **Created**:`) 且是**跨项目**面 ⇒ 英文语境的采用方须逐字写中文字段名。这是跨项目约定, **不由本 Spec 自裁** ⇒ 上呈为 **O-2** |

**Rule #6 (rule6_note)** —— 逐 hunk 判, 不逐文件判:

| hunk | 判据表落格 | 处置 |
|---|---|---|
| `aria/skills/spec-drafter/SKILL.md` 的模板义务段 (§1 第二处) | **第二行「处方性 · 运行时指令面 / 能 / 照跑 AB」** —— 它改变 spec-drafter **产出**的 proposal 形态 | **照跑现有 `aria-plugin-benchmarks/ab-suite/spec-drafter.json`**。实核: 该套件实存, `evals` **2** 条 (id 1 = 「判断规范等级」, id 2 = 「双语输入处理」)。验「加字段义务后既有 2 个场景行为是否漂移」 |
| 同上 hunk 的**新增行为**「新建 proposal 时必须写出该字段且写法过 E0/E2/E5」 | **第三行「处方性 · 套件覆盖外」** —— 上述 2 条 eval 一条判 Level、一条判双语输出, **结构性覆盖不到** authoring 是否写出某字段 | 三条缺一不可: (1) **点名行为** = SC-7 的行为臂 (下表); (2) **建可证伪定向 fixture** (双臂: 写出合规字段 vs 省略/写成 markdown 链接形, 两臂须可分辨); (3) **套件缺口开 issue** —— 与 `aria-plugin#117`「缺 authoring 维度」同族, 归并或新开由 A.2 定 |
| `standards/openspec/templates/proposal-minimal.md` | **第一行「描述性 (schema / 字段)」** —— 纯模板文本, 零 AI 指令面 | **substitute = SC-6**, baseline 必红 (实测该文件今天 `grep -c "关联 Issue"` = **0**) |
| `aria/skills/state-scanner/scripts/linked_issue_field_probe.py` (**新建**) + 主仓 `.aria/state-checks.yaml` (注册) | **该 hunk 落在 plugin 分发面内, 故必须逐条论证它不改变 AI 行为面** (round-2 宿主改判后这一格的论证负担加重了, 不能沿用 round-1 的「`.aria/` 不分发」): 判据是**内容是否影响 AI 行为**, 不按目录判 —— (a) 新脚本是**确定性 Python**, 不进 `SKILL.md` / 不进 frontmatter / 不被任何 skill 的加载面读取 (与同目录既有两条探针 `issue_cache_freshness_probe.py` / `coordination_probe.py` 同性质, 二者 ship 时同样未跑 AB); (b) 它**只在 `.aria/state-checks.yaml` 注册后**由 Phase 1.11 以子进程调用, `state-scanner/SKILL.md:119` 仅把该 yaml 记为「Opt-in 子阶段」的**存在条件**, 其内容由 `collectors/custom_checks.py:399` 机械读取, 非 AI 指令; (c) 本 Spec **不改** `state-scanner/SKILL.md` 一个字 | 行为面由 **SC-4 / SC-5 / SC-8** 结构化测试承担。**这不是声称「Rule #6 不适用」的豁免** —— 是「该 hunk 不改变任何 Skill 的运行时指令面」这一事实判定, 三条依据各带可复核锚点。⚠️ **若 A.2 落地时需要改 `state-scanner/SKILL.md`** (例如在其 Layer L 段登记该 check), 该 hunk **另行按判据表重判**, 不由本格覆盖 |

**不申请豁免。**

---

## Success Criteria

> ## ⛔ 验证宿主 (R3/QA-F6, 主控 2026-08-25 补 —— **不补这段就是复发本 Spec 自己要治的病**)
>
> R3/QA 判定: 本 Spec 的 SC-1~6 / SC-8 全部标「代码」类却**没有一条声明测试宿主** —— 而本 Spec 存在的理由 (R2/C-A) 正是
> 「承重规则 defer 到 A.2 ⇒ 上线即恒红」, 以及姊妹母 Spec 的 R1/C4「把 SC 挂在**不存在的**测试宿主上」。**同一个病在这里复发了。**
>
> | SC | 被测对象 | **宿主 (逐字路径)** | 现状 |
> |---|---|---|---|
> | SC-1~4 (E0–E6 四态与定位) | `lib/linked_issue_field.py::extract_linked_issue_field(text)` (纯函数, R3/C3 新增) | **`aria/skills/state-scanner/tests/test_linked_issue_field.py`** (新建; 目录实存, 与 `test_release_by_track.py` / `test_coordination_default_lockin.py` 同级) | 目录实存, 文件待建 |
> | SC-5 (探针判据分区五臂) | `scripts/linked_issue_field_probe.py` **CLI 全链路** (exit code + stdout) | **同上文件** (以 `subprocess` 跑 CLI, 仿 `test_release_by_track.py:531` 的 `_GATE = Path(_SKILL_ROOT)/"scripts"/...` 既有体例) | 同上 |
> | SC-6 (模板 SOT) | `standards/openspec/templates/proposal-minimal.md` 文本 | **`aria/skills/state-scanner/tests/test_linked_issue_field.py`** 内一条结构断言 (读**主仓**该文件; 跨仓读取属已知限, 见下) | 同上 |
> | SC-8 (脚本路径不得回落 `.aria/probes/`) | 仓内文件布局 | 同上 (`Path` 存在性断言) | 同上 |
>
> **⚠️ SC-6 的跨仓已知限**: 该断言从 `aria/` 子模块内的测试去读**主仓** `standards/` 子模块的文件 —— 在 plugin 单独分发时该路径不存在。
> ⇒ 该条**必须** fail-soft 成 **skip 而非 fail** (零证据不当负证据), 并在 skip 时打印原因。**这是本 Spec 的已知限, 成文不假装覆盖。**

> **编号说明**: 本 Spec 从 **SC-1** 重新编号 (独立文件独立命名空间)。**本 Spec 的 SC-1 ~ SC-5 共同承接母 Spec 旧 SC-13** (「proposal 无『关联 Issue』字段 / 值不可解析 ⇒ custom check warning; 显式 `无` 则通过」) —— 旧 SC-13 把「定位 / token / 多值 / `无` / 判据分区」五件事捆在一条断言里, 按 R2 的 **M-16** (「把 CLI 可验字段与消费层措辞捆在一条」) 拆开, 每条只留**一个**可机械判定的断言。母 Spec 侧保留 SC-13 行, 内容改为「→ 已迁 `linked-issue-field-availability`」。

| SC | 类别 | 场景 | 期望 | **它怎么会红** |
|----|------|------|------|---------|
| **SC-1** | 代码 | **E0 定位三谓词**。四份夹具: (a) 头部 `> **关联 Issue**: \`10CG/aria-plugin#122\``; (b) 文件**无** depth-1 字段行, 但**围栏代码块内**含一行逐字相同的字段行; (c) 文件只含 `   > > **关联 Issue**: \`10CG/aria-plugin#122\``; (d) 文件无 depth-1 字段行, 但**blockquote 内的围栏块**里含一行 `> **关联 Issue**: \`other/repo#999\`` | (a) 抽到 token 串 `10CG/aria-plugin#122`; (b)(c)(d) **判 `NO_FIELD`** | 用松谓词 (`grep '\*\*关联 Issue\*\*'` / 不锚行首 / 不做 fence 状态机) 的实现在 (b)(c)(d) 上抽出 token ⇒ 红; **fence 正则漏掉 `(?:> ?)?` 的实现在 (d) 上抽出 `other/repo#999` ⇒ 红**。**baseline 必红** (今天无任何实现)。(c) 的形状在真实语料上有实例: 母 Spec `:88` |
| **SC-2** | 代码 | **E2 token 起始位**。输入 `> **关联 Issue**: [10CG/aria-plugin #122](url) (triage \`confirmed\`)` | 判 **`NO_TOKEN`**, 且**不得**抽出 `confirmed` | 「取该行第一个 code span」的实现抽出 `confirmed` ⇒ 红。该形状在真实语料上 **6** 条 (路径见 §3 E2 引用块), 夹具须至少复用其中 1 条的**逐字原文** |
| **SC-3** | 代码 | **E4/E5/E6 多值**。(a) token 串 `10CG/a#1, 10CG/b#2`; (b) token 串 `10CG/a#1, [b](url)` | (a) **合法**, 两元素各自解析成功, `--linked-issue` 实参逐字节 = `10CG/a#1`; (b) **`BAD_TOKEN`** 且输出点名 `[b](url)` | 把整串直喂归一的实现在 (a) 上判不可解析 ⇒ 红; 只校验第一个元素的实现在 (b) 上判合法 ⇒ 红; 对 (a) 把实参取成整串或第二元素的实现 ⇒ 红 |
| **SC-4** | 代码 | **`无` 两分支**。(a) `> **关联 Issue**: \`无\` — 说明`; (b) `> **关联 Issue**: 无 (由 \`x\` 发现)` (裸 `无`, 无 code span) | (a) **合法**, 且**不产生任何 `--linked-issue` 实参**; (b) **`NO_TOKEN`** | 把 `无` 当普通 token 传给 `--linked-issue` 的实现 ⇒ 红 (母 Spec NEW-01 实测: 两份无关 Spec 都写 `无` 会互相命中 overlap); 接受裸 `无` 的实现在 (b) 上 ⇒ 红。**(b) 有真实语料实例**: `openspec/archive/2026-08-23-linked-issue-normalization/proposal.md:6` 逐字 `> **关联 Issue**: 无` (实跑 `cat -A` 见 §实读清单) |
| **SC-5** | 代码 | **探针判据分区四臂**。(a) 作用域内新增一份 `NO_FIELD` 且**不在** `GRANDFATHERED`; (b) 仅 `GRANDFATHERED` 内的 6 条不合规; (c) **仓本地** `.aria/linked-issue-field-grandfathered.txt` 含一条已不在作用域的 path; (d) 归一模块不可导入 | (a) **exit 1** 且输出点名该 path; (b) **exit 0** 首行 `OK`; (c) **exit 1** 且文案含「allowlist 陈旧」并点名该 path; (d) **exit 0** 首行以 `##SKIP##` 开头 | (a) 判 OK 的实现 (正向枚举 / catch-all 放行) ⇒ 红; (c) 静默忽略的实现 ⇒ 红 (allowlist 退化成永久豁免); (d) 判 OK 的实现 ⇒ 红 (零证据当正证据)。**四臂两两可辨** —— (a) 与 (c) 都 exit 1, 靠文案区分; (b) 与 (d) 都 exit 0, 靠首行标记区分 **(e) (R3/C2 补; ⚠️ R4/K9 订正措辞)**: `--grandfathered` 指向一个**不存在**的文件 ⇒ **「文件缺失」这件事本身不得成为错误** —— 白名单视为**空集**, 探针**照常判定**作用域内全部 proposal 并按判据表出结论。**原措辞「不得 exit 1」在本仓自相矛盾且教出真 fail-open** (R4/silent-failure + type-design 两席同判): 本仓该文件今天就不存在, 而作用域 9 份里有 6 份 `NO_FIELD` ⇒ **必然** exit 1; 照原字面去消解矛盾的实现 = **`rm` 一条命令就永久静默整条 enabled check**。⇒ 正确的断言拆成两句: **(e1)** 文件缺失时**不得**因「读不到白名单」而报错/中止 (须继续判定); **(e2)** 文件缺失时若作用域内存在不合规项, **仍须 exit 1 并逐条点名** (缺白名单 ⇒ 无人被豁免, 这才是采用方的正确默认); 把「白名单文件缺失」当错误、或把 6 条 Aria 路径硬编码进脚本的实现 **必红** |
| **SC-6** | 代码 | **SOT 模板自身合规 + 引用未断**。`standards/openspec/templates/proposal-minimal.md` 含**恰一条**满足 E0 三谓词的行; 其 `## Template Usage Notes` 段含「无关联时逐字写 `` `无` ``」一条; `aria/skills/spec-drafter/SKILL.md` 里对该模板的相对路径引用解析到**存在的文件** | 如左 | 模板加了字段但写成裸文本 / markdown 链接 (不过 E0) ⇒ 红; 加了字段但漏 Usage Note ⇒ 红; spec-drafter 的引用路径漂移/失效 ⇒ 红。**baseline 必红**: 实测该模板今天 `grep -c "关联 Issue"` = **0**。⚠️ 本条**不断言** E5 (D8: 模板值是 placeholder) |
| **SC-7** | **行为 (定向 fixture)** | spec-drafter 新建一份 Level 2 proposal | 产出的 `proposal.md` 头部含一条过 E0 + E2 + E5 的字段行; 无关联时逐字 `` `无` `` | 省略该行 / 写成 markdown 链接形 / 留空 的臂应可分辨。**类别是「行为」不是「代码」** —— 断言对象是 AI 的 authoring 行为, **无代码宿主**, 不冒充结构化测试 (母 Spec R2 的 M-16 同款教训) |
| **SC-8** | 代码 | **check 宿主真被注册且真能跑, 且脚本真在分发面内**。三条同批: (a) `.aria/state-checks.yaml` 含 name 为 `linked-issue-field-availability` 的条目, 其 `command` 指向的文件存在; (b) 该文件路径**位于 `aria/skills/` 之下** (= 随 plugin 分发, 不是 `.aria/`); (c) 实跑该 command 得到 exit ∈ {0, 1} 且 **stdout 首行前缀 ∈ {`OK`, `FAIL`, `##SKIP##`}** | 如左 | 只建脚本不注册 (或路径拼错) ⇒ (a) 红; **把探针放回 `.aria/probes/` ⇒ (b) 红** (这一臂直接钉住 D3 的改判, 防它被悄悄退回); 探针崩溃 (traceback → stdout 空) ⇒ (c) 红。**baseline 必红** (三者今天都不存在)。⚠️ (c) **不断言 exit 值本身** —— 断言值就把测试绑死在当日语料上 |

---

## 非目标

- **不做** A.1 入口认领 / track-id 契约 / heartbeat —— 母 Spec 范围;
- **不做**竞品 spec 探针 —— `sibling-spec-probe` 范围;
- **不改** `linked_issue` 归一算法本身 —— 姊妹 Spec `linked-issue-normalization` 已 ship (v1.67.0), 本 Spec **只 import** 它 (D4);
- **不改** `aria/skills/state-scanner/` 下的任何一行代码 —— `collision.py` / `phase1_gate.py` 均**零改动**;
- **不扫** `openspec/archive/` (D5), **不回填**归档件的字段;
- **不跨轨回填** 6 份 M6/M7 proposal (D6; 待 O-1);
- **不把** severity 升为 `error` / block (D7);
- **不新增**英文别名字段名 (D9; 后果成文, 待 O-2);
- **不做**采用方侧的 check **自动注册** (让 `config.template.json` 或 init 流程替采用方写入该条目) —— 那会改变「项目自主决定跑哪些 check」的既有语义, 属另一交付面; M-2 的残余缺口即止于此 (§1);
- **不建** basename 别名表 (母 Spec D9)。

---

## Impact

| 文件 | 变更 | 来源 |
|------|------|------|
| **`aria/skills/state-scanner/lib/linked_issue_field.py`** (**新建**) | E0–E6 交付为**可 import 的纯函数** `extract_linked_issue_field(text: str) -> FieldVerdict`; 输入文本 blob 非路径 (探针要在远端 ref 的 blob 上调用)。CLI check 与 `sibling-spec-probe` **都 import 它**, 二者不自写第二份 | **R3/C3** |
| **`.aria/linked-issue-field-grandfathered.txt`** (**新建, 仓本地数据**) | `GRANDFATHERED` 白名单移出分发件; 每行一条 `openspec/changes/<slug>`; 探针经 `--grandfathered <path>` 读取, 缺省/文件不存在 ⇒ 空集 | **R3/C2** |
| `standards/openspec/templates/proposal-minimal.md` (**跨项目共享子模块 · SOT**) | 头部 blockquote 增 `> **关联 Issue**: \`{<org>/<repo>#<n>}\``; `## Template Usage Notes` 增「无关联时逐字写 `` `无` ``, 不留空、不删行」一条。实测该文件当前 0 命中 | **R2/M-2** (F-39) |
| `aria/skills/spec-drafter/SKILL.md` | 声明该字段为**必填** + 写法引本 Spec §3; **不重复模板正文** (SOT 在 standards, `:429` 已有委托引用)。⚠️ **与母 Spec 同文件不同 hunk** (母 Spec 改「A.1 第二落点」与 frontmatter `allowed-tools`) ⇒ **逐 hunk 判 Rule #6**, 两 Spec 互不覆盖、互不替代; 落地时须逐 hunk 对齐 | **R2/M-2** (F-40) |
| `aria/skills/state-scanner/scripts/linked_issue_field_probe.py` (**plugin 分发面**) | **新建** — E0–E6 抽取 + 五臂 fail-CLOSED 分区 + `GRANDFATHERED` 白名单 + 三子情形陈旧守卫; 入参照既有两条取 `argv[0]` 作 project root | **R2/M-10** (round-2 改判宿主) |
| `.aria/state-checks.yaml` | 注册 check `linked-issue-field-availability` (`severity: warning` / `timeout_seconds: 10` / `enabled: true`), 骨架见 §4 | **R2/M-10** + 母 Spec S4 |
| `aria/skills/state-scanner/lib/collision.py` | **零改动** —— 只 `import normalize_linked_issue` (`:178`; 实读 aria `d50f9c3` 与 `58a49e7` 对该文件 `git diff --stat` **为空**, 两 SHA 行号一致) | D4 |
| `openspec/changes/aria-2.0-m{6,7}-*/proposal.md` ×6 | **本 Spec 不改** —— 以 `GRANDFATHERED` 具名在册 (D6); owner 若裁 O-1 = 回填, 则逐份补一行并同步删 allowlist 条目 | D6 / U-2 |
| AB 套件 — `aria-plugin-benchmarks/ab-suite/spec-drafter.json` | **照跑现有 2 evals** (实核实存, id 1/2), 验扩义务后既有场景行为是否漂移 | rule6_note 第一格 |
| AB 套件 — spec-drafter **覆盖外**档 | 定向 fixture ×1 (SC-7 双臂) + 套件缺口 issue (与 `aria-plugin#117` 同族, 归并或新开由 A.2 定); 与上一行**互不替代** | rule6_note 第二格 |
| 版本号 | aria 侧唯一指令面改动 = `spec-drafter/SKILL.md` ⇒ 按 CLAUDE.md「新增 Skill / Skill 架构重构 = MINOR+」之下、「文档更新 = PATCH」之上 —— 本 Spec **自判 MINOR** (新增运行时 authoring 义务, 行为面扩大) —— ⚠️ **但 CLAUDE.md 的两条判据都不字面覆盖本例** (既非「新增 Skill / 架构重构」, 也非「纯文档更新」), **若 owner 改判 PATCH 请裁**; **号段落地时计算, 不预写字面量**。⚠️ **standards 子模块另有自己的版本与 PR 流程**, 且按 CLAUDE.md 多远程硬约束 1: 子模块合并**一律本地做 + 双推 + 逐个 `ls-remote` 核验**, 禁 Forgejo 服务端合并 | — |
| 发版同步面 | 按 CLAUDE.md §版本管理 与 `standards/conventions/version-management.md` 执行, **本 Spec 不复述引用点清单** (复述即产生第二份会漂移的清单 — Aria #177 的形状) | — |

---

## 实读与重测清单 — ⛔ **整节已切出**

> **迁往**: [`.aria/audit-reports/linked-issue-field-availability-audit-trail.md`](../../../.aria/audit-reports/linked-issue-field-availability-audit-trail.md) §1 —— **按字节搬运, 未重写任何一句**。
> **切分理由 (主控 2026-08-25 裁定, 已标请 owner 复议)**: 该表是**核验证据**不是交付面; 与母 Spec / 探针 Spec 同批同刀, 三份体例一致。owner 2026-08-07 对 `linked-issue-normalization` 的「交付面与审计史切开」裁定是先例。
> **本文件正文所有 `文件:行号` 引用的实读基线 = 主仓 `cc1bdef` / aria 子模块 `d50f9c3`**。**复核命令 (逐字)**: `git -C aria show d50f9c3:<path> | sed -n '<N>p'`; 语料统计命令见审计轨 §1。
> **正文里形如「见清单 #N」的交叉引用**, 一律指审计轨 §1 表内的第 N 行。
> ⚠️ 审计轨 append-only 且**不维护与本文件的一致性** —— 二者不一致**以本文件为准**, 按上面的复核命令重新实读裁决。

## 本轮引入的新表面 (未审)

> 硬约束 5「不新增未被要求的机制」的对账: 下列每一条都须能回答「不加它, 哪条 R2 findings 消解不掉」。

1. **`aria/skills/state-scanner/scripts/linked_issue_field_probe.py`** —— 新脚本, **落在 plugin 分发面** (round-2 改判)。**不加它 M-10 无解** (M-10 的字面就是「无实现宿主」)。三条未验风险: (a) `lib/collision.py` 缺失或版本 < v1.67.0 时走 `##SKIP##` 分支, **本轮未在真实降级下实测**, 只验了正常导入路径; (b) 本探针在 `sys.path` 上绑定 `lib` → `state-scanner/lib`, 与同目录 `coordination_probe.py` 的选择相反, **两者不在同一进程内**故无冲突, 但**未实测**「同一 pytest 进程内先后 import 两者」的情形; (c) 它随 plugin 进入**每个采用方**的分发面 —— 即使采用方没注册这条 check, 脚本文件也会到达, **这是新增的分发体积与新增的被误调面**, 与既有两条同形但确是新表面。
2. **`GRANDFATHERED` 白名单 + 陈旧条目守卫** —— **这是本执笔席的综合裁断, R2 的任何一席都没提出这个形态**。不加它: C-A 只解决了「抽取规则」一半, 「check 上线恒红」那一半仍在 (作用域 9 份里 6 份不合规)。风险: 白名单是**硬编码路径清单**, M6/M7 目录改名会同时触发「新违规」与「陈旧条目」两条 FAIL —— SC-5 的 (a)/(c) 两臂要求文案可分辨, 但**两条同时出现**时的输出顺序/合并方式**未定义**。
3. **fence 状态机** (E0 谓词 2) —— 引入 markdown 结构解析。不加它, SC-1(b) 那类「文档里的示例」无法与真字段区分。**已知限 (三条, 成文不假装覆盖)**: (i) 只认「三个反引号」与 `~~~` 两种围栏标记, **不处理**缩进代码块 (4 空格); (ii) **不处理嵌套围栏的长度差异** (更长的围栏内包更短的围栏) —— 本文件 `:123` 自己就有一个 4 反引号 code span 内含 3 反引号, 它不在行首故不触发状态机, 但**同形写法出现在行首时会误翻转**; (iii) blockquote 内的围栏只认**一层** `> ` 前缀 (`(?:> ?)?`), 两层及以上 (`> > ` + 围栏) 未处理 —— 该形态在真实语料上零实例, 未构造夹具。
4. **对 `standards/` 子模块的写入** —— 跨仓交付面。走 aria-standards 自身 PR + 主仓 gitlink bump, 且受 CLAUDE.md 多远程硬约束 1/2 管辖 (本地合并 + 双推 + `ls-remote` 逐个核验)。本 Spec **未**估算该流程的耗时/门。**round-2 追加**: 宿主改判后本 Spec 的写入面变成**三个仓** (`standards/` 模板 + `aria/` 两处 + 主仓 `.aria/state-checks.yaml` 与 Spec), 交付顺序与 gitlink bump 次序**未排**, 属 A.2。
5. **与母 Spec 同文件不同 hunk 地改 `spec-drafter/SKILL.md`** —— 两 Spec 若非同批 ship 会产生 merge 面接触。依赖方向已声明为「任意顺序」, 但**落地顺序的 merge 冲突面未评估**。
6. **`.aria/state-checks.yaml` 的 minimal YAML parser 对未知键的行为未验** —— §4 骨架**只用既有 check (当日观测 11 条) 已在用的 7 个键**以规避它, 但「未知键会怎样」这一事实本轮**没有实测**, 只读了 parser 的自陈 (`:63` / `:122-123`)。⇒ 落地时**不得**为本 check 引入新键。

---

## 闸门状态 (Rule #10 — AI 不自行判定)

`audit.checkpoints.post_spec = "convergence"` **enabled**; 封闭豁免白名单四类 (config 显式 off / adaptive_rules 映射 / 已成文 lane 降级 / 结构性前提不成立) **无一适用** ⇒ **本 Spec 按默认跑 post_spec, 不豁免**。

1. **轮次从 R1 起算, 不继承母 Spec 的 R1/R2** —— 那两轮审的是**含旧 §1 的母文本**; 本文件是拆分后的新交付面, 其 §3 抽取规则 / §4 宿主 / §5 allowlist **全部是未经任何席位审过的新文字**。把母 Spec 的轮次算到本文件头上会虚报收敛度。
2. **本 Spec 不是母 Spec 的阻塞前置** (见头部依赖方向段), 也**不阻塞**母 Spec 的 R3。
3. **AI 不预判 R1 的裁决结果。** 本 Spec 在 R1 通过并经 owner 批准前**不进 A.2/A.3**。

**待 owner 裁 (AI 不自行拍板)**:

| # | 事项 | 本 Spec 的落版取值 | 为什么不由 AI 定 |
|---|---|---|---|
| **O-1** | 承 R1 editlist **U-2**: 是否授权回填 6 份 `aria-orchestrator` 轨的 M6/M7 proposal 头部 | **不回填 + `GRANDFATHERED` 具名在册** (D6) | 对**他人在制产物**的写入不能自我授权 (memory `sync≠push-auth` / `feedback_concurrent_feature_collision_claim_before_build`)。⭐ **两方案不互斥**: allowlist 就是「尚未回填清单」, 若 owner 授权回填, **回填一份删一条**, 探针逻辑零改动, 全部回填后 allowlist 为空 ⇒ 选 O-1=回填**不需要**改本 Spec 的任何设计 |
| **O-2** | 字段名维持单一中文 token `关联 Issue`, 还是加英文别名 / 只在中文项目要求 | **单一中文 token** (D9) | SOT 模板 `proposal-minimal.md` 全文为英文且是**跨项目**共享面 ⇒ 英文语境采用方须逐字写中文字段名。这是**跨项目约定**, 属 `standards/` 治理面, 不由单个项目的 Spec 自裁 |
| **O-3** *(round-2 已缩小)* | M-2 的**残余**已知限 —— 脚本随 plugin 分发但**注册须采用方自做** —— 是否就此接受 | **接受, 成文为已知限** (§1 的 ⛔ 段) | round-1 原写的「其他项目拿不到校验」已因 D3 改判**不再成立**, 已订正留痕。残余的「须自行注册」与既有 `issue_cache_freshness_probe` / `coordination_probe` **同形**, 不是本 Spec 独有的新缺口; 消除它 = 自动注册, 会改变「项目自主决定跑哪些 check」的既有语义 ⇒ 属范围决策, 不由 AI 拍板 |

**本 Spec 的全部流程判断已写在上表, 请 owner 复议** (Rule #10: AI 任何自作主张的流程判断必须留痕请复议)。
