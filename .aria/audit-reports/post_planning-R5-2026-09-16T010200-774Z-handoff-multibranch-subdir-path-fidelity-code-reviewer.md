---
checkpoint: post_planning
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-16T01:24:57.637Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_planning R5 — code-reviewer (字符级正确性)

> 对象: 主仓 master `0e60b08` · aria `1cb3872` (v1.73.3) · standards `8b49562`。
> 本席 R5 新派, 未参与 R1–R4。全部结论基于自建对抗构造与实跑, 未沿用 R4 各席的坏态。
> 临时件全部落 `scratchpad/r5-code-reviewer/`, 已删除; 三仓 HEAD 与 porcelain 审后未变 (仅出现他席 R5 报告文件, 未读)。

---

## 审计结论

**counts: 0 Critical / 2 Major / 6 Minor。**

### 一、R4 处置落地核验

| R4 条目 | 处置要求 | 落地证据 (file:line) | 判定 |
|---|---|---|---|
| PP4-M1 | 第 4 / 6 步基准改「台账最近一次记录」+ 恢复后追加新记录 + 重走口径入清单 | `detailed-tasks.yaml:806`「相对台账中最近一次记录的取号时 SHA (首次 = TASK-027 的记录)」「按 TASK-027 的记录格式在台账追加新的取号时 SHA 与取号值」· `:808`「== 台账最近一次记录的取号值」· `tasks.md:60` 清单 22 (a) | 已落地 |
| PP4-M2 | 两仓视为整体 + 第 3 步 ff-only 后复核 + 论证句同步 | `detailed-tasks.yaml:807`「任一仓退出码非 0 ⇒ 对两个仓都走下一条的回退条」· `:805`「ff-only 之后再断言一次两者相等 …… 实测这一支 merge --ff-only 返回 Already up to date. 且退出码 0」· `:802` 论证句 | 已落地 (残留见 m4) |
| PP4-M3 | 删第 7 步 `--emit-json` 核验, 一致性归 TASK-001 | `detailed-tasks.yaml:810` 第 7 步已无该句 · `:195` TASK-001 保留「两份谓词原文的唯一机械核验点」· `tasks.md:65` 清单 27 | 已落地 (残留见 m6) |
| PP4-M4 | 主仓推送交 C.2.5 + 核配置事实 + 断言改 match=true + owner_gates 补 | `detailed-tasks.yaml:882` · `:159` owner_gates 第 11 项 | 文字已落地, **机制不成立 → M2** |
| PP4-M5 | owner_gates 两条补「不进 TASK-030」+ TASK-030 前置双远端 + TASK-031/032 补被拒/半推 | `detailed-tasks.yaml:157`/`:158`「不进 TASK-030」· `:857`「任一方未核验一致 …… 不 bump」· `:879` · `:909` | 已落地 |
| PP4-M6 | (j1)(j2)(j3) 换量为平衡括号 + 三新坏态 + authoring_rules + 跨行不假红 | `sc11-predicate-validation.py:312-314` · `:291-293` 三态 · `detailed-tasks.yaml:133` authoring_rules · `:298` alt_tuple_wrapped | 文字已落地, **判据仍可绕 → M1** |
| PP4-M7 | (l1) 丢标题行余部 + Scenarios 结构化 + 标题括注坏态 | `sc11-predicate-validation.py:318` `partition(chr(10))[2]` 与 `len(a)>=4 and any(target_in_subdir)` · `:294` bad_l1_title_paren | 已落地 (门限面见 m2) |
| m1 | owner_gates 顶部注明 + 补四处止损 + 第 2 步重执行断言 | `detailed-tasks.yaml:147` · `:156` · `:804` | 已落地 |
| m2 | TASK-001 补 B.0 未授权抑制手段 | `detailed-tasks.yaml:191` | 已落地 |
| m3 | tasks.md「须特别留意」纳入两处 fail-closed | `tasks.md:74`「其中五处」 | 已落地 |
| m4 | touchpoints 与 AB worktree 落 scratchpad | `detailed-tasks.yaml:192` · `:726` | 已落地 |
| m5 | TASK-026 扩面拆任务的 parent / metadata / 清单 | `detailed-tasks.yaml:738` | 已落地 |
| m6 | 台账骨架补停下记录去处 | `detailed-tasks.yaml:29`「停下与上报」 | 已落地 |
| m7 | 正向条件可执行式 + 负控写「非 0 (占位处数)」 | `detailed-tasks.yaml:804` `grep -qE '10CG/aria-plugin#[0-9]+'` /「值 = 当时的占位处数」 | 已落地 |
| m8 | TASK-029 提到 3.5–4h + metadata 同批 | `detailed-tasks.yaml:793` `est_hours: 4` · 求和 107 == `:166` | 已落地 (实测求和相符) |
| m9 | 第 6 步 CHANGELOG 计数括注改写 | `detailed-tasks.yaml:808`「本任务内第 5 步已排除在 master 上解冲突, 故这条断言只在重走时可红」 | 已落地 |
| m10 | 读前必看 14 与 v4/v5 谓词同步 | `tasks.md:31` (l1) 已同步 | **仅半 → m3** |
| m11 | (j4) 左边界改 `(^\|[^0-9A-Za-z])` | `sc11-predicate-validation.py:315` · `detailed-tasks.yaml:97` | 已落地 |
| m12 | TASK-009 字面量约束收窄 | `detailed-tasks.yaml:347`「docstring / 注释里引用该路径说明契约不受此限」 | 已落地 |
| m13 | (c2) 收紧 + 其余写入 handoff | `detailed-tasks.yaml:306` AST 版 (c2) · `:295` bad_c2_module_only · `:907` 十条已知边界 | 已落地 (清单实测精确, 见「核对无误」11) |
| m14 | TASK-018 补丁 4 给出具体三行 | `detailed-tasks.yaml:525` | 已落地 |
| m15 | 作废后补跑该 eval | `detailed-tasks.yaml:727`「修正两臂路径后补跑该 eval 一次」 | 已落地 |
| m16 | 台账行括注三处统一 | `detailed-tasks.yaml:522`/`:655`/`:676` 与同组兄弟一致 | 已落地 |
| 跨簇 4 | EXPECTED 收窄且断言强度不变 | 实测: 18 共有态 x 19 谓词 342 格与 v4 定值矩阵**零差异**, 6 新态纯增量 | 已落地 (证据见「核对无误」3) |
| 跨簇 5 | 本轮跳过/降级/替代判断入清单 | `tasks.md:65-68` 清单 27–30 | 已落地 |

**7 簇 Major 中 5 簇实质闭合, 2 簇 (PP4-M4 / PP4-M6) 文字落地而机制未闭合; 16 条 Minor 中 15 条闭合, m10 落一半。**

### 二、实施者试派生 (5 个 TASK)

1. **TASK-020 (4.2, collector 键层级)** — 指令 `detailed-tasks.yaml:598`「注释块 :370 与 docstring :430 的 `(parse_ok, …)` 元组各加第 5 元, 且第 5 元写在元组的括号之内」。我按语境派生的另一支合法读法是「把元组澄清清楚: `filename` 是 basename 不是 `rel_path`」。派生结果: 元组仍四元, (j1)(j3) 照过 → **M1**。另: 指令没有钉死第 5 元的字面, 写成单个 `rel_path` (而非代码里的 `(rel_path == filename, rel_path)`) 同样过 (j1) 而与 TASK-014 的 `return` 不符 —— 归入 M1 的建议改法。
2. **TASK-013 (2.5, writer)** — 逐条可落笔: 判据字面 / 三分派前初始化 / 三值集合 / :140 与 :159 同批改, 我实读确认该句在 `latest_md_writer.py` 全文**恰 2 处** (`:140` `:159`), 与指令一致; `_render_pointer` 在 `:124` 内部 `return _render_pointer_unavailable(...)`, 两函数同时改成返回二元组后该行无需额外改写。Scenarios 第 4 条结局行两种派生 (拆两行 / 并一行) 都过 (l1)。**可无歧义落地。**
3. **TASK-009 (2.1, 枚举层)** — `:177` 注释写「trailing slash required」而 `:178` 值 `"docs/handoff"` 无斜杠, 与指令的描述逐字相符; 契约句「含 path relative to 且写在 `_list_handoff_files` 自己的 docstring」在 `:350` 点名, 派生无歧义。但我另派生的一支「保留 basename 语义、只把措辞改掉」能同时过 (c1)(c2) → **m1**。
4. **TASK-019 (4.1, schema)** — `:575` 给出了五元元组的完整字面, 派生唯一。我实读确认 schema 全文只有 `:1124` 一行含 `(parse_ok`, 故 (j2) 的 `all()` 今日无历史行假红面; 但同一行的括注攻击同样成立 → **M1**。
5. **TASK-029 (5.2, 八步)** — 逐步走前置: 第 2 步断言对象是提交内容而非工作树 (`git show <feature>:...`), 正确; 第 3 步 ff-only 后复核闭合了 PP4-M2; 第 4 / 6 步基准已是「台账最近一次」, 恢复后追加新记录使重走可终止。**残留**: 第 5 步只判退出码, 没有正向断言「本轮确实产生了新的合并提交」→ **m4**。

### 三、Findings

#### M1 — `[Major] type=issue · category=mechanical-check-discriminating-power · scope=sc11-predicates/(j1)(j2)(j3) · v5 引入: 是`

**证据 (自建对抗构造, 未沿用 R4 坏态)**: v5 的 `ok()` 判「`(parse_ok` 起的那一对平衡括号之内是否含 `rel_path`」(`sc11-predicate-validation.py:312-314`, `detailed-tasks.yaml:94-96`)。只要在元组**内部**放一个自身平衡的括注并在其中提到 `rel_path`, 外层括号仍在元组自己的 `)` 处闭合, 而 `rel_path` 已落在窗口内。三处各构造一态, 代码侧用 v5 的正确实现 (`return (bucket, dt, filename, row.get("branch") or "", (rel == filename, rel))`), 只让文档侧留四元:

```
adv_j1_inner_paren   docstring: ``(parse_ok, updated_at, filename (basename, never ``rel_path``), branch)``
adv_j3_inner_paren   注释块:    # ``(parse_ok, parsed_updated_at, filename (basename, never ``rel_path``), branch)``
adv_j2_inner_paren   schema:    the **five-level** compound key `(parse_ok, parsed updated_at, filename (basename, never `rel_path`), branch)`
```

三态实跑结果 — **19 条谓词全 PASS**:

```
state                 a1   a2   b    c1   c2   f1   f2   g    i1   i2   j1   j2   j3   j4   j5   k    l1   l2   l3
adv_j1_inner_paren    PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS
adv_j3_inner_paren    PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS
adv_j2_inner_paren    PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS
```

坏态的像真性: 插入的括注是「`filename` 是 basename, 不是 `rel_path`」—— 本 Spec 的全部主题就是这两个概念的区分, 写文档的人在这一行写这句澄清是**最可能的**落笔, 不是刻意构造。另有一支 `adv_j1_unclosed` (元组后跟一个不闭合的 `(`) 被 (j1) 抓住 (FAIL), 说明漏的是「嵌套」这一支而非「不平衡」那一支。

**照计划执行会出的错**: TASK-019 `:575` 与 TASK-020 `:598` 的执行者把层数词改成五级、补上一句括注说明, 元组本身忘了改 —— `metadata.sc11_baseline_predicates` 19 条在 TASK-021 `:621` 与 TASK-029 第 7 步 `:810` 全绿, 合并、打 tag、发版一路放行。落地后果: schema SOT (`:1124`) 与 collector 契约 (`:370` `:430`) 对外声明的排序键是四元, 而代码是五元 —— 正是 Rule #3 与 (j) 族存在的唯一理由。

**这是第四轮同族未闭合** (R2 → R3 → R4 → R5)。R4 主控自查已写明「每轮都在『块内是否出现 rel_path』这个量上挪边界」并声称本轮换量; 实测**没有换量** —— 三轮的量依次是「块内出现 / `(parse_ok` 之后出现 / 平衡括号之内出现」, 三次问的都是同一个问题「`rel_path` 这个串出现在某个文本窗口里没有」, 只是窗口越缩越小 (memory `redfix-change-quantity`)。

**建议改法 (已三态实跑, 零回归)**: 换成**结构量** —— 数平衡括号内深度 1 的元素个数, 要求 >= 5 且第 5 个元素含 `rel_path`:

```python
def grp(s):
    d = 0
    for k, c in enumerate(s):
        d += (c == '(') - (c == ')')
        if d == 0: return s[:k+1]
    return ''
def elems(s):
    g = grp(s)
    if not g: return []
    out, d = [''], 0
    for c in g[1:-1]:
        d += (c == '(') - (c == ')')
        if c == ',' and d == 0: out.append('')
        else: out[-1] += c
    return out
ok = lambda s: len(elems(s)) >= 5 and 'rel_path' in elems(s)[4]
```

我在全部 24 个既有态 + 我的 10 个态上跑过该替换 (memory `check-runs-at-baseline-first`):

- base 全 FAIL / target 全 PASS / 18 个既有坏态与 3 个 alt 态 (含 `alt_tuple_wrapped` 元组跨两行) **逐格与 v5 期望一致, 零回归**;
- 我的 `adv_j1_inner_paren` / `adv_j3_inner_paren` / `adv_j2_inner_paren` 三攻击 **全部翻 FAIL**, `adv_j1_unclosed` 仍 FAIL。

同批把 `authoring_rules` 的「第 5 元写在元组括号之内」改写为「元组恰五个深度 1 的元素, 第 5 元就是 `(rel_path == filename, rel_path)`; 任何括注只能写在元组之外」, 并把这三个新坏态加进 `EXPECTED_FAILS` (每态一行, 成本已被 v5 的收窄降到最低)。**若不改判据**, 最小兜底是在 TASK-019 / TASK-020 的 verification 各加一句「元组第 5 元的字面必须与 TASK-014 `return` 语句逐字同形, 由主控在各自提交前人工逐字比对」—— 用一次人工比对补机械判据的缺口, 不动脚本。

#### M2 — `[Major] type=issue · category=delegated-mechanism-precondition · scope=TASK-031 主仓多远程推送 · v5 引入: 是`

**证据**: v5 按 PP4-M4 把主仓 master 的多远程推送整个交给 `phase-c-integrator` C.2.5 (`detailed-tasks.yaml:882`, `tasks.md:137`), 断言「C.2.5 的 per-remote 矩阵对 origin 与 github 两个 remote 均推送成功且 `verify_parity_post_push` 的 match 为 true」。去 C.2.5 源码核 (memory `delegate-verify` 的三问):

- 真做吗: 做 —— `aria/skills/phase-c-integrator/SKILL.md:617-621` 第 4 步 a/c/d 逐 remote 推子模块与主仓并做 parity; 有代码宿主 (`git-remote-helper/scripts/verify_post_push.py`)。
- **方式合约吗: 不合** —— `SKILL.md:602-603` 触发条件写死「Phase C.2 合并成功 (**master 已 fast-forward**)」, `:616` 第 1 步 `expected_sha = git rev-parse HEAD` 括注「**合并后本地 master HEAD**」。而本计划 TASK-031 全程 (`detailed-tasks.yaml:876-883`) **没有任何一步**把主仓本地 master 快进到合并后的 `origin/master`; 计划自己在 TASK-032 开头写明「TASK-031 走 Forgejo 服务端合并, **本地 master 此时落后**」(`detailed-tasks.yaml:900`)。
- 失败会发红吗: 会 —— 但发的是**误红**: 陈旧 master 推 origin 得「Everything up-to-date」(本地是祖先), 随后 `verify_parity_post_push(expected_sha=陈旧 SHA)` 与 origin 的合并后 SHA 不等 ⇒ 4 次 attempt 后阻断。

即: TASK-031 `:882` 与 TASK-032 `:900` 二者**必有一错**。若 C.2.5 真按其前置跑过, 本地 master 就不会落后; 若本地 master 确实落后, C.2.5 就是在陈旧 master 上推, github 永远拿不到那个合并提交而 origin 判 match=false。PP4-M4 判的「恒假」没有消除, 只是从「计划里没人推 github」换成了「被委托方的前置没人建立」。

**附带同根一处**: `detailed-tasks.yaml:880` 的「合并后核台账所记各主仓提交 SHA 均为 `origin/master` 的祖先 (`git merge-base --is-ancestor`)」同样缺 fetch 前置 —— 服务端合并后本地 `origin/master` 远端跟踪 ref 陈旧, 该断言必然为假 (memory `freshness-must-be-fetched` / `stale-local-main`), 是一次必然发生的误停。

**照计划执行会出的错**: 执行者走到 TASK-031 最后一步, 面对「C.2.5 的触发前置不成立」而计划没写怎么办 —— 按 Rule #10 他不得自行豁免, 只能停下上报, owner 在 Phase C 末尾多一个非计划内等待点; 此时主仓 origin 已带合并提交而 github 未同步, 处于镜像分叉态直到 TASK-032 的 Phase D 双推才恢复。(好消息: gitlink 侧无 10CG/Aria#165 暴露 —— TASK-030 `:857` 的双远端前置与 TASK-034 的 ls-remote 核验都在 TASK-031 之前, 子模块不会孤立。)

**建议改法**: TASK-031 在「PR 以 merge commit 合并」与「交 C.2.5」之间插一步, 写死:

```
git fetch origin && git checkout master && git merge --ff-only origin/master
断言 git rev-parse HEAD == <PR 合并提交 SHA>; 不能快进 ⇒ 停下上报
```

并把祖先断言移到这一步之后 (此时 `origin/master` 已新鲜); TASK-032 `:900` 的同一动作改写为「若 TASK-031 已快进则本步为幂等核验」。改动是三行, 不新增流程层。

#### m1 — `[Minor] type=risk · category=predicate-discriminating-power · scope=(c1)+(c2) · v5 引入: 部分 ((c2) 是 v5 收紧的那条)`

(c1) 只否定一个精确字面 `Returns only the basename`, (c2) 只正向要求 `path relative to` 出现在 `_list_handoff_files` 的 docstring 里。构造 `adv_c2_prefix_word`: 把契约句改写为「Returns the basename; the caller builds the **path relative to** the repo root」—— 语义仍是旧契约 (返回 basename), 但 (c1)(c2) **双双 PASS**, 19 条全绿 (实跑)。R4 m13 的收紧只堵住了「写错地方」, 没堵住「换个说法保留旧语义」。**建议**: (c1) 由单字面改为「函数 docstring 内不得同时出现 `basename` 与 `Returns`」这类结构判据, 或给 (c2) 加一个 `bad_c2_reworded_basename` 隔离态把该边界显式登记进 `:907` 的已知边界清单。

#### m2 — `[Minor] type=risk · category=threshold-criterion · scope=(l1) Scenarios · v5 引入: 是`

(l1) 的「含 `→` 的结局行 >= 4 且其中一条含 `target_in_subdir`」用门限代替结构。反向实证两支: `adv_l1_existing_line_plus_filler` (把 `target_in_subdir` 挂到既有结局行 + 加一条填充行) 被抓住 FAIL —— 门限确有边际价值; 但 `adv_l1_filler_only` (在 Scenarios 段插一条带 `→` 的旁白式交叉引用行 `(see ``_render_pointer``) → reasons: … "target_in_subdir"`, 第四种结局**根本没写**) **19 条全 PASS**。即门限只要求「多一条带箭头的行」, 不要求它是结局。**建议**: 判据加一条形状约束 (例: 该行须以 `active count` 开头, 或箭头左侧非空且右侧含 `"pointer"` / `"banner"` / `"skipped"` 之一), 并补一个 `bad_l1_decorative_arrow` 态。另注: `→` (U+2192) 被钉死, 用 ASCII `->` 写第四条结局会假红 (`legit_l1_ascii_arrow` 实测 (l1) FAIL) —— 已在 `authoring_rules` 事先告知, 属可见假红, 但 TASK-013 `:424` 正文只写「另起一条含 → 的结局行」, 建议补一句「必须用 U+2192, ASCII 箭头不算」。

#### m3 — `[Minor] type=issue · category=doc-sync · scope=tasks.md 读前必看第 14 条 · v5 引入: 是`

R4 m10 要求读前必看 14 与 v4/v5 谓词同步。(l1) 那半已落 (`tasks.md:31` 写到「结局行至少四条 (基线三条) 并有一条含 target_in_subdir」), **(c) 那半没落**: `:31` 仍写「(c) 前两条同原文 (c1)(c2)」。而 proposal `:425` 的原文 (c2) 是 `grep -q "path relative to" collectors/handoff_multibranch.py` —— **整文件 grep**; v5 已改成 AST 限定到 `_list_handoff_files` 自己的 docstring (`detailed-tasks.yaml:88`)。照读前必看字面派生的实现者会把契约句写进模块 docstring (proposal 原文恰恰在同一段讨论「模块 docstring 两个块各归其位」), 落地后 (c2) 红, 须回头返工。yaml `:350` 的任务正文写对了, 所以这是可恢复的一次误导。**建议**: `:31` 的 (c) 条改为「(c1) 同原文; **(c2) v5 收紧** —— 由整文件 grep 改为 `_list_handoff_files` 自身 docstring 的 AST 检查, 只写进模块 docstring 不算」。

#### m4 — `[Minor] type=risk · category=assertion-shape · scope=TASK-029 第 5 步 · v5 引入: 部分`

PP4-M2 的处置论证里明写了「重走时 `--no-ff` 会返回 `Already up to date.` 而不产生本轮的合并提交」(`detailed-tasks.yaml:807`), 但落地只治了成因 (两仓整体回退), 没有加正向断言。第 5 步现在只判退出码非 0; `Already up to date.` 退出码为 0, 于是第 6 步 (版本值 / CHANGELOG 计数 / 无同名 tag) 与第 7 步 (`HEAD == 合并 SHA`, 而「合并 SHA」正是刚取的那个未变的 HEAD) 全部照过, 第 8 步照打 tag —— 一棵没有本轮合并提交的树被打了发版 tag。计划内该分支需要「远端 master 已含 feature 分支」才可达 (第 3 步已挡住本地领先那一支), 概率低, 故判 Minor。**建议 (memory `assert-this-action`: 验动作发生须钉本次新产生的对象)**: 第 5 步收尾加一句「断言 `git -C <仓> rev-parse HEAD` 不等于第 3 步记下的 SHA 且 `git -C <仓> rev-parse HEAD^2` 成功并等于该仓 feature 分支 HEAD; 不成立 ⇒ 停下上报 (本轮未产生合并提交)」。

#### m5 — `[Minor] type=risk · category=authoring-constraint-surfacing · scope=authoring_rules 与各 TASK 正文 · v5 引入: 部分`

三条「合法写法会假红」的约束目前只在 `detailed-tasks.yaml:133` 的 `authoring_rules` 长串里: (a) (l1) 钉死 U+2192; (b) (c2) 钉死 `path relative to` 字面 (实测 `legit_c2_other_wording` 把契约句写成「Returns each file's ``docs/handoff/``-relative path」即 (c2) FAIL); (c) (j2) 要求 schema 元组不跨行。执行 TASK-009 / TASK-013 / TASK-019 的 subagent 读的是各自任务的 verification 列表, 其中 (b) 在 `:350` 有点名、(c) 在 `:575` 有点名、**(a) 没有**。都是可见假红 (会在 TASK-021 暴露), 但每次都要一轮返工。**建议**: 把三条各自复述到对应任务的 verification 一行内。

#### m6 — `[Minor] type=risk · category=single-check-point · scope=两份谓词原文一致性 · v5 引入: 是 (PP4-M3 的处置)`

PP4-M3 删掉了 TASK-029 第 7 步的 `--emit-json` 比对 (删得对 —— 我实跑确认实现落地后锚点必漂移, rc=3 拿不到 JSON), 把一致性全部压到 TASK-001 一次 (`:195`)。但 TASK-001 自身又允许「矩阵因此需变时由脚本输出重生成 yaml 各块」(`:196`), 而此后 TASK-021 `:621` / TASK-029 第 7 步 `:810` 跑的是 **yaml 副本**的 19 条。B.1 之后这条链没有第二个核验点。风险不高 (两份都在同一个 change 目录且无人改动), 但值得显式登记。**建议**: 把这条并进 `:907` 已经在写的「已知边界」段落 (一句话), 或在 TASK-021 加一句「若期间改过谓词, 重跑一次 `--emit-json` 比对」。

---

## 核对无误的部分

1. **脚本退出码六态全部实跑负控**: rc=0 (基线) · rc=1 (扰动 `EXPECTED_FAILS["bad_k_paraphrase"]` 加 `"b"` ⇒ `mismatch [bad_k_paraphrase][b]: expected FAIL, got PASS`) · rc=2 (未知 flag / 两个位置参数 / 源目录缺 FILES, 三支各自实跑) · rc=3 (改一个 count=1 锚点 ⇒ `anchor drift: … 锚点应恰出现 1 次, 实际 0 次`) · rc=4 **四个子因各自实跑** (未知标签 / 重复标签 / docstring 漏列状态 / `EXPECTED_FAILS` 与 `STATES` 顺序不一致) · rc=5 (源文件非 UTF-8 ⇒ `unexpected error: UnicodeDecodeError`)。全部与 `sc11-predicate-validation.py:40-43` 与 `detailed-tasks.yaml:104` 的口径逐字相符。
2. **`finally` 清理与只读性**: 六次异常路径与正常路径跑完后 `TMPDIR` 下零残留; 脚本只从 `src` 复制出去、只写 tmp, 审后三仓 HEAD (`0e60b08` / `1cb3872` / `8b49562`) 与 porcelain 未变。
3. **`EXPECTED_FAILS` + `expand_expected()` 的等价性**: 与 v4 (`edd256d`) 的定值矩阵在 18 个共有态 x 19 谓词 = 342 格上**零差异**, 表头顺序一致, 6 个新态纯增量 —— `tasks.md:68` 清单 30「断言强度不变」属实。`expand_expected` 的三重自检 (状态集/顺序 · 未知标签 · 重复标签) 与 `check_doc_lists_states` 的 docstring 漏列检查均已实跑证伪。
4. **实测矩阵与 yaml 逐字节一致**: 仓库根实跑 `python3 -B …sc11-predicate-validation.py` ⇒ rc=0, `verdict: OK (mismatch cells 0, stderr notes 0; 24 states x 19 predicates)`, stdout 与 `detailed-tasks.yaml:108-132` 的 `measured_2026_09_16_at_1cb3872_v5` 块**逐字节相同**。
5. **两份谓词原文一致 (本席独立实跑比对)**: `--emit-json` 的四字段全部与 yaml 对应块逐字节一致 —— `predicates` vs `sc11_baseline_predicates` 中 `(label)` 开头的 19 行、`states` vs `:105`、`expected` vs `:106`、`matrix` vs `:108-132`。
6. **机械计数自洽**: 35 个 TASK (id 无重复) · 27 个 parent 与 tasks.md 27 个 checkbox **双向无缺** · `est_hours` 求和 107.0 == `est_hours_total: 107` · agent 分布 qa 15 / ba 10 / km 10 == `metadata.agents` · 全部 `dependencies` 引用零悬空。
7. **行号锚点抽验全中 (1cb3872 实读)**: schema `:1076` `:1081` `:1103` `:1105` `:1113` `:1116` `:1124` `:1128` `:1134` `:1138` `:1158`; collector `:36` `:177` `:178` `:240` `:246` `:332` `:355` `:368` `:370` `:429` `:430` `:438` `:490` `:492` `:494` `:586` `:619` `:644` `:686` `:716`; writer `:30` `:277` `:287` 与「仅在单 active track 场景下写真实指针」**恰 2 处** (`:140` `:159`)。`:177` 注释与 `:178` 无斜杠值的矛盾确如 TASK-009 所述。
8. **归档门只读预演与 TASK-032 预测逐条相符**: 在 scratchpad 副本上勾满 27 行并以真 project_root 调 `gate_result` ⇒ `complete=True` / `verdict=warn` / `unverified_claims` **恰三条**, 且正是 `detailed-tasks.yaml:902` 点名的三条 (2.2 行 `HEALTHY_TRACKS` unclassified reference form · 4.4 行 no extractable symbol · 4.3 行 dogfood 无可链接产物路径)。`d_payload` 非 null (含 `unverified_claims` 键) ⇒ 按 `openspec-archive/SKILL.md:596` Step 7 会触发, `metadata.owner_gates` 第 12 项不是空转。`complete` 走 tasks.md 全 [x] 那半 OR 分支, 与 `:904`「全部勾选且无 carry-forward / defer 标注」的描述一致 (`spec_complete.py:257-292`)。
9. **TASK-032 的 5.5 父目录 token 处置确实有效**: `_ARTIFACT_PATH_TOKEN_RE` 在 5.5 整行只抽出 `aria-plugin-benchmarks/ab-results/` **一个** token (`AB_TEST_OPERATIONS.md` 不被抽出, 我原先担心的「前面还有一个存在的路径先命中」不成立); 把该 token 换成尚不存在的结果目录后 `classify_artifact_claim` 由 `verified=True` 翻 `False` ⇒ 替换动作确实把恒过变成可红。
10. **C.2.5 的三项配置事实属实**: `.aria/config.json` 的 `phase_c_integrator` 下**无** `multi_remote_push` 键 ⇒ `enabled` 走默认 true (`SKILL.md:604`); 配置无顶层 `multi_remote` ⇒ `enforced_remotes` 空 ⇒ 自动发现所有 remote (`SKILL.md:615`); `fail_on_partial_push: true` + 非 read_only 默认阻断 (`SKILL.md:630`)。(不成立的是它的**触发前置**, 见 M2。)
11. **`:907` 的已知边界清单精确**: 从 `EXPECTED_FAILS` 机械求解「哪些谓词有单点隔离态」, 结果恰为其补集 {a1, b, c1, f1, f2, i1, i2, j5, l2, l3} 十条无隔离态, 且 (g) 确由 `bad_changelog_only` 反向隔离、(j4) 的三个坏态确是同一条正则在三个文件上的行为 —— 与文字逐字相符。
12. **锚点唯一性 (今日实测)**: collector 中 `^# Tie-break` 恰 1 行、`^def _dedupe_sort_key(` 恰 1 行 ⇒ (j3) 的 fail-closed 前置成立; schema 全文只有 `:1124` 一行含 `(parse_ok` ⇒ (j2) 的 `all()` 今日无历史行假红面; `dictionary-max` 命中 6 行 (`:59` `:60` `:95` `:491` `:492` `:716`) 而四条模拟改动经「本行或下一行」窗口全覆盖 ⇒ (j5) 在 target 上为真不是侥幸。
13. **TASK-011 的区间锚点足以消歧**: `:644` 与 `:686` 两行 `fallback_date = _get_file_commit_date(project_root, branch, filename)` **逐字节相同**(含缩进), 但 deliverables 给的是「主循环 `:637-658`」区间, 恰好只框住 git show 失败那一支; 且实读确认 `:644` 的 `fallback_date` 唯一消费者就是被删除的那个 legacy append 块。
14. **content-integrity 自检 (v5 新增 191 行)**: `check_bare_issue_refs.py --repo-root=/home/dev/Aria` ⇒ 「裸 issue 引用: 0」rc=0; §4.5 自查命令对带圈/带框编号字符零输出; 字面 U+FFFD 计数 0。判据里用 `chr(0xFFFD)` 而非裸字符, 与 `hard_constraints` 末条一致。
15. **组 5 执行序与依赖图一致**: TASK-025/026 (5.3/5.5) 互不依赖且均先于 TASK-027 (5.1 aria) → TASK-028 (5.6) → TASK-029 → TASK-034 → TASK-030 (5.1 主仓) → TASK-031 → TASK-032, 与 `tasks.md:134` 标题行的执行序逐段相符。

---

## Verdict

**PASS_WITH_WARNINGS** — 0 Critical / 2 Major / 6 Minor。

组 1–4 的 24 个任务在本席的字符级镜头下未发现新缺陷 (行号锚点、区间消歧、机械计数、归档门预测全部实证相符), 与 R4 的分布事实一致。两条 Major 都落在 R4 已点名的两簇 (PP4-M6 谓词族 / PP4-M4 主仓推送) 上: **文字按处置落了, 机制没闭合**。两条的修法都是「换一个量」或「插一步 fetch + ff」, 不新增流程层, 且我已把谓词那条的替换写法在 34 个状态上实跑验证过。

## Vote

**REVISE**

理由: M1 是同一族谓词连续第四轮被绕过, 且这一轮的绕法 (元组内嵌括注) 比前三轮更像真实落笔; 放它进 Phase B 等于把一条「本 Spec 核心契约的文档同步」判据留成装饰。M2 把一个「计划里没人做」的恒假换成了「被委托方前置没人建立」的恒假, 会在 Phase C 最后一步炸出一个非计划内的 owner 等待点, 并在 origin 已合并而 github 未同步的窗口里停留。两条合计约 5 行改动 + 3 个新坏态, 修完不必再开一轮 —— 我不建议加 R6, 建议**定点修这两条后由主控核验放行**。

---

## 边际判断

### 1. SC-11 谓词族这一轮的换量是否终于结构性?

**否, 仍是同一个量的第三次挪边界。** 三轮的判据依次是「块内出现 `rel_path`」→「`(parse_ok` 之后出现」→「平衡括号之内出现」, 问的始终是同一个问题:「`rel_path` 这个串落在某个文本窗口里没有」, 变的只是窗口边界。我把窗口缩到理论最小 (元组自己的括号内) 之后, 仍能用一句合乎语境的括注把串塞进去, 而那句括注 (`filename (basename, never rel_path)`) 恰恰是本 Spec 语境下最可能被写出来的澄清。**攻击面没有收敛到「只能靠真的改元组才能通过」**, 只是把攻击构造从「加一句」升级成「加一句带括号的」。真正的结构量是「元组有几个深度 1 的元素、第 5 个是什么」—— 换上之后, R4 两席的三个攻击、我的三个攻击、加上不闭合括号那一支, 全部翻红, 24 个既有态零回归 (我已实跑)。判断口径给未来: 判据里凡是 `X in 某段文本` 形态的, 都还在「串出现没有」这个量上; 只有开始数结构元素 (元素个数 / 位置 / 类型) 才算换了量。

### 2. 24 态 x 19 谓词相对它保护的对象是否划算?

**体系本身已经便宜, 不划算的是覆盖分布。** v5 的 `EXPECTED_FAILS` 收窄是本轮最成功的一项 —— 我新加 10 个态只写了 10 个函数 + 0 行期望表 (它们不进 `EXPECTED_FAILS` 也能单独跑), 加态成本确实塌到接近零。问题在分布: 19 条谓词里 9 条 (j1 j2 j3 j4 k l1 a2 c2 g) 吃掉了全部 15 个隔离态, 另 10 条一个都没有; 而这 9 条里 (j1)(j2)(j3) 独占 6 个态, 连续四轮的缺陷也全在这 6 个态想守的同一个地方 —— **态数增长与鉴别力增长已经脱钩**。

收口形态 (建议给 owner 的可执行版): (a) (j1)(j2)(j3) 合成一条共享判据 —— 它们本来就共用同一个 `ok()`, 只是取文本的三种方式; 判据换成元素计数式后, 坏态从 6 个缩到 2 个 (「元组没改」与「括注冒充」各一); (b) 省下的 4 个态匀给今天零隔离、却真会被漏改的 (i2)(j5)(l2); (c) 十条无隔离态的清单保持写进周期 handoff (`:907` 已在做, 处理正确)。净结果: 总态数 24 → 约 20, 鉴别力升而不降。**不划算的从来不是「记录已知边界」, 是继续在同一族上加轮。**

### 3. 若 owner 选「接受当前结论进 Phase B」, 执行期风险?

三条, 按后果由重到轻:

1. **M1 会静默通过, 后果落在 ship 之后。** TASK-021 与 TASK-029 第 7 步的「19 条谓词全部为真」会全绿, 合并、打 tag、发版一路放行; 真正的代价是 `state-snapshot-schema.md:1124` 这条机读契约 SOT 与 collector 的两处契约注释对外声明四元排序键, 而代码是五元 —— 下一个读 schema 的消费方 (Layer L / `track_board.py` 的 renderer parity 论证就挂在 `:1134`) 拿到错误的键层级, 而这正是本 Spec 立 (j) 族的唯一理由。**零脚本改动的缓解**: TASK-019 / TASK-020 各加一句「元组第 5 元的字面必须与 TASK-014 `return` 语句逐字同形, 主控提交前人工逐字比对」。
2. **M2 会在 Phase C 最后一步炸。** 执行者发现 C.2.5 的触发前置 (本地 master 已 ff) 不成立, 按 Rule #10 不得自行补步骤, 只能停下上报 —— owner 多一个非计划内等待点, 而此时主仓 origin 已带合并提交、github 未同步, 镜像分叉要等到 TASK-032 的 Phase D 双推才恢复。子模块侧无 10CG/Aria#165 暴露 (TASK-030 的双远端前置在 TASK-031 之前)。**缓解成本三行** (fetch + checkout + ff-only + 一条 HEAD 断言)。
3. **小额返工摩擦。** m3 会让实施者按读前必看把契约句写错位置 (一次返工); m5 的三条假红约束没有复述到任务正文, 每条命中一次就是一轮 subagent 往返; m2 的装饰性箭头行与 m1 的措辞改写属于「判据没抓到但人也不太会那么写」, 执行期大概率不触发。

**总的判断**: 组 1–4 我这一轮用字符级镜头过了一遍, 没有找到新的执行期障碍; 风险确实只剩这两处, 且两处的修法都是「加一句 / 换一个表达式」而不是新机制。**我倾向的三选一是「定点修 M1 + M2 后由主控核验放行, 不开 R6」** —— 加轮的边际产出在本议题上已经转负 (memory `marginal-return-negative`), 而这两条的修法是可证伪的、我已经在 34 个状态上跑过其中一条。

---

## 轮次记录

| 轮 | counts | 本席关注面的演化 |
|---|---|---|
| R1 | 0C/13M | SC-11 由整文件 grep 改为 19 条定位谓词 (PP1-M2) |
| R2 | 0C/9M | (a2) 定位到 Fail-soft 行反引号内的形状 dict; (j4) 同义词扩面; (k) 只认字面; (l1) 分段 |
| R3 | 0C/9M | (j1)(j3)(j2) 由「块内出现」改为「`(parse_ok` 之后出现」(第一次挪边界); (l1) 取标题到首个空行 |
| R4 | 0C/7M (REVISE 3 / PASS 2) | 同族被「同段 / 同块 / 同行在元组后补一句」攻破 (PP4-M6); (l1) 标题括注 (PP4-M7); 主仓推送恒假 (PP4-M4) |
| **R5 (本席)** | **0C/2M/6m · REVISE** | 平衡括号仍被「元组内嵌括注」攻破 (第三次挪边界, M1); 主仓推送的恒假换成被委托方前置不成立 (M2); 组 1–4 字符级零新缺陷; 脚本六态退出码 / 四字段一致性 / 342 格等价性 / 归档门三条预测 全部实证相符 |

**收敛读法**: Major 趋势 13 → 9 → 9 → 7 → **2**, 且两条同属 R4 已点名的两簇 (不是新面), 修法均为「删/换表达式/插一步」。按 memory `stop-adding-rounds`, major 仍在降且本轮是新鲜眼睛 —— 但降幅已进入「两条定点缺陷」量级, 继续加轮的边际产出转负 (memory `marginal-return-negative`)。本席建议不开 R6。
