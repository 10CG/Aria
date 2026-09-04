---
unverified_claims:
  - claim: "建 `aria-plugin-benchmarks/ab-suite/audit-engine.json` (经 /skill-creator 产出; 2 个 eval: α 每轮入口调用探针并渲染进 `### Round N` / β not_established · exit≠0 · 非 JSON ⇒ 渲染「未能核实」不得「无竞品」不阻断 = SC-16; 产出形态 descriptive) + `ab-suite/version.yaml` MINOR 升版 (计数程序化重算)。B.1 前置 (proposal :473); 建不成 ⇒ 不自判豁免, 原样上呈 owner"
    reason: "symbol 'not_established' unclassified reference form (fail-toward-warn; unclassified_files = ab-results/…/eval-2-…/eval_metadata.json, ab-suite/audit-engine.json — 两者均为 JSON, gate 的符号引用分类器不认 JSON 形态; 该 symbol 在生产代码 aria/skills/audit-engine/scripts/sibling_spec_probe.py 与 references/execution-modes.md 契约节均有真实引用)"
    symbols: ["not_established"]
unverified_ack: false
---
# Proposal: sibling-spec-probe

> **Status**: ✅ **Complete** — Shipped 2026-09-04 (aria-plugin v1.69.0 `2eca24b`, 含 v1.68.2 `4c6489c`; 双远端 master + 两 tag 核验一致; 主仓 PR #191 merged `be4417b`; Rule #6 AB with 8/8 vs old 3/8, +0.62), archived 2026-09-04 by phase-d-closer
> **Created**: 2026-08-25
> **Spec Level**: 2
> **Linked Issue**: `none` — 本 Spec 由母 Spec 的 owner 裁定 (2026-08-23 方向 b「缩 scope」) 拆出, 无独立 issue 号 (2026-08-30 起按姊妹 Spec 的英文 canonical 写, `关联 Issue` / `无` 仍是合法 alias)。与之相关但**不由本 Spec 关闭**的 issue: `10CG/aria-plugin#135` (认领机制三处缺口 — 属母 Spec 主机制面) 与 `10CG/aria-plugin#150` (Rule #6 兜底对无 AB 套件的 skill 不可执行 — 见 §rule6_note)。
> **代码落点**: `aria/` 子模块 `skills/audit-engine/`; Spec 落主仓 (Rule #5)
> **ship target**: ✅ aria-plugin **v1.69.0** (2026-09-04; 档位 MINOR 按 2026-09-01 裁定, 三份串行各占一号)
> **母 Spec**: [`a1-entry-claim-duplicate-work-guard`](../a1-entry-claim-duplicate-work-guard/proposal.md) —— 本 Spec 承接其 **§4 竞品 spec 探针**整节 + 决策记录 **D7/D11** + 旧 **SC-16/17/18/19**。
> **拆分依据**: owner 2026-08-23 裁定 2 (方向 b)。母 Spec 三轮 rework 后 post_spec R2 判 REVISE 未收敛 (3C/17M, major 持平), 主控处置建议第 (2) 条「缩 scope — §4 探针 (M-1/M-5 两簇) 与 §1 抽取规则各自独立成小 Spec」经 owner 采纳。R2 聚合: `.aria/audit-reports/post_spec-R2-1787481000000-a1-entry-claim-rewrite-aggregated.md`。

> **📌 本文件只规定「要建什么」。** 本 Spec 消解的四条审计 finding (R2 簇 **M-1 / M-5 / M-6 的 audit-engine 半 / M-17 的「§4 无 stdout 契约」项**) 与两条 R1 editlist 条目 (**FIX-10 / FIX-19**) 的原始叙事留在各自审计报告内, 本文件**不复述**其历史, 只落结论与可核对锚点。
>
> **📌 「规定是怎么来的」已切出**: 事实断言逐条实读清单 (起草时全部实测命令与输出) 见 **[审计轨](../../../.aria/audit-reports/sibling-spec-probe-audit-trail.md)**。四条声明: ① 本文件只规定「要建什么」; ② 审计轨 **append-only**; ③ 审计轨**显式不维护**与本文件的一致性, 二者不一致**以本文件为准**; ④ **不得**因审计轨的历史记述而回改本文件。
>
> **⚠️ 母 Spec 与本 Spec 是两份独立的收敛面。** 母 Spec 仍在 rework, 其行号与条款会继续变动; 本文件**不引用母 Spec 的任何行号**, 只引用其**小节名与决策编号**。二者不一致时, 探针面以本文件为准。

---

## Why

### 主机制够不到的两类场景

母 Spec 的主机制是 **A.1 入口认领** —— 它在 `refs/aria/coordination` 上写 claim, 用 `linked_issue_overlaps()` 查同 issue 的活跃竞品。它的前提是**双方都走了那个入口**。

有两类场景结构上不满足这个前提:

| 场景 | 主机制为什么够不到 |
|---|---|
| (a) 对方**没走 claim** (历史容器 / 第三方容器 / 未装本插件的轨) | 没有 claim 记录可查 —— 查询方读到的是空集, 而空集与「真的没人在做」不可区分 |
| (b) 对方**已 ship 并归档** | claim 早已 `done`, 被 `_TERMINAL` skip; 而它的产物 (`openspec/archive/<date>-<slug>/proposal.md`) 还在, 且正是「你不该继续做」的最硬证据 |

⇒ 探针换一条完全独立的证据通道: **不看 claim, 直接看远端仓里已落盘的 proposal 语料**。它与主机制**没有共享失效模式** —— 主机制死于「没人写 claim」, 探针死于「没人写关联 Issue 字段」, 两者互不蕴含。

### 第 5 次事故的形态就是 (b)

母 Spec §Why 记载的第 5 次重复劳动: 起草者在 07-31 做修订前没有 fetch, 而并发轨已把同一个 issue 走完十步循环 ship 并归档 —— **三天的修订对象在修订期间已经作废**。主机制对这个形态**结构性无效** (对方 claim 已终态), 而语料通道上那份归档 proposal **一直躺在 `archive/` 里**。

### 语料实测: 这条通道今天就有信号

在主仓**已提交的** `cc1bdef` 上跑本 Spec §3 定义的谓词 (实跑见 §实读清单 #15/#16; 跑已提交树而非工作树, 因为母 Spec 正被另一执笔席并发修改), 147 篇 proposal 语料里存在 **3 个同 key 簇**:

| key | 命中的两份 spec 目录 |
|---|---|
| `("aria-plugin", 95)` | `archive/2026-07-05-aria-archive-gate-runtime-reality` · `archive/2026-07-09-runtime-probe-archive-gate-integration` |
| `("aria-plugin", 122)` | `archive/2026-07-31-phase-c-gate-path-coverage-not-applicable` · `archive/2026-08-22-phase-c-integrator-ci-path-coverage` |
| `("aria-plugin", 137)` | `archive/2026-08-16-premerge-gate-branch-existence` · `archive/2026-08-16-premerge-gate-mainbranch-failclosed` |

**⚠️ 这三个簇里至少有一个不是重复劳动** —— `#137` 那两份是同一个 issue 被有意拆成两份 Spec 交付 (与母 Spec 决策 D-C「同 issue 多方向」同形)。⇒ **「同 issue」≠「重复劳动」**, 这是探针**必须 advisory、必须不阻断**的实证理由 (承接 D11), 而不是一句一般性的谨慎措辞。

**⚠️ 同一次实跑还抓到一个假阳性, 它决定了 §3 层 0 的写法**: 用「行内任意位置匹配」的宽松定位规则时, **母 Spec 自己**会被算进 `#122` 簇 —— 它在 `cc1bdef` 上并没有该字段, 只是正文 `:75` 有一行**嵌套引用的示例** `   > > **关联 Issue**: [10CG/aria-plugin #122](…)`。讨论该字段的 Spec 天然会引用别人的字段行, 于是**探针会把「谈论 X」误判成「在做 X」**。§3 层 0 的行首约束就是为它写的。

---

## What Changes

### §1 探针形态与定位

- **新增** `aria/skills/audit-engine/scripts/sibling_spec_probe.py` —— **stdlib-only**, 无第三方依赖。
  > 实读: `audit-engine` 在 aria `d50f9c3` 上**既无 `scripts/` 也无 `tests/`** (全目录 8 个文件, 见 §实读清单 #28) ⇒ 两个目录都要新建。
- **新增** `aria/skills/audit-engine/tests/test_sibling_spec_probe.py`。
  > 实读: `skills/run_all_tests.sh` 以 `find "$SKILLS_DIR" -type d -name tests | sort` 发现测试目录 (`:48`), 要求目录内至少有一个 `test_*.py` (`:50`), 无 pytest 依赖时走 `python3 -m unittest discover -s . -p "test_*.py"` (`:71`) ⇒ 新目录**会被自动纳入全量套件**, 不需要额外接线。这是「移交给 X」前去 X 源码核过的结论 (memory `delegate-verify`), 不是推断。
- **定位: 副机制 (advisory)**。它**不阻断**任何轮次、不改变收敛判定、不写 claim、不读 claim。

#### 依赖方向 (逐字, 不留隐式前置)

1. **本 Spec 不是母 Spec 的阻塞前置。** 母 Spec 的 A.1 入口认领与 track-id 契约在本 Spec 完全缺席时照常成立; 母 Spec 对探针的唯一依赖是其 §6 缺口表里「legacy 轨 — §4 探针部分覆盖」一行, 该行在本 Spec 未 ship 时**退化为「无覆盖」, 不影响母 Spec 其余任何条款**。
2. **母 Spec 也不是本 Spec 的阻塞前置。** 探针不消费 claim、不消费 track-id、不消费 `linked_issue_overlaps()` 的返回。
   > 母 Spec 旧 **SC-19(b)**「不得把自己的 claim (同 track_id) 计入 overlap」**不迁入本 Spec** —— 它用的是 claim / track_id 词汇, 描述的是主机制 overlap 通道的断言, 与探针语境词汇错配 (post_spec R2 · QA/F5)。该断言留在母 Spec。
3. **姊妹 Spec `linked-issue-field-availability` 的纯函数 `lib/linked_issue_field.py::extract_linked_issue_field` 是本 Spec 的硬前置** (owner 2026-08-30 (R6 后) 裁定 (i), R6 接缝 C2: 「可先于姊妹 ship 全走层 2」与「E0–E6 一条不复制」+「钉死 import」三者不可同时成立 —— 层 0 定位与层 2 的字段行都只有该模块一个宿主)。**ship 顺序 = 姊妹先, 本 Spec 后**; 本 Spec 的 SC-1~15/17~21 宿主 `tests/test_sibling_spec_probe.py` 以该模块存在为前提, 缺席时整套 skip 并报「前置未 ship」。原「能力上限提升项, 非阻塞前置」(2026-08-25) 作废。
4. **前置 Spec `linked-issue-normalization` 已 ship** (v1.67.0, 已归档 `openspec/archive/2026-08-23-linked-issue-normalization/`), 其导出的纯函数 `normalize_linked_issue()` 今天即可 import —— 本 Spec 是它的**第二个消费方**, 不复写归一。

### §2 扫描范围

- **语料 glob**: `openspec/changes/*/proposal.md` 与 `openspec/archive/*/proposal.md` —— **单层目录**, 实测两者合计 147 篇 (§实读清单 #14)。
- **必须含 `archive/`**: 实测三个同 key 簇的 **6 份 proposal 全部在 `archive/` 下**, `changes/` 下为 0 (§实读清单 #16)。⇒ 只扫 `changes/` 的实现在**本 Spec 全部真实语料上返回空集**, 即它在自己的立项理由上失效。
- **扫描的是远端 ref, 不是工作树**: 探针比对的对象是**别人已 push 的产物**; 本轨自己的工作树内容不参与 (自己不是自己的竞品, 见 §7 的 `own_spec_dir` 排除)。
- **ref 维度 (2026-09-01 P11 扩)**: 每个 enforced remote 的全部 `refs/heads/*` (1 条默认 ref + ≤ `MAX_REFS_SCANNED` 条非默认 ref; 取法见 §5(f), 上限 / 去重 / 陈旧过滤见 §6 / P11 / SC-22~25)。

### §3 「同 issue」匹配谓词 (字符级 — M-1)

> **消解 R2 簇 M-1**: 「§4 探针『同 issue』匹配谓词全文未定义」(TL-M4 · QA-M3 · CR)。本节落 R1 editlist **FIX-10** 的 1.5 层。

探针对每份 proposal 产出一个**比较键集合**; 两份的集合**有交集**即命中。集合是**去重的** —— 同一份 proposal 内重复出现的同一个键只计一次, 且一份 proposal **永不是自己的竞品**。谓词分「**层 0 定位** → **按姊妹四态分派** → 层 1 / 层 1.5 / 层 2 / 层 3」, **顺序固定, 不得重排**。

> **📎 上游 SOT 逐字点名**: 层 0 的定位规则与层 1 的 token 解析规则, **本体 SOT 都在姊妹 Spec [`linked-issue-field-availability`](../linked-issue-field-availability/proposal.md) 的 §3「抽取规则 (钉到字符级)」的 E0–E6 七条与其「四态判定 (穷尽, 无第五态)」表**。**本 Spec 一律不另立、不重定义、不复制**; 本节只定义**在那四态之上的分派** —— 即「姊妹判出什么态, 探针把它送进哪一层、产出什么键」。姊妹侧改动四态定义 ⇒ 本节的映射表须同批改。

**层 0 — 字段行定位 (SOT = 姊妹 §3 E0, 本 Spec 逐字采纳其三条谓词)**

姊妹 E0 三条谓词**全部满足**才算命中: (1) **行首锚定, depth 恰为 1** —— 逐字节以 `> **Linked Issue**:` **或** `> **关联 Issue**:` 开头 (姊妹 E0 的两拼写集合, 2026-08-30 起; 集合封闭, 本 Spec 不另加), 行首无任何空白, `>` 后恰一个 U+0020, 禁 `> > ` / 缩进 / 全角冒号; (2) **fenced code block 排除** —— 扫描时维护开合布尔量, 围栏行的匹配式含 `(?:> ?)?` 前缀以覆盖 blockquote 内的围栏; (3) **取文档序第一条**, 其余忽略。三条全不满足 ⇒ 该 proposal 落 `NO_FIELD`。

> **本席独立实测 (与姊妹各自跑, 结论一致 —— 这是收敛信号, 不是互抄)**。本轮在 `cc1bdef` 语料 147 篇上做三臂对照:
>
> | 定位规则 | 分层分布 | 同 key 簇 |
> |---|---|---|
> | 宽松 (行内任意位置匹配 `**关联 Issue**:`) | `no_field` 132 / `url_fallback` **14** / `no_token_no_url` 1 | 3 个, 其中 `#122` 簇**混入母 Spec 这个假阳性** |
> | **行首 `> ` 逐字** (= 姊妹 E0 谓词 1) | `no_field` **133** / `url_fallback` **13** / `no_token_no_url` 1 | 3 个, **假阳性消失**, 三个真簇一个不少 |
> | (反面对照) 再加「只在首条 `---` 之前找」 | `no_field` 136 / `url_fallback` 10 / `no_token_no_url` 1 | **只剩 1 个** —— 真簇里的 `#122` 与 `#95` 被误杀 |
>
> - **谓词 1 的必要性**: 母 Spec 在 `cc1bdef` 上**自己没有**该字段, 却因 `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:75` 的一行嵌套引用 (`   > > **关联 Issue**: [10CG/aria-plugin #122](…)`, depth 2 + 前导空白) 被宽松规则误算进 `#122` 簇。**讨论该字段的 Spec 会引用别人的字段行, 于是探针会把「谈论 X」读成「在做 X」** (同族形状: memory `reference_secret_guard_false_positive_on_spec_docs`);
> - **反面对照必须列出**: 「只扫头部区」是最容易想到的加固, 而它砍掉三分之二的真信号。**姊妹席独立否决了同一方案**, 点名的是同两份文件 `openspec/archive/2026-08-16-premerge-gate-branch-existence/proposal.md:61` 与 `openspec/archive/2026-08-16-premerge-gate-mainbranch-failclosed/proposal.md:45` (字段落在超长头部 blockquote 的第 61 / 45 行)。**两席各自实测、各自否决、点名同一组文件**;
> - **谓词 2 (围栏排除) 是本 Spec 采纳姊妹的, 不是本席实测的**: 本席三臂里没有围栏臂。姊妹以合成夹具 `j-bq-fence` 实测「不加 ⇒ `OK`(假阳性) / 加 ⇒ `NO_FIELD`(正确)」, 且在真实语料上加与不加的**判定差异 = 0** (两次逐份对跑, 147 与 149 份均为 0)。⇒ **代价为零、收益非零, 本 Spec 采纳**。姊妹侧原文写「不要求探针 Spec 加这条, 只点名」—— 本席仍加, 理由是**两份 Spec 各留一个定位器就是 seam 本身**, 而不是因为它在今天的语料上有差异。

**层 1 分派 — 姊妹四态 × 本 Spec 的层归属 (逐格, 无第五态, 不留推断)**

> **消解 SEAM-2** (主控 2026-08-25 核验): 上一版本节声明消费契约是**三态** (`TOKEN(s)` / `无` / `NO_TOKEN`), 而姊妹 §3 定义的是**四态**且 `OK` 同时覆盖 `无` 与真 token ⇒ 产 4 消 3, 映射未定义。下表逐格补全。

| 姊妹 verdict | 附加判据 | 本 Spec 走哪一层 | 产出的比较键 | `own_layer` / `hits[].layer` 枚举值 |
|---|---|---|---|---|
| `NO_FIELD` | — | **层 3** (不可见) | ∅ | `"no_field"` |
| `NO_TOKEN` | — | **层 2** (URL 回落) | 该字段行内全部 `/<org>/<repo>/issues/<n>` 片段成键; 无片段则 ∅ 并落层 3 | `"url_fallback"` (无片段时 `"no_token_no_url"`) |
| **`BAD_TOKEN`** | — | **层 1 与层 2 都跑, 取并集** | 层 1: 逐 token 元素成键 (可解析→归一键, 不可解析→原串键) **∪** 层 2: 该行 URL 片段成键 | `"bad_token_union"` (2026-08-30 统一拼写, 与 §7 `own_layer` 一致) **⚠️ R4/C-M3 + 姊妹 K8 交叉补 (2026-08-27, 未经审计轮)**: 层 1 的**原串键** `("r", t)` 对**常量串无守卫** —— 两份都还没填 issue 号的 proposal, 其字段值都是 SOT 模板的 placeholder `` `{<org>/<repo>#<n>}` `` (判 `BAD_TOKEN`), 原串相等 ⇒ **互相命中**, 与姊妹 Spec 的 NEW-01 同形且**什么都不做就中**。**落版**: 原串键**排除一个成文的常量黑名单** —— 至少含 SOT 模板 placeholder 的逐字串与姊妹 §2 的哨兵集合 (`none` 大小写折叠后 / `无`); 命中黑名单的 token 元素**不产生任何键**。黑名单逐字内容与姊妹 Spec §3 的模板默认值**同源**, 任一改动须同批改另一侧。**新增 SC-19**: 两份 proposal 字段值均为该 placeholder ⇒ **不命中**; 照产原串键的实现必红 |
| `OK` | token 串为**哨兵** (姊妹 §2 集合 `{none, 无}`: `none` 按 ASCII 大小写折叠 / `无` 逐字节) | **层 1.5** | **∅** (且**不进**层 2) | `"none_sentinel"` (原 `"wu_empty"`, 2026-08-30 改名) |
| `OK` | 其余 (token 串非哨兵) | **层 1** | 逐 token 元素 (姊妹 E4: 按 ASCII `,` split 后各段 `strip()`) 成键 | `"canonical"` |

- **层 2 的触发集逐字 = {`NO_TOKEN`, `BAD_TOKEN`}**, 且仅当。**不是**「canonical 集合为空」—— `OK`+哨兵 的集合也是空的, 但它**不得**回落 (层 1.5 的整个存在理由);
- **`OK` 的两分靠什么区分要写死**: 靠**姊妹 E3 的 token 串本身** (未 strip) 判是否为哨兵: 逐字节等于 `无` (单个 U+65E0), 或 ASCII 大小写折叠后等于 `none`, 两端无空白 (姊妹 §2 集合 + E5 原文; R6/CR 探针 M1 同步旧句「只比 `无`」), **不靠**归一结果、**不靠**集合是否为空。

**`BAD_TOKEN` 的归档选择与理由 (主控要求明确选一档并写出来)**

**选择: 层 1 与层 2 都跑, 取并集** —— 即**采纳姊妹席的建议 (「`BAD_TOKEN` 应触发 URL 回落」) 并在其上追加一条 (层 1 已解析出的元素不丢弃)**。姊妹要的那一半原样保留, 因此**姊妹侧四态定义无需任何改动**。

两个反例各自否掉一个单层方案 (本轮实跑, 用 `d50f9c3` 的真实 `normalize_linked_issue`):

| 反例 | 字段行 | 姊妹判定 | 只走层 2 (姊妹建议) | 只走层 1 | **并集 (本 Spec)** |
|---|---|---|---|---|---|
| **A** — 有效号 + 坏元素 | `` > **关联 Issue**: `10CG/aria-plugin#122, TBD` — 第二个待定 `` | `BAD_TOKEN` (元素 `TBD` → `None`) | **∅ — 竞品 `#122` 丢失** ❌ | `{("k","aria-plugin",122), ("r","TBD")}` ✅ | `{("k","aria-plugin",122), ("r","TBD")}` ✅ |
| **B** — 元素全坏 + 行内有 URL | `` > **关联 Issue**: `TBD` — 讨论见 https://forgejo.10cg.pub/10CG/aria-plugin/issues/122 `` | `BAD_TOKEN` | `{("k","aria-plugin",122)}` ✅ | **`{("r","TBD")}` — `#122` 丢失** ❌ | `{("k","aria-plugin",122), ("r","TBD")}` ✅ |

⇒ **两个单层方案各有一个假阴性, 并集两个都过。** 探针的极性是 fail-toward-reporting (假阳性花人一眼, 假阴性花人几天), 故取并集。

> **⚠️ 对姊妹席「反向不成立」那条论证的回应 (不是反驳, 是澄清两个不同的面)**: 姊妹原文写「若探针把 `BAD_TOKEN` 映射成 `TOKEN(s)`, 脏元素会直接进它的比较键集合 —— 与它自己 §3 层 2 的『绝不把脏串喂进主机制匹配面』逐字冲突」。**这两处说的不是同一个面**: 本 Spec 那条禁令的对象是 **`--linked-issue` 实参**(主机制的匹配面), 而 `BAD_TOKEN` 的脏元素进的是**探针自己的只读比较键集合**。脏元素在其中落**原串键** `("r","TBD")`, 它与任何归一键**永不相等** (首元不同, 本轮实跑核过), 只能与逐字节相同的另一个原串键命中 —— 这正是 `normalize_linked_issue` docstring 逐字要求的 `None` 回落语义。**`--linked-issue` 实参由姊妹 E6 单独规定, 本 Spec 一个字都不碰** ⇒ 冲突不成立, 姊妹那条禁令与本选择可以并存。

> **⛔ 本 Spec 不得内含第二份抽取实现 (E0–E6 一条都不复制)。**
>
> **⚠️ 该约束的实现归属 (R3/C3 订正, 主控 2026-08-25)**: R3 判定「三条约束 (逐字采纳姊妹 E0 ∧ 不得内含第二份实现 ∧ 不改 state-scanner) **不可同时满足**」—— 姊妹 round-1/2 的唯一宿主是**无导出 API 的 CLI check** (作用域还写死 `changes/`), 而本 Spec 要在**远端 ref 的 blob** 上求四态。
> **处置**: 姊妹 Spec 已同批承诺把 E0–E6 交付为**可 import 的纯函数** `lib/linked_issue_field.py::extract_linked_issue_field(text: str) -> FieldVerdict` —— **输入是文本 blob 而非路径**, 正是为本 Spec 的调用形态定的; 本 Spec **import 它**, 一条都不复制。
> **⇒ 依赖方向 (owner 2026-08-30 (R6 后) 裁定 (i), 取代 2026-08-25「可先于姊妹 ship」的旧措辞)**: 本 Spec **不可**先于姊妹 ship —— 姊妹的 `lib/linked_issue_field.py` 是硬前置 (§1 第 3 条); 本 Spec 的层 0 / 层 1 / 层 1.5 / 层 2 全部经该纯函数取四态, **不存在**「层 1 恒 `NO_TOKEN` 全走层 2」的过渡形态。旧文「可先于姊妹 ship —— 此时层 1 恒 `NO_TOKEN`、全部走层 2; 姊妹 ship 后必须改为 import 该纯函数」作废 (它在实现层为假: 没有该模块时层 0 定位无宿主, R6/CR 接缝 C2)。
> **⚠️ 本条是 R3 之后新增的订正 (未经审计轮) —— 请审计席优先审 (R4–R6 已审)。**
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
> import sys
> from pathlib import Path
> _SS_ROOT = str(Path(__file__).resolve().parents[2] / "state-scanner")                 # 供 lib.* (Layer L)
> _SS_SCRIPTS = str(Path(__file__).resolve().parents[2] / "state-scanner" / "scripts")  # 供 collectors.*
> for _p in (_SS_SCRIPTS, _SS_ROOT):   # 顺序承重: 最后插入的 _SS_ROOT 排在 sys.path 最前 (R6/BA 探针 M1)
>     if _p not in sys.path:
>         sys.path.insert(0, _p)
> from lib.collision import normalize_linked_issue              # 解析到 state-scanner/lib
> from lib.linked_issue_field import extract_linked_issue_field
> from collectors.multi_remote import resolve_enforced_remotes   # 解析到 state-scanner/scripts/collectors
> ```
> **已知限 (成文; R6/BA 探针 M1 订正 —— 同名碰撞的另一方**今天就存在**, 不是「将来」)**: `state-scanner/scripts/lib/` 是一个既有的、带 `__init__.py` 的包 (含 `runtime_probe.py` 等), 与 `state-scanner/lib/` (Layer L, 含 `collision.py`) **同名**; `coordination_probe.py:80-85` 为同一根因绕开过一次。上面代码块的插入顺序是**承重的**: 若 `_SS_SCRIPTS` 排在 `_SS_ROOT` 之前, `import lib.collision` 会静默绑定到 `scripts/lib` 并 `ModuleNotFoundError` (BA 席在 /tmp 按 `git archive d50f9c3` 树实跑复现: 安全顺序全过, 反序必炸)。⇒ **实现约束**: (1) 两条路径的插入与三条 import **只在这一个代码块里出现一次**, 不得拆到两处各写各的; (2) 绑定 `lib` → `state-scanner/lib` 之后**不得**再 import `scripts/lib` 下任何模块 (`lib.runtime_probe` 等); (3) `audit-engine` 内不得新建名为 `lib/` 或 `collectors/` 的顶层目录, 探针自己的 helper 一律放 `scripts/` 下并用模块名前缀; (4) **由 SC-21 (代码) 钉住**。
> 若 `audit-engine` 将来自己长出 `lib/` 或 `collectors/`, 会与之**同名冲突** (`coordination_probe.py:80-83` 点名过同名包陷阱)。
> ⇒ **A.2 的一条显式约束**: `audit-engine` 内**不得**新建名为 `lib/` 或 `collectors/` 的顶层目录; 探针自己的 helper 一律放 `scripts/` 下并用模块名前缀。
> **降级说明**: R4/S-1 原判 Critical 的依据是「无先例 ⇒ 不可行」; 前提被推翻后, 真实缺陷是「**没给 import 代码**」—— 本段即补上, 严重度按 Major 处置。

> **姊妹 Spec 未 ship 时的行为 (owner 2026-08-30 (R6 后) 裁定 (i) 后)**: **不定义** —— 本 Spec 不在姊妹之前 ship (硬前置); 若实现者在姊妹模块缺席的环境下跑探针, import 失败按 §7 「探针自身失败」处置 (非 0 exit, stdout 不保证 JSON), 消费面按「未能核实」。历史观测保留供参考: 基线 `cc1bdef` 上经层 0 定位到的 14 行字段中冒号后首个非空白是反引号的 = 0 行 (§审计轨 #14) —— 即姊妹 ship 前 canonical 层无输出; 该事实只影响「探针上限」, 不再构成一条独立的运行形态。

**层 1.5 — 哨兵 (`none` / `无`) 的归属 (承重, 勿省 — FIX-10; 集合定义在姊妹 §2, 本 Spec 引用)**

姊妹判 `OK` **且** token 串为哨兵 (`无` 逐字节, 或 `none` 按 ASCII 大小写折叠) ⇒ 该 proposal 的比较键集合为 **空集 ∅**, 且**不触发**层 2 的 URL 回落。

- 哨兵的语义是「已核实无关联」(**正证据**), 与 `NO_TOKEN` 的「读不到」(**零证据**) 是两回事, **不得**合并处置;
- ∅ 与任何集合无交集 ⇒ **两份写哨兵的 proposal 永不互相命中** (不论各写 `none` 还是 `无`)。

> **这一层是承重的, 有实测证据, 不是推理**: `normalize_linked_issue("无")` 返回 **`None`** (§审计轨 #15 实跑)。而该函数 docstring 逐字要求「Callers must fall back to raw-string equality on `None` — never treat `None` as "no match"」⇒ 若把 `无` 当普通 token 送进比较, 它会落到**原串相等**分支, `"无" == "无"` ⇒ **两份 `无` 互相命中**。层 1.5 缺席时的失效是必然的, 不是概率的。`none` 同理 (无 `#` ⇒ `normalize_linked_issue` 必返 `None` ⇒ 原串相等 `"none" == "none"` 命中), 且 `none` 是英文作者最自然的写法, 触发面比 `无` 更宽。

**层 2 — URL 回落层 (仅探针用)**

姊妹判定 ∈ {`NO_TOKEN`, `BAD_TOKEN`} 时 (**且仅当**), 从该 proposal 的**「关联 Issue」字段行本身**提取全部形如 `/<org>/<repo>/issues/<n>` 的片段, 每个片段组成 token `<org>/<repo>#<n>` 后按下方规则成键。

- **只扫字段行, 不扫全文散文** —— 扫全文会把任何提到过 issue URL 的 proposal 全部拉进匹配面;
- **触发条件逐字是「姊妹判定 ∈ {`NO_TOKEN`, `BAD_TOKEN`}」, 不是「canonical 集合为空」** —— 两者在 `OK`+`无` 上取值相反 (集合都为空, 但一个该回落一个不该);
- **⛔ 作用域分离是承重的**: URL 回落**只用于探针的只读比对**, **绝不**用于产生 `--linked-issue` 实参 —— 后者由姊妹 E6 单独规定 (E6 四态表: 「只有 `OK` 且非哨兵那一格产生实参, 哨兵 / `BAD_TOKEN` / `NO_TOKEN` / `NO_FIELD` 一律整参省略」—— R6/CR 探针 M1 订正旧引述)。混用会把脏串喂进主机制的匹配面。姊妹 §3 与本条**互为镜像, 任一被改必须同批改另一侧**。

**层 3 — 各层都没产出键 ⇒ 该 proposal 对探针不可见**

**不猜标题、不猜 slug、不做模糊匹配。** 落 §10 盲区, 不假装覆盖。

**比较键的构造 (钉到字符级, 供两人独立实现得同一结果)**

对每个 token (层 1 的 token 元素 / 层 2 的 URL 片段所组 token) `t`:

```
k = normalize_linked_issue(t)
键 = ("k", k[0], k[1])   若 k is not None      # 归一键
键 = ("r", t)            若 k is None          # 原串键 (fail-toward-reporting)
```

- 两类键**永不相等** (首元 `"k"` / `"r"` 不同) ⇒ 归一失败的值只与**逐字节相同**的另一个归一失败值命中, 与 `normalize_linked_issue` docstring 的 `None` 回落契约同义;
- `normalize_linked_issue` 的**确切签名与返回契约**实读见 §审计轨 #1: `def normalize_linked_issue(value: str) -> "Optional[tuple[str, int]]"`, key = `(repo_basename, number)`, **org 不参与**, 三类不可解析值返回 `None`;
- **多元素**: 一份 proposal 的多个 token 元素各自成键, 全部进该 proposal 的集合 (探针是集合求交, 不受姊妹 E6「`--linked-issue` 只取第一个元素」的限制)。

**自检 (可证伪, 已实跑)**: 以 `openspec/archive/2026-07-31-phase-c-gate-path-coverage-not-applicable/proposal.md:6` 与 `openspec/archive/2026-08-22-phase-c-integrator-ci-path-coverage/proposal.md:22` 两行字段原文为夹具 —— 两者姊妹判定均为 `NO_TOKEN` (冒号后首个非空白是 `[`), 经层 2 均得键 `("k","aria-plugin",122)` ⇒ **命中**。实跑输出见 §审计轨 #15。

### §4 「各自默认分支」的取法 (fail-closed — M-5a)

> **消解 R2 簇 M-5 前半**: 「§4『各自默认分支』取法未定义 (本仓 `github` remote 无 symbolic-ref 复现)」(BA-M2 · QA-M7 · KM-M6 · CR)。

**步骤 1 — remote 集合从哪来**

复用已 ship 的纯函数 `resolve_enforced_remotes(configured, actual_remotes, read_only)` —— **`read_only` 的来源**: `.aria/config.json` 的 `state_scanner.multi_remote.read_only_remotes` (缺省空元组; 实读 `collectors/multi_remote.py:1376` 生产调用即如此取值, R6/CR 探针 m3 钉来源) (`skills/state-scanner/scripts/collectors/multi_remote.py:255-286`, 实读见 §实读清单 #12), 其中:

- `configured` = `.aria/config.json` → `state_scanner.multi_remote.enforced_remotes` (**本仓实测该段为 `null`** ⇒ 走该函数的 auto-discover 分支);
- `actual_remotes` **必须**取自 `git remote` 的输出 (**配置面**), **禁止**取自 `refs/remotes/*` 的目录名 (**ref 面**)。

> **⚠️ 这不是洁癖, 本仓当场可复现**: `git remote` 输出 `github` / `origin` 两个; 而 `refs/remotes/` 下有 **三个**名字 —— 多出的 `probe` 来自一个已从 config 中移除的 remote (`git config --get remote.probe.url` 空且 exit 1)。用 ref 面枚举的实现会对一个不存在的 remote 跑网络操作, 并可能读到**永远不会再更新的陈旧 ref**。实跑见 §实读清单 #11。

- 解析结果为**空集** (无 remote / 全部落 `read_only`) ⇒ `status="skipped"`, `reason="no_enforced_remote"`, `verdict="not_established"`, **exit 0**。

**步骤 2 — 默认分支只认远端实时应答**

对每个 remote `R` 逐字执行:

```
git -C <repo> ls-remote --symref R HEAD
```

从其 stdout 取**第一条以 `ref: ` 开头的行**, 按**制表符**切成两段, 第一段去掉前缀 `ref: ` 得完整 ref; 该 ref **必须**以 `refs/heads/` 开头, 去掉该前缀即默认分支名。

**实测 (本轮实跑, 2026-08-25)**: 本仓两个 remote 与 `aria` 子模块的 `github` 上, 该命令均返回 `ref: refs/heads/master<TAB>HEAD` (§实读清单 #5/#6/#8)。

**步骤 3 — fail-closed, 不猜**

上述任一步不成立 (子进程非 0 / 超时 / 无 `ref: ` 行 / 前缀不符) ⇒ 该 remote 记 `default_branch: null` + `error_kind` 非空, **不得**回落到字面 `master` / `main`; 整体 `status` 降 `degraded`, `verdict="not_established"`。

> **为什么不复用既有的 `_resolve_default_branch`**: `skills/phase-d-closer/scripts/fetch_gate.py:108-128` 有一份现成的默认分支解析器, 但它 (a) **origin 硬编码** (`_ORIGIN_HEAD_REFS` 三个候选全是 `refs/remotes/origin/*`, `:50-54`), 对多 remote 不可用; (b) 末端是 **`_DEFAULT_BRANCH_FALLBACKS = ("master", "main")` 名字猜测** (`:55`, `:124-127`) —— **猜测形态与本 Spec 的 fail-closed 要求方向相反**。实读见 §实读清单 #23。⇒ **不复用, 也不复制。**

**步骤 4 — 本地 symbolic-ref 不作为替代, 也不作为加速旁路**

```
git symbolic-ref refs/remotes/origin/HEAD   → refs/remotes/origin/master   (exit 0)
git symbolic-ref refs/remotes/github/HEAD   → fatal: ... is not a symbolic ref  (exit 128)
```

两条实跑 (§实读清单 #3/#4; `aria` 子模块同款故障见 #7) 证明: **CLAUDE.md 明文要求双推的 `github` 这个 remote 上, 本地符号引用根本不存在**。且本机 `git version 2.39.5` 的 `git-fetch` **无 `followRemoteHEAD`** (man 页 grep 命中 0, §实读清单 #9) ⇒ **fetch 不会补写该 ref**。

> **即使它存在也不能用**: `refs/remotes/<R>/HEAD` 是 clone 时一次性写入、此后不随上游改名更新的**本地状态**。用它等于「测量新鲜度」而非「获取新鲜度」(memory `feedback_freshness_must_be_fetched_not_measured`), 会静默给出陈旧答案 —— 而默认分支改名恰恰是**静默失败**的典型。

### §5 fetch 代价与超时预算

**探针自带 fetch, 且它不轻量。**

**(a) 承接自母 Spec 的 spike S2 实测 (历史一次性测量, 非本轮复跑)**

| 项 | S2 实测 |
|---|---|
| 双远端 fetch ×5 | 12.5 / 13.4 / 14.1 / 15.9 / 13.0 s (均值 **~13.8s**) |
| 3 轮审计净增 | ~41s |
| 瞬时失败 | 该会话内 github 2 次 SSH 失败, 重试即恢复 |

**(b) 本轮新增的网络腿 (本 Spec 引入, 2026-08-25 实测, 各一次采样)**

| 命令 | 耗时 |
|---|---|
| `git ls-remote --symref github HEAD` | **4.5s** |
| `git ls-remote --symref origin HEAD` | **6.0s** |
| `git remote show github` (仅作对照, **不采用**) | 4.3s |

⇒ §4 步骤 2 给每轮**新增约 10.5s** 的网络时间 (2 remote), 叠加在 S2 的 ~13.8s fetch 之上。**这是本 Spec 引入的新成本, 明写, 不摊进 S2 的旧数字。**

**(c) 本轮实测的本地代价 (对比用, 说明瓶颈在哪)**

| 操作 | 耗时 |
|---|---|
| 单 ref 上枚举全部 proposal (`git ls-tree`) | **5ms** (147 条) |
| 单 ref 上抽全部字段行 (`git grep`) | **12ms** (15 行) |

⇒ **本地解析不是瓶颈, 全部成本在网络腿。**

**(d) 预算与重试**

- **超时是「每个 git 子进程各 30s」, 不是整轮总预算 30s** —— 母 Spec 的「30s 超时预算」未指明作用域, 若当成整轮总预算, 按 (a)+(b) 本仓单轮就会必然超时;
- 每个 remote 的 `fetch` 腿最多尝试 **2 次** (1 次重试), 每次独立计 30s。理由是 S2 观测到的瞬时 SSH 失败重试即恢复; **P11 扩后** (2026-09-01) 单次 fetch 取全部 `refs/heads/*` (带 `--prune`), 冷仓耗时高于单分支形态 —— 仍**不加长** 30s, 超时按 `degraded` 处置 (fail-closed 极性不变);
- 超时 / 失败 ⇒ 该 remote `error_kind` 非空 + `status="degraded"` + `verdict="not_established"`, **不阻断**, exit 0。

**(e) 不复用 `remote_refresh` 缓存 (承接 D7)**

缓存的唯一写入点是 `remote_refresh.py:691` 的 `_write_cache_atomic(...)`, 它在 `collect_remote_refresh()` (`:568`) 内; 而该函数的**唯一生产调用点是 `scan.py:312`** (Phase 0.5, `/state-scanner` 入口)。实读见 §实读清单 #22。

⇒ audit-engine 的轮间**没有任何机制保证跑过 `/state-scanner`** ⇒ 跨天审计会读到首轮的陈旧缓存 —— **正是本 Spec 要治的病换条更深的路径复现**。

**(f) fetch 写进私有 ref 命名空间**

```
git -C <repo> fetch --no-tags --prune R +refs/heads/*:refs/aria/sibling-probe/R/*
```

- **不动共享的 `refs/remotes/*`** (避免与并发的 `/state-scanner` 互踩), **不依赖全局 `FETCH_HEAD`** (它是全局单槽, 并发下会被覆盖);
- `refs/aria/*` 是本仓既有的私有命名空间 (实测现存 3 条: `refs/aria/coord-check` / `refs/aria/coordination` / `refs/aria/coordination-remote`, §实读清单 #27)。

### §6 规模上限与 no-silent-caps

- **ref 维度**: 每个 enforced remote = **1 条默认 ref + ≤ `MAX_REFS_SCANNED` 条非默认 ref** (探针自有常量, **默认 100**; 2026-09-01 P11 扩; 原「恰 1 条 ref, 无需额外 cap」随之作废) ⇒ 非默认 ref 数走 SC-25 的 no-silent-caps;
- **语料维度** (**⚠️ 2026-09-03 Amendment A1 修订计数单位, 见文末**): **单 remote 上跨其全部 ref 累计**参与扫描的 proposal 数上限 = 探针自有常量 `MAX_PROPOSALS_SCANNED`, **默认 1000** (2026-09-01 P11 扩后由「单 ref」改为「单 remote 累计」: 默认 ref 先计, 超限从枚举序尾部截断 ⇒ 分支语料先被截; 全轮总量 ≤ |enforced_remotes| × 1000, 防失控语义不变)。
  > 依据: 本仓实测单 ref 147 篇、抽取 12ms ⇒ 1000 仍是亚秒级。cap 的作用**不是性能, 是防失控** (第三方仓语料规模未知 / glob 误配)。
- **排序 (决定性, 供两人独立实现得同一截断点)**: 先 `openspec/changes/*/proposal.md`, 后 `openspec/archive/*/proposal.md`; 各自按**完整路径的字节序** (`LC_ALL=C` 语义) 升序。超限**从尾部截断**。
  > 为什么 `changes/` 排前: in-flight 的竞品住在 `changes/`, cap 触发时**绝不能先丢掉它们**。
- **no silent caps**: 触发 cap ⇒ (i) stderr `log()` 逐字披露被丢弃的范围 (截断点路径 + 丢弃条数); (ii) stdout `caps_applied[]` 非空; (iii) `status` 降 `degraded`, `verdict="not_established"`。
- **⛔ 不复用 `state_scanner.handoff_multibranch.max_branches` 这个旋钮。** 同库 `handoff_multibranch.py` 因 440 条远端分支踩坑后做过 scan cap (承接自母 Spec 的历史记述), 其披露形态 (`soft_error` + `log.warning` + 逐字消息, 实读 `:589-598`) 值得照抄, 但**旋钮本身不可复用** —— 它的作用域是「分支数」, 与本 cap 的作用域「单 ref 上的 proposal 数」不相等。用作用域不匹配的开关会把恒红换成假绿 (memory `knob-granularity`)。 **⚠️ 2026-09-01 P11 后补**: 新增的 `MAX_REFS_SCANNED` 作用域确与该旋钮相同 (分支数), **仍不复用** —— 第二条理由与作用域无关: 该旋钮属 `state_scanner` 配置树, 探针不读 state-scanner 的 config key (Impact「不改 state-scanner」), 且两者降级语义不同 (那边 `soft_error`, 这边 `verdict=not_established`)。

### §7 stdout / exit code / stderr 契约 (M-17)

> **消解 R2 簇 M-17 的「§4 无 stdout 契约」一项** (CR/M6): 「exit code 三分意味着调用方只能靠 stdout 区分命中与否, 而全文没有定义任何输出格式」。

**stdout — 恰一个 JSON 对象, 无其他任何字节**

| 字段 | 类型 | 语义 |
|---|---|---|
| `schema_version` | `str` | 固定 `"1"`; 消费方读到未知值须按「未能核实」处置, 不得猜 |
| `probe` | `str` | 固定 `"sibling_spec_probe"` |
| `status` | `str` | `"ok"` \| `"degraded"` \| `"skipped"` —— **运行面**: 覆盖是否完整 |
| `reason` | `str \| null` | **`status != "ok"` 或 `verdict == "not_established"` 时必非空** (二者是**或**关系 —— `own_keys` 为空时运行面一切正常 `status="ok"`, 判定面却是 `not_established`, 只写「status 非 ok 才要 reason」会让这一格恒空); 枚举 `"no_enforced_remote"` \| `"remote_unresolved"` \| `"fetch_failed"` \| `"cap_applied"` \| `"own_token_absent"` |
| **`verdict`** | `str` | **判定面 (一等字段)**: `"sibling_found"` \| `"no_sibling_found"` \| `"not_established"` |
| `own_spec_dir` | `str` | 本轨 spec 目录名 (自命中排除键) |
| `own_layer` | `str` | 本轨 proposal 走了哪一层: `"canonical"` \| `"none_sentinel"` (原 `"wu_empty"`, 2026-08-30 改名 —— 拼音 hack 换成语义名, 与姊妹哨兵集合同批) \| `"url_fallback"` \| `"no_token_no_url"` \| `"no_field"` \| **`"bad_token_union"`** (**R3/TL-P2 补**: §3 的 `BAD_TOKEN` 走「层 1 ∪ 层 2」并集分支, 该取值原未传导进本枚举 ⇒ 消费方按 5 值枚举做穷尽匹配时会落空; 现补为第 6 值) **⚠️ R4/C-M1 拼写统一**: 本枚举值逐字为 `"bad_token_union"`, §3 映射表 2026-08-30 已改为同一拼写 (R3/TL-P2 只修了一侧, R4 又只加批注没改表 —— 全文自此只有一种拼写) |
| `own_keys` | `list` | 本轨比较键 (每项 `["k",<basename>,<n>]` 或 `["r",<原串>]`) |
| `remotes` | `list[obj]` | 每 remote 一项: `name` / `default_branch` (`str\|null`) / `resolved_by` (`"ls_remote_symref"\|null`) / `error_kind` (`str\|null`) / `scanned` (`int`) / `capped` (`bool`) / `refs_scanned` (`int`, P11 2026-09-01) / `stale_skipped` (`int`, P11) |
| `hits` | `list[obj]` | **恒为 list, 永不为 `null`**; 每项 `remote` / `branch` / `corpus` (`"changes"\|"archive"`) / `spec_dir` / `path` / `field_line` (`int`) / `key` / `layer` / `refs` (`list[str]`, `R/<branch>` 全部命中处, 字节序; P11 2026-09-01) |
| `caps_applied` | `list[obj]` | 每项 `remote` / `total` / `kept` / `dropped_from` (`kind="proposals"` 时为截断点**路径**; `kind="refs"` 时为首个被丢弃的 **`R/<branch>`**) / `kind` (`"proposals"` \| `"refs"`; P11 2026-09-01) |
| `elapsed_ms` | `int` | 探针总耗时 |

**`verdict` 是一等字段, 不让消费方从 `hits == []` 推断 —— 这是本节的承重条款:**

| `verdict` | 何时取该值 |
|---|---|
| `"sibling_found"` | `hits` 非空 |
| `"no_sibling_found"` | `hits` 为空 **且** 覆盖完整 (全部 enforced remote 均解析出默认分支、fetch 成功、其全部 `refs/heads/*` 均已枚举、未触发**任一 kind** 的 cap) **且** `own_keys` 非空 |
| `"not_established"` | 其余全部情形 —— 含 `own_keys` 为空 (本轨无可比较的输入)、任一 remote 未解析 / fetch 失败、cap 触发 (任一 kind)、enforced 集合为空。**`stale_skipped > 0` 不降级** (陈旧副本是被抑制的重复项, 不是未覆盖的语料; P11 2026-09-01 逐字成文以免两人分歧) |

> **它消解的是同一族的病**: `hits == []` 在「已完整扫过, 确实没有竞品」与「根本没扫到 / 本轨没有输入」两种情形下取值相同 —— 让消费方从它推断结论, 就是把**零证据当正证据**。母 Spec 的四态契约 (决策 D-F) 在 claim 通道上解同一个问题; 本节是同一纪律在探针输出面的落点, **不是新机制**。

**exit code**

| exit | 语义 |
|---|---|
| `0` | 探针完成了**一次有定义的判定** —— `verdict` 三值之一已写入 stdout。**命中与不命中都是 0** (命中不是错误) |
| 非 `0` | **仅**探针自身失败 (参数错 / 内部异常 / 仓库不可读)。此时 stdout **不保证**是合法 JSON |

> **勘正母 Spec 旧 SC-18**: 旧 SC-18 写「探针 fetch 失败 / **无远端** ⇒ ... **exit 非 0**」, 与决策 D11「非 0 **仅**用于探针自身失败」正面冲突 (post_spec R1 · CR/M6 + R2 · TL/m4)。**冲突按 D11 解**: fetch 失败 = `degraded` + exit 0; 无远端 = `skipped` + exit 0。否则**无远端的项目每轮恒非 0**, 该信号立刻退化成噪声 (memory `feedback_false_green_dual_is_permanent_red`)。旧 SC-18 在本 Spec 拆成 SC-3 / SC-4 两条。

**stderr**

- 人读日志 + `log()` 披露 (每 remote 的解析与 fetch 结果、cap 丢弃范围、各腿耗时);
- **stderr 的任何内容不得混入 stdout** —— 混入即破坏 stdout 的「恰一个 JSON 对象」契约;
- **⛔ 不得回显 git 的原始 stderr**: remote URL 可能内嵌凭据。错误一律映射为稳定的非 secret 枚举 `error_kind`, 形态照抄同库既有先例 `fetch_gate.py:86-101` 的 `_classify_error` (`network` / `auth_403` / `non_ff` / `git_missing` / `other`; 其 docstring 逐字写明「Raw stderr is intentionally never returned — remote URLs in stderr may embed credentials」, 实读见 §实读清单 #23)。这同时是 CLAUDE.md **Rule #7** 在本 Spec 的落点。

### §8 per-round 入口: 命名与两模式落点

**命名 = 「per-round 入口探针」, 不叫「Step 0.5」。**

> 实读 `audit-engine/SKILL.md:83` 是 `### Step 0: Anchor 固化 (Drift Guard #17, v1.44.0)`, `:85` 逐字「入口逻辑完成后、**Round 1 启动前一次性**执行」(§实读清单 #18) ⇒ 把一个**每轮**跑的东西挂在它旁边并沿用它的编号, 与「每轮」自相矛盾。

**落点 = `references/execution-modes.md` 的两个模式块, 两块都改。**

| 模式 | 节标题行 | 插入位置 | 插入的字面串 |
|---|---|---|---|
| Convergence | `## Convergence 模式` (`:84`) | 围栏块内 `Round N:` 行之后、现有 `1. 调用 agent-team-audit 单轮引擎` 之前 | 下方「插入串 (两行, 逐字)」 |
| Challenge | `## Challenge 模式` (`:113`) | 围栏块内 `Round N (一个完整周期):` 行之后、现有 `Step 1: 讨论组 spawn` 之前 | 同一串 (逐字相同) |

- **现有编号一律不动** —— Convergence 的 `1./2./3./4.` 与 Challenge 的 `Step 1..Step 5` 都保持原值, 避免连带引用漂移;
- **两块用逐字相同的串**, 使「只 patch 了一块」可被一条计数断言当场抓住 (SC-17);
- **两块都要改的理由不是对称美感**: 本仓 post_spec 被 pin 死在 convergence 上不受影响, 但 aria-plugin 是跨项目分发的, `config-loader/DEFAULTS.json:124-128` 的 `adaptive_rules` 里 `"level_3": "challenge"` (实读见 §实读清单 #20) 意味着**下游项目的 Level-3 审计会走 Challenge** —— 只 patch 前者会让那些项目**静默漏掉探针**。

> **插入串 (两行, 逐字; R5/C1 落版 —— 旧串 `每轮入口: 竞品 spec 探针` 是一个 9 字名词短语, 无动词、无脚本路径、无参数、无 verdict 消费, 运行时 AI 无从知道跑什么; 现按母 Spec D17 ② 改为可执行形, 首行前缀保留使 SC-17 的计数不变)**:
>
> ```
>   每轮入口: 竞品 spec 探针 —— python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/audit-engine/scripts/sibling_spec_probe.py" --own-spec-dir "<本轨 spec 目录名>" --repo-path "<repo root>"
>   读 stdout JSON 的 verdict: sibling_found ⇒ 本轮 🔴 (含 N 份/归档标注) · no_sibling_found ⇒ 「已完整扫描, 未发现同 issue 竞品」 · not_established / exit≠0 / 非 JSON / schema_version 未知 ⇒ 「未能核实」(禁止渲染为无竞品); 不阻断本轮
> ```
>
> - **SC-17 的「恰 2 次」是有意的保守** (R5/m1: 此前只写在「新表面」段, 实现者读 §8 落地 ⇒ 补在此): 若将来出现第三个模式块, 该断言会把「正确地插了三处」判红 —— 漏插比多插危险, 届时改断言而不是改保守方向;
> - **SKILL.md 侧的对应小节 (Impact) 须含同一条命令行与三档消费措辞的字面** —— 由 **SC-20** 钉住 (D17 ①②③: 块边界 / 完整命令行 / fail 分支措辞 `未能核实`); stdout 契约 (§7 十二字段) 与消费措辞 (§9) 的**权威可执行版**落 `execution-modes.md` 新节 (R5/M3), SKILL.md 放概述 + 指针, 与 `audit-engine/SKILL.md:237`「权威可执行版见 references/…」(`:236` 是另一句注释, R6/TL m6)的既有体例一致。

### §9 消费面

- 命中 (`verdict == "sibling_found"`) ⇒ 该轮审计报告的**轮次记录**里, 对应的 `### Round N` 项下新增一行渲染 🔴 (`report-format.md:50-71` 的 `## 轮次记录` / `### Round N` 模板, 实读见 §实读清单 #25), 并写入聚合报告;
- **不阻断**: 不改 verdict 计算、不改收敛判定、不改轮次路由;
- **措辞按 `verdict` 分档, 三档不得合并**:

| `verdict` | 消费面措辞 |
|---|---|
| `"sibling_found"` | 「🔴 检测到 N 份同 issue 的竞品 Spec: …」; 命中项在 `archive/` 下时须标注**「已完成的 Spec」** |
| `"no_sibling_found"` | 「本轮已完整扫描, 未发现同 issue 竞品」 |
| `"not_established"` | 「**未能核实** —— 本轮竞品扫描未取到完整证据 (原因: `<reason>`)」。**禁止**渲染为「无竞品」 |

- **消费方的 fail-closed 义务**: `exit != 0` **或** stdout 无法解析为 JSON **或** `schema_version` 未知 ⇒ 一律按 `"not_established"` 处置。

### §10 盲区声明 (成文, 不当主防线 — M-5b)

> **消解 R2 簇 M-5 后半**: 「只扫默认分支 ⇒ in-flight 竞品结构性不可见, 盲区声明未勘正」(KM-M6)。

**⚠️ 勘正母 Spec 原盲区声明。** 母 Spec §4 原文写「只看得见**已 push** 的竞品」—— **这句话不准确, 且方向是乐观的**。竞品可以已 push 而仍然完全不可见。准确的说法是: **只看得见已 push 到被扫 remote 任一分支的竞品** (2026-09-01 P11 扩后; 扩前是「已进入被扫默认分支」)。

| # | 盲区 | 探针为什么看不见 |
|---|---|---|
| **B1** | 对方 Spec 在**非默认分支** (feature branch) 上进行中, 尚未合并 | ~~§4 只扫各 remote 的默认分支~~ **✅ 2026-09-01 P11 扩后已纳入** (全部 `refs/heads/*` 均扫, SC-22; 残余 = 对方**未 push** 的本地分支, 归 B2)。扩前原文留痕: 一份仍在制的竞品 Spec **按定义几乎总是活在 feature 分支上**, 直到合并才进默认分支 —— **而那时它已经不是「来得及协调」的 in-flight, 而是既成事实**。这是母 Spec 原声明漏掉的第三类盲区, 也是**最该被看见却看不见**的那一类 |
| **B2** | 双方都未 push | 秒级到分钟级窗口, 无任何机制覆盖 |
| **B3** | 对方的 proposal **没有「关联 Issue」字段** (或有但不在层 0 认的位置) | 层 1/层 2 皆空 ⇒ 层 3 判不可见。**实测量级: `cc1bdef` 的 147 篇语料中 133 篇落 `no_field` (90.5%)** —— 探针今天只对 **13** 篇可见 (§实读清单 #16) |
| **B4** | **本轨自己**没有该字段 (`own_keys` 为空) | 没有可比较的输入 ⇒ `verdict="not_established"` + `reason="own_token_absent"`。**这是量级最大的一类**: 按 B3 的同一实测, 随机一份 proposal 落入本类的概率约九成 |
| **B5** | 同 issue 的多份 Spec 是**有意拆分**而非重复劳动 | 探针**不区分**这两者 (§Why 的 `#137` 簇即实例) ⇒ 命中是**告警不是判决**, 必须 advisory |
| **B6** | 一份**只是在讨论**某 issue 的 Spec, 其字段行恰好写在行首且是单个 `>` | §3 层 0 只挡住了**嵌套引用**这一形态 (`> >` / 带前导空白, 即本仓实测到的那个假阳性)。若有人把示例写成合规的行首形态, 探针仍会把「谈论 X」读成「在做 X」。**残余, 成文不假装覆盖** —— 处置靠 D11 的 advisory 定位 (人一眼可辨), 不靠加更多正则 |

**⇒ 探针实际覆盖的是母 Spec §Why 里两类场景中的 (b)「对方已 ship 并归档」, 以及 (a)「对方没走 claim」中**其 Spec 已 push 到任一被扫分支**的那一部分 (2026-09-01 P11 扩后; 扩前只有「已进默认分支」)。** 它**不是**「早期预防」机制 —— 它是「止损」机制: 在你已经投入的第 2、第 3 轮审计入口把「这件事别人做完了」摆到台面上。第 5 次事故里被浪费的三天, 正是这样被止住的那种。

> **本 Spec 自身的 dogfood 观察**: 本文件的「Linked Issue」写的是哨兵 `none` ⇒ 按层 1.5, **它对本探针永不命中**。这是设计如此 (正证据), 不是缺陷; 但它也意味着**本 Spec 不能拿自己当端到端夹具**, 夹具必须取 §3 点名的真实 `#122` 簇。

---

## 决策记录

| # | 决策 | 依据 |
|---|------|------|
| **P1** (承接母 Spec **D7**) | 探针自带 fetch, **不称轻量**; 超时 = **每个 git 子进程各 30s** (非整轮总预算) + fetch 腿 1 次重试; 超时按 `degraded` 处置 | S2 历史实测 ~13.8s/轮 + 本轮新增 ~10.5s 的 `ls-remote` 腿 (§5); 「整轮 30s」在本仓必然超时 |
| **P2** (承接母 Spec **D11**) | 不阻断; **exit 0 覆盖全部有定义的判定** (含 `degraded` / `skipped`); 非 0 仅探针自身失败 | 与主机制同为 advisory; 且 §Why 的 `#137` 簇实证「同 issue ≠ 重复劳动」。**旧 SC-18「无远端 ⇒ exit 非 0」与本条冲突, 按本条解** (§7) |
| **P3** | 不复用 `remote_refresh` 缓存 (承接 D7 后半) | 缓存唯一写入点 `remote_refresh.py:691` 只在 `collect_remote_refresh():568` 内, 其唯一生产调用点是 `scan.py:312` ⇒ audit-engine 轮间无机制保证跑过 `/state-scanner` (实读 #22) |
| **P4** | canonical 抽取规则的 SOT 在姊妹 Spec `linked-issue-field-availability`, 本 Spec **不重定义、不私搭第二份实现**; 比较用已 ship 的 `normalize_linked_issue()` | 双实现漂移 = 前置 Spec spike S5 刚揭示的病换位置复发; 该函数已公开导出 (实读 #1) |
| **P5** | 哨兵 (`none` / `无`, 姊妹 §2 集合) 独立成层 1.5: ∅ + 不进 URL 回落; 与 `NO_TOKEN` 分档; 枚举值 `"none_sentinel"` | **实测**: `normalize_linked_issue("无")` 返回 `None` ⇒ 当普通 token 则落原串相等 ⇒ 两份哨兵互相命中 (实读 #15); `none` 同理且触发面更宽 |
| **P6** | 默认分支**只认** `git ls-remote --symref <R> HEAD` 的实时应答; 取不到即 fail-closed, **不猜** `master`/`main`; 不复用既有 `_resolve_default_branch` | 本仓 `github` 无本地 symbolic-ref (exit 128) 且 git 2.39.5 的 fetch 不补写 (实读 #3/#9); 既有解析器 origin 硬编码 + 名字猜测 (实读 #23) |
| **P7** | remote 集合从 **`git remote` 配置面**取, 经 `resolve_enforced_remotes()`; **禁止**从 `refs/remotes/*` glob 取 | 本仓当场可复现: `refs/remotes/probe/*` 存在而 `remote.probe.url` 不存在 (实读 #11) |
| **P8** | fetch 落 **私有 ref 命名空间** `refs/aria/sibling-probe/<remote>/<branch>`; 不动 `refs/remotes/*`, 不依赖全局 `FETCH_HEAD` | `FETCH_HEAD` 是全局单槽, 并发下被覆盖; `refs/aria/*` 是本仓既有私有命名空间 (实读 #27) |
| **P9** | 判定结论用一等字段 `verdict` 承载, **不让消费方从 `hits == []` 推断** | `hits == []` 在「扫完没有」与「没扫到 / 本轨无输入」上取值相同 ⇒ 推断即零证据当正证据。母 Spec D-F 的同一纪律换面落点, 非新机制 |
| **P10** | 规模上限用探针自有常量, **不复用** `state_scanner.handoff_multibranch.max_branches` | 该旋钮作用域是「分支数」, 与本 cap 的「单 ref 上 proposal 数」不等; 作用域不匹配的开关把恒红换成假绿 (memory `knob-granularity`)。**2026-09-01 P11 后补**: `MAX_REFS_SCANNED` 的作用域确与该旋钮相同, 仍不复用 —— 第二条理由: 该旋钮属 `state_scanner` 配置树, 探针不读 state-scanner config key, 且降级语义不同 (`soft_error` vs `verdict=not_established`) |
| **P11** | 扫描范围**扩为**「enforced_remotes × 全部 `refs/heads/*`」, 配三道护栏: 按 `spec_dir` 去重 (SC-23) / 默认 ref 已归档同名 ⇒ 陈旧跳过 (SC-24) / 非默认 ref 数 cap `MAX_REFS_SCANNED` (SC-25); B1 命中由 SC-22 钉 | **✅ 2026-09-01 技术裁定** (决策单 `.aria/decisions/2026-09-01-a1-entry-h1-h6-technical-rulings-product-vs-technical-split.md` §H3): 产品目标 (#174 在实现前抓 in-flight 重复) 倒推 —— in-flight 竞品按定义活在非默认分支 (§10 B1), 只扫默认分支对目标场景结构性失明; owner 2026-08-23 缩 scope 的成本前提已被下方实测推翻 (~0.15s/轮); 反向成本 (重复命中 / 陈旧假阳性) 化为两条可证伪 SC, 不是「不做」的理由。落点: TASK-012/013 verification + tasks.md 3.3/3.4 + TASK-007 RED (SC-22~25) |

> **✅ 2026-09-01 已裁: 扩** (技术级裁定, 判据见上行 P11 与决策单 §H3)。以下为裁定前的上呈原文, 留痕不改:
>
> **⚠️ 请 owner 复议 (P11 的成本前提) — 主控/执笔席不自行改 scope**
>
> 母 Spec 把「只扫默认分支」的理由挂在**规模代价**上 (援引 `handoff_multibranch.py` 的 440 分支 scan cap 先例)。**本轮实测该前提不成立**:
>
> - `git fetch <remote>` 默认已把该 remote 的**全部** `refs/heads/*` 取到本地 ⇒ 扩大扫描范围**不新增任何网络腿**;
> - 已 fetch 后逐 ref 抽取语料的**本地**代价实测: 单 ref **12ms**; 本仓全部 **11 条**远端跟踪 ref 合计 **151ms** (§实读清单 #17)。
>
> ⇒ 「扫全部活跃分支」相对「只扫默认分支」的边际代价在本仓约 **0.15s/轮**, 而它**恰好补上盲区 B1 (in-flight 竞品)** —— 即探针最有价值却当前完全看不见的那一类。
>
> (**裁定前原文**) **本 Spec 按 owner 的缩 scope 裁定执行, 不自行扩展。** 但上述实测与母 Spec 的成本理由直接冲突, 按 Rule #10 与 memory `narrow-owner-options` 留痕上呈: 若 owner 认为该选项应纳入, 它是一个**独立的小改动**, 不需要重开本 Spec 的其余部分。反向的成本项也一并列出 (不预设结论): 分支面扫描会引入**同一份 Spec 在多个分支上的重复命中**去重问题, 以及**已废弃分支上的陈旧 Spec 造成假阳性** —— 两者都是本 Spec 当前设计不需要面对的。

### Rule #6 (rule6_note) — 诚实处置, **不自判豁免**

本 Spec 的处方性 · 运行时指令面改动落在 **`audit-engine`** 一个 skill 上 (`SKILL.md` + `references/execution-modes.md`, §8): 「每轮审计入口必跑 `sibling_spec_probe.py`, Convergence 与 Challenge 两块对称」。

**结构性事实 (本轮实核)**: `aria-plugin-benchmarks/ab-suite/` 下**没有 `audit-engine.json`** (目录 **31** 个 `.json` (**R4/S-3 订正**: 原写 30, 与本文件后段「实测的 31」自相矛盾; 实测为 31) + 4 个 fixture 目录 + `version.yaml`, 无该文件; §实读清单 #2)。

按 CLAUDE.md Rule #6 判据表:

| 判据表行 | 对本 Spec 是否成立 |
|---|---|
| 第二行「处方性 · 运行时指令面 / 能测 / 照跑 AB」 | **不适用** —— 无套件可跑 |
| 第三行「套件覆盖外」: 点名行为 + 可证伪定向 fixture + 套件缺口开 issue (**缺一照跑**) | 三条**逐条处置如下** |

1. **点名行为 (能做, 本 Spec 落)**: (α) 每轮审计入口调用 `sibling_spec_probe.py` 并把结果渲染进当轮 `### Round N` 记录; (β) `verdict == "not_established"` 时渲染「未能核实」而**非**「无竞品」。—— **这两条是 audit-engine 自己的新行为**, 与母 Spec rule6_note 里那三条 (a)(b)(c) (全是 A.1 / phase1_gate 侧行为) **无一重合**; 母 Spec 把 audit-engine 列进覆盖外档却零点名, 正是 R2/TL-M9 判的那条 major, 本条即其处置。
2. **可证伪定向 fixture (能做, A.2 落)**: 为 (α)(β) 各建 1 个 eval case, 双臂须能分辨。**宿主 = 新建 `aria-plugin-benchmarks/ab-suite/audit-engine.json`** (格式照既有套件, 见 `spec-drafter.json`; **必须经 `/skill-creator` 产出 (R4/S-2 补)** —— CLAUDE.md 不可协商规则 #6 逐字「**Skill 基准测试必须用 `/skill-creator`** (自研 runner 已废弃)」⇒ **手工仿写既有套件的 JSON 格式不满足该规则**。建立流程照 `AB_TEST_OPERATIONS.md` §场景 2「新增 Skill 首次基线」)。
3. **套件缺口开 issue (已存在, 不新开)**: **`10CG/aria-plugin#150`** —— 标题逐字「[benchmark] Rule #6 判据表第三行的兜底「缺一照跑」对 14/43 个 skill 结构上不可执行 — 它们根本没有 AB 套件」(本轮实核, §实读清单 #26)。它记录的正是本 Spec 撞到的**类级**问题。同族先例 `10CG/aria-plugin#157` (state-scanner 套件对 Layer L 段零覆盖) 亦已在册。

**⚠️ 哪半做不到, 明写**: 判据表第三行的兜底是「缺一**照跑**」。本 Spec 三条都做得到, 兜底按字面不触发 —— **但这只是因为第 2 条被解释成「新建套件」**。若 A.2 因任何原因未能建成 `audit-engine.json`, 第 2 条即缺失, 兜底触发, 而**兜底本身在无套件时结构上不可执行** —— 这正是 `#150` 的内容。**此时不得自判豁免** (Rule #10; `standards/conventions/skill-benchmark-exemption.md` 的封闭白名单四类无一适用), 必须显式上呈 owner 请裁。

> **谁在什么时点检查这个条件 (主控 2026-08-25 补 —— 否则它是一条没有触发者的义务, 即 memory `feedback_completion_signals_vs_runtime_invocation` 的形状)**: 该条件**不是**一句提醒, 而是 **A.2 任务清单的一条显式验收项** + **本 Spec 进 Phase B.1 的前置断言** —— A.2 须派生一条任务「建 `ab-suite/audit-engine.json` 并使其含 (α)(β) 两个双臂可辨的 eval」, 验收 = `test -f aria-plugin-benchmarks/ab-suite/audit-engine.json` 且两 eval 在坏实现上必红; **该任务未 done 则 Phase B.1 不得开始**。届时**不得自判豁免**, 须把「第 2 条缺失 ⇒ 兜底触发 ⇒ 兜底在无套件时结构上不可执行」原样上呈 owner (Rule #10)。

**本 Spec 不申请豁免。**

---

## Success Criteria

> **编号说明**: 本 Spec 从 **SC-1** 重新编号 (独立文件独立命名空间)。与母 Spec 旧编号的对应: 本 **SC-1** 承接旧 **SC-16**; 本 **SC-2** 承接旧 **SC-17**; 本 **SC-3 / SC-4** 由旧 **SC-18** 拆出 (旧条自相矛盾, 见 §7); 本 **SC-5 / SC-6** 承接旧 **SC-19** 的 (a)(c) 两项 —— 旧 (b) **不迁入**, 理由见 §1 依赖方向第 2 条。**本文正文里形如「旧 SC-NN」的一律指母 Spec 的编号**; 本表新增的 SC-19 / SC-20 / SC-21 与之无关 (R6/CR 探针 m1)。
>
> **验证面分层**: 代码类宿主 = `skills/audit-engine/tests/` (新建, 自动纳入 `run_all_tests.sh`); 行为类只能由 AB 定向 fixture 覆盖, **不冒充结构化测试**。

| SC | 类 | 场景 | 期望 | 怎么会红 |
|----|----|------|------|---------|
| **SC-1** (旧 SC-16) | 代码 | 竞品 proposal 位于 `openspec/archive/` 下。夹具 = §3 自检点名的真实 `#122` 两份 | 命中; `hits[].corpus == "archive"`; 消费面措辞含**「已完成的 Spec」** | 只扫 `openspec/changes/` 的实现在本仓真实语料上返回空 —— 实测三个同 key 簇的 6 份全在 `archive/`, `changes/` 下 0 份 ⇒ 必红 |
| **SC-2** (旧 SC-17) | 代码 | 全部 enforced remote 均解析成功且 fetch 成功, 语料中无同 key proposal | `status="ok"`, `verdict="no_sibling_found"`, `hits == []`, **exit 0** | 把「无命中」映射成非 0 exit 的实现必红 |
| **SC-3** (旧 SC-18 拆 a) | 代码 | 某 remote 的 fetch 失败 / 超时 | `status="degraded"`, `verdict="not_established"`, 该 remote 的 `error_kind` 非空, **exit 0**; 另一 remote 已找到的命中项**仍留在 `hits[]`** | (i) 把 `verdict` 算成 `no_sibling_found` 的实现必红 (零证据当正证据); (ii) 把 degraded 映射成非 0 exit 的实现必红 (违 D11); (iii) 把 `hits` 整体丢弃成空的实现必红 (丢掉真实正证据) |
| **SC-4** (旧 SC-18 拆 b) | 代码 | `resolve_enforced_remotes()` 解析为空集 (无 remote / 全部 read_only) | `status="skipped"`, `reason="no_enforced_remote"`, `verdict="not_established"`, **exit 0** | 照旧 SC-18 字面写「无远端 ⇒ exit 非 0」的实现在本条必红 —— 该写法会让无远端的项目**每轮恒非 0** |
| **SC-5** (旧 SC-19a) | 代码 | 本轨 spec 目录名在被扫的**任一 ref (默认 ref 或非默认 ref)** 上**已存在** (即本 Spec 自己已合并, 或别人分支上留有副本; P11 2026-09-01 扩维, 夹具须含一条非默认 ref 上的副本) | 该目录**不得**出现在 `hits[]`, 无论它落在哪个 remote / 哪个 corpus / 哪条 ref | 不做自命中排除的实现在「本 Spec 合并后」每轮自报一条命中 ⇒ 必红 |
| **SC-6** (旧 SC-19c) | 代码 | `MAX_PROPOSALS_SCANNED` 置 1, 语料含 1 份 `changes/` + 1 份 `archive/` | 保留的是 **`changes/` 那份**; `caps_applied[]` 非空且含截断点路径与丢弃条数; `status="degraded"`, `verdict="not_established"`; stderr 有 `log()` 披露 | (i) 静默截断 (`caps_applied` 为空) 必红; (ii) 排序把 `archive/` 排前而丢掉 `changes/` 的实现必红; (iii) 截断后仍报 `no_sibling_found` 的实现必红 |
| **SC-7** ⭐ (M-1 主条) | 代码 | 夹具 = `archive/2026-07-31-phase-c-gate-path-coverage-not-applicable/proposal.md:6` 与 `archive/2026-08-22-phase-c-integrator-ci-path-coverage/proposal.md:22` 两行**字段原文** | **命中**, 且命中键逐字为 `["k","aria-plugin",122]` | 只实现层 1 (canonical) 的实现在此返回空 —— 实测两行冒号后首个非空白都是 `[`, canonical 层判 `NO_TOKEN` ⇒ 必红。**这正是探针的立项案例** |
| **SC-8** ⭐ (M-1, 提取器位置约束) | 代码 | 夹具 = 上述 `:6` 那一行原文 (它冒号后首非空白是 `[`, **但行内后段含 code span** `` `confirmed` `` / `` `major` `` / `` `next-cycle` ``) | canonical 层判 **`NO_TOKEN`**; **不得**抽出 `confirmed` | 把提取器写成「行内**第一个** code span (任意位置)」的实现会抽到 `confirmed` (**本轮实跑复现, §实读清单 #15**) ⇒ 归一得 `None` ⇒ 落原串键 `["r","confirmed"]` ⇒ 与对方不命中且键值可辨 ⇒ 必红。**与 SC-18 是两个不同的取错**: 本条是「层 1 在**行内**取错 span」, SC-18 是「层 0 取错**行**」 |
| **SC-9** ⭐ (FIX-10 对照臂 1) | 代码 | 两份 proposal 的 canonical token 串**均为哨兵** —— 三组: (`无`,`无`) / (`none`,`none`) / (`none`,`无`) | **三组都不命中**; 两份的 `layer` 均为 `"none_sentinel"` | 把哨兵当普通 token 参与求交的实现必红 —— 实测 `normalize_linked_issue("无") is None` ⇒ 回落原串相等 ⇒ 命中; 只认 `无` 的实现在 (`none`,`none`) 组上原串相等 ⇒ 命中 ⇒ 红 (owner 2026-08-30 6i) |
| **SC-10** ⭐ (FIX-10 对照臂 2) | 代码 | 一份 canonical token 为哨兵 **且其字段行内含一个 issue URL** (两臂: `> **关联 Issue**: \`无\` — 讨论见 https://forgejo.10cg.pub/10CG/aria-plugin/issues/122` 与 `> **Linked Issue**: \`none\` — see https://forgejo.10cg.pub/10CG/aria-plugin/issues/122`); 另一份 token 为 `10CG/aria-plugin#122` | **不命中**; 且哨兵那份的 `layer` 必须是 `"none_sentinel"` 而非 `"url_fallback"` | 回落触发条件写成「canonical **集合为空**」而非「canonical 层 **== `NO_TOKEN`**」的实现, 会让哨兵那份走 URL 回落抽到 `#122` ⇒ 命中 ⇒ 必红 |
| **SC-11** | 代码 | 一份 canonical token 为哨兵; 一份**根本没有**字段行 | 两者比较键集合都为空, 但 `layer` 必须可辨: `"none_sentinel"` vs `"no_field"` | 把两者折叠成同一枚举值的实现必红 —— 正证据与零证据合并, 与 §7 `verdict` 条款同一病 |
| **SC-12** ⭐ (M-5a) | 代码 | 对一个**无本地 `refs/remotes/<R>/HEAD`** 的 remote 解析默认分支 (本仓 `github` 实况: `git symbolic-ref refs/remotes/github/HEAD` exit **128**) | 仍解析出 `default_branch="master"`, `resolved_by="ls_remote_symref"` | 只读本地 symbolic-ref 的实现在 `github` 上取不到 ⇒ 该 remote 记 unresolved ⇒ 必红。**这是 R2/BA 在 `aria` 子模块独立复现过的同一故障** |
| **SC-13** ⭐ (M-5a fail-closed) | 代码 | `ls-remote --symref` 非 0 退出 / 超时 / 输出无 `ref: ` 行 (夹具用注入式 runner, 不打真网络) | 该 remote `default_branch=null` + `error_kind` 非空; **stdout 中不得出现字面 `master` 或 `main` 作为该 remote 的 `default_branch`**; `status="degraded"` | 照抄既有 `_resolve_default_branch` 的 `_DEFAULT_BRANCH_FALLBACKS = ("master","main")` 名字猜测 (`fetch_gate.py:55,124-127`) 的实现在此必红 |
| **SC-14** ⭐ (P7) | 代码 | 仓库中存在一个 `refs/remotes/<name>/*` 但 `git config --get remote.<name>.url` 为空的**陈旧 remote-tracking ref** (本仓 `probe` 实况) | `remotes[]` 中**不得**出现该名字 | 用 `refs/remotes/*` glob 枚举 remote 的实现会把 `probe` 纳入 ⇒ 必红 |
| **SC-15** (M-17 stdout 契约) | 代码 | 三种终局 (`ok` / `degraded` / `skipped`) 各跑一次 | stdout 每次都是**恰一个**可 `json.loads` 的对象, 含表中全部必填键; stderr 的任何内容不出现在 stdout | 把 `log()` 写进 stdout 的实现使 `json.loads` 抛异常 ⇒ 必红 |
| **SC-16** (M-17 消费面) | **行为** (定向 fixture) | 探针 `exit != 0`, 或 stdout 不可解析, 或 `verdict == "not_established"` | audit-engine 渲染**「未能核实」**, **不得**渲染「无竞品」, 且不阻断该轮 | 把三者任一折叠成「无竞品」的实现必红。**本条无代码宿主** —— 它断言的是 AI 是否照 SKILL.md 行事, 只能由 AB 定向 fixture 覆盖 (rule6_note 点名行为 β) |
| **SC-17** ⭐ (§8 双落点; **R6/TL M7 + CR 探针 m2 收窄计数域**) | 代码 | 对 `references/execution-modes.md` 的 `## Convergence 模式` 与 `## Challenge 模式` **两节的围栏块切片**分别计数字面串 `每轮入口: 竞品 spec 探针` | **每块恰 1 次** (共 2); **负控**: 除这两处围栏外, 全文 (含新增的 `## 竞品 spec 探针 (per-round 入口)` 契约节) 该字面 **0 次** —— 契约节用「探针的 stdout 契约如下」之类措辞, 不复用该前缀 | baseline 命中 **0** ⇒ 必红; **只 patch Convergence 的实现命中 1 ⇒ 必红** —— 这正是「下游 Level-3 走 Challenge 会静默漏掉探针」那条失败模式的机械护栏。**docstring 须写明**: 若将来出现第三个模式块, 本条会把「正确地插了三处」判红 —— 这是**有意的**保守 (漏插比多插危险), 不是 bug; 由「全文恰 2 次」改为分块计数是为了不误伤同文件新增的契约节 (旧写法会把正确实现判红) |
| **SC-18** ⭐ (§3 层 0, 假阳性拒绝) | 代码 | 三臂**同批**跑, 语料取 `cc1bdef` 全部 147 篇: (a) 行首 `> ` 规则 (本 Spec 采用); (b) 宽松「行内任意位置」规则; (c) 行首 + 「只在首条 `---` 之前找」 | (a) 得 `no_field` **133** / `url_fallback` **13** / `no_token_no_url` **1**, 簇 **3** 个且**不含** `a1-entry-claim-duplicate-work-guard`; (b) 得 `url_fallback` **14** 且 `#122` 簇**含**该目录 (**假阳性**); (c) 得 `url_fallback` **10** 且簇**只剩 1 个** | 这是一条**验拒绝能力**而非验当前取值的断言 (memory `adversarial-fixture`): 实现只要退回宽松定位, (b) 臂的假阳性就会出现在 (a) 臂上 ⇒ 必红; 实现若「顺手加固」成只扫头部区, `#122`/`#95` 两个真簇消失 ⇒ 必红。**两个坏实现都是像样的、有人会真写出来的**, 不是稻草人 **⚠️ 第四臂 (R3/TL-P3 补, 主控 2026-08-25)**: 原三臂 (宽松 / 行首 / 行首+仅头部) **无一验 E0 谓词 2 (围栏排除)**, 而姊妹实测「真实语料上加与不加围栏排除的判定差异 = 0」⇒ **漏实现围栏排除的实现在真实语料上也全绿**, 本条形同无断言 (memory `feedback_gate_tracks_reality_synthetic_fixture`: 追踪现实的 gate 不能只钉真实语料)。**补第四臂 (合成夹具, 必须造)**: 一份 proposal **只有围栏内的深度-1 字段行、没有真字段** (即 ```` ``` ```` 块内一行逐字 `> **关联 Issue**: `10CG/x#1``) ⇒ 期望判 **`no_field`**; 不做围栏排除的实现会把它当真字段并算进 `#1` 簇 ⇒ **必红**。**该形态在真实语料里有活实例**: 姊妹 Spec 自己的 proposal 有两行 (其 §Why 与模板示例块内), 可直接取作夹具原文 |
| **SC-19** ⭐ (R4/C-M3 + 姊妹 K8 → **2026-08-30 入表**; 常量黑名单) | 代码 | 两份 proposal 的字段值均为 SOT 模板 placeholder `` `{<org>/<repo>#<n>}` `` (姊妹判 `BAD_TOKEN`) | **不命中**; 二者的原串键集合均**不含** `("r", "{<org>/<repo>#<n>}")`; `own_layer` 为 `"bad_token_union"` | 照产原串键的实现 ⇒ 两份 placeholder 原串相等 ⇒ 命中 ⇒ 必红 (与姊妹 NEW-01 同形且**什么都不做就中**)。黑名单逐字内容与姊妹 §3 的模板默认值 + §2 哨兵集合**同源**, 任一改动须同批改另一侧 |
| **SC-20** ⭐ (R5/C1; 引母 Spec **D17**, 落 ①②③; **R6/TL M8 + m7 补**) | 代码 | (i) `skills/audit-engine/SKILL.md` 的「per-round 入口探针」小节 —— **块边界** = 从该小节标题行 (正则 `(?m)^#{2,4}[ \t]+per-round 入口探针`, **锚定标题起首, 不允许 `Step 0.5:` 之类前缀** —— R6/TL m7; **不在围栏内**) 起至下一个 `^#{1,4}[ \t]` 行止; (ii) `references/execution-modes.md` 含标题字面 `## 竞品 spec 探针 (per-round 入口)` | (i) 切片内含四个字面量 `sibling_spec_probe.py` / `verdict` / `not_established` / `未能核实`, **且**含一条以 `python3` 起首、含 `sibling_spec_probe.py` 与 `--own-spec-dir` 的完整命令行 (D17 ②); (ii) 该节切片 (至下一个 `^## ` 行) 内含 §7 的 `verdict` / `status` / `hits` 三个字面与 §9 三档措辞的字面 `未能核实` / `已完整扫描` / `检测到` | 「插两行短语 + 写一段消歧散文」的实现 (SC-17 全绿) 在 (i) 四字面量缺失 ⇒ 红; 把字面量写在小节外 (如 `## 相关文档`) 的实现因块边界 ⇒ 红; 标题写成 `Step 0.5: per-round 入口探针` 的实现因锚定起首 ⇒ 红; **跳过契约节的实现在 (ii) 上 ⇒ 红** (否则 SKILL.md 的指针悬空)。**baseline 必红** (小节与契约节今天都不存在) |
| **SC-21** (新, R6/BA 探针 M1; import 顺序) | 代码 | 在 `tests/test_sibling_spec_probe.py` 内 import 探针模块后断言 `sys.modules["lib"].__file__` 落在 `state-scanner/lib/__init__.py`, 且 `collectors.multi_remote.resolve_enforced_remotes` 可导入 | 两者同时成立 | 把 `_SS_SCRIPTS` 插在 `_SS_ROOT` **之后** (即排在 `sys.path` 更前) 的实现 ⇒ `lib` 绑定到 `scripts/lib` ⇒ `ModuleNotFoundError: lib.collision` ⇒ 红 (BA 席 /tmp 实跑复现); 把插入拆到两处、顺序由文件位置决定的实现同样可红。**baseline 必红** (探针今天不存在) |
| **SC-22** (新, 2026-09-01 P11 扩; B1 补盲) | 代码 | 注入 runner: remote R 的私有命名空间含默认 ref 与 `R/feature/x` 两条 ref; `feature/x` 上有 `openspec/changes/<other>/proposal.md` 且其字段与本轨同键, 默认 ref 上无该目录 | `hits[]` 恰含 `<other>` 一条, 其 `refs == ["R/feature/x"]`、`branch == "feature/x"`; `verdict == "sibling_found"` | 只枚举默认 ref 的实现 (裁定前形态) ⇒ `hits == []` ⇒ 红 |
| **SC-23** (新, P11 去重) | 代码 | 夹具默认分支取 `master`; 同一 `<other>/proposal.md` (同键) 同时出现在 R 的默认 ref 与 `R/a`、`R/b` 三条 ref | `hits[]` 恰 1 条 `<other>`, `refs == ["R/a", "R/b", "R/master"]` (整串字节序, 与枚举序无关), `branch == "master"` (枚举序首个命中 ref); `remotes[].refs_scanned == 3` | 逐 ref 追加不去重的实现 ⇒ 3 条 ⇒ 红; 按枚举序 append 不重排的实现 ⇒ `refs == ["R/master", "R/a", "R/b"]` ⇒ 红 |
| **SC-24** (新, P11 陈旧过滤; 过滤先于去重) | 代码 | `R/old/y` 上有 `openspec/changes/<z>/proposal.md` (同键), 而 R 默认 ref 上存在 `openspec/archive/2026-01-01-<z>/proposal.md` 且无 `changes/<z>`; 负控 (b) 另备夹具: 默认 ref 只有 `openspec/archive/2026-01-01-w-<z>/proposal.md` | `hits[]` 恰 1 条: `spec_dir == "2026-01-01-<z>"` (第三段目录名逐字, 与 `<z>` 是两个不同的去重键)、`corpus == "archive"`、`refs == ["R/<default>"]`; `hits[]` 中**不含** `spec_dir == "<z>"` 的项; `remotes[].stale_skipped == 1`。负控 (b) 下 `<z>` **入** hits 且 `stale_skipped == 0` | 不做陈旧过滤的实现 ⇒ 多出一条 `spec_dir="<z>"` / `corpus="changes"` ⇒ 红; 用 `*-<spec_dir>` 后缀 glob 的实现在负控 (b) 下误杀 `<z>` ⇒ 红 |
| **SC-25** (新, P11 refs cap) | 代码 | `MAX_REFS_SCANNED` 打桩为 1, R 有默认 ref + 非默认 `R/a`、`R/b`、`R/c` | 扫默认 ref + 字节序首条 `R/a`; `caps_applied[]` 含 `{remote: R, kind: "refs", total: 3, kept: 1, dropped_from: "R/b"}`; `status == "degraded"`、`verdict == "not_established"`、`reason == "cap_applied"`; stderr 披露 | 静默截断 (不写 `caps_applied` / 不降级) 的实现 ⇒ 红 (与 SC-6 同形) |

---

## 非目标

- **不阻断**任何轮次、不改 verdict 计算、不改收敛判定、不改轮次路由 (P2);
- **不读也不写** coordination claim; **不引入**任何 track-id / claim 语义 (那是母 Spec 的语义母体);
- **不定义**「关联 Issue」字段的抽取规则 (SOT 在姊妹 Spec `linked-issue-field-availability`), **不私搭第二份抽取实现** (P4);
- **不改** `lib/collision.py` 的任何签名或返回 schema —— 本 Spec 只**调用** `normalize_linked_issue()`;
- **不做**标题 / slug / 语义相似度的模糊匹配 (§3 层 3);
- ~~**不扩展**扫描范围到非默认分支~~ **2026-09-01 改判: 扩到全部 `refs/heads/*`** (P11 技术裁定, 决策单 §H3; 落点 TASK-012/013 + SC-22~25); 仍**不扫**未 push 的本地分支 (B2);
- **不回填**存量 132 篇无「关联 Issue」字段的 proposal (那是姊妹 Spec 的范围);
- **不修**代码库既有的 `STALE_TTL` / `SWEEP_TTL` 措辞误写等与探针无关的缺陷;
- **不修** `fetch_gate.py:21` / `:111` 对 `state-scanner sync.py::_resolve_default_branch` 的**悬空函数名引用** (**R4 行号订正**: 原引 `:23`, 实读 `:23` 是另一句「state-scanner git.py — but the original locks ``@{upstream}``」; `sync.py::_resolve_default_branch` 那句在 **`:21`**。断言内容本身独立核实为真 —— `sync.py` 在 `d50f9c3` 上 8 个顶层 def 中确无该函数) —— 本轮实读确认 `sync.py` 在 `d50f9c3` 上**没有**该函数 (只有同族常量 `_ORIGIN_HEAD_REFS:46`), 属既有文档缺陷, **记 follow-up, 不混进本 Spec 变更面**。

---

## Impact

| 文件 | 变更 | 来源 |
|------|------|------|
| `skills/audit-engine/scripts/sibling_spec_probe.py` | **新增** (`scripts/` 目录也新建; 实读确认 audit-engine 现零 `scripts/`)。stdlib-only。**CLI 入参**: `--own-spec-dir <本轨 spec 目录名>` (必需; 自命中排除键, 写入 §7 `own_spec_dir`) / `--repo-path <repo root>` (必需; 不假定 cwd, 与 plugin 侧既有两条探针同一纪律)。含 §3 谓词 (层 1.5 / 层 2 / 键构造 / SC-19 常量黑名单) + §4 默认分支解析 + §5 fetch/重试/超时 + §6 cap + §7 输出契约 | M-1 / M-5 / M-17 + R5/C1 |
| `skills/audit-engine/tests/test_sibling_spec_probe.py` | **新增** (`tests/` 目录也新建)。承载 SC-1~15、SC-17、SC-18。经 `skills/run_all_tests.sh` 的 `find ... -type d -name tests` 自动发现 (`:48`), 无 pytest 时走 `unittest discover` (`:71`); 目录内无 `test_*.py` 会被 `:50` 跳过 | R1/C4 同族 (SC 必须有真实宿主) |
| `skills/audit-engine/SKILL.md` | 新增「per-round 入口探针」小节 (**概述 + 指针**, R5/M3: 与本 skill 既有 progressive-disclosure 体例一致, `SKILL.md:237`「权威可执行版见 references/…」(`:236` 是另一句注释, R6/TL m6)); 小节**须含**四个字面量 `sibling_spec_probe.py` / `verdict` / `not_established` / `未能核实` 与一条完整命令行 (**SC-20**, 母 Spec D17); **须与 `### Step 0: Anchor 固化` (`:83`, 「Round 1 启动前一次性」`:85`) 显式消歧**, 不沿用其编号 | R3/M5 + 母 Spec §4 命名条款 + R5/C1, M3 |
| `skills/audit-engine/references/execution-modes.md` | **Convergence (`:84` 起) 与 Challenge (`:113` 起) 两块各插入 §8 的两行插入串** (逐字相同, 首行前缀 `每轮入口: 竞品 spec 探针` 保留供 SC-17 计数); 现有编号不动。**另新增一节** `## 竞品 spec 探针 (per-round 入口)` 承载 §7 十二字段 stdout 契约 + exit code 三分 + §9 三档消费措辞的**权威可执行版** (R5/M3: 指令面原被拆到三个文件且无一处含完整契约); **该契约节不得出现前缀字面 `每轮入口: 竞品 spec 探针`** (SC-17 负控, R6/TL M7), 其存在由 SC-20 (ii) 钉住 (R6/TL M8) | R3/M5; 跨项目分发的 `adaptive_rules.level_3 = "challenge"` (`DEFAULTS.json:124-128`); R5/C1, M3 |
| `skills/audit-engine/references/report-format.md` | `## 轮次记录` 的 `### Round N` 模板 (`:50-71`) 增一行探针结果; 措辞按 `verdict` 三档 (§9) | post_spec R1/QA「消费环节缺口」 |
| `aria-plugin-benchmarks/ab-suite/audit-engine.json` | **新建套件** (2 个定向 eval, 钉 rule6_note 点名行为 α/β; 其一即 SC-16)。当前**不存在** (本轮实核) | rule6_note 第 2 条 |
| **不改** `skills/state-scanner/**` | 探针**只 import** 已 ship 的 `normalize_linked_issue()` 与 `resolve_enforced_remotes()` 的**行为契约**, 不改其任何签名或实现; 探针**永不**产生 `--linked-issue` 实参 (§3 层 2 作用域分离 —— 那是姊妹 E6 / 母 Spec 的面) | P4 / §4 步骤 1 |

**跨 skill 复用的形态 —— 已在 §3「跨 skill import 的可运行模式」逐字钉死, 本段不再另说** (R5/M2 订正: 旧版此处写「复制或 import 由 A.2 定」, 与 §3 的「本 Spec 采用该模式, 逐字钉死」**同文件两处相反指令** —— 主控 R4 落 import 补丁块时未回灌本段, memory `fixes-contradict`)。补充两点: (1) `normalize_linked_issue` 与 `extract_linked_issue_field` 一律经 §3 的 `sys.path` 插 `state-scanner` skill root 后 `from lib.… import`, **不得复制**; (2) **`resolve_enforced_remotes` 亦经同一路径 import** (`from collectors.multi_remote import resolve_enforced_remotes`, 实读该函数在 `skills/state-scanner/scripts/collectors/multi_remote.py:255`; 先例 `handoff_autofill.py:48-51` 用的正是 `.../state-scanner/scripts` + `from collectors.multi_remote import …`), **不得复制** —— 复制即第二份实现, 与 P4 同病; 两条路径的插入顺序与三条 import **只见 §3 的唯一代码块** (顺序承重, R6/BA 探针 M1), 本段不复述; 已知限 (同名包 `scripts/lib` 今天就存在) 见 §3。

**follow-up (不在本 Spec)**:
1. `fetch_gate.py:21` / `:111` 的悬空函数名引用 `sync.py::_resolve_default_branch` (实读: `sync.py` 在 `d50f9c3` 上 8 个顶层 def 中无该函数);
2. `AB_TEST_OPERATIONS.md` §现有资产盘点写「Skill eval suites 28 个 ✅ **全量覆盖**」, 而实测 `ab-suite/` 有 **31** 个 `.json`, `10CG/aria-plugin#150` 又记「14/43 个 skill 没有套件」—— **三方互不一致**, 且「✅ 全量覆盖」是**假绿标注**。建议并入 `#150`;
3. ~~P11 复议项 (扫描范围是否扩到非默认分支)~~ ✅ 2026-09-01 已裁: 扩 (决策单 §H3)。

---

## 事实断言逐条实读清单 — ⛔ **整表已切出**

> **迁往**: [`.aria/audit-reports/sibling-spec-probe-audit-trail.md`](../../../.aria/audit-reports/sibling-spec-probe-audit-trail.md) §1 —— **按字节搬运, 未重写任何一句**。
> **切分理由 (主控 2026-08-25 裁定, 已标请 owner 复议)**: 该表是**核验证据**不是交付面; 与母 Spec / 姊妹 Spec 同批同刀, 三份体例一致。owner 2026-08-07 对 `linked-issue-normalization` 的「交付面与审计史切开」裁定是先例。
> **本文件正文所有 `文件:行号` 引用的实读基线 = aria 子模块 `d50f9c3`** (= v1.67.1 `58a49e7` + 2 commit) / 主仓 `cc1bdef`。**复核命令 (逐字)**: `git -C aria show d50f9c3:<path> | sed -n '<N>p'`。
> **正文里形如「见清单 #N」的交叉引用**, 一律指审计轨 §1 表内的第 N 行。
> ⚠️ 审计轨 append-only 且**不维护与本文件的一致性** —— 二者不一致**以本文件为准**, 按上面的复核命令重新实读裁决。

## 本轮引入的新表面 (未审)

1. **`verdict` 一等字段** (§7 / P9) —— 母 Spec §4 只定义了 exit code 三分, 没有判定面字段。这是本席的综合裁断: 它把「零证据 vs 正证据」从消费方的推断变成 payload 里的显式取值。**代价**: 输出契约多一个字段, 且 `verdict` 与 `status` 存在可能不一致的组合 (如 `status="ok"` 配 `verdict="not_established"` —— 当 `own_keys` 为空时**正是**该组合)。SC-2/3/4 覆盖了三种主要组合, **未穷举全部 3×3**。
2. **私有 ref 命名空间 `refs/aria/sibling-probe/<remote>/<branch>`** (§5(f) / P8) —— 新的 ref 写入面。**未测**: 它在并发的 `/state-scanner` 与本探针同时跑时的行为; 也**未定义** GC (这些 ref 会累积, 每个 remote/branch 一条 —— 本设计下最多 `|enforced_remotes|` 条, 量级极小, 但没有清理机制)。
3. **`MAX_PROPOSALS_SCANNED = 1000` 常量** (§6) —— 新的规模面。数值依据是本仓 147 篇的实测外推, **对第三方仓未验证**。刻意**不做**成 config key (避免新配置面), 代价是采用者无法调整。
4. **新建 `ab-suite/audit-engine.json`** (rule6_note 第 2 条) —— 从零建一份 AB 套件会把 `ab-suite/` 的 `.json` 从实测的 **31** 增到 **32**, 且是 `#150` 所列无套件 skill 中的第一个被补上的。**未审**: 建套件本身是否需要单独走 `/skill-creator` 的基线流程 (`AB_TEST_OPERATIONS.md` §场景 2「新增 Skill 首次基线」说要), 以及那次基线跑是否属于本 Spec 的交付范围。**另**: `AB_TEST_OPERATIONS.md` 的资产盘点写「Skill eval suites 28 个 ✅ 全量覆盖」, 与实测 31 个 `.json` 及 `#150` 的「14/43 无套件」**三方互不一致** —— 已记 follow-up, 本 Spec 不修。
5. **对 `execution-modes.md` 两块插入逐字相同的串** (§8) —— SC-17 用「计数恰为 2」做断言。**已知弱点**: 若将来出现第三个模式块, 该断言会把「正确地插了三处」判成红。这是**有意的**保守 (漏插比多插危险), 但须在 SC-17 的 docstring 里写明, 否则下一个人会以为它是 bug。
6. **对姊妹 Spec `linked-issue-field-availability` 的消费契约** (§3 层 1) —— **⚠️ R3/M7 状态更新 (主控 2026-08-25)**: 本条原自陈「单方面声明、未交叉核对、本轮最实的跨 Spec 风险」。**该风险已闭环**: 姊妹 Spec 已落盘并被本 Spec 实读, §3 已补四态逐格映射 (`BAD_TOKEN` 取层1∪层2 并集), 姊妹侧亦已回灌确认其四态定义无需改动 ⇒ **不再是单方面声明**。以下为当时的原始记述 (留痕): 本 Spec 单方面声明了它的抽取器返回三态 (`TOKEN(s)` / `无` / `NO_TOKEN`)。**该 Spec 由另一执笔席同批起草, 本席未与其交叉核对** ⇒ 若其最终定稿的返回形态不是三态, §3 层 1/1.5/2 的分派条件须同批修订。**这是本轮最实的跨 Spec 风险。** (—— 2026-08-25 原始记述的结尾句; 该风险已闭环, 见本条段首)
7. **§3 层 0 的字段行定位规则** —— 母 Spec §4 全文没有这一层 (它默认「字段行」是无歧义的)。本席在实跑中撞到假阳性后新增, 并用 SC-18 的三臂对照钉住。**它同时是一条跨 Spec 接缝**: 层 0 定位的是**行**, 姊妹 Spec 的抽取器定位的是**行内的 token** —— 两者若各自演化, 会出现「姊妹认这行、探针不认」或反之。**未与姊妹席对齐**, 与第 6 条同源。
8. **(2026-08-30) §8 插入串改为可执行两行 + SC-20 + SKILL.md/execution-modes.md 的概述/权威版分工** (R5/C1, M3) —— 新的指令面形态; 请 R6 看: 两行串在围栏内是否仍能被 SC-17 的「恰 2 次」正确计数 (前缀保留), 以及 `--own-spec-dir` / `--repo-path` 两个新 CLI 入参是否与 §7 的 `own_spec_dir` 输出自洽。
9. **(2026-08-30) 哨兵集合 `{none, 无}` + `"none_sentinel"` 改名 + 层 0 两拼写** (姊妹 6i / O-2 的镜像) —— 跨 Spec 接缝, 请 R6 核三份一致; SC-19 常量黑名单与姊妹 §2 集合**同源**这条同步义务是新的。
10. **(2026-08-30) `resolve_enforced_remotes` 经 `state-scanner/scripts` 路径 import** —— **R6/BA 席已在 /tmp 实测: 顺序敏感** (`scripts/lib` 与 `lib` 同名, 今天就存在), 已钉死为 §3 唯一代码块 + SC-21; 不再是「未实测」。

---

## 闸门状态 (Rule #10 — AI 不自行判定)

`audit.checkpoints.post_spec = "convergence"` **enabled**; `standards/conventions/configured-gate-authority.md` 的封闭豁免白名单四类 (config 显式 off / adaptive_rules 映射 / 已成文 lane 降级 / 结构性前提不成立) **无一适用** ⇒ **本 Spec 按默认跑 post_spec, 不豁免**。

**已裁事实与待裁事项**:

1. **本 Spec 是一份新文件**, 母 Spec 的 R1/R2 **不为本文件背书**。自 2026-08-25 起随母 Spec **联审**: 母 R3 = 本文件 R1, 母 R4 = R2, 母 R5 = R3 (R5/skill-reviewer 判本文件 1C/2M/1m, 已于 2026-08-30 落版); **下一步 R6 = 本文件第 4 轮**, 由 owner 显式加 (决策单第 3 项)。
2. **Rule #6 处置见 rule6_note**: 三条要件逐条落, 兜底不触发的前提是 A.2 真的建成 `ab-suite/audit-engine.json`; **若建不成, 不得自判豁免, 须显式上呈 owner**。
3. **owner 裁定**: (a) **P11 的扫描范围复议** → **✅ 2026-09-01 技术裁定 = 扩** (owner 2026-09-01 分工: 产品级 owner / 技术级 AI; 判据 = 产品目标 #174 倒推 + 成本前提已被实测推翻; 落点 P11 行 / §7 / §10 B1 / SC-22~25 / TASK-007·012·013; 决策单 `.aria/decisions/2026-09-01-a1-entry-h1-h6-technical-rulings-product-vs-technical-split.md` §H3 含一句话回退指引); (b) **对姊妹纯函数的依赖方向 → ✅ 已裁 (i) 硬前置** (owner 2026-08-30 (R6 后) 裁定), §1 第 3 条 / §3 两段已落版; 姊妹 O-4 同步。
4. **R6 已跑 (REVISE → 清账 → 定向复核 PASS), owner 裁不再加轮。** ~~本 Spec 在 owner 批准前不进 A.2/A.3。~~ **owner 2026-08-30 已批准进 A.2/A.3**; A.2/A.3 产物已派生, post_planning (combined) 按默认跑, 不豁免; P11 扫描范围仍待裁。

---

## Amendment A1 (2026-09-03, B.2 运行实际 vs Spec 陈述 — append-only, 原文不改)

**触发证据 (实现席真仓实跑, aria `feature/sibling-spec-probe`, 主仓 `/home/dev/Aria`)**: `origin` 有 9 条 `refs/heads/*`, 私有命名空间 11 条 ref; 按 §6 原计数单位「(ref, path) 逐条累计」得 origin **1097** 条 (> 1000) ⇒ `caps_applied` 触发 ⇒ 每轮 `status=degraded` / `verdict=not_established` / `reason=cap_applied`, **本仓上 `no_sibling_found` 永不可达** —— 探针在自己的宿主仓恒「未能核实」= 恒红零信息 (memory `feedback_false_green_dual_is_permanent_red`)。同一批 (ref, path) 去重到 **blob 对象**只有 **165** 个: 同一份 proposal 在 9 条分支上是同一个 blob, 逐 ref 重复计数把「防失控」cap 变成了「分支数 × 语料数」的必触发。

**原陈述**: §6「语料维度 … 单 remote 上跨其全部 ref 累计参与扫描的 proposal 数上限 … 默认 ref 先计, 超限从枚举序尾部截断」+ TASK-013「`git ls-tree -r --name-only <ref>`」「`MAX_PROPOSALS_SCANNED` 按 remote 跨 ref **累计**」。

**修正 (技术级裁定 D6, 决策单 2026-09-01 文件 §2026-09-03 段)**: 计数单位改为 **唯一 blob** —— `git ls-tree -r <ref> -- openspec/changes openspec/archive` (默认格式, 取 `<mode> <type> <sha>\t<path>`), 同一 remote 内按 `<sha>` 去重: 同 blob 只分类一次 (缓存), 只计一次; `remotes[].scanned` = 该 remote 实分类的**唯一 blob 数**; cap 比较对象 = 唯一 blob 数; 截断仍按枚举序 (默认 ref 先, 其余 ref 字节序; ref 内 changes 先 archive 后各自字节序) 从尾部丢弃**首次出现**的 blob, `caps_applied[].dropped_from` = 首个被丢弃 blob 的路径, `total` = 唯一 blob 总数。(ref, path) 级别的 hits 组装 / 去重 (SC-23 `refs[]`) / 陈旧过滤 (SC-24) / 自命中排除 (SC-5) **全部不变** —— 它们看的是 (ref, path) 归属, 与 blob 缓存正交。`MAX_PROPOSALS_SCANNED = 1000` 数值不变 (本仓唯一 blob 165, 余量 6×; 第三方仓语料 > 1000 份**不同**文档才触发, 才是「失控」)。

**可证伪判据**: 双远端可达时本仓实跑 `status == "ok"` 且 `caps_applied == []`; `remotes[origin].scanned` ≈ 唯一 blob 数 (165 ± 并发漂移) 而非 (ref, path) 数; SC-6 (单 ref, 两份不同 blob, cap 打桩 1) / SC-23 (同一 blob 三 ref ⇒ hits 1, refs 3) / SC-25 (refs cap) 断言不变。

**未做**: 不改 `MAX_PROPOSALS_SCANNED` 数值; 不引入 config key (P10 不变); 不改 §7 十二字段。`audit.checkpoints.mid_post_spec` 未配置 (默认 off) ⇒ 本 amendment 由主控按 phase-b-developer B.drift 的 append-only 体例落版, 不跑 mini-audit (Rule #10: 该闸门未启用, 不是自行豁免)。
