---
checkpoint: post_planning
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-12T02:10:00.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R4 — tech-lead 席位报告

## 0. 被审对象的更正 (先说, 因为它改变了本轮的计量口径)

任务书正文写「R3 — 被审对象 = R2-fix 后的 A.2 产物 (commit `0dd26ce`)」, **与仓内实况不符**。实跑:

```
$ git log --oneline -15 -- openspec/changes/premerge-gate-mainbranch-failclosed/
e970943 docs(spec): R3-fix — 不再做第四次同形换量, 改为「停止预写量 + 诚实上报」; xcheck 补齐维度
878ee44 docs(spec): post_planning R2 (FAIL) + R2-fix — 换人执笔量化 53%, 并加一道机械条款间交叉检查
6818773 docs(spec): R1-fix 换人执笔 — 4 条待裁项结清 + 10 席裁定
0e27f0d docs(spec): premerge-gate-mainbranch-failclosed A.2 + 六轮审计
ab4da15 docs(spec): A.1 premerge-gate-mainbranch-failclosed (Level 2)

$ git status --short openspec/changes/premerge-gate-mainbranch-failclosed/
(空 — 工作树干净, HEAD = e970943)
```

且 `.aria/audit-reports/` 内 **post_planning R3 五席报告 + R3 aggregate 均已存在** (R3-0..R3-4 + `post_planning-R3-1786494000000-...-aggregate.md`)。交付契约要求的文件名是 **`R4-0`**、frontmatter 要求 `rounds: 4`。

⇒ **我审的是 R3-fix 后的产物 (`e970943`), 我是 R4 的 tech-lead 席位。** 任务书的「R2/R2-fix」措辞是 R3 轮提示词的陈旧复制。
本报告据此把 schema 字段 `introduced_by_r2fix` 一律读作「**由本轮被审的那次 fix (= R3-fix) 引入**」, 并在 §5 给出两种口径的比例。

---

## 1. 投票

| 项 | 值 |
|---|---|
| VOTE | **REVISE** |
| VERDICT | **FAIL** (1 Critical) |
| findings | **1C + 5M + 2m = 8** |
| blocks_phase_b | **3** |
| 由 R3-fix 引入 | **4 / 8 = 50%** (仅计三件套产物则 1/5 = 20%, 见 §5) |

---

## 2. R2 的 1C + ~13M 是否真闭合 —— 逐条回源

**结论: R2 那一批已实质闭合**, 我逐条回到源文件核过, 没有采信「已修」的声称。同时 R3 的两条 Critical 与三条事实错误也已闭合。

| R2 条目 | 回源核验 | 判定 |
|---|---|---|
| **Critical** TASK-020 fail-CLOSED 无插入点规定 | `proposal.md §6.1` 存在 (`:222-258`); 三条用例表 `:249-253`; 信号通道条款 `:255-256` 要求走 CLI 真实路径 | ✅ 闭合 |
| TASK-010 移交 TASK-008 而无依赖边 | 实跑 PyYAML: `TASK-008.dependencies = [003,004,005,007,010]` | ✅ |
| TASK-015 排在 TASK-020 之前 (AB SHA ≠ ship SHA) | `TASK-015.dependencies` 含 `TASK-021`; `TASK-021` 闭包含 `TASK-020` | ✅ |
| TASK-014 第三版量 `{:610}` 恒红 | 已作废并逐条留痕 (a)(b)(c)(d); 本轮停止预写量 | ✅ (处置见 §3) |
| MAJOR 落地面 8 文件无 task / 不在 scope | `TASK-017.deliverables` 含 10 条真实文件路径; `scope_repos` 两侧均已补 | ✅ (但引入新缺陷, F-1/F-7) |
| SC-M12 仍只挂 spike | `TASK-011` 新增「SC-M12 对落地文本复跑」认领 + deliverables 补 `test_pre_merge_gate.py` | ✅ (但机械检查对其复发失明, F-4) |
| SC-M10 缺 legacy key 交叉输入变体 | `proposal.md:321` 逐字含变体 (a)/(b) | ✅ |
| `:338`/`:345` 两条早退缺因果断言 | `TASK-008` verification 逐字含 `assert ls-remote 未被调用` | ✅ |
| config-loader 无 rule6_note / substitute SC / issue | `proposal.md §Rule #6` 三件套齐 + SC-M17 + TASK-019 (8) | ✅ |
| SC-M3b 拒绝域窄于其声称 | pattern 已扩 `['\"]?`; TASK-001 本轮同步 | ✅ |
| §5 catch-all 里 `UnicodeDecodeError` 无编号 | SC-M14 已编号 | ✅ |
| TASK-019 未真正含 standards 矛盾项 | 现为第 (7) 项, tasks.md:167 与「已裁」段口径一致 | ✅ |
| 步骤 6 确定式 vs 条件式矛盾 | `proposal.md §3` 已改条件式 | ✅ |
| 无终局全量收口 | TASK-021 存在, **且其依赖闭包经我实跑证实完整** (见下) | ✅ |

**TASK-021 是否真收口 —— 实跑而非采信** (我的席位职责):

```python
# 交付 SC 断言面文件、但不在 TASK-021 依赖闭包内的任务
交付 SC 断言面文件、但**不在** TASK-021 依赖闭包内的任务:
  (空)
TASK-021 闭包: TASK-001..TASK-014 + TASK-020  (15 条)
与 TASK-021 无序: TASK-016(交 CLAUDE.md) / TASK-018(交核验记录) / TASK-019(交 issue)
```
⇒ **TASK-021 在「谁还会改被 SC 断言的文件」这个维度上是完整的**, 三条无序任务无一交付 SC 断言面文件。这是本 Spec 少数经得起机械复核的结构性修复。

**R3 的两条 Critical + 三条事实错误** 也已闭合, 我独立复跑:

```
$ grep -cE '^#### +TASK-014 验收判据' proposal.md          → 0     (TASK-014 今日红, 且不预设 F 形状)
$ grep -c -- '<MAIN_BRANCH>' .../SKILL.md                  → 0     (SC-M16 今日实测确为 0, R3 抓到的假值 1 已改)
$ git rev-parse HEAD:aria/skills/phase-c-integrator/SKILL.md  → rc=128 fatal (旧命令确不可执行)
$ git -C aria rev-parse HEAD:skills/phase-c-integrator/SKILL.md → rc=0 4c1fd90…  (新命令可执行)
$ cd aria/skills/phase-c-integrator/tests && python3 -m pytest -q → 111 passed   (红窗前提仍成立)
$ 四文件承诺措辞计数 → 2 / 4 / 3 / 0   (SC-M18 声称值逐位命中)
$ grep -cE '…' config-loader/SKILL.md → 2                  (SC-M17 声称值命中)
```

⇒ **`r2_closure` = 闭合**。本轮 findings 中**没有一条**是 R2 旧条目的复发。

---

## 3. 那道机械交叉检查真的有效吗 —— 我做了 8 个独立对抗构造

先跑当前取值 (仅作起点, 不作证据):

```
$ python3 …/xcheck.py openspec/changes/premerge-gate-mainbranch-failclosed
RESULT: PASS — 六项交叉检查全部通过
```

然后**在隔离副本上做 8 个构造, 全部不在它自带的 `xcheck_adversarial.py` 覆盖内** (脚本: `/tmp/claude-1000/-home-dev-Aria/a87f33ea-9a9d-49e2-a762-18d0fd38bfc4/scratchpad/r4_adv.py`):

| # | 构造 | 目标 | 结果 |
|---|---|---|---|
| A | 删掉 TASK-011 对 SC-M12 的「落地文本复跑」认领 ⇒ **原样复现 R2 那条 Major「SC-M12 仍只挂 spike」** | CHECK2 | 🔴 **放行 (PASS)** |
| B | `TASK-009.dependencies` 由 `[TASK-008]` 改 `[TASK-006]` ⇒ SC-M6 两个半边**失序** | CHECK1 | 🔴 **放行 (PASS)** |
| C | 把行号重新做成验收量, 写成「grep -n 输出的行号必须是 262 与 559」(**不带冒号**) | CHECK3 | 🔴 **放行 (PASS)** |
| D | (正控) proposal 加「存在性核验的核验点必须落在 `evaluate_path_coverage` **之后**」 | CHECK4 | ✅ 拒绝 |
| E | 同一冲突改写成「存在性核验**紧随** `evaluate_path_coverage` 执行, 不得早于它」 | CHECK4 | 🔴 **放行 (PASS)** |
| F | 抽掉 TASK-020 的 `test_pre_merge_gate.py` 交付面 | CHECK2 | ✅ 拒绝 (SC-M17/M18) |
| G | `TASK-021` 不再依赖 `TASK-020` | CHECK1 | ✅ 拒绝 |
| H | SC-M18 今日实测 `2/4/3/0` 篡改为 `2/4/0/0` | CHECK5 | ✅ 拒绝 |

**4 拒绝 / 4 放行。** 对比 R3 的 1/5, 拒绝能力**确有实质提升** (CHECK5/CHECK6 是真新增能力, CHECK1 对显式句式的方向断言是真的, CHECK2 对「真 owner 无测试交付面」是真的)。但:

### 3.1 逐条回答任务书的四个问题

**(1) 四项判据覆盖得住 R2 那两个形状吗? 有没有 R2 findings 属于这两形状却逃过?**
**有, 而且是最关键的一条。** 构造 A 把 R2 的 Major「SC-M12 仍只挂 spike」原样放回去, xcheck **仍报 PASS**:

```
  SC-M12   转绿认领=TASK-001✓,TASK-002✗                      红窗=-         ✓
RESULT: PASS — 六项交叉检查全部通过
```

病因: CHECK2 的 `RED_CTX` 只认 `("必须 RED","⇒ RED","先看到红","先看到全红","实施前实测")` 五个串。TASK-001 里那条**「明确不建红窗的四条 + 理由」**的 bullet 一个都不含 ⇒ 它对 SC-M10/M11/M12/M15 的**免责说明**被判成「转绿认领」, 而 TASK-001 交付 `test_pre_merge_gate.py` ⇒ 一个 ✓ 就把整行顶绿。
未变异的当前输出里, **SC-M3b / SC-M3c / SC-M12 / SC-M15 四行的 `TASK-001✓` 全是这个误判** ⇒ CHECK2 对 20 行中的 4 行结构上 fail-OPEN。R3 诊断 CHECK2 的病是「把作废/否定语境算作 owner」, 本轮修的是**作废**语境, 漏的是**免责-不建红窗**语境 —— 同族, 只修了实例。

**(2) 有没有恒绿的判据?**
- CHECK4 的三条「回归性子项」是硬编码串存在性, 代码里已自陈「只防删除, 不构成对新矛盾的检测」—— 诚实, 但那三行相对于产生它们的 fix 仍是重言式;
- CHECK5 对 SC-M6..SC-M14 共 **9/20 行**因「今日实测非数字」直接 skip ⇒ 那些行零覆盖;
- CHECK1 的定向断言只覆盖 **20 / 82** 对 (task, 被点名 TASK) 提及 = **24%**;
- CHECK6 只看 `dependencies` 的 `task_group` 数值倒置, **看不见 tasks.md 组标题的散文承诺** (见 F-8)。

**(3) 它自己是不是「只修实例不修类」的产物?**
**是。** 三条硬证据:
- `RED_CTX` / `HANDOFF` / `HISTORY` / `QUANT_EXEMPT` / `PRESCRIBE` **全部是从本 Spec 当前文本里采下来的字面串**。构造 C (行号当量但不写冒号) 与 E (同义词表达的插入点冲突) 都因此逃逸;
- CHECK1 的注释逐字写「⚠️ 不收『半边归 TASK-xxx』这类措辞 —— 歧义句式一律不断言」。而**「按半边拆分认领」正是 R3-fix 自己新造的移交形态** (TASK-008/TASK-009 拆 SC-M6, 并被提升为 `metadata.evaluation_time_convention` 派生规则 (1))。⇒ **本轮新造的那一类移交, 恰好是 CHECK1 明文不管的那一类** (构造 B 实证);
- CHECK4 的 `SUBJECT`/`ANCHOR` 仍是本 Spec 专属的两个插入点与六个代码锚。

**(4) 拒绝能力 vs 当前取值** — 上表即是, 我没有采信任何「当前 PASS」。

### 3.2 对 tasks.md 与 audit_state 那句声称的判定

`tasks.md:7` 逐字:「**每项都以「好实现 PASS + 像样的坏实现 FAIL」的对抗 fixture 验过拒绝能力 (12/12 构造被拒, 含 R3 那 5 个原样复现)**」; `metadata.audit_state` 同义。

12/12 是**对它自己挑的 12 个构造**成立的。换一组独立构造得 4/8。**该句在字面上为真、在读者会读出的含义上为假** —— 读者会读成「R2 那两个形状已被机械杜绝」, 而构造 A 证明 R2 自己那条 Major 放回去仍是绿的。这与本 Spec 通篇援引的 memory `adversarial-fixture` / `selfcheck-values-not-questions` 是同一形状。

---

## 4. 逐条 finding

### F-1 🔴 **Critical** — TASK-017 第 9 项「主仓 gitlink」判据在 Phase B 结构上不可求值; 若照字面在 Phase B 求值, 产出的正是它自己引用的 Aria #165 失效

**locator**: `detailed-tasks.yaml` TASK-017 verification 第 4 条 · `tasks.md:141` · `proposal.md:394`
**逐字** (tasks.md:141):
> ⇒ **判据换到树对象层**: 主仓根跑 `git rev-parse HEAD:aria` (实跑 rc=0), 断言其值 == aria 子模块本 change 落地 commit 的 SHA。**怎么会红**: root README badge 已写新版本而 gitlink 仍指旧 SHA ⇒ `clone --recursive` 拿到旧插件 (**Aria #165 同族**)

**实跑**:
```
$ git rev-parse HEAD:aria           → af87caeeed88af6af76f29a8002badbe1228d927
$ git -C aria rev-parse HEAD        → af87caeeed88af6af76f29a8002badbe1228d927
$ python3 -c "…TASK-017 verification 里 'Phase C'/'Phase B'/'移交'/'不计入' 的出现次数"
  Phase C -> 0   Phase B -> 0   移交 -> 0   不计入 -> 0
```

**缺陷**: 「aria 子模块本 change **落地** commit」在 Phase B **不存在** —— 子模块的落地 commit 由 Phase C.2 的本地 merge 产生 (CLAUDE.md「多远程推送 — 两条硬约束」约束 1 逐字规定子模块合并必须本地做, 主仓**随后**才 bump gitlink)。于是两个独立实施者:
- 实施者甲: 判定不可求值 ⇒ 跳过 / 标注移交 Phase C ⇒ **该判据在 Phase B 恒真空转**;
- 实施者乙: 为让断言成立, 在 Phase B 把主仓 gitlink bump 到 **aria feature 分支的 tip** ⇒ 那正是 CLAUDE.md 约束 1 逐字点名的 **orphaned gitlink**, `clone --recursive` 断裂 —— **即本判据自己写在「怎么会红」里的那个失效** (Aria #165, CLAUDE.md 记载已四次复发)。

**为什么算 Critical 而不是 Major**: (i) 两个独立实施者对同一规格得相反结果 (memory `spec-underdetermination`, R2 判 TASK-020 插入点为 Critical 用的就是这条判据); (ii) 错的那支的后果是本仓最重的一类生产事故。

**同轮的类/实例证据 (这是本条最关键的地方)**: R3-fix 在**同一次提交**里把 TASK-015 的 blob-SHA 判据**正确地**拆成了
`**[Phase B · 本任务 · 机械可求值]**` + `**[Phase C · 明确移交 · 不在 Phase B 求值]**`, 并把该规则提升为 `metadata.evaluation_time_convention` 派生规则 (2) 逐字:
> 若某条断言的比较对象在 Phase B 内根本不存在 (典型:「与 Phase C 落地时的 X 相等」) ⇒ 必须拆成「Phase B 可求值的那半」+「明确标注移交 Phase C 的那半」

**而同一轮新写的 TASK-017 第 9 项没有做这个拆分。** ⇒ 「只修实例不修类」在**关闭该类的同一轮里、由同一位执笔者、在相邻两条任务上**复发 (memory `fix-recurs-in-fallback`)。

**怎么会红**: 让实施者在 TASK-017 完成点执行该判据 —— 要么答不出「落地 commit 的 SHA」是什么 (不可求值), 要么 bump 到未合并的 SHA (制造 orphan)。任一分支即证实本条。
**blocks_phase_b**: 是。

---

### F-2 🟠 **Major** — CLAUDE.md 规则 #8 的同步面只覆盖了「分支存在性」这一条腿; TASK-020 的 legacy-key 硬失败使 `CLAUDE.md:113` 的既有陈述条件性为假, 而没有任何任务承接它

**locator**: `detailed-tasks.yaml` TASK-016 (deps=`[TASK-008]`, 机械腿 `grep -cE '分支存在性|main-branch-not-found' CLAUDE.md`) · `tasks.md:134-136` · `proposal.md §6.1 用例表 :252`
**实读 `CLAUDE.md:113`** (逐字):
> 8. **PR merge 前必跑 pre-merge gate** — … **无可用 backend 按 `no_ci_fallback` 显式降级**; stub backend 抛 NotImplementedError 时 gate 必须 abort, 不得静默降级。

**实读 `proposal.md:252`** (§6.1 三条用例之二, 逐字):
> `enabled=true` + `no_aether_fallback` + 无可用 backend | `fail` + `raw_message` 点名旧键

⇒ 本 change 落地后, **对「带 legacy key 且无可用 backend」这一输入类, `CLAUDE.md:113` 描述的行为不再发生** (硬失败在 `:337` 之前触发, 根本走不到 `:339` 的 `no_ci_fallback` 降级)。

**实跑**:
```
$ grep -cE '分支存在性|main-branch-not-found' CLAUDE.md          → 0   (TASK-016 的机械腿, 今日红, 正确)
$ python3 …  TASK-016.dependencies                               → ['TASK-008']    (**不含 TASK-020**)
```

**缺陷**: TASK-016 的 title/verification/机械腿**三处**都只锚在「新增第三条阻断腿 = 分支存在性」, 对 TASK-020 新造的**第四条阻断行为**零覆盖; 且 DAG 上 TASK-016 与 TASK-020 **无序** ⇒ 即使实施者想一并同步, 排序也不保证他此时看得到 TASK-020 的落地形态。这直接抵触不可协商规则 #3「文档与代码必须同步更新」, 而 Rule #8 的 SOT 段正是本 Spec 自己在改的东西。

**怎么会红**: 落地后跑 `grep -nE 'primitive_preference|no_aether_fallback|legacy' CLAUDE.md` → 0, 同时 `gate_check(config={"no_aether_fallback":"abort"}, …)` 在无 backend 下返 `verdict="fail"` 而非按 `:113` 所述降级 ⇒ 文档与代码相反。
**introduced_by_r3fix**: 否 (TASK-016 的窄口径自初稿即有; R3-fix 加的机械腿把这个窄口径**固化**成了看起来已闭合的样子)。
**blocks_phase_b**: 是。

---

### F-3 🟠 **Major** — `.aria/config.template.json` 的 **legacy 键名面**零机械断言; SC-M18 这个「类级修复」把真正的对外爆炸面显式排除在外

**locator**: `proposal.md:329` (SC-M18 行) · `tasks.md:148, :150, :161` · TASK-020 verification
**实跑**:
```
$ grep -nE 'primitive_preference|no_aether_fallback' .aria/config.template.json
75:      "primitive_preference": [
78:      "no_aether_fallback": "skip_with_warning",
$ grep -cE 'still (readable|works)|removed in v2\.0|仍读|v2\.0 移除' .aria/config.template.json → 0
```
**实读 `proposal.md:329` 逐字**:
> ⚠️ `.aria/config.template.json` 今日已是 0 … ⇒ 该分量是**负控** … 其**键名面**归零由 TASK-020 的中英并列枚举口径管辖, **不并入本 SC**

**缺陷**: SC-M18 是 R3-fix 为闭合「只修实例 (SC-M17) 不修类」而新增的类级 SC。但它管的是**承诺措辞**维度; 而模板文件在承诺措辞维度**今日就是 0**, 它真正的问题在**键名维度** —— 且这是**唯一一个受众在仓外**的落点 (CLAUDE.md 指定的采用方复制源)。⇒ 一个删光全部「v2.0 移除」措辞、却把 `"primitive_preference"` / `"no_aether_fallback"` 原样留在模板里的实现, **能通过 SC-M1..SC-M18 全部 20 行、通过 §6.1 三条用例、通过 CLI 真实路径用例、通过 TASK-021 终局收口**, 而每个新采用方 clone 后第一次跑 gate 就撞 fail-CLOSED。`tasks.md:161` 自己逐字写着「**模板必须同批改, 否则每个新采用方一开箱就撞硬失败**」—— 后果被写下来了, 但**没有任何机械信号会为它变红**。

这正是本 Spec 通篇用来定 Major 的那句判据 (`tasks.md:148` 逐字):「无编号即不被任何机械勾稽点找到, 只能靠人工读散文」。

**怎么会红**: 建一个「删措辞不删键名」的实现, 跑完 SC-M1..M18 全绿。
**introduced_by_r3fix**: 否 (缺口早于本轮; R3-fix 的 SC-M18 显式把它排除, 属**未扩到**而非**新造**)。
**blocks_phase_b**: 是。

---

### F-4 🟠 **Major** — `xcheck.py` CHECK2 对 SC 表 20 行中的 4 行 fail-OPEN; 把 R2 那条 Major 原样放回去它仍报 PASS ⇒ `tasks.md:7` / `audit_state` 的「12/12 构造被拒」不支持它被读出的结论

**locator**: `tasks.md:7` · `detailed-tasks.yaml metadata.audit_state` 末段 · 机制 `scratchpad/xcheck.py` CHECK2 (`RED_CTX`)
**实跑** (构造 A, 隔离副本, 只删掉 TASK-011 那条 SC-M12 认领 bullet, YAML 解析通过):
```
  SC-M12   转绿认领=TASK-001✓,TASK-002✗                      红窗=-         ✓
RESULT: PASS — 六项交叉检查全部通过
```
未变异版本的同一行是 `转绿认领=TASK-001✓,TASK-002✗,TASK-011✓`。**删掉唯一的真转绿 owner, 判据不变。**

**缺陷**: `RED_CTX` 五个串识别不了 TASK-001 那条「明确不建红窗的四条 + 理由」bullet, 于是它对 **SC-M10 / SC-M11 / SC-M12 / SC-M15** 的免责被记成转绿认领, 而 TASK-001 交付测试文件 ⇒ 这四行永远有一个 ✓。R3 诊断的 CHECK2 病因是「把作废/否定语境算作 owner」, 本轮只修了「作废」这一支。

**怎么会红**: 上面那条实跑即是。修法方向: 把「转绿认领」判据落在**任务是否声明自己使该 SC 达到期望值**上, 而不是「提到了它且没说作废」。
**introduced_by_r3fix**: 是 (CHECK2 与那句「12/12」声称都是本轮产物)。
**blocks_phase_b**: 否 (它不阻断实施, 但它是本轮**核心处方**的有效性证据本身)。

---

### F-5 🟠 **Major** — CHECK1 对本轮**自己新造**的「SC 按半边拆分认领」移交形态零断言; 把 SC-M6 两个半边的 DAG 序抽掉仍 PASS

**locator**: `xcheck.py` CHECK1 注释「⚠️ 不收『半边归 TASK-xxx』这类措辞 … 歧义句式一律不断言」 · `metadata.evaluation_time_convention` 派生规则 (1)/(3) · TASK-008 / TASK-009 verification
**实跑** (构造 B): 把 `TASK-009.dependencies` 由 `[TASK-008]` 改为 `[TASK-006]` ⇒
```
RESULT: PASS — 六项交叉检查全部通过
```
**缺陷**: `evaluation_time_convention` 派生规则 (3) 逐字要求「凡 verification 里点名其他 TASK 作为移交对象, DAG 上必须存在**方向正确**的依赖边, 机械判据见 xcheck.py CHECK1」。而 CHECK1 **明文把「半边」句式排除在断言之外** —— 于是这条规则对它自己点名的那个新形态 (SC-M6 的 verdict 半边 / raw_message 半边) **没有机械执行力**。变异后, 一个合法拓扑序可把 TASK-009 排在 TASK-008 之前 ⇒ TASK-009 要为一条尚不存在的核验路径写 `raw_message` 诊断, 其 verification 在完成那一刻不可求值 —— **正是 evaluation_time_convention 要禁的那件事**。

另: CHECK1 的定向断言只覆盖 **20/82** 对 (task, 被点名 TASK) 提及 = **24%**, 其余一律不断言 (脚本已诚实标注覆盖边界, 但该边界恰好切掉了本轮新增的那类)。

**怎么会红**: 上面那条实跑即是。
**introduced_by_r3fix**: 是。
**blocks_phase_b**: 否。

---

### F-6 🟠 **Major** — CHECK3(b) 与 CHECK4 判的是**字面形状**而非**性质**; 两个像样的坏写法各自逃逸

**locator**: `xcheck.py` CHECK3 `QUANT` 正则 · CHECK4 `PRESCRIBE` / `REL_BEFORE` / `REL_AFTER` 字面元组
**实跑**:
- 构造 C — 把行号重新做成活验收量, 写成「验收: `grep -n` 输出的**行号必须是 262 与 559** 两个值, 否则判红」(不带冒号前缀) ⇒ **PASS**。`QUANT = (恰为|恰好为|恰等于|==|等于)\s*[{\[（(]{0,2}\s*[:：]\d{2,4}` 强制要求比较符**紧接冒号锚**, 去掉冒号即逃逸。而 TASK-014 作废量 (c) 的本质是「**行号成了验收量**」, 与写不写冒号无关。
- 构造 E — 把与 §6 相反的插入点指令写成「存在性核验**紧随** `evaluate_path_coverage` 执行, 不得早于它」⇒ **PASS**。同一冲突改用 `必须落在 … 之后` (构造 D, 正控) 则被正确拒绝。⇒ CHECK4 拒的是**动词表**里的词, 不是**关系**。

**缺陷**: 两项都对「换一种说法的同一个错」免疫。这与 memory `invariant-dimension` 是同一诊断的下一层: R3 说它是「无向」的, 本轮补了方向; 但它仍是**词表匹配**而非**语义判定**。

**怎么会红**: 上面两条实跑即是。
**introduced_by_r3fix**: 是。
**blocks_phase_b**: 否。

---

### F-7 🟡 **minor** — 「**8 个已知文件落点**」与实际列出的 **10 条文件路径**计数法不一致 (本 Spec 自己的口径规则)

**locator**: `proposal.md:394` · `tasks.md:140` · `TASK-017.deliverables`
**实跑**:
```
$ python3 -c "…TASK-017 deliverables…"
['版本引用点清单 (随 Phase C 落地)', 'aria/.claude-plugin/plugin.json', 'aria/.claude-plugin/marketplace.json',
 'aria/VERSION', 'aria/CHANGELOG.md', 'aria/README.md', 'VERSION', 'README.md',
 'README.ja.md', 'README.ko.md', 'README.zh.md']        ← 10 条文件路径
```
「8」只在把 `README.{ja,ko,zh}.md` 算作 1 项时成立。本 Spec 通篇要求「引用计数前必须并列写出总体 / 范围 / 计数法」(`proposal.md:83`, memory `critique-repeats-error`), 而这个承重清单自己没写计数法。
**怎么会红**: 复核者数 deliverables 得 10, 与「8 个已知文件落点必须在最终清单内」对不上, 判 Spec 错。
**introduced_by_r3fix**: 否 (8 是 R2-fix 写的; R3-fix 在其上加了第 9 项而未复核基数)。

---

### F-8 🟡 **minor** — `tasks.md:63` 组 1 标题「组 0 全绿后」与 DAG 直接矛盾, 而 CHECK6 结构上看不到组标题散文

**locator**: `tasks.md:63` (逐字 `## 组 1 — 实现 (组 0 全绿后; 组内先后以 DAG 为准)`) · `xcheck.py` CHECK6
**实跑**:
```
TG-0 成员是否都是 TG-1 全体的祖先?
   TASK-005 缺: ['TASK-002']
   TASK-006 缺: ['TASK-002', 'TASK-003', 'TASK-004']
   TASK-007 缺: ['TASK-002', 'TASK-003', 'TASK-004']
   TASK-008 缺: ['TASK-002']
   TASK-009 缺: ['TASK-002']
   TASK-010 缺: ['TASK-002', 'TASK-003', 'TASK-004']
```
⇒ 合法拓扑序可把 TASK-006 排在 TASK-002/003/004 之前, 「组 0 全绿后」不成立。R3-fix 用 `tasks.md:18` 的 SOT 声明 + CHECK6 处置了这个类, 但 **CHECK6 只比较 `dependencies` 两端的 `task_group` 数值**, 对组**标题**里的顺序承诺天然失明 —— 而 R3/tech-lead 原始诊断逐字就是「**本文件的组标题逐字承诺了组序**」。缓解: `:18` 与 `:24` 两处声明确实覆写了它, 故只判 minor。
**怎么会红**: 跑 Kahn 拓扑取任一含 `TASK-006 < TASK-002` 的合法序。
**introduced_by_r3fix**: 否。

---

## 5. 「本轮 fix 引入」的量化 (两种口径, 并列写出)

| 口径 | 总体 | 计数法 | 引入 / 总数 | 比例 |
|---|---|---|---|---|
| **全部 findings** | 本报告 8 条 | `introduced_by_r3fix == true` 的条数 | **4 / 8** (F-1, F-4, F-5, F-6) | **50%** |
| **仅三件套产物缺陷** (剔除 F-4/F-5/F-6 这三条对机制的) | 本报告 5 条 | 同上 | **1 / 5** (F-1) | **20%** |

历史序列 (取自 R2/R3 aggregate, 同为「本轮 fix 引入占比」口径):
`post_spec R1–R5 73–100% → post_planning R1→R2 53% → R2→R3 70% → R3→R4 **50% (全口径) / 20% (产物口径)**`

**诚实判定**: 任务书的判据是「**低于 50%** 才说明那道机械检查真的起作用了」。全口径 **恰好 50%, 不低于** ⇒ **按字面判据不成立**。
但两个方向的信号必须并列, 否则是选择性读数:
- ✅ **Critical 由 2 降到 1; 三件套产物本身的新引入率从 70% 降到 20%; R2 与 R3 的旧条目零复发** —— 这是八轮以来第一次;
- 🔴 **本轮 4 条新引入里有 3 条 (F-4/F-5/F-6) 是那道机械检查自己的覆盖缺口**, 且其中 F-4 让 R2 自己那条 Major 放回去仍绿, F-5 恰好放过本轮新造的那类移交。**「加一道机械检查」这个处方每加强一次, 就把缺陷推到它新的覆盖边界上** —— 与 memory `marginal-return-negative`「每件新手段 = 新表面」逐字吻合。

⇒ 我的读法: **换人执笔 + 机械交叉检查这两件手段, 对「产物缺陷」是有效的 (70% → 20%)**; 而**对「手段自身的覆盖边界」不可能自证** —— 那需要一个不共享其词表的外部构造者, 也就是本轮我做的事。这一点值得写进 handoff 作为方法论结论, 与「该不该再加一轮」分开决策。

---

## 6. 阻塞 Phase B 的条目 (3 条)

| # | 条目 | 理由 |
|---|---|---|
| F-1 | TASK-017 gitlink 判据不可求值 / 求值即造 orphan | Critical; 两实施者相反结果, 错的一支 = Aria #165 同族生产事故 |
| F-2 | CLAUDE.md 规则 #8 未同步 TASK-020 的第四条阻断行为 | 违反不可协商规则 #3, 且无任务承接、DAG 上无序 |
| F-3 | 模板 legacy 键名面零机械断言 | 唯一受众在仓外的落点, 全套 SC 对其失明 |

按 CLAUDE.md 规则 #10, 上述阻断不得由 AI 自行豁免。

---

## 7. 我认为不该再报的 (防下一轮重复劳动)

- **TASK-021 的收口完整性** —— 已实跑证实其依赖闭包覆盖全部交付 SC 断言面文件的任务, 三条无序任务无一交付该类文件。**这是本 Spec 最扎实的一处结构性修复, 不要再动它**;
- **TASK-014 停止预写量** —— 我判定它是**诚实标注而非变相回避**: `grep -cE '^#### +TASK-014 验收判据' proposal.md` 今日实跑 = 0 是一条真红且不预设 F 形状, 残余部分被明确标为 owner 裁量项。这是本 Spec 八轮里第一次选择「诚实交付一半」而不是造第五个假量 (memory `knob-granularity` 的正确形状);
- **`metadata.scope_repos[Aria].head = 7582238` 不等于当前 HEAD** —— `head_semantics` 已自陈它是行锚复核基线而非新鲜度断言, 且我复跑三条主仓行锚 (`README.md:8` badge / `config.template.json:75` / `:78`) **全部仍命中**。按 memory `false_green_dual_is_permanent_red`, 把它做成 `head == git rev-parse HEAD` 才是恒红。**不要把它当缺陷报。**

---

## 8. 席位结论

**VOTE: REVISE · VERDICT: FAIL (1C + 5M + 2m, 3 条阻塞)**

R2 与 R3 的旧条目**确已闭合且经我回源核验**, 这是八轮以来第一次。产物侧的新引入率降到 20%。
但仍有一条 Critical (F-1) 是「只修实例不修类」在**关闭该类的同一轮、由同一执笔者、在相邻两条任务上**的复发; 且本轮的核心处方 —— 那道机械交叉检查 —— 在我 8 个独立构造下**放行 4 个, 其中一个就是 R2 自己那条 Major**。

`converged: null` (单席无权判收敛)。
